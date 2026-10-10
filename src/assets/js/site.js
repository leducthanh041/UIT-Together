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
      function update() {
        var query = input ? normalize(input.value) : '';
        var year = select ? select.value : '';
        var type = typeSelect ? typeSelect.value : '';
        var venue = venueSelect ? venueSelect.value : '';
        var words = query.split(/\s+/).filter(Boolean);
        var count = 0;
        records.forEach(function (record) {
          var visible = !record.initiallyHidden && words.every(function (word) { return record.text.indexOf(word) !== -1; }) && (!year || year === 'all' || record.year === year) && (!type || record.type === type) && (!venue || record.venue === venue);
          record.element.hidden = !visible;
          if (visible) count += 1;
        });
        scope.querySelectorAll('[data-venue-group]').forEach(function (group) {
          group.hidden = !records.some(function (record) { return !record.element.hidden && group.contains(record.element); });
        });
        status.textContent = count + ' / ' + records.filter(function (record) { return !record.initiallyHidden; }).length + (vietnamese ? ' kết quả' : ' results');
        empty.hidden = count > 0;
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
        if (observer) observer.unobserve(element);
      }
      function showAll() {
        targets.forEach(show);
        if (observer) observer.disconnect();
      }
      try {
        observer = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) show(entry.target);
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
