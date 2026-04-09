 # 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language. 
  - Our recommender system compares a user's taste preference (favorite genre, mood, energy level, and acoustic preference) against each song's audio features (genre, mood, energy, tempo, valence, etc) to calculate a similarity score. Songs are ranked by score and the top k are returned. 

Some prompts to answer:

- What features does each `Song` use in your system
  - In our recommender system, we will use `energy`, `valence`, `dancability`, `acousticness`, `temp_dpm`, `genre`, and `artist`. 
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
  - The `UserProfile` stores four preference fields: `favorite_genre` (a string like "lofi" or "pop"), `favorite_mood` (a string like "chill" or "happy"), `target_energy` (a float between 0.0 and 1.0 representing how energetic the user wants their music), and `likes_acoustic` (a boolean for whether the user prefers acoustic-sounding tracks). Together these four dimensions give the system enough signal to distinguish between very different listener types, such as someone who wants intense rock versus someone who wants calm lofi.
- How does your `Recommender` compute a score for each song
  - For each song, the system checks four dimensions and adds up points: +2.0 for a genre match, +1.0 for a mood match, up to +1.0 for energy similarity (calculated as `1.0 - abs(song.energy - target_energy)`, so closer values earn more), and +0.5 if the song's acousticness fits the user's preference (above 0.6 for acoustic lovers, below 0.4 otherwise). The maximum possible score is 4.5. Genre carries the most weight because it is the strongest signal of listener intent.
- How do you choose which songs to recommend
  - Every song in the catalog gets scored against the user's profile, then the full list is sorted from highest to lowest score. The system returns the top K songs (default 5) along with their scores and a human-readable explanation string showing which dimensions matched and how close the energy was. This means the recommendations are purely rank-ordered by fit, with no randomness or diversity re-ranking applied.
- Potential biases
  - This system might over-prioritize genre, since a genre match alone (2.0 pts) can outweigh mood, energy, and acoustic fit combined (2.5 pts max). A song that matches genre but clashes on every other dimension can still rank above a song that perfectly matches mood, energy, and acousticness but belongs to a neighboring genre. The system also treats similar genres as completely different: "indie pop" and "pop" score as a total mismatch, even though most pop listeners would enjoy both. Finally, because valence, danceability, and tempo are ignored entirely, the system cannot distinguish "happy pop" from "melancholic pop" or a slow ballad from an uptempo dance track within the same genre.

```
  INPUT                    PROCESS                        OUTPUT
┌───────────┐   ┌──────────────────────────────┐   ┌─────────────┐
│ songs.csv │──▶│  load_songs()                 │   │             │
└───────────┘   │  List of song dicts           │   │  Top-K      │
                └──────────────┬───────────────┘   │  Results    │
┌───────────┐                  │                   │             │
│ User      │   ┌──────────────▼───────────────┐   │ (song,      │
│ Prefs     │──▶│  For each song:               │──▶│  score,     │
│           │   │                              │   │  explain)   │
│ genre     │   │  Genre match?   +0 or +2.0   │   │             │
│ mood      │   │  Mood match?    +0 or +1.0   │   └─────────────┘
│ energy    │   │  Energy sim.    +0.0 to +1.0 │
│ likes_    │   │  Acoustic fit?  +0 or +0.5   │
│  acoustic │   │  ──────────────────────────  │
└───────────┘   │  total score = sum above     │
                │  explanation = describe why  │
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

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

