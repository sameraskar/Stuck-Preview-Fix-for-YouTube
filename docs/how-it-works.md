# How the fix works

The observed failure mode is not simply a CSS focus style. YouTube appears to leave an inline-preview interaction state alive when the browser opens a link through a path that bypasses YouTube's normal left-click/navigation cleanup.

The strongest practical clue is that manually clicking empty page space stops the stuck preview.

The extension therefore reconstructs several normal cleanup signals instead of relying on one undocumented YouTube attribute:

1. **Blur** - removes lingering DOM focus.
2. **Pause card-local preview video** - immediately silences/stops the preview without touching the main player.
3. **Pointer/mouse leave** - asks YouTube's existing hover/preview handlers to tear down the card state.
4. **Neutral app-shell click** - triggers the same broad deselection path as clicking empty space.
5. **Short delayed repeats** - handles preview nodes that YouTube replaces just after the new-tab/context-menu action.

This is intentionally defensive. It avoids depending on a single unstable internal attribute such as `selected`, `is-active`, or a Polymer implementation detail that YouTube may rename.

## Trigger behavior

### Middle-click

Chromium exposes the middle mouse button through `auxclick` with `button === 1`. The listener never calls `preventDefault()`, so normal browser new-tab behavior is preserved.

### Right-click

The page receives `contextmenu` before the user chooses an item from the browser-owned native context menu. Page JavaScript cannot reliably learn which native command is chosen afterward, so the extension clears the preview immediately on a right-clicked video card. The context menu itself is not blocked.
