import subprocess
import json

test_cases = [
    {"opponent": "bot1", "history": ["rock", "rock", "rock"]},
    {"opponent": "bot2", "history": ["paper", "scissors", "paper", "scissors"]},
    {
        "opponent": "bot3",
        "history": ["rock", "paper", "scissors", "rock", "paper", "scissors"],
    },
    {"opponent": "bot4", "history": ["scissors", "scissors", "scissors", "scissors"]},
    {
        "opponent": "bot5",
        "history": ["rock", "paper", "rock", "paper", "rock", "paper"],
    },
]

for case in test_cases:
    proc = subprocess.Popen(
        ["python3", "rps_bot.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = proc.communicate(json.dumps(case))
    print(
        f"Opponent: {case['opponent']}, History: {case['history']}, Bot output: {stdout.strip()}"
    )
    if stderr:
        print("Error:", stderr.strip())
