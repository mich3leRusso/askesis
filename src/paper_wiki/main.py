import os
from paper_wiki.tools.open_pdf import parse_pdf_with_mineru

def main():
    pdf_folder = '/home/michele/paper-wiki/pdf_store'
    print(f"Scanning folder: {pdf_folder} for PDF files...")

    if not os.path.exists(pdf_folder):
        print(f"Error: Folder {pdf_folder} does not exist")
        return

    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Processing {pdf_path}...")
            try:
                result = parse_pdf_with_mineru(pdf_path)
                print(result)
                print(f"✓ Successfully processed {filename}")
            except Exception as e:
                print(f"✗ Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main()