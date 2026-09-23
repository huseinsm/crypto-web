"""
transposition.py — Columnar Transposition Cipher (transposisi kolom).

Huruf TIDAK diganti, hanya URUTANNYA diacak berdasarkan kunci kata.
Langkah:
  1. Bersihkan teks, tulis baris per baris ke matriks dengan lebar = panjang kunci.
  2. Isi sel kosong dengan 'X'.
  3. Urutkan kolom berdasarkan huruf kunci (A=terkecil).
  4. Baca kolom sesuai urutan -> ciphertext.

Visualisasi: matriks asli + urutan kolom + matriks hasil baca.
"""

from common import ALPHABET, only_letters


def _key_order(key_clean: str) -> list:
    """Kembalikan urutan ranking tiap posisi kolom (untuk menangani huruf sama)."""
    ranked = sorted(range(len(key_clean)), key=lambda i: (key_clean[i], i))
    rank = [0] * len(key_clean)
    for pos, col in enumerate(ranked):
        rank[col] = pos
    return rank


def process(text: str, key: str, mode: str = "encrypt") -> dict:
    key_clean = only_letters(key)
    if not key_clean:
        raise ValueError("Kunci tidak boleh kosong (harus mengandung huruf).")

    ncol = len(key_clean)
    clean = only_letters(text)
    rank = _key_order(key_clean)
    # urutan kolom dari rank terkecil -> terbesar
    order = sorted(range(ncol), key=lambda c: rank[c])

    if mode == "encrypt":
        # bangun matriks baris
        nrow = (len(clean) + ncol - 1) // ncol
        padded = clean.ljust(nrow * ncol, "X")
        grid = [list(padded[r * ncol:(r + 1) * ncol]) for r in range(nrow)]
        result = "".join(
            "".join(grid[r][c] for r in range(nrow)) for c in order
        )
        return {
            "cipher": "transposition",
            "mode": mode,
            "key": {"key": key_clean},
            "key_rank": rank,
            "col_order": order,
            "ncol": ncol,
            "nrow": nrow,
            "input_clean": clean,
            "padded": padded,
            "grid": grid,
            "result": result,
            "note": "Sel kosong diisi huruf X. Kolom dibaca sesuai urutan kunci.",
        }

    # ---- DEKRIPSI ----
    L = len(clean)
    nrow = (L + ncol - 1) // ncol
    # kolom yang terisi penuh
    full = L % ncol or ncol
    col_lens = [nrow if rank[c] < full else nrow - 1 for c in range(ncol)]

    grid = [[""] * ncol for _ in range(nrow)]
    pos = 0
    for c in order:
        ln = col_lens[c]
        for r in range(ln):
            grid[r][c] = clean[pos]
            pos += 1

    result = "".join("".join(row) for row in grid)
    return {
        "cipher": "transposition",
        "mode": mode,
        "key": {"key": key_clean},
        "key_rank": rank,
        "col_order": order,
        "ncol": ncol,
        "nrow": nrow,
        "input_clean": clean,
        "grid": grid,
        "result": result,
        "note": "Ciphertext dibagi per kolom sesuai urutan kunci, lalu dibaca baris per baris.",
    }
