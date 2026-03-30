import fitz
from pathlib import Path
from nltk.tokenize import sent_tokenize

class DocumentIngester:
    def extract_pdf(self, fp):
        doc = fitz.open(fp)
        txt = ''.join(p.get_text('text') + chr(10) for p in doc)
        doc.close()
        return txt.strip()

    def extract_txt(self, fp):
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read().strip()

    def extract_docx(self, fp):
        from docx import Document
        d = Document(fp)
        return chr(10).join(p.text for p in d.paragraphs if p.text.strip())

    def extract(self, fp):
        ext = Path(fp).suffix.lower()
        if ext == '.pdf':   return self.extract_pdf(fp)
        if ext == '.txt':   return self.extract_txt(fp)
        if ext in ('.docx', '.doc'): return self.extract_docx(fp)
        raise ValueError(f'Unsupported: {ext}')

    def chunk_text(self, text, chunk_size=300):
        sentences = sent_tokenize(text)
        chunks, cur, cur_len = [], [], 0
        for s in sentences:
            wlen = len(s.split())
            if cur_len + wlen > chunk_size and cur:
                chunks.append(' '.join(cur))
                cur = cur[-2:]
                cur_len = sum(len(x.split()) for x in cur)
            cur.append(s)
            cur_len += wlen
        if cur: chunks.append(' '.join(cur))
        return [c for c in chunks if len(c.split()) > 30]
