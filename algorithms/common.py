"""
common.py — fungsi bersama untuk semua algoritma cipher.

Dipakai oleh: caesar.py, vigenere.py, transposition.py, playfair.py, substitution.py
Tidak ada dependensi eksternal (cukup library standar Python).
"""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def only_letters(text: str) -> str:
    """Ambil hanya huruf A-Z, ubah ke huruf besar. Spasi/simbol dibuang."""
    return "".join(ch for ch in text.upper() if ch.isalpha() and ch.isascii())


def mod_inverse(a: int, m: int = 26):
    """Invers modulo. Dipakai substitusi affine bila perlu."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def chunk(text: str, n: int):
    """Potong teks menjadi potongan panjang n."""
    return [text[i:i + n] for i in range(0, len(text), n)]
