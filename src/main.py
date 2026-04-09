"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def run_profile(name: str, user_prefs: dict, songs: list) -> None:
    """Run the recommender for one profile and print results."""
    recommendations = recommend_songs(user_prefs, songs, k=5)
    print(f"\n{'=' * 60}")
    print(f"  Profile: {name}")
    print(f"  genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
          f"energy={user_prefs['energy']}, acoustic={user_prefs['likes_acoustic']}")
    print(f"{'=' * 60}")
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n  {i}. {song['title']} by {song['artist']}")
        print(f"     Score: {score:.2f} / 4.50")
        print(f"     {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = [
        (
            "High-Energy Pop",
            {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
        ),
        (
            "Chill Lofi",
            {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
        ),
        (
            "Intense Rock",
            {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
        ),
        (
            "Conflicting: High Energy + Chill",
            {"genre": "lofi", "mood": "chill", "energy": 0.95, "likes_acoustic": True},
        ),
        (
            "Nonexistent Genre & Mood",
            {"genre": "k-pop", "mood": "euphoric", "energy": 0.5, "likes_acoustic": False},
        ),
        (
            "Acoustic + High Energy",
            {"genre": "folk", "mood": "nostalgic", "energy": 0.95, "likes_acoustic": True},
        ),
    ]

    for name, prefs in profiles:
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
