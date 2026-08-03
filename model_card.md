# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0.

## 2. Goal / Task

This recommender suggests songs that seem to match a user's taste. It tries to predict which songs a user will like based on genre, mood, and audio features. This is for classroom exploration, not real-world music streaming.

## 3. Data Used

The model uses 18 songs from `data/songs.csv`. Each song has genre, mood, energy, tempo, valence, danceability, acousticness, popularity, release year, instrumentalness, lyrical intensity, and freshness. The dataset is still small, but it covers more styles than before.

## 4. Algorithm Summary

The system gives points for a genre match, a mood match, and energy closeness. It also adds small points for acousticness, tempo, valence, danceability, popularity, release year, instrumentalness, lyrical intensity, and freshness. Higher scores mean a better match, and the top scores become the recommendations. I also added three ranking modes so the list can be sorted in a few different ways.

## 5. Observed Behavior / Biases

The system can over-prioritize energy and keep similar songs near the top. It also uses exact genre and mood labels, so mixed or fuzzy tastes are harder to capture. Because the catalog is still small, the same songs can appear again and again, which reduces variety. I added an artist penalty to help with that.

I added a small artist penalty so the same artist is less likely to fill the top of the list. This helps reduce filter bubbles and makes the recommendations look more varied.

## 6. Evaluation Process

I tested several user profiles to see how the rankings changed. I used a conflicting high-energy sad profile, a blank neutral profile, a case-mismatch high-energy profile, and an acoustic low-energy lo-fi profile. The results surprised me because `Gym Hero` and `Sunrise City` kept rising for happy pop users, while low-energy lo-fi users shifted toward calmer songs like `Library Rain` and `Midnight Coding`.

The conflicting profile showed that the model still prefers strong genre and energy matches even when the mood does not fit perfectly. The blank profile showed that the system falls back to energy and acousticness when the user gives little information. The case-mismatch profile behaved almost the same as the normal version because the code ignores capitalization. The acoustic lo-fi profile made sense because it pushed the ranking toward quieter, more acoustic songs.

## 7. Intended Use and Non-Intended Use

This model is meant for learning how simple recommenders work. It is good for small experiments and classroom discussion. It should not be used as a real music recommendation system because it is too small and too simple.

It should not be used to judge a person's taste, make high-stakes decisions, or claim that one music style is better than another. It also should not be treated as fair or complete across all listeners.

## 8. Ideas for Improvement

I would balance the weights more carefully so one feature does not dominate everything. I would also add more songs so the system can recommend a wider range of music. I would improve the user profile so it can handle softer preferences instead of only exact matches.

I also added an artist diversity penalty, which is a simple fairness step. It helps avoid showing the same artist over and over in the top results.

I would also tune the new ranking modes so users can switch between balanced, genre-first, and energy-first views more intentionally.

## 9. Personal Reflection

My biggest learning moment was seeing how much the score changed when I adjusted only one weight. Small changes in the rules can make a song jump to the top. AI tools helped me write and organize the reflection, but I still had to double-check the ranking logic and the terminal output because a suggestion can look right even when the math is slightly off.

What surprised me most was that a simple algorithm can still feel like a real recommender. It does not understand music the way a person does, but it can still produce patterns that seem reasonable. If I extended this project, I would add more songs, try softer preference ranges, and test whether diversity improves when the weights are less extreme.

## 10. Reflection on Building the RAG Feature

Adding the RAG explanation layer meant collaborating closely with AI on both the design and the implementation. I used AI to help scope a realistic feature for a short timeline, design the retrieval/generation split, and write the initial versions of `knowledge_base.py`, `retriever.py`, and `rag_explainer.py`.

**One helpful AI suggestion:** Building in a deterministic fallback from the start, rather than treating error handling as an afterthought, was suggested early on. This turned out to matter a lot in practice — I built and tested this entire feature without ever purchasing API credits, because the fallback let the app run correctly the whole time. It also meant that when I eventually connected a real API key, nothing about the rest of the system had to change.

**One flawed AI suggestion:** The first version of `retriever.py` used a type hint of `List[str] or str`, which isn't valid Python typing syntax — it happens to run without erroring, but it's misleading and would look like a mistake to anyone reviewing the code. I caught this by reading through the file carefully rather than just running it, and fixed it to use `Union[List[str], str]` instead. It was a good reminder that AI-generated code can look correct and run without crashing while still containing something that isn't actually right.

**Limitations of this system:** The RAG layer's local knowledge base is small and only covers a handful of genres and moods, so it falls back to a generic note for anything outside that list. I added automated tests for the retrieval layer (`tests/test_retriever.py`), but the generation layer (`rag_explainer.py`) still relies on manual verification and log review, since it depends on a live API call that would need mocking to test automatically — a gap I'd want to close if I extended this project further.

