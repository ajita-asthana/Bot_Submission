# Bot Submission

1) Language + version
Python 3.11 (single-file executable via shebang) (or Go/Rust/C++ if you prefer — but Python is totally fine under 100ms)

2) How to run / build
Example for Python: echo '{"opponent":"abc123","history":["rock","rock","rock"]}' | python3 rps_bot.py

3) Approach and design choices
Goal: exceed 70% win-or-tie against a mix of opponent behaviors with only last-10 move history per opponent.

High-level strategy: use an ensemble of lightweight predictors over the opponent’s last moves, score them online, and play the counter to the best-performing predictor.

Predictors that work well in practice for these sandboxes:

Frequency model Predict opponent’s next move as the most common in history (or weighted toward recent moves).

Cycle detector If the last moves match a repeating pattern (e.g., r,p,s,r,p,s), extrapolate the next.

Last-move repeat / inertia If opponent repeats, predict same as last.

Reaction model (opponent reacts to our previous move) 
Look for mapping from our previous move → their next move. Even though we don’t directly receive our own move history, we can infer it by storing it per opponent locally (allowed — no network, but local state across invocations is typically allowed by writing to a file). If file I/O is not allowed, you can still do a weaker version based only on opponent history.

N-gram / Markov (order-2/3) Use last k opponent moves as a key; predict what usually follows.

Action selection: each predictor outputs a predicted opponent move. We compute the counter-move (paper beats rock, etc.). Maintain a running score per predictor (reward +1 for win, 0 for tie, -1 for loss). Choose the predictor with highest recent score (optionally use exponential decay).

This “online bandit over predictors” is simple, robust, and adapts quickly to different opponents.

4) Assumptions
Bot receives opponent id and last up-to-10 opponent moves (oldest→newest).
Bot must output exactly one of: rock|paper|scissors.
Optional: local persistence is allowed (write a small JSON state keyed by opponent id). If not allowed, the bot still works using only the provided history, but will be weaker against opponents that react to our move.

5) Trade-offs
Simplicity vs optimality: An ensemble avoids overfitting to one opponent type.

Persistence vs portability: Persisting state improves performance against reactive opponents, but depends on filesystem permissions.
Model complexity vs latency: All predictors are O(10) per call; well under 100ms.

6) How well does your bot perform against itself?
In self-play, both bots adapt similarly and converge toward high tie rates (often near ~100% ties if both detect each other’s patterns) or oscillatory behavior depending on exploration settings. Practically, expect win-or-tie to be very high (ties dominate), but win rate close to ~33% because symmetric opponents cancel advantages.
