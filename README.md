 # Music Recommender Simulation

## Project Summary

VibeFinder 1.0 is a content-based music recommender that scores 20 songs against a user's taste profile and returns the top 5 matches. It uses four dimensions — genre, mood, energy, and acousticness — to produce a weighted score (max 4.50) with a human-readable explanation for each recommendation. We tested it across six user profiles including adversarial edge cases, ran two weight experiments, and documented the results in a model card.

---

## How The System Works

Our recommender compares a user's taste preferences (genre, mood, energy level, acoustic preference) against each song's attributes to calculate a similarity score. Songs are ranked by score and the top k are returned.

- **Song features used:** genre, mood, energy, acousticness. Tempo, valence, and danceability exist in the dataset but are not used in scoring.
- **UserProfile stores:** `favorite_genre`, `favorite_mood`, `target_energy` (0.0-1.0), and `likes_acoustic` (boolean). These four dimensions distinguish listener types like intense rock fans from chill lofi listeners.
- **Scoring:** Genre match = +1.0, mood match = +1.0, energy closeness = up to +2.0 (calculated as `2.0 * (1.0 - abs(song.energy - target))`), acoustic fit = +0.5. Max score is 4.50. Energy carries the most weight after our tuning experiment.
- **Ranking:** Every song gets scored, the list is sorted descending, and the top 5 are returned with scores and explanation strings. No randomness or diversity re-ranking is applied.

```
  INPUT                    PROCESS                        OUTPUT
┌───────────┐   ┌──────────────────────────────┐   ┌─────────────┐
│ songs.csv │──▶│  load_songs()                │   │             │
└───────────┘   │  List of song dicts          │   │  Top-K      │
                └──────────────┬───────────────┘   │  Results    │
┌───────────┐                  │                   │             │
│ User      │   ┌──────────────▼───────────────┐   │ (song,      │
│ Prefs     │──▶│  For each song:              │──▶│  score,     │
│           │   │                              │   │  explain)   │
│ genre     │   │  Genre match?   +0 or +1.0   │   │             │
│ mood      │   │  Mood match?    +0 or +1.0   │   └─────────────┘
│ energy    │   │  Energy sim.    +0.0 to +2.0 │
│ likes_    │   │  Acoustic fit?  +0 or +0.5   │
│  acoustic │   │  ──────────────────────────  │
└───────────┘   │  total score = sum above     │
                │  explanation = describe why   │
                │                              │
                │  Sort by score DESC          │
                │  Return top K                │
                └──────────────────────────────┘
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   PYTHONPATH=src python src/main.py
   ```

### Running Tests

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

- **Weight shift (genre x1, energy x2):** Halved genre weight from 2.0 to 1.0 and doubled energy from 1.0 to 2.0. This caused Rooftop Lights (indie pop/happy) to jump over Gym Hero (pop/intense) for the High-Energy Pop profile, producing more musically intuitive rankings. We kept this change.
- **Mood removal:** Commented out the mood check entirely. Rankings flattened — songs with completely different vibes scored nearly identically. Groove Committee (funk/groovy) ranked above Rooftop Lights (indie pop/happy) for a happy pop listener. We reverted this change.
- **Six user profiles tested:** High-Energy Pop, Chill Lofi, Intense Rock, Conflicting (high energy + chill), Nonexistent Genre (k-pop/euphoric), and Acoustic + High Energy. The conflicting profile showed that genre+mood dominates even with extreme energy mismatch. The nonexistent genre profile produced flat, low-confidence results clustered between 1.2-2.2.

<a href="/course_images/Screenshot 2026-04-09 at 2.35.54 PM.png" target="_blank"><img src='/course_images/ai110/Screenshot 2026-03-31 at 10.36.26 AM.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.
<a href="/course_images/Screenshot 2026-04-09 at 2.43.04 PM.png" target="_blank"><img src='/course_images/ai110/Screenshot 2026-03-31 at 10.36.26 AM.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.

---

## Limitations and Risks

- **Tiny catalog:** Only 20 songs across 17 genres means most genres have a single entry. The system can't offer variety within a genre.
- **Exact-match genre bias:** "indie pop" and "pop" are treated as completely different. Users who like related genres get no credit for near-matches.
- **Acoustic-energy correlation:** Every high-acousticness song in the dataset has low energy. Users who want both high energy and acoustic music will always get conflicting results.
- **No negative penalties:** A wildly mismatched song still earns a small positive energy score rather than being penalized, preventing truly bad matches from sinking to the bottom.
- **Ignores available features:** Tempo, valence, and danceability columns exist but are unused, limiting the system's ability to distinguish songs within the same genre.

See [model_card.md](model_card.md) for a deeper analysis.

---

## Reflection

[**Model Card**](model_card.md) | [**Reflection: Profile Comparisons**](reflection.md)

Recommenders turn data into predictions by reducing complex human taste to a handful of numbers, then doing arithmetic. What surprised me most is how effective this can be — four weighted rules produced a Chill Lofi top 5 that genuinely felt curated, not random. But the same simplicity creates blind spots: the system has no concept of genre similarity, so it treats "indie pop" and "pop" as unrelated as "pop" and "metal." In a real product, this kind of rigid matching could create filter bubbles where users never discover adjacent music they'd love.

Bias shows up in subtle structural ways, not just in the weights. The dataset's correlation between acousticness and energy means acoustic-loving users are silently funneled toward low-energy music, even if that's not what they asked for. A real system deployed at scale would need to audit these hidden correlations — they're invisible to the user but shape every recommendation they see.
