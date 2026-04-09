# Algorithm Recipe: Content-Based Music Recommender

A reference for what our scoring system needs before implementation.

---

## What We Have

### Song Features (`data/songs.csv`)
| Feature | Type | Range | Status |
|---------|------|-------|--------|
| energy | float | 0.0–1.0 | ✅ Ready |
| valence | float | 0.0–1.0 | ✅ Ready |
| danceability | float | 0.0–1.0 | ✅ Ready |
| acousticness | float | 0.0–1.0 | ✅ Ready |
| tempo_bpm | float | 60–152 | ⚠️ Needs normalization |
| genre | string | categorical | ✅ Ready (binary match) |
| mood | string | categorical | ⚠️ Redundant with valence+energy |

### User Preferences (`UserProfile` in `src/recommender.py`)
| Field | Type | Status |
|-------|------|--------|
| favorite_genre | str | ✅ Ready |
| favorite_mood | str | ⚠️ Redundant — mood is derived from valence+energy |
| target_energy | float | ✅ Ready |
| likes_acoustic | bool | ⚠️ Binary — should be a float target |

---

## What's Missing

### 1. Richer User Preference Vector

The user profile must have a numeric target for **every** numeric song feature so we can compute a proper distance vector.

| Missing Field | Type | Purpose |
|---------------|------|---------|
| `target_valence` | float (0.0–1.0) | Express preference for happy vs sad sounding music |
| `target_danceability` | float (0.0–1.0) | Distinguish chill listener from dance-floor seeker |
| `target_tempo` | float (0.0–1.0) | Express preference for fast vs slow songs (normalized) |
| `target_acousticness` | float (0.0–1.0) | Replace binary `likes_acoustic` with a continuous preference |

### 2. Feature Weights

Allow each user to express **which features matter most** to them.

| Missing Field | Type | Purpose |
|---------------|------|---------|
| `feature_weights` | Dict[str, float] | e.g. `{"energy": 0.3, "valence": 0.25, "danceability": 0.2, "acousticness": 0.15, "genre": 0.1}` |

Without weights, the algorithm treats all features as equally important — which is rarely true for any real listener.

### 3. Negative Signals

The system needs to know what the user **doesn't** want, not just what they prefer.

| Missing Field | Type | Purpose |
|---------------|------|---------|
| `disliked_genres` | List[str] | Filter out entire genres (e.g. "anything but country") |
| `disliked_moods` | List[str] | Avoid certain vibes (e.g. "nothing sad") |
| `energy_floor` | float | Minimum acceptable energy level |
| `energy_ceiling` | float | Maximum acceptable energy level |

Without negatives, the system can only rank by best match — it cannot filter out bad matches.

### 4. Listening History

Content-based systems build user profiles **from past behavior**. Even a simulated history enables key features.

| Missing Field | Type | Purpose |
|---------------|------|---------|
| `liked_song_ids` | List[int] | Avoid re-recommending songs already heard/liked |
| `disliked_song_ids` | List[int] | Penalize songs similar to ones the user rejected |

Bonus: with a listen history, the user preference vector can be **derived** by averaging the features of liked songs rather than requiring the user to declare their preferences manually.

### 5. Ranking / Diversity Controls

The scoring formula produces per-song scores, but the **ranking step** needs its own parameters to avoid repetitive results.

| Missing Field | Type | Purpose |
|---------------|------|---------|
| `max_per_artist` | int (default 2) | Cap how many songs from one artist can appear in top-k |
| `same_genre_penalty` | float (default 0.10) | Score penalty when a song shares genre with the previous pick in the ranked list |

These live on the `Recommender` (not `UserProfile`) since they control the system's ranking behavior, not individual taste.

### 6. Tempo Normalization

`tempo_bpm` ranges from 60–152+ while all other features are 0.0–1.0. Without normalization, tempo dominates any distance calculation.

**Normalization formula:**
```
normalized_tempo = (tempo_bpm - MIN_TEMPO) / (MAX_TEMPO - MIN_TEMPO)
```

Using the current dataset: `MIN_TEMPO = 60`, `MAX_TEMPO = 152`.

---

## Scoring Formula Outline

Once the above gaps are filled, the scoring algorithm follows this recipe:

```
1. FILTER  — Remove songs matching disliked_genres, disliked_moods,
             or outside energy floor/ceiling
2. FILTER  — Remove songs already in liked_song_ids (already heard)
3. NORMALIZE — Scale tempo_bpm to 0.0–1.0
4. VECTORIZE — Build user vector:  [target_energy, target_valence,
               target_danceability, target_acousticness, target_tempo]
             — Build song vector:  [energy, valence,
               danceability, acousticness, normalized_tempo]
5. SCORE    — For each remaining song, compute weighted proximity:
               score = sum(weight_i * (1 - |user_i - song_i|)) + genre_bonus
6. RANK     — Greedy re-rank with diversity:
               a. Pick highest-scoring candidate
               b. Penalize next candidate if same genre as previous pick
               c. Skip candidate if artist already at max_per_artist cap
               d. Repeat until top-k filled
7. RETURN   — Top-k songs with scores and explanations
```

---

## Implementation Checklist

- [ ] Extend `UserProfile` with target_valence, target_danceability, target_tempo, target_acousticness
- [ ] Add feature_weights dict to `UserProfile`
- [ ] Add disliked_genres, disliked_moods, energy_floor, energy_ceiling to `UserProfile`
- [ ] Add liked_song_ids and disliked_song_ids to `UserProfile`
- [ ] Write a tempo normalization utility
- [ ] Add max_per_artist and same_genre_penalty to `Recommender.__init__()`
- [ ] Implement the scoring formula in `Recommender.recommend()`
- [ ] Implement greedy diversity re-ranking in `Recommender.recommend()`
- [ ] Implement explanation logic in `Recommender.explain_recommendation()`
- [ ] Implement `load_songs()` to read from CSV
- [ ] Implement `recommend_songs()` functional interface
- [ ] Update tests to cover new scoring behavior
