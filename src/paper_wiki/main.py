import os
from paper_wiki.tools.open_pdf import parse_pdf_with_mineru
from paper_wiki.tools.md_extractor import MD_Extractor
from paper_wiki.embedd import init_chroma, embed_sections
from .search import search

def main():
    pdf_folder = '/home/michele/paper-wiki/paper_catalog'
    print(f"Scanning folder: {pdf_folder} for PDF files...")
    save_path = '/home/michele/paper-wiki/parsed_results/'
    if not os.path.exists(pdf_folder):
        print(f"Error: Folder {pdf_folder} does not exist")
        return

    collection = init_chroma("papers")

    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Processing {pdf_path}...")
            try:
                result = parse_pdf_with_mineru(pdf_path, save_path=save_path)
                markdown = result.markdown(image_renderer=lambda block: "")
                md_extractor = MD_Extractor(markdown, filename)
                sections, title = md_extractor.get_sections()
                count = embed_sections(collection, sections, filename , title)
                print(f"✓ {filename}: '{title}' - embedded {count} sections")
            except Exception as e:
                print(f"✗ Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main()