
import os

def fix_encoding():
    env_path = "backend/.env"
    if not os.path.exists(env_path):
        print("No .env found.")
        return

    content = ""
    # Try reading as UTF-16 (little endian, common in PowerShell)
    try:
        with open(env_path, "r", encoding="utf-16") as f:
            content = f.read()
        print("Read as UTF-16.")
    except Exception as e:
        print(f"Not UTF-16: {e}")
        # Try UTF-8
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                content = f.read()
            print("Read as UTF-8 (already correct?).")
        except Exception as e:
             print(f"Not UTF-8 either: {e}")
             return

    # Write back as UTF-8
    if content:
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print("Converted to UTF-8.")

if __name__ == "__main__":
    fix_encoding()
