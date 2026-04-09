# Scoring Rule: Proximity-Based Content Similarity

The core principle: **closer to the user's target = higher score**. A song with energy 0.7 and a song with energy 0.3 should score equally for a user who targets 0.5 — neither is "better" for having a higher or lower value.

---

## Step 1: Normalize All Features to 0.0–1.0

Before scoring, every feature must be on the same scale.

Four features are already normalized: `energy`, `valence`, `danceability`, `acousticness` (all 0.0–1.0).

Tempo needs min-max normalization:

```
                    tempo_bpm - MIN_TEMPO
normalized_tempo = ───────────────────────
                    MAX_TEMPO - MIN_TEMPO
```

Where `MIN_TEMPO = 60` and `MAX_TEMPO = 152` (from current dataset).

Example: a song at 120 bpm → `(120 - 60) / (152 - 60) = 0.652`

---

## Step 2: Compute Per-Feature Proximity Score

For each numeric feature, compute how **close** the song's value is to the user's target.

```
proximity(feature) = 1 - | user_target - song_value |
```

This produces a value between 0.0 and 1.0 where:
- **1.0** = perfect match (song value equals user target exactly)
- **0.0** = maximum mismatch (opposite ends of the scale)

### Example

```
User target_energy = 0.8
Song A energy      = 0.82  →  proximity = 1 - |0.8 - 0.82| = 1 - 0.02 = 0.98
Song B energy      = 0.42  →  proximity = 1 - |0.8 - 0.42| = 1 - 0.38 = 0.62
Song C energy      = 0.91  →  proximity = 1 - |0.8 - 0.91| = 1 - 0.11 = 0.89
```

Song A scores highest — not because it has the highest energy, but because it's **closest** to what the user wants.

---

## Step 3: Apply Feature Weights

Not all features matter equally. Weights let the system (or user) control importance.

```
weighted_proximity(feature) = weight(feature) × proximity(feature)
```

### Default Weights

| Feature | Weight | Rationale |
|---------|--------|-----------|
| energy | 0.30 | Strongest context signal (workout vs sleep) |
| valence | 0.25 | Emotional tone drives satisfaction |
| danceability | 0.20 | Key for activity-based listening |
| acousticness | 0.15 | Separates taste clusters |
| tempo | 0.10 | Matters but less perceptible than other features |
| **Total** | **1.00** | |

Weights must sum to 1.0 so the final score stays in the 0.0–1.0 range.

---

## Step 4: Compute Genre Bonus

Genre is categorical — it can't use proximity. Instead, apply a flat bonus for an exact match.

```
genre_bonus = GENRE_WEIGHT  if song.genre == user.favorite_genre
              0.0           otherwise
```

Where `GENRE_WEIGHT = 0.15` (added on top of the weighted sum).

---

## Step 5: Final Score Formula

```
                    n
score(song) =  Σ   weight_i × (1 - |user_target_i - song_value_i|)  +  genre_bonus
                   i=1
```

Expanded:

```
score =   0.30 × (1 - |target_energy       - song.energy|)
        + 0.25 × (1 - |target_valence      - song.valence|)
        + 0.20 × (1 - |target_danceability  - song.danceability|)
        + 0.15 × (1 - |target_acousticness  - song.acousticness|)
        + 0.10 × (1 - |target_tempo         - song.normalized_tempo|)
        + genre_bonus
```

### Score Range

- **Without genre bonus:** 0.0 to 1.0
- **With genre bonus:** 0.0 to 1.15
- To keep scores in 0.0–1.0, optionally divide by (1 + GENRE_WEIGHT): `final = score / 1.15`

---

## Worked Example

**User Profile:**
```
target_energy       = 0.80
target_valence      = 0.85
target_danceability = 0.75
target_acousticness = 0.20
target_tempo        = 0.63  (≈ 118 bpm normalized)
favorite_genre      = "pop"
```

**Song: "Sunrise City"** (pop, energy=0.82, valence=0.84, danceability=0.79, acousticness=0.18, tempo=118bpm)

```
normalized_tempo = (118 - 60) / (152 - 60) = 0.630

energy proximity      = 1 - |0.80 - 0.82| = 0.980  × 0.30 = 0.294
valence proximity     = 1 - |0.85 - 0.84| = 0.990  × 0.25 = 0.248
danceability proximity= 1 - |0.75 - 0.79| = 0.960  × 0.20 = 0.192
acousticness proximity= 1 - |0.20 - 0.18| = 0.980  × 0.15 = 0.147
tempo proximity       = 1 - |0.63 - 0.63| = 1.000  × 0.10 = 0.100
                                                     ─────────────
                                          subtotal =         0.981
genre bonus (pop == pop)                           =       + 0.150
                                                     ─────────────
                                        raw score  =         1.131
                                        normalized =  1.131 / 1.15 = 0.983
```

**Song: "Spacewalk Thoughts"** (ambient, energy=0.28, valence=0.65, danceability=0.41, acousticness=0.92, tempo=60bpm)

```
normalized_tempo = (60 - 60) / (152 - 60) = 0.000

energy proximity      = 1 - |0.80 - 0.28| = 0.480  × 0.30 = 0.144
valence proximity     = 1 - |0.85 - 0.65| = 0.800  × 0.25 = 0.200
danceability proximity= 1 - |0.75 - 0.41| = 0.660  × 0.20 = 0.132
acousticness proximity= 1 - |0.20 - 0.92| = 0.280  × 0.15 = 0.042
tempo proximity       = 1 - |0.63 - 0.00| = 0.370  × 0.10 = 0.037
                                                     ─────────────
                                          subtotal =         0.555
genre bonus (ambient ≠ pop)                        =       + 0.000
                                                     ─────────────
                                        raw score  =         0.555
                                        normalized =  0.555 / 1.15 = 0.483
```

