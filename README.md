# GoRedTech website

The public RedTech site is generated from modular canonical source in `site-src/`.
Do not edit generated root HTML, root `css/`/`js/`, or `dist/` directly.

## Structure

- `site-src/pages/` — page body source
- `site-src/partials/` — shared head, header, and footer
- `site-src/css/` — modular stylesheets
- `site-src/js/` — modular progressive enhancement
- `site-src/assets/` — self-hosted production assets
- `build.py` — assembles and validates the flat site in `dist/`
- `publish.py` — copies validated output to the repository root while preserving unrelated directories

## Build and validate

```bash
python3 build.py
node --check site-src/js/navigation.js
node --check site-src/js/interactions.js
```

The builder fails on unresolved placeholders, broken local references, or an invalid count of primary page landmarks. It emits web-safe `755` directory and `644` file permissions.

## Repository publishing

After validating `dist/`:

```bash
python3 publish.py
```

This keeps the tracked repository-root output synchronized for source control and preserves the unrelated `landstock/` directory.

## Production deployment

The live domain is served from the isolated IONOS site leaf:

`/homepages/6/d4299715341/htdocs/goredtech/`

Deploy only validated `dist/` output to that exact leaf. Preserve the unrelated `landstock/` subdirectory during synchronization. Before a destructive checksum sync, create and verify a local rollback snapshot of the existing live leaf, inspect an itemized dry run, and confirm the destination path again.

After deployment, verify every HTML page and first-party CSS, JavaScript, and image asset over both the IONOS origin and the public Cloudflare-backed domain.
