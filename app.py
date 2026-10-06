import os
import tempfile
import pandas as pd
import streamlit as st

from analyzer import ResumeAnalyzer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Intelligent Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS ONLY
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #f4f7fb;
}

[data-testid="stAppViewContainer"] {
    background-color: #f4f7fb;
}

[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #dbe3ee;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Titles */

h1, h2, h3 {
    color: #12355b !important;
}

p {
    color: #334155;
}

/* Buttons */

.stButton > button {
    background-color: #12355b !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 800 !important;
    min-height: 50px !important;
}

.stButton > button:hover {
    background-color: #1d4f7a !important;
}

/* Metrics */

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #dbe3ee;
    border-radius: 15px;
    padding: 18px;
}

/* File uploader */

[data-testid="stFileUploader"] {
    background-color: white;
    border: 2px dashed #7c9cc6;
    border-radius: 15px;
    padding: 12px;
}

/* Expander */

[data-testid="stExpander"] {
    background-color: white;
    border: 1px solid #dbe3ee;
    border-radius: 15px;
}

/* Download */

.stDownloadButton > button {
    border: 2px solid #12355b !important;
    color: #12355b !important;
    background-color: white !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# MAIN TITLE
# ============================================================

st.title("📄 Intelligent Resume Analyzer")

st.subheader(
    "AI-Powered Resume Screening, Skill Matching & Candidate Ranking"
)

st.write(
    "Upload • Analyze • Compare • Rank • Report"
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Project Information")

    st.info(
        """
        **Intelligent Resume Analyzer**

        This application compares candidate
        resumes with a Job Description and
        calculates a resume-to-job matching score.
        """
    )

    st.subheader("🔍 Analysis Features")

    st.markdown("✅ Resume Matching")
    st.markdown("✅ Skill Extraction")
    st.markdown("✅ Missing Skill Detection")
    st.markdown("✅ Candidate Scoring")
    st.markdown("✅ Candidate Ranking")
    st.markdown("✅ Recommendations")
    st.markdown("✅ Detailed Report")

    st.divider()

    st.markdown("### Developed by")

    # YOUR NAME IN BOLD
    st.markdown("**G. Santhiya**")

    st.markdown("III Year AI & DS")


# ============================================================
# STEP 1
# ============================================================

st.header("📋 Step 1 — Upload Job Description")

st.write(
    "Upload the job description that will be used "
    "to evaluate candidate resumes."
)

jd_file = st.file_uploader(
    "📄 Choose Job Description",
    type=["txt"],
    help="Upload a .txt Job Description file.",
    key="jd_upload"
)


# ============================================================
# STEP 2
# ============================================================

st.header("📄 Step 2 — Upload Candidate Resumes")

st.write(
    "Upload one or more candidate resumes. "
    "Multiple candidates can be analyzed and ranked."
)

resume_files = st.file_uploader(
    "📁 Choose Candidate Resumes",
    type=["txt"],
    accept_multiple_files=True,
    help="You can upload multiple .txt resume files.",
    key="resume_upload"
)


# ============================================================
# UPLOAD STATUS
# ============================================================

col1, col2 = st.columns(2)

with col1:

    if jd_file:
        st.success(
            f"✅ Job Description selected: {jd_file.name}"
        )
    else:
        st.info(
            "📋 Please select a Job Description."
        )


with col2:

    if resume_files:
        st.success(
            f"✅ {len(resume_files)} resume(s) selected."
        )
    else:
        st.info(
            "📄 Please select candidate resumes."
        )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.write("")

analyze_button = st.button(
    "🚀 ANALYZE ALL RESUMES",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if jd_file is None:

        st.error(
            "❌ Please upload a Job Description before analysis."
        )

        st.stop()


    if not resume_files:

        st.error(
            "❌ Please upload at least one candidate resume."
        )

        st.stop()


    # --------------------------------------------------------
    # TEMP DIRECTORY
    # --------------------------------------------------------

    temp_directory = tempfile.mkdtemp()


    # --------------------------------------------------------
    # SAVE JD
    # --------------------------------------------------------

    jd_path = os.path.join(
        temp_directory,
        "job_description.txt"
    )

    with open(
        jd_path,
        "wb"
    ) as file:

        file.write(
            jd_file.getbuffer()
        )


    # --------------------------------------------------------
    # SAVE RESUMES
    # --------------------------------------------------------

    resume_paths = []

    for index, resume_file in enumerate(resume_files):

        safe_name = (
            resume_file.name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        resume_path = os.path.join(
            temp_directory,
            f"{index}_{safe_name}"
        )

        with open(
            resume_path,
            "wb"
        ) as file:

            file.write(
                resume_file.getbuffer()
            )

        resume_paths.append(resume_path)


    # --------------------------------------------------------
    # RUN ANALYZER
    # --------------------------------------------------------

    with st.spinner(
        "🔄 Analyzing resumes and calculating scores..."
    ):

        try:

            analyzer = ResumeAnalyzer()

            results = analyzer.analyze_multiple_resumes(
                resume_paths,
                jd_path
            )

        except Exception as error:

            st.error(
                "❌ An error occurred during analysis."
            )

            st.exception(error)

            st.stop()


    # --------------------------------------------------------
    # CHECK RESULTS
    # --------------------------------------------------------

    if not results:

        st.warning(
            "⚠️ No valid resume results were generated."
        )

        st.stop()


    # ========================================================
    # SUCCESS
    # ========================================================

    st.success(
        f"🎉 Analysis completed successfully for "
        f"{len(results)} candidate(s)."
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    st.header("📊 Analysis Summary")

    total_candidates = len(results)

    best_candidate = results[0]

    scores = [
        float(result["score"])
        for result in results
    ]

    average_score = (
        sum(scores) / len(scores)
    )

    highest_score = max(scores)


    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👥 Candidates",
            total_candidates
        )

    with col2:

        st.metric(
            "🏆 Best Score",
            f"{highest_score:.2f}%"
        )

    with col3:

        st.metric(
            "📈 Average Score",
            f"{average_score:.2f}%"
        )

    with col4:

        st.metric(
            "🥇 Top Candidate",
            best_candidate["candidate"]
        )


    # ========================================================
    # TOP CANDIDATE
    # ========================================================

    st.header("🥇 Top Recommended Candidate")

    st.success(
        f"""
        **{best_candidate["candidate"]}**

        Rank: #{best_candidate["rank"]}

        Match Score: **{best_candidate["score"]}%**

        Rating: **{best_candidate["rating"]}**
        """
    )


    # ========================================================
    # RANKING TABLE
    # ========================================================

    st.header("🏆 Candidate Ranking")

    ranking_data = []

    for result in results:

        ranking_data.append(
            {
                "Rank": result["rank"],
                "Candidate": result["candidate"],
                "Score": f'{result["score"]}%',
                "Rating": result["rating"],
                "Resume": result["file"]
            }
        )


    ranking_df = pd.DataFrame(
        ranking_data
    )


    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # SCORE CHART
    # ========================================================

    st.header("📈 Candidate Score Comparison")

    chart_data = pd.DataFrame(
        {
            "Candidate": [
                result["candidate"]
                for result in results
            ],
            "Match Score": [
                float(result["score"])
                for result in results
            ]
        }
    )

    chart_data = chart_data.set_index(
        "Candidate"
    )

    st.bar_chart(
        chart_data,
        height=400
    )


    # ========================================================
    # DETAILED ANALYSIS
    # ========================================================

    st.header("🔍 Detailed Candidate Analysis")


    for result in results:

        candidate = result["candidate"]

        score = float(
            result["score"]
        )

        rating = result["rating"]


        if result["rank"] == 1:

            icon = "🥇"

        elif result["rank"] == 2:

            icon = "🥈"

        elif result["rank"] == 3:

            icon = "🥉"

        else:

            icon = "👤"


        with st.expander(
            f"{icon} Rank #{result['rank']} | "
            f"{candidate} | "
            f"{score:.2f}% | "
            f"{rating}",
            expanded=(result["rank"] == 1)
        ):

            # ------------------------------------------------
            # SCORE
            # ------------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Resume Match Score",
                    f"{score:.2f}%"
                )

            with col2:

                st.metric(
                    "Rating",
                    rating
                )


            st.progress(
                min(
                    max(
                        score / 100,
                        0.0
                    ),
                    1.0
                )
            )


            st.divider()


            # ------------------------------------------------
            # SKILLS
            # ------------------------------------------------

            matched = sorted(
                list(
                    result.get(
                        "matched",
                        []
                    )
                )
            )

            missing = sorted(
                list(
                    result.get(
                        "missing",
                        []
                    )
                )
            )

            extra = sorted(
                list(
                    result.get(
                        "extra",
                        []
                    )
                )
            )


            skill_col1, skill_col2, skill_col3 = st.columns(3)


            # ------------------------------------------------
            # MATCHED
            # ------------------------------------------------

            with skill_col1:

                st.subheader("✅ Matched Skills")

                if matched:

                    for skill in matched:

                        st.success(
                            skill
                        )

                else:

                    st.info(
                        "No matching skills found."
                    )


            # ------------------------------------------------
            # MISSING
            # ------------------------------------------------

            with skill_col2:

                st.subheader("❌ Missing Skills")

                if missing:

                    for skill in missing:

                        st.error(
                            skill
                        )

                else:

                    st.success(
                        "No major missing skills."
                    )


            # ------------------------------------------------
            # EXTRA
            # ------------------------------------------------

            with skill_col3:

                st.subheader("⭐ Additional Skills")

                if extra:

                    for skill in extra:

                        st.info(
                            skill
                        )

                else:

                    st.info(
                        "No additional skills detected."
                    )


            st.divider()


            # ------------------------------------------------
            # RECOMMENDATION
            # ------------------------------------------------

            st.subheader("💡 Recommendation")

            recommendation = result.get(
                "recommendation",
                "No recommendation available."
            )

            st.info(
                recommendation
            )


            # ------------------------------------------------
            # SUGGESTIONS
            # ------------------------------------------------

            suggestions = result.get(
                "suggestions",
                []
            )

            if suggestions:

                st.subheader("📝 Suggestions")

                for suggestion in suggestions:

                    st.write(
                        f"• {suggestion}"
                    )


    # ========================================================
    # COMPLETE REPORT
    # ========================================================

    st.header("📑 Complete Analysis Report")

    try:

        report = analyzer.generate_multiple_report(
            results,
            jd_path
        )


        st.text_area(
            "Analysis Report",
            report,
            height=500
        )


        st.download_button(
            label="⬇️ Download Complete Report",
            data=report,
            file_name="resume_analysis_report.txt",
            mime="text/plain",
            use_container_width=True
        )


    except Exception as error:

        st.warning(
            "⚠️ The report could not be generated."
        )

        st.exception(error)


    # ========================================================
    # FINAL RECOMMENDATION
    # ========================================================

    st.header("🏅 Final Recommendation")

    st.success(
        f"""
        🥇 **{best_candidate["candidate"]}**

        **Match Score:** {best_candidate["score"]}%

        **Rating:** {best_candidate["rating"]}

        This candidate achieved the highest
        resume-to-job-description matching score
        among the uploaded resumes.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "📄 Intelligent Resume Analyzer | "
    "AI & Data Science | Resume Screening & Candidate Ranking"
)

st.markdown(
    "**Developed by G. Santhiya**"
)

st.caption("III Year AI & DS")