**Result:** Sunrise City (0.983) ranks far above Spacewalk Thoughts (0.483) — not because it has higher energy, but because every feature is **closer** to what this user wants.

---

## Step 6: Ranking with Diversity

Scoring alone produces a ranked list — but naive score-sorting creates repetitive recommendations. The ranking layer re-orders the scored list to balance **relevance** (high scores) with **diversity** (variety across genres, artists, and sound).

### The Problem with Score-Only Ranking

```
Pure score sort for a pop/happy user:
1. Pop   — Sunrise City       — 0.983
2. Pop   — Gym Hero           — 0.941
3. Pop   — Rooftop Lights*    — 0.912   (* indie pop, close enough)
4. Pop   — ...more pop...
→ User hears the same sound 5 times. Bored. Leaves.
```

### Greedy Re-Ranking Algorithm

After scoring all songs, build the final list one slot at a time using a **greedy selection** that balances score and diversity:

```
ranked_list = []
candidates  = all songs sorted by score descending

for each slot in top-k:
    for each candidate (highest score first):
        penalty = 0.0

        # Artist cap: skip if this artist already appears too many times
        if count(candidate.artist in ranked_list) >= MAX_PER_ARTIST:
            skip this candidate

        # Genre repetition penalty: reduce score if same genre as previous song
        if ranked_list is not empty AND candidate.genre == ranked_list[-1].genre:
            penalty += SAME_GENRE_PENALTY

        adjusted_score = candidate.score - penalty

    pick the candidate with the highest adjusted_score
    add to ranked_list
    remove from candidates
```

### Tunable Parameters

| Parameter | Default | Effect |
|-----------|---------|--------|
| `MAX_PER_ARTIST` | 2 | No artist appears more than twice in top-k. Prevents one artist dominating. |
| `SAME_GENRE_PENALTY` | 0.10 | Reduces score by 0.10 if a song shares genre with the previous pick. Encourages genre alternation without overriding strong matches. |

### Why These Defaults Work

- **`MAX_PER_ARTIST = 2`**: With only 10 songs in the catalog, a cap of 2 is generous. In a real catalog of millions, this would be 2–3.
- **`SAME_GENRE_PENALTY = 0.10`**: Small enough that a great match still wins (a 0.95 pop song beats a 0.88 lofi song even after penalty), but large enough to break ties in favor of variety.

### Worked Example

User targets: pop, high energy. Top 5 by raw score:

```
Raw score order:
1. Sunrise City      (pop,  Neon Echo)     — 0.983
2. Gym Hero          (pop,  Max Pulse)     — 0.941
3. Rooftop Lights    (indie pop, Indigo)   — 0.912
4. Night Drive Loop  (synthwave, Neon Echo)— 0.804
5. Storm Runner      (rock, Voltline)      — 0.762
```

Greedy re-ranking with diversity:

```
Slot 1: Sunrise City (0.983) — first pick, no penalty
        → ranked_list = [Sunrise City]

Slot 2: Gym Hero raw = 0.941, but same genre as slot 1 → 0.941 - 0.10 = 0.841
        Rooftop Lights raw = 0.912, indie pop ≠ pop → no penalty → 0.912
        → Pick Rooftop Lights (0.912 > 0.841)
        → ranked_list = [Sunrise City, Rooftop Lights]

Slot 3: Gym Hero raw = 0.941, pop ≠ indie pop (prev) → no penalty → 0.941
        → Pick Gym Hero (0.941)
        → ranked_list = [Sunrise City, Rooftop Lights, Gym Hero]

Slot 4: Night Drive Loop raw = 0.804, synthwave ≠ pop (prev) → no penalty → 0.804
        → Pick Night Drive Loop (0.804)
        → ranked_list = [..., Night Drive Loop]

Slot 5: Storm Runner raw = 0.762, rock ≠ synthwave (prev) → no penalty → 0.762
        But wait — Neon Echo already has 2 songs (Sunrise City + Night Drive Loop)
        → MAX_PER_ARTIST check passes for Storm Runner (Voltline has 1)
        → Pick Storm Runner (0.762)
```

**Final list with diversity:**
```
1. Sunrise City      (pop)       — 0.983  ← best match
2. Rooftop Lights    (indie pop) — 0.912  ← genre break
3. Gym Hero          (pop)       — 0.941  ← pop returns after a break
4. Night Drive Loop  (synthwave) — 0.804  ← new genre introduced
5. Storm Runner      (rock)      — 0.762  ← discovery slot
```

Compare to pure score sort which would have been: pop, pop, indie pop, synthwave, rock. The diversity-aware version **interleaves genres** while keeping the highest-scoring song at #1.

---

## Summary

| Step | Operation | Output |
|------|-----------|--------|
| 1 | Normalize tempo to 0–1 | All features on same scale |
| 2 | `1 - |target - value|` per feature | Proximity score per feature (0–1) |
| 3 | Multiply by weight | Weighted proximity per feature |
| 4 | Add genre bonus if match | Categorical boost |
| 5 | Sum all terms | Individual song score |
| **6** | **Greedy re-rank with diversity penalties** | **Final ordered recommendation list** |
