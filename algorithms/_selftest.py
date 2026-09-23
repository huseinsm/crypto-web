"""Uji cepat semua algoritma (round-trip encrypt -> decrypt)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import caesar, vigenere, transposition, playfair, substitution

MSGS = ["HALO DUNIA", "KRIPTOGRAFI KLASIK", "SERANG SUBUH", "AA BB CC"]

def rt(mod, text, key):
    e = mod.process(text, key, "encrypt")["result"]
    d = mod.process(e, key, "decrypt")["result"]
    return e, d

print("== CAESAR ==")
for m in MSGS:
    e, d = rt(caesar, m, 3)
    print(f"  {m:22} -> {e:26} -> {d}")

print("== VIGENERE ==")
for m in MSGS:
    e, d = rt(vigenere, m, "KUNCI")
    print(f"  {m:22} -> {e:26} -> {d}")

print("== TRANSPOSITION ==")
for m in MSGS:
    e, d = rt(transposition, m, "KRIPTO")
    print(f"  {m:22} -> {e:26} -> {d}")

print("== PLAYFAIR ==")
for m in MSGS:
    e, d = rt(playfair, m, "MONARCHY")
    print(f"  {m:22} -> {e:26} -> {d}")

print("== SUBSTITUTION ==")
for m in MSGS:
    e, d = rt(substitution, m, "ZEBRA")
    print(f"  {m:22} -> {e:26} -> {d}")

print()
print("matrix playfair:", playfair.build_matrix("MONARCHY"))
print("brute caesar (HALO):", [b['hasil'] for b in caesar.brute_force('KDOO')][:5], "...")
