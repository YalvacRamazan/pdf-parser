from unstructured.partition.pdf import partition_pdf

def pdf_to_markdown(pdf_path: str, output_md_path: str):

    elements = partition_pdf(
        filename=pdf_path,
        strategy="fast",
        infer_table_structure=True # Tablo Yapısını Korur
    )

    md_content = []
    for el in elements:
        category = el.category
        text = str(el).strip()

        if not text:
            continue

        if category == "Title":
            md_content.append(f"# {text}\n")
        elif category == "Subtitle":
            md_content.append(f"## {text}\n")
        elif category == "ListItem":
            md_content.append(f"- {text}\n")
        elif category == "Table":
            md_content.append(f"\n{el.metadata.text_as_html or text}\n")
        else: 
            md_content.append(f"{text}\n")
        
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))

if __name__ == "__main__":
    pdf_to_markdown("ornek.pdf", "cikti.md")
    print("Çıktınız hazır") 