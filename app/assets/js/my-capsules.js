(() => {
  "use strict";

  const LOCAL_USER_ID = "local_user";

  // Prototype: fixed Capsule IDs.
  // Later this will be replaced by an API / database query.
  const FIXED_CAPSULE_IDS = [
    "2606050001"
  ];

  const grid = document.getElementById("capsuleGrid");

  async function loadJson(url) {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`${url} -> HTTP ${response.status}`);
    }
    return response.json();
  }

  function formatDate(metadata) {
    const date =
      metadata?.recording?.date ||
      metadata?.recording?.recorded_at?.slice(0, 10) ||
      metadata?.created_at?.slice(0, 10) ||
      "";

    return date ? date.replaceAll("-", "/") : "";
  }

  function basename(path) {
    if (!path) return "";
    return path.split("/").filter(Boolean).pop() || path;
  }

  function buildDescription(metadata) {
    const filename = basename(metadata?.meva_source?.file);
    if (filename) {
      return `MEVAソースデータ: ${filename}`;
    }
    return "MEVAソースデータ";
  }

  function buildModalities(metadata) {
    const result = ["MEVA"];

    const format = metadata?.meva_source?.format;
    if (format) {
      result.push(String(format).toUpperCase());
    }

    return [...new Set(result)];
  }

  function createCard(capsuleId, metadata) {
    const capsule = {
      id: capsuleId,
      title: metadata?.title || capsuleId,
      date: formatDate(metadata),
      description: buildDescription(metadata),
      modalities: buildModalities(metadata)
    };

    const card = document.createElement("article");
    card.className = "capsule-card";
    card.tabIndex = 0;

    card.innerHTML = `
      <div class="card-top">
        <div>
          <div class="card-kicker">${capsule.id}</div>
          <div class="card-title">${capsule.title}</div>
        </div>
        <div class="card-meta">${capsule.date}</div>
      </div>
      <div class="card-meta">${capsule.description}</div>
      <div class="card-footer">
        ${capsule.modalities
          .map((m) => `<span class="badge">${m}</span>`)
          .join("")}
      </div>
    `;

    const open = () => {
      const url = new URL("capsule/", window.location.href);

      // capsule.js currently accepts id/title.
      url.searchParams.set("id", capsule.id);
      url.searchParams.set("title", capsule.title);

      window.location.href = url.toString();
    };

    card.addEventListener("click", open);
    card.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        open();
      }
    });

    return card;
  }

  function createErrorCard(capsuleId, error) {
    const card = document.createElement("article");
    card.className = "capsule-card";

    card.innerHTML = `
      <div class="card-top">
        <div>
          <div class="card-kicker">${capsuleId}</div>
          <div class="card-title">Capsuleを読み込めません</div>
        </div>
      </div>
      <div class="card-meta">${error.message}</div>
      <div class="card-footer">
        <span class="badge badge-gray">ERROR</span>
      </div>
    `;

    return card;
  }

  async function loadCapsuleCard(capsuleId) {
    const basePath =
      `/workspace/users/${LOCAL_USER_ID}/capsules/${encodeURIComponent(capsuleId)}`;

    try {
      const metadata = await loadJson(`${basePath}/metadata.json`);
      return createCard(capsuleId, metadata);
    } catch (error) {
      console.error(`Capsule load failed: ${capsuleId}`, error);
      return createErrorCard(capsuleId, error);
    }
  }

  async function init() {
    if (!grid) return;

    grid.innerHTML = "";

    for (const capsuleId of FIXED_CAPSULE_IDS) {
      const card = await loadCapsuleCard(capsuleId);
      grid.appendChild(card);
    }
  }

  init();
})();
