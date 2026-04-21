# Frontend/Backend Address Configuration

This project now keeps frontend-to-backend address settings in a small set of files so port or host changes can be done without touching business code.

## Main config files

- `backend/config.py`
  - Backend `HOST` / `PORT` default runtime settings
- `frontend/.env.development`
  - `VITE_API_BASE_URL`
  - `VITE_DEV_PROXY_TARGET`
  - `VITE_BACKEND_ORIGIN`
- `frontend/.env.production`
  - `VITE_API_BASE_URL`
  - `VITE_BACKEND_ORIGIN`
- `frontend/vite.config.ts`
  - Reads `VITE_DEV_PROXY_TARGET`
  - Proxies `/api`, `/images`, `/exports` in dev mode

## What each variable does

- Backend `PORT`
  - Backend runtime port used by `python main.py`
  - Default is now `18080`
  - Can be overridden with the `PORT` environment variable

- `VITE_API_BASE_URL`
  - API prefix used by axios and direct API downloads.
  - Recommended value for same-origin deployment: `/api/v1`
  - Example cross-origin value: `https://api.example.com/api/v1`

- `VITE_DEV_PROXY_TARGET`
  - Dev-only Vite proxy target.
  - Change this when backend host or port changes during local development.
  - Example: `http://127.0.0.1:18080`

- `VITE_BACKEND_ORIGIN`
  - Optional override for backend-origin resources such as `/images/...` and `/exports/...`.
  - Leave empty when frontend and backend are served under the same host/reverse proxy.
  - Example: `https://api.example.com`

## Recommended setups

### Local development

```env
VITE_API_BASE_URL=/api/v1
VITE_DEV_PROXY_TARGET=http://127.0.0.1:18080
VITE_BACKEND_ORIGIN=
```

### Production behind one reverse proxy

```env
VITE_API_BASE_URL=/api/v1
VITE_BACKEND_ORIGIN=
```

### Production with separate backend domain

```env
VITE_API_BASE_URL=https://api.example.com/api/v1
VITE_BACKEND_ORIGIN=https://api.example.com
```

## Code entry points changed in this update

- `frontend/src/utils/backendUrl.ts`
  - Central API/backend URL builder
- `frontend/src/api/request.ts`
  - Uses the centralized API base with a safe default
- `frontend/src/views/dataset/DatasetManagement.vue`
  - Dataset export now uses the configured API base directly
- `frontend/src/components/corpus/CorpusPreview.vue`
  - Image URLs now use the centralized backend URL builder
- `frontend/src/components/corpus/CorpusGroupedView.vue`
  - Image URLs now use the centralized backend URL builder
- `frontend/src/views/document/DataList.vue`
  - Preview image URLs now use the centralized backend URL builder

## Operational note

If remote devices access the Vite dev server by LAN IP, keep `VITE_API_BASE_URL=/api/v1`. Do not set it to `http://localhost:18080/api/v1`, or the browser will send requests to the remote device's own localhost instead of the development machine.
