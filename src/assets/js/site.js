/* Progressive enhancement: accessible navigation and DOM-only filtering.
 * Optional contract: data-filter-scope wraps controls and items;
 * data-filter-item and data-year can override legacy markup discovery.
 */
(function () {
  'use strict';
  function init() {
    document.documentElement.classList.add('js');
    document.querySelectorAll('.menu-toggle, [data-menu-toggle]').forEach(function (button) {
      var id = button.getAttribute('aria-controls');
      var menu = id ? document.getElementById(id) : document.querySelector('.site-menu');
      if (!menu) return;
      function setOpen(open) {
        menu.classList.toggle('is-open', open);
        button.setAttribute('aria-expanded', String(open));
      }
      setOpen(false);
      button.addEventListener('click', function () { setOpen(button.getAttribute('aria-expanded') !== 'true'); });
      menu.addEventListener('click', function (event) {
        if (event.target.closest('a')) setOpen(false);
      });
      document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
          setOpen(false);
          button.focus();
        }
      });
      var desktop = window.matchMedia('(min-width: 1024px)');
      function resetMenu() { if (desktop.matches) setOpen(false); }
      if (desktop.addEventListener) desktop.addEventListener('change', resetMenu);
    });

    // Avoid automatically playing research animations when reduced motion is requested.
    var reduceVideoMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    document.querySelectorAll('[data-research-video]').forEach(function (video) {
      function applyVideoPreference() {
        if (reduceVideoMotion.matches) {
          video.autoplay = false;
          video.pause();
        }
      }
      applyVideoPreference();
      if (reduceVideoMotion.addEventListener) reduceVideoMotion.addEventListener('change', applyVideoPreference);
    });

    var vietnamese = document.documentElement.lang === 'vi';
    function createPager(scope, allItems, size, onRender) {
      var current = 1, matches = allItems.slice();
      var nav = document.createElement('nav');
      nav.className = 'list-pagination';
      nav.setAttribute('aria-label', vietnamese ? 'Phân trang' : 'Pagination');
      var info = document.createElement('p');
      info.className = 'pagination-status';
      info.setAttribute('role', 'status');
      var buttons = document.createElement('div');
      buttons.className = 'pagination-buttons';
      nav.appendChild(info); nav.appendChild(buttons); scope.insertBefore(nav, scope.firstChild);
      function render(focusPage) {
        var pages = Math.max(1, Math.ceil(matches.length / size));
        current = Math.min(current, pages);
        allItems.forEach(function (item) { item.hidden = true; });
        matches.slice((current - 1) * size, current * size).forEach(function (item) { item.hidden = false; });
        buttons.textContent = '';
        nav.hidden = matches.length <= size;
        info.textContent = (vietnamese ? 'Trang ' : 'Page ') + current + ' / ' + pages;
        function button(label, page, disabled, active) {
          var element = document.createElement('button');
          element.type = 'button'; element.textContent = label; element.disabled = disabled;
          if (active) element.setAttribute('aria-current', 'page');
          element.addEventListener('click', function () { current = page; render(true); });
          buttons.appendChild(element);
          if (focusPage && active) element.focus({preventScroll: true});
        }
        button(vietnamese ? 'Trước' : 'Previous', current - 1, current === 1, false);
        var first = Math.max(1, Math.min(current - 2, pages - 4));
        var last = Math.min(pages, first + 4);
        function ellipsis() {
          var gap = document.createElement('span');
          gap.className = 'pagination-gap'; gap.textContent = '…';
          gap.setAttribute('aria-hidden', 'true'); buttons.appendChild(gap);
        }
        if (first > 1) button('1', 1, false, false);
        if (first > 2) ellipsis();
        for (var page = first; page <= last; page++) button(String(page), page, false, page === current);
        if (last < pages - 1) ellipsis();
        if (last < pages) button(String(pages), pages, false, false);
        button(vietnamese ? 'Sau' : 'Next', current + 1, current === pages, false);
        if (onRender) onRender();

      }
      return {setItems:function (items) { matches = items; current = 1; render(false); }};
    }
    function normalize(value) {
      return value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D').toLocaleLowerCase().trim();
    }
    function yearFor(item, scope) {
      var explicit = item.closest('[data-year]');
      if (explicit) return explicit.getAttribute('data-year');
      var node = item;
      while (node && node !== scope) {
        var sibling = node.previousElementSibling;
        while (sibling) {
          if (/^H[2-4]$/.test(sibling.tagName)) {
            var headingYear = sibling.textContent.match(/\b(?:19|20)\d{2}\b/);
            if (headingYear) return headingYear[0];
          }
          sibling = sibling.previousElementSibling;
        }
        node = node.parentElement;
      }
      var textYear = item.textContent.match(/\b(?:19|20)\d{2}\b/g);
      return textYear ? textYear[textYear.length - 1] : '';
    }
    var scopes = new Set();
    document.querySelectorAll('[data-filter-input], [data-year-filter], [data-type-filter], [data-venue-filter]').forEach(function (control) {
      scopes.add(control.closest('[data-filter-scope]') || control.closest('.page-content') || document.querySelector('main') || document.body);
    });
    scopes.forEach(function (scope) {
      var input = scope.querySelector('[data-filter-input]');
      var select = scope.querySelector('[data-year-filter]');
      var typeSelect = scope.querySelector('[data-type-filter]');
      var venueSelect = scope.querySelector('[data-venue-filter]');
      var explicitItems = scope.querySelectorAll('[data-filter-item]');
      var items = Array.from(explicitItems.length ? explicitItems : scope.querySelectorAll('.paperbox, .memberbox, .list-group-item'));
      if (!items.length) return;
      var records = items.map(function (item) {
        return { element: item, text: normalize(item.getAttribute('data-search-text') || item.textContent), year: yearFor(item, scope), type: item.getAttribute('data-publication-type') || '', venue: item.getAttribute('data-venue') || '', venueName: item.getAttribute('data-venue-name') || '', initiallyHidden: item.hidden };
      });
      if (select && select.options.length <= 1) {
        Array.from(new Set(records.map(function (record) { return record.year; }).filter(Boolean))).sort().reverse().forEach(function (year) {
          var option = document.createElement('option');
          option.value = year;
          option.textContent = year;
          select.appendChild(option);
        });
      }
      function populateVenues() {
        if (!venueSelect) return;
        var previous = venueSelect.value;
        while (venueSelect.options.length > 1) venueSelect.remove(1);
        var names = new Map();
        records.forEach(function (record) {
          if (record.venue && (!typeSelect || !typeSelect.value || record.type === typeSelect.value)) names.set(record.venue, record.venueName);
        });
        Array.from(names.entries()).sort(function (a, b) { return a[1].localeCompare(b[1]); }).forEach(function (pair) {
          var option = document.createElement('option');
          option.value = pair[0]; option.textContent = pair[1]; venueSelect.appendChild(option);
        });
        venueSelect.value = names.has(previous) ? previous : '';
      }
      populateVenues();
      var status = scope.querySelector('[data-filter-status]');
      if (!status) {
        status = document.createElement('p');
        status.className = 'filter-status';
        status.setAttribute('data-filter-status', '');
        var toolbar = (input || select).closest('.filter-toolbar');
        if (toolbar) toolbar.insertAdjacentElement('afterend', status);
        else (input || select).insertAdjacentElement('afterend', status);
      }
      status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');
      var empty = scope.querySelector('[data-filter-empty]');
      if (!empty) {
        empty = document.createElement('p');
        empty.className = 'filter-empty';
        empty.textContent = vietnamese ? 'Không tìm thấy kết quả. Hãy thử từ khóa khác hoặc bỏ bộ lọc.' : 'No results found. Try another keyword or clear the filters.';
        status.insertAdjacentElement('afterend', empty);
      }
      function syncGroups() {
        Array.from(scope.querySelectorAll('[data-venue-group]')).concat(Array.from(scope.querySelectorAll('[data-page-group]'))).forEach(function (group) {
          group.hidden = !records.some(function (record) { return !record.element.hidden && group.contains(record.element); });
        });
      }
      var size = scope.getAttribute ? Number(scope.getAttribute('data-page-size')) : 0;
      var pager = size ? createPager(scope, items, size, syncGroups) : null;
      function update() {
        var query = input ? normalize(input.value) : '';
        var year = select ? select.value : '';
        var type = typeSelect ? typeSelect.value : '';
        var venue = venueSelect ? venueSelect.value : '';
        var words = query.split(/\s+/).filter(Boolean);
        var matches = records.filter(function (record) {
          return !record.initiallyHidden && words.every(function (word) { return record.text.indexOf(word) !== -1; }) && (!year || year === 'all' || record.year === year) && (!type || record.type === type) && (!venue || record.venue === venue);
        });
        records.forEach(function (record) { record.element.hidden = matches.indexOf(record) === -1; });
        if (pager) pager.setItems(matches.map(function (record) { return record.element; }));
        else syncGroups();
        status.textContent = matches.length + ' / ' + records.filter(function (record) { return !record.initiallyHidden; }).length + (vietnamese ? ' kết quả' : ' results');
        empty.hidden = matches.length > 0;
      }
      if (input) input.addEventListener('input', update);
      if (select) select.addEventListener('change', update);
      if (typeSelect) typeSelect.addEventListener('change', function () { populateVenues(); update(); });
      if (venueSelect) venueSelect.addEventListener('change', update);
      scope.querySelectorAll('[data-filter-reset]').forEach(function (button) {
        button.addEventListener('click', function () {
          if (input) input.value = '';
          if (select) select.value = '';
          if (typeSelect) typeSelect.value = '';
          if (venueSelect) venueSelect.value = '';
          populateVenues();
          update();
          if (input) input.focus();
        });
      });
      update();
    });

    document.querySelectorAll('[data-paginate]').forEach(function (scope) {
      var items = Array.from(scope.querySelectorAll('[data-page-item]'));
      if (!items.length) return;
      createPager(scope, items, Number(scope.getAttribute('data-page-size')) || 6).setItems(items);
    });

    document.querySelectorAll('[data-slideshow]').forEach(function (carousel) {
      var slides = Array.from(carousel.querySelectorAll('[data-slide]'));
      if (slides.length < 2) return;
      var index = 0, paused = false, hovering = false;
      var motion = window.matchMedia('(prefers-reduced-motion: reduce)');
      var pause = carousel.querySelector('[data-slide-pause]');
      carousel.querySelector('.slideshow-controls').hidden = false;
      function showSlide(next) {
        index = (next + slides.length) % slides.length;
        slides.forEach(function (slide, i) {
          slide.classList.toggle('is-active', i === index);
          slide.setAttribute('aria-hidden', String(i !== index));
        });
        carousel.querySelector('[data-slide-status]').textContent = (index + 1) + ' / ' + slides.length;
      }
      carousel.querySelector('[data-slide-prev]').addEventListener('click', function () { showSlide(index - 1); });
      carousel.querySelector('[data-slide-next]').addEventListener('click', function () { showSlide(index + 1); });
      pause.addEventListener('click', function () {
        paused = !paused;
        pause.setAttribute('aria-pressed', String(paused));
        pause.textContent = paused ? (vietnamese ? 'Tiếp tục' : 'Play') : (vietnamese ? 'Tạm dừng' : 'Pause');
      });
      carousel.addEventListener('mouseenter', function () { hovering = true; });
      carousel.addEventListener('mouseleave', function () { hovering = false; });
      window.setInterval(function () {
        var rect = carousel.getBoundingClientRect();
        if (!paused && !hovering && !motion.matches && !document.hidden && !carousel.contains(document.activeElement) && rect.bottom > 0 && rect.top < window.innerHeight) showSlide(index + 1);
      }, 4500);
    });

    // Viewport intersections also respect clipping by nested .content-scroll regions.
    var motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
    if ('IntersectionObserver' in window && !motionPreference.matches) {
      var selector = '.hero-copy, .hero-visual, [data-reveal], .group-introduction, .section-heading, ' +
        '.news-entry, .memberbox, .paperbox, .publication-citation, .publication-row, .contact-card, .cohort-list, ' +
        '.gallery-item, .homes-directory-link, .homes-introduction, .page-content h2, .page-content img';
      var targets = Array.from(document.querySelectorAll(selector)).filter(function (element) {
        // Animate a card as a unit rather than animating its image and heading twice.
        return !element.parentElement.closest(selector);
      });
      var observer;
      function show(element) {
        element.classList.add('is-revealed');

      }
      function showAll() {
        targets.forEach(show);
        if (observer) observer.disconnect();
      }
      try {
        observer = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) show(entry.target);
            else if (!entry.target.contains(document.activeElement)) entry.target.classList.remove('is-revealed');
          });
        }, { threshold: 0, rootMargin: '0px 0px -16px 0px' });
        targets.forEach(function (element) {
          element.classList.add('scroll-reveal');
          observer.observe(element);
        });
        // Tab navigation must never land on an invisible link or control.
        document.addEventListener('focusin', function (event) {
          var element = event.target.closest('.scroll-reveal');
          if (element) show(element);
        });
        if (motionPreference.addEventListener) {
          motionPreference.addEventListener('change', function (event) {
            if (event.matches) showAll();
          });
        }
      } catch (error) {
        showAll();
      }
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
}());
