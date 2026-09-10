import * as THREE from "three";
import {OrbitControls} from "three/examples/jsm/controls/OrbitControls.js";
import loadMujoco from "@mujoco/mujoco";

const $ = id => document.getElementById(id);
const ui = {
  viewport: $("viewport"), loading: $("loading"), loadingText: $("loadingText"),
  errorPanel: $("errorPanel"), errorText: $("errorText"), retry: $("retryButton"),
  robotTitle: $("robotTitle"), pose: $("poseSelect"), play: $("playButton"),
  resetCamera: $("resetCameraButton"), selectedName: $("selectedName"),
  selectedDetail: $("selectedDetail"), selectionLabel: $("selectionLabel"),
  jointViz: $("jointVizToggle"), collision: $("collisionToggle"),
  transparent: $("transparentToggle"), labels: $("labelsToggle"),
  filter: $("filterInput"), list: $("structureList"), timeline: $("timeline"),
  frameText: $("frameText"), fpsText: $("fpsText"), warning: $("warningPanel"),
};

let app;
ui.retry.addEventListener("click", () => location.reload());

function fail(error, prefix = "") {
  console.error(error);
  ui.loading.hidden = true;
  ui.errorPanel.hidden = false;
  const message = error instanceof Error ? error.message : String(error);
  ui.errorText.textContent = `${prefix}${message}`;
}

function enumValue(value) {
  return typeof value === "object" && value !== null && "value" in value ? value.value : value;
}

function cleanParams() {
  const source = new URLSearchParams(location.search);
  const required = ["manufacturer", "robot_id", "robot_variant"];
  for (const name of required) if (!source.get(name)) throw new Error(`Viewer URLに ${name} がありません。`);
  const result = new URLSearchParams();
  for (const name of ["manufacturer", "robot_id", "robot_variant", "capsule_id", "run_id", "stage", "main_id", "user_id"])
    if (source.get(name)) result.set(name, source.get(name));
  return {api: result, source};
}

async function fetchJson(url) {
  const response = await fetch(url, {cache: "no-store"});
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(typeof body.detail === "string" ? body.detail : `${response.status} ${response.statusText}`);
  return body;
}

async function mapLimit(items, limit, worker) {
  let next = 0;
  async function run() {
    while (next < items.length) {
      const index = next++;
      await worker(items[index], index);
    }
  }
  await Promise.all(Array.from({length: Math.min(limit, items.length)}, run));
}

function parseViewerBin(buffer) {
  if (buffer.byteLength < 16) throw new Error("Motion data is empty or truncated.");
  const view = new DataView(buffer);
  const magic = new TextDecoder().decode(new Uint8Array(buffer, 0, 8));
  if (magic !== "MEVAVW01" && magic !== "MEVAVW02") throw new Error("Unsupported motion data format.");
  const fixed = magic === "MEVAVW02" ? 16 : 12;
  const formatVersion = magic === "MEVAVW02" ? view.getUint32(8, true) : null;
  const headerLength = view.getUint32(magic === "MEVAVW02" ? 12 : 8, true);
  if (fixed + headerLength > buffer.byteLength) throw new Error("Motion data header is truncated.");
  const header = JSON.parse(new TextDecoder().decode(new Uint8Array(buffer, fixed, headerLength)));
  if (formatVersion !== null && Number(header.format_version) !== formatVersion) throw new Error("Motion data version mismatch.");
  const arrays = {};
  const payloadStart = fixed + headerLength;
  for (const block of header.blocks || []) {
    const start = payloadStart + Number(block.offset);
    const end = start + Number(block.nbytes);
    if (start < payloadStart || end > buffer.byteLength) throw new Error(`Motion block is truncated: ${block.name}`);
    const bytes = buffer.slice(start, end);
    arrays[block.name] = block.dtype === "uint8" ? new Uint8Array(bytes) :
      block.dtype === "int32" ? new Int32Array(bytes) : new Float32Array(bytes);
  }
  return {header, arrays};
}

