# Stuck Preview Fix

A tiny, open-source Manifest V3 extension that stops YouTube inline/video-card previews from continuing to play after you middle-click a video or right-click it to open it in a new tab.

The extension is intentionally narrow: no popup, no settings page, no background service worker, no analytics, no storage, and no network calls.

## The bug

With YouTube's **Video previews** / inline playback enabled, opening a video from the Home page or a channel's Videos grid in a new tab can leave the preview playing in the original tab. Clicking empty page space stops it, which indicates that YouTube's normal preview-cleanup state was not triggered by the browser's new-tab path.

## What this extension does

On a video-card middle-click or right-click, it:

1. Blurs any focused element left active by YouTube.
2. Pauses preview `<video>` elements only inside the clicked card.
3. Dispatches pointer/mouse leave events to the link/card.
4. Dispatches a neutral click to the YouTube app shell, mirroring the manual “click empty space” workaround.
5. Repeats cleanup at 0 ms, 60 ms, and 180 ms to cover YouTube asynchronously replacing preview DOM.

It never cancels the original mouse action, so the browser still opens the link or native context menu normally.

## Browser support

The same Manifest V3 package is designed for:

- Google Chrome
- Microsoft Edge
- Chromium
- Thorium
- Brave and other Chromium-based browsers that support standard MV3 content scripts

The extension uses no browser-specific extension API.

## Get the extension

<table>
  <tr>
    <td align="center" width="180">
      <a href="https://microsoftedge.microsoft.com/addons/detail/stuck-preview-fix/igkgbonnjdjpbhjiaodhhkmbogodplln" target="_blank" rel="noopener noreferrer">
        <img src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Microsoft_Edge_logo_%282019%29.svg" alt="Microsoft Edge" width="96" height="96">
      </a>
      <br>
      <a href="https://microsoftedge.microsoft.com/addons/detail/stuck-preview-fix/igkgbonnjdjpbhjiaodhhkmbogodplln" target="_blank" rel="noopener noreferrer"><strong>Microsoft Edge</strong></a>
    </td>
    <td align="center" width="180">
      <a href="https://github.com/sameraskar/Stuck-Preview-Fix-for-YouTube/releases" target="_blank" rel="noopener noreferrer">
        <img src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Google_Chrome_icon_%28February_2022%29.svg" alt="Google Chrome" width="96" height="96">
      </a>
      <br>
      <a href="https://github.com/sameraskar/Stuck-Preview-Fix-for-YouTube/releases" target="_blank" rel="noopener noreferrer"><strong>Download</strong></a>
      <br>
      <sub>(Store coming soon)</sub>
    </td>
  </tr>
</table>

## Install locally

### Chrome / Chromium / Thorium

1. Download or clone this repository.
2. Run `python scripts/build.py` from the repository root.
3. Open `chrome://extensions`.
4. Enable **Developer mode**.
5. Click **Load unpacked**.
6. Select `dist/stuck-preview-fix`.
7. Reload YouTube.

### Microsoft Edge

1. Build the extension with `python scripts/build.py`.
2. Open `edge://extensions`.
3. Enable **Developer mode**.
4. Click **Load unpacked**.
5. Select `dist/stuck-preview-fix`.
6. Reload YouTube.

## Build

No npm dependencies, bundler, transpiler, minifier, or generated JavaScript are used.

```bash
python scripts/build.py
```

The build script validates the manifest, copies the readable source into `dist/stuck-preview-fix`, and creates store upload packages in `dist/packages/`.

Outputs:

- `dist/stuck-preview-fix/` - unpacked extension
- `dist/packages/stuck-preview-fix-1.0.0-chrome.zip`
- `dist/packages/stuck-preview-fix-1.0.0-edge.zip`

The Chrome and Edge ZIP files intentionally contain identical extension code.

## Userscript version

A Tampermonkey/Violentmonkey-compatible version is included at:

`userscript/stuck-preview-fix.user.js`

It implements the same behavior with `@grant none`.

## Privacy

See [PRIVACY.md](PRIVACY.md). In short: no data collection, analytics, storage, or external requests.

## Debugging

`src/content.js` contains:

```js
const DEBUG = false;
```

Set it to `true` temporarily if YouTube changes its DOM and you need console diagnostics. Release/store builds should keep it `false`.

## Store publishing

See [STORE_SUBMISSION.md](STORE_SUBMISSION.md) for ready-to-paste Chrome Web Store and Microsoft Edge Add-ons text, privacy answers, reviewer notes, asset sizes, and submission checklist.

## Contributing

Bug reports are especially useful if they include:

- browser and version
- YouTube page type (Home, channel Videos tab, search, etc.)
- whether Video previews / inline playback is enabled
- whether the trigger was middle-click or right-click
- the relevant card HTML/selector if YouTube changed its DOM

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Trademark notice

This project is an independent browser extension and is not affiliated with, endorsed by, or sponsored by Google LLC or YouTube. YouTube is a trademark of Google LLC. The project name and icon intentionally do not use YouTube branding.

## License

MIT, see [LICENSE](LICENSE).
