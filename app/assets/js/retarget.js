(() => {
  "use strict";

  const LOCAL_USER_ID = "local_user";

  const robotSelect = document.getElementById("robotSelect");
  const variantSelect = document.getElementById("variantSelect");
  const robotManufacturer = document.getElementById("robotManufacturer");
  const variantDetail = document.getElementById("variantDetail");
  const mappingTitle = document.getElementById("mappingTitle");
  const capsuleIdElement = document.getElementById("capsuleId");
  const capsuleBack = document.getElementById("capsuleBack");
  const retargetLead = document.getElementById("retargetLead");
  const notice = document.getElementById("notice");
  const continueBtn = document.getElementById("continueBtn");

  const params = new URLSearchParams(window.location.search);

  // Both forms are accepted during the prototype phase:
  //   ?capsule=2606050000
  //   ?id=2606050000
  const capsuleId = params.get("capsule") || params.get("id");

  let robotCatalog = null;
  let currentManifest = null;
  let capsule = null;

  async function loadJson(url) {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`${url} -> HTTP ${response.status}`);
    }
    return response.json();
  }

  async function fileExists(url) {
    // GET is used instead of HEAD because python -m http.server
    // and future storage layers may not treat HEAD uniformly.
    const response = await fetch(url, {
      method: "GET",
      cache: "no-store"
    });
    return response.ok;
  }

  function setNotice(message, isError = false) {
    if (!notice) return;
    notice.textContent = message;
    notice.style.color = isError ? "#b42318" : "";
  }

  function basename(path) {
    if (!path) return "";
    return path.split("/").filter(Boolean).pop() || path;
  }

  function getSourceMotionBox() {
    const fields = [...document.querySelectorAll(".field")];
    return fields.find((field) => {
      const label = field.querySelector("label");
      return label?.dataset?.i18n === "app.source_motion";
    }) || null;
  }

  function updateSourceMotionUI(metadata, csvAvailable) {
    const field = getSourceMotionBox();
    if (!field) return;

    const title = field.querySelector(".status-title");
    const note = field.querySelector(".status-note");
    const badge = field.querySelector(".badge");

    const source = metadata?.meva_source || {};
    const filename = basename(source.file);

    if (title) {
      title.textContent = filename || "MEVA source data";
      title.removeAttribute("data-i18n");
    }

    const subject = metadata?.subject || {};
    const recording = metadata?.recording || {};

    const details = [];
    if (metadata?.title) details.push(metadata.title);

    const subjectParts = [];
    if (subject.id) subjectParts.push(subject.id);
    if (subject.height_m !== "" && subject.height_m != null) {
      subjectParts.push(`${Math.round(Number(subject.height_m) * 100)} cm`);
    }
    if (subject.weight_kg !== "" && subject.weight_kg != null) {
      subjectParts.push(`${subject.weight_kg} kg`);
    }
    if (subject.gender) subjectParts.push(subject.gender);

    if (subjectParts.length) details.push(subjectParts.join(" / "));

    if (recording.recorded_at) {
      details.push(recording.recorded_at.replace("T", " "));
    }

    if (note) {
      note.textContent = details.join(" · ") || "Capsule内のMEVA CSVを使用します。";
      note.removeAttribute("data-i18n");
    }

    if (badge) {
      badge.textContent = csvAvailable ? "Available" : "Missing";
      badge.removeAttribute("data-i18n");
      badge.classList.toggle("badge-gray", !csvAvailable);
    }
  }

  async function loadCapsule() {
    if (!capsuleId) {
      throw new Error(
        "Capsule IDがURLにありません。?capsule=2606050000 の形式で開いてください。"
      );
    }

    const basePath =
      `/workspace/users/${LOCAL_USER_ID}/capsules/${encodeURIComponent(capsuleId)}`;

    const metadataUrl = `${basePath}/metadata.json`;
    const metadata = await loadJson(metadataUrl);

    const sourceFile = metadata?.meva_source?.file || "";
    const isCsv =
      metadata?.meva_source?.format?.toLowerCase() === "csv" ||
      sourceFile.toLowerCase().endsWith(".csv");

    if (!sourceFile) {
      throw new Error("metadata.json に meva_source.file がありません。");
    }

    if (!isCsv) {
      throw new Error(
        `MEVAソースデータがCSVではありません: ${sourceFile}`
      );
    }

    const csvUrl = `${basePath}/${sourceFile.replace(/^\/+/, "")}`;
    const csvAvailable = await fileExists(csvUrl);

    capsule = {
      id: capsuleId,
      basePath,
      metadata,
      csvUrl,
      csvAvailable
    };

    if (capsuleIdElement) {
      capsuleIdElement.textContent = capsuleId;
    }

    if (capsuleBack) {
      capsuleBack.href = `../capsule/?capsule=${encodeURIComponent(capsuleId)}`;
      capsuleBack.textContent = metadata.title || "Capsule";
    }

    if (retargetLead) {
      const title = metadata.title || capsuleId;
      retargetLead.textContent =
        `${title} のMEVAソースデータをロボットモーションへ変換します。`;
    }

    updateSourceMotionUI(metadata, csvAvailable);

    if (!csvAvailable) {
      throw new Error(`MEVA CSVが見つかりません: ${csvUrl}`);
    }

    return capsule;
  }

  function populateRobotSelect() {
    const robots = (robotCatalog?.robots || []).filter(
      (robot) => robot.enabled !== false
    );

    robotSelect.innerHTML = "";

    if (!robots.length) {
      const option = document.createElement("option");
      option.value = "";
      option.textContent = "No robots available";
      robotSelect.appendChild(option);
      robotSelect.disabled = true;
      return;
    }

    robots.forEach((robot) => {
      const option = document.createElement("option");
      option.value = robot.robot_id;
      option.textContent = robot.robot_name;
      option.dataset.manifest = robot.manifest;
      option.dataset.manufacturer = robot.manufacturer_name || "";
      robotSelect.appendChild(option);
    });

    robotSelect.disabled = false;
  }

  function populateVariantSelect(manifest) {
    const variants = (manifest?.variants || []).filter(
      (variant) => variant.enabled !== false
    );

    variantSelect.innerHTML = "";

    if (!variants.length) {
      const option = document.createElement("option");
      option.value = "";
      option.textContent = "No variants available";
      variantSelect.appendChild(option);
      variantSelect.disabled = true;
      updateVariantDetail();
      return;
    }

    variants.forEach((variant) => {
      const option = document.createElement("option");
      option.value = variant.id;
      option.textContent =
        variant.name ||
        variant.short_name ||
        variant.id;
      variantSelect.appendChild(option);
    });

    variantSelect.disabled = false;
    updateVariantDetail();
  }

  function selectedRobot() {
    const robotId = robotSelect.value;
    return (robotCatalog?.robots || []).find(
      (robot) => robot.robot_id === robotId
    );
  }

  function selectedVariant() {
    const variantId = variantSelect.value;
    return (currentManifest?.variants || []).find(
      (variant) => variant.id === variantId
    );
  }

  function updateVariantDetail() {
    const variant = selectedVariant();

    if (!variant) {
      variantDetail.textContent = "";
      updateMappingTitle();
      return;
    }

    const bits = [];
    if (variant.dof != null) bits.push(`${variant.dof} DoF`);
    if (variant.model?.format) bits.push(variant.model.format);
    if (variant.model?.file) bits.push(variant.model.file);

    variantDetail.textContent = bits.join(" · ");
    updateMappingTitle();
  }

  function updateMappingTitle() {
    if (!mappingTitle) return;

    const robot = selectedRobot();
    const variant = selectedVariant();

    if (!robot) {
      mappingTitle.textContent = "MEVA → —";
      return;
    }

    const target =
      variant?.short_name
        ? `${robot.robot_name} ${variant.short_name}`
        : variant?.name || robot.robot_name;

    mappingTitle.textContent = `MEVA → ${target}`;
  }

  async function loadSelectedRobotManifest() {
    const option = robotSelect.selectedOptions[0];

    if (!option?.dataset?.manifest) {
      currentManifest = null;
      variantSelect.innerHTML =
        '<option value="">Select a robot first</option>';
      variantSelect.disabled = true;
      robotManufacturer.textContent = "";
      variantDetail.textContent = "";
      updateMappingTitle();
      return;
    }

    robotManufacturer.textContent =
      option.dataset.manufacturer || "";

    const manifestUrl =
      `/server/robots/${option.dataset.manifest.replace(/^\/+/, "")}`;

    currentManifest = await loadJson(manifestUrl);
    populateVariantSelect(currentManifest);
  }

  async function loadRobots() {
    robotCatalog = await loadJson("/server/robots/robots.json");
    populateRobotSelect();

    if (robotSelect.value) {
      await loadSelectedRobotManifest();
    }
  }

  robotSelect?.addEventListener("change", async () => {
    try {
      await loadSelectedRobotManifest();
    } catch (error) {
      console.error(error);
      setNotice(`Robot manifestの読み込みに失敗しました: ${error.message}`, true);
    }
  });

  variantSelect?.addEventListener("change", updateVariantDetail);

  continueBtn?.addEventListener("click", () => {
    const robot = selectedRobot();
    const variant = selectedVariant();

    if (!capsule?.csvAvailable) {
      setNotice("MEVAソースデータを確認できません。", true);
      return;
    }

    if (!robot || !variant) {
      setNotice("Target Robot と Robot model を選択してください。", true);
      return;
    }

    // Mapping画面は次の実装で接続する。
    setNotice(
      `準備OK: ${capsule.metadata.title || capsule.id} / ` +
      `${basename(capsule.metadata.meva_source.file)} / ` +
      `${robot.robot_name} ${variant.short_name || variant.name}`
    );
  });

  async function init() {
    const errors = [];

    try {
      await loadCapsule();
    } catch (error) {
      console.error("Capsule load error:", error);
      errors.push(error.message);
    }

    try {
      await loadRobots();
    } catch (error) {
      console.error("Robot catalog load error:", error);
      errors.push(error.message);
    }

    if (errors.length) {
      setNotice(errors.join(" / "), true);
    } else {
      setNotice("CapsuleとMEVAソースデータを認識しました。Mappingへ進む準備ができています。");
    }
  }

  init();
})();
