const DEFAULT_API_BASE_URL = '/api/v1'

function stripTrailingSlash(value: string): string {
  return value.replace(/\/+$/, '')
}

function normalizePath(path: string): string {
  return path.startsWith('/') ? path : `/${path}`
}

function isAbsoluteUrl(value: string): boolean {
  return /^https?:\/\//i.test(value)
}

function getExplicitBackendOrigin(): string {
  const backendOrigin = stripTrailingSlash(import.meta.env.VITE_BACKEND_ORIGIN?.trim() || '')
  if (backendOrigin) {
    return backendOrigin
  }

  const apiBaseUrl = getApiBaseUrl()
  if (isAbsoluteUrl(apiBaseUrl)) {
    return new URL(apiBaseUrl).origin
  }

  return ''
}

export function getApiBaseUrl(): string {
  const configured = stripTrailingSlash(import.meta.env.VITE_API_BASE_URL?.trim() || '')
  return configured || DEFAULT_API_BASE_URL
}

export function buildApiUrl(path: string): string {
  return `${getApiBaseUrl()}${normalizePath(path)}`
}

export function buildBackendUrl(path: string): string {
  if (!path) {
    return ''
  }

  if (isAbsoluteUrl(path)) {
    return path
  }

  const normalizedPath = normalizePath(path)
  const backendOrigin = getExplicitBackendOrigin()
  return backendOrigin ? `${backendOrigin}${normalizedPath}` : normalizedPath
}
