# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder is a content-based music recommender designed for classroom exploration. It generates a ranked list of 5 songs from a small catalog based on a user's stated preferences for genre, mood, energy level, and acoustic taste. It assumes users know what genre and mood they want upfront — it does not learn from listening history or adapt over time. This is an educational tool for understanding how recommendation scoring works, not a production system.

**Not intended for:** real-world music apps, commercial playlist generation, or drawing conclusions about actual user behavior. The catalog is too small (20 songs), genre matching is too rigid, and the system has no awareness of listening history, popularity, or cultural context. It should not be used to profile or make decisions about real users.

---

## 3. How the Model Works

The system scores every song in the catalog against a user profile, then returns the top 5. Think of it like a checklist with weighted importance:

- **Genre match (1.0 pts):** Does the song's genre exactly match what the user asked for? This is all-or-nothing — "indie pop" does not count as "pop."
- **Mood match (1.0 pts):** Same exact-match logic for mood. "Chill" matches "chill" but not "relaxed."
- **Energy closeness (up to 2.0 pts):** How close is the song's energy level to what the user wants? This is the most influential dimension — a perfect energy match earns 2.0, and the score decreases linearly with distance.
- **Acoustic fit (0.5 pts):** If the user likes acoustic music, songs with acousticness above 0.6 get a bonus. If not, songs below 0.4 get it.

The maximum possible score is 4.50. We started with genre weighted at 2.0 and energy at 1.0, but after experimentation we found that doubling energy's weight and halving genre's weight produced more musically intuitive rankings.

---

## 4. Data

The catalog contains **20 songs** spanning 17 genres and 16 moods. Each song has numeric attributes for energy, tempo, valence, danceability, and acousticness.

- **Genre distribution:** Lofi has 3 songs, pop has 2, and every other genre (rock, jazz, edm, metal, folk, etc.) has exactly 1. This means most genre preferences can only match a single song.
- **Mood distribution:** Chill has 3 songs, happy and intense each have 2, and the remaining 13 moods have 1 each.
- **Missing representation:** Popular genres like latin, k-pop, punk, and blues have zero representation. The catalog also has no songs with both high energy (>0.7) and high acousticness (>0.6), which is a real combination in music (e.g., acoustic punk, flamenco).
- **Unused features:** Tempo, valence, and danceability exist in the data but are not used by the scoring logic.

---

## 5. Strengths

- Works well for users whose preferences align with well-represented genres. The "Chill Lofi" profile produced a perfect 4.50/4.50 match (Library Rain), and the "Intense Rock" profile scored 4.48 with Storm Runner.
- Energy closeness as a continuous score (rather than binary) captures real musical nuance — a song at 0.82 energy feels different from one at 0.93, and the scoring reflects that.
- The explanation strings make the scoring transparent. A user can see exactly which dimensions matched and why a song ranked where it did.

---

## 6. Limitations and Bias

The system's genre matching is strictly exact, which creates a structural bias against users who like genres that are close but not identical to catalog entries — a user who likes "pop" will never see "indie pop" recommendations even though these genres share significant musical DNA. This also means the system over-rewards the few genres with multiple entries (lofi with 3 songs gets 3 chances to match, while rock gets only 1), creating an uneven playing field where lofi fans consistently get higher-scoring results than fans of solo-entry genres. Additionally, the dataset contains a hidden correlation between acousticness and energy: every song with acousticness above 0.6 has energy below 0.63, which means users who want high-energy acoustic music (a real preference — think live Mumford & Sons) will always receive conflicting recommendations where the system cannot satisfy both dimensions simultaneously. Finally, the energy gap calculation never produces negative scores, so even a wildly mismatched song (energy 0.01 for a user wanting 0.99) still earns 0.04 from energy rather than being penalized — this prevents truly bad matches from being pushed to the bottom.

---

## 7. Evaluation

We tested six user profiles across two weight configurations:

