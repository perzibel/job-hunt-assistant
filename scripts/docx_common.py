"""Shared helper: convert a .docx to .pdf with whatever is available (docx2pdf/Word, or LibreOffice)."""
import os, shutil, subprocess


def to_pdf(docx_path):
    pdf = os.path.splitext(docx_path)[0] + ".pdf"
    try:
        from docx2pdf import convert  # uses Microsoft Word on Windows/macOS
        convert(docx_path, pdf)
        return "Wrote " + pdf
    except Exception:
        pass
    if os.name == "nt":  # Microsoft Word via COM, no extra packages needed
        src, dst = os.path.abspath(docx_path).replace("'", "''"), os.path.abspath(pdf).replace("'", "''")
        ps = (f"$w = New-Object -ComObject Word.Application; $w.Visible = $false; "
              f"$d = $w.Documents.Open('{src}'); $d.SaveAs([ref]'{dst}', [ref]17); $d.Close(); $w.Quit()")
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=False, capture_output=True, timeout=120)
        if os.path.exists(pdf):
            return "Wrote " + pdf
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice and os.name == "nt":
        cand = r"C:\Program Files\LibreOffice\program\soffice.exe"
        soffice = cand if os.path.exists(cand) else None
    if soffice:
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir",
                        os.path.dirname(os.path.abspath(docx_path)), docx_path], check=False, capture_output=True)
        if os.path.exists(pdf):
            return "Wrote " + pdf
    return ("PDF not created: install Word + `pip install docx2pdf`, or LibreOffice. "
            "Or open the .docx and Save As PDF.")
