// Калькулятор подбора узла огнестойкой проходки ФП-БУСТ-ПКМ-01
(function () {
  const form = document.getElementById("calcForm");
  const result = document.getElementById("calcResult");
  if (!form || !result) return;

  const TYPES = {
    kabel: { code: "4", letter: "EIT", name: "Кабельная проходка", link: "../kabelnye-prohodki/" },
    shina: { code: "Ш", letter: "EIT", name: "Проход шинопровода", link: "../shinoprovody/" },
    truba: { code: "Т", letter: "EI", name: "Проход трубопровода / воздуховода", link: "../truby-vozduhovody/" },
    kombi: { code: "К", letter: "EI", name: "Комбинированная проходка", link: "../kombinirovannye-prohodki/" },
  };

  function num(id) {
    const v = parseInt(document.getElementById(id).value, 10);
    return Number.isFinite(v) ? v : 0;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const t = TYPES[document.getElementById("calcType").value] || TYPES.kabel;
    const w = num("calcW");
    const h = num("calcH");
    const eit = document.getElementById("calcEit").value;

    if (w < 50 || h < 50) {
      result.innerHTML =
        '<h3>Результат подбора</h3><p class="calc-error">Укажите ширину и высоту проёма (от 50 мм).</p>';
      return;
    }

    const marking = `ФП-БУСТ-ПКМ-01-${w}х${h}-${t.code}/ПМ(1)-${eit}`;
    const areaM2 = (w * h) / 1e6;
    const perimM = (2 * (w + h)) / 1000;

    result.innerHTML = `
      <h3>Предварительный подбор узла</h3>
      <p class="calc-marking">${marking}</p>
      <dl class="calc-spec">
        <div><dt>Тип узла</dt><dd>${t.name}</dd></div>
        <div><dt>Предел огнестойкости</dt><dd>${t.letter} ${eit} минут</dd></div>
        <div><dt>Проём A×B</dt><dd>${w} × ${h} мм (${areaM2.toFixed(2)} м², периметр ${perimM.toFixed(2)} м)</dd></div>
      </dl>
      <h4>Состав заделки</h4>
      <ul class="calc-materials">
        <li>Минераловатная плита плотностью ≥150 кг/м³ — заполнение свободного пространства проёма</li>
        <li>Пена противопожарная ФП-БУСТ-01 — вокруг коммуникаций на всю глубину заделки</li>
        <li>Герметик ФП-БУСТ-05 — наружные швы и финишный абляционный слой ≥1 мм с обеих сторон</li>
      </ul>
      <p class="calc-note">Это предварительная маркировка по введённым данным. Точный узел, исполнение и спецификацию материалов подтверждает инженер при подготовке КП.</p>
      <div class="calc-actions">
        <a class="button button-primary full" href="../#contacts">Получить точный расчёт и КП</a>
        <a class="button button-secondary full" href="${t.link}">Подробнее о типе проходки</a>
      </div>
    `;
    result.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });
})();
