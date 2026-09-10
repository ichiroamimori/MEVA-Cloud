/* Shared entry point for the independent browser MuJoCo Robot Viewer. */
window.launchRobotViewer = function(registration, motion, button, status) {
  const variant = registration?.variant?.id;
  if (!variant || !registration.manufacturer_id || !registration.robot_id) {
    status.textContent = "Robot variant を選択してください。";
    return;
  }
  const hasMotion = Boolean(
    motion?.capsule_id && motion?.run_id && motion.run_id !== "new",
  );
  const query = new URLSearchParams({
    robot_variant: variant,
    manufacturer: registration.manufacturer_id,
    robot_id: registration.robot_id,
    pose: hasMotion ? "motion" : "model_default",
    source_screen: status?.id === "dataRobotViewerStatus" ? "view_data" : "ik_retargeting",
  });
  if (hasMotion) {
    query.set("capsule_id", motion.capsule_id);
    query.set("run_id", motion.run_id);
    query.set("stage", motion.stage || "primary");
    query.set("main_id", motion.main_id || "legacy");
  }
  const opened = window.open(`/robot-viewer/?${query}`, "_blank");
  if (opened) opened.opener = null;
  status.textContent = opened
    ? "Browser Robot Viewerを新しいtabで開きました。"
    : "Viewer tabを開けませんでした。ブラウザのpopup設定を確認してください。";
};
