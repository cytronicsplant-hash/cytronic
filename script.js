// Menú en celular
const toggle = document.querySelector('.nav-toggle');
const nav = document.getElementById('nav');

const setMenu = (open) => {
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  nav.classList.toggle('is-open', open);
};
toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
nav.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setMenu(false)));
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

// Sombra del header al bajar
const header = document.querySelector('.header');
const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if ('IntersectionObserver' in window) {
  // Resaltar en el menú la sección visible (solo en la página de inicio)
  const links = [...nav.querySelectorAll('a[href*="#"]:not(.btn)')];
  const byId = {};
  links.forEach((a) => {
    const [path, id] = a.getAttribute('href').split('#');
    const el = id && document.getElementById(id);
    if (el && (path === '' || location.pathname.endsWith(path) || (path === 'index.html' && location.pathname.endsWith('/')))) {
      (byId[id] = byId[id] || []).push(a);
    }
  });
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      links.forEach((a) => a.classList.remove('is-active'));
      (byId[entry.target.id] || []).forEach((a) => a.classList.add('is-active'));
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  Object.keys(byId).forEach((id) => spy.observe(document.getElementById(id)));

  // Aparición suave, escalonada dentro de cada grupo
  const groups = ['.stats', '.mv', '.svc-grid', '.projects', '.results', '.values', '.features', '.checklist', '.chips', '.steps', '.mini-grid', '.svc-project'];
  const reveal = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        reveal.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  if (!reduceMotion) {
    document.querySelectorAll(groups.join(',')).forEach((g) => {
      [...g.children].forEach((el, i) => {
        el.classList.add('reveal');
        el.style.setProperty('--rd', `${Math.min(i, 6) * 80}ms`);
        reveal.observe(el);
      });
    });
  }

  // Contadores animados (+15, 6, 8, 35%, 45%)
  const counters = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      counters.unobserve(entry.target);
      const el = entry.target;
      const end = Number(el.dataset.count);
      const pre = el.dataset.prefix || '';
      const suf = el.dataset.suffix || '';
      if (reduceMotion) return;
      const t0 = performance.now();
      const dur = 1200;
      const step = (t) => {
        const k = Math.min((t - t0) / dur, 1);
        el.textContent = pre + Math.round(end * (1 - Math.pow(1 - k, 3))) + suf;
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    });
  }, { threshold: 0.6 });
  document.querySelectorAll('[data-count]').forEach((el) => counters.observe(el));
}

// Formulario de contacto (envío por FormSubmit, sin recargar la página)
document.querySelectorAll('[data-form]').forEach((form) => {
  const status = form.querySelector('.form__status');
  const button = form.querySelector('.form__submit');

  const setStatus = (msg, type) => {
    status.textContent = msg;
    status.className = 'form__status' + (type ? ' is-' + type : '');
  };

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Validación propia, con mensajes en español
    let firstBad = null;
    form.querySelectorAll('[required]').forEach((input) => {
      const bad = !input.value.trim() || (input.type === 'email' && !input.checkValidity());
      input.closest('.field').classList.toggle('is-invalid', bad);
      if (bad && !firstBad) firstBad = input;
    });
    if (firstBad) {
      setStatus('Revise los campos marcados: nombre, un correo válido y el mensaje son obligatorios.', 'error');
      firstBad.focus();
      return;
    }
    if (form._honey && form._honey.value) return; // bot

    button.disabled = true;
    const label = button.textContent;
    button.textContent = 'Enviando…';
    setStatus('', '');

    try {
      const res = await fetch(form.action, {
        method: 'POST',
        headers: { Accept: 'application/json' },
        body: new FormData(form),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok || String(data.success) === 'false') throw new Error(data.message || res.status);
      form.reset();
      setStatus('¡Gracias! Recibimos su solicitud y le contactaremos pronto.', 'ok');
    } catch (err) {
      setStatus('No se pudo enviar. Escríbanos por WhatsApp al 0960071515 o a cytronicsplant@gmail.com.', 'error');
    } finally {
      button.disabled = false;
      button.textContent = label;
    }
  });

  form.querySelectorAll('input, textarea').forEach((input) =>
    input.addEventListener('input', () => input.closest('.field')?.classList.remove('is-invalid'))
  );
});

document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
