"""Phase 1 structural check; no third-party packages required."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "AGENTS.md", "README.md", ".gitignore", "sources.md",
    "wiki/index.md", "wiki/log.md", "outline.md", "report.md",
    ".agents/workflows/README.md", "raw/README.md"
]
REQUIRED_DIRS = ["raw", "raw/assets", "wiki", "cards", "drafts", "assets", "tests", ".agents/workflows"]


def main():
    failed = []
    for path in REQUIRED_FILES:
        good = (ROOT / path).is_file()
        print(f"{'PASS' if good else 'FAIL'} file: {path}")
        if not good:
            failed.append(path)
    for path in REQUIRED_DIRS:
        good = (ROOT / path).is_dir()
        print(f"{'PASS' if good else 'FAIL'} dir:  {path}")
        if not good:
            failed.append(path)
    # This validator runs in every phase. A generated deck is expected after Phase 4.
    deck = (ROOT / "deck.html").exists()
    if deck:
        good = (ROOT / "drafts/slide_01.md").is_file() and (ROOT / "assets/slide_content.json").is_file()
        print(f"{'PASS' if good else 'FAIL'} Phase 4 artifacts consistent with project scaffold")
        if not good:failed.append("incomplete Phase 4 scaffold")
    else:
        print("PASS: deck.html not yet generated (pre-Phase 4 allowed)")
    print(f"RESULT: {'FAIL' if failed else 'PASS'} ({len(failed)} issues)")
    return int(bool(failed))


if __name__ == "__main__":
    raise SystemExit(main())
