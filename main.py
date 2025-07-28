import fitz  # PyMuPDF
import os
import json
import re
from statistics import mode

# Denylist of common form/table headers (customize this)
DENYLIST = {
    "s.no", "name", "date", "age", "relationship", "remarks",
    "signature", "designation", "block", "amount", "version",
    "reference", "identifier", "rs.", "days", "pay"
}

# Keywords that should always be considered as headings if isolated
ALWAYS_HEADINGS = {
    "summary", "timeline", "background", "milestones", "evaluation", "appendix"
}

def get_title(page):
    blocks = page.get_text("dict")["blocks"]
    lines = []

    max_size = 0
    for block in blocks:
        for line in block.get("lines", []):
            for span in line["spans"]:
                if span["size"] > max_size and len(span["text"].strip()) > 1:
                    max_size = span["size"]

    # Gather all text with that max size
    for block in blocks:
        for line in block.get("lines", []):
            line_text = ""
            for span in line["spans"]:
                if abs(span["size"] - max_size) < 0.5:
                    line_text += span["text"].strip() + " "
            if line_text.strip():
                lines.append(line_text.strip())

    return " ".join(lines).strip()

def is_toc_page(page):
    text = page.get_text()
    dot_count = text.count(" .")
    return dot_count > 10

def get_outline(doc, title):
    outline = []
    candidates = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        if is_toc_page(page):
            continue

        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                text = ""
                sizes = []
                fonts = []

                for span in line["spans"]:
                    t = span["text"].strip()
                    if not t:
                        continue
                    text += t + " "
                    sizes.append(span["size"])
                    fonts.append(span["font"])

                text = text.strip()
                if not text:
                    continue

                font_size = max(sizes)
                is_bold = any("Bold" in f for f in fonts)
                is_upper = text.isupper()

                candidates.append({
                    "text": text,
                    "size": font_size,
                    "bold": is_bold,
                    "uppercase": is_upper,
                    "page": page_num
                })

    # Estimate normal font size
    sizes = [c["size"] for c in candidates]
    try:
        normal_size = mode(sizes)
    except:
        normal_size = sorted(sizes)[len(sizes)//2]

    for c in candidates:
        text = c["text"].strip()
        size = c["size"]
        is_bold = c["bold"]
        is_upper = c["uppercase"]
        page = c["page"]

        # Cleaned text
        clean = text.lower().strip(" :*–-")
        if clean in DENYLIST:
            continue

        if text == title:
            continue

        if not re.search(r"[A-Za-z]", text):
            continue
        if text[0].islower():
            continue
        if len(text.split()) > 20:
            continue
        if not is_bold and size <= normal_size:
            if clean not in ALWAYS_HEADINGS:
                continue
        if is_upper and not is_bold and size <= normal_size + 1:
            continue
        if re.search(r"\.\s*[\*\-]*$", text):
            continue

        # Heading level logic
        level = None
        if re.match(r"^\d+\.\d+\.\d+\.\d+", text):
            level = "H4"
        elif re.match(r"^\d+\.\d+\.\d+", text):
            level = "H3"
        elif re.match(r"^\d+\.\d+", text):
            level = "H2"
        elif re.match(r"^\d+\.", text):
            level = "H1"
        elif is_bold and size >= normal_size + 3:
            level = "H1"
        elif is_bold and size >= normal_size + 2:
            level = "H2"
        elif is_bold and size >= normal_size:
            level = "H3"
        elif clean in ALWAYS_HEADINGS:
            level = "H2"

        if level:
            outline.append({
                "level": level,
                "text": text,
                "page": page
            })

    return outline

def process_pdf(filepath):
    doc = fitz.open(filepath)
    title = get_title(doc[0])
    outline = get_outline(doc, title)
    return {
        "title": title,
        "outline": outline
    }

if __name__ == "__main__":
    input_dir = "./input"
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(input_dir, filename)
            result = process_pdf(filepath)
            output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

    print("✅ Done: PDFs processed.")



# Build your image
# docker build --platform linux/amd64 -t pdfoutliner:challenge .

# Run it
# docker run --rm -v "C:\Users\lenovo\Desktop\adobe\input:/app/input" -v "C:\Users\lenovo\Desktop\adobe\output:/app/output" --network none pdfoutliner:challenge
