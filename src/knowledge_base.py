"""Small local knowledge base used for retrieval in the RAG explanation feature."""

GENRE_NOTES = {
    "pop": "Pop tracks tend to prioritize catchy hooks, polished production, and broad appeal.",
    "rock": "Rock often centers on guitar-driven energy, strong rhythm sections, and raw intensity.",
    "lofi": "Lo-fi favors relaxed tempos, warm imperfect textures, and a laid-back, background-friendly feel.",
    "jazz": "Jazz emphasizes improvisation, complex harmony, and expressive, loose timing.",
    "electronic": "Electronic music leans on synthesized textures, repetition, and built, layered energy.",
    "hiphop": "Hip-hop centers rhythm and vocal delivery, often with strong bass and beat-driven structure.",
    "classical": "Classical music draws on acoustic instrumentation, structured composition, and dynamic range.",
}

MOOD_NOTES = {
    "happy": "Happy-tagged tracks usually pair upbeat tempo with bright, major-leaning tonality.",
    "chill": "Chill tracks favor lower intensity, smoother transitions, and a relaxed pace.",
    "intense": "Intense tracks push higher energy, driving rhythms, and a heavier emotional weight.",
    "sad": "Sad-tagged tracks often slow down tempo and lean into minor-leaning, reflective tones.",
    "calm": "Calm tracks minimize sharp dynamic shifts and favor steady, soothing pacing.",
}

def get_genre_note(genre: str) -> str:
    return GENRE_NOTES.get(str(genre).lower(), f"No specific notes available for the '{genre}' genre.")

def get_mood_note(mood: str) -> str:
    return MOOD_NOTES.get(str(mood).lower(), f"No specific notes available for the '{mood}' mood.")

ARTIST_NOTES = {
    "neon echo": "Known for blending upbeat pop hooks with electronic production.",
    "indigo parade": "An indie act known for atmospheric, mood-driven tracks.",
    "max pulse": "A high-energy act often associated with workout and driving playlists.",
    "voltline": "An electronic-leaning artist known for driving, textured production.",
}

def get_artist_note(artist: str) -> str:
    return ARTIST_NOTES.get(str(artist).lower(), f"No specific notes available for the artist '{artist}'.")