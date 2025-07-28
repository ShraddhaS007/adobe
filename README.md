#  PDF Outline Extractor — Round 1A (Adobe India Hackathon)

> **Challenge Theme:** Connecting the Dots Through Docs  
> **Task:** Extract structured document outlines from PDFs  
> **By:** [Your Name / Team Name]

---

##  Problem Statement

Given a PDF document (max 50 pages), extract:
- **Title**
- **Headings** (classified into levels: H1, H2, H3)
- **Page numbers** for each heading

Output should be a valid JSON in the following format:
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
Approach
This solution uses PyMuPDF (fitz) to parse PDF content.

Rather than relying solely on font size heuristics, the approach includes:

Semantic filtering (capitalization, bullet patterns, keyword exclusions)

Font weight (bold detection) and visual hierarchy

Heading number patterns (e.g., 1., 1.1, 2.3.1, etc.)

Exclusion of non-structural text (tables, headers, form labels)

Key Steps
Title Extraction: Selects the largest prominent text on the first page.

Heading Candidates: Identifies heading-like spans using style + structure.

Heading Classification: Uses rules for H1/H2/H3 detection.

Filtering: Excludes repeated lines, small text, lowercased text, etc.

Requirements
Python 3.9+

PyMuPDF

Install via:

bash
Copy
Edit
pip install -r requirements.txt
Docker Instructions
Build the Docker Image
bash
Copy
Edit
docker build --platform linux/amd64 -t pdfoutliner:challenge .
Run the Container
bash
Copy
Edit
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdfoutliner:challenge
All .pdf files in /input will be processed.

Corresponding .json outputs will be saved to /output.

Testing
Example:

bash
Copy
Edit
/input/file01.pdf → /output/file01.json
Performance:

≤ 10 seconds for 50-page documents

Runs entirely offline

No model > 200MB used

Tech Stack
Python 3.9

PyMuPDF (fitz)

Docker (CPU-only, amd64)

Constraints Met
 No external internet/API calls

 Compatible with amd64

 ≤ 10 seconds runtime for 50-page PDFs

 Model size ≤ 200MB (none used)

 H1/H2/H3 heading classification

 Works fully offline

Author
Team Name: Binary Bits
