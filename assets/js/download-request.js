(() => {
  const modal = document.querySelector('[data-request-modal]');
  const form = document.querySelector('[data-request-form]');
  if (!modal || !form) return;

  const titleEl = modal.querySelector('[data-request-modal-title]');
  const leadEl = modal.querySelector('[data-request-modal-lead]');
  const datasetNameEl = modal.querySelector('[data-request-dataset-name]');
  const datasetIdInput = modal.querySelector('[data-request-dataset-id]');
  const emailInput = modal.querySelector('[data-request-email]');
  const organizationInput = modal.querySelector('[data-request-organization]');
  const purposeInput = modal.querySelector('[data-request-purpose]');
  const customDetailsInput = modal.querySelector('[data-custom-details]');
  const consentInput = modal.querySelector('[data-request-consent]');
  const statusEl = modal.querySelector('[data-request-status]');
  const dialogEl = modal.querySelector('.request-dialog');
  const termsBoxEl = modal.querySelector('.terms-box');

  let lastFocused = null;

  function t(key, fallback) {
    return (window.MEVA_MESSAGES && window.MEVA_MESSAGES[key]) || fallback || key;
  }

  function normalizeEmail(value) {
    return (value || '')
      .trim()
      .replace(/[Ａ-Ｚａ-ｚ０-９]/g, (ch) => String.fromCharCode(ch.charCodeAt(0) - 0xFEE0))
      .replace(/＠/g, '@')
      .replace(/[．。]/g, '.');
  }

  function isValidEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }

  function setStatus(message, isError = false) {
    statusEl.textContent = message || '';
    statusEl.classList.toggle('error', Boolean(isError));
  }

  function getDatasetName(button) {
    const titleKey = button.getAttribute('data-dataset-title-key');
    const translated = t(titleKey, '');
    if (translated && translated !== titleKey) return translated;
    const card = button.closest('.dataset-card');
    const h3 = card ? card.querySelector('h3') : null;
    return h3 ? h3.textContent.trim() : button.getAttribute('data-dataset-id');
  }

  function openModal(button) {
    lastFocused = button;
    const datasetId = button.getAttribute('data-dataset-id') || '';
    const datasetName = getDatasetName(button);
    const kind = button.getAttribute('data-request-kind') || 'dataset';
    form.reset();
    datasetIdInput.value = datasetId;
    datasetNameEl.textContent = datasetName;
    modal.setAttribute('data-request-kind', kind);
    setStatus('');

    if (kind === 'custom') {
      if (titleEl) titleEl.textContent = t('custom.modal.title', 'Request custom data');
      if (leadEl) leadEl.textContent = t('custom.modal.lead', 'Tell us what kind of motion, subjects, formats, and use case you need. We will contact you by email.');
    } else {
      if (titleEl) titleEl.textContent = t('request.modal.title', 'Request download link');
      if (leadEl) leadEl.textContent = t('request.modal.lead', 'Enter your email address and accept the dataset terms. We will send a time-limited download link to your email.');
    }

    modal.hidden = false;
    document.body.style.overflow = 'hidden';

    // Always open the request modal from the top.
    // Browsers preserve scrollTop on the same DOM element, so reset it explicitly.
    if (dialogEl) dialogEl.scrollTop = 0;
    if (termsBoxEl) termsBoxEl.scrollTop = 0;

    setTimeout(() => {
      if (dialogEl) dialogEl.scrollTop = 0;
      if (termsBoxEl) termsBoxEl.scrollTop = 0;
      emailInput.focus();
    }, 0);
  }

  function closeModal() {
    modal.hidden = true;
    document.body.style.overflow = '';
    setStatus('');
    if (lastFocused) lastFocused.focus();
  }

  document.querySelectorAll('[data-dataset-id].request-trigger').forEach((button) => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      openModal(button);
    });
  });

  modal.querySelectorAll('[data-request-cancel]').forEach((button) => {
    button.addEventListener('click', closeModal);
  });

  document.addEventListener('keydown', (event) => {
    if (!modal.hidden && event.key === 'Escape') closeModal();
  });

  emailInput.addEventListener('blur', () => {
    emailInput.value = normalizeEmail(emailInput.value);
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const email = normalizeEmail(emailInput.value);
    emailInput.value = email;

    if (!email) {
      setStatus(t('request.error.email_required', 'Please enter your email address.'), true);
      emailInput.focus();
      return;
    }

    if (!isValidEmail(email)) {
      setStatus(t('request.error.email_invalid', 'Please enter a valid email address.'), true);
      emailInput.focus();
      return;
    }

    if (!consentInput.checked) {
      setStatus(t('request.error.consent_required', 'Please confirm the dataset terms.'), true);
      consentInput.focus();
      return;
    }

    const kind = modal.getAttribute('data-request-kind') || 'dataset';
    const customDetails = customDetailsInput ? customDetailsInput.value.trim() : '';
    if (kind === 'custom' && !customDetails) {
      setStatus(t('custom.error.details_required', 'Please enter your custom data request details.'), true);
      if (customDetailsInput) customDetailsInput.focus();
      return;
    }

    const request = {
      dataset_id: datasetIdInput.value,
      dataset_name: datasetNameEl.textContent,
      email,
      organization: organizationInput.value.trim(),
      purpose: purposeInput ? purposeInput.value.trim() : '',
      custom_details: customDetails,
      request_kind: kind,
      language: window.MEVA_LANG || document.documentElement.lang || 'en',
      requested_at: new Date().toISOString(),
      mode: 'frontend-mock'
    };

    const stored = JSON.parse(localStorage.getItem('mevaCloudMockRequests') || '[]');
    stored.push(request);
    localStorage.setItem('mevaCloudMockRequests', JSON.stringify(stored));

    setStatus(kind === 'custom'
      ? t('custom.success.mock', 'Test mode: custom data request accepted. We would contact you by email.')
      : t('request.success.mock', 'Test mode: request accepted. A download link would be sent by email.'));
  });
})();
