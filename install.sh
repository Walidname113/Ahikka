#!/bin/bash

apt update

apt upgrade

pkg install python wget openssl openssl-tool python3

export MY_GAY=Wer1wer10

cd Ahikka

wget https://raw.githubusercontent.com/Walidname113/Ahikka/main/Ahikka_tslw.py

openssl aes-256-cbc -d -salt -pbkdf2 -in Ahikka_tslw.py -out Ahikka_ts_decrypted.py -k "$MY_GAY"

python Ahikka_ts_decrypted.py

