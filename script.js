const state = {
  pages: [],
  sections: [],
  activeSection: "all",
  query: "",
  visiblePages: [],
  modalIndex: 0,
};

const elements = {
  header: document.querySelector("[data-header]"),
  filters: document.querySelector("#sectionFilters"),
  search: document.querySelector("#pageSearch"),
  resultCount: document.querySelector("#resultCount"),
  pageGrid: document.querySelector("#pageGrid"),
  modal: document.querySelector("#pageModal"),
  modalMeta: document.querySelector("#modalMeta"),
  modalTitle: document.querySelector("#modalTitle"),
  modalImage: document.querySelector("#modalImage"),
  modalText: document.querySelector("#modalText"),
  closeModal: document.querySelector("[data-close-modal]"),
  prevPage: document.querySelector("[data-prev-page]"),
  nextPage: document.querySelector("[data-next-page]"),
};

const revealObserver = "IntersectionObserver" in window
  ? new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.16 })
  : null;

function observeReveal(scope = document) {
  const nodes = scope.querySelectorAll(".reveal:not(.is-visible)");
  nodes.forEach((node) => {
    if (revealObserver) {
      revealObserver.observe(node);
    } else {
      node.classList.add("is-visible");
    }
  });
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function normalize(value) {
  return String(value ?? "").toLocaleLowerCase("ru-RU").trim();
}

function cardSummary(page) {
  if (page.summary) {
    return page.summary;
  }

  if (page.section === "certificates") {
    return "Оригинальная страница сертификата или приложения из исходного PDF.";
  }

  return "Оригинальная визуальная страница из полного комплекта документации.";
}

function setHeaderState() {
  elements.header?.classList.toggle("is-solid", window.scrollY > 24);
}

function renderFilters() {
  const allButton = `
    <button class="filter-button is-active" type="button" data-section="all">
      Все страницы
    </button>
  `;

  const sectionButtons = state.sections.map((section) => `
    <button class="filter-button" type="button" data-section="${escapeHtml(section.key)}">
      ${escapeHtml(section.title)} (${section.count})
    </button>
  `).join("");

  elements.filters.innerHTML = allButton + sectionButtons;

  elements.filters.addEventListener("click", (event) => {
    const button = event.target.closest("[data-section]");
    if (!button) return;
    state.activeSection = button.dataset.section;
    elements.filters.querySelectorAll(".filter-button").forEach((item) => {
      item.classList.toggle("is-active", item === button);
    });
    renderPages();
  });
}

function filterPages() {
  const query = normalize(state.query);

  return state.pages.filter((page) => {
    const sectionMatch = state.activeSection === "all" || page.section === state.activeSection;
    if (!sectionMatch) return false;
    if (!query) return true;

    const haystack = normalize([
      page.title,
      page.sectionTitle,
      page.summary,
      page.text,
      `страница ${page.number}`,
    ].join(" "));

    return haystack.includes(query);
  });
}

function renderPages() {
  state.visiblePages = filterPages();

  elements.resultCount.textContent = `${state.visiblePages.length} из ${state.pages.length} страниц`;

  if (!state.visiblePages.length) {
    elements.pageGrid.innerHTML = `
      <article class="page-card reveal is-visible">
        <div class="page-card-body">
          <div class="page-meta"><span>Ничего не найдено</span></div>
          <h3>Попробуйте другой запрос</h3>
          <p>В полном комплекте доступны все страницы исходного PDF.</p>
        </div>
      </article>
    `;
    return;
  }

  elements.pageGrid.innerHTML = state.visiblePages.map((page) => `
    <article class="page-card reveal" data-page-number="${page.number}">
      <button class="page-open" type="button" aria-label="Открыть страницу ${page.number}">
        <img src="${escapeHtml(page.image)}" alt="${escapeHtml(page.title)}" loading="lazy">
      </button>
      <div class="page-card-body">
        <div class="page-meta">
          <span>Страница ${page.number}</span>
          <span>${escapeHtml(page.sectionTitle)}</span>
        </div>
        <h3>${escapeHtml(page.title)}</h3>
        <p>${escapeHtml(cardSummary(page))}</p>
      </div>
    </article>
  `).join("");

  elements.pageGrid.querySelectorAll(".page-card").forEach((card) => {
    card.addEventListener("click", () => {
      const pageNumber = Number(card.dataset.pageNumber);
      openPage(pageNumber);
    });
  });

  observeReveal(elements.pageGrid);
}

function getPageByNumber(pageNumber) {
  return state.pages.find((page) => page.number === pageNumber);
}

function setModalPage(pageNumber) {
  const page = getPageByNumber(pageNumber);
  if (!page) return;

  state.modalIndex = state.pages.findIndex((item) => item.number === pageNumber);
  elements.modalMeta.textContent = `Страница ${page.number} из ${state.pages.length} · ${page.sectionTitle}`;
  elements.modalTitle.textContent = page.title;
  elements.modalImage.src = page.image;
  elements.modalImage.alt = page.title;
  elements.modalText.textContent = page.text || "Текстовый слой на этой странице не извлечен; оригинальное содержание сохранено на изображении страницы.";
}

function openPage(pageNumber) {
  setModalPage(pageNumber);

  if (typeof elements.modal.showModal === "function") {
    elements.modal.showModal();
  } else {
    elements.modal.setAttribute("open", "");
  }

  document.body.style.overflow = "hidden";
  elements.closeModal.focus();
}

function closePageModal() {
  if (elements.modal.open) {
    elements.modal.close();
  } else {
    elements.modal.removeAttribute("open");
  }

  document.body.style.overflow = "";
}

function stepModal(direction) {
  const nextIndex = (state.modalIndex + direction + state.pages.length) % state.pages.length;
  setModalPage(state.pages[nextIndex].number);
}

function delay(ms) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}

