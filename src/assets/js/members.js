/* Natural document scrolling: independent member reveals and section links. */
(function () {
  'use strict';
  const directory = document.querySelector('.member-directory');
  if (!directory) return;
  const chapters = Array.from(directory.querySelectorAll('[data-member-chapter]'));
  const panels = Array.from(directory.querySelectorAll('[data-member-reveal]'));
  const nav = directory.querySelector('[data-member-nav]');
  const links = Array.from(nav.querySelectorAll('a'));
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  function setActive(id) {
    links.forEach(link => {
      if (link.getAttribute('href') === '#' + id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  function offsets() {
    const header = document.querySelector('.site-header');
    const height = header ? header.getBoundingClientRect().height : 84;
    document.documentElement.style.setProperty('--member-header-height', height + 'px');
    document.documentElement.style.setProperty('--member-anchor-offset', height + nav.getBoundingClientRect().height + 32 + 'px');
  }
  offsets();
  window.addEventListener('resize', offsets);
  if ('ResizeObserver' in window) {
    const sizes = new ResizeObserver(offsets);
    sizes.observe(nav);
    const header = document.querySelector('.site-header');
    if (header) sizes.observe(header);
  }
      // Capture document and nested-container scrolling; upward reveals are immediate.
      var scrollPositions = new WeakMap();
      if (document.scrollingElement) scrollPositions.set(document.scrollingElement, document.scrollingElement.scrollTop || 0);
      var scrollingDown = true;
      document.addEventListener('scroll', function (event) {
        var scroller = event.target === document ? document.scrollingElement : event.target;
        if (!scroller) return;
        var current = scroller.scrollTop || 0;
        var previous = scrollPositions.get(scroller) || 0;
        if (current === previous) return;
        scrollingDown = current > previous;
        scrollPositions.set(scroller, current);
        panels.forEach(function (element) {
          if (scrollingDown) element.classList.remove('member-instant');
          else element.classList.add('member-instant');
        });
      }, {capture: true, passive: true});
  function showAll() {
    panels.forEach(chapter => chapter.classList.add('is-member-visible'));
  }
  if ('IntersectionObserver' in window) {
    const visible = new Set();
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          visible.add(entry.target);
        } else {
          visible.delete(entry.target);
        }
      });
      const candidates = chapters.filter(chapter => !chapter.hidden && visible.has(chapter));
      const current = candidates.find(chapter => chapter.getBoundingClientRect().top >= 0) || candidates[candidates.length - 1];
      if (current) setActive(current.id);
    }, { threshold: 0, rootMargin: '-150px 0px -20% 0px' });
    chapters.forEach(chapter => observer.observe(chapter));
    try {
      const reveal = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) entry.target.classList.add('is-member-visible');
          else if (!motion.matches && !entry.target.contains(document.activeElement)) entry.target.classList.remove('is-member-visible');
        });
      }, { threshold: 0.08, rootMargin: '0px 0px -32px 0px' });
      panels.forEach((panel, index) => {
        if (!motion.matches) panel.classList.add('has-member-motion');
        // Small alternating delays; later rows never wait for previous rows.
        panel.style.setProperty('--member-reveal-delay', index % 2 ? '80ms' : '0ms');
        reveal.observe(panel);
      });
    } catch (_) { showAll(); }
  } else showAll();
  nav.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (link && nav.contains(link)) setActive(link.getAttribute('href').slice(1));
    // Keep the browser's anchor behavior, history and keyboard navigation.
  });
  document.addEventListener('focusin', event => {
    const chapter = event.target.closest('[data-member-reveal]');
    if (chapter) {
      chapter.classList.add('is-member-visible');
      const parent = chapter.closest('[data-member-chapter]');
      if (parent) { parent.classList.add('is-member-visible'); setActive(parent.id); }
    }
  });
  if (motion.addEventListener) motion.addEventListener('change', event => { if (event.matches) showAll(); });
  const main = directory.closest('main');
  function filterChanged() {
    chapters.forEach(chapter => {
      const link = links.find(item => item.getAttribute('href') === '#' + chapter.id);
      if (link) link.hidden = chapter.hidden;
    });
    const first = chapters.find(chapter => !chapter.hidden);
    if (first) setActive(first.id);
  }
  main.addEventListener('input', filterChanged);
  main.addEventListener('change', filterChanged);
  main.addEventListener('click', event => { if (event.target.closest('[data-filter-reset]')) filterChanged(); });
}());
