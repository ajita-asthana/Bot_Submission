import subprocess
import json

# sample input
input_data = {
    "opponent": "test_bot",
    "history": ["rock", "paper", "scissors", "rock", "rock", "paper"],
}

# proc rps_bot.py
proc = subprocess.Popen(
    ["python3", "rps_bot.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

stdout, stderr = proc.communicate(json.dumps(input_data))

print("Bot output:", stdout.strip())
if stderr:
    print("Bot error:", stderr.strip())
