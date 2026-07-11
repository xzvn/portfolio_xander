from pathlib import Path
from pprint import pformat


ROOT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = ROOT_DIR / "templates"
OUTPUT_FILE = ROOT_DIR / "embedded_templates.py"


def main() -> None:
    if not TEMPLATE_DIR.is_dir():
        raise SystemExit(f"Folder template tidak ditemukan: {TEMPLATE_DIR}")

    template_files = sorted(TEMPLATE_DIR.rglob("*.html"))

    if not template_files:
        raise SystemExit("Tidak ada file HTML di dalam folder templates.")

    templates: dict[str, str] = {}

    for file_path in template_files:
        template_name = file_path.relative_to(TEMPLATE_DIR).as_posix()
        templates[template_name] = file_path.read_text(encoding="utf-8")

    generated_content = (
        '"""File ini dibuat otomatis oleh build_templates.py.\n'
        "Jangan diedit manual. Jalankan ulang build_templates.py "
        'setelah mengubah template.\n'
        '"""\n\n'
        f"EMBEDDED_TEMPLATES = {pformat(templates, width=120, sort_dicts=True)}\n"
    )

    OUTPUT_FILE.write_text(
        generated_content,
        encoding="utf-8",
        newline="\n",
    )

    print(f"Berhasil membuat {OUTPUT_FILE.name}")
    print(f"Jumlah template: {len(templates)}")

    for template_name in templates:
        print(f"- {template_name}")


if __name__ == "__main__":
    main()
