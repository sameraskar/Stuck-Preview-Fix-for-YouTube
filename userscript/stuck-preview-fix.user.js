// ==UserScript==
// @name         Stuck Preview Fix
// @namespace    https://github.com/sameraskar/Stuck-Preview-Fix-for-YouTube
// @version      1.0.0
// @description  Stops stuck video previews on YouTube after middle-click or right-clicking a video to open it in a new tab.
// @match        https://www.youtube.com/*
// @run-at       document-start
// @grant        none
// @license      MIT
// ==/UserScript==

(() => {
  'use strict';

  const DEBUG = false;
  const CARD_SELECTOR = [
    'ytd-rich-item-renderer',
    'ytd-rich-grid-media',
    'ytd-video-renderer',
    'ytd-grid-video-renderer',
    'yt-lockup-view-model'
  ].join(',');

  const VIDEO_LINK_SELECTOR = [
    'a[href^="/watch"]',
    'a[href^="/shorts/"]',
    'a[href^="/live/"]',
    'a[href*="youtube.com/watch"]',
    'a[href*="youtube.com/shorts/"]',
    'a[href*="youtube.com/live/"]'
  ].join(',');

  const log = (...args) => DEBUG && console.debug('[Stuck Preview Fix]', ...args);

  function findVideoContext(target) {
    if (!(target instanceof Element)) return null;
    const directLink = target.closest(VIDEO_LINK_SELECTOR);
    const card = target.closest(CARD_SELECTOR);
    const link = directLink || card?.querySelector(VIDEO_LINK_SELECTOR);
    return link ? { link, card: card || link.closest(CARD_SELECTOR) } : null;
  }

  function dispatchLeave(element) {
    if (!element?.isConnected) return;
    const common = {
      bubbles: true,
      cancelable: false,
      composed: true,
      relatedTarget: document.body,
      view: window
    };
    try {
      element.dispatchEvent(new PointerEvent('pointerout', common));
      element.dispatchEvent(new PointerEvent('pointerleave', { ...common, bubbles: false }));
    } catch (_) {}
    element.dispatchEvent(new MouseEvent('mouseout', common));
    element.dispatchEvent(new MouseEvent('mouseleave', { ...common, bubbles: false }));
  }

  function clearStuckPreview({ link, card }) {
    const active = document.activeElement;
    if (active instanceof HTMLElement && active !== document.body) active.blur();

    if (card?.isConnected) {
      card.querySelectorAll('video').forEach((video) => {
        try { video.pause(); } catch (_) {}
      });
    }

    dispatchLeave(link);
    dispatchLeave(card);

    const neutral = document.querySelector('ytd-app') || document.body;
    neutral?.dispatchEvent(new MouseEvent('click', {
      bubbles: true,
      cancelable: true,
      composed: true,
      view: window
    }));

    log('Preview cleanup applied');
  }

  function scheduleCleanup(context) {
    [0, 60, 180].forEach((delay) => {
      window.setTimeout(() => clearStuckPreview(context), delay);
    });
  }

  document.addEventListener('auxclick', (event) => {
    if (event.button !== 1) return;
    const context = findVideoContext(event.target);
    if (context) scheduleCleanup(context);
  }, true);

  document.addEventListener('contextmenu', (event) => {
    const context = findVideoContext(event.target);
    if (context) scheduleCleanup(context);
  }, true);
})();
