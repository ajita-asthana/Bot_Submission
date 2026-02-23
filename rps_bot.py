import sys
import json
import os
import random
from collections import defaultdict

STATE_FILE = "rps_state.json"
MOVES = ["rock", "paper", "scissors"]


def beats(m):
    return {"rock": "paper", "paper": "scissors", "scissors": "rock"}[m]


def loses_to(m):
    return {"rock": "scissors", "paper": "rock", "scissors": "paper"}[m]


def valid(m):
    return m in MOVES


# --------- Persistance ----------


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_state(state):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except:
        pass


# ------- Predictors ----------


def freq_predict(history):
    if not history:
        return None
    counts = defaultdict(int)
    for m in history:
        if valid(m):
            counts[m] += 1
    return max(MOVES, key=lambda m: counts[m])


def markov1_predict(history):
    if len(history) < 2:
        return None
    last = history[-1]
    counts = defaultdict(int)
    for i in range(len(history) - 1):
        if history[i] == last:
            counts[history[i + 1]] += 1
    if not counts:
        return None
    return max(counts, key=counts.get)


def markov2_predict(history):
    if len(history) < 3:
        return None
    a, b = history[-2], history[-1]
    counts = defaultdict(int)
    for i in range(len(history) - 2):
        if history[i] == a and history[i + 1] == b:
            counts[history[i + 2]] += 1
    if not counts:
        return None
    return max(counts, key=counts.get)


def cycle_predict(history):
    n = len(history)
    if n < 4:
        return None
    for p in range(2, min(6, n)):
        if history[-p:] == history[-2 * p : -p]:
            return history[-p]
    return None


def react_predict(state):
    my = state["my_moves"]
    opp = state["opp_moves"]
    if len(my) < 2 or len(opp) < 2:
        return None

    hypothesis = {
        "copy": lambda m: m,
        "counter": lambda m: beats(m),
        "throw": lambda m: loses_to(m),
    }

    best_acc = 0
    best_pred = 0

    for name, fn in hypotheses.items():
        correct = 0
        total = 0
        for i in range(1, len(opp)):
            if fn(my[i - 1]) == opp[i]:
                correct += 1
            total += 1
        if total > 0:
            acc = correct / total
            if acc > best_acc:
                best_acc = acc
                best_pred = fn(my[-1])

    if best_acc > 0.55:
        return best_pred
    return None


# ------ Utility ---------


def overlap(prev, curr):
    # find longest suffix of prev matching of curr
    for k in range(min(len(prev), len(curr)), -1, -1):
        if prev[-k:] == curr[:k]:
            return k
    return 0


# ----------- Main ----------


def main():
    data = json.loads(sys.stdin.read())
    opponent = data["opponent"]
    history = [m for m in data.get("history", []) if valid(m)]

    state = load_state()

    if opponent not in state:
        state[opponent] = {
            "prev_history": [],
            "my_moves": [],
            "opp_moves": [],
            "scores": {},
            "last_prediction": None,
        }

    opp_state = state[opponent]

    # Sync new opponent move
    k = overlap(opp_state["prev_history"], history)
    new_moves = history[k:]

    if new_moves:
        opp_state["opp_moves"].extend(new_moves)

        # update predictor score
        if opp_state["last_prediction"]:
            pred = opp_state["last_prediction"]
            actual = new_moves[-1]
            score = opp_state["scores"].get(pred, 0)
            opp_state["scores"][pred] = score * 0.9 + (1 if pred == actual else 0)

    opp_state["prev_history"] = history.copy()

    predictors = {
        "freq": freq_predict(history),
        "markov1": markov1_predict(history),
        "markov2": markov2_predict(history),
        "cycle": cycle_predict(history),
        "react": react_predict(opp_state),
    }

    best_name = None
    best_score = -1
    best_prediction = None

    for name, prediction in predictors.items():
        if prediction:
            score = opp_state["scores"].get(name, 0)
            if score > best_score:
                best_score = score
                best_name = name
                best_prediction = prediction

    if not best_prediction:
        my_move = random.choice(MOVES)
        opp_state["last_prediction"] = None
    else:
        my_move = beats(best_prediction)
        opp_state["last_prediction"] = best_name

    opp_state["my_moves"].append(my_move)
    save_state(state)

    print(my_move)


if __name__ == "__main__":
    main()
