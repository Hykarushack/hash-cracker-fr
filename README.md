# 🔐 hash-cracker-fr

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/bug404found/hash-cracker-fr?style=social)](https://github.com/bug404found/hash-cracker-fr)

> A hash cracking toolkit built for CTF players, pentesters, and security researchers — with **French wordlists and custom rules** baked in.

## 📖 Overview

Password hash cracking tools often ship with English-centric wordlists, leaving French-language targets underserved during CTF challenges and authorized penetration tests. **hash-cracker-fr** solves this by combining a fast, multi-algorithm cracking engine with curated French dictionaries and mutation rules. Whether you're dealing with MD5, SHA-1, SHA-256, or bcrypt, this toolkit helps you recover plaintexts efficiently — with a special focus on French passwords, accents, and common patterns.

## 🚀 Installation

### From source (recommended)

```bash
git clone https://github.com/bug404found/hash-cracker-fr.git
cd hash-cracker-fr
pip install -r requirements.txt
```

### Via pip

```bash
pip install hash-cracker-fr
```

## 💻 Usage

### Command line

```bash
# Crack a single MD5 hash using the French wordlist
python -m hash_cracker_fr crack \
  --hash 5f4dcc3b5aa765d61d8327deb882cf99 \
  --algo md5 \
  --wordlist wordlists/fr_common.txt \
  --rules rules/fr_mutations.rule
```

### Python API

```python
from hash_cracker_fr import Cracker

cracker = Cracker(
    algorithm="sha256",
    wordlist="wordlists/fr_common.txt",
    rules="rules/fr_mutations.rule",
)

result = cracker.crack("2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b")

if result.found:
    print(f"[+] Password found: {result.plaintext}")
else:
    print("[-] Not found in wordlist")
```

### Batch mode

```bash
# Crack a file of hashes (one per line)
python -m hash_cracker_fr batch \
  --input hashes.txt \
  --algo sha1 \
  --wordlist wordlists/fr_common.txt \
  --output cracked.txt
```

## ✨ Features

- 🔑 **Multi-algorithm support** — MD5, SHA-1, SHA-256, SHA-512, bcrypt, and more
- 🇫🇷 **French wordlists included** — common passwords, names, and leaked patterns curated for FR targets
- 🧬 **Rule-based mutations** — apply case toggles, leetspeak, suffixes, and French accent variants
- ⚡ **Multi-threaded engine** — parallel cracking with configurable worker count
- 🧩 **Modular rules engine** — write your own `.rule` files for custom transformations
- 📊 **Progress & logging** — real-time stats, ETA, and structured logs
- 🧪 **CTF-friendly CLI** — one-liners for fast hash submission workflows
- 🐍 **Pure Python** — no native dependencies, easy to audit and extend

## 🤝 Contributing

Contributions are welcome! Whether you want to add a new wordlist, improve the rules engine, or fix a bug:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and follow the existing code style. For major changes, open an issue first to discuss what you'd like to change.

> ⚠️ **Ethical use only.** This tool is intended for CTF competitions, authorized penetration testing, and security research. Never use it against systems you don't own or have explicit permission to test.

## About

This project is maintained by **[bug404found.com](https://bug404found.com/?utm_source=github&utm_medium=readme&utm_campaign=opensource&utm_content=hash-cracker-fr)** — a cybersecurity recruitment platform that evaluates candidates through hands-on, practical labs rather than traditional interviews. If you're a security enthusiast looking to prove your skills on real challenges, or a company searching for vetted cyber talent, check us out.

👉 [bug404found.com](https://bug404found.com/?utm_source=github&utm_medium=readme&utm_campaign=opensource&utm_content=hash-cracker-fr)