from pathlib import Path

def secrets_ignored(text: str) -> bool:
    lines = {line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")}
    return ".env" in lines and ".env.*" in lines and "!.env.example" in lines

if __name__ == "__main__":
    content = Path(".gitignore").read_text(encoding="utf-8")
    assert secrets_ignored(content)
    print("PASS: .env files are ignored; .env.example may be committed")
