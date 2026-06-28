(() => {
  const MANIFEST_URL = 'assets/data/capsules.json';
  let capsuleCache = null;

  const THUMB_SVGS = {
    walk: '<svg viewBox="0 0 420 190" preserveAspectRatio="none"><path d="M20 136 C82 62 137 156 202 90 C256 34 308 114 400 50" stroke="rgba(55,215,202,.62)" stroke-width="3" fill="none" stroke-dasharray="7 10"/><circle cx="210" cy="92" r="35" fill="rgba(55,215,202,.13)" stroke="rgba(55,215,202,.75)"/><path d="M85 132 L122 104 L164 128 L205 94 L248 122 L305 74" stroke="rgba(255,255,255,.23)" stroke-width="2" fill="none"/></svg>',
    jog: '<svg viewBox="0 0 420 190" preserveAspectRatio="none"><path d="M34 128 C88 82 130 112 174 78 C226 38 276 86 386 44" stroke="rgba(55,215,202,.65)" stroke-width="4" fill="none"/><path d="M42 148 C93 126 139 145 188 120 C240 92 290 122 382 92" stroke="rgba(101,167,216,.44)" stroke-width="2" fill="none" stroke-dasharray="5 8"/><circle cx="175" cy="78" r="10" fill="rgba(55,215,202,.75)"/><circle cx="276" cy="86" r="10" fill="rgba(242,140,66,.70)"/></svg>',
    pirouette: '<svg viewBox="0 0 420 190" preserveAspectRatio="none"><circle cx="210" cy="95" r="56" fill="none" stroke="rgba(55,215,202,.55)" stroke-width="3" stroke-dasharray="8 10"/><circle cx="210" cy="95" r="24" fill="rgba(181,108,255,.22)" stroke="rgba(181,108,255,.70)"/><path d="M210 42 L210 95 L176 135 M210 95 L250 130 M184 72 L236 72" stroke="rgba(255,255,255,.46)" stroke-width="4" fill="none" stroke-linecap="round"/></svg>',
    jazz: '<svg viewBox="0 0 420 190" preserveAspectRatio="none"><path d="M60 135 C92 70 140 138 178 78 C218 22 252 128 306 62 C342 22 366 64 390 44" stroke="rgba(242,140,66,.62)" stroke-width="4" fill="none"/><path d="M110 125 L150 88 L190 122 L240 74 L310 118" stroke="rgba(55,215,202,.55)" stroke-width="3" fill="none" stroke-linecap="round"/></svg>',
    radio: '<svg viewBox="0 0 420 190" preserveAspectRatio="none"><path d="M58 96 H362" stroke="rgba(255,255,255,.18)"/><path d="M210 50 L210 120 M160 80 L210 120 L260 80 M182 150 L210 120 L238 150" stroke="rgba(55,215,202,.70)" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="210" cy="42" r="16" fill="rgba(55,215,202,.22)" stroke="rgba(55,215,202,.70)"/></svg>',
    awa: '<svg viewBox="0 0 420 190" preserveAspectRatio="none"><path d="M80 130 C118 92 150 130 188 92 C226 54 258 130 300 92 C332 64 360 72 388 52" stroke="rgba(242,140,66,.65)" stroke-width="4" fill="none"/><path d="M125 70 L165 110 L205 70 M220 70 L260 110 L300 70" stroke="rgba(55,215,202,.56)" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="165" cy="110" r="9" fill="rgba(242,140,66,.72)"/><circle cx="260" cy="110" r="9" fill="rgba(55,215,202,.72)"/></svg>',
    sit: '<svg viewBox="0 0 420 190" preserveAspectRatio="none"><rect x="70" y="128" width="120" height="14" rx="7" fill="rgba(255,255,255,.18)"/><path d="M135 60 L155 98 L190 128 M155 98 L116 128 M145 76 L196 70" stroke="rgba(55,215,202,.62)" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M252 52 L252 116 L224 145 M252 116 L285 145 M222 76 L286 76" stroke="rgba(101,167,216,.52)" stroke-width="4" fill="none" stroke-linecap="round"/></svg>',
    object: '<svg viewBox="0 0 420 190" preserveAspectRatio="none"><rect x="270" y="112" width="54" height="42" rx="8" fill="rgba(242,140,66,.36)" stroke="rgba(242,140,66,.72)"/><path d="M120 54 L140 102 L118 150 M140 102 L184 98 L270 126 M140 102 L178 150" stroke="rgba(55,215,202,.62)" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M184 98 C214 92 234 100 270 126" stroke="rgba(255,255,255,.22)" stroke-width="2" fill="none"/></svg>',
    lettuce_transplant: '<svg viewBox="0 0 420 190" preserveAspectRatio="none"><path d="M64 138 C115 98 155 130 205 90 C250 54 302 84 362 52" stroke="rgba(55,215,202,.58)" stroke-width="4" fill="none"/><path d="M96 142 H348" stroke="rgba(255,255,255,.18)" stroke-width="5" stroke-linecap="round"/><path d="M150 82 C130 58 106 62 94 84 C118 88 138 98 150 82 Z" fill="rgba(99,220,151,.45)" stroke="rgba(99,220,151,.75)"/><path d="M264 96 C240 70 208 76 196 104 C226 108 250 120 264 96 Z" fill="rgba(99,220,151,.38)" stroke="rgba(99,220,151,.70)"/><path d="M154 88 L180 128 M202 106 L230 138" stroke="rgba(242,140,66,.68)" stroke-width="4" stroke-linecap="round"/></svg>',
    lettuce_selection: '<svg viewBox="0 0 420 190" preserveAspectRatio="none"><rect x="68" y="122" width="286" height="22" rx="11" fill="rgba(255,255,255,.16)"/><circle cx="132" cy="104" r="28" fill="rgba(99,220,151,.38)" stroke="rgba(99,220,151,.72)"/><circle cx="216" cy="98" r="34" fill="rgba(99,220,151,.45)" stroke="rgba(99,220,151,.78)"/><circle cx="302" cy="108" r="26" fill="rgba(99,220,151,.30)" stroke="rgba(99,220,151,.62)"/><path d="M96 62 C142 36 188 54 216 96 C248 58 300 48 344 72" stroke="rgba(55,215,202,.42)" stroke-width="3" fill="none" stroke-dasharray="6 9"/><path d="M214 42 L214 98 L184 132 M214 98 L248 132 M176 70 L250 70" stroke="rgba(255,255,255,.35)" stroke-width="4" fill="none" stroke-linecap="round"/></svg>',
    custom: '<svg viewBox="0 0 420 190" preserveAspectRatio="none"><path d="M34 126 C78 72 128 89 165 118 C202 148 245 151 282 112 C319 73 365 72 392 108" fill="none" stroke="rgba(255,255,255,.36)" stroke-width="10" stroke-linecap="round"/><path d="M60 58 H178 M60 92 H138 M232 62 H360 M232 96 H322" stroke="rgba(117,211,214,.44)" stroke-width="9" stroke-linecap="round"/><circle cx="95" cy="142" r="20" fill="rgba(117,211,214,.34)"/><circle cx="210" cy="142" r="20" fill="rgba(245,177,98,.30)"/><circle cx="325" cy="142" r="20" fill="rgba(156,124,255,.28)"/><path d="M112 142 H190 M228 142 H305" stroke="rgba(255,255,255,.34)" stroke-width="7" stroke-linecap="round"/></svg>'
  };

  function t(key, fallback) {
    return (window.MEVA_MESSAGES && window.MEVA_MESSAGES[key]) || fallback || key;
  }

  function localize(value, lang) {
    if (!value) return '';
    if (typeof value === 'string') return value;
    return value[lang] || value.en || '';
  }

  function escapeHtml(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  async function loadCapsules() {
    if (capsuleCache) return capsuleCache;
    const manifestRes = await fetch(MANIFEST_URL);
    if (!manifestRes.ok) throw new Error('Failed to load capsules.json');
    const manifest = await manifestRes.json();
    const items = (manifest.capsules || [])
      .filter((item) => item.enabled !== false)
      .sort((a, b) => (a.order || 9999) - (b.order || 9999));

    capsuleCache = await Promise.all(items.map(async (item) => {
      const res = await fetch(`assets/data/${item.file}`);
      if (!res.ok) throw new Error(`Failed to load capsule: ${item.file}`);
      const capsule = await res.json();
      return { ...capsule, order: item.order, source_file: item.file };
    }));
    return capsuleCache;
  }

  function renderCapsule(capsule, lang) {
    const title = localize(capsule.title, lang);
    const description = localize(capsule.description, lang);
    const requestKind = capsule.request_kind || 'dataset';
    const requestButtonKey = capsule.request_button_key || 'capsule.request';
    const category = capsule.category
      ? `<span class="badge category ${escapeHtml(capsule.category)}">${escapeHtml(t(`category.${capsule.category}`, capsule.category))}</span>`
      : '';
    const dataTypeClass = { motion: 'teal', gcp: 'purple', exo: 'blue' };
    const dataTypeBadges = (capsule.data_types || []).map((dataType) => {
      const kind = String(dataType.kind || '').toLowerCase();
      const format = String(dataType.format || '').toLowerCase();
      const labelKey = `datatype.${kind}_${format}`;
      const fallback = kind && format ? `${kind}/${format}` : (kind || format || '');
      return `<span class="badge ${escapeHtml(dataTypeClass[kind] || 'orange')}">${escapeHtml(t(labelKey, fallback))}</span>`;
    }).join('');
    const legacyTags = (capsule.tags || []).map((tag) => (
      `<span class="badge ${escapeHtml(tag.class || '')}">${escapeHtml(t(tag.key, tag.key))}</span>`
    )).join('');
    const tags = dataTypeBadges ? `${category}${dataTypeBadges}` : legacyTags;
    const specs = (capsule.specs || []).map((spec) => {
      const label = spec.label_key ? t(spec.label_key, spec.label_key) : localize(spec.label, lang);
      const value = localize(spec.value, lang);
      return `<div class="spec"><small>${escapeHtml(label)}</small><b>${escapeHtml(value)}</b></div>`;
    }).join('');
    const customClass = requestKind === 'custom' ? ' custom-data-card' : '';
    const requestKindAttr = requestKind === 'custom' ? ' data-request-kind="custom"' : '';
    const thumbClass = capsule.thumb_class || capsule.id;
    const thumbnail = capsule.thumbnail
      ? `<img class="capsule-thumbnail" src="${escapeHtml(capsule.thumbnail)}" loading="lazy">`
      : (THUMB_SVGS[thumbClass] || '');

    return `
      <article class="dataset-card${customClass}" data-capsule-id="${escapeHtml(capsule.id)}">
        <div class="thumb ${escapeHtml(thumbClass)}">
          <div class="badge-row">${tags}</div>
          ${thumbnail}
        </div>
        <div class="card-body">
          <h3>${escapeHtml(title)}</h3>
          <p>${escapeHtml(description)}</p>
          <div class="specs">${specs}</div>
          <div class="download-details request-details">
            <button type="button" class="request-trigger" data-dataset-id="${escapeHtml(capsule.id)}"${requestKindAttr} data-dataset-title="${escapeHtml(title)}">${escapeHtml(t(requestButtonKey, 'Request this capsule →'))}</button>
          </div>
        </div>
      </article>`;
  }

  async function renderCapsules(lang) {
    const container = document.querySelector('[data-capsule-cards]');
    if (!container) return;
    try {
      const capsules = await loadCapsules();
      const safeLang = lang || window.MEVA_LANG || document.documentElement.lang || 'en';
      container.innerHTML = capsules.map((capsule) => renderCapsule(capsule, safeLang)).join('');
    } catch (error) {
      console.error(error);
      container.innerHTML = '<p class="capsule-load-error">Failed to load capsule data.</p>';
    }
  }

  window.addEventListener('meva:language-applied', (event) => {
    renderCapsules(event.detail && event.detail.lang);
  });

  document.addEventListener('DOMContentLoaded', () => {
    if (window.MEVA_LANG) renderCapsules(window.MEVA_LANG);
  });
})();
