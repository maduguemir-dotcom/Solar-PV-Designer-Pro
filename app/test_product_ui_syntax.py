from pathlib import Path
import traceback

print("=" * 70)
print("PRODUCT_UI.PY SYNTAX DIAGNOSTIC")
print("=" * 70)

file_path = Path(__file__).parent / "product_ui.py"

print(f"\nChecking file:\n{file_path}\n")

try:
    source_code = file_path.read_text(encoding="utf-8")

    compile(
        source_code,
        str(file_path),
        "exec"
    )

    print("SUCCESS: product_ui.py has no syntax or indentation errors.")

except SyntaxError as error:

    print("\nERROR DETECTED")
    print("-" * 70)

    print(f"Error type: {type(error).__name__}")
    print(f"Message: {error.msg}")
    print(f"Line number: {error.lineno}")
    print(f"Column: {error.offset}")

    lines = source_code.splitlines()

    start = max(0, error.lineno - 6)
    end = min(len(lines), error.lineno + 5)

    print("\nCODE AROUND THE ERROR:")
    print("-" * 70)

    for index in range(start, end):
        marker = ">>>" if index + 1 == error.lineno else "   "

        print(
            f"{marker} {index + 1:4}: "
            f"{lines[index]}"
        )

    print("\nFULL TRACEBACK:")
    print("-" * 70)

    traceback.print_exc()

except Exception as error:

    print("\nUNEXPECTED ERROR:")
    print(error)

    traceback.print_exc()
