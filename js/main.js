(() => {
  'use strict';

  const CONFIG = {
    whatsappNumber: '584125003831',
    whatsappDefaultMessage: 'Hola ACC, quiero cotizar un requerimiento para mi planta.',
    whatsappProductMessage: (name) => `Hola ACC, quiero cotizar: ${name}.`,
    instagramUrl: 'https://www.instagram.com/accinversiones/',
    mapsQuery: 'Inversiones ACC 2018 Valencia Carabobo',
  };

  document.querySelectorAll('[data-whatsapp]').forEach((link) => {
    const message = link.dataset.product
      ? CONFIG.whatsappProductMessage(link.dataset.product)
      : CONFIG.whatsappDefaultMessage;
    link.href = `https://wa.me/${CONFIG.whatsappNumber}?text=${encodeURIComponent(message)}`;
  });
  document.querySelectorAll('[data-instagram]').forEach((link) => {
    link.href = CONFIG.instagramUrl;
  });

  const menu = document.querySelector('#mobile-menu');
  const toggle = document.querySelector('.menu-toggle');
  const close = document.querySelector('.menu-close');

  const closeMenu = () => {
    menu.close();
    toggle.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('menu-open');
    toggle.focus({ preventScroll: true });
  };

  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    menu.showModal();
    toggle.setAttribute('aria-expanded', 'true');
    document.body.classList.add('menu-open');
    close.focus();
  });
  close.addEventListener('click', closeMenu);
  menu.addEventListener('cancel', (event) => {
    event.preventDefault();
    closeMenu();
  });
  menu.addEventListener('click', (event) => {
    const link = event.target.closest('a');
    if (!link) return;
    closeMenu();
    if (link.hash && link.origin === location.origin) {
      const section = document.querySelector(link.hash);
      section?.setAttribute('tabindex', '-1');
      section?.focus({ preventScroll: true });
    }
  });
  menu.addEventListener('keydown', (event) => {
    if (event.key !== 'Tab') return;
    const links = menu.querySelectorAll('button, a[href]');
    const first = links[0];
    const last = links[links.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
  window.matchMedia('(min-width: 768px)').addEventListener('change', (event) => {
    if (event.matches && menu.open) closeMenu();
  });

  const header = document.querySelector('.site-header');
  const updateHeader = () => header.classList.toggle('is-scrolled', window.scrollY > 0);
  window.addEventListener('scroll', updateHeader, { passive: true });
  updateHeader();

  const year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();

  const map = document.querySelector('[data-map]');
  if (map) {
    const query = new URLSearchParams({ q: CONFIG.mapsQuery, output: 'embed' });
    const source = `https://www.google.com/maps?${query}`;
    if (map.src !== source) map.src = source;
  }
})();
