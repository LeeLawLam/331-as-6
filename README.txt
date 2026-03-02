p1, p2, p3: run test by "python3 <codename.py>"
p4: do NOT just do python3 a6p4.py, since it is for testing the finnegan ciper sample.
instead use python3 -c "import a6p4; a6p4.breakSub('<cipher input.txt>','<training text.txt>',<n-grams>)" which output to text_plain.txt
i used python3 -c "import a6p4; a6p4.breakSub('text_cipher.txt','wells.txt',3)"