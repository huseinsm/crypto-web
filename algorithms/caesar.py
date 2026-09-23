"""
caesar.py — Caesar Cipher (substitusi monoalfabetik, geseran tetap).

Enkripsi : C = (P + k) mod 26
Dekripsi : P = (C - k) mod 26
Visualisasi: tabel per-huruf (asli -> indeks -> indeks bergeser -> hasil).
"""

from common import ALPHABET, only_letters


def process(text: str, shift: int, mode: str = "encrypt") -> dict:
    k = int(shift) % 26
    if mode == "decrypt":
        k = (-k) % 26

    clean = only_letters(text)
    out = []
    steps = []

    for i, ch in enumerate(clean):
        idx = ALPHABET.index(ch)
        new_idx = (idx + k) % 26
        new_ch = ALPHABET[new_idx]
        out.append(new_ch)
        steps.append({
            "i": i,
            "char": ch,
            "index": idx,
            "new_index": new_idx,
            "cipher": new_ch,
        })

    return {
        "cipher": "caesar",
        "mode": mode,
        "key": {"shift": int(shift) % 26},
        "alphabet": ALPHABET,
        "input_clean": clean,
        "result": "".join(out),
        "steps": steps,
    }


def brute_force(text: str) -> list:
    """Coba semua 25 geseran (untuk pembelajaran)."""
    return [
        {"shift": s, "hasil": process(text, s, "decrypt")["result"]}
        for s in range(1, 26)
    ]
