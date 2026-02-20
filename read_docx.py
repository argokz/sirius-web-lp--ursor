
import docx
import os

def read_docx(file_path):
    print(f"\n--- START CONTENT: {file_path} ---")
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
            
        doc = docx.Document(file_path)
        # Print first 2000 chars to avoid overwhelming output, or full if short
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text)
        
        text = '\n'.join(full_text)
        print(text[:5000]) # Limit to 5000 chars for now
        if len(text) > 5000:
            print("\n... [TRUNCATED] ...")
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    print(f"--- END CONTENT: {file_path} ---\n")

if __name__ == "__main__":
    read_docx(r"h:\projects\sirius-web-lp\Сайт_ТГИД.docx")
    # read_docx(r"h:\projects\sirius-web-lp\Сбор информации с сайта Politerm.com.docx") 