class RobotViewer {
  constructor(mujoco, config, sourceParams) {
    this.mujoco = mujoco;
    this.config = config;
    this.sourceParams = sourceParams;
    this.model = null;
    this.data = null;
    this.mjvOption = null;
    this.mjvPerturb = null;
    this.mjvCamera = null;
    this.mjvScene = null;
    this.renderer = null;
    this.camera = null;
    this.controls = null;
    this.scene = new THREE.Scene();
    this.geometryCache = new Map();
    this.renderObjects = [];
    this.bodyNames = [];
    this.jointNames = [];
    this.selected = null;
    this.activeTab = "bodies";
    this.motion = null;
    this.motionJointAddresses = [];
    this.freeQposAddress = -1;
    this.motionFrame = 0;
    this.playing = false;
    this.playStartedAt = 0;
    this.playStartedFrame = 0;
    this.raf = null;
    this.renderQueued = false;
    this.sceneDirty = true;
    this.lastUiUpdate = 0;
    this.warnings = new Set();
    this.raycaster = new THREE.Raycaster();
    this.pointer = new THREE.Vector2();
    this.bodyAxes = new THREE.AxesHelper(.13);
    this.jointAxis = new THREE.ArrowHelper(new THREE.Vector3(0, 0, 1), new THREE.Vector3(), .15, 0xf4cc52, .035, .018);
    this.scene.add(this.bodyAxes, this.jointAxis);
    this.bodyAxes.visible = false;
    this.jointAxis.visible = false;
  }

  async initialize() {
    await this.loadFilesAndModel();
    this.createScene();
    this.buildStructureUi();
    this.bindUi();
    await this.loadMotion();
    this.applyRequestedPose();
    this.resetCamera();
    ui.loading.hidden = true;
    this.requestRender();
  }

  async loadFilesAndModel() {
    const base = "/meva-robot";
    const totalBytes = this.config.files.reduce((sum, file) => sum + Number(file.size || 0), 0);
    let loadedBytes = 0;
    this.mujoco.FS.mkdirTree(base);
    await mapLimit(this.config.files, 6, async file => {
      const response = await fetch(file.url, {cache: "force-cache"});
      if (!response.ok) throw new Error(`Missing mesh / asset: ${file.path} (${response.status})`);
      const bytes = new Uint8Array(await response.arrayBuffer());
      const slash = file.path.lastIndexOf("/");
      if (slash >= 0) this.mujoco.FS.mkdirTree(`${base}/${file.path.slice(0, slash)}`);
      this.mujoco.FS.writeFile(`${base}/${file.path}`, bytes);
      loadedBytes += bytes.byteLength;
      ui.loadingText.textContent = `Robot assets ${Math.min(100, Math.round(loadedBytes / Math.max(1, totalBytes) * 100))}%`;
    });
    ui.loadingText.textContent = "MuJoCo modelをコンパイルしています…";
    try {
      this.model = this.mujoco.MjModel.from_xml_path(`${base}/${this.config.model_path}`);
    } catch (error) {
      throw new Error(`XML load error: ${error instanceof Error ? error.message : error}`);
    }
    if (!this.model) throw new Error("XML load error: MuJoCo did not create a model.");
    this.data = new this.mujoco.MjData(this.model);
    this.mjvOption = new this.mujoco.MjvOption();
    this.mjvPerturb = new this.mujoco.MjvPerturb();
    this.mjvCamera = new this.mujoco.MjvCamera();
    this.mjvScene = new this.mujoco.MjvScene(this.model, Math.max(4096, Number(this.model.ngeom || 0) * 8));
    this.mujoco.mj_forward(this.model, this.data);
    this.bodyNames = Array.from({length: Number(this.model.nbody)}, (_, id) => this.nameOf(this.mujoco.mjtObj.mjOBJ_BODY, id, `body_${id}`));
    this.jointNames = Array.from({length: Number(this.model.njnt)}, (_, id) => this.nameOf(this.mujoco.mjtObj.mjOBJ_JOINT, id, `joint_${id}`));
  }

  nameOf(type, id, fallback) {
    try { return this.mujoco.mj_id2name(this.model, enumValue(type), id) || fallback; }
    catch { return fallback; }
  }

