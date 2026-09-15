from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Introduction to eigenvectors ---
        # ----------------------------------------------------------------------
        # 1️⃣ Scene setup
        # ----------------------------------------------------------------------
        # Background colour from the style guide
        self.camera.background_color = "#181825"

        # ----------------------------------------------------------------------
        # 2️⃣ Objects (precise position, colour and size)
        # ----------------------------------------------------------------------
        # Title – placed high up
        title_1 = Text(
            "Introduction to eigenvectors",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # Main statement – centre of the screen
        main_1 = Text(
            "Today we are exploring eigenvectors.",
            font_size=48,
            color="#89b4fa",  # first colour of the palette
        ).move_to(ORIGIN)

        # ----------------------------------------------------------------------
        # 3️⃣ Animations (creative yet pedagogically clear)
        # ----------------------------------------------------------------------
        # Write the title (2 s)
        self.play(Write(title_1, run_time=2.0))

        # Write the main sentence (2 s)
        self.play(Write(main_1, run_time=2.0))

        # Hold the completed frame for the remaining time (2 s)
        self.wait(2.0)
        # --- Scene 2: Step 2: Why eigenvectors matters ---
        # --------------------------------------------------------------------
        # 1️⃣  General scene style
        # --------------------------------------------------------------------
        self.camera.background_color = "#181825"  # dark background

        # --------------------------------------------------------------------
        # 2️⃣  Objects
        # --------------------------------------------------------------------
        # Axes (core visual metaphor)
        main_2 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": "#fab387", "stroke_width": 2.0},
        )
        main_2.shift(ORIGIN)  # explicit positioning

        # Title text
        title_2 = Text(
            "Why eigenvectors matters",
            font="Sans",
            font_size=36,
            color=WHITE,
        ).shift(UP * 3)

        # --------------------------------------------------------------------
        # 3️⃣  Animations (exact total run‑time = 6 s)
        # --------------------------------------------------------------------
        # 1 s → fade‑in the title
        self.play(FadeIn(title_2, shift=UP * 0.5), run_time=1.5)

        # 2 s → hand‑write the axes (including tick marks & numbers)
        self.play(Write(main_2), run_time=2.5)

        # 2 s → pause so the total scene length matches the requested 6 s
        self.wait(2.0)
        # --- Scene 3: Step 3: Core mechanics of eigenvectors ---
        # ------------------------------------------------------------------
        # 1.  Scene style
        # ------------------------------------------------------------------
        self.camera.background_color = "#181825"  # dark background

        # ------------------------------------------------------------------
        # 2.  Objects
        # ------------------------------------------------------------------
        # Title – written at the top
        title_3 = Text(
            "Core mechanics of eigenvectors",
            font_size=36,
            color=WHITE,
        ).shift(UP * 3)

        # Number line – placed near the bottom, coloured with the palette hue
        main_3 = NumberLine(
            x_range=[-5, 5],
            length=10,
            include_numbers=True,
            color="#f38ba8",  # pink‑ish from the palette
        ).shift(DOWN)

        # The line’s numbers need to be added after creation
        main_3.add_numbers()

        # A small dot at the origin to illustrate the “eigen‑direction”
        # (extra visual metaphor, not required by the storyboard but
        # helps keep the 6‑second timing clean)
        origin_dot = Dot(
            point=main_3.n2p(0),
            radius=0.08,
            color="#a6e3a1",  # teal from the palette
        )

        # ------------------------------------------------------------------
        # 3.  Build the scene with a choreography that totals 6 seconds
        # ------------------------------------------------------------------
        # Write the title (2 s)
        self.play(Write(title_3, run_time=2.0))

        # Fade‑in the number line with its tick marks (2 s)
        self.play(FadeIn(main_3, run_time=2.0))

        # Grow the origin dot from its centre (1 s)
        self.play(GrowFromCenter(origin_dot, run_time=1.0))

        # Hold the final frame for the remaining second (1 s)
        self.wait(1.0)
        # --- Scene 4: Step 4: Common pitfalls in eigenvectors ---
        # ----------------------------------------------------------------------
        # 1. Global style & background
        # ----------------------------------------------------------------------
        self.camera.background_color = "#181825"  # dark background per style guide
        default_stroke_width = 2.0  # from style guidelines

        # ----------------------------------------------------------------------
        # 2. Title – written in the first 1.5 s
        # ----------------------------------------------------------------------
        title_4 = Text(
            "Common pitfalls in eigenvectors",
            font="Sans",
            font_size=36,
            color=WHITE,
        )
        title_4.move_to(UP * 3)

        # ----------------------------------------------------------------------
        # 3. Main content – a VGroup that will hold bullet points and a warning icon
        # ----------------------------------------------------------------------
        # ─── bullet points (common misconceptions) ─────────────────────────────
        bullet_texts = [
            "Any vector can be an eigenvector → not true",
            "Eigenvectors must be orthogonal",
            "Eigenvectors have to be unit‑length",
        ]
        bullet_items = VGroup()
        for i, txt in enumerate(bullet_texts):
            # using a slightly smaller font for the bullets
            b = Text(
                f"• {txt}",
                font="Sans",
                font_size=28,
                color="#f38ba8",  # a reddish palette colour
            )
            b.next_to(title_4, DOWN, buff=0.8 + i * 0.6)
            bullet_items.add(b)

        # ─── warning icon (exclamation inside a circle) ───────────────────────
        warning_circle = Circle(
            radius=0.4,
            color="#fab387",  # orange‑ish from the palette
            stroke_width=default_stroke_width,
        )
        warning_excl = Text(
            "!",
            font="Sans",
            font_size=36,
            color=WHITE,
        )
        warning_excl.move_to(warning_circle.get_center())
        warning_icon = VGroup(warning_circle, warning_excl)
        warning_icon.next_to(bullet_items, DOWN, buff=0.8)

        # Assemble everything into the requested VGroup `main_4`
        main_4 = VGroup(bullet_items, warning_icon)
        main_4.set_color("#a6e3a1")  # the colour specified for the group
        main_4.move_to(ORIGIN)  # positioned at the origin as requested

        # ----------------------------------------------------------------------
        # 4. Animations (total duration = 6 s)
        # ----------------------------------------------------------------------
        # 4.1 Write the title (1.5 s)
        self.play(Write(title_4, run_time=1.5))

        # 4.2 Fade‑in the bullet points one after another (total 2.5 s)
        bullet_fadeins = [FadeIn(item, run_time=0.8) for item in bullet_items]
        self.play(
            LaggedStart(*bullet_fadeins, lag_ratio=0.3),
            run_time=2.5,
        )

        # 4.3 Grow the warning icon from its centre (0.5 s)
        self.play(GrowFromCenter(warning_icon, run_time=0.5))

        # 4.4 Hold the final frame so the narration can finish (1.5 s)
        self.wait(1.5)
        # --- Scene 5: Step 5: Practical application of eigenvectors ---
        # --------------------------------------------------------------------
        # 0. Scene styling
        # --------------------------------------------------------------------
        self.camera.background_color = "#181825"  # Dark background
        self.default_stroke_width = 2.0  # Consistent stroke width

        # --------------------------------------------------------------------
        # 1. Objects
        # --------------------------------------------------------------------
        # Title --------------------------------------------------------------
        title_5 = Text(
            "Practical application of eigenvectors",
            font_size=36,
            color=WHITE,
        ).shift(UP * 3)

        # Table ---------------------------------------------------------------
        # Simple illustrative data – feel free to replace with the real content
        data = [
            ["Scenario", "Eigenvector", "Interpretation"],
            [
                "Population growth",
                r"\begin{bmatrix}1\\1\end{bmatrix}",
                "Aligns with the dominant growth direction",
            ],
            [
                "Markov chain",
                r"\begin{bmatrix}0.6\\0.4\end{bmatrix}",
                "Steady‑state distribution",
            ],
        ]
        main_5 = (
            Table(
                data,
                include_outer_lines=True,
                line_config={"stroke_width": 2},
            )
            .scale(0.7)
            .set_color("#94e2d5")
        )  # palette colour for the table
        main_5.move_to(ORIGIN)

        # A faint background rectangle improves legibility on the dark canvas
        bg_rect = BackgroundRectangle(
            main_5,
            fill_opacity=0.75,
            fill_color=BLACK,
            stroke_width=0,
        )
        # Group the background and the table so they appear together
        table_group = VGroup(bg_rect, main_5)

        # --------------------------------------------------------------------
        # 2. Animations
        # --------------------------------------------------------------------
        # (a) Write the title – 1.5 s
        self.play(Write(title_5), run_time=1.5)

        # (b) Grow the table from its centre – 2.5 s
        self.play(GrowFromCenter(table_group), run_time=2.5)

        # (c) Highlight the eigenvector cell of the second example – 1.0 s
        # Row index 2 (third row), column index 1 (second column)
        eigen_cell = main_5.get_cell((2, 1))
        self.play(Indicate(eigen_cell, color=YELLOW, scale_factor=1.3), run_time=1.0)

        # --------------------------------------------------------------------
        # 3. End – wait the remaining time so the whole scene lasts 6 s
        # --------------------------------------------------------------------
        self.wait(1.0)  # 1.5 + 2.5 + 1.0 + 1.0 = 6.0 seconds total