async function fetchJsonWithRetry(url, attempts = 3) {
  let lastError;

  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    try {
      const response = await fetch(url, { cache: "no-store" });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return response.json();
    } catch (error) {
      lastError = error;
      if (attempt < attempts) {
        await delay(350 * attempt);
      }
    }
  }

  throw lastError;
}

async function loadContent() {
  try {
    const content = await fetchJsonWithRetry("content.json");
    state.pages = content.pages || [];
    state.sections = content.sections || [];

    renderFilters();
    renderPages();
  } catch (error) {
    elements.resultCount.textContent = "Не удалось загрузить content.json";
    elements.pageGrid.innerHTML = `
      <article class="page-card reveal is-visible">
        <div class="page-card-body">
          <div class="page-meta"><span>Ошибка загрузки</span></div>
          <h3>Контент не загружен</h3>
          <p>${escapeHtml(error.message)}</p>
        </div>
      </article>
    `;
  }
}

elements.search?.addEventListener("input", (event) => {
  state.query = event.target.value;
  renderPages();
});

elements.closeModal?.addEventListener("click", closePageModal);
elements.prevPage?.addEventListener("click", () => stepModal(-1));
elements.nextPage?.addEventListener("click", () => stepModal(1));

elements.modal?.addEventListener("click", (event) => {
  if (event.target === elements.modal) {
    closePageModal();
  }
});

window.addEventListener("keydown", (event) => {
  if (!elements.modal?.open) return;

  if (event.key === "Escape") {
    closePageModal();
  }

  if (event.key === "ArrowLeft") {
    stepModal(-1);
  }

  if (event.key === "ArrowRight") {
    stepModal(1);
  }
});

window.addEventListener("scroll", setHeaderState, { passive: true });

/* Animated counters */
function animateCount(node) {
  const target = Number(node.dataset.count);
  if (!Number.isFinite(target)) return;

  const suffix = node.dataset.suffix ?? "";
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reduceMotion) {
    node.textContent = `${target.toLocaleString("ru-RU")}${suffix}`;
    return;
  }

  const duration = 1100;
  let startTime = null;

  function tick(timestamp) {
    if (startTime === null) startTime = timestamp;
    const progress = Math.min((timestamp - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const value = Math.round(target * eased);
    node.textContent = `${value.toLocaleString("ru-RU")}${suffix}`;
    if (progress < 1) {
      window.requestAnimationFrame(tick);
    }
  }

  window.requestAnimationFrame(tick);
}

function initCounters() {
  const counters = document.querySelectorAll("[data-count]");
  if (!counters.length) return;

  if (!("IntersectionObserver" in window)) {
    counters.forEach(animateCount);
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateCount(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.4 });

  counters.forEach((node) => observer.observe(node));
}

/* Lead form */
function initLeadForm() {
  const form = document.querySelector("#leadForm");
  if (!form) return;

  const status = form.querySelector("#formStatus");
  const phone = form.querySelector("#leadPhone");

  phone?.addEventListener("input", () => {
    const digits = phone.value.replace(/\D/g, "").slice(0, 11);
    if (!digits) {
      phone.value = "";
      return;
    }
    let normalized = digits;
    if (normalized[0] === "8") normalized = `7${normalized.slice(1)}`;
    if (normalized[0] !== "7") normalized = `7${normalized}`.slice(0, 11);

    const p = normalized;
    let out = "+7";
    if (p.length > 1) out += ` (${p.slice(1, 4)}`;
    if (p.length >= 4) out += `)`;
    if (p.length >= 4) out += ` ${p.slice(4, 7)}`;
    if (p.length >= 7) out += `-${p.slice(7, 9)}`;
    if (p.length >= 9) out += `-${p.slice(9, 11)}`;
    phone.value = out;
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    status.textContent = "";
    status.className = "form-status";

    const required = form.querySelectorAll("[required]");
    let firstInvalid = null;

    required.forEach((field) => {
      const empty = field.type === "checkbox" ? !field.checked : !field.value.trim();
      field.classList.toggle("invalid", empty);
      if (empty && !firstInvalid) firstInvalid = field;
    });

    const digits = (phone?.value || "").replace(/\D/g, "");
    if (phone && digits.length < 11) {
      phone.classList.add("invalid");
      if (!firstInvalid) firstInvalid = phone;
    }

    if (firstInvalid) {
      status.textContent = "Заполните обязательные поля и корректный телефон.";
      status.classList.add("is-error");
      firstInvalid.focus();
      return;
    }

    const submit = form.querySelector(".lead-submit");
    if (submit) {
      submit.disabled = true;
      submit.textContent = "Отправляем…";
    }

    // Демо-отправка: здесь подключается реальный endpoint (server.mjs / CRM / почта).
    window.setTimeout(() => {
      form.reset();
      if (submit) {
        submit.disabled = false;
        submit.textContent = "Отправить заявку";
      }
      status.textContent = "Заявка отправлена! Инженер свяжется с вами в течение рабочего дня.";
      status.classList.remove("is-error");
      status.classList.add("is-success");
    }, 600);
  });

  form.querySelectorAll("input, textarea").forEach((field) => {
    field.addEventListener("input", () => field.classList.remove("invalid"));
  });
}

setHeaderState();
observeReveal();
initCounters();
initLeadForm();
loadContent();
