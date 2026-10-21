"""Build dist/the-optimist-cookbook-app.html: inlines the Optimist font and cover texture into the page."""
import base64, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
b64 = lambda p: base64.b64encode((root / p).read_bytes()).decode()
html = (root / "src/app.template.html").read_text(encoding="utf8")
html = html.replace("__OPTIMIST__", b64("assets/fonts/Optimist-Regular.ttf")).replace("__TEXTURE__", b64("assets/tex-orange.jpg"))
(root / "dist").mkdir(exist_ok=True)
(root / "dist/the-optimist-cookbook-app.html").write_text(html, encoding="utf8")
print("built", len(html), "bytes")
