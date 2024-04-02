import fitz


doc= fitz.open("../PDFExtraction/pdfs/AnnualReport1.pdf")

print(f"total pages :{doc.page_count}")

for i in range(5,10): 
    current_page= doc.load_page(i)
    page_on_text=current_page.get_text()
    print(f"text on page {i}")
    print(page_on_text)


