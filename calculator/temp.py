import subprocess

expression = "3 + 7 * 2"

result = subprocess.run(["python", "main.py", expression], capture_output=True, text=True)

print(result.stdout)
print(result.stderr)