**Standard profiles tested:**
- **High-Energy Pop** (pop/happy/0.8/non-acoustic): Sunrise City scored 4.46 — near-perfect match. Rooftop Lights (indie pop/happy) ranked #2, beating Gym Hero (pop/intense) because energy closeness outweighed genre match after our weight shift. This felt musically right.
- **Chill Lofi** (lofi/chill/0.35/acoustic): Library Rain scored a perfect 4.50. The top 3 were all lofi — expected given lofi has 3 catalog entries.
- **Intense Rock** (rock/intense/0.9/non-acoustic): Storm Runner was the clear #1 at 4.48. Metal and EDM songs appeared in the top 5 due to similar energy, which makes musical sense.

**Adversarial profiles tested:**
- **Conflicting: High Energy + Chill** (lofi/chill/0.95/acoustic): Lofi songs still ranked #1-3 despite energy being marked "far." Genre+mood dominance held, but scores dropped from 4.36 to 3.44 compared to the non-conflicting Chill Lofi profile. Drop Zone (edm, energy 0.96) appeared at #5 — the energy pull was visible but not enough to overcome genre matching.
- **Nonexistent Genre & Mood** (k-pop/euphoric/0.5/non-acoustic): All scores clustered between 1.2-2.2 with no clear winner. The system degraded gracefully but had no way to signal low confidence.
- **Acoustic + High Energy** (folk/nostalgic/0.95/acoustic): Creek Walk (folk, energy 0.31) won at 3.22, but #2-5 were all high-energy non-acoustic songs (Drop Zone, Gym Hero, Iron Collapse). The tension between acoustic preference and energy preference was clearly visible.

**Weight experiment:** Doubling energy weight (1.0 to 2.0) and halving genre weight (2.0 to 1.0) made rankings more sensitive to energy proximity, which we kept. Removing mood entirely flattened rankings — songs with different vibes scored nearly identically — so we reverted that change.

---

## 8. Future Work

- **Genre similarity scoring:** Replace exact-match with a similarity map (e.g., "indie pop" gets 0.7 credit against "pop") to reduce the filter bubble effect.
- **Use unused features:** Incorporate valence, danceability, and tempo into scoring — a happy user probably wants high valence, and a party user wants high danceability.
- **Negative penalties:** Allow energy scores to go negative for extreme mismatches so truly bad recommendations get pushed out of the top 5.
- **Confidence indicator:** When no genre or mood matches exist, surface a warning like "low confidence — no direct matches found" instead of silently returning mediocre results.
- **Expand the catalog:** 20 songs with 17 genres means most genres are singletons. A larger, more balanced dataset would make the system more useful for diverse tastes.

---

## 9. Personal Reflection

**Biggest learning moment:** Realizing that weights matter more than features. The same four dimensions — genre, mood, energy, acoustic — produced noticeably different rankings just by changing how much each one counted. When we halved genre weight and doubled energy weight, Rooftop Lights jumped over Gym Hero for the High-Energy Pop profile. That single number change made the output feel more musically correct. It showed me that designing a recommender isn't just about *what* you measure, it's about *how much you trust* each measurement.

**Using AI tools:** Claude helped design the six test profiles, identify the acoustic-energy correlation in the dataset, and write the scoring explanation in plain language. The moments where I had to double-check were the edge case predictions — Claude predicted that removing mood would "flatten" rankings, which I verified by actually running the output. Numbers matched, but I wouldn't have trusted the prediction without seeing the terminal output myself. AI is fast at reasoning about what *should* happen; you still need to run the code to confirm it *does* happen.

**What surprised me about simple algorithms:** The system uses four rules and some addition, yet the top results for the Chill Lofi profile genuinely felt like something a friend with good music taste would recommend. Library Rain (4.50/4.50) is exactly the kind of song you'd queue up for a late-night study session. I didn't expect four weighted conditions to produce results that felt *curated*. The surprise is that "feels like a recommendation" is a low bar — you just need the most obviously wrong options to score low enough to not appear.

**What I'd try next:** Add genre similarity scoring (so "indie pop" gets partial credit for "pop"), incorporate the valence and danceability columns that are already in the dataset, and experiment with allowing negative energy scores for extreme mismatches. The negative penalty idea is the one I'm most curious about — it would let the system actively reject bad fits rather than just weakly preferring good ones.
