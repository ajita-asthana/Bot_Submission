**README**

1. **Language and version**
   - Python 3.11 (single-file executable via shebang)

2. **Build instructions**
   - No compilation required.
   - Run example:
     ```bash
     echo '{"opponent":"abc123","history":["rock","rock","rock"]}' | python3 rps_bot.py
     ```

3. **Approach and design choices**
   - Goal: Exceed 70% win-or-tie against diverse opponents using only last-10 move history.
   - Uses an ensemble of lightweight predictors (frequency, cycle, repeat, reaction, n-gram).
   - Scores predictors online and plays the counter to the best-performing predictor.

4. **Assumptions**
   - Bot receives opponent id and last up-to-10 moves.
   - Outputs one of: rock, paper, or scissors.
   - Optional: local persistence allowed for per-opponent modeling.

5. **Trade-offs**
   - Ensemble avoids overfitting to one opponent type.
   - Persistence improves performance against reactive opponents but depends on filesystem permissions.
   - Predictors are O(10) per call; well under 100ms.

6. **How well does your bot perform against itself?**
   - In self-play, bots adapt and converge toward high tie rates (often near 100% ties).
   - Win-or-tie rate is very high; win rate close to 33% due to symmetry.
