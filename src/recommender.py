import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_song(self, user: UserProfile, song: Song) -> float:
        """Score a song against a user profile on genre, mood, energy, and acousticness."""
        score = 0.0
        if song.genre == user.favorite_genre:
            score += 2.0
        if song.mood == user.favorite_mood:
            score += 1.0
        score += 1.0 * (1.0 - abs(song.energy - user.target_energy))
        if user.likes_acoustic and song.acousticness > 0.6:
            score += 0.5
        elif not user.likes_acoustic and song.acousticness < 0.4:
            score += 0.5
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs sorted by descending match score."""
        scored = [(self._score_song(user, song), song) for song in self.songs]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Build a human-readable string showing which dimensions matched and how close."""
        parts = []
        genre_match = song.genre == user.favorite_genre
        parts.append(f"Genre: {song.genre} {'✓' if genre_match else '✗'}")

        mood_match = song.mood == user.favorite_mood
        parts.append(f"Mood: {song.mood} {'✓' if mood_match else '✗'}")

        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff < 0.10:
            proximity = "very close"
        elif energy_diff < 0.25:
            proximity = "close"
        else:
            proximity = "far"
        parts.append(f"Energy: {song.energy:.2f} vs {user.target_energy:.2f} ({proximity})")

        if user.likes_acoustic:
            acoustic_fit = song.acousticness > 0.6
        else:
            acoustic_fit = song.acousticness < 0.4
        parts.append(f"Acoustic: {song.acousticness:.2f} {'✓' if acoustic_fit else '✗'}")

        return " | ".join(parts)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs

def _score_song_dict(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Score a song dict against user prefs and return (score, explanation)."""
    score = 0.0
    parts = []

    genre_match = song["genre"] == user_prefs.get("genre", "")
    if genre_match:
        score += 2.0
    parts.append(f"Genre: {song['genre']} {'✓' if genre_match else '✗'}")

    mood_match = song["mood"] == user_prefs.get("mood", "")
    if mood_match:
        score += 1.0
    parts.append(f"Mood: {song['mood']} {'✓' if mood_match else '✗'}")

    target_energy = user_prefs.get("energy", 0.5)
    energy_diff = abs(song["energy"] - target_energy)
    score += 1.0 * (1.0 - energy_diff)
    if energy_diff < 0.10:
        proximity = "very close"
    elif energy_diff < 0.25:
        proximity = "close"
    else:
        proximity = "far"
    parts.append(f"Energy: {song['energy']:.2f} vs {target_energy:.2f} ({proximity})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        if likes_acoustic and song["acousticness"] > 0.6:
            score += 0.5
            acoustic_fit = True
        elif not likes_acoustic and song["acousticness"] < 0.4:
            score += 0.5
            acoustic_fit = True
        else:
            acoustic_fit = False
        parts.append(f"Acoustic: {song['acousticness']:.2f} {'✓' if acoustic_fit else '✗'}")

    return score, " | ".join(parts)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, explanation = _score_song_dict(user_prefs, song)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
