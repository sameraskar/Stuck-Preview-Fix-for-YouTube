# Contributing

Contributions are welcome, especially compatibility fixes after YouTube DOM changes.

## Development rules

- Keep the project single-purpose.
- Do not add telemetry, analytics, advertising, tracking, or network requests.
- Avoid extension permissions unless they are strictly required for the existing purpose.
- Do not prevent the browser's normal middle-click or context-menu behavior.
- Do not pause the main YouTube watch-page player.
- Keep store builds readable and unminified.

## Test matrix

Before submitting a pull request, test as many as possible:

- Chrome stable
- Microsoft Edge stable
- Chromium/Thorium
- YouTube Home
- Channel Videos tab
- Search results/video grids
- Middle-click on thumbnail/title
- Right-click on thumbnail/title and then Open link in new tab

Run:

```bash
python scripts/build.py
python scripts/validate.py
```
