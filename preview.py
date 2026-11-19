from playwright.sync_api import sync_playwright
import pathlib, sys

base = pathlib.Path("/workspace/system-lab/index.html").as_uri()
out = pathlib.Path("/workspace/tool-results/preview"); out.mkdir(parents=True, exist_ok=True)

def shots(pw, w, h, tag):
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
    pg.goto(base, wait_until="load")
    pg.wait_for_timeout(1200)
    total = pg.evaluate("document.body.scrollHeight")
    print(tag, "height", total)
    pg.screenshot(path=str(out / f"{tag}-01-top.png"))
    for i, y in enumerate([int(total*0.28), int(total*0.55), int(total*0.78)]):
        pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(700)
        pg.screenshot(path=str(out / f"{tag}-0{i+2}-scroll.png"))
    # bottom
    pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(700)
    pg.screenshot(path=str(out / f"{tag}-05-bottom.png"))
    b.close()

with sync_playwright() as pw:
    shots(pw, 1440, 900, "pc")
    shots(pw, 390, 844, "mo")
print("done")
