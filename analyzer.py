"""
analyzer.py

Main analysis engine for Intelligent Resume Analyzer.

Supports:
1. Single resume analysis
2. Multiple resume analysis
3. Candidate ranking
4. Report generation

Only Python built-in modules are used.
"""

import os

from resume_reader import (
    read_resume,
    read_job_description,
    validate_file
)

from keyword_extractor import (
    compare_keywords
)

from score import (
    create_score_summary
)


class ResumeAnalyzer:

    def __init__(self):

        self.resume_text = ""

        self.jd_text = ""

        self.resume_path = ""

        self.jd_path = ""

        self.matched_skills = set()

        self.missing_skills = set()

        self.extra_skills = set()

        self.result = {}

        self.multiple_results = []

    # ---------------------------------------------------------
    # LOAD SINGLE RESUME
    # ---------------------------------------------------------

    def load_files(self, resume_path, jd_path):

        if not validate_file(resume_path):

            raise FileNotFoundError(
                f"Resume file not found or empty: {resume_path}"
            )

        if not validate_file(jd_path):

            raise FileNotFoundError(
                f"Job Description file not found or empty: {jd_path}"
            )

        self.resume_path = resume_path

        self.jd_path = jd_path

        self.resume_text = read_resume(resume_path)

        self.jd_text = read_job_description(jd_path)

        return True

    # ---------------------------------------------------------
    # ANALYZE SINGLE RESUME
    # ---------------------------------------------------------

    def analyze(self):

        if not self.resume_text:

            raise ValueError(
                "Resume has not been loaded."
            )

        if not self.jd_text:

            raise ValueError(
                "Job Description has not been loaded."
            )

        (
            self.matched_skills,
            self.missing_skills,
            self.extra_skills
        ) = compare_keywords(
            self.resume_text,
            self.jd_text
        )

        self.result = create_score_summary(
            self.matched_skills,
            self.missing_skills
        )

        return self.result

    # ---------------------------------------------------------
    # GENERATE SINGLE REPORT
    # ---------------------------------------------------------

    def generate_report(self):

        if not self.result:

            self.analyze()

        lines = []

        lines.append("=" * 70)

        lines.append(
            "              INTELLIGENT RESUME ANALYZER"
        )

        lines.append("=" * 70)

        lines.append("")

        lines.append(
            f"Resume File : {self.resume_path}"
        )

        lines.append(
            f"Job Description : {self.jd_path}"
        )

        lines.append("")

        lines.append("-" * 70)

        lines.append(
            "                    ANALYSIS REPORT"
        )

        lines.append("-" * 70)

        lines.append("")

        lines.append(
            f"Total Required Skills : "
            f"{self.result['total_required']}"
        )

        lines.append(
            f"Matched Skills        : "
            f"{self.result['matched_count']}"
        )

        lines.append(
            f"Missing Skills        : "
            f"{self.result['missing_count']}"
        )

        lines.append("")

        lines.append("-" * 70)

        lines.append("MATCHED SKILLS")

        lines.append("-" * 70)

        if self.matched_skills:

            for skill in sorted(self.matched_skills):

                lines.append(
                    f"  [MATCH] {skill}"
                )

        else:

            lines.append(
                "  No matching skills found."
            )

        lines.append("")

        lines.append("-" * 70)

        lines.append("MISSING SKILLS")

        lines.append("-" * 70)

        if self.missing_skills:

            for skill in sorted(self.missing_skills):

                lines.append(
                    f"  [MISSING] {skill}"
                )

        else:

            lines.append(
                "  No major missing skills."
            )

        lines.append("")

        lines.append("-" * 70)

        lines.append("ADDITIONAL RESUME SKILLS")

        lines.append("-" * 70)

        if self.extra_skills:

            for skill in sorted(self.extra_skills):

                lines.append(
                    f"  [EXTRA] {skill}"
                )

        else:

            lines.append(
                "  No additional skills detected."
            )

        lines.append("")

        lines.append("-" * 70)

        lines.append("RESUME MATCH SCORE")

        lines.append("-" * 70)

        lines.append("")

        lines.append(
            f"  Score  : {self.result['score']}%"
        )

        lines.append(
            f"  Rating : {self.result['rating']}"
        )

        lines.append("")

        lines.append("-" * 70)

        lines.append("SUGGESTIONS")

        lines.append("-" * 70)

        for suggestion in self.result["suggestions"]:

            lines.append(
                f"  • {suggestion}"
            )

        lines.append("")

        lines.append("-" * 70)

        lines.append("FINAL RECOMMENDATION")

        lines.append("-" * 70)

        lines.append("")

        lines.append(
            f"  {self.result['recommendation']}"
        )

        lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)

    # ---------------------------------------------------------
    # SAVE SINGLE REPORT
    # ---------------------------------------------------------

    def save_report(self, output_path):

        report = self.generate_report()

        output_directory = os.path.dirname(output_path)

        if output_directory:

            os.makedirs(
                output_directory,
                exist_ok=True
            )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(report)

        return output_path

    # ---------------------------------------------------------
    # ANALYZE MULTIPLE RESUMES
    # ---------------------------------------------------------

    def analyze_multiple_resumes(
        self,
        resume_paths,
        jd_path
    ):

        if not resume_paths:

            raise ValueError(
                "No resume files were selected."
            )

        if not validate_file(jd_path):

            raise FileNotFoundError(
                "Job Description file not found or empty."
            )

        jd_text = read_job_description(
            jd_path
        )

        self.multiple_results = []

        for resume_path in resume_paths:

            try:

                if not validate_file(resume_path):

                    continue

                resume_text = read_resume(
                    resume_path
                )

                (
                    matched,
                    missing,
                    extra
                ) = compare_keywords(
                    resume_text,
                    jd_text
                )

                score_result = create_score_summary(
                    matched,
                    missing
                )

                candidate_name = self.extract_candidate_name(
                    resume_text,
                    resume_path
                )

                result = {

                    "candidate": candidate_name,

                    "file": os.path.basename(
                        resume_path
                    ),

                    "path": resume_path,

                    "score": score_result["score"],

                    "rating": score_result["rating"],

                    "matched": matched,

                    "missing": missing,

                    "extra": extra,

                    "recommendation":
                        score_result[
                            "recommendation"
                        ],

                    "suggestions":
                        score_result[
                            "suggestions"
                        ]
                }

                self.multiple_results.append(
                    result
                )

            except Exception as error:

                print(
                    f"Error analyzing "
                    f"{resume_path}: {error}"
                )

        # Highest score first
        self.multiple_results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        # Add ranking
        for index, result in enumerate(
            self.multiple_results,
            start=1
        ):

            result["rank"] = index

        return self.multiple_results

    # ---------------------------------------------------------
    # EXTRACT CANDIDATE NAME
    # ---------------------------------------------------------

    def extract_candidate_name(
        self,
        resume_text,
        resume_path
    ):

        lines = resume_text.splitlines()

        for line in lines:

            cleaned = line.strip()

            if not cleaned:

                continue

            lower = cleaned.lower()

            if lower.startswith("name:"):

                name = cleaned.split(
                    ":",
                    1
                )[1].strip()

                if name:

                    return name

        # If Name: is not present,
        # use the first non-empty line
        # if it looks like a candidate name.

        for line in lines:

            cleaned = line.strip()

            if cleaned:

                if (
                    "resume" not in
                    cleaned.lower()
                ):

                    return cleaned

        return os.path.splitext(
            os.path.basename(resume_path)
        )[0]

    # ---------------------------------------------------------
    # GENERATE MULTIPLE RESUME REPORT
    # ---------------------------------------------------------

    def generate_multiple_report(
        self,
        results,
        jd_path
    ):

        lines = []

        lines.append("=" * 80)

        lines.append(
            "             INTELLIGENT RESUME ANALYZER"
        )

        lines.append("=" * 80)

        lines.append("")

        lines.append(
            f"Job Description: "
            f"{os.path.basename(jd_path)}"
        )

        lines.append(
            f"Total Resumes Analyzed: "
            f"{len(results)}"
        )

        lines.append("")

        lines.append("=" * 80)

        lines.append(
            "                     CANDIDATE RANKING"
        )

        lines.append("=" * 80)

        lines.append("")

        header = (
            f"{'Rank':<8}"
            f"{'Candidate':<25}"
            f"{'Score':<12}"
            f"{'Rating':<20}"
        )

        lines.append(header)

        lines.append("-" * 80)

        for result in results:

            candidate = result["candidate"]

            if len(candidate) > 23:

                candidate = candidate[:23]

            row = (
                f"{result['rank']:<8}"
                f"{candidate:<25}"
                f"{str(result['score']) + '%':<12}"
                f"{result['rating']:<20}"
            )

            lines.append(row)

        lines.append("")

        lines.append("=" * 80)

        lines.append(
            "                    DETAILED RESULTS"
        )

        lines.append("=" * 80)

        for result in results:

            lines.append("")

            lines.append("-" * 80)

            lines.append(
                f"RANK #{result['rank']}"
            )

            lines.append(
                f"Candidate : {result['candidate']}"
            )

            lines.append(
                f"Resume    : {result['file']}"
            )

            lines.append(
                f"Score     : {result['score']}%"
            )

            lines.append(
                f"Rating    : {result['rating']}"
            )

            lines.append("")

            lines.append(
                "MATCHED SKILLS:"
            )

            if result["matched"]:

                for skill in sorted(
                    result["matched"]
                ):

                    lines.append(
                        f"  [MATCH] {skill}"
                    )

            else:

                lines.append(
                    "  No matching skills."
                )

            lines.append("")

            lines.append(
                "MISSING SKILLS:"
            )

            if result["missing"]:

                for skill in sorted(
                    result["missing"]
                ):

                    lines.append(
                        f"  [MISSING] {skill}"
                    )

            else:

                lines.append(
                    "  No missing skills."
                )

            lines.append("")

            lines.append(
                "ADDITIONAL SKILLS:"
            )

            if result["extra"]:

                for skill in sorted(
                    result["extra"]
                ):

                    lines.append(
                        f"  [EXTRA] {skill}"
                    )

            else:

                lines.append(
                    "  No additional skills."
                )

            lines.append("")

            lines.append(
                "RECOMMENDATION:"
            )

            lines.append(
                f"  {result['recommendation']}"
            )

        lines.append("")

        lines.append("=" * 80)

        lines.append(
            "                    END OF REPORT"
        )

        lines.append("=" * 80)

        return "\n".join(lines)

    # ---------------------------------------------------------
    # SAVE MULTIPLE REPORT
    # ---------------------------------------------------------

    def save_multiple_report(
        self,
        results,
        jd_path,
        output_path
    ):

        report = self.generate_multiple_report(
            results,
            jd_path
        )

        output_directory = os.path.dirname(
            output_path
        )

        if output_directory:

            os.makedirs(
                output_directory,
                exist_ok=True
            )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(report)

        return output_path

    # ---------------------------------------------------------
    # CONSOLE MULTIPLE RESUME TEST
    # ---------------------------------------------------------

    def run(self):

        jd_path = os.path.join(
            "sample_data",
            "jd.txt"
        )

        resume_files = []

        sample_directory = "sample_data"

        if os.path.exists(
            sample_directory
        ):

            for filename in os.listdir(
                sample_directory
            ):

                if (
                    filename.lower().endswith(
                        ".txt"
                    )
                    and filename.lower()
                    != "jd.txt"
                ):

                    resume_files.append(
                        os.path.join(
                            sample_directory,
                            filename
                        )
                    )

        if not resume_files:

            print(
                "No resume files found."
            )

            return

        print("=" * 70)

        print(
            "       INTELLIGENT RESUME ANALYZER"
        )

        print("=" * 70)

        print(
            f"\nFound {len(resume_files)} resume(s)."
        )

        print(
            "\nAnalyzing resumes..."
        )

        results = self.analyze_multiple_resumes(
            resume_files,
            jd_path
        )

        report = self.generate_multiple_report(
            results,
            jd_path
        )

        print("\n")

        print(report)

        output_path = os.path.join(
            "output",
            "report.txt"
        )

        self.save_multiple_report(
            results,
            jd_path,
            output_path
        )

        print(
            f"\nReport saved to: "
            f"{output_path}"
        )


if __name__ == "__main__":

    analyzer = ResumeAnalyzer()

    analyzer.run()