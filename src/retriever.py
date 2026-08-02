"""Retrieval layer: gathers structured context about a song before generation."""

from typing import Dict, List, Union
from .knowledge_base import get_genre_note, get_mood_note


def retrieve_context(song: Dict, score: float, reasons: Union[List[str], str]) -> Dict:
    """
    Pulls together everything the explanation generator is allowed to use:
    - the song's own attributes
    - genre/mood background notes from the knowledge base
    - the score breakdown already computed by the recommender

    Nothing here is invented — it's all retrieved from existing data.
    """
    if isinstance(reasons, list):
        reasons_text = "; ".join(reasons)
    else:
        reasons_text = reasons

    return {
        "title": song.get("title", "Unknown"),
        "artist": song.get("artist", "Unknown"),
        "genre": song.get("genre", ""),
        "mood": song.get("mood", ""),
        "genre_note": get_genre_note(song.get("genre", "")),
        "mood_note": get_mood_note(song.get("mood", "")),
        "score": score,
        "score_reasons": reasons_text,
    }