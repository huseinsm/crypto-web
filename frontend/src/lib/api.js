// api.js — pembungkus panggilan ke backend Python (Flask).
// Saat dev, Vite mem-proxy /api ke http://127.0.0.1:5000 (lihat vite.config.js).
const BASE = import.meta.env?.VITE_API_BASE ?? ''

export async function fetchCiphers() {
  const r = await fetch(`${BASE}/api/ciphers`)
  if (!r.ok) throw new Error('Gagal memuat daftar cipher')
  return r.json()
}

export async function runCipher(name, { text, key, mode }) {
  const r = await fetch(`${BASE}/api/${name}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, key, mode })
  })
  const data = await r.json().catch(() => ({}))
  if (!r.ok) throw new Error(data.error || 'Terjadi kesalahan pada server')
  return data
}
