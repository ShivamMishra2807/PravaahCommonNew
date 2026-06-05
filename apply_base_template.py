from pathlib import Path

src = Path(r"C:\Users\Admin\Downloads\base (1).html").read_text(encoding="utf-8")
Path("templates/base.html").write_text(src, encoding="utf-8")
print("Wrote templates/base.html")
