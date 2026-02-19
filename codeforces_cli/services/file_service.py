from pathlib import Path
import subprocess

from codeforces_cli.submit.languages import EXTENSION_TO_LANGUAGE, LANGUAGES


def create_solution_file(contest_id: int, index: str, language: str) -> Path:
    normalized_language = language.lower()
    if normalized_language not in LANGUAGES:
        allowed = ", ".join(sorted(LANGUAGES.keys()))
        raise Exception(f"Unsupported language '{language}'. Allowed: {allowed}")

    contest_dir = Path(str(contest_id))
    contest_dir.mkdir(parents=True, exist_ok=True)

    extension = LANGUAGES[normalized_language]["extension"]
    file_path = contest_dir / f"{index.upper()}.{extension}"

    if file_path.exists():
        raise Exception(f"File already exists: {file_path}")

    template = LANGUAGES[normalized_language]["template"]
    file_path.write_text(template, encoding="utf-8")

    return file_path


def find_solution_file(contest_id: int, index: str) -> Path:
    contest_dir = Path(str(contest_id))
    if not contest_dir.exists():
        raise Exception(f"Contest folder not found: {contest_dir}")

    uppercase_index = index.upper()
    for extension in EXTENSION_TO_LANGUAGE:
        candidate = contest_dir / f"{uppercase_index}{extension}"
        if candidate.exists():
            return candidate

    raise Exception(f"No solution file found for {contest_id} {uppercase_index}")


def detect_language_from_file(file_path: Path) -> str:
    language = EXTENSION_TO_LANGUAGE.get(file_path.suffix.lower())
    if not language:
        raise Exception(f"Unsupported file extension: {file_path.suffix}")
    return language


def open_file_in_vscode(file_path: Path) -> None:
    subprocess.run(["code", str(file_path.resolve())], check=True)
