import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: What is a wave: frequency, wavelength, and propagation ---
        self.clear()
        self.camera.background_color = "#181825"

        # Color palette from style guidelines
        BLUE = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        WHITE = "#FFFFFF"

        # Title at the top
        title = Text(
            "What is a wave: frequency, wavelength, and propagation",
            font_size=36,
            color=WHITE,
        )
        title.move_to(UP * 3)

        # Axes for the wave (positioned slightly below center)
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=3.5,
            axis_config={
                "stroke_width": 2,
                "color": WHITE,
                "include_tip": True,
            },
            x_axis_config={
                "numbers_to_include": [0, 2, 4, 6, 8, 10],
                "color": WHITE,
            },
        )
        axes.move_to(DOWN * 0.5)

        # Wave function (sine wave)
        wave = axes.plot(lambda x: 1.5 * np.sin(x), color=BLUE, stroke_width=3)

        # Wavelength brace (full cycle from 0 to 2π)
        wave_start = axes.c2p(0, 0)
        wave_end = axes.c2p(2 * PI, 0)
        wavelength_brace = BraceBetweenPoints(wave_start, wave_end, direction=DOWN)

        # FIX: Use MathTex directly instead of brace.get_text() which fails on Unicode
        wavelength_label = MathTex(r"\lambda", font_size=28, color=PEACH)
        wavelength_brace.put_at_tip(wavelength_label)

        # Frequency dots (peaks representing cycles)
        freq_group = VGroup()
        for x in [PI / 2, 5 * PI / 2, 9 * PI / 2]:
            dot = Dot(axes.c2p(x, 0), color=PINK, radius=0.08)
            freq_group.add(dot)

        # Frequency label
        freq_text = Text("Frequency = cycles/second", font_size=28, color=PINK)
        freq_text.next_to(freq_group, UP, buff=0.5)

        # Wave speed formula
        speed_text = MathTex(r"v = f 	imes \lambda", font_size=32, color=GREEN)
        speed_text.to_edge(DOWN, buff=0.8)

        # --- Animation Sequence (Total: 6.0 seconds) ---
        # Step 1: Write the title (0.0s - 1.5s)
        self.play(Write(title), run_time=1.5)

        # Step 2: Create the axes (1.5s - 2.5s)
        self.play(Create(axes), run_time=1.0)

        # Step 3: Draw the sine wave (2.5s - 4.0s)
        self.play(Create(wave), run_time=1.5)

        # Step 4: Show wavelength brace and label (4.0s - 5.0s)
        self.play(
            GrowFromCenter(wavelength_brace), FadeIn(wavelength_label), run_time=1.0
        )

        # Step 5: Show frequency dots, label, and speed formula (5.0s - 6.0s)
        self.play(
            LaggedStart(*[FadeIn(dot) for dot in freq_group], lag_ratio=0.3),
            FadeIn(freq_text),
            FadeIn(speed_text),
            run_time=1.0,
        )

        # Final hold to ensure exact 6.0 second duration
        self.wait(0.5)
        # --- Scene 2: Step 2: Stationary source and observer ---
        self.clear()

        # Set the background color
        self.camera.background_color = "#181825"

        # Colors from palette
        PEACH = "#fab387"
        PINK = "#f38ba8"
        BLUE = "#89b4fa"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"

        # ===== TITLE =====
        title = Text("Stationary source and observer", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)

        # ===== AXES =====
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=6,
            axis_config={
                "color": PEACH,
                "stroke_width": 2,
            },
        )

        # ===== SOURCE & OBSERVER =====
        # Place them at axis positions for perfect alignment
        source_pos = axes.c2p(-1.5, 0)
        observer_pos = axes.c2p(1.5, 0)

        # Source dot (pink)
        source_dot = Dot(point=source_pos, radius=0.12, color=PINK)
        source_label = Text("Source", font_size=24, color=PINK)
        source_label.next_to(source_dot, UP, buff=0.15)

        # Observer dot (blue)
        observer_dot = Dot(point=observer_pos, radius=0.12, color=BLUE)
        observer_label = Text("Observer", font_size=24, color=BLUE)
        observer_label.next_to(observer_dot, UP, buff=0.15)

        # ===== WAVEFRONTS (Concentric circles around source) =====
        # These represent sound/radio waves emitted at regular intervals
        wavefronts = VGroup()
        max_radius = 2.5
        num_waves = 5
        for i in range(1, num_waves + 1):
            radius = 0.5 * i
            if radius <= max_radius:
                circle = Circle(
                    radius=radius,
                    color=GREEN,
                    stroke_width=1.5,
                    stroke_opacity=0.6 - (i - 1) * 0.05,
                )
                circle.move_to(source_pos)
                wavefronts.add(circle)

        # ===== FREQUENCY LABELS =====
        # True frequency label
        freq_text = Text("True frequency", font_size=28, color=GREEN)
        freq_text.next_to(source_dot, DOWN, buff=0.5)

        # ===== ARROW SHOWING WAVE DIRECTION =====
        # From source to observer
        arrow = Arrow(
            start=axes.c2p(-0.5, 0),
            end=axes.c2p(0.5, 0),
            color=TEAL,
            buff=0.1,
            tip_length=0.2,
        )

        # ===== ANIMATION SEQUENCE =====
        # Total: 6.0 seconds

        # 1. Show title (1.0s)
        self.play(Write(title), run_time=1.0)

        # 2. Build the axes (1.5s)
        self.play(Create(axes), run_time=1.5)

        # 3. Grow the source and observer from center (1.0s)
        self.play(
            GrowFromCenter(source_dot),
            GrowFromCenter(observer_dot),
            FadeIn(source_label),
            FadeIn(observer_label),
            run_time=1.0,
        )

        # 4. Expand wavefronts outward (1.5s)
        self.play(
            LaggedStart(*[GrowFromCenter(wave) for wave in wavefronts], lag_ratio=0.3),
            run_time=1.5,
        )

        # 5. Show direction arrow and frequency label (1.0s)
        self.play(FadeIn(arrow), FadeIn(freq_text), run_time=1.0)

        # Total duration: 1.0 + 1.5 + 1.0 + 1.5 + 1.0 = 6.0 seconds
        # --- Scene 3: Step 3: Source moving toward observer ---
        # --- Scene 3: Step 3: Source moving toward observer ---
        self.camera.background_color = "#181825"

        # Color constants from the workflow palette
        SAPPHIRE = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"

        # ============================================================
        # 1. Objects
        # ============================================================

        # Title
        title = Text("Source moving toward observer", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.8)

        # Central NumberLine (the "highway" of the Doppler story)
        main_3 = NumberLine(
            x_range=[-5, 5, 1], length=10, color=PINK, include_numbers=True
        )
        main_3.shift(DOWN * 1.5)

        # Observer marker on the positive side
        observer = Dot(main_3.number_to_point(3), color=GREEN, radius=0.12)
        observer_label = Text("Observer", font_size=20, color=GREEN)
        observer_label.next_to(observer, UP)

        # Wave source marker starts on the left, moving toward observer
        source = Dot(main_3.number_to_point(0), color=PEACH, radius=0.12)
        source_label = Text("Source", font_size=20, color=PEACH)
        source_label.next_to(source, UP)

        # Compression annotation
        compression = Text(
            "Wavefronts compress → higher frequency", font_size=24, color=TEAL
        )
        compression.to_edge(DOWN, buff=0.8)

        # ============================================================
        # 2. Animations (Write, FadeIn, GrowFromCenter)
        #    Total planned run_time = 6.0 s
        # ============================================================

        self.play(Write(title), run_time=1.5)
        self.play(GrowFromCenter(main_3), run_time=1.5)

        self.play(
            FadeIn(observer, scale=1.5),
            FadeIn(observer_label, shift=UP * 0.2),
            run_time=0.8,
        )

        self.play(
            FadeIn(source, scale=1.5),
            FadeIn(source_label, shift=UP * 0.2),
            run_time=0.8,
        )

        self.play(Write(compression), run_time=1.4)

        # ============================================================
        # 3. Final hold (must be > 0 for Manim)
        # ============================================================
        self.wait(0.1)
        # --- Scene 4: Step 4: Source moving away from observer ---
        self.clear()
        # 1. Scene setup ---------------------------------------------------------
        self.camera.background_color = "#181825"

        COLORS = ["#89b4fa", "#fab387", "#f38ba8", "#a6e3a1", "#94e2d5"]

        # Title
        title = Text("Source moving away from observer", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # Number-line axis
        axis = NumberLine(
            x_range=[-7, 7],
            length=14,
            include_tip=True,
            tip_width=0.25,
            tip_height=0.25,
        )
        axis.set_color(COLORS[0])

        # Observer (left side)
        observer = Dot(radius=0.12, color=COLORS[2])
        observer.move_to(axis.n2p(-5))
        observer_label = Text("Observer", font_size=24, color=COLORS[2])
        observer_label.next_to(observer, UP, buff=0.2)

        # Source (starts right-of-centre, moving farther right)
        source = Star(n=5, outer_radius=0.3, inner_radius=0.12, color=COLORS[1])
        source_label = Text("Source", font_size=24, color=COLORS[1])
        source.move_to(axis.n2p(1.5))
        source_label.next_to(source, UP, buff=0.2)

        # Wavefronts emitted at successive instants while source was moving right
        wf1 = Circle(radius=1.2, stroke_width=2.5, color=COLORS[3])
        wf2 = Circle(radius=0.8, stroke_width=2.5, color=COLORS[3])
        wf3 = Circle(radius=0.4, stroke_width=2.5, color=COLORS[3])
        wf4 = Circle(radius=0.05, stroke_width=2.5, color=COLORS[3])

        wf1.move_to(axis.n2p(-1.0))
        wf2.move_to(axis.n2p(0.0))
        wf3.move_to(axis.n2p(0.75))
        wf4.move_to(axis.n2p(1.5))

        # Annotation at bottom
        annotation = Text("Spread out → lower frequency", font_size=30, color=COLORS[4])
        annotation.move_to(DOWN * 2.5)

        # Build the main VGroup (requested object)
        main_group = VGroup(
            axis,
            observer,
            observer_label,
            source,
            source_label,
            wf1,
            wf2,
            wf3,
            wf4,
            annotation,
        )

        # 2. Animations -----------------------------------------------------------
        self.play(Write(title), run_time=1.5)
        self.play(GrowFromCenter(axis), run_time=1.0)
        self.play(FadeIn(observer, observer_label), run_time=0.8)
        self.play(FadeIn(source, source_label), run_time=0.8)
        self.play(
            FadeIn(wf1, scale=0.8),
            FadeIn(wf2, scale=0.8),
            FadeIn(wf3, scale=0.8),
            run_time=1.0,
        )
        self.play(FadeIn(wf4), run_time=0.4)

        # Wavefronts expand while source moves farther right
        self.play(
            wf1.animate.scale(1.3),
            wf2.animate.scale(1.8),
            wf3.animate.scale(2.5),
            wf4.animate.scale(4.0),
            source.animate.move_to(axis.n2p(3.5)),
            source_label.animate.next_to(axis.n2p(3.5), UP, buff=0.2),
            run_time=1.5,
        )

        # Bottom annotation
        self.play(Write(annotation), run_time=1.0)

        # 3. Duration pad ---------------------------------------------------------
        self.wait(1.54)
        # --- Scene 5: Step 5: Observer moving toward stationary source ---
        self.clear()
        self.camera.background_color = "#181825"

        # ============================================================
        # 1. Title
        # ============================================================
        title = Text(
            "Observer moving toward stationary source", font_size=36, color=WHITE
        )
        title.to_edge(UP, buff=0.5)

        # ============================================================
        # 2. Supporting Visual Metaphor (Wavefronts + Moving Observer)
        # ============================================================
        # Stationary source (speaker) emitting wavefronts
        source = Dot(point=LEFT * 4.5, color="#fab387", radius=0.15)
        source_label = Text("Source", font_size=24, color="#fab387")
        source_label.next_to(source, DOWN, buff=0.2)

        # Concentric wavefront arcs emanating from source (stationary)
        wavefronts = VGroup()
        for i, radius in enumerate([1.0, 1.8, 2.6, 3.4]):
            arc = Arc(
                radius=radius,
                start_angle=-PI / 3,
                angle=2 * PI / 3,
                color="#89b4fa",
                stroke_width=2,
            )
            arc.shift(LEFT * 4.5)
            wavefronts.add(arc)

        # Observer moving toward source (right to left)
        observer = Dot(point=RIGHT * 4.5, color="#a6e3a1", radius=0.15)
        observer_label = Text("Observer", font_size=24, color="#a6e3a1")
        observer_label.next_to(observer, UP, buff=0.2)

        # Direction arrow showing observer moving toward source
        obs_arrow = Arrow(
            start=RIGHT * 3.2,
            end=RIGHT * 1.8,
            color="#a6e3a1",
            stroke_width=3,
            tip_length=0.2,
        )

        # ============================================================
        # 3. Key Explanation Table (Centered in lower half)
        # ============================================================
        table_data = [
            ["Variable", "Effect"],
            ["Observer speed", "Toward source"],
            ["Distance to wavefronts", "Shortens"],
            ["Crest arrival rate", "Increases (↑)"],
            ["Perceived frequency", "Higher (↑)"],
            ["Perceived pitch", "Higher (↑)"],
        ]

        table = Table(
            table_data,
            v_buff=0.25,
            h_buff=0.4,
            line_config={"stroke_width": 1, "color": "#94e2d5"},
        )
        # Style the header row — FIX: use get_rows() instead of get_row()
        for entry in table.get_rows()[0]:
            entry.set_color("#f38ba8")
            entry.set_weight(BOLD)
        # Color the data cells for emphasis
        for entry in table.get_rows()[3]:
            entry.set_color("#89b4fa")
        for entry in table.get_rows()[4]:
            entry.set_color("#89b4fa")
        for entry in table.get_rows()[5]:
            entry.set_color("#a6e3a1")

        table.next_to(title, DOWN, buff=0.8)
        table.scale(0.75)

        # ============================================================
        # 4. Bottom Summary Label
        # ============================================================
        summary = Text(
            "Crests arrive more frequently → perceived pitch rises",
            font_size=26,
            color="#f38ba8",
        )
        summary.to_edge(DOWN, buff=0.4)

        # ============================================================
        # 5. Assemble and Animate
        # ============================================================
        # Phase 1: Fade in title (0 - 1.2s)
        self.play(Write(title), run_time=1.2)

        # Phase 2: Grow wavefronts + fade in source/observer visuals (1.2 - 3.2s)
        self.play(
            FadeIn(source, scale=0.8),
            FadeIn(source_label),
            LaggedStart(*[GrowFromCenter(arc) for arc in wavefronts], lag_ratio=0.2),
            FadeIn(observer, scale=0.8),
            FadeIn(observer_label),
            FadeIn(obs_arrow),
            run_time=2.0,
        )

        # Phase 3: Build the table (3.2 - 5.0s)
        self.play(GrowFromCenter(table), run_time=1.8)

        # Phase 4: Reveal summary (5.0 - 5.8s)
        self.play(Write(summary), run_time=0.8)

        # Phase 5: Final comprehension pause (5.8 - 6.0s)
        self.wait(0.2)
        # --- Scene 6: Step 6: Relative velocity and observed frequency formula ---
        self.camera.background_color = "#181825"

        # ── 1. Title ────────────────────────────────────────────
        title = Text(
            "Relative velocity and observed frequency formula",
            font_size=36,
            color="#cdd6f4",
        ).shift(UP * 3)
        self.play(Write(title), run_time=1.0)

        # ── 2. Visual metaphor: Observer & Source approaching ─
        observer = Dot(LEFT * 4, color="#89b4fa", radius=0.15)
        source = Dot(RIGHT * 4, color="#f38ba8", radius=0.15)

        v_observer = Arrow(
            observer.get_center() + LEFT * 0.3,
            observer.get_center() + RIGHT * 1.5,
            color="#89b4fa",
            buff=0,
        )
        v_source = Arrow(
            source.get_center() + RIGHT * 0.3,
            source.get_center() + LEFT * 1.5,
            color="#f38ba8",
            buff=0,
        )

        obs_text = MathTex(r"v_{	ext{obs}}", color="#89b4fa").next_to(
            v_observer, UP, buff=0.1
        )
        src_text = MathTex(r"v_{	ext{src}}", color="#f38ba8").next_to(
            v_source, UP, buff=0.1
        )

        self.play(
            FadeIn(observer, source),
            GrowFromCenter(v_observer),
            GrowFromCenter(v_source),
            Write(obs_text),
            Write(src_text),
            run_time=1.0,
        )

        # ── 3. Main Arrow (requested in storyboard) ─────────────
        main_arrow = Arrow(LEFT * 1.2, RIGHT * 1.2, color="#cdd6f4", buff=0.1)
        self.play(GrowFromCenter(main_arrow), run_time=0.5)

        # ── 4. Doppler formula with color-coding ────────────────
        formula = MathTex(
            r"f' = f \cdot \frac{v + v_{	ext{obs}}}{v - v_{	ext{src}}}",
            font_size=42,
            color="#cdd6f4",
        ).shift(DOWN * 1.8)

        formula.set_color_by_tex(r"f'", "#94e2d5")
        formula.set_color_by_tex(r"f", "#fab387")
        formula.set_color_by_tex(r"v_{	ext{obs}}", "#89b4fa")
        formula.set_color_by_tex(r"v_{	ext{src}}", "#f38ba8")

        self.play(Write(formula), run_time=1.0)

        # ── 5. Supporting label with arrow ─────────────────────
        note = Text(
            "Motion toward each other increases f'", font_size=24, color="#a6e3a1"
        ).next_to(formula, DOWN, buff=0.5)

        note_arrow = Arrow(
            formula.get_bottom(), note.get_top(), color="#a6e3a1", buff=0.15
        )
        self.play(FadeIn(note), GrowFromCenter(note_arrow), run_time=0.5)

        # ── 6. Final hold ──────────────────────────────────────
        self.wait(2.0)
        # --- Scene 7: Step 7: Electromagnetic waves: redshift and blueshift ---
        self.camera.background_color = "#181825"

        # Colors from palette
        blue = "#89b4fa"
        pink = "#f38ba8"

        # ======== 1. TITLE ========
        title = Text(
            "Electromagnetic waves: redshift and blueshift", font_size=36, color=WHITE
        )
        title.to_edge(UP, buff=0.5)

        # ======== 2. VISUALIZING WAVES ========

        # Create axes for both wave diagrams
        axes_left = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=5.5,
            y_length=2.0,
            axis_config={"color": GREY_D, "stroke_width": 1.5},
            tips=False,
        )
        axes_left.to_edge(LEFT, buff=0.3).shift(DOWN * 0.5)

        axes_right = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=5.5,
            y_length=2.0,
            axis_config={"color": GREY_D, "stroke_width": 1.5},
            tips=False,
        )
        axes_right.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)

        # REDSHIFT WAVE (stretched, lower frequency, moving away)
        wave_red = axes_left.plot(
            lambda x: 0.8 * np.sin(0.8 * x), color=pink, stroke_width=3
        )

        # BLUESHIFT WAVE (compressed, higher frequency, moving closer)
        wave_blue = axes_right.plot(
            lambda x: 0.8 * np.sin(1.6 * x), color=blue, stroke_width=3
        )

        # Add wavelength visual indicators (braces)
        brace_red = Brace(
            Line(axes_left.c2p(-2 * PI / 0.8, 0), axes_left.c2p(0, 0)),
            direction=UP,
            color=pink,
        )
        brace_red_label = MathTex(r"\lambda_{max}", color=pink, font_size=30)
        brace_red_label.next_to(brace_red, UP, buff=0.2)

        brace_blue = Brace(
            Line(axes_right.c2p(-PI / 0.8, 0), axes_right.c2p(0, 0)),
            direction=UP,
            color=blue,
        )
        brace_blue_label = MathTex(r"\lambda_{min}", color=blue, font_size=30)
        brace_blue_label.next_to(brace_blue, UP, buff=0.2)

        # Labels for each side
        redshift_label = Text("REDSHIFT", font_size=28, color=pink)
        redshift_label.move_to(axes_left.get_top() + UP * 0.8)

        blueshift_label = Text("BLUESHIFT", font_size=28, color=blue)
        blueshift_label.move_to(axes_right.get_top() + UP * 0.8)

        # Description texts
        red_desc = Text("Moving away", font_size=24, color=GREY_B)
        red_desc.next_to(axes_left, DOWN, buff=0.4)

        blue_desc = Text("Moving closer", font_size=24, color=GREY_B)
        blue_desc.next_to(axes_right, DOWN, buff=0.4)

        # Arrows indicating motion direction
        red_arrow = Arrow(
            start=axes_left.get_center() + DOWN * 1.8,
            end=axes_left.get_center() + LEFT * 2 + DOWN * 1.8,
            color=pink,
            buff=0.1,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )

        blue_arrow = Arrow(
            start=axes_right.get_center() + DOWN * 1.8,
            end=axes_right.get_center() + RIGHT * 2 + DOWN * 1.8,
            color=blue,
            buff=0.1,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )

        # ======== 3. ANIMATIONS ========

        # Title
        self.play(Write(title), run_time=0.8)
        self.wait(0.2)

        # Left side (redshift)
        self.play(FadeIn(axes_left), run_time=0.5)
        self.play(Create(wave_red), run_time=0.7)
        self.play(
            FadeIn(redshift_label), FadeIn(red_desc), FadeIn(red_arrow), run_time=0.4
        )
        self.play(GrowFromCenter(brace_red), FadeIn(brace_red_label), run_time=0.4)
        self.wait(0.2)

        # Right side (blueshift)
        self.play(FadeIn(axes_right), run_time=0.5)
        self.play(Create(wave_blue), run_time=0.7)
        self.play(
            FadeIn(blueshift_label), FadeIn(blue_desc), FadeIn(blue_arrow), run_time=0.4
        )
        self.play(GrowFromCenter(brace_blue), FadeIn(brace_blue_label), run_time=0.4)
        self.wait(0.2)

        # Final highlights
        red_highlight = SurroundingRectangle(
            VGroup(axes_left, wave_red, redshift_label, red_desc, red_arrow),
            color=pink,
            buff=0.15,
            stroke_width=2,
        )
        blue_highlight = SurroundingRectangle(
            VGroup(axes_right, wave_blue, blueshift_label, blue_desc, blue_arrow),
            color=blue,
            buff=0.15,
            stroke_width=2,
        )
        self.play(
            FadeIn(red_highlight, scale=0.95),
            FadeIn(blue_highlight, scale=0.95),
            run_time=0.5,
        )
        self.wait(0.1)
        # --- Scene 8: Step 8: Real-world applications of the Doppler effect ---
        self.camera.background_color = "#181825"

        # Palette from style guidelines
        palette = ["#89b4fa", "#fab387", "#f38ba8", "#a6e3a1", "#94e2d5"]

        # 1. Axes (main object)
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=6,
            axis_config={
                "color": palette[1],
                "stroke_width": 2.0,
                "include_tip": True,
            },
        )

        # 2. Title
        title = Text(
            "Real-world applications of the Doppler effect",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # 3. Application texts placed around the axes
        radar = Text(
            "Speed radar measures frequency shift\nto calculate vehicle velocity",
            font_size=22,
            color=palette[0],
        ).move_to(LEFT * 3 + UP * 0.8)

        ultrasound = Text(
            "Medical ultrasound uses Doppler\nto monitor blood flow",
            font_size=22,
            color=palette[3],
        ).move_to(ORIGIN + UP * 1.2)

        galaxy = Text(
            "Redshift of galaxies reveals\nexpansion of the universe",
            font_size=22,
            color=palette[2],
        ).move_to(RIGHT * 3 + UP * 0.8)

        # 4. Underlying wave plots signifying signals in each domain
        wave1 = axes.plot(
            lambda x: 0.7 * np.sin(4 * x), color=palette[0], x_range=[-2.8, -0.5]
        )
        wave2 = axes.plot(
            lambda x: 0.5 * np.sin(3 * x + 1), color=palette[4], x_range=[-1.2, 1.2]
        )
        wave3 = axes.plot(
            lambda x: 0.6 * np.sin(2.5 * x + 0.5), color=palette[2], x_range=[0.5, 2.8]
        )

        # 5. Bright dots on the waves
        dot1 = Dot(
            axes.c2p(-1.6, 0.7 * np.sin(4 * (-1.6))), color=palette[0], radius=0.08
        )
        dot2 = Dot(
            axes.c2p(0.0, 0.5 * np.sin(3 * 0.0 + 1)), color=palette[3], radius=0.08
        )
        dot3 = Dot(
            axes.c2p(1.6, 0.6 * np.sin(2.5 * 1.6 + 0.5)), color=palette[2], radius=0.08
        )

        # ── Animations ─────────────────────────────────────
        self.play(Write(title), run_time=1.5)
        self.play(Create(axes), run_time=1.5)
        self.play(
            FadeIn(radar, shift=UP),
            FadeIn(ultrasound, shift=UP),
            FadeIn(galaxy, shift=UP),
            run_time=1.0,
        )
        self.play(
            GrowFromCenter(dot1),
            GrowFromCenter(dot2),
            GrowFromCenter(dot3),
            run_time=0.75,
        )
        self.play(
            Create(wave1),
            Create(wave2),
            Create(wave3),
            run_time=1.25,
        )
        self.wait(1.0)
        # Total = 1.5 + 1.5 + 1.0 + 0.75 + 1.25 + 1.0 = 6.0 seconds
