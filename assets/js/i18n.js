const SUPPORTED_LANGS = ['en', 'zh-CN', 'de', 'fr', 'es', 'ja'];
const DEFAULT_LANG = 'en';

function getInitialLang() {
  const params = new URLSearchParams(window.location.search);
  const urlLang = params.get('lang');
  if (SUPPORTED_LANGS.includes(urlLang)) return urlLang;

  const stored = localStorage.getItem('mevaCloudLang');
  if (SUPPORTED_LANGS.includes(stored)) return stored;

  const browser = (navigator.language || '').toLowerCase();
  if (browser.startsWith('ja')) return 'ja';
  if (browser.startsWith('zh')) return 'zh-CN';
  if (browser.startsWith('de')) return 'de';
  if (browser.startsWith('fr')) return 'fr';
  if (browser.startsWith('es')) return 'es';
  return DEFAULT_LANG;
}

async function loadMessages(lang) {
  const response = await fetch(`assets/i18n/${lang}.json`);
  if (!response.ok) throw new Error(`Failed to load language: ${lang}`);
  return response.json();
}

function applyMessages(messages, lang) {
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    if (messages[key] !== undefined) el.textContent = messages[key];
  });

  document.querySelectorAll('[data-i18n-html]').forEach((el) => {
    const key = el.getAttribute('data-i18n-html');
    if (messages[key] !== undefined) el.innerHTML = messages[key];
  });

  document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (messages[key] !== undefined) el.setAttribute('placeholder', messages[key]);
  });

  if (messages['meta.title']) document.title = messages['meta.title'];

  const mevaLink = document.querySelector('[data-meva-link]');
  if (mevaLink) {
    mevaLink.href = lang === 'ja'
      ? 'https://xenoma.com/business/eskin-meva/'
      : 'https://xenoma.com/en/business/eskin-meva/';
  }

  document.querySelectorAll('[data-lang]').forEach((button) => {
    button.classList.toggle('active', button.getAttribute('data-lang') === lang);
  });
}

async function setLanguage(lang) {
  const safeLang = SUPPORTED_LANGS.includes(lang) ? lang : DEFAULT_LANG;
  try {
    const messages = await loadMessages(safeLang);
    applyMessages(messages, safeLang);
    localStorage.setItem('mevaCloudLang', safeLang);
    const url = new URL(window.location.href);
    url.searchParams.set('lang', safeLang);
    window.history.replaceState({}, '', url);
  } catch (error) {
    console.error(error);
    if (safeLang !== DEFAULT_LANG) setLanguage(DEFAULT_LANG);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-lang]').forEach((button) => {
    button.addEventListener('click', () => setLanguage(button.getAttribute('data-lang')));
  });
  setLanguage(getInitialLang());
});
