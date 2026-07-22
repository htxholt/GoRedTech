# GoRedTech website

The public site is generated from modular source in `site-src/`.

## Build

```bash
python3 build.py
```

The build writes a flat, dependency-free site to `dist/` for GitHub Pages. Shared header, footer, metadata, styles, scripts, and assets remain modular in source.

## Publish

After validating `dist/`, copy only the generated site files into the repository root while preserving the unrelated `landstock/` directory, then commit and push `main`.

Do not edit generated root HTML directly. Change `site-src/`, rebuild, and republish.
