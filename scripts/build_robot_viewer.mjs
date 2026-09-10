import {build} from "esbuild";
import {copyFile, mkdir} from "node:fs/promises";

const output = "app/assets/robot-viewer";
await mkdir(output, {recursive: true});
await build({
  entryPoints: ["app/robot-viewer/browser-viewer.js"],
  bundle: true,
  format: "esm",
  minify: true,
  sourcemap: false,
  outfile: `${output}/browser-viewer.js`,
  target: ["chrome120", "edge120"],
  external: ["module"],
});
await copyFile("node_modules/@mujoco/mujoco/mujoco.wasm", `${output}/mujoco.wasm`);
