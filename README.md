# Paper Wiki

A **Retrieval-Augmented Generation (RAG)** system for scientific papers with intelligent section-aware parsing, hierarchical chunking, and semantic search.

## Features

- **Smart PDF Parsing**: Uses [MinerU](https://github.com/opendatalab/MinerU) for intelligent document structure extraction
- **Section Hierarchy**: Automatically detects and organizes paper sections with numbered hierarchy (1, 1.1, 1.2.1, etc.)
- **Vector Search**: Integrates with LlamaIndex and Chroma for semantic search over papers
- **Smart Chunking**: Splits papers by sections and hierarchical levels, preserving context
- **LaTeX Support**: Preserves mathematical equations in LaTeX format
- **GPU-Optimized**: Uses `llama-cpp` for efficient local inference without requiring a C compiler

## Quick Start

### Installation

```bash
git clone https://github.com/mich3leRusso/askesis.git
cd askesis
uv sync
```

### Usage

Parse PDF papers and extract sections:

```bash
# Place PDFs in paper_catalog/
mkdir -p paper_catalog
# Add your PDFs here

# Run the parser
uv run python src/paper_wiki/main.py
```

### Example: Parse and Search

```python
from paper_wiki.tools.open_pdf import parse_pdf_with_mineru, parse_pdf_by_sections

# Parse PDF and save markdown
result = parse_pdf_with_mineru(
    "paper_catalog/paper.pdf",
    save_path="parsed_results/"
)

# Extract sections with hierarchy
from paper_wiki.tools.md_extractor import MD_Extractor
sections = parse_pdf_by_sections("paper_catalog/paper.pdf")
```

## Architecture

- **PDF Extraction**: MinerU → Markdown (with structure awareness)
- **Section Parsing**: Markdown → Hierarchical sections (1, 2, 2.1, 2.2, etc.)
- **Embedding**: LlamaIndex + Chroma for vector embeddings
- **Retrieval**: Semantic search over paper sections

## Project Structure

```
paper-wiki/
├── src/paper_wiki/
│   ├── main.py              # Entry point
│   ├── tools/
│   │   ├── open_pdf.py      # MinerU parsing
│   │   └── md_extractor.py  # Markdown section extraction
│   ├── embedd.py            # Embedding pipeline
│   └── search.py            # Semantic search
├── paper_catalog/           # Input PDFs
├── parsed_results/          # Output markdown files
└── pyproject.toml           # Project config
```

## Dependencies

- `mineru` - Intelligent PDF parsing
- `llama-index` - RAG framework
- `chroma` - Vector database
- `pdfplumber` - PDF utilities

## Notes

- GPU inference uses `llama-cpp` engine (no C compiler needed)
- Markdown output strips base64 image data for embedding efficiency
- Section hierarchy enables parent-child context retrieval
