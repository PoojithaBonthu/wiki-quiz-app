import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException
import re

WIKI_BASE = "https://en.wikipedia.org/wiki/"

# -------------------------------------------------
# NORMALIZE INPUT (URL OR NAME)
# -------------------------------------------------

def normalize_wikipedia_url(input_text: str) -> str:
    """
    Accepts:
    - Full Wikipedia URL
    - Article name (Isaac_Newton)
    - Plain text (Isaac Newton)
    Converts everything to a valid Wikipedia URL.
    """
    if not input_text:
        raise HTTPException(
            status_code=400,
            detail="Empty input"
        )

    input_text = input_text.strip()

    # If already a full URL
    if input_text.startswith("http"):
        return input_text

    # Convert name/text → Wikipedia format
    article = input_text.replace(" ", "_")
    return WIKI_BASE + article


# -------------------------------------------------
# CLEAN TEXT
# -------------------------------------------------

def clean_text(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)   # remove [1], [2]
    text = re.sub(r"\s+", " ", text)      # normalize spaces
    return text.strip()


# -------------------------------------------------
# SCRAPER
# -------------------------------------------------

def scrape_wikipedia(input_text: str):
    url = normalize_wikipedia_url(input_text)

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; WikiQuizBot/1.0)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException:
        raise HTTPException(
            status_code=500,
            detail="Failed to connect to Wikipedia"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Wikipedia page not found"
        )

    soup = BeautifulSoup(response.text, "html.parser")

    # ----------------------------
    # TITLE
    # ----------------------------
    title_tag = soup.find("h1")
    title = title_tag.text if title_tag else "No title"

    # ----------------------------
    # SUMMARY (FIRST 3 PARAGRAPHS)
    # ----------------------------
    paragraphs = soup.select("p")
    summary_parts = []

    for p in paragraphs:
        if p.text.strip():
            summary_parts.append(clean_text(p.text))
        if len(summary_parts) >= 3:
            break

    summary = " ".join(summary_parts)

    # ----------------------------
    # SECTIONS
    # ----------------------------
    sections = [
        h.text for h in soup.select("h2 span.mw-headline")
    ]

    # ----------------------------
    # CONTENT FOR LLM (FIRST 5 PARAGRAPHS)
    # ----------------------------
    content_parts = []
    for p in paragraphs[:5]:
        if p.text.strip():
            content_parts.append(clean_text(p.text))

    content = " ".join(content_parts)

    return {
        "url": url,
        "title": title,
        "summary": summary,
        "sections": sections,
        "content": content,
        "raw_html": response.text
    }
