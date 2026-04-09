# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the app (from repo root)
python -m src.main

# Run tests
pytest

# Install dependencies
pip install -r requirements.txt
```

## Architecture

There are **two parallel implementations** in this codebase that serve different purposes:

### OOP Interface (`src/recommender.py` + `tests/`)
- `Song` — dataclass with music attributes (genre, mood, energy, tempo_bpm, valence, danceability, acousticness)
- `UserProfile` — dataclass with user taste preferences (favorite_genre, favorite_mood, target_energy, likes_acoustic)
- `Recommender` — class initialized with a list of `Song` objects; exposes `recommend(user, k)` and `explain_recommendation(user, song)`
- Tests import via `from src.recommender import Song, UserProfile, Recommender`

### Functional Interface (`src/main.py` uses this)
- `load_songs(csv_path)` — loads `data/songs.csv`, returns a list of dicts
- `recommend_songs(user_prefs, songs, k)` — takes a dict of user prefs, returns `List[Tuple[song_dict, score, explanation]]`
- `src/main.py` imports directly: `from recommender import load_songs, recommend_songs` (no `src.` prefix — run via `python -m src.main`)

### Key Implementation TODOs
All logic stubs are in `src/recommender.py`:
- `Recommender.recommend()` — currently returns first k songs unscored
- `Recommender.explain_recommendation()` — returns placeholder string
- `load_songs()` — returns empty list
- `recommend_songs()` — returns empty list

### Data
`data/songs.csv` — the song catalog used by the functional interface. Songs have the same fields as the `Song` dataclass.
