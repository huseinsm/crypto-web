# 🔐 Crypto Lab — Visualisasi 5 Algoritma Cipher Klasik

Web interaktif untuk **mengenkripsi & mendekripsi** serta **memvisualisasikan langkah demi langkah** lima algoritma cipher klasik:

| # | Algoritma | Keluarga | Kunci |
|---|-----------|----------|-------|
| 1 | **Caesar** | Substitusi monoalfabetik | Geseran angka (0–25) |
| 2 | **Vigenère** | Substitusi polialfabetik | Kata kunci |
| 3 | **Columnar Transposition** | Transposisi | Kata kunci |
| 4 | **Playfair** | Substitusi digraf (matriks 5×5) | Kata kunci |
| 5 | **Keyword Substitution** | Substitusi monoalfabetik | Kata kunci |

> **Inti proyek:** seluruh *logika algoritma* ditulis di **Python** (`algorithms/`).
> Frontend **Svelte 5** hanya menangani tampilan & visualisasi, dan memanggil logika
> lewat API. Jadi tidak ada duplikasi algoritma di JavaScript.

---

## 🏗️ Arsitektur

```
┌─────────────────────────┐        HTTP/JSON        ┌──────────────────────────┐
│  Browser                │  ───────────────────▶   │  Flask (Python)          │
│  Svelte 5 + Vite        │   POST /api/<cipher>    │  app.py                  │
│  UI + Visualisasi       │  ◀───────────────────   │  algorithms/*.py         │
└─────────────────────────┘   langkah + hasil (JSON) └──────────────────────────┘
```

- Python mengembalikan **data langkah** (indeks, aturan, matriks, dsb.) → UI merendernya
  menjadi tabel/animasi. Visualisasi **tidak** dihitung ulang di JS.

---

## 📁 Struktur Direktori

```
crypto-web/
├── algorithms/                 # ← INTI: logika cipher (Python murni, tanpa dependensi)
│   ├── common.py               #   fungsi bersama (ALPHABET, pembersih teks, dll.)
│   ├── caesar.py               #   1. Caesar
│   ├── vigenere.py             #   2. Vigenère (+ Tabula Recta)
│   ├── transposition.py        #   3. Columnar Transposition
│   ├── playfair.py             #   4. Playfair (matriks 5×5)
│   ├── substitution.py         #   5. Keyword Substitution
│   └── _selftest.py            #   uji round-trip cepat (encrypt → decrypt)
│
├── app.py                      # Flask: API + menyajikan UI hasil build
├── requirements.txt            # dependensi Python (Flask, gunicorn)
├── Procfile                    # perintah start untuk Heroku
├── runtime.txt                 # versi Python untuk Heroku
│
└── frontend/                   # ← UI: Svelte 5 + Vite + Tailwind CSS
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── dist/                   # hasil build (di-commit agar Heroku tinggal jalan)
    └── src/
        ├── main.js
        ├── app.css
        ├── App.svelte          # halaman utama (form, mode, kontrol langkah)
        └── lib/
            ├── api.js          # pembungkus fetch ke Flask
            └── components/
                ├── CaesarViz.svelte
                ├── VigenereViz.svelte
                ├── TranspositionViz.svelte
                ├── PlayfairViz.svelte
                └── SubstitutionViz.svelte
```

---

## 🚀 Menjalankan di Lokal

### 1. Backend (Python)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python app.py          # jalan di http://127.0.0.1:5000
```

### 2. Frontend (Svelte) — mode pengembangan

Buka terminal lain:

```bash
cd frontend
npm install
npm run dev            # http://127.0.0.1:5173 (proxy /api ke :5000)
```

### 3. Build produksi (satu server)

```bash
cd frontend && npm run build     # hasil ke frontend/dist
cd .. && python app.py           # UI + API di http://127.0.0.1:5000
```

Cek algoritma tanpa UI:

```bash
python algorithms/_selftest.py
```

---

## 🔌 API

| Method | Endpoint | Body | Keterangan |
|--------|----------|------|------------|
| GET | `/api/ciphers` | — | daftar cipher + metadata |
| GET | `/api/<cipher>` | — | info satu cipher |
| POST | `/api/<cipher>` | `{ "text": "...", "key": "...", "mode": "encrypt"\|"decrypt" }` | hasil + langkah visualisasi |

Contoh:

```bash
curl -X POST http://127.0.0.1:5000/api/vigenere \
  -H "Content-Type: application/json" \
  -d '{"text":"HALO DUNIA","key":"KUNCI","mode":"encrypt"}'
```

```json
{
  "cipher": "vigenere",
  "result": "RUYQLEHVC",
  "steps": [ { "char": "H", "p_index": 7, "key_char": "K", "k_index": 10, "new_index": 17, "cipher": "R" }, ... ],
  "tabula_recta": [ ["A","B",...], ... ]
}
```

---

## ☁️ Deploy ke Heroku

Repo ini sudah **Heroku-ready**: `Procfile`, `requirements.txt`, `runtime.txt`, dan
`frontend/dist` yang sudah di-build.

```bash
# butuh Heroku CLI & akun berbayar
heroku login
heroku create nama-app-kamu

git init
git add .
git commit -m "Crypto Lab: 5 algoritma cipher + visualisasi"
git push heroku main        # atau: git push heroku master

heroku open
```

> ⚠️ **Heroku tidak lagi gratis** (sejak Nov 2022). Butuh dyno berbayar + kartu kredit.

### Alternatif gratis (kode sama, tinggal ganti platform)

| Platform | Cara |
|----------|------|
| **Render** | New → Web Service → Build: `pip install -r requirements.txt` · Start: `gunicorn app:app` |
| **Railway** | New Project → Deploy from repo (deteksi otomatis Procfile) |
| **Fly.io** | `fly launch` → pilih Python; `fly deploy` |

Untuk Render/Railway, pastikan **frontend sudah di-build** (`frontend/dist` ada), karena
buildpack Python tidak menjalankan `npm run build`.

---

## 🧠 Catatan Algoritma

**Caesar** — `C = (P + k) mod 26`. Hanya 25 kunci → lemah; sediakan *brute force* saat dekripsi.

**Vigenère** — `C = (P + K) mod 26`, kunci diulang. Menghancurkan pola frekuensi, tapi bisa
dipatahkan dengan **Kasiski test** bila panjang kunci tertebak.

**Columnar Transposition** — huruf **tidak diganti**, hanya urutannya diacak mengikuti urutan
kolom berdasarkan kunci. Sel kosong diisi `X`.

**Playfair** — substitusi **per pasangan huruf** lewat matriks 5×5 dari kata kunci
(J digabung ke I). Aturan: baris sama → geser kanan; kolom sama → geser bawah; beda keduanya → tukar kolom.

**Keyword Substitution** — tabel cipher dibangun dari kata kunci (huruf unik dulu, lalu sisa
alfabet). Contoh `ZEBRA` → `ZEBRACDFGHIJKLMNOPQSTUVWXY`.

> **Substitusi** mengubah *identitas* huruf · **Transposisi** mengubah *urutan* huruf.

---

## 🛠️ Teknologi

- **Python 3.12** · Flask 3 · flask-cors · gunicorn
- **Svelte 5** · Vite 8 · Tailwind CSS 4
- Tanpa dependensi eksternal untuk logika cipher (hanya pustaka standar Python).
