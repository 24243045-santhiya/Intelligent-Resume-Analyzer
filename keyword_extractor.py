"""
keyword_extractor.py

Extracts important skills and keywords from a Resume and Job Description.

No external libraries are used.
"""

import re


# Common technical and professional skills
KNOWN_SKILLS = {
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "html",
    "css",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "data visualization",
    "natural language processing",
    "computer vision",
    "pandas",
    "numpy",
    "matplotlib",
    "tensorflow",
    "pytorch",
    "scikit learn",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "google cloud",
    "cloud computing",
    "linux",
    "windows",
    "flask",
    "django",
    "fastapi",
    "react",
    "reactjs",
    "node",
    "nodejs",
    "spring",
    "spring boot",
    "rest api",
    "api",
    "mongodb",
    "firebase",
    "tableau",
    "power bi",
    "excel",
    "hadoop",
    "spark",
    "hdfs",
    "mapreduce",
    "communication",
    "leadership",
    "teamwork",
    "problem solving",
    "time management",
    "critical thinking",
    "adaptability",
    "creativity",
    "project management",
}


def clean_text(text):
    """
    Convert text into a simple normalized format.
    """

    text = text.lower()

    # Keep letters, numbers, #, + and spaces
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)

    # Replace multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_words(text):
    """
    Convert text into individual words.
    """

    cleaned = clean_text(text)

    if not cleaned:
        return []

    return cleaned.split()


def extract_all_words(text):
    """
    Return unique words from text.
    """

    words = get_words(text)

    return set(words)


def extract_known_skills(text):
    """
    Identify known skills present in the given text.
    """

    cleaned = clean_text(text)

    found_skills = set()

    for skill in KNOWN_SKILLS:

        skill_cleaned = clean_text(skill)

        # Word/phrase matching
        pattern = r"(?<![a-z0-9])" + re.escape(skill_cleaned) + r"(?![a-z0-9])"

        if re.search(pattern, cleaned):
            found_skills.add(skill)

    return found_skills


def extract_keyword_frequency(text):
    """
    Count how frequently each word appears.
    """

    words = get_words(text)

    frequency = {}

    for word in words:

        if len(word) <= 2:
            continue

        frequency[word] = frequency.get(word, 0) + 1

    return frequency


def extract_relevant_keywords(text):
    """
    Extract known skills and useful words.
    """

    skills = extract_known_skills(text)

    frequency = extract_keyword_frequency(text)

    # Remove common non-useful words
    stop_words = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "this",
        "that",
        "are",
        "you",
        "your",
        "our",
        "will",
        "have",
        "has",
        "using",
        "use",
        "work",
        "working",
        "job",
        "role",
        "candidate",
        "required",
        "requirements",
        "experience",
        "years",
    }

    additional_words = set()

    for word in frequency:

        if word not in stop_words:
            additional_words.add(word)

    return skills, additional_words


def compare_keywords(resume_text, jd_text):
    """
    Compare resume and JD keywords.

    Returns:
        matched skills
        missing skills
        extra resume skills
    """

    resume_skills = extract_known_skills(resume_text)
    jd_skills = extract_known_skills(jd_text)

    matched = resume_skills.intersection(jd_skills)

    missing = jd_skills.difference(resume_skills)

    extra = resume_skills.difference(jd_skills)

    return matched, missing, extra


if __name__ == "__main__":

    print("=" * 60)
    print("KEYWORD EXTRACTOR TEST")
    print("=" * 60)

    sample_resume = """
    Python Java SQL Machine Learning Git
    Communication Leadership
    """

    sample_jd = """
    Python SQL Machine Learning Docker Git
    Communication Teamwork
    """

    matched, missing, extra = compare_keywords(
        sample_resume,
        sample_jd
    )

    print("\nMatched Skills:")
    for skill in sorted(matched):
        print("✓", skill)

    print("\nMissing Skills:")
    for skill in sorted(missing):
        print("✗", skill)

    print("\nAdditional Resume Skills:")
    for skill in sorted(extra):
        print("+", skill)