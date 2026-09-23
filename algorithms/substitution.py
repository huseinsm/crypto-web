"""
substitution.py — Keyword Substitution Cipher (substitusi monoalfabetik berkunci).

Membangun alfabet cipher dari kata kunci:
  - Huruf unik kata kunci ditulis lebih dulu (berurut sesuai kemunculan).
  - Sisa alfabet ditambahkan setelahnya.
  - A -> cipher[0], B -> cipher[1], dst.

Contoh keyword "ZEBRA":
  cipher alphabet = Z E B R A C D F G H I J K L M N O P Q S T U V W X Y
  Pemetaan        = A->Z, B->E, C->B, D->R, E->A, F->C, ...
"""

from common import ALPHABET, only_letters


def build_cipher_alphabet(key: str) -> str:
    key_clean = only_letters(key)
    unique = []
    for ch in key_clean:
        if ch not in unique:
            unique.append(ch)
    for ch in ALPHABET:
        if ch not in unique:
            unique.append(ch)
    return "".join(unique)[:26]


def process(text: str, key: str, mode: str = "encrypt") -> dict:
    cipher_alpha = build_cipher_alphabet(key)
    clean = only_letters(text)

    if mode == "encrypt":
        mapping = {ALPHABET[i]: cipher_alpha[i] for i in range(26)}
    else:
        mapping = {cipher_alpha[i]: ALPHABET[i] for i in range(26)}

    out = []
    steps = []
    for i, ch in enumerate(clean):
        new_ch = mapping.get(ch, ch)
        out.append(new_ch)
        steps.append({
            "i": i,
            "char": ch,
            "plain_index": ALPHABET.index(ch) if mode == "encrypt" else cipher_alpha.index(ch),
            "cipher": new_ch,
        })

    return {
        "cipher": "substitution",
        "mode": mode,
        "key": {"key": only_letters(key) or "ZEBRA"},
        "plain_alphabet": ALPHABET,
        "cipher_alphabet": cipher_alpha,
        "input_clean": clean,
        "result": "".join(out),
        "steps": steps,
    }
