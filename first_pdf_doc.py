import fitz 
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

class PDFOkuyucu:
    def __init__(self, pdf_yolu: str):
        self.doc = fitz.open(pdf_yolu)

    def yapiyi_ayikla(self) -> list[dict]:
        elements = []
        for page in self.doc:
            blocks = page.get_text("dict")["blocks"]
            for b in blocks:
                if "lines" not in b:
                    continue
                for line in b["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        size = round(span["size"], 1)
                        flags = span["flags"]

                        if not text:
                            continue
                        
                        if size >= 16:
                            role = "H1"
                        elif 12 <= size < 16:
                            role = "H2"
                        else:
                            role = "Item"
                        
                        elements.append({"text": text, "role": role, "size": size})
            return elements

class PDFOlusturucu:
    def __init__(self, cikti_yolu: str):
        self.cikti_yolu = cikti_yolu
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle('H1_Style', parent=self.styles['Heading1'], fontSize=16, leading=20, spaceAfter=8))
        self.styles.add(ParagraphStyle('H2_Style', parent=self.styles['Heading2'], fontSize=13, leading=16, spaceAfter=6, leftIndent=10))
        self.styles.add(ParagraphStyle('Item_Style', parent=self.styles['Normal'], fontSize=10, leading=14, spaceAfter=4, leftIndent=20))

    def pdf_olustur(self, elements: list[dict]):
        doc = SimpleDocTemplate(self.cikti_yolu, pagesize=letter)
        story = []

        for el in elements:
            role = el["role"]
            text = el["text"]

            if role == "H1":
                story.append(Paragraph(f"<b>{text}</b>", self.styles['H1_Style']))
                story.append(Spacer(1, 4))
            elif role == "H2":
                story.append(Paragraph(f"<b>{text}</b>", self.styles['H2_Style']))
                story.append(Spacer(1, 3))
            else:
                story.append(Paragraph(text, self.styles['Item_Style']))
                story.append(Spacer(1, 2))
        doc.build(story)

# Ornek Kullanim
try:
    if __name__ == "__main__":
        pdf_yolu = "ornek.pdf"
        cikti_yolu = "yeni_dosya.pdf"

        okuyucu = PDFOkuyucu(pdf_yolu)
        yapilar = okuyucu.yapiyi_ayikla()

        olusturucu = PDFOlusturucu(cikti_yolu)
        olusturucu.pdf_olustur(yapilar)
        print(f"Cikti olustu")
except Exception as e:
    print(f"Hata olustu: {e}")