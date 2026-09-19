import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple


def parse_pdf_with_mineru(pdf_path: str, tier: str = "standard"):
    """Parse PDF using MinerU. Returns a mineru.ParseResult.

    engine is pinned to llama-cpp because "auto" selects vLLM on Linux+CUDA,
    which JIT-compiles Triton kernels and needs a C compiler on PATH.
    """
    from mineru import parse
    from mineru.config import VlmConfig

    return parse(pdf_path, tier=tier, vlm_config=VlmConfig(engine="llama-cpp"))


def parse_pdf_by_sections(pdf_path: str) -> List[Dict]:
    """
    Parse PDF by sections using MinerU's markdown rendering.
    MinerU emits '#'-style headers for detected titles, so we split on those.
    """
    result = parse_pdf_with_mineru(pdf_path)
    # Default markdown() inlines figures as base64 data URIs, which bloats
    # sections to hundreds of KB and is useless as embedding input.
    markdown = result.markdown(image_renderer=lambda block: "")

    sections = []
    current_title = None
    current_content = ""

    for line in markdown.split("\n"):
        if line.startswith("#"):
            if current_title is not None or current_content.strip():
                sections.append({
                    "title": current_title,
                    "content": current_content.strip(),
                })
            current_title = line.lstrip("#").strip()
            current_content = ""
        else:
            current_content += "\n" + line

    if current_title is not None or current_content.strip():
        sections.append({
            "title": current_title,
            "content": current_content.strip(),
        })

    return sections
