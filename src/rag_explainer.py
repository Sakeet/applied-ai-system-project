"""Generation layer: turns retrieved context into a natural-language explanation."""

import os
import logging
from typing import Dict, Optional

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

try:
    import anthropic
    _CLIENT_AVAILABLE = True
except ImportError:
    _CLIENT_AVAILABLE = False


def generate_explanation(context: Dict, client: Optional["anthropic.Anthropic"] = None) -> str:
    """
    Generates a natural-language explanation of a recommendation,
    grounded strictly in the retrieved context (no free invention).
    Falls back to a deterministic explanation if the API is unavailable.
    """
    fallback = (
        f"'{context['title']}' by {context['artist']} scored {context['score']:.2f}. "
        f"Reasons: {context['score_reasons']}."
    )

    if not _CLIENT_AVAILABLE:
        logger.warning("anthropic package not installed; using fallback explanation.")
        return fallback

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.warning("ANTHROPIC_API_KEY not set; using fallback explanation.")
        return fallback

    try:
        if client is None:
            client = anthropic.Anthropic(api_key=api_key)

        prompt = (
            "You are explaining a music recommendation to a user. "
            "Use ONLY the facts provided below — do not invent details about the song.\n\n"
            f"Song: {context['title']} by {context['artist']}\n"
            f"Genre: {context['genre']} — {context['genre_note']}\n"
            f"Mood: {context['mood']} — {context['mood_note']}\n"
            f"Score: {context['score']:.2f}\n"
            f"Score reasons: {context['score_reasons']}\n\n"
            "Write a warm, 1-2 sentence explanation of why this song was recommended, "
            "grounded in the facts above."
        )

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
        )

        text = "".join(
            block.text for block in response.content if block.type == "text"
        ).strip()

        if not text:
            raise ValueError("Empty response from API")

        logger.info(f"Generated explanation for '{context['title']}'")
        return text

    except Exception as e:
        logger.error(f"RAG explanation failed for '{context['title']}': {e}")
        return fallback