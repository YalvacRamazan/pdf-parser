import pdfplumber
import requests
import json

# Docker'da çalışan Ollama API adresi
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b"

SYSTEM_PROMPT = """You are an expert PDF-to-Markdown converter.
Your goal is to reformat raw text extracted from PDFs into clean, structured Markdown for AI Agents.

RULES:
1. Preserve all semantic content and details without dropping info.
2. Fix headings (#, ##, ###) and restore list structures.
3. Keep or re-format tables into Markdown syntax (| col1 | col2 |).
4. Output ONLY valid Markdown. Do not add intro/outro chit-chat.
"""

def extract_text_from_pdf(pdf_path):
    """pdfplumber kullanarak PDF'ten ham metni çıkarır."""
    raw_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for index, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                raw_pages.append(f"--- SAYFA {index + 1} ---\n{text}")
    return "\n\n".join(raw_pages)

def format_with_ollama(raw_text):
    """Ollama API'sine istek atarak metni Markdown'a dönüştürür."""
    prompt = f"Convert the following raw PDF text into clean Markdown:\n\n{raw_text}"
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "stream": False,  # Yanıtı tek seferde almak için
        "options": {
            "temperature": 0.2, # AI'ın hayal gücünü düşürüp sadık kalmasını sağlar
            "num_ctx": 4096     # Bağlam penceresi (4k PDF kısıtın için ideal)
        }
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
    except Exception as e:
        print(f"Ollama API Hatası: {e}")
        return None

def process_pdf(pdf_file_path, output_md_path):
    print(f"1. '{pdf_file_path}' ayrıştırılıyor...")
    raw_text = extract_text_from_pdf(pdf_file_path)
    
    if not raw_text:
        print("Hata: PDF'ten metin okunamadı.")
        return
        
    print("2. Metin Qwen2.5 (Ollama) ile Markdown'a dönüştürülüyor...")
    markdown_output = format_with_ollama(raw_text)
    
    if markdown_output:
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(markdown_output)
        print(f"✅ Başarılı! Çıktı '{output_md_path}' dosyasına kaydedildi.")

# --- KULLANIM ÖRNEĞİ ---
if __name__ == "__main__":
    # Test etmek istediğin PDF dosyasının adını buraya yaz:
    sample_pdf = "ornek.pdf" 
    output_md = "cikti.md"
    
    # İşlemi başlat
    process_pdf(sample_pdf, output_md)