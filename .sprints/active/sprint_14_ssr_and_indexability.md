# Sprint 14: Server-Side Rendering for /data Indexability

## Objective

Make the `/data` route fully indexable by Google, LLM web fetchers (Claude, GPT Browse), and other crawlers that do not execute JavaScript. The current SPA shell is invisible to these clients; the structured data and `useEffect` head updates added in Sprint 13 are a partial mitigation, not a full solution.

## Background

- `/data` uses React 19 `use()` + Suspense — fully client-rendered.
- LLM fetchers (Claude web fetch, GPT Browse, Bing crawler) receive an empty HTML shell.
- Googlebot can execute JS but lags days–weeks on JS-rendered content.
- Structured data (`id="data-page-jsonld"`) and `useEffect` title/description updates were added as a Sprint 13 stopgap.
- The long-term fix is server-side rendering for this route.

## Approach options (ranked)

### Option A — Django template view for `/data` (recommended for this stack)

Add a Django view that:
1. Calls `SODAService().get_city_stats()` (already cached 6h)
2. Renders a Django template with the full data as semantic HTML — same content as `DataStories.tsx`
3. Includes populated `<meta name="description">`, `<title>`, and `<script type="application/ld+json">` with live stats

Routing:
- Configure Render (or nginx) to serve `/data` from Django for User-Agents matching known crawlers
- Browsers with `Accept: text/html` + no bot UA get the React SPA as normal
- Alternatively: use a dedicated `/data.html` route that always serves the Django view, with `<link rel="canonical" href="/data">` pointing back to the SPA

**Pros:** No framework migration. Reuses existing cache. Full HTML for all crawlers.
**Cons:** Maintains two renderings of the same UI (React + Django template). Routing logic needed.

### Option B — Vite SSG (Static Site Generation)

Use `vite-plugin-ssg` or `@vitejs/plugin-ssr` to pre-render `/data` at build time.

**Pros:** Single codebase. Standard Vite ecosystem.
**Cons:** Requires build-time API access (city-stats must be fetchable during `npm run build`). Stale between builds; `/data` data changes daily.

### Option C — Next.js migration

Migrate frontend to Next.js with `generateStaticParams` or `getServerSideProps` for `/data`.

**Pros:** Full SSR/SSG support, best-in-class for this use case.
**Cons:** Full framework migration. Significant rewrite of all components.

## Recommended implementation (Option A)

### Backend tasks

- [ ] Add `DataStoriesView` in `buildings_app/views.py` — calls `SODAService().get_city_stats()`, renders `buildings_app/templates/data_stories.html`
- [ ] Create `backend/buildings_app/templates/data_stories.html` — semantic HTML matching DataStories.tsx content; includes populated JSON-LD with live stats
- [ ] Add URL route: `path('data-ssr/', DataStoriesView.as_view())` in `buildings_app/urls.py`
- [ ] Add `<link rel="canonical" href="https://elevatoradvocate.nyc/data">` in the template

### Frontend tasks

- [ ] Add `<link rel="alternate" href="https://elevatoradvocate.nyc/data-ssr/">` to DataPage head (signals crawler-friendly version exists)
- [ ] Update `sitemap.xml` to include `/data` with `<changefreq>daily</changefreq>`

### Render / routing tasks

- [ ] Evaluate bot-detection middleware in Django (`django-user-agents`) to transparently serve the template view at `/data` for known crawlers, React SPA for browsers
- [ ] OR: document `/data-ssr/` as the canonical crawler URL and submit it to Google Search Console

## Notes

- `SODAService.get_city_stats()` is already cached for 6 hours — the Django template view adds zero extra SODA load
- The Django template does not need to match the React design precisely; semantic HTML with the data is sufficient for indexability
- The `id="data-page-jsonld"` script in `index.html` and the `useEffect` head updates in `DataStoriesInner` remain as the client-side complement; they are not removed by this sprint
