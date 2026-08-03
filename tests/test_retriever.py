"""Tests for the retrieval layer (src/retriever.py)."""

import pytest

try:
    from src.retriever import retrieve_context
except ImportError:
    from retriever import retrieve_context


SAMPLE_SONG = {
    "title": "Sunrise City",
    "artist": "Neon Echo",
    "genre": "pop",
    "mood": "happy",
}


def test_retrieve_context_returns_all_expected_keys():
    """The context dict should contain every field the generator depends on."""
    context = retrieve_context(SAMPLE_SONG, score=7.11, reasons=["genre match (+1.0)", "mood match (+1.0)"])

    expected_keys = {
        "title", "artist", "genre", "mood",
        "genre_note", "mood_note", "score", "score_reasons",
    }
    assert expected_keys.issubset(context.keys())


def test_retrieve_context_preserves_song_fields():
    """The song's own title/artist/genre/mood should pass through unchanged."""
    context = retrieve_context(SAMPLE_SONG, score=5.0, reasons="genre match (+1.0)")

    assert context["title"] == "Sunrise City"
    assert context["artist"] == "Neon Echo"
    assert context["genre"] == "pop"
    assert context["mood"] == "happy"


def test_retrieve_context_accepts_list_of_reasons():
    """A list of reason strings should be joined into a single string."""
    context = retrieve_context(SAMPLE_SONG, score=5.0, reasons=["genre match (+1.0)", "mood match (+1.0)"])

    assert "genre match (+1.0)" in context["score_reasons"]
    assert "mood match (+1.0)" in context["score_reasons"]


def test_retrieve_context_accepts_string_reasons():
    """A single string of reasons should pass through as-is."""
    context = retrieve_context(SAMPLE_SONG, score=5.0, reasons="genre match (+1.0), mood match (+1.0)")

    assert context["score_reasons"] == "genre match (+1.0), mood match (+1.0)"


def test_retrieve_context_handles_missing_song_fields():
    """A song dict missing fields should still produce a valid context, not crash."""
    incomplete_song = {"title": "Untitled Track"}

    context = retrieve_context(incomplete_song, score=1.0, reasons="no strong match")

    assert context["title"] == "Untitled Track"
    assert context["artist"] == "Unknown"
    assert context["genre"] == ""
    assert context["mood"] == ""


def test_retrieve_context_unknown_genre_falls_back_gracefully():
    """A genre not in the knowledge base should return a generic fallback note, not crash."""
    song = {**SAMPLE_SONG, "genre": "polka"}

    context = retrieve_context(song, score=3.0, reasons="genre match (+1.0)")

    assert "polka" in context["genre_note"]


def test_retrieve_context_score_is_preserved():
    """The numeric score passed in should appear unchanged in the context."""
    context = retrieve_context(SAMPLE_SONG, score=6.42, reasons="test")

    assert context["score"] == 6.42