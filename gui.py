"""
=============================================================
        INTELLIGENT RESUME ANALYZER
        Modern GUI Dashboard
=============================================================

Purpose:
    Compare multiple resumes with one Job Description.

Features:
    1. Select Job Description
    2. Select multiple resumes
    3. Validate selected files
    4. Analyze all resumes
    5. Rank candidates
    6. Display scores and ratings
    7. Display detailed analysis
    8. Save report through analyzer
    9. Modern dashboard UI
   10. Scrollable complete interface

IMPORTANT:
    No external GUI package is used.
    This file uses only Python built-in Tkinter.

Project structure is NOT changed.
=============================================================
"""

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from analyzer import ResumeAnalyzer


# =============================================================
# MAIN GUI CLASS
# =============================================================

class ResumeAnalyzerGUI:

    # =========================================================
    # COLOR PALETTE
    # =========================================================

    BG = "#F3F6FB"
    CARD = "#FFFFFF"

    DARK = "#172033"
    DARK2 = "#202D45"

    TEXT = "#263449"
    MUTED = "#718096"

    PRIMARY = "#5B5FEF"
    PRIMARY_DARK = "#4548C9"
    PRIMARY_LIGHT = "#EEF0FF"

    SUCCESS = "#16A34A"
    SUCCESS_LIGHT = "#EAF8EF"

    WARNING = "#F59E0B"
    WARNING_LIGHT = "#FFF7E6"

    DANGER = "#DC2626"
    DANGER_LIGHT = "#FDECEC"

    BLUE = "#2563EB"

    BORDER = "#DCE3EE"

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, root):

        self.root = root

        # -----------------------------------------------------
        # Window
        # -----------------------------------------------------

        self.root.title(
            "Intelligent Resume Analyzer"
        )

        self.root.geometry(
            "1400x900"
        )

        self.root.minsize(
            1100,
            700
        )

        self.root.configure(
            bg=self.BG
        )

        # Try to maximize on Windows
        try:
            self.root.state("zoomed")
        except Exception:
            pass

        # -----------------------------------------------------
        # Data variables
        # -----------------------------------------------------

        self.jd_path = ""

        self.resume_paths = []

        self.last_results = []

        self.last_report = ""

        # -----------------------------------------------------
        # Build application
        # -----------------------------------------------------

        self.configure_styles()

        self.create_header()

        self.create_scrollable_area()

        self.create_main_content()

        self.create_status_bar()

        # -----------------------------------------------------
        # Bind resize / mouse wheel
        # -----------------------------------------------------

        self.root.bind(
            "<Configure>",
            self.on_window_resize
        )

    # =========================================================
    # STYLE CONFIGURATION
    # =========================================================

    def configure_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        # -----------------------------------------------------
        # Treeview
        # -----------------------------------------------------

        style.configure(
            "Treeview",
            background=self.CARD,
            foreground=self.TEXT,
            fieldbackground=self.CARD,
            rowheight=45,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background=self.DARK,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=10
        )

        style.map(
            "Treeview",
            background=[
                ("selected", self.PRIMARY_LIGHT)
            ],
            foreground=[
                ("selected", self.DARK)
            ]
        )

        # -----------------------------------------------------
        # Scrollbar
        # -----------------------------------------------------

        style.configure(
            "Vertical.TScrollbar",
            background="#D5DDEA",
            troughcolor="#F3F6FB",
            bordercolor="#F3F6FB",
            arrowcolor=self.DARK
        )

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.DARK,
            height=115
        )

        header.pack(
            fill="x",
            side="top"
        )

        header.pack_propagate(
            False
        )

        # -----------------------------------------------------
        # Left side
        # -----------------------------------------------------

        left = tk.Frame(
            header,
            bg=self.DARK
        )

        left.pack(
            side="left",
            padx=35,
            pady=15
        )

        # AI box

        ai_box = tk.Label(
            left,
            text="AI",
            bg=self.PRIMARY,
            fg="white",
            font=("Segoe UI", 18, "bold"),
            width=4,
            height=2
        )

        ai_box.pack(
            side="left",
            padx=(0, 16)
        )

        # Title area

        title_frame = tk.Frame(
            left,
            bg=self.DARK
        )

        title_frame.pack(
            side="left"
        )

        title = tk.Label(
            title_frame,
            text="Intelligent Resume Analyzer",
            bg=self.DARK,
            fg="white",
            font=("Segoe UI", 23, "bold")
        )

        title.pack(
            anchor="w"
        )

        subtitle = tk.Label(
            title_frame,
            text=(
                "AI-powered resume screening "
                "& candidate ranking"
            ),
            bg=self.DARK,
            fg="#AAB6CA",
            font=("Segoe UI", 10)
        )

        subtitle.pack(
            anchor="w",
            pady=(4, 0)
        )

        # -----------------------------------------------------
        # Right status
        # -----------------------------------------------------

        self.header_status = tk.Label(
            header,
            text="●  READY TO ANALYZE",
            bg="#263550",
            fg="#8EF0A9",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=10
        )

        self.header_status.pack(
            side="right",
            padx=35
        )

    # =========================================================
    # SCROLLABLE AREA
    # =========================================================

    def create_scrollable_area(self):

        # Main canvas

        self.canvas = tk.Canvas(
            self.root,
            bg=self.BG,
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Vertical scrollbar

        self.main_scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview,
            style="Vertical.TScrollbar"
        )

        self.main_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=self.main_scrollbar.set
        )

        # Content frame

        self.scroll_frame = tk.Frame(
            self.canvas,
            bg=self.BG
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor="nw"
        )

        # Update scroll region

        self.scroll_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        # Mouse wheel

        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_wheel
        )

        # Linux mouse wheel

        self.canvas.bind_all(
            "<Button-4>",
            self.mouse_wheel_linux_up
        )

        self.canvas.bind_all(
            "<Button-5>",
            self.mouse_wheel_linux_down
        )

    # =========================================================
    # UPDATE SCROLL REGION
    # =========================================================

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # =========================================================
    # RESIZE
    # =========================================================

    def on_window_resize(self, event):

        try:

            width = self.canvas.winfo_width()

            self.canvas.itemconfig(
                self.canvas_window,
                width=width
            )

        except Exception:
            pass

    # =========================================================
    # MOUSE WHEEL
    # =========================================================

    def mouse_wheel(self, event):

        try:

            self.canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        except Exception:
            pass

    # =========================================================
    # LINUX SCROLL UP
    # =========================================================

    def mouse_wheel_linux_up(self, event):

        self.canvas.yview_scroll(
            -3,
            "units"
        )

    # =========================================================
    # LINUX SCROLL DOWN
    # =========================================================

    def mouse_wheel_linux_down(self, event):

        self.canvas.yview_scroll(
            3,
            "units"
        )

    # =========================================================
    # MAIN CONTENT
    # =========================================================

    def create_main_content(self):

        outer = tk.Frame(
            self.scroll_frame,
            bg=self.BG
        )

        outer.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=25
        )

        # -----------------------------------------------------
        # PAGE TITLE
        # -----------------------------------------------------

        page_title = tk.Label(
            outer,
            text="Candidate Screening Dashboard",
            bg=self.BG,
            fg=self.DARK,
            font=("Segoe UI", 20, "bold")
        )

        page_title.pack(
            anchor="w"
        )

        page_description = tk.Label(
            outer,
            text=(
                "Upload one Job Description and compare "
                "it against multiple candidate resumes."
            ),
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 10)
        )

        page_description.pack(
            anchor="w",
            pady=(4, 20)
        )

        # -----------------------------------------------------
        # UPLOAD SECTION
        # -----------------------------------------------------

        upload_frame = tk.Frame(
            outer,
            bg=self.BG
        )

        upload_frame.pack(
            fill="x"
        )

        upload_frame.columnconfigure(
            0,
            weight=1
        )

        upload_frame.columnconfigure(
            1,
            weight=1
        )

        self.create_jd_card(
            upload_frame
        )

        self.create_resume_card(
            upload_frame
        )

        # -----------------------------------------------------
        # ACTION BUTTONS
        # -----------------------------------------------------

        self.create_action_buttons(
            outer
        )

        # -----------------------------------------------------
        # SUMMARY
        # -----------------------------------------------------

        self.create_summary_cards(
            outer
        )

        # -----------------------------------------------------
        # RANKING
        # -----------------------------------------------------

        self.create_ranking_section(
            outer
        )

        # -----------------------------------------------------
        # DETAILED REPORT
        # -----------------------------------------------------

        self.create_report_section(
            outer
        )

        # -----------------------------------------------------
        # Bottom padding
        # -----------------------------------------------------

        bottom_space = tk.Frame(
            outer,
            bg=self.BG,
            height=30
        )

        bottom_space.pack(
            fill="x"
        )

    # =========================================================
    # JOB DESCRIPTION CARD
    # =========================================================

    def create_jd_card(self, parent):

        card = tk.Frame(
            parent,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        # Icon

        icon = tk.Label(
            card,
            text="FILE",
            bg=self.PRIMARY_LIGHT,
            fg=self.PRIMARY,
            font=("Segoe UI", 9, "bold"),
            width=7,
            height=2
        )

        icon.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # Title

        title = tk.Label(
            card,
            text="Job Description",
            bg=self.CARD,
            fg=self.DARK,
            font=("Segoe UI", 14, "bold")
        )

        title.pack(
            anchor="w",
            padx=20
        )

        # Description

        desc = tk.Label(
            card,
            text=(
                "Upload the .txt file containing "
                "the job requirements."
            ),
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )

        desc.pack(
            anchor="w",
            padx=20,
            pady=(4, 12)
        )

        # Button

        button = tk.Button(
            card,
            text="Choose JD File",
            command=self.select_jd,
            bg=self.PRIMARY_LIGHT,
            fg=self.PRIMARY_DARK,
            activebackground="#DFE3FF",
            activeforeground=self.PRIMARY_DARK,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=18,
            pady=9
        )

        button.pack(
            anchor="w",
            padx=20
        )

        # Selected file

        self.jd_label = tk.Label(
            card,
            text="No Job Description selected",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )

        self.jd_label.pack(
            anchor="w",
            padx=20,
            pady=(10, 20)
        )

    # =========================================================
    # RESUME CARD
    # =========================================================

    def create_resume_card(self, parent):

        card = tk.Frame(
            parent,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        # Icon

        icon = tk.Label(
            card,
            text="USERS",
            bg=self.PRIMARY_LIGHT,
            fg=self.PRIMARY,
            font=("Segoe UI", 9, "bold"),
            width=7,
            height=2
        )

        icon.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # Title

        title = tk.Label(
            card,
            text="Candidate Resumes",
            bg=self.CARD,
            fg=self.DARK,
            font=("Segoe UI", 14, "bold")
        )

        title.pack(
            anchor="w",
            padx=20
        )

        # Description

        desc = tk.Label(
            card,
            text=(
                "Select multiple .txt resumes "
                "for comparison."
            ),
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )

        desc.pack(
            anchor="w",
            padx=20,
            pady=(4, 12)
        )

        # Button

        button = tk.Button(
            card,
            text="Choose Resume Files",
            command=self.select_resumes,
            bg=self.PRIMARY_LIGHT,
            fg=self.PRIMARY_DARK,
            activebackground="#DFE3FF",
            activeforeground=self.PRIMARY_DARK,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=18,
            pady=9
        )

        button.pack(
            anchor="w",
            padx=20
        )

        # Selected files

        self.resume_label = tk.Label(
            card,
            text="No resumes selected",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )

        self.resume_label.pack(
            anchor="w",
            padx=20,
            pady=(10, 20)
        )

    # =========================================================
    # ACTION BUTTONS
    # =========================================================

    def create_action_buttons(self, parent):

        frame = tk.Frame(
            parent,
            bg=self.BG
        )

        frame.pack(
            fill="x",
            pady=20
        )

        # Analyze button

        analyze_button = tk.Button(
            frame,
            text="▶  ANALYZE ALL RESUMES",
            command=self.analyze_resumes,
            bg=self.PRIMARY,
            fg="white",
            activebackground=self.PRIMARY_DARK,
            activeforeground="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=30,
            pady=13
        )

        analyze_button.pack(
            side="left"
        )

        # Clear button

        clear_button = tk.Button(
            frame,
            text="↻  CLEAR",
            command=self.clear_all,
            bg=self.CARD,
            fg=self.TEXT,
            activebackground="#E9EEF6",
            activeforeground=self.TEXT,
            font=("Segoe UI", 10, "bold"),
            relief="solid",
            bd=1,
            cursor="hand2",
            padx=25,
            pady=11
        )

        clear_button.pack(
            side="left",
            padx=12
        )

    # =========================================================
    # SUMMARY CARDS
    # =========================================================

    def create_summary_cards(self, parent):

        frame = tk.Frame(
            parent,
            bg=self.BG
        )

        frame.pack(
            fill="x",
            pady=(0, 20)
        )

        for i in range(4):

            frame.columnconfigure(
                i,
                weight=1
            )

        self.total_card = self.create_stat_card(
            frame,
            0,
            "TOTAL RESUMES",
            "0",
            "Candidates analyzed"
        )

        self.top_card = self.create_stat_card(
            frame,
            1,
            "TOP CANDIDATE",
            "-",
            "Highest matching score"
        )

        self.score_card = self.create_stat_card(
            frame,
            2,
            "TOP SCORE",
            "0%",
            "Best resume match"
        )

        self.status_card = self.create_stat_card(
            frame,
            3,
            "STATUS",
            "READY",
            "System status"
        )

    # =========================================================
    # STAT CARD
    # =========================================================

    def create_stat_card(
        self,
        parent,
        column,
        title,
        value,
        description
    ):

        card = tk.Frame(
            parent,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=5
        )

        title_label = tk.Label(
            card,
            text=title,
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        )

        title_label.pack(
            anchor="w",
            padx=17,
            pady=(14, 0)
        )

        value_label = tk.Label(
            card,
            text=value,
            bg=self.CARD,
            fg=self.DARK,
            font=("Segoe UI", 17, "bold")
        )

        value_label.pack(
            anchor="w",
            padx=17,
            pady=(3, 0)
        )

        desc_label = tk.Label(
            card,
            text=description,
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 8)
        )

        desc_label.pack(
            anchor="w",
            padx=17,
            pady=(0, 14)
        )

        return value_label

    # =========================================================
    # RANKING SECTION
    # =========================================================

    def create_ranking_section(self, parent):

        card = tk.Frame(
            parent,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        # IMPORTANT:
        # Fixed height through table.
        # It will not disappear anymore.

        card.pack(
            fill="x",
            pady=(0, 20)
        )

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = tk.Frame(
            card,
            bg=self.CARD
        )

        header.pack(
            fill="x",
            padx=22,
            pady=(18, 12)
        )

        title = tk.Label(
            header,
            text="Candidate Ranking",
            bg=self.CARD,
            fg=self.DARK,
            font=("Segoe UI", 15, "bold")
        )

        title.pack(
            side="left"
        )

        subtitle = tk.Label(
            header,
            text=(
                "Candidates sorted by "
                "resume-job match"
            ),
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )

        subtitle.pack(
            side="left",
            padx=12
        )

        # -----------------------------------------------------
        # Table
        # -----------------------------------------------------

        table_frame = tk.Frame(
            card,
            bg=self.CARD
        )

        table_frame.pack(
            fill="x",
            padx=22,
            pady=(0, 22)
        )

        columns = (
            "rank",
            "candidate",
            "score",
            "rating"
        )

        self.ranking_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=6
        )

        # Headings

        self.ranking_table.heading(
            "rank",
            text="RANK"
        )

        self.ranking_table.heading(
            "candidate",
            text="CANDIDATE"
        )

        self.ranking_table.heading(
            "score",
            text="MATCH SCORE"
        )

        self.ranking_table.heading(
            "rating",
            text="RATING"
        )

        # Columns

        self.ranking_table.column(
            "rank",
            width=100,
            minwidth=80,
            anchor="center"
        )

        self.ranking_table.column(
            "candidate",
            width=450,
            minwidth=250,
            anchor="w"
        )

        self.ranking_table.column(
            "score",
            width=250,
            minwidth=150,
            anchor="center"
        )

        self.ranking_table.column(
            "rating",
            width=280,
            minwidth=180,
            anchor="center"
        )

        # Tags

        self.ranking_table.tag_configure(
            "excellent",
            foreground=self.SUCCESS
        )

        self.ranking_table.tag_configure(
            "good",
            foreground=self.BLUE
        )

        self.ranking_table.tag_configure(
            "average",
            foreground=self.WARNING
        )

        self.ranking_table.tag_configure(
            "low",
            foreground=self.DANGER
        )

        self.ranking_table.pack(
            side="left",
            fill="x",
            expand=True
        )

        # Vertical scrollbar

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.ranking_table.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.ranking_table.configure(
            yscrollcommand=scrollbar.set
        )

    # =========================================================
    # DETAILED REPORT SECTION
    # =========================================================

    def create_report_section(self, parent):

        card = tk.Frame(
            parent,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            pady=(0, 20)
        )

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = tk.Frame(
            card,
            bg=self.CARD
        )

        header.pack(
            fill="x",
            padx=22,
            pady=(18, 10)
        )

        title = tk.Label(
            header,
            text="Detailed Analysis",
            bg=self.CARD,
            fg=self.DARK,
            font=("Segoe UI", 15, "bold")
        )

        title.pack(
            side="left"
        )

        self.report_status = tk.Label(
            header,
            text="No analysis yet",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )

        self.report_status.pack(
            side="right"
        )

        # -----------------------------------------------------
        # Report frame
        # -----------------------------------------------------

        report_frame = tk.Frame(
            card,
            bg=self.CARD
        )

        report_frame.pack(
            fill="both",
            padx=22,
            pady=(0, 22)
        )

        # -----------------------------------------------------
        # Text box
        # -----------------------------------------------------

        self.result_box = tk.Text(
            report_frame,
            bg="#F8FAFC",
            fg=self.TEXT,
            insertbackground=self.TEXT,
            selectbackground=self.PRIMARY,
            selectforeground="white",
            font=("Consolas", 10),
            relief="solid",
            borderwidth=1,
            wrap="word",
            height=22
        )

        self.result_box.pack(
            side="left",
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # Scrollbar
        # -----------------------------------------------------

        scrollbar = ttk.Scrollbar(
            report_frame,
            orient="vertical",
            command=self.result_box.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.result_box.configure(
            yscrollcommand=scrollbar.set
        )

        # -----------------------------------------------------
        # Text formatting
        # -----------------------------------------------------

        self.result_box.tag_configure(
            "title",
            foreground=self.PRIMARY,
            font=("Consolas", 12, "bold")
        )

        self.result_box.tag_configure(
            "excellent",
            foreground=self.SUCCESS,
            font=("Consolas", 10, "bold")
        )

        self.result_box.tag_configure(
            "warning",
            foreground=self.WARNING,
            font=("Consolas", 10, "bold")
        )

        self.result_box.tag_configure(
            "danger",
            foreground=self.DANGER,
            font=("Consolas", 10, "bold")
        )

    # =========================================================
    # STATUS BAR
    # =========================================================

    def create_status_bar(self):

        status = tk.Frame(
            self.root,
            bg=self.DARK,
            height=32
        )

        status.pack(
            fill="x",
            side="bottom"
        )

        status.pack_propagate(
            False
        )

        self.status_label = tk.Label(
            status,
            text=(
                "●  Ready — Select a Job Description "
                "and resumes"
            ),
            bg=self.DARK,
            fg="#B7C3D8",
            font=("Segoe UI", 9)
        )

        self.status_label.pack(
            side="left",
            padx=20
        )

        version = tk.Label(
            status,
            text="Python • Tkinter • Resume Analyzer",
            bg=self.DARK,
            fg="#7D8BA4",
            font=("Segoe UI", 8)
        )

        version.pack(
            side="right",
            padx=20
        )

    # =========================================================
    # SELECT JOB DESCRIPTION
    # =========================================================

    def select_jd(self):

        file_path = filedialog.askopenfilename(
            title="Select Job Description",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        valid, message = (
            self.validate_job_description(
                file_path
            )
        )

        if not valid:

            messagebox.showerror(
                "Invalid Job Description",
                message
            )

            self.jd_path = ""

            self.jd_label.config(
                text=(
                    "No valid Job Description selected"
                ),
                fg=self.MUTED
            )

            return

        self.jd_path = file_path

        self.jd_label.config(
            text=(
                "✓  " +
                os.path.basename(file_path)
            ),
            fg=self.SUCCESS
        )

        self.header_status.config(
            text="●  JD SELECTED",
            fg="#8EF0A9"
        )

        self.status_label.config(
            text=(
                "●  Job Description selected successfully"
            )
        )

    # =========================================================
    # SELECT MULTIPLE RESUMES
    # =========================================================

    def select_resumes(self):

        file_paths = (
            filedialog.askopenfilenames(
                title="Select Multiple Resumes",
                filetypes=[
                    ("Text Files", "*.txt"),
                    ("All Files", "*.*")
                ]
            )
        )

        if not file_paths:
            return

        valid_resumes = []

        for path in file_paths:

            valid, message = (
                self.validate_resume(
                    path
                )
            )

            if valid:

                valid_resumes.append(
                    path
                )

        self.resume_paths = valid_resumes

        count = len(
            self.resume_paths
        )

        if count == 0:

            self.resume_label.config(
                text="No valid resumes selected",
                fg=self.DANGER
            )

            messagebox.showerror(
                "Invalid Resumes",
                "No valid resume files were selected."
            )

            return

        self.resume_label.config(
            text=(
                f"✓  {count} resume(s) selected"
            ),
            fg=self.SUCCESS
        )

        self.header_status.config(
            text="●  FILES READY",
            fg="#8EF0A9"
        )

        self.status_label.config(
            text=(
                f"●  {count} candidate resume(s) "
                "ready for analysis"
            )
        )

    # =========================================================
    # VALIDATE JOB DESCRIPTION
    # =========================================================

    def validate_job_description(
        self,
        file_path
    ):

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read().strip()

        except Exception:

            return (
                False,
                "Unable to read the selected file."
            )

        if not text:

            return (
                False,
                "The selected Job Description is empty."
            )

        lower_text = text.lower()

        # -----------------------------------------------------
        # Resume indicators
        # -----------------------------------------------------

        resume_indicators = [
            "resume",
            "career objective",
            "education",
            "experience",
            "certifications",
            "personal details",
            "phone:",
            "email:",
            "projects"
        ]

        resume_count = 0

        for item in resume_indicators:

            if item in lower_text:

                resume_count += 1

        # If several resume indicators are present,
        # prevent user from uploading a resume as JD.

        if resume_count >= 4:

            return (
                False,
                "The selected file appears to be "
                "a RESUME, not a Job Description.\n\n"
                "Please select your jd.txt file."
            )

        # -----------------------------------------------------
        # Job description indicators
        # -----------------------------------------------------

        jd_indicators = [
            "job description",
            "job title",
            "job summary",
            "required skills",
            "technical skills",
            "responsibilities",
            "requirements",
            "qualifications",
            "required experience",
            "candidate should",
            "we are looking",
            "position",
            "role",
            "skills required"
        ]

        jd_count = 0

        for item in jd_indicators:

            if item in lower_text:

                jd_count += 1

        if jd_count == 0:

            return (
                False,
                "This file does not appear to be "
                "a valid Job Description."
            )

        return (
            True,
            "Valid Job Description"
        )

    # =========================================================
    # VALIDATE RESUME
    # =========================================================

    def validate_resume(
        self,
        file_path
    ):

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read().strip()

        except Exception:

            return (
                False,
                "Cannot read file"
            )

        if not text:

            return (
                False,
                "Empty file"
            )

        lower_text = text.lower()

        indicators = [
            "resume",
            "career objective",
            "education",
            "technical skills",
            "soft skills",
            "experience",
            "projects",
            "certifications",
            "name:",
            "email:",
            "skills"
        ]

        count = 0

        for item in indicators:

            if item in lower_text:

                count += 1

        if count < 2:

            return (
                False,
                "Does not appear to be a resume"
            )

        return (
            True,
            "Valid Resume"
        )

    # =========================================================
    # ANALYZE RESUMES
    # =========================================================

    def analyze_resumes(self):

        # -----------------------------------------------------
        # Validate JD
        # -----------------------------------------------------

        if not self.jd_path:

            messagebox.showwarning(
                "Job Description Required",
                "Please select jd.txt first."
            )

            return

        # -----------------------------------------------------
        # Validate resumes
        # -----------------------------------------------------

        if not self.resume_paths:

            messagebox.showwarning(
                "Resumes Required",
                "Please select one or more resumes."
            )

            return

        try:

            # -------------------------------------------------
            # Change status
            # -------------------------------------------------

            self.status_label.config(
                text=(
                    "●  Analyzing candidates..."
                )
            )

            self.header_status.config(
                text="●  ANALYZING",
                fg="#FFD166"
            )

            self.status_card.config(
                text="ANALYZING"
            )

            self.root.update_idletasks()

            # -------------------------------------------------
            # Create analyzer
            # -------------------------------------------------

            analyzer = ResumeAnalyzer()

            # -------------------------------------------------
            # Analyze multiple resumes
            # -------------------------------------------------

            results = (
                analyzer.analyze_multiple_resumes(
                    self.resume_paths,
                    self.jd_path
                )
            )

            if not results:

                messagebox.showerror(
                    "Analysis Error",
                    "No resumes could be analyzed."
                )

                return

            # -------------------------------------------------
            # Store results
            # -------------------------------------------------

            self.last_results = results

            # -------------------------------------------------
            # Generate report
            # -------------------------------------------------

            report = (
                analyzer.generate_multiple_report(
                    results,
                    self.jd_path
                )
            )

            self.last_report = report

            # -------------------------------------------------
            # Output directory
            # -------------------------------------------------

            output_path = os.path.join(
                "output",
                "report.txt"
            )

            os.makedirs(
                "output",
                exist_ok=True
            )

            # -------------------------------------------------
            # Save report
            # -------------------------------------------------

            analyzer.save_multiple_report(
                results,
                self.jd_path,
                output_path
            )

            # -------------------------------------------------
            # Display report
            # -------------------------------------------------

            self.display_report(
                report
            )

            # -------------------------------------------------
            # Update summary
            # -------------------------------------------------

            self.update_summary(
                results
            )

            # -------------------------------------------------
            # Update ranking
            # -------------------------------------------------

            self.update_ranking(
                results
            )

            # -------------------------------------------------
            # Final status
            # -------------------------------------------------

            self.status_card.config(
                text="COMPLETE"
            )

            self.header_status.config(
                text="●  ANALYSIS COMPLETE",
                fg="#8EF0A9"
            )

            self.status_label.config(
                text=(
                    f"●  Analysis complete — "
                    f"{len(results)} candidates ranked"
                )
            )

            self.report_status.config(
                text=(
                    "✓  Report saved to output/report.txt"
                ),
                fg=self.SUCCESS
            )

            # -------------------------------------------------
            # Show success message
            # -------------------------------------------------

            messagebox.showinfo(
                "Analysis Complete",
                (
                    f"{len(results)} resume(s) analyzed.\n\n"
                    "Candidates have been ranked "
                    "successfully.\n\n"
                    "Report saved to:\n"
                    "output/report.txt"
                )
            )

            # -------------------------------------------------
            # Scroll to ranking section
            # -------------------------------------------------

            self.root.after(
                300,
                self.scroll_to_results
            )

        except Exception as error:

            self.status_card.config(
                text="ERROR"
            )

            self.header_status.config(
                text="●  ERROR",
                fg="#FF7777"
            )

            self.status_label.config(
                text="●  Analysis failed"
            )

            messagebox.showerror(
                "Analysis Error",
                str(error)
            )

    # =========================================================
    # SCROLL TO RESULTS
    # =========================================================

    def scroll_to_results(self):

        try:

            self.canvas.yview_moveto(
                0.35
            )

        except Exception:
            pass

    # =========================================================
    # UPDATE SUMMARY
    # =========================================================

    def update_summary(
        self,
        results
    ):

        total = len(
            results
        )

        self.total_card.config(
            text=str(total)
        )

        if not results:

            self.top_card.config(
                text="-"
            )

            self.score_card.config(
                text="0%"
            )

            return

        sorted_results = sorted(
            results,
            key=self.get_score,
            reverse=True
        )

        top = sorted_results[0]

        candidate = (
            self.get_candidate_name(
                top
            )
        )

        score = (
            self.get_score(
                top
            )
        )

        self.top_card.config(
            text=candidate
        )

        self.score_card.config(
            text=f"{score:.1f}%"
        )

    # =========================================================
    # GET CANDIDATE NAME
    # =========================================================

    def get_candidate_name(
        self,
        result
    ):

        if not isinstance(
            result,
            dict
        ):

            return "Candidate"

        possible_keys = [
            "candidate",
            "candidate_name",
            "name",
            "resume_name",
            "file_name",
            "filename"
        ]

        for key in possible_keys:

            if key in result:

                value = result[key]

                if value:

                    value = str(
                        value
                    )

                    # Remove extension

                    if value.lower().endswith(
                        ".txt"
                    ):

                        value = value[:-4]

                    return value

        return "Candidate"

    # =========================================================
    # GET SCORE
    # =========================================================

    def get_score(
        self,
        result
    ):

        if not isinstance(
            result,
            dict
        ):

            return 0.0

        possible_keys = [
            "score",
            "match_score",
            "percentage",
            "matching_score"
        ]

        for key in possible_keys:

            if key in result:

                try:

                    value = float(
                        result[key]
                    )

                    # If score is decimal
                    # Example: 0.85 -> 85

                    if value <= 1:

                        value = value * 100

                    return value

                except Exception:

                    pass

        return 0.0

    # =========================================================
    # GET RATING
    # =========================================================

    def get_rating(
        self,
        result,
        score
    ):

        if isinstance(
            result,
            dict
        ):

            for key in [
                "rating",
                "grade",
                "status"
            ]:

                if key in result:

                    value = result[key]

                    if value:

                        return str(
                            value
                        )

        # Automatic rating

        if score >= 80:

            return "Excellent"

        if score >= 60:

            return "Good"

        if score >= 40:

            return "Average"

        if score >= 20:

            return "Needs Improvement"

        return "Low"

    # =========================================================
    # UPDATE RANKING
    # =========================================================

    def update_ranking(
        self,
        results
    ):

        # -----------------------------------------------------
        # Remove old rows
        # -----------------------------------------------------

        for item in (
            self.ranking_table.get_children()
        ):

            self.ranking_table.delete(
                item
            )

        # -----------------------------------------------------
        # Sort
        # -----------------------------------------------------

        sorted_results = sorted(
            results,
            key=self.get_score,
            reverse=True
        )

        # -----------------------------------------------------
        # Add candidates
        # -----------------------------------------------------

        for index, result in enumerate(
            sorted_results,
            start=1
        ):

            candidate = (
                self.get_candidate_name(
                    result
                )
            )

            score = (
                self.get_score(
                    result
                )
            )

            rating = (
                self.get_rating(
                    result,
                    score
                )
            )

            rating_lower = (
                rating.lower()
            )

            # -------------------------------------------------
            # Select row color
            # -------------------------------------------------

            if "excellent" in rating_lower:

                tag = "excellent"

            elif "good" in rating_lower:

                tag = "good"

            elif "average" in rating_lower:

                tag = "average"

            else:

                tag = "low"

            # -------------------------------------------------
            # Insert
            # -------------------------------------------------

            self.ranking_table.insert(
                "",
                "end",
                values=(
                    index,
                    candidate,
                    f"{score:.1f}%",
                    rating
                ),
                tags=(tag,)
            )

    # =========================================================
    # DISPLAY REPORT
    # =========================================================

    def display_report(
        self,
        report
    ):

        self.result_box.delete(
            "1.0",
            tk.END
        )

        lines = report.splitlines()

        for line in lines:

            lower = line.lower()

            # -------------------------------------------------
            # Title
            # -------------------------------------------------

            if (
                "intelligent resume analyzer"
                in lower
            ):

                self.result_box.insert(
                    tk.END,
                    line + "\n",
                    "title"
                )

            # -------------------------------------------------
            # Excellent
            # -------------------------------------------------

            elif "excellent" in lower:

                self.result_box.insert(
                    tk.END,
                    line + "\n",
                    "excellent"
                )

            # -------------------------------------------------
            # Average
            # -------------------------------------------------

            elif "average" in lower:

                self.result_box.insert(
                    tk.END,
                    line + "\n",
                    "warning"
                )

            # -------------------------------------------------
            # Low / Missing
            # -------------------------------------------------

            elif (
                "low" in lower
                or "missing" in lower
            ):

                self.result_box.insert(
                    tk.END,
                    line + "\n",
                    "danger"
                )

            # -------------------------------------------------
            # Normal
            # -------------------------------------------------

            else:

                self.result_box.insert(
                    tk.END,
                    line + "\n"
                )

        # Move to top

        self.result_box.see(
            "1.0"
        )

    # =========================================================
    # CLEAR ALL
    # =========================================================

    def clear_all(self):

        # -----------------------------------------------------
        # Clear variables
        # -----------------------------------------------------

        self.jd_path = ""

        self.resume_paths = []

        self.last_results = []

        self.last_report = ""

        # -----------------------------------------------------
        # Clear JD
        # -----------------------------------------------------

        self.jd_label.config(
            text="No Job Description selected",
            fg=self.MUTED
        )

        # -----------------------------------------------------
        # Clear resumes
        # -----------------------------------------------------

        self.resume_label.config(
            text="No resumes selected",
            fg=self.MUTED
        )

        # -----------------------------------------------------
        # Clear summary
        # -----------------------------------------------------

        self.total_card.config(
            text="0"
        )

        self.top_card.config(
            text="-"
        )

        self.score_card.config(
            text="0%"
        )

        self.status_card.config(
            text="READY"
        )

        # -----------------------------------------------------
        # Clear table
        # -----------------------------------------------------

        for item in (
            self.ranking_table.get_children()
        ):

            self.ranking_table.delete(
                item
            )

        # -----------------------------------------------------
        # Clear report
        # -----------------------------------------------------

        self.result_box.delete(
            "1.0",
            tk.END
        )

        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        self.report_status.config(
            text="No analysis yet",
            fg=self.MUTED
        )

        self.header_status.config(
            text="●  READY TO ANALYZE",
            fg="#8EF0A9"
        )

        self.status_label.config(
            text=(
                "●  Ready — Select a Job Description "
                "and resumes"
            )
        )

        # -----------------------------------------------------
        # Go to top
        # -----------------------------------------------------

        self.canvas.yview_moveto(
            0
        )


# =============================================================
# APPLICATION ENTRY POINT
# =============================================================

def main():

    root = tk.Tk()

    app = ResumeAnalyzerGUI(
        root
    )

    root.mainloop()


# =============================================================
# RUN APPLICATION
# =============================================================

if __name__ == "__main__":

    main()