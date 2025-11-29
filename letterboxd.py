#!/usr/bin/env python3
import sys
import re
import unicodedata
import requests


def parse_title_and_year(raw: str):
    raw = raw.strip()
    m = re.match(r"^(.*?)(?:\s*\((\d{4})\)|\s+(\d{4}))\s*$", raw)
    if m:
        title = m.group(1).strip()
        year = m.group(2) or m.group(3)
        return title, year
    return raw, None


def slugify_title(title: str) -> str:
    s = title.lower().strip()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip()
    s = re.sub(r"-+", "-", s)
    return s


def make_letterboxd_url(raw_title: str) -> str:
    title, year = parse_title_and_year(raw_title)
    slug = slugify_title(title)
    if year is not None:
        slug = f"{slug}-{year}"
    return f"https://letterboxd.com/film/{slug}/"


def letterboxd_exists(url: str) -> bool:
    try:
        r = requests.get(
            url,
            allow_redirects=True,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        return r.status_code == 200
    except Exception:
        return False


def main():
    raw_title = " ".join(sys.argv[1:]).strip()
    if not raw_title:
        return

    url = make_letterboxd_url(raw_title)

    if letterboxd_exists(url):
        print(url)
    else:
        print("Movie not found.")


if __name__ == "__main__":
    main()
