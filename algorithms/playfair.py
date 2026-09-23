"""
playfair.py — Playfair Cipher (substitusi digraf / pasangan huruf).

Matriks 5x5 dibangun dari kata kunci (huruf J digabung ke I, alfabet 25 huruf).
Aturan enkripsi per pasangan:
  1. Baris sama  -> geser 1 kolom ke kanan.
  2. Kolom sama  -> geser 1 baris ke bawah.
  3. Beda keduanya -> tukar kolom (bentuk persegi).

Penataan pesan:
  - Huruf sama berpasangan (mis. LL) -> sisipkan X.
  - Jumlah huruf ganjil -> tambah X di akhir.

Visualisasi: matriks 5x5 + info posisi + aturan yang dipakai tiap pasangan.
"""

from common import only_letters

SIZE = 5


def build_matrix(key: str) -> list:
    seen = []
    for ch in only_letters(key).replace("J", "I") + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in seen:
            seen.append(ch)
    seen = seen[:25]
    return [seen[r * SIZE:(r + 1) * SIZE] for r in range(SIZE)]


def _find(matrix: list, ch: str):
    for r in range(SIZE):
        for c in range(SIZE):
            if matrix[r][c] == ch:
                return r, c
    raise ValueError(f"Huruf {ch} tidak ada di matriks.")


def _prepare(text: str) -> str:
    s = only_letters(text).replace("J", "I")
    out = []
    i = 0
    while i < len(s):
        a = s[i]
        if i + 1 < len(s):
            b = s[i + 1]
            if a == b:
                out.append(a + "X")
                i += 1
            else:
                out.append(a + b)
                i += 2
        else:
            out.append(a + "X")
            i += 1
    return "".join(out)


def process(text: str, key: str, mode: str = "encrypt") -> dict:
    matrix = build_matrix(key)
    prepared = _prepare(text)

    pairs = [prepared[i:i + 2] for i in range(0, len(prepared), 2)]
    shift = 1 if mode == "encrypt" else -1

    out = []
    steps = []
    for a, b in pairs:
        ra, ca = _find(matrix, a)
        rb, cb = _find(matrix, b)
        if ra == rb:  # baris sama
            na, nb = (ca + shift) % SIZE, (cb + shift) % SIZE
            rule = "baris sama \u2192 geser kolom"
            ea, eb = matrix[ra][na], matrix[rb][nb]
        elif ca == cb:  # kolom sama
            na, nb = (ra + shift) % SIZE, (rb + shift) % SIZE
            rule = "kolom sama \u2192 geser baris"
            ea, eb = matrix[na][ca], matrix[nb][cb]
        else:  # persegi
            rule = "beda baris & kolom \u2192 tukar kolom (persegi)"
            ea, eb = matrix[ra][cb], matrix[rb][ca]
        out.append(ea + eb)
        steps.append({
            "pair": a + b,
            "pos": [{"ch": a, "r": ra, "c": ca}, {"ch": b, "r": rb, "c": cb}],
            "rule": rule,
            "cipher": ea + eb,
        })

    return {
        "cipher": "playfair",
        "mode": mode,
        "key": {"key": only_letters(key) or "MONARCHY"},
        "matrix": matrix,
        "input_clean": only_letters(text),
        "prepared": prepared,
        "pairs": ["".join(p) for p in pairs],
        "result": "".join(out),
        "steps": steps,
    }
