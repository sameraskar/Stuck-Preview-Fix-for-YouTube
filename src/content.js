(() => {
  'use strict';

  // Set to true only when diagnosing a YouTube DOM change.
  // Keep false in release/store builds.
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

  function log(...args) {
    if (DEBUG) console.debug('[Stuck Preview Fix]', ...args);
  }

  function findVideoContext(target) {
    if (!(target instanceof Element)) return null;

    const directLink = target.closest(VIDEO_LINK_SELECTOR);
    const card = target.closest(CARD_SELECTOR);
    const link = directLink || card?.querySelector(VIDEO_LINK_SELECTOR);

    if (!link) return null;

    return {
      link,
      card: card || link.closest(CARD_SELECTOR)
    };
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
      element.dispatchEvent(
        new PointerEvent('pointerleave', { ...common, bubbles: false })
      );
    } catch (_) {
      // PointerEvent exists in current Chromium/Edge. MouseEvent below is the
      // fallback if a browser or embedded context does not expose it.
    }

    element.dispatchEvent(new MouseEvent('mouseout', common));
    element.dispatchEvent(
      new MouseEvent('mouseleave', { ...common, bubbles: false })
    );
  }

  function pausePreviewVideos(card) {
    if (!card?.isConnected) return;

    // Restrict this to the clicked video card so the main /watch player is not
    // touched. Inline previews use <video> elements inside the card.
    card.querySelectorAll('video').forEach((video) => {
      try {
        video.pause();
      } catch (_) {
        // A disappearing preview node is harmless; the later cleanup passes
        // cover YouTube replacing preview DOM asynchronously.
      }
    });
  }

  function blurActiveElement() {
    const active = document.activeElement;
    if (active instanceof HTMLElement && active !== document.body) {
      active.blur();
    }
  }

  function dispatchNeutralClick() {
    // Clicking empty page space manually clears the stuck preview. Dispatching
    // a neutral click on the app shell triggers the same global cleanup path
    // without navigating or preventing the user's original action.
    const neutral = document.querySelector('ytd-app') || document.body;
    if (!neutral) return;

    neutral.dispatchEvent(
      new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        composed: true,
        view: window
      })
    );
  }

  function clearStuckPreview(context) {
    blurActiveElement();
    pausePreviewVideos(context.card);
    dispatchLeave(context.link);
    dispatchLeave(context.card);
    dispatchNeutralClick();
    log('Preview cleanup applied', context);
  }

  function scheduleCleanup(context) {
    // YouTube may update or replace the inline-preview DOM immediately after a
    // new tab/context menu action. A few tiny delayed passes make the fix more
    // reliable without polling or keeping any background process alive.
    [0, 60, 180].forEach((delay) => {
      window.setTimeout(() => clearStuckPreview(context), delay);
    });
  }

  document.addEventListener(
    'auxclick',
    (event) => {
      // Middle mouse button. Never preventDefault(), so the browser keeps its
      // normal "open link in new tab" behavior.
      if (event.button !== 1) return;

      const context = findVideoContext(event.target);
      if (context) scheduleCleanup(context);
    },
    true
  );

  document.addEventListener(
    'contextmenu',
    (event) => {
      // A webpage cannot know which command is later chosen in the browser's
      // native context menu. Clear the preview as soon as a video link/card is
      // right-clicked. We do not preventDefault(), so the menu opens normally.
      const context = findVideoContext(event.target);
      if (context) scheduleCleanup(context);
    },
    true
  );
})();
