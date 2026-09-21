import os
from paper_wiki.tools.open_pdf import parse_pdf_with_mineru
from paper_wiki.tools.md_extractor import MD_Extractor

def main():
    pdf_folder = '/home/michele/paper-wiki/paper_catalog'
    print(f"Scanning folder: {pdf_folder} for PDF files...")
    save_path = '/home/michele/paper-wiki/parsed_results/'
    if not os.path.exists(pdf_folder):
        print(f"Error: Folder {pdf_folder} does not exist")
        return

    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Processing {pdf_path}...")
            try:
                result = parse_pdf_with_mineru(pdf_path, save_path=save_path)
                print(f"✓ Successfully processed {filename}")
                # start of division of the file 
                markdown = result.markdown(image_renderer=lambda block: "")
                md_extractor = MD_Extractor(markdown, filename)
                sections, title = md_extractor.get_sections()
                print(f"Sections extracted from {filename}:")
                print(f"Title: {title}")
                for section_number, section in sections.items():
                    print(f"Section {section_number}: {section['title']}")
                    input("Press Enter to see the content of this section...")      
                    print(f"Content: {section['content'][:100]}...")  # Print first 100 chars
                    input()
            except Exception as e:
                print(f"✗ Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main()