// 프로젝트 목록의 기술 필터. JS가 없으면 필터를 숨기고 전체 목록을 보여준다.
(function () {
  var box = document.querySelector('[data-filter]');
  if (!box) return;
  var chips = Array.prototype.slice.call(box.querySelectorAll('[data-tech]'));
  var cards = Array.prototype.slice.call(document.querySelectorAll('[data-stack]'));
  var status = box.querySelector('[data-filter-status]');

  function apply(tech) {
    var shown = 0;
    chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.dataset.tech === tech)); });
    cards.forEach(function (card) {
      var match = !tech || card.dataset.stack.split('|').indexOf(tech) !== -1;
      card.hidden = !match;
      if (match) shown++;
    });
    status.textContent = tech ? tech + ': 프로젝트 ' + shown + '개' : '';
    var url = new URL(location.href);
    if (tech) url.searchParams.set('tech', tech); else url.searchParams.delete('tech');
    history.replaceState(null, '', url);
  }

  chips.forEach(function (c) { c.addEventListener('click', function () { apply(c.dataset.tech); }); });
  box.hidden = false;
  var initial = new URL(location.href).searchParams.get('tech') || '';
  apply(chips.some(function (c) { return c.dataset.tech === initial; }) ? initial : '');
})();
