# Crypto Lab

Aplikasi web untuk mengenkripsi dan mendekripsi teks serta memvisualisasikan lima
algoritma cipher klasik secara langkah demi langkah.

| Algoritma | Keluarga | Kunci |
|-----------|----------|-------|
| Caesar | Substitusi monoalfabetik | Geseran angka (0–25) |
| Vigenère | Substitusi polialfabetik | Kata kunci |
| Columnar Transposition | Transposisi | Kata kunci |
| Playfair | Substitusi digraf (matriks 5×5) | Kata kunci |
| Keyword Substitution | Substitusi monoalfabetik | Kata kunci |

Seluruh logika algoritma ditulis di Python (`algorithms/`). Frontend Svelte 5 hanya
menangani tampilan dan visualisasi, lalu memanggil logika tersebut lewat API — tidak ada
duplikasi algoritma di sisi JavaScript.

## Arsitektur

```
Browser (Svelte 5)          HTTP/JSON               Flask (Python)
UI + visualisasi      ──── POST /api/<cipher> ────  app.py
                      ◀──── langkah + hasil ─────  algorithms/*.py
```

Python mengembalikan data langkah (indeks, aturan, matriks, dan seterusnya). UI cukup
merendernya menjadi tabel atau animasi; perhitungan visualisasi tidak diulang di JS.

## Struktur direktori

```
crypto-web/
├── algorithms/                 logika cipher (Python murni, tanpa dependensi)
│   ├── common.py               fungsi bersama (alfabet, pembersih teks)
│   ├── caesar.py
│   ├── vigenere.py             termasuk Tabula Recta
│   ├── transposition.py        columnar transposition
│   ├── playfair.py             matriks 5×5
│   ├── substitution.py         keyword substitution
│   └── _selftest.py            uji round-trip cepat
├── app.py                      Flask: API + menyajikan hasil build
├── requirements.txt
├── Procfile
├── runtime.txt
├── render.yaml                 blueprint Render
└── frontend/                   Svelte 5 + Vite + Tailwind CSS
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── dist/                   hasil build (di-commit)
    └── src/
        ├── main.js
        ├── app.css
        ├── App.svelte
        └── lib/
            ├── api.js
            └── components/     CaesarViz, VigenereViz, TranspositionViz,
                                PlayfairViz, SubstitutionViz
```

## Menjalankan di lokal

Backend:

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
pip install -r requirements.txt
python app.py                    # http://127.0.0.1:5000
```

Frontend dalam mode pengembangan (terminal terpisah):

```bash
cd frontend
npm install
npm run dev                      # http://127.0.0.1:5173, proxy /api ke :5000
```

Build produksi (satu server):

```bash
cd frontend && npm run build
cd .. && python app.py
```

Uji algoritma tanpa UI:

```bash
python algorithms/_selftest.py
```

## API

| Method | Endpoint | Body | Keterangan |
|--------|----------|------|------------|
| GET | `/api/ciphers` | — | daftar cipher + metadata |
| GET | `/api/<cipher>` | — | info satu cipher |
| POST | `/api/<cipher>` | `{"text", "key", "mode"}` | hasil + langkah visualisasi |

`mode` bernilai `"encrypt"` atau `"decrypt"`.

```bash
curl -X POST http://127.0.0.1:5000/api/vigenere \
  -H "Content-Type: application/json" \
  -d '{"text":"HALO DUNIA","key":"KUNCI","mode":"encrypt"}'
```

```json
{
  "cipher": "vigenere",
  "result": "RUYQLEHVC",
  "steps": [
    { "char": "H", "p_index": 7, "key_char": "K", "k_index": 10, "new_index": 17, "cipher": "R" }
  ],
  "tabula_recta": [["A", "B", "..."]]
}
```

## Deploy

Heroku sudah berbayar sejak November 2022, dan Hugging Face Docker Spaces berbayar sejak
2025. Opsi yang tetap gratis:

### Render (rekomendasi)

Repo menyertakan `render.yaml`. Buka <https://dashboard.render.com/blueprints>, pilih
**New Blueprint Instance**, hubungkan repo `crypto-web`, lalu **Deploy**.

Cara manual: **New → Web Service**, dengan pengaturan:

- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60`

Free tier Render tertidur saat tidak dipakai, tetapi bangun otomatis ketika diakses
(cold start sekitar 30–60 detik).

### Alternatif

| Platform | Catatan |
|----------|---------|
| Railway | Trial credit, Procfile terdeteksi otomatis |
| Fly.io | `fly launch`; butuh kartu, tidak ditagih selama masih dalam free allowance |
| Cloudflare Quick Tunnel | Tanpa akun, tetapi URL hanya aktif selama server lokal berjalan |

Pada semua platform, pastikan `frontend/dist` sudah di-build — buildpack Python tidak
menjalankan `npm run build`, sehingga hasil build di-commit ke repo.

## Catatan algoritma

- **Caesar** — `C = (P + k) mod 26`. Hanya 25 kunci; brute force tersedia saat dekripsi.
- **Vigenère** — `C = (P + K) mod 26`, kunci diulang. Menghapus pola frekuensi, tetapi
  dapat dipatahkan dengan Kasiski test bila panjang kunci tertebak.
- **Columnar Transposition** — huruf tidak diganti, hanya urutannya diacak mengikuti
  urutan kolom dari kunci. Sel kosong diisi `X`.
- **Playfair** — substitusi per pasangan huruf melalui matriks 5×5 dari kata kunci
  (J digabung ke I). Baris sama digeser ke kanan, kolom sama digeser ke bawah, selain itu
  kolomnya ditukar.
- **Keyword Substitution** — tabel cipher dibangun dari kata kunci (huruf unik lebih dulu,
  lalu sisa alfabet). Contoh: `ZEBRA` menjadi `ZEBRACDFGHIJKLMNOPQSTUVWXY`.

Substitusi mengubah identitas huruf; transposisi mengubah urutannya.

## Teknologi

- Python 3.12 · Flask 3 · flask-cors · gunicorn
- Svelte 5 · Vite 8 · Tailwind CSS 4
- Logika cipher hanya memakai pustaka standar Python
