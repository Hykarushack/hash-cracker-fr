import argparse
import hashlib
import hmac
import os
import sys
from pathlib import Path

# Common French wordlist paths and rule-based mutations
DEFAULT_WORDLISTS = [
    "/usr/share/wordlists/rockyou.txt",
    "/usr/share/wordlists/french.txt",
    "./wordlists/french.txt",
    "./french.txt",
]

FRENCH_SUFFIXES = ["", "1", "12", "123", "1234", "!", "!!", "2023", "2024", "2025", "01", "69"]
FRENCH_PREFIXES = ["", "le", "la", "les", "mon", "ma", "mes"]


def detect_hash_type(hash_str):
    """Guess hash type from length and charset."""
    h = hash_str.strip().lower()
    length = len(h)
    if length == 32:
        return "md5"
    if length == 40:
        return "sha1"
    if length == 56:
        return "sha224"
    if length == 64:
        return "sha256"
    if length == 96:
        return "sha384"
    if length == 128:
        return "sha512"
    return None


def hash_string(value, algo):
    """Hash a string using the given algorithm."""
    try:
        return hashlib.new(algo, value.encode("utf-8", errors="ignore")).hexdigest()
    except (ValueError, TypeError):
        return None


def load_wordlist(path):
    """Load a wordlist, stripping whitespace and skipping empties."""
    words = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                w = line.strip()
                if w:
                    words.append(w)
    except OSError as e:
        print(f"[!] Cannot read wordlist {path}: {e}", file=sys.stderr)
    return words


def apply_rules(word):
    """Generate French-flavored mutations of a word."""
    variants = set()
    variants.add(word)
    variants.add(word.lower())
    variants.add(word.capitalize())
    variants.add(word.upper())
    for suf in FRENCH_SUFFIXES:
        variants.add(word + suf)
        variants.add(word.capitalize() + suf)
    for pre in FRENCH_PREFIXES:
        if pre:
            variants.add(pre + word)
            variants.add(pre.capitalize() + word)
    # Leet-ish substitutions
    leet = word.replace("a", "@").replace("e", "3").replace("i", "1").replace("o", "0")
    if leet != word:
        variants.add(leet)
        variants.add(leet.capitalize())
    return variants


def find_wordlists(user_paths):
    """Resolve wordlists from user args or defaults."""
    if user_paths:
        return [p for p in user_paths if Path(p).is_file()]
    return [p for p in DEFAULT_WORDLISTS if Path(p).is_file()]


def crack(target_hash, algo, wordlists, use_rules, verbose):
    """Attempt to crack a single hash against wordlists."""
    target = target_hash.strip().lower()
    for wl in wordlists:
        if verbose:
            print(f"[*] Trying wordlist: {wl}")
        words = load_wordlist(wl)
        for word in words:
            candidates = apply_rules(word) if use_rules else {word}
            for cand in candidates:
                if hash_string(cand, algo) == target:
                    return cand
    return None


def main():
    parser = argparse.ArgumentParser(
        prog="hash-cracker-fr",
        description="Hash cracking toolkit with French wordlists and rules",
    )
    parser.add_argument("-H", "--hash", required=True, help="Hash string to crack")
    parser.add_argument(
        "-t", "--type",
        help="Hash type (md5, sha1, sha256, sha512...). Auto-detected if omitted.",
    )
    parser.add_argument(
        "-w", "--wordlist", action="append",
        help="Wordlist path (can be repeated). Uses defaults if omitted.",
    )
    parser.add_argument(
        "-r", "--rules", action="store_true",
        help="Apply French mutation rules (suffixes, prefixes, leet).",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output.")
    args = parser.parse_args()

    target = args.hash.strip()
    if not target:
        print("[!] Empty hash provided.", file=sys.stderr)
        return 2

    algo = args.type.lower() if args.type else detect_hash_type(target)
    if not algo:
        print("[!] Could not detect hash type. Use -t to specify.", file=sys.stderr)
        return 2

    try:
        hashlib.new(algo)
    except ValueError:
        print(f"[!] Unsupported hash algorithm: {algo}", file=sys.stderr)
        return 2

    wordlists = find_wordlists(args.wordlist)
    if not wordlists:
        print("[!] No usable wordlists found. Provide one with -w.", file=sys.stderr)
        return 2

    if args.verbose:
        print(f"[*] Target: {target}")
        print(f"[*] Algorithm: {algo}")
        print(f"[*] Wordlists: {len(wordlists)}")
        print(f"[*] Rules: {args.rules}")

    result = crack(target, algo, wordlists, args.rules, args.verbose)

    if result is not None:
        print(f"[+] Cracked: {result}")
        return 0
    else:
        print("[-] Not found in provided wordlists.")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted.", file=sys.stderr)
        sys.exit(130)