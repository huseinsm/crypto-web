"""
vigenere.py — Vigenère Cipher (substitusi polialfabetik).

Enkripsi : C = (P + K) mod 26
Dekripsi : P = (C - K) mod 26
Kunci diulang mengikuti panjang pesan.
Visualisasi: tabel per-huruf + baris kunci berulang + tabel Vigenère (Tabula Recta).
"""

from common import ALPHABET, only_letters


def build_tabula_recta() -> list:
    """Tabel Vigenère 26x26 (Tabula Recta) untuk visualisasi."""
    rows = []
    for r in range(26):
        rows.append([ALPHABET[(r + c) % 26] for c in range(26)])
    return rows


def process(text: str, key: str, mode: str = "encrypt") -> dict:
    key_clean = only_letters(key)
    if not key_clean:
        raise ValueError("Kunci tidak boleh kosong (harus mengandung huruf).")

    clean = only_letters(text)
    sign = 1 if mode == "encrypt" else -1

    key_stream = [key_clean[i % len(key_clean)] for i in range(len(clean))]

    out = []
    steps = []
    for i, ch in enumerate(clean):
        kch = key_stream[i]
        pi = ALPHABET.index(ch)
        ki = ALPHABET.index(kch)
        ni = (pi + sign * ki) % 26
        out.append(ALPHABET[ni])
        steps.append({
            "i": i,
            "char": ch,
            "p_index": pi,
            "key_char": kch,
            "k_index": ki,
            "new_index": ni,
            "cipher": ALPHABET[ni],
        })

    return {
        "cipher": "vigenere",
        "mode": mode,
        "key": {"key": key_clean},
        "alphabet": ALPHABET,
        "input_clean": clean,
        "key_stream": "".join(key_stream),
        "result": "".join(out),
        "steps": steps,
        "tabula_recta": build_tabula_recta(),
    }
