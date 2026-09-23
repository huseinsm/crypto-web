"""
app.py — Flask API + penyaji UI (Svelte build).

Endpoints:
  POST /api/<cipher>   body: {text, key, mode}  -> JSON hasil + langkah visualisasi
  GET  /api/<cipher>                              -> info default cipher
  GET  /api/ciphers                               -> daftar cipher
  GET  /              -> UI (frontend/dist)

Dijalankan di Heroku: gunicorn app:app
"""

import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "algorithms"))

import caesar
import vigenere
import transposition
import playfair
import substitution

DIST = os.path.join(BASE, "frontend", "dist")

app = Flask(__name__, static_folder=DIST, static_url_path="")
CORS(app)

CIPHERS = {
    "caesar": {
        "label": "Caesar Cipher",
        "family": "Substitusi monoalfabetik",
        "key_label": "Geseran (angka)",
        "key_default": "3",
        "key_type": "number",
        "desc": "Setiap huruf digeser sejauh n pada alfabet. Contoh: A + 3 = D.",
    },
    "vigenere": {
        "label": "Vigen\u00e8re Cipher",
        "family": "Substitusi polialfabetik",
        "key_label": "Kata kunci",
        "key_default": "KUNCI",
        "key_type": "text",
        "desc": "Geseran berubah tiap huruf mengikuti kata kunci, menghancurkan pola frekuensi.",
    },
    "transposition": {
        "label": "Columnar Transposition",
        "family": "Transposisi",
        "key_label": "Kata kunci",
        "key_default": "KRIPTO",
        "key_type": "text",
        "desc": "Huruf tidak diganti \u2014 hanya urutannya diacak lewat urutan kolom hasil kunci.",
    },
    "playfair": {
        "label": "Playfair Cipher",
        "family": "Substitusi digraf",
        "key_label": "Kata kunci",
        "key_default": "MONARCHY",
        "key_type": "text",
        "desc": "Substitusi per pasangan huruf memakai matriks 5\u00d75 dari kata kunci.",
    },
    "substitution": {
        "label": "Keyword Substitution",
        "family": "Substitusi monoalfabetik",
        "key_label": "Kata kunci",
        "key_default": "ZEBRA",
        "key_type": "text",
        "desc": "Tabel substitusi dibangun dari kata kunci, lalu A\u2192tabel[0], B\u2192tabel[1], dst.",
    },
}

MODULES = {
    "caesar": caesar,
    "vigenere": vigenere,
    "transposition": transposition,
    "playfair": playfair,
    "substitution": substitution,
}


@app.get("/api/ciphers")
def list_ciphers():
    return jsonify({k: v for k, v in CIPHERS.items()})


@app.post("/api/<name>")
def run_cipher(name):
    if name not in MODULES:
        return jsonify({"error": f"Cipher '{name}' tidak dikenal."}), 404

    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    key = data.get("key", CIPHERS[name]["key_default"])
    mode = data.get("mode", "encrypt")

    if not text:
        return jsonify({"error": "Teks tidak boleh kosong."}), 400

    try:
        result = MODULES[name].process(text, key, mode)
        result["meta"] = CIPHERS[name]
        if name == "caesar":
            # sertakan tabel brute force saat dekripsi (pembelajaran)
            result["brute_force"] = caesar.brute_force(text) if mode == "decrypt" else []
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:  # noqa
        return jsonify({"error": f"Kesalahan: {e}"}), 500


@app.get("/api/<name>")
def info_cipher(name):
    if name not in CIPHERS:
        return jsonify({"error": "tidak ditemukan"}), 404
    return jsonify(CIPHERS[name])


# ---------- Sajikan UI (Svelte build) ----------
@app.get("/")
def index():
    if os.path.exists(os.path.join(DIST, "index.html")):
        return send_from_directory(DIST, "index.html")
    return (
        "<h1>crypto-web</h1><p>UI belum di-build. Jalankan: "
        "<code>cd frontend &amp;&amp; npm install &amp;&amp; npm run build</code></p>",
        200,
    )


@app.errorhandler(404)
def not_found(e):
    # SPA fallback
    if os.path.exists(os.path.join(DIST, "index.html")) and not request.path.startswith("/api/"):
        return send_from_directory(DIST, "index.html")
    return jsonify({"error": "not found"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
