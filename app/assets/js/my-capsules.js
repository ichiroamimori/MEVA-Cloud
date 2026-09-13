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

    const top = document.createElement("div");
    top.className = "card-top";
    const heading = document.createElement("div");
    const kicker = document.createElement("div");
    kicker.className = "card-kicker";
    kicker.textContent = capsule.id;
    const title = document.createElement("div");
    title.className = "card-title";
    title.textContent = capsule.title;
    heading.append(kicker, title);
    const date = document.createElement("div");
    date.className = "card-meta";
    date.textContent = capsule.date;
    top.append(heading, date);
    const description = document.createElement("div");
    description.className = "card-meta";
    description.textContent = capsule.description;
    const footer = document.createElement("div");
    footer.className = "card-footer";
    for (const modality of capsule.modalities) {
      const badge = document.createElement("span");
      badge.className = "badge";
      badge.textContent = modality;
      footer.appendChild(badge);
    }
    card.append(top, description, footer);

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

    const top = document.createElement("div");
    top.className = "card-top";
    const heading = document.createElement("div");
    const kicker = document.createElement("div");
    kicker.className = "card-kicker";
    kicker.textContent = capsuleId;
    const title = document.createElement("div");
    title.className = "card-title";
    title.textContent = "Capsuleを読み込めません";
    heading.append(kicker, title);
    top.appendChild(heading);
    const detail = document.createElement("div");
    detail.className = "card-meta";
    detail.textContent = String(error?.message || error || "Unknown error");
    const footer = document.createElement("div");
    footer.className = "card-footer";
    const badge = document.createElement("span");
    badge.className = "badge badge-gray";
    badge.textContent = "ERROR";
    footer.appendChild(badge);
    card.append(top, detail, footer);

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
