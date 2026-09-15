import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Waves have a source, a medium, and an observer ---
        self.camera.background_color = "#181825"

        # --- Title and main statement ---
        title_1 = Text(
            "Waves have a source, a medium, and an observer", font_size=36, color=WHITE
        )
        title_1.move_to(UP * 3)

        main_1 = Text(
            "Source \u2192 Medium \u2192 Observer", font_size=48, color="#89b4fa"
        )
        main_1.move_to(UP * 1.5)

        # --- Source: filled core with concentric emission arcs ---
        source = VGroup(
            Circle(
                radius=0.25,
                color="#f38ba8",
                fill_color="#f38ba8",
                fill_opacity=1.0,
                stroke_width=2.0,
            ),
            Arc(
                radius=0.5, start_angle=0, angle=TAU, color="#f38ba8", stroke_width=2.0
            ),
            Arc(
                radius=0.75, start_angle=0, angle=TAU, color="#f38ba8", stroke_width=2.0
            ),
            Arc(
                radius=1.0, start_angle=0, angle=TAU, color="#f38ba8", stroke_width=2.0
            ),
        )
        source.move_to(LEFT * 4 + DOWN * 1)
        source_label = Text("Source", font_size=28, color="#f38ba8")
        source_label.next_to(source, DOWN, buff=0.3)
        source_group = VGroup(source, source_label)

        # --- Medium: staggered grid of particles ---
        medium_dots = VGroup()
        for row in range(3):
            for col in range(5):
                dot = Dot(radius=0.08, color="#fab387")
                dot.move_to(
                    LEFT * 1.2
                    + RIGHT * (col * 0.6)
                    + UP * 0.4
                    + DOWN * (row * 0.4)
                    + RIGHT * (0.3 * (row % 2))
                    + DOWN * 1
                )
                medium_dots.add(dot)
        medium_label = Text("Medium", font_size=28, color="#fab387")
        medium_label.next_to(medium_dots, DOWN, buff=0.4)
        medium_group = VGroup(medium_dots, medium_label)

        # --- Observer: stylized eye ---
        eye = VGroup(
            Ellipse(width=1.4, height=0.8, color="#94e2d5", stroke_width=2.0),
            Circle(
                radius=0.2,
                color="#94e2d5",
                fill_color="#94e2d5",
                fill_opacity=1.0,
                stroke_width=2.0,
            ),
        )
        eye.move_to(RIGHT * 4 + DOWN * 1)
        observer_label = Text("Observer", font_size=28, color="#94e2d5")
        observer_label.next_to(eye, DOWN, buff=0.3)
        observer_group = VGroup(eye, observer_label)

        # --- Connecting arrows ---
        arrow_1 = Arrow(
            source.get_right() + RIGHT * 0.1,
            medium_dots.get_left() + LEFT * 0.1,
            buff=0.1,
            stroke_width=2.0,
            color=WHITE,
        )
        arrow_2 = Arrow(
            medium_dots.get_right() + RIGHT * 0.1,
            eye.get_left() + LEFT * 0.1,
            buff=0.1,
            stroke_width=2.0,
            color=WHITE,
        )

        # --- Animations (total 7.0s) ---
        self.play(Write(title_1), run_time=1.0)
        self.play(GrowFromCenter(main_1), run_time=1.0)
        self.play(
            LaggedStart(
                FadeIn(source_group, shift=RIGHT * 0.5),
                FadeIn(medium_group, shift=RIGHT * 0.5),
                FadeIn(observer_group, shift=RIGHT * 0.5),
                lag_ratio=0.3,
            ),
            run_time=1.5,
        )
        self.play(Create(arrow_1), Create(arrow_2), run_time=1.0)
        self.play(
            ScaleInPlace(source, 1.15),
            medium_dots.animate(rate_func=there_and_back, run_time=1.0).shift(
                RIGHT * 0.15
            ),
            run_time=1.0,
        )
        self.wait(1.5)
        # --- Scene 2: Step 2: Frequency and wavelength define a wave ---
        self.clear()
        # --- Scene 2: Step 2: Frequency and wavelength define a wave ---
        AX_COL = "#fab387"
        WAVE_COL = "#89b4fa"
        CREST_COL = "#f38ba8"
        LAMBDA_COL = "#a6e3a1"
        BG_COL = "#181825"

        self.camera.background_color = BG_COL

        # Title
        title = Text(
            "Frequency and wavelength define a wave",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # Axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=3.5,
            axis_config={"color": AX_COL, "stroke_width": 2.0},
        ).move_to(ORIGIN + DOWN * 0.2)

        # The wave: y = sin(2*pi*x), wavelength = 1 unit, about 5 cycles
        wave = axes.plot(
            lambda x: 1.3 * np.sin(2 * PI * x),
            x_range=[-2.5, 2.5],
            color=WAVE_COL,
            stroke_width=4,
        )

        # Frequency label
        freq_label = MathTex(
            r"f = \frac{\mathrm{crests}}{\mathrm{second}}",
            font_size=36,
            color=CREST_COL,
        )
        freq_label.next_to(axes, LEFT, buff=0.5).shift(UP * 1.7)

        # Wavelength brace between two adjacent crests (x = 0.25 and 1.25)
        crest_a = axes.c2p(0.25, 1.3)
        crest_b = axes.c2p(1.25, 1.3)
        wl_brace = BraceBetweenPoints(crest_a, crest_b, UP, color=LAMBDA_COL)
        wl_label = MathTex(r"\lambda", font_size=42, color=LAMBDA_COL)
        wl_label.next_to(wl_brace, UP, buff=0.1)

        # Speed relation
        speed_eq = MathTex(r"v = f \lambda", font_size=44, color=WHITE)
        speed_eq.next_to(axes, DOWN, buff=0.7)

        # Build the scene
        self.play(Write(title), run_time=1.2)
        self.play(GrowFromCenter(axes), run_time=1.0)
        self.play(Create(wave), run_time=1.5)

        # Frequency: dots marking successive crests
        crest_points = VGroup(
            *[
                Dot(axes.c2p(x, 1.3 * np.sin(2 * PI * x)), radius=0.07, color=CREST_COL)
                for x in np.linspace(-2.25, 2.25, 6)
            ]
        )
        self.play(
            FadeIn(crest_points, lag_ratio=0.2),
            Write(freq_label),
            run_time=1.5,
        )

        # Wavelength
        self.play(GrowFromCenter(wl_brace), Write(wl_label), run_time=1.2)

        # Wave speed equation with highlight
        self.play(Write(speed_eq), run_time=1.0)
        self.play(Circumscribe(speed_eq, color=YELLOW), run_time=1.0)
        self.wait(0.5)
        # --- Scene 3: Step 3: A stationary source emits evenly spaced wavefronts ---
        self.clear()
        self.camera.background_color = "#181825"

        C_PINK = "#f38ba8"
        C_BLUE = "#89b4fa"
        C_PEACH = "#fab387"
        C_GREEN = "#a6e3a1"

        # Title
        title = Text(
            "A stationary source emits evenly spaced wavefronts",
            font_size=36,
            color=WHITE,
        )
        title.move_to(UP * 3)
        self.play(Write(title), run_time=1.2)

        # NumberLine at bottom
        numline = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            include_numbers=True,
            color=C_PINK,
            stroke_width=2.0,
        )
        numline.move_to(DOWN * 2.5)
        self.play(Create(numline), run_time=1.0)

        # Source at origin
        source = Dot(ORIGIN, radius=0.12, color=C_PEACH)
        source_label = Text("source", font_size=24, color=C_PEACH).next_to(
            source, UP, buff=0.15
        )
        self.play(FadeIn(source, scale=0.5), GrowFromCenter(source_label), run_time=0.8)

        # Concentric wavefronts (perfectly even spacing = wavelength)
        wavefronts = VGroup(
            Circle(radius=1.0, color=C_BLUE, stroke_width=2.0),
            Circle(radius=2.0, color=C_BLUE, stroke_width=2.0),
            Circle(radius=3.0, color=C_GREEN, stroke_width=2.0),
            Circle(radius=4.0, color=C_GREEN, stroke_width=2.0),
        )
        self.play(
            LaggedStart(*[Create(c) for c in wavefronts], lag_ratio=0.3), run_time=1.5
        )

        # Wavelength brace showing even spacing along the baseline
        brace1 = BraceBetweenPoints(
            ORIGIN + RIGHT * 1.0 + DOWN * 3.4,
            ORIGIN + RIGHT * 2.0 + DOWN * 3.4,
        )
        wl_text = MathTex(r"\lambda", font_size=34, color=C_GREEN)
        brace1.put_at_tip(wl_text)

        self.play(
            FadeIn(brace1),
            GrowFromCenter(wl_text),
            run_time=0.5,
        )

        # Highlight the evenly spaced wavefronts
        self.play(
            Indicate(wavefronts, color=C_PEACH, scale_factor=1.05),
            run_time=0.5,
        )

        self.wait(0.5)
        # --- Scene 4: Step 4: A moving source compresses waves ahead and stretches them behind ---
        self.camera.background_color = "#181825"

        # Title
        title_4 = Text(
            "A moving source compresses waves ahead and stretches them behind",
            font_size=36,
            color=WHITE,
        )
        title_4.move_to(UP * 3)
        if title_4.width > 12:
            title_4.scale_to_fit_width(12)
        self.play(Write(title_4), run_time=1.0)

        # Source: glowing orange dot at the origin
        source = VGroup(
            Circle(
                radius=0.22,
                color="#fab387",
                fill_color="#fab387",
                fill_opacity=0.35,
                stroke_width=2.0,
            ),
            Dot(point=ORIGIN, radius=0.08, color="#fab387"),
        )
        self.play(FadeIn(source, scale=0.6), run_time=0.5)

        # Stationary source: symmetric concentric wavefronts
        radii = [0.35, 0.9, 1.45, 2.0]
        main_4 = VGroup(
            *[
                Circle(radius=r, color="#a6e3a1", stroke_width=2.0).move_to(ORIGIN)
                for r in radii
            ]
        )
        self.play(
            LaggedStart(*[GrowFromCenter(c) for c in main_4], lag_ratio=0.2),
            run_time=1.5,
        )
        self.wait(0.5)

        # Motion cue above the source
        motion_arrow = Arrow(
            start=ORIGIN,
            end=RIGHT * 0.9,
            buff=0.0,
            tip_length=0.18,
            stroke_width=3,
            color="#fab387",
        )
        motion_text = Text("motion", font_size=24, color="#fab387")
        motion_group = VGroup(motion_arrow, motion_text)
        motion_group.arrange(DOWN, buff=0.15)
        motion_group.next_to(source, UP, buff=0.3)
        self.play(
            GrowFromCenter(motion_arrow),
            FadeIn(motion_text, shift=DOWN * 0.2),
            run_time=0.5,
        )

        # Core move: the source slides right and every wavefront recenters
        # on the point where it was emitted, so the circles bunch together
        # ahead of the motion and spread apart behind it.
        emission_points = [RIGHT * 1.2, RIGHT * 0.8, RIGHT * 0.4, ORIGIN]
        target_circles = VGroup(
            *[
                Circle(radius=r, color="#a6e3a1", stroke_width=2.0).move_to(p)
                for r, p in zip(radii, emission_points)
            ]
        )
        self.play(
            source.animate.shift(RIGHT * 1.2),
            motion_group.animate.shift(RIGHT * 1.2),
            *[
                ReplacementTransform(main_4[i], target_circles[i])
                for i in range(len(radii))
            ],
            run_time=1.5,
        )
        main_4 = target_circles

        # Labels with pointer arrows toward each region
        comp_label = Text("compressed (ahead)", font_size=24, color="#89b4fa")
        comp_label.move_to(RIGHT * 4.7)
        comp_arrow = Arrow(
            start=comp_label.get_left() + LEFT * 0.15,
            end=RIGHT * 2.2,
            buff=0.05,
            tip_length=0.18,
            stroke_width=2.5,
            color="#89b4fa",
        )
        stretch_label = Text("stretched (behind)", font_size=24, color="#f38ba8")
        stretch_label.move_to(LEFT * 4.7)
        stretch_arrow = Arrow(
            start=stretch_label.get_right() + RIGHT * 0.15,
            end=LEFT * 2.3,
            buff=0.05,
            tip_length=0.18,
            stroke_width=2.5,
            color="#f38ba8",
        )
        self.play(
            FadeIn(comp_label, shift=RIGHT * 0.3),
            GrowFromCenter(comp_arrow),
            FadeIn(stretch_label, shift=LEFT * 0.3),
            GrowFromCenter(stretch_arrow),
            run_time=0.5,
        )

        # Highlight the bunched wavefronts ahead of the moving source
        bunch_zone = Rectangle(
            width=0.7, height=1.7, stroke_width=2.0, stroke_opacity=0.0
        )
        bunch_zone.move_to(RIGHT * 1.8)
        self.play(Circumscribe(bunch_zone, color="#89b4fa", buff=0.12), run_time=1.0)

        self.wait(0.5)
        # --- Scene 5: Step 5: Compressed wavefronts mean a higher perceived pitch ---
        self.clear()

        BG = "#181825"
        TEAL = "#94e2d5"
        BLUE = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        TXT = "#CDD6F4"
        SUB = "#A6ADC8"
        GRID = "#45475A"

        self.camera.background_color = BG

        # ---------- Title ----------
        title = Text(
            "Compressed wavefronts mean a higher perceived pitch",
            font_size=36,
            color=WHITE,
        )
        title.move_to(UP * 3)

        # ---------- Small wavefront diagram (above the table) ----------
        source = Dot(point=ORIGIN, radius=0.1, color=PEACH)
        ahead_circles = VGroup(
            *[Circle(radius=r, stroke_width=2.0, color=BLUE) for r in [0.4, 0.7, 1.0]]
        )
        behind_circles = VGroup(
            *[Circle(radius=r, stroke_width=2.0, color=PINK) for r in [0.4, 0.8, 1.2]]
        )
        ahead_circles.next_to(source, RIGHT, buff=0.3)
        behind_circles.next_to(source, LEFT, buff=0.3)
        ahead_circles.stretch_to_fit_height(1.6)
        behind_circles.stretch_to_fit_height(1.6)
        wave_diagram = VGroup(source, ahead_circles, behind_circles)
        wave_diagram.move_to(UP * 1.5)

        front_label = Tex("crests bunched: high $f$", font_size=30, color=BLUE)
        back_label = Tex("crests spread: low $f$", font_size=30, color=PINK)
        front_label.next_to(ahead_circles, RIGHT, buff=0.2)
        back_label.next_to(behind_circles, LEFT, buff=0.2)

        # ---------- Main Table (mobject entries, pass-through converter) ----------
        def _pass_through(item, **kwargs):
            return item

        row_labels = [
            Text("Observer", font_size=28, color=SUB),
            Text("Crest spacing", font_size=28, color=SUB),
            Text("Arrival rate", font_size=28, color=SUB),
            Text("Perceived pitch", font_size=28, color=SUB),
        ]
        col_labels = [
            Text("In front", font_size=28, color=BLUE),
            Text("Behind", font_size=28, color=PINK),
        ]
        hi_front = MathTex(r"f' > f", font_size=30, color=GREEN)
        hi_behind = MathTex(r"f' < f", font_size=30, color=PINK)
        data = [
            [
                Text("Approaching source", font_size=26, color=TXT),
                Text("Receding source", font_size=26, color=TXT),
            ],
            [
                Text("Compressed (tight)", font_size=26, color=TEAL),
                Text("Stretched (wide)", font_size=26, color=TEAL),
            ],
            [
                Text("Crests meet often", font_size=26, color=TEAL),
                Text("Crests meet rarely", font_size=26, color=TEAL),
            ],
            [hi_front, hi_behind],
        ]

        table = Table(
            table=data,
            row_labels=row_labels,
            col_labels=col_labels,
            element_to_mobject=_pass_through,
            include_outer_lines=True,
            line_config={"stroke_width": 2.0, "color": GRID},
        )

        table.scale(0.72)
        table.move_to(DOWN * 1.4)

        # ---------- Animations (total 6.0s) ----------
        self.play(Write(title), run_time=1.2)

        self.play(
            GrowFromCenter(wave_diagram),
            FadeIn(front_label, shift=RIGHT * 0.3),
            FadeIn(back_label, shift=LEFT * 0.3),
            run_time=1.6,
        )

        self.play(GrowFromCenter(table), run_time=2.0)

        self.play(
            Circumscribe(
                VGroup(hi_front, hi_behind),
                shape=Rectangle,
                buff=0.1,
                color=GREEN,
            ),
            run_time=1.2,
        )
        # --- Scene 6: Step 6: Observer motion produces the same effect ---
        self.camera.background_color = "#181825"

        # ---------------- Palette ----------------
        C_TEXT = "#cdd6f4"
        C_BLUE = "#89b4fa"
        C_PEACH = "#fab387"
        C_RED = "#f38ba8"
        C_GREEN = "#a6e3a1"
        C_TEAL = "#94e2d5"

        # ---------------- Title ----------------
        title_6 = Text(
            "Observer motion produces the same effect",
            font="Sans",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # ---------------- Oncoming wave crests ----------------
        crest_xs = [-5.6, -4.4, -3.2, -2.0, -0.8]
        crests = VGroup(
            *[
                Line(UP * 1.5, DOWN * 1.5, color=C_BLUE, stroke_width=3.5).shift(
                    RIGHT * x
                )
                for x in crest_xs
            ]
        )
        crest_label = Text("wave crests", font="Sans", font_size=24, color=C_BLUE)
        crest_label.move_to([-3.2, -1.95, 0])
        sweep_group = VGroup(crests, crest_label)

        # ---------------- Observer (fixed at ORIGIN) ----------------
        observer_dot = Dot(ORIGIN, radius=0.14, color=C_GREEN)
        observer_label = Text("Observer", font="Sans", font_size=24, color=C_GREEN)
        observer_label.next_to(observer_dot, UP, buff=0.28)

        # ---------------- main_6 : observer velocity arrow ----------------
        main_6 = Arrow(
            ORIGIN,
            LEFT * 1.2,
            buff=0,
            stroke_width=6,
            tip_length=0.25,
            color=C_TEXT,
        )

        # ---------------- Outcome column ----------------
        toward_title = Text(
            "toward the crests", font="Sans", font_size=26, color=C_PEACH
        )
        faster_txt = Text("crossing faster", font="Sans", font_size=22, color=C_TEAL)
        up_tri = Triangle().scale(0.13).set_fill(C_RED, 1).set_stroke(width=0)
        higher_txt = Text("higher pitch", font="Sans", font_size=26, color=C_RED)
        higher_row = VGroup(up_tri, higher_txt).arrange(RIGHT, buff=0.18)

        away_title = Text(
            "away from the crests", font="Sans", font_size=26, color=C_PEACH
        )
        slower_txt = Text("crossing slower", font="Sans", font_size=22, color=C_TEAL)
        down_tri = (
            Triangle().scale(0.13).set_fill(C_BLUE, 1).set_stroke(width=0).rotate(PI)
        )
        lower_txt = Text("lower pitch", font="Sans", font_size=26, color=C_BLUE)
        lower_row = VGroup(down_tri, lower_txt).arrange(RIGHT, buff=0.18)

        outcome_col = (
            VGroup(
                toward_title,
                faster_txt,
                higher_row,
                away_title,
                slower_txt,
                lower_row,
            )
            .arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            .move_to(RIGHT * 4.3 + DOWN * 0.1)
        )

        # ---------------- Build-up ----------------
        self.play(Write(title_6), run_time=0.8)

        self.play(
            LaggedStart(*[Create(line) for line in crests], lag_ratio=0.2),
            FadeIn(crest_label),
            run_time=0.8,
        )

        self.play(
            GrowFromCenter(observer_dot),
            FadeIn(observer_label),
            run_time=0.5,
        )

        self.play(Create(main_6), run_time=0.5)

        # ---------------- Phase A : moving TOWARD the crests ----------------
        self.play(FadeIn(toward_title), run_time=0.4)

        self.play(
            sweep_group.animate.shift(RIGHT * 1.4),
            Indicate(observer_dot, scale_factor=1.7, color=C_RED),
            run_time=0.9,
        )

        self.play(
            FadeIn(faster_txt),
            FadeIn(higher_row),
            run_time=0.5,
        )

        # ---------------- Phase B : moving AWAY from the crests ----------------
        self.play(
            Rotate(main_6, angle=PI, about_point=ORIGIN),
            FadeIn(away_title),
            run_time=0.6,
        )

        self.play(sweep_group.animate.shift(RIGHT * 0.4), run_time=0.7)

        self.play(
            FadeIn(slower_txt),
            FadeIn(lower_row),
            run_time=0.4,
        )

        self.wait(0.4)
        # --- Scene 7: Step 7: The Doppler formula quantifies the shift ---
        self.clear()
        self.camera.background_color = "#181825"

        primary_text = "#CDD6F4"
        accent_blue = "#89b4fa"
        accent_orange = "#fab387"
        accent_pink = "#f38ba8"
        accent_green = "#a6e3a1"
        accent_teal = "#94e2d5"

        # Title
        title_7 = Text(
            "The Doppler formula quantifies the shift",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # Main formula (central object at ORIGIN)
        formula = MathTex(
            r"f_{	ext{obs}}",
            r"=",
            r"f_{	ext{src}}",
            r"\cdot",
            r"\frac{v}{v - v_{	ext{src}}}",
            font_size=72,
        ).move_to(ORIGIN + UP * 0.3)
        formula[0].set_color(accent_blue)
        formula[2].set_color(accent_teal)
        formula[4].set_color(accent_orange)

        # Supporting labels
        label_obs = Text(
            "observed frequency",
            font_size=26,
            color=accent_blue,
        ).next_to(formula[0], DOWN, buff=0.6)
        label_src = Text(
            "source frequency",
            font_size=26,
            color=accent_teal,
        ).next_to(formula[2], DOWN, buff=0.6)
        label_ratio = Text(
            "wave speed / (wave speed − source speed)",
            font_size=26,
            color=accent_orange,
        ).next_to(formula[4], DOWN, buff=0.6)

        line_obs = Line(
            formula[0].get_bottom() + DOWN * 0.1,
            label_obs.get_top(),
            stroke_width=2.0,
            color=accent_blue,
            buff=0.05,
        )
        line_src = Line(
            formula[2].get_bottom() + DOWN * 0.1,
            label_src.get_top(),
            stroke_width=2.0,
            color=accent_teal,
            buff=0.05,
        )
        line_ratio = Line(
            formula[4].get_bottom() + DOWN * 0.1,
            label_ratio.get_top(),
            stroke_width=2.0,
            color=accent_orange,
            buff=0.05,
        )

        # Bottom metaphor: source moving toward observer raises the result
        source_dot = Dot(radius=0.12, color=accent_pink)
        observer_dot = Dot(radius=0.12, color=accent_green)
        wave_arc = Arc(
            radius=0.5,
            start_angle=-PI / 3,
            angle=2 * PI / 3,
            color=accent_orange,
            stroke_width=2.0,
        )
        mover = VGroup(source_dot, wave_arc)
        receiver_note = VGroup(
            observer_dot,
            Text("observer", font_size=24, color=accent_green),
        ).arrange(RIGHT, buff=0.15)

        note_layout = VGroup(mover, receiver_note).arrange(RIGHT, buff=2.0)
        note_layout.move_to(DOWN * 2.0)
        motion_arrow = Arrow(
            mover.get_right() + RIGHT * 0.2,
            observer_dot.get_left() + LEFT * 0.2,
            buff=0.1,
            stroke_width=2.0,
            color=accent_pink,
            max_tip_length_to_length_ratio=0.5,
        )
        result_note = MathTex(
            r"f_{	ext{obs}} > f_{	ext{src}}",
            font_size=40,
            color=accent_green,
        ).next_to(note_layout, RIGHT, buff=1.0)

        # Animations (total = 7.5 s)
        self.play(FadeIn(title_7), run_time=1.0)
        self.play(Write(formula), run_time=1.8)
        self.play(
            LaggedStart(
                FadeIn(label_obs, shift=UP * 0.2),
                Create(line_obs),
                FadeIn(label_src, shift=UP * 0.2),
                Create(line_src),
                FadeIn(label_ratio, shift=UP * 0.2),
                Create(line_ratio),
                lag_ratio=0.15,
            ),
            run_time=1.7,
        )
        self.play(
            GrowFromCenter(source_dot),
            Create(wave_arc),
            GrowFromCenter(receiver_note),
            run_time=1.2,
        )
        self.play(
            GrowFromCenter(motion_arrow),
            FadeIn(result_note, shift=RIGHT * 0.3),
            run_time=1.0,
        )
        self.play(
            Circumscribe(result_note, color=accent_green, buff=0.1),
            Indicate(formula[4], color=accent_orange),
            run_time=0.8,
        )
        self.wait(1.0)
        # --- Scene 8: Step 8: The relativistic Doppler effect for light ---
        self.clear()
        self.camera.background_color = "#181825"

        RED_C = "#f38ba8"
        BLUE_C = "#89b4fa"
        PEACH = "#fab387"
        TEAL = "#94e2d5"

        # ---------- Title ----------
        title = Text(
            "The relativistic Doppler effect for light",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # ---------- Central axes (the observer's record of the light) ----------
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=5.5,
            y_length=3.0,
            axis_config={"color": PEACH, "include_ticks": True},
            tips=True,
        )
        axes.set_stroke(width=2.0)

        time_label = Text("time", font_size=20, color=PEACH)
        time_label.next_to(axes, DOWN, buff=0.12)

        # ---------- Waves seen by the observer ----------
        # Receding source -> stretched wave (long wavelength, redder)
        red_wave = axes.plot(
            lambda x: 0.7 + 0.5 * np.sin(0.7 * x),
            x_range=[-3, 3],
            color=RED_C,
        )
        red_wave.set_stroke(width=3)

        # Approaching source -> compressed wave (short wavelength, bluer)
        blue_wave = axes.plot(
            lambda x: -0.7 + 0.5 * np.sin(2.0 * x),
            x_range=[-3, 3],
            color=BLUE_C,
        )
        blue_wave.set_stroke(width=3)

        red_label = MathTex(
            r"\lambda_{\mathrm{obs}} > \lambda_0",
            font_size=30,
            color=RED_C,
        ).move_to(axes.coords_to_point(1.1, 1.7))

        blue_label = MathTex(
            r"\lambda_{\mathrm{obs}} < \lambda_0",
            font_size=30,
            color=BLUE_C,
        ).move_to(axes.coords_to_point(1.1, -1.7))

        # ---------- Relativistic Doppler formula ----------
        formula = MathTex(
            r"f_{\mathrm{obs}} = f_0\,\sqrt{\frac{1-\beta}{1+\beta}}",
            font_size=40,
            color=WHITE,
        ).move_to(DOWN * 2.7)

        caption = Text(
            "light needs no medium — time dilation modifies the shift",
            font_size=22,
            color=TEAL,
        ).move_to(DOWN * 3.6)

        # ---------- Receding source (left): redshift ----------
        left_center = LEFT * 5.2 + UP * 0.3

        left_star = Star(
            n=5,
            outer_radius=0.32,
            color=RED_C,
            fill_opacity=1,
        ).move_to(left_center)

        # Stretched wavefronts heading toward the observer
        left_arcs = VGroup(
            Arc(
                radius=0.6,
                start_angle=-PI / 3,
                angle=2 * PI / 3,
                color=RED_C,
                stroke_width=2.0,
            ),
            Arc(
                radius=1.3,
                start_angle=-PI / 3,
                angle=2 * PI / 3,
                color=RED_C,
                stroke_width=2.0,
            ),
            Arc(
                radius=2.0,
                start_angle=-PI / 3,
                angle=2 * PI / 3,
                color=RED_C,
                stroke_width=2.0,
            ),
        ).shift(left_center)

        # Motion: moving away from the observer at the center
        left_arrow = Arrow(
            start=left_center + UP * 1.3 + LEFT * 0.5,
            end=left_center + UP * 1.3 + LEFT * 1.5,
            color=RED_C,
            stroke_width=3,
            buff=0,
        )

        left_label = Text("redshift (receding)", font_size=22, color=RED_C)
        left_label.next_to(left_star, DOWN, buff=1.1)

        # ---------- Approaching source (right): blueshift ----------
        right_center = RIGHT * 5.2 + UP * 0.3

        right_star = Star(
            n=5,
            outer_radius=0.32,
            color=BLUE_C,
            fill_opacity=1,
        ).move_to(right_center)

        # Compressed wavefronts bunched toward the observer
        right_arcs = VGroup(
            Arc(
                radius=0.5,
                start_angle=2 * PI / 3,
                angle=2 * PI / 3,
                color=BLUE_C,
                stroke_width=2.0,
            ),
            Arc(
                radius=0.95,
                start_angle=2 * PI / 3,
                angle=2 * PI / 3,
                color=BLUE_C,
                stroke_width=2.0,
            ),
            Arc(
                radius=1.4,
                start_angle=2 * PI / 3,
                angle=2 * PI / 3,
                color=BLUE_C,
                stroke_width=2.0,
            ),
        ).shift(right_center)

        # Motion: moving toward the observer at the center
        right_arrow = Arrow(
            start=right_center + RIGHT * 0.5 + UP * 1.3,
            end=right_center - RIGHT * 0.4 + UP * 1.3,
            color=BLUE_C,
            stroke_width=3,
            buff=0,
        )

        right_label = Text("blueshift (approaching)", font_size=22, color=BLUE_C)
        right_label.next_to(right_star, DOWN, buff=1.1)

        # ---------- Animation sequence (total = 7.5 s) ----------
        self.play(Write(title), run_time=0.8)
        self.play(Create(axes), FadeIn(time_label, shift=UP * 0.2), run_time=0.6)
        self.play(
            GrowFromCenter(formula),
            FadeIn(caption, shift=UP * 0.2),
            run_time=0.7,
        )
        self.play(Create(red_wave), FadeIn(red_label), run_time=0.8)
        self.play(Create(blue_wave), FadeIn(blue_label), run_time=0.8)

        self.play(
            LaggedStart(
                GrowFromCenter(left_star),
                Create(left_arcs[0]),
                Create(left_arcs[1]),
                Create(left_arcs[2]),
                FadeIn(left_arrow, shift=LEFT * 0.3),
                Write(left_label),
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )

        self.play(
            LaggedStart(
                GrowFromCenter(right_star),
                Create(right_arcs[0]),
                Create(right_arcs[1]),
                Create(right_arcs[2]),
                FadeIn(right_arrow, shift=LEFT * 0.3),
                Write(right_label),
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )

        self.play(Circumscribe(formula, color=PEACH), run_time=0.7)
        self.wait(1.1)
        # --- Scene 9: Step 9: Applications: from radar to cosmology ---
        self.clear()
        self.camera.background_color = "#181825"

        C_BLUE = "#89b4fa"
        C_PEACH = "#fab387"
        C_PINK = "#f38ba8"
        C_GREEN = "#a6e3a1"
        C_TEAL = "#94e2d5"
        C_TEXT = "#cdd6f4"

        # ---------- Title ----------
        title = Text(
            "Applications: from radar to cosmology",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # ---------- Doppler shift number line ----------
        line = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            color=C_PINK,
            stroke_width=2.0,
            font_size=22,
        ).shift(DOWN * 1.9)

        blue_label = Text("Blueshift (approaching)", font_size=20, color=C_BLUE)
        blue_label.move_to(line.n2p(-3.2) + DOWN * 0.95)
        red_label = Text("Redshift (receding)", font_size=20, color=C_PEACH)
        red_label.move_to(line.n2p(3.2) + DOWN * 0.95)
        axis_label = Text("Doppler shift", font_size=22, color=C_TEXT)
        axis_label.move_to(line.n2p(0) + DOWN * 0.95)

        # ---------- Application icons ----------
        u_waves = VGroup(
            Dot(point=ORIGIN, radius=0.07, color=C_PINK),
            Arc(
                radius=0.2,
                start_angle=-PI / 3,
                angle=2 * PI / 3,
                color=C_PINK,
                stroke_width=2.0,
            ),
            Arc(
                radius=0.34,
                start_angle=-PI / 3,
                angle=2 * PI / 3,
                color=C_PINK,
                stroke_width=2.0,
            ),
            Arc(
                radius=0.48,
                start_angle=-PI / 3,
                angle=2 * PI / 3,
                color=C_PINK,
                stroke_width=2.0,
            ),
        ).move_to(UP * 1.0 + LEFT * 4)
        u_label = Text(
            "Ultrasound\nblood flow", font_size=22, color=C_PINK, line_spacing=0.9
        )
        u_label.next_to(u_waves, DOWN, buff=0.3)
        u_group = VGroup(u_waves, u_label)

        car = VGroup(
            Rectangle(width=1.1, height=0.42, color=C_BLUE, stroke_width=2.0),
            Circle(radius=0.13, color=C_BLUE, stroke_width=2.0).shift(
                LEFT * 0.3 + DOWN * 0.28
            ),
            Circle(radius=0.13, color=C_BLUE, stroke_width=2.0).shift(
                RIGHT * 0.3 + DOWN * 0.28
            ),
        ).move_to(UP * 1.0)
        r_label = Text(
            "Radar\nspeed guns", font_size=22, color=C_BLUE, line_spacing=0.9
        )
        r_label.next_to(car, DOWN, buff=0.3)
        r_group = VGroup(car, r_label)

        g_star = Star(
            n=5, outer_radius=0.5, color=C_PEACH, fill_opacity=0.25, stroke_width=2.0
        )
        g_star.move_to(UP * 1.0 + RIGHT * 4)
        g_label = Text(
            "Cosmic\nredshift", font_size=22, color=C_PEACH, line_spacing=0.9
        )
        g_label.next_to(g_star, DOWN, buff=0.3)
        g_group = VGroup(g_star, g_label)

        # ---------- Arrows from each application down to the scale ----------
        arrow_u = Arrow(
            u_group.get_bottom() + DOWN * 0.12,
            line.n2p(-3.0),
            color=C_GREEN,
            buff=0.1,
            stroke_width=2.5,
        )
        arrow_r = Arrow(
            r_group.get_bottom() + DOWN * 0.12,
            line.n2p(-1.5),
            color=C_GREEN,
            buff=0.1,
            stroke_width=2.5,
        )
        arrow_g = Arrow(
            g_group.get_bottom() + DOWN * 0.12,
            line.n2p(4.0),
            color=C_GREEN,
            buff=0.1,
            stroke_width=2.5,
        )

        # ---------- Passing flashes along the axis ----------
        flash_blue = Line(line.n2p(-0.2), line.n2p(-1.8), color=C_BLUE, stroke_width=6)
        flash_blue.shift(UP * 0.14)
        flash_red = Line(line.n2p(0.2), line.n2p(4.0), color=C_PEACH, stroke_width=6)
        flash_red.shift(UP * 0.14)

        # ---------- Summary ----------
        summary = Text(
            "One principle explains them all: the Doppler effect",
            font_size=28,
            color=C_TEAL,
        ).move_to(UP * 2.1)

        # ---------- Animations ----------
        self.play(Write(title), run_time=1.0)

        self.play(Create(line), run_time=0.7)
        nums = line.add_numbers()
        nums.set_color(C_TEXT)
        self.play(
            FadeIn(nums, shift=UP * 0.2),
            FadeIn(blue_label),
            FadeIn(red_label),
            FadeIn(axis_label),
            run_time=0.4,
        )

        self.play(
            LaggedStart(
                GrowFromCenter(u_group),
                GrowFromCenter(r_group),
                GrowFromCenter(g_group),
                lag_ratio=0.25,
            ),
            run_time=1.6,
        )

        self.play(
            LaggedStart(
                Create(arrow_u),
                Create(arrow_r),
                Create(arrow_g),
                lag_ratio=0.2,
            ),
            run_time=0.8,
        )

        self.play(
            ShowPassingFlash(flash_blue, time_width=0.35),
            ShowPassingFlash(flash_red, time_width=0.35),
            run_time=0.6,
        )

        self.play(FadeIn(summary, shift=UP * 0.3), run_time=0.6)
        self.play(Circumscribe(summary, color=C_TEAL), run_time=0.7)
        self.wait(1.6)
