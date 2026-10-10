"""Build static HTML from trusted local templates and JSON data."""
from pathlib import Path
import json
import shutil
import tempfile
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
ROOT = Path(__file__).resolve().parent.parent

def build():
    source = ROOT / "src"
    data = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (source / "data").glob("*.json")}
    env = Environment(loader=FileSystemLoader(str(source)), autoescape=select_autoescape(["html"]), undefined=StrictUndefined)
    output = Path(tempfile.mkdtemp(prefix=".uit-build-", dir=ROOT))
    try:
        for page in data["pages"]:
            target = output / page["source"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(env.get_template("pages/" + page["source"]).render(page=page, **data), encoding="utf-8")
        # Preserve public asset routes during migration.
        for name, destination in [("css", "assets/css"), ("fonts", "assets/fonts"), ("images", "assets/images"), ("pdfs", "assets/pdfs"), ("themes", "assets/themes"), ("js", "js")]:
            path = source / "assets" / name
            if path.exists():
                shutil.copytree(path, output / destination, dirs_exist_ok=True)
        shutil.copytree(source / "static", output, dirs_exist_ok=True)
        (output / ".nojekyll").touch()
        old = ROOT / "dist"
        if old.exists():
            shutil.rmtree(old)
        output.rename(old)
        print(f"Built {len(data['pages'])} pages → {old}")
        return old
    except Exception:
        shutil.rmtree(output)
        raise

if __name__ == "__main__":
    build()
