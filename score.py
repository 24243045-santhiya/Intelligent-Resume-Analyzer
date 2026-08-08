"""
score.py

Calculates resume matching score and rating.
"""


def calculate_score(matched_count, total_required):
    """
    Calculate percentage match.

    Formula:

        Score = matched / total * 100
    """

    if total_required == 0:
        return 0.0

    score = (matched_count / total_required) * 100

    return round(score, 2)


def get_rating(score):
    """
    Convert score into a rating.
    """

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Very Good"

    elif score >= 60:
        return "Good"

    elif score >= 40:
        return "Average"

    else:
        return "Needs Improvement"


def get_recommendation(score):
    """
    Generate recommendation based on score.
    """

    if score >= 90:
        return (
            "Your resume strongly matches the Job Description. "
            "You are highly suitable for this position."
        )

    elif score >= 75:
        return (
            "Your resume matches most of the required skills. "
            "You are a good candidate for this position."
        )

    elif score >= 60:
        return (
            "Your resume has a reasonable match. "
            "Consider improving the missing skills."
        )

    elif score >= 40:
        return (
            "Your resume partially matches the Job Description. "
            "Add the missing skills and relevant projects."
        )

    else:
        return (
            "Your resume has a low match with the Job Description. "
            "Consider improving your technical skills and resume content."
        )


def generate_suggestions(missing_skills):
    """
    Generate suggestions for missing skills.
    """

    suggestions = []

    for skill in sorted(missing_skills):

        suggestion = (
            f"Consider learning or highlighting your experience in {skill}."
        )

        suggestions.append(suggestion)

    if not suggestions:
        suggestions.append(
            "No major missing skills were detected."
        )

    return suggestions


def create_score_summary(matched, missing):
    """
    Create complete score summary.
    """

    matched_count = len(matched)
    missing_count = len(missing)

    total = matched_count + missing_count

    score = calculate_score(
        matched_count,
        total
    )

    rating = get_rating(score)

    recommendation = get_recommendation(score)

    suggestions = generate_suggestions(missing)

    return {
        "matched_count": matched_count,
        "missing_count": missing_count,
        "total_required": total,
        "score": score,
        "rating": rating,
        "recommendation": recommendation,
        "suggestions": suggestions,
    }


if __name__ == "__main__":

    matched = {
        "python",
        "sql",
        "git",
        "communication"
    }

    missing = {
        "docker",
        "machine learning"
    }

    result = create_score_summary(
        matched,
        missing
    )

    print("=" * 50)
    print("SCORE TEST")
    print("=" * 50)

    print("Matched :", result["matched_count"])
    print("Missing :", result["missing_count"])
    print("Score   :", result["score"], "%")
    print("Rating  :", result["rating"])