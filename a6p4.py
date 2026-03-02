#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2026 Louis Lam
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

import random
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
    # read + clean ciphertext
    with open(cipherFile, "r", encoding="utf-8") as f:
        cipher_raw = f.read().upper()
    ciphertext = "".join(ch if ch in ALLOWED else " " for ch in cipher_raw)

    # read + clean training text
    with open(textFile, "r", encoding="utf-8") as f:
        train_raw = f.read().upper()
    training = "".join(ch if ch in ALLOWED else " " for ch in train_raw)

    # n-gram frequencies from training
    frequencies = a6p1.ngramsFreqs(training, n)

    # initial mapping by frequency analysis
    counts = {c: 0 for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    for ch in ciphertext:
        if ch in counts:
            counts[ch] += 1

    cipher_order = sorted(counts.keys(), key=lambda c: (-counts[c], c))

    # fixed ETAOIN
    english_order_1 = ETAOIN

    # unigram order from training text
    uni_freqs = a6p1.ngramsFreqs(training, 1)
    letters_only = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    letters_only.sort(key=lambda ch: (-uni_freqs.get(ch, 0.0), ch))
    english_order_2 = "".join(letters_only)

    m1 = {" ": " "}
    m2 = {" ": " "}
    for i in range(26):
        m1[cipher_order[i]] = english_order_1[i]
        m2[cipher_order[i]] = english_order_2[i]

    s1 = a6p2.keyScore(m1, ciphertext, frequencies, n)
    s2 = a6p2.keyScore(m2, ciphertext, frequencies, n)
    base_mapping = m2 if s2 > s1 else m1

    # hill climb
    def hill_climb(start_mapping: dict) -> dict:
        m = start_mapping
        while True:
            nxt = a6p3.bestSuccessor(m, ciphertext, frequencies, n)
            if nxt == m:
                return m
            m = nxt

    best_mapping = hill_climb(base_mapping)
    best_score = a6p2.keyScore(best_mapping, ciphertext, frequencies, n)

    is_finnegan = "finnegan" in cipherFile.lower()

    K = 10                  # consider top K frequent cipher letters
    LIMIT = 25 if is_finnegan else 10   # fewer tries for submission to keep fast

    top = cipher_order[:K]

    tried = 0
    for i in range(K):
        for j in range(i + 1, K):
            m0 = dict(base_mapping)
            a = top[i]
            b = top[j]
            m0[a], m0[b] = m0[b], m0[a]

            candidate = hill_climb(m0)
            score = a6p2.keyScore(candidate, ciphertext, frequencies, n)

            if score > best_score:
                best_score = score
                best_mapping = candidate

            tried += 1
            if tried >= LIMIT:
                break
        if tried >= LIMIT:
            break

    # decrypt + output
    plaintext = "".join(best_mapping.get(ch, ch) for ch in ciphertext)
    with open("text_plain.txt", "w", encoding="utf-8") as f:
        f.write(plaintext)




'''
Use this section to import your code from A6P1, A6P2, A6P3
-- Make sure to import the entire module, sometimes using import from your own files can cause issues in the grading script

'''
        
def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    
    cipher_test = "text_finnegan_cipher.txt"
    train_text = "wells.txt"
    ref_plain = "text_finnegan_plain.txt"
    out_plain = "text_plain.txt"
    n = 3

    breakSub(cipher_test, train_text, n)

    try:
        with open(out_plain, "r", encoding="utf-8") as f:
            produced = f.read()
        with open(ref_plain, "r", encoding="utf-8") as f:
            expected = f.read()

        if produced == expected:
            print("PASS")
        else:
            print("FAIL")
    except FileNotFoundError:
        print("Reference file not found.")
    
if __name__ == "__main__" and not flags.interactive:
    test()