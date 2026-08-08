"""
main.py

Entry point for Intelligent Resume Analyzer.
"""

from analyzer import ResumeAnalyzer


def main():

    print("\n")

    print("=" * 70)

    print(
        "       WELCOME TO INTELLIGENT RESUME ANALYZER"
    )

    print("=" * 70)

    print()

    print(
        "This application analyzes multiple resumes "
        "against a Job Description."
    )

    print()

    print(
        "It identifies:"
    )

    print(
        "  1. Matching skills"
    )

    print(
        "  2. Missing skills"
    )

    print(
        "  3. Resume score"
    )

    print(
        "  4. Candidate rating"
    )

    print(
        "  5. Candidate ranking"
    )

    print()

    analyzer = ResumeAnalyzer()

    analyzer.run()


if __name__ == "__main__":

    main()