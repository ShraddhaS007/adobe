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
Instead of relying purely on font size heuristics, it emphasizes:

Semantic filtering (capitalization, bullet patterns, keywords)

Font weight (bold) and visual hierarchy

Text patterns like 1., 1.1, 2.3.1, etc.

Exclusion of non-headings (like table headers)

Key Steps:
Title Extraction: Pick the largest visible text on the first page

Heading Candidates: Analyze spans for boldness, font size, casing

Heading Classification: Assign H1/H2/H3 based on numeric patterns or style

Filtering: Remove repeated, irrelevant or structural elements like table rows

 Requirements
Python 3.9+

Dependencies installed via requirements.txt:

PyMuPDF

 Docker Instructions
 Build Docker Image

docker build --platform linux/amd64 -t pdfoutliner:challenge .
 Run the Container

docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdfoutliner:challenge
All .pdf files in /input will be processed

Corresponding .json files will be saved to /output

 Testing
Example:

/input/file01.pdf → /output/file01.json
Run time: ≤10s for 50-page documents
Works offline (no external calls)
Model size: No external model used (no >200MB dependencies)


 Tech Stack
 Python 3.9

 PyMuPDF (fitz)

 Docker (CPU, amd64)

 Constraints Met
 No external internet/API calls

 Compatible with amd64

 Runs within 10 seconds for 50-page PDFs

 Model size under 200MB (none used)

 Headings classified into H1/H2/H3

 Works offline

 Author
Team Name: [Binary Bits]

