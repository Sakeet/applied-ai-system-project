"""
Evaluation harness: runs the recommender system against a set of predefined
user profiles and reports pass/fail results for each check.

Run with: python -m src.evaluate
"""

import os

try:
    from .recommender import load_songs, recommend_songs
    from .retriever import retrieve_context
    from .rag_explainer import generate_explanation
except ImportError:
    from recommender import load_songs, recommend_songs
    from retriever import retrieve_context
    from rag_explainer import generate_explanation


TEST_PROFILES = {
    "High Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lo-Fi": {"genre": "lofi", "mood": "chill", "energy": 0.4},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
    "Blank Profile": {"genre": "", "mood": "", "energy": 0.5},
    "Case Mismatch": {"genre": "POP", "mood": "HAPPY", "energy": 0.8},
}


def check_recommendations_returned(recommendations, k):
    """Recommender should return up to k songs, and at least 1 if songs exist."""
    return len(recommendations) > 0 and len(recommendations) <= k


def check_scores_descending(recommendations):
    """Recommendations should be sorted from highest score to lowest."""
    scores = [score for (_song, score, _explanation) in recommendations]
    return scores == sorted(scores, reverse=True)


def check_explanations_generate_without_crashing(recommendations):
    """Every recommendation should produce a retrieval context and an explanation
    without raising an exception, regardless of API availability."""
    try:
        for song, score, explanation in recommendations:
            context = retrieve_context(song, score, explanation)
            text = generate_explanation(context)
            if not text or not isinstance(text, str):
                return False
        return True
    except Exception:
        return False


def run_evaluation():
    os.makedirs("logs", exist_ok=True)
    songs = load_songs("data/songs.csv")

    results = []

    for profile_name, user_prefs in TEST_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5, ranking_mode="balanced")

        checks = {
            "Returns recommendations": check_recommendations_returned(recommendations, k=5),
            "Scores are descending": check_scores_descending(recommendations),
            "Explanations generate without crashing": check_explanations_generate_without_crashing(recommendations),
        }

        results.append((profile_name, checks))

    return results


def print_summary(results):
    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    total_checks = 0
    total_passed = 0

    for profile_name, checks in results:
        print(f"\nProfile: {profile_name}")
        for check_name, passed in checks.items():
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] {check_name}")
            total_checks += 1
            if passed:
                total_passed += 1

    print("\n" + "-" * 70)
    pass_rate = (total_passed / total_checks * 100) if total_checks else 0
    print(f"Overall: {total_passed}/{total_checks} checks passed ({pass_rate:.0f}%)")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    results = run_evaluation()
    print_summary(results)