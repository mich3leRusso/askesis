import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple

def parse_pdf_with_mineru(pdf_path: str, tier: str = "standard", save_path: Optional[str] = None):
    """Parse PDF using MinerU. Returns a mineru.ParseResult.

    engine is pinned to llama-cpp because "auto" selects vLLM on Linux+CUDA,
    which JIT-compiles Triton kernels and needs a C compiler on PATH.

    Args:
        pdf_path: Path to PDF file
        tier: Parsing tier (flash, basic, standard, advanced)
        save_path: If provided, saves markdown to this file path
    """
    from mineru import parse
    from mineru.config import VlmConfig

    result = parse(pdf_path, tier=tier, vlm_config=VlmConfig(engine="llama-cpp"))

    if save_path is not None:
        markdown = result.markdown(image_renderer=lambda block: "")
        save_path_obj = Path(save_path)

        # If save_path is a directory, create filename from PDF
        if save_path.endswith('/') or save_path.endswith(os.sep):
            save_path_obj = save_path_obj / f"{Path(pdf_path).stem}.md"
        elif not save_path.endswith('.md'):
            # If it looks like a directory without trailing slash, treat as such
            save_path_obj = save_path_obj / f"{Path(pdf_path).stem}.md"

        save_path_obj.parent.mkdir(parents=True, exist_ok=True)
        save_path_obj.write_text(markdown)
        print(f"Saved markdown to {save_path_obj}")

    return result


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