  createScene() {
    let context;
    try {
      const test = document.createElement("canvas");
      context = test.getContext("webgl2") || test.getContext("webgl");
      if (!context) throw new Error("WebGL unavailable. Chrome / EdgeのGPU設定を確認してください。");
      this.renderer = new THREE.WebGLRenderer({antialias: true, powerPreference: "high-performance"});
    } catch (error) {
      throw new Error(`WebGL initialization failure: ${error instanceof Error ? error.message : error}`);
    }
    this.renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.5));
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.domElement.tabIndex = 0;
    ui.viewport.prepend(this.renderer.domElement);
    this.scene.background = new THREE.Color(0x10151a);
    this.camera = new THREE.PerspectiveCamera(42, 1, .01, 200);
    this.camera.up.set(0, 0, 1);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = false;
    this.controls.screenSpacePanning = true;
    this.controls.addEventListener("change", () => this.requestRender(false));
    this.scene.add(new THREE.HemisphereLight(0xe8f0f7, 0x222b32, 2.2));
    const key = new THREE.DirectionalLight(0xffffff, 2.5);
    key.position.set(-2, -3, 5);
    this.scene.add(key);
    this.resize();
    this.resizeObserver = new ResizeObserver(() => { this.resize(); this.requestRender(false); });
    this.resizeObserver.observe(ui.viewport);
    this.renderer.domElement.addEventListener("pointerdown", event => this.pointerDown = {x: event.clientX, y: event.clientY});
    this.renderer.domElement.addEventListener("pointerup", event => {
      if (this.pointerDown && Math.hypot(event.clientX - this.pointerDown.x, event.clientY - this.pointerDown.y) < 4) this.pick(event);
      this.pointerDown = null;
    });
  }

  resize() {
    const rect = ui.viewport.getBoundingClientRect();
    if (!this.renderer || rect.width < 1 || rect.height < 1) return;
    this.renderer.setSize(rect.width, rect.height, false);
    this.camera.aspect = rect.width / rect.height;
    this.camera.updateProjectionMatrix();
  }

  buildStructureUi() {
    document.querySelectorAll(".tabs button").forEach(button => button.addEventListener("click", () => {
      document.querySelectorAll(".tabs button").forEach(item => item.classList.toggle("active", item === button));
      this.activeTab = button.dataset.tab;
      this.refreshList();
    }));
    ui.filter.addEventListener("input", () => this.refreshList());
    this.refreshList();
  }

  refreshList() {
    const type = this.activeTab === "bodies" ? "body" : "joint";
    const names = type === "body" ? this.bodyNames : this.jointNames;
    const needle = ui.filter.value.trim().toLowerCase();
    const fragment = document.createDocumentFragment();
    names.forEach((name, id) => {
      if (needle && !name.toLowerCase().includes(needle)) return;
      const row = document.createElement("button");
      row.type = "button";
      row.className = `structure-row${this.selected?.type === type && this.selected.id === id ? " selected" : ""}`;
      row.textContent = name;
      const meta = document.createElement("small");
      meta.textContent = `#${id}`;
      row.appendChild(meta);
      row.addEventListener("click", () => this.select(type, id));
      fragment.appendChild(row);
    });
    ui.list.replaceChildren(fragment);
  }

  bindUi() {
    ui.resetCamera.addEventListener("click", () => this.resetCamera());
    ui.pose.addEventListener("change", () => this.applyPose(ui.pose.value));
    ui.play.addEventListener("click", () => this.setPlaying(!this.playing));
    ui.timeline.addEventListener("input", () => {
      this.setPlaying(false);
      this.applyMotionFrame(Number(ui.timeline.value));
    });
    ui.jointViz.addEventListener("change", () => { this.sceneDirty = true; this.requestRender(); });
    ui.collision.addEventListener("change", () => { this.sceneDirty = true; this.requestRender(); });
    ui.transparent.addEventListener("change", () => this.updateAppearance());
    ui.labels.addEventListener("change", () => { this.updateSelectionHelpers(); this.requestRender(false); });
    window.addEventListener("keydown", event => {
      if (event.code === "Space" && event.target?.tagName !== "INPUT") { event.preventDefault(); this.setPlaying(!this.playing); }
      if (event.key.toLowerCase() === "r") this.resetCamera();
    });
    window.addEventListener("pagehide", () => this.dispose(), {once: true});
  }

  async loadMotion() {
    const option = ui.pose.querySelector('option[value="motion"]');
    if (!this.config.motion_url) {
      option.disabled = true;
      return;
    }
    try {
      const response = await fetch(this.config.motion_url, {cache: "no-store"});
      if (!response.ok) {
        const detail = await response.json().catch(() => ({}));
        throw new Error(detail.detail || `${response.status} ${response.statusText}`);
      }
      this.motion = parseViewerBin(await response.arrayBuffer());
      if (this.motion.header.kind !== "retarget") throw new Error("Selected data is not Robot motion.");
      this.prepareMotionMapping();
      ui.timeline.max = Math.max(0, Number(this.motion.header.frame_count) - 1);
      ui.timeline.disabled = false;
      ui.play.disabled = false;
      ui.fpsText.textContent = `${this.motionFps().toFixed(2)} FPS`;
    } catch (error) {
      option.disabled = true;
      this.warn(`Motion load error: ${error instanceof Error ? error.message : error}`);
    }
  }

  motionFps() {
    const fps = Number(this.motion?.header?.fps);
    return Number.isFinite(fps) && fps > 0 ? fps : 30;
  }

  prepareMotionMapping() {
    const freeType = enumValue(this.mujoco.mjtJoint.mjJNT_FREE);
    this.freeQposAddress = -1;
    for (let id = 0; id < Number(this.model.njnt); id++) {
      if (Number(this.model.jnt_type[id]) === freeType) {
        this.freeQposAddress = Number(this.model.jnt_qposadr[id]);
        break;
      }
    }
    this.motionJointAddresses = (this.motion.header.joint_names || []).map(name => {
      const id = this.mujoco.mj_name2id(
        this.model, enumValue(this.mujoco.mjtObj.mjOBJ_JOINT), name,
      );
      return id >= 0 ? Number(this.model.jnt_qposadr[id]) : -1;
    });
  }

  applyRequestedPose() {
    const requested = this.sourceParams.get("pose");
    const requestedFrame = Number(this.sourceParams.get("frame"));
    if (requested === "standing") ui.pose.value = "standing";
    else if (requested === "motion" && this.motion) ui.pose.value = "motion";
    else ui.pose.value = "model_default";
    this.applyPose(ui.pose.value, Number.isFinite(requestedFrame) ? requestedFrame : 0);
  }

  applyPose(kind, frame = 0) {
    this.setPlaying(false);
    if (kind === "motion") {
      if (!this.motion) { this.warn("Motion data is unavailable."); ui.pose.value = "model_default"; return; }
      this.applyMotionFrame(frame);
      return;
    }
    if (kind === "standing") {
      if (!this.applyPoseDefinition(this.config.standing_pose, "Standing Pose")) {
        this.warn("Standing PoseはこのRobot manifestに定義されていません。");
        ui.pose.value = "model_default";
        this.applyPose("model_default");
      }
      return;
    }
    this.mujoco.mj_resetData(this.model, this.data);
    this.mujoco.mj_forward(this.model, this.data);
    this.motionFrame = 0;
    this.sceneDirty = true;
    this.updateMotionUi();
    this.requestRender();
  }

  applyPoseDefinition(definition, label) {
    if (!definition || typeof definition !== "object") return false;
    const type = definition.type || (Array.isArray(definition.qpos) ? "qpos" : "");
    try {
      if (type === "model_default") this.mujoco.mj_resetData(this.model, this.data);
      else if (type === "keyframe") {
        const id = this.mujoco.mj_name2id(this.model, enumValue(this.mujoco.mjtObj.mjOBJ_KEY), String(definition.name || ""));
        if (id < 0) throw new Error(`keyframe '${definition.name || ""}' not found`);
        this.mujoco.mj_resetDataKeyframe(this.model, this.data, id);
      } else if (type === "qpos") {
        if (!Array.isArray(definition.qpos) || definition.qpos.length !== Number(this.model.nq)) throw new Error(`invalid qpos length (expected ${this.model.nq})`);
        if (!definition.qpos.every(Number.isFinite)) throw new Error("qpos contains a non-finite value");
        this.mujoco.mj_resetData(this.model, this.data);
        this.data.qpos.set(definition.qpos);
      } else throw new Error(`unsupported pose type '${type}'`);
      this.mujoco.mj_forward(this.model, this.data);
      this.sceneDirty = true;
      this.requestRender();
      return true;
    } catch (error) {
      this.warn(`${label} load failure: ${error instanceof Error ? error.message : error}`);
      return false;
    }
  }

  applyMotionFrame(frame) {
    if (!this.motion) return;
    const count = Number(this.motion.header.frame_count);
    const index = Math.max(0, Math.min(count - 1, Math.round(frame)));
    const arrays = this.motion.arrays;
    const rootPos = arrays.root_pos;
    const rootQuat = arrays.root_rot;
    const dof = arrays.dof_pos;
    const jointNames = this.motion.header.joint_names || [];
    const qpos = this.data.qpos;
    qpos.set(this.model.qpos0);
    if (this.freeQposAddress >= 0) {
      const address = this.freeQposAddress;
      if (!rootPos || !rootQuat) { this.warn("Invalid qpos: motion root pose is missing."); return; }
      qpos[address] = rootPos[index * 3]; qpos[address + 1] = rootPos[index * 3 + 1]; qpos[address + 2] = rootPos[index * 3 + 2];
      const order = String(this.motion.header.root_rot_order || "wxyz").toLowerCase();
      if (order === "xyzw") {
        qpos[address + 3] = rootQuat[index * 4 + 3];
        qpos[address + 4] = rootQuat[index * 4]; qpos[address + 5] = rootQuat[index * 4 + 1]; qpos[address + 6] = rootQuat[index * 4 + 2];
      } else for (let axis = 0; axis < 4; axis++) qpos[address + 3 + axis] = rootQuat[index * 4 + axis];
    }
    if (!dof || dof.length < count * jointNames.length) { this.warn("Invalid qpos: motion joint data is missing."); return; }
    for (let column = 0; column < jointNames.length; column++) if (this.motionJointAddresses[column] >= 0)
      qpos[this.motionJointAddresses[column]] = dof[index * jointNames.length + column];
    for (let i = 0; i < qpos.length; i++) if (!Number.isFinite(qpos[i])) { this.warn(`Invalid qpos at index ${i}.`); return; }
    this.mujoco.mj_forward(this.model, this.data);
    this.motionFrame = index;
    this.sceneDirty = true;
    const now = performance.now();
    if (!this.playing || now - this.lastUiUpdate >= 100) {
      this.lastUiUpdate = now;
      this.updateMotionUi();
    }
    this.requestRender();
  }

  setPlaying(value) {
    if (!this.motion || ui.pose.value !== "motion") value = false;
    this.playing = Boolean(value);
    ui.play.textContent = this.playing ? "PAUSE" : "PLAY";
    if (this.playing) {
      this.playStartedAt = performance.now();
      this.playStartedFrame = this.motionFrame;
      this.requestRender();
    }
  }

  updateMotionUi() {
    ui.timeline.value = String(this.motionFrame);
    ui.frameText.textContent = this.motion ? `FRAME ${this.motionFrame + 1} / ${this.motion.header.frame_count}` : "FRAME —";
  }

  requestRender(updateScene = true) {
    if (updateScene) this.sceneDirty = true;
    if (this.raf === null) this.raf = requestAnimationFrame(time => {
      try { this.tick(time); }
      catch (error) { this.setPlaying(false); fail(error, "Rendering error: "); }
    });
  }

  tick(time) {
    this.raf = null;
    if (this.playing) {
      const count = Number(this.motion.header.frame_count);
      const elapsedFrames = Math.floor((time - this.playStartedAt) * this.motionFps() / 1000);
      const frame = (this.playStartedFrame + elapsedFrames) % count;
      if (frame !== this.motionFrame) this.applyMotionFrame(frame);
    }
    if (this.sceneDirty) this.updateMuJoCoScene();
    this.updateSelectionHelpers();
    this.renderer.render(this.scene, this.camera);
    if (this.playing) this.requestRender(false);
  }

  geometryFor(geom) {
    const type = Number(geom.type);
    let dataId = Number(geom.dataid);
    const objectId = Number(geom.objid);
    if (
      type === enumValue(this.mujoco.mjtGeom.mjGEOM_MESH)
      && Number(geom.objtype) === enumValue(this.mujoco.mjtObj.mjOBJ_GEOM)
      && objectId >= 0 && objectId < Number(this.model.ngeom)
    ) dataId = Number(this.model.geom_dataid[objectId]);
    const size = Array.from(geom.size || []);
    const key = `${type}:${dataId}:${size.map(value => Number(value).toPrecision(7)).join(",")}`;
    if (this.geometryCache.has(key)) return {key, geometry: this.geometryCache.get(key)};
    const g = this.mujoco.mjtGeom;
    let geometry;
    if (type === enumValue(g.mjGEOM_PLANE)) geometry = new THREE.PlaneGeometry(Math.min(20, 2 * (size[0] || 10)), Math.min(20, 2 * (size[1] || 10)));
    else if (type === enumValue(g.mjGEOM_SPHERE)) geometry = new THREE.SphereGeometry(size[0], 24, 16);
    else if (type === enumValue(g.mjGEOM_CAPSULE)) { geometry = new THREE.CapsuleGeometry(size[0], 2 * size[2], 8, 16); geometry.rotateX(Math.PI / 2); }
    else if (type === enumValue(g.mjGEOM_BOX)) geometry = new THREE.BoxGeometry(2 * size[0], 2 * size[1], 2 * size[2]);
    else if (type === enumValue(g.mjGEOM_CYLINDER)) { geometry = new THREE.CylinderGeometry(size[0], size[0], 2 * size[2], 24); geometry.rotateX(Math.PI / 2); }
    else if (type === enumValue(g.mjGEOM_ELLIPSOID)) { geometry = new THREE.SphereGeometry(1, 24, 16); geometry.scale(size[0], size[1], size[2]); }
    else if (type === enumValue(g.mjGEOM_MESH)) geometry = this.meshGeometry(dataId);
    else if ([g.mjGEOM_ARROW, g.mjGEOM_ARROW1, g.mjGEOM_ARROW2, g.mjGEOM_LINE].some(value => type === enumValue(value))) {
      geometry = new THREE.CylinderGeometry(Math.max(.001, size[0]), Math.max(.001, size[0]), Math.max(.001, 2 * size[2]), 10);
      geometry.rotateX(Math.PI / 2);
    }
    else {
      geometry = new THREE.BufferGeometry();
      this.warn(`Unsupported MuJoCo geometry type ${type} is hidden.`);
    }
    this.geometryCache.set(key, geometry);
    return {key, geometry};
  }

  meshGeometry(id) {
    if (id < 0 || id >= Number(this.model.nmesh)) {
      this.warn(`MuJoCo decoration mesh ${id} is outside the model mesh table and was hidden.`);
      return new THREE.BufferGeometry();
    }
    const vertexAddress = Number(this.model.mesh_vertadr[id]);
    const vertexCount = Number(this.model.mesh_vertnum[id]);
    const faceAddress = Number(this.model.mesh_faceadr[id]);
    const faceCount = Number(this.model.mesh_facenum[id]);
    if (!vertexCount || !faceCount) throw new Error(`Unsupported asset: mesh ${id} has no triangles`);
    const positions = new Float32Array(vertexCount * 3);
    for (let i = 0; i < positions.length; i++) positions[i] = this.model.mesh_vert[vertexAddress * 3 + i];
    const indices = new Uint32Array(faceCount * 3);
    for (let i = 0; i < indices.length; i++) indices[i] = this.model.mesh_face[faceAddress * 3 + i];
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    geometry.setIndex(new THREE.BufferAttribute(indices, 1));
    geometry.computeVertexNormals();
    geometry.computeBoundingSphere();
    return geometry;
  }

  updateMuJoCoScene() {
    const jointFlag = enumValue(this.mujoco.mjtVisFlag.mjVIS_JOINT);
    this.mjvOption.flags[jointFlag] = ui.jointViz.checked ? 1 : 0;
    if (this.mjvOption.geomgroup?.length > 3) this.mjvOption.geomgroup[3] = ui.collision.checked ? 1 : 0;
    this.mujoco.mjv_updateScene(this.model, this.data, this.mjvOption, this.mjvPerturb, this.mjvCamera, enumValue(this.mujoco.mjtCatBit.mjCAT_ALL), this.mjvScene);
    const geoms = this.mjvScene.geoms;
    let count = 0;
    let appearanceChanged = false;
    try {
      count = geoms.size();
      for (let i = 0; i < count; i++) {
        const geom = geoms.get(i);
        if (!geom) continue;
        try {
          const descriptor = this.geometryFor(geom);
          let object = this.renderObjects[i];
          if (!object) {
            object = new THREE.Mesh(descriptor.geometry, new THREE.MeshPhongMaterial({side: THREE.FrontSide}));
            object.matrixAutoUpdate = false;
            this.renderObjects[i] = object;
            this.scene.add(object);
          } else if (object.userData.geometryKey !== descriptor.key) object.geometry = descriptor.geometry;
          object.userData.geometryKey = descriptor.key;
          object.userData.objtype = Number(geom.objtype);
          object.userData.objid = Number(geom.objid);
          object.visible = descriptor.geometry.getAttribute("position") !== undefined;
          object.matrix.set(
            geom.mat[0], geom.mat[1], geom.mat[2], geom.pos[0],
            geom.mat[3], geom.mat[4], geom.mat[5], geom.pos[1],
            geom.mat[6], geom.mat[7], geom.mat[8], geom.pos[2],
            0, 0, 0, 1,
          );
          object.matrixWorldNeedsUpdate = true;
          const material = object.material;
          const rgbaKey = `${geom.rgba[0]},${geom.rgba[1]},${geom.rgba[2]},${geom.rgba[3]},${geom.shininess}`;
          if (material.userData.rgbaKey !== rgbaKey) {
            material.userData.rgbaKey = rgbaKey;
            material.color.setRGB(geom.rgba[0], geom.rgba[1], geom.rgba[2], THREE.SRGBColorSpace);
            material.userData.baseOpacity = Number(geom.rgba[3]);
            material.shininess = Math.max(8, Number(geom.shininess || 0) * 128);
            appearanceChanged = true;
          }
        } finally { geom.delete(); }
      }
    } finally { geoms.delete(); }
    for (let i = count; i < this.renderObjects.length; i++) this.renderObjects[i].visible = false;
    this.sceneDirty = false;
    if (appearanceChanged) this.updateAppearance(false);
  }

  updateAppearance(schedule = true) {
    const opacityScale = ui.transparent.checked ? .34 : 1;
    for (const object of this.renderObjects) {
      if (!object) continue;
      const opacity = (object.material.userData.baseOpacity ?? 1) * opacityScale;
      object.material.opacity = opacity;
      object.material.transparent = opacity < .999;
      object.material.depthWrite = opacity >= .999;
      object.material.needsUpdate = true;
    }
    if (schedule) this.requestRender(false);
  }

  pick(event) {
    const rect = this.renderer.domElement.getBoundingClientRect();
    this.pointer.set((event.clientX - rect.left) / rect.width * 2 - 1, -(event.clientY - rect.top) / rect.height * 2 + 1);
    this.raycaster.setFromCamera(this.pointer, this.camera);
    const hit = this.raycaster.intersectObjects(this.renderObjects.filter(item => item?.visible), false)[0];
    if (!hit) return;
    const objectType = hit.object.userData.objtype;
    const objectId = hit.object.userData.objid;
    if (objectType === enumValue(this.mujoco.mjtObj.mjOBJ_GEOM) && objectId >= 0) {
      const body = Number(this.model.geom_bodyid[objectId]);
      this.select("body", body);
    } else if (objectType === enumValue(this.mujoco.mjtObj.mjOBJ_JOINT) && objectId >= 0) this.select("joint", objectId);
  }

  select(type, id) {
    this.selected = {type, id};
    const name = type === "body" ? this.bodyNames[id] : this.jointNames[id];
    ui.selectedName.textContent = name || `${type}_${id}`;
    if (type === "joint") {
      const jointType = Number(this.model.jnt_type[id]);
      const parentBody = Number(this.model.jnt_bodyid[id]);
      ui.selectedDetail.textContent = `Joint #${id} · Body: ${this.bodyNames[parentBody]} · Type: ${this.jointTypeName(jointType)}`;
    } else {
      const parent = Number(this.model.body_parentid[id]);
      ui.selectedDetail.textContent = `Body / Link #${id} · Parent: ${this.bodyNames[parent] || "world"}`;
    }
    this.refreshList();
    this.updateSelectionHelpers();
    this.requestRender(false);
  }

  jointTypeName(type) {
    const kinds = this.mujoco.mjtJoint;
    for (const [name, value] of Object.entries(kinds)) if (enumValue(value) === type) return name.replace("mjJNT_", "");
    return String(type);
  }

  updateSelectionHelpers() {
    this.bodyAxes.visible = false;
    this.jointAxis.visible = false;
    ui.selectionLabel.hidden = true;
    if (!this.selected) return;
    let position;
    if (this.selected.type === "body") {
      const id = this.selected.id;
      position = new THREE.Vector3(this.data.xpos[id * 3], this.data.xpos[id * 3 + 1], this.data.xpos[id * 3 + 2]);
      this.bodyAxes.position.copy(position);
      const matrix = this.data.xmat;
      const rotation = new THREE.Matrix4().set(
        matrix[id * 9], matrix[id * 9 + 1], matrix[id * 9 + 2], 0,
        matrix[id * 9 + 3], matrix[id * 9 + 4], matrix[id * 9 + 5], 0,
        matrix[id * 9 + 6], matrix[id * 9 + 7], matrix[id * 9 + 8], 0,
        0, 0, 0, 1,
      );
      this.bodyAxes.quaternion.setFromRotationMatrix(rotation);
      this.bodyAxes.visible = true;
    } else {
      const id = this.selected.id;
      position = new THREE.Vector3(this.data.xanchor[id * 3], this.data.xanchor[id * 3 + 1], this.data.xanchor[id * 3 + 2]);
      const direction = new THREE.Vector3(this.data.xaxis[id * 3], this.data.xaxis[id * 3 + 1], this.data.xaxis[id * 3 + 2]).normalize();
      this.jointAxis.position.copy(position);
      this.jointAxis.setDirection(direction);
      this.jointAxis.visible = ui.jointViz.checked;
    }
    if (ui.labels.checked && position) {
      const projected = position.clone().project(this.camera);
      const rect = this.renderer.domElement.getBoundingClientRect();
      if (projected.z >= -1 && projected.z <= 1) {
        ui.selectionLabel.textContent = this.selected.type === "body" ? this.bodyNames[this.selected.id] : this.jointNames[this.selected.id];
        ui.selectionLabel.style.left = `${(projected.x * .5 + .5) * rect.width + 8}px`;
        ui.selectionLabel.style.top = `${(-projected.y * .5 + .5) * rect.height - 12}px`;
        ui.selectionLabel.hidden = false;
      }
    }
  }

  resetCamera() {
    if (!this.model || !this.camera) return;
    const points = [];
    for (let id = 1; id < Number(this.model.nbody); id++) points.push(new THREE.Vector3(this.data.xpos[id * 3], this.data.xpos[id * 3 + 1], this.data.xpos[id * 3 + 2]));
    const box = new THREE.Box3().setFromPoints(points);
    const center = box.getCenter(new THREE.Vector3());
    const size = Math.max(.5, box.getSize(new THREE.Vector3()).length());
    this.controls.target.copy(center);
    this.camera.position.set(center.x + size * 1.25, center.y - size * 1.8, center.z + size * .65);
    this.camera.near = Math.max(.005, size / 1000);
    this.camera.far = Math.max(50, size * 30);
    this.camera.updateProjectionMatrix();
    this.controls.update();
    this.requestRender(false);
  }

  warn(message) {
    this.warnings.add(message);
    ui.warning.hidden = false;
    ui.warning.textContent = [...this.warnings].join("\n");
  }

  dispose() {
    if (this.raf !== null) cancelAnimationFrame(this.raf);
    this.resizeObserver?.disconnect();
    this.controls?.dispose();
    for (const object of this.renderObjects) object?.material?.dispose();
    for (const geometry of this.geometryCache.values()) geometry.dispose();
    this.renderer?.dispose();
    for (const value of [this.mjvScene, this.mjvCamera, this.mjvPerturb, this.mjvOption, this.data, this.model]) value?.delete();
  }
}

async function main() {
  try {
    const {api, source} = cleanParams();
    ui.loadingText.textContent = "Robot configurationを取得しています…";
    const config = await fetchJson(`/api/retarget/robots/viewer/browser/config?${api}`);
    ui.robotTitle.textContent = `${config.robot.robot_name} / ${config.robot.variant_name}`;
    document.title = `${config.robot.variant_name} — Robot Viewer`;
    if (!config.standing_pose) ui.pose.querySelector('option[value="standing"]').textContent = "STANDING POSE (UNDEFINED)";
    ui.loadingText.textContent = "MuJoCo WASM を初期化しています…";
    let mujoco;
    try {
      mujoco = await loadMujoco({locateFile: path => path.endsWith(".wasm") ? "/assets/robot-viewer/mujoco.wasm" : path});
    } catch (error) {
      throw new Error(`MuJoCo WASM initialization failure: ${error instanceof Error ? error.message : error}`);
    }
    app = new RobotViewer(mujoco, config, source);
    await app.initialize();
  } catch (error) { fail(error); }
}

main();
