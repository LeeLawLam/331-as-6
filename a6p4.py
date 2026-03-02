#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2026 <<Insert your name here>>
#
# Redistribution is forbidden in all circumstances. Use of this software
# without explicit authorization from the author is prohibited.
#
# This software was produced as a solution for an assignment in the course
# CMPUT 331 - Computational Cryptography at the University of
# Alberta, Canada. This solution is confidential and remains confidential 
# after it is submitted for grading.
#
# Copying any part of this solution without including this copyright notice
# is illegal.
#
# If any portion of this software is included in a solution submitted for
# grading at an educational institution, the submitter will be subject to
# the sanctions for plagiarism at that institution.
#
# If this software is found in any public website or public repository, the
# person finding it is kindly requested to immediately report, including 
# the URL or other repository locating information, to the following email
# address:
#
#          gkondrak <at> ualberta.ca
#
#---------------------------------------------------------------

"""
Problem 4
"""

from sys import flags


ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"   # This is the true English letter frequency

import a6p1
import a6p2
import a6p3


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
ALLOWED = set(ALPHABET)

def breakSub(cipherFile: str, textFile: str, n: int) -> None:
    """
    Inputs:
        cipherFile: 
            'text_finnegan_cipher.txt' for implementation
            'text_cipher.txt' for submission
            This string is a path to the file itself
        textFile: 'wells.txt'
        This string is a path to the text file 
    Outputs:
        'text_finnegan_plain.txt' for implementation
        'text_plain.txt' for submission
        
    """
    # ---- Read + clean ciphertext ----
    with open(cipherFile, "r", encoding="utf-8") as f:
        ciphertext_raw = f.read().upper()

    allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ ")
    ciphertext = "".join(ch if ch in allowed else " " for ch in ciphertext_raw)

    # ---- Read + clean training text, build n-gram frequencies ----
    with open(textFile, "r", encoding="utf-8") as f:
        training_raw = f.read().upper()

    training = "".join(ch if ch in allowed else " " for ch in training_raw)
    frequencies = a6p1.ngramsFreqs(training, n)

    # ---- Initial mapping by frequency analysis (try two starts) ----
    counts = {c: 0 for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    for ch in ciphertext:
        if ch in counts:
            counts[ch] += 1

    # Deterministic: sort by (-count, letter)
    cipher_order = sorted(counts.keys(), key=lambda c: (-counts[c], c))

    # English order #1: given ETAOIN
    english_order_1 = ETAOIN

    # English order #2: derived from training text unigram order
    uni_freqs = a6p1.ngramsFreqs(training, 1)
    letters_only = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    letters_only.sort(key=lambda ch: (-uni_freqs.get(ch, 0.0), ch))
    english_order_2 = "".join(letters_only)

    def build_map(eng_order: str) -> dict:
        m = {" ": " "}
        for i in range(26):
            m[cipher_order[i]] = eng_order[i]
        return m

    m1 = build_map(english_order_1)
    m2 = build_map(english_order_2)

    # pick better start using trigram score
    if a6p2.keyScore(m2, ciphertext, frequencies, n) > a6p2.keyScore(m1, ciphertext, frequencies, n):
        mapping = m2
    else:
        mapping = m1

    # ---- Hill-climb until no better successor ----
    while True:
        successor = a6p3.bestSuccessor(mapping, ciphertext, frequencies, n)
        if successor == mapping:
            break
        mapping = successor

    # ---- Decrypt and write output ----
    plaintext = "".join(mapping.get(ch, ch) for ch in ciphertext)

    outFile = "text_finnegan_plain.txt" if "finnegan" in cipherFile.lower() else "text_plain.txt"
    with open(outFile, "w", encoding="utf-8") as f:
        f.write(plaintext)




'''
Use this section to import your code from A6P1, A6P2, A6P3
-- Make sure to import the entire module, sometimes using import from your own files can cause issues in the grading script

'''
        
def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    
if __name__ == "__main__" and not flags.interactive:
    test()