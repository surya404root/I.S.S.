#!/data/data/com.termux/files/usr/bin/bash

pkg update -y && pkg upgrade -y
pkg install python -y

pip install -r requirements.txt

mkdir -p reports

chmod +x cli/cyber_speed.py

echo "Run using: python cli/cyber_speed.py"
