const params = new URLSearchParams(window.location.search);
const capsuleId = params.get("id") || "CAP-BON-001";
const capsuleTitle = params.get("title") || "盆踊り";

document.getElementById("capsuleId").textContent = capsuleId;
document.getElementById("capsuleTitle").textContent = capsuleTitle;
document.getElementById("crumbTitle").textContent = capsuleTitle;
document.title = `${capsuleTitle} | MEVA Cloud`;

const retargetUrl = new URL("../retarget/", window.location.href);
retargetUrl.searchParams.set("capsule", capsuleId);
retargetUrl.searchParams.set("title", capsuleTitle);
document.getElementById("retargetLink").href = retargetUrl.toString();
