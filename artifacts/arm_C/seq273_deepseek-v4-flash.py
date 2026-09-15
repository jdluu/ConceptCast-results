import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Title Intro ---
        self.clear()
        # Set background color per style guidelines
        self.camera.background_color = "#181825"

        # --- Create Objects ---

        # Main title with accent_1 (lavender/purple)
        main_title = Text(
            "The Fourier Transform",
            font_size=48,
            weight="BOLD",
            color="#CBA6F7",
            font="Sans",
        )
        main_title.move_to(ORIGIN)

        # Subtle glow behind title
        title_glow = Text(
            "The Fourier Transform",
            font_size=48,
            weight="BOLD",
            color="#CBA6F7",
            font="Sans",
        )
        title_glow.move_to(ORIGIN)
        title_glow.set_opacity(0.25)
        title_glow.scale(1.06)

        # Thin animated underline line (accent_3, warm orange)
        underline = Line(
            start=LEFT * 2.5, end=RIGHT * 2.5, color="#FAB387", stroke_width=3
        )
        underline.next_to(main_title, DOWN, buff=0.4)

        # --- Animation Sequence (total = 5.0s) ---

        # 1. Fade in glow (0.6s)
        self.play(FadeIn(title_glow, scale=1.2), run_time=0.6)

        # 2. Write title text (0.9s)
        self.play(Write(main_title), run_time=0.9)

        # 3. Grow underline from center (0.5s)
        self.play(GrowFromCenter(underline), run_time=0.5)

        # 4. Pulse animation on the underline (3 pulses, 1.5s total = 0.5s each)
        for i in range(3):
            self.play(
                underline.animate.scale(1.15, about_edge=ORIGIN).set_stroke_width(4),
                rate_func=there_and_back,
                run_time=0.5,
            )

        # 5. Final hold (1.5s)
        self.wait(1.5)

        # Timing check: 0.6 + 0.9 + 0.5 + (3*0.5) + 1.5 = 0.6+0.9+0.5+1.5+1.5 = 5.0 ✓
        # --- Scene 2: What is a Signal? ---
        self.clear()

        # --- 1. CREATE OBJECTS ---

        # Create the axes - positioned on the left portion of the screen
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=8,
            y_length=4.5,
            axis_config={
                "color": "#89B4FA",
                "include_numbers": True,
                "font_size": 22,
                "include_tip": True,
            },
        )
        axes.shift(LEFT * 1.5 + DOWN * 0.2)

        # Define the signal function: f(x) = 1.2 * sin(x)
        signal_func = lambda x: 1.2 * np.sin(x)

        # Create sine wave (glow layer behind)
        wave_glow = axes.plot(
            signal_func,
            x_range=[0, 6],
            color="#A6E3A1",
            stroke_width=8,
            stroke_opacity=0.2,
        )

        # Create sine wave (main visible wave)
        sine_wave = axes.plot(
            signal_func,
            x_range=[0, 6],
            color="#A6E3A1",
            stroke_width=4,
        )

        # Create axis labels
        x_label = axes.get_x_axis_label(
            MathTex("\	ext{Time}", color="#CDD6F4"),
            edge=DOWN,
            direction=DOWN,
            buff=0.3,
        )

        y_label = Tex("Amplitude", color="#FAB387", font_size=30)
        y_label.next_to(axes, UP + LEFT, buff=0.05)
        y_label.shift(RIGHT * 0.5)

        # Key points along the wave at notable positions
        key_coords = [
            (0.0, 0.0),  # Start at origin
            (1.57, 1.2),  # pi/2 -> peak
            (3.14, 0.0),  # pi -> zero crossing
            (4.71, -1.2),  # 3pi/2 -> trough
            (6.0, -0.28),  # Near end of range
        ]

        key_dots = VGroup()
        for x, y in key_coords:
            dot = Dot(
                axes.c2p(x, y),
                color="#FAB387",
                radius=0.09,
            )
            key_dots.add(dot)

        # Glow rings for key points
        glow_rings = VGroup()
        for dot in key_dots:
            ring = Circle(
                radius=0.18,
                color="#A6E3A1",
                stroke_width=1.5,
                stroke_opacity=0.6,
                fill_opacity=0.0,
            ).move_to(dot.get_center())
            glow_rings.add(ring)

        # Tracer dot that moves along the wave
        tracer = Dot(
            point=axes.c2p(0, 0),
            color="#A6E3A1",
            radius=0.12,
        )
        tracer_glow = Circle(
            radius=0.2,
            color="#A6E3A1",
            stroke_width=0,
            fill_opacity=0.4,
        ).move_to(tracer.get_center())

        # Invisible path for tracer to follow
        tracer_path = axes.plot(
            signal_func,
            x_range=[0, 6],
            color="#A6E3A1",
            stroke_width=0,
        )

        # --- 2. ANIMATIONS ---
        # Total duration must be exactly 5.0 seconds

        # Phase 1: Create axes (0.8s)
        self.play(Create(axes), run_time=0.8)

        # Phase 2: Write axis labels (0.5s)
        self.play(Write(x_label), Write(y_label), run_time=0.5)

        # Phase 3: Draw the sine wave with glow effect (1.2s)
        self.play(
            Create(wave_glow),
            Create(sine_wave),
            run_time=1.2,
        )

        # Phase 4: Animate tracer moving along the wave (0.8s)
        self.add(tracer_glow, tracer)
        self.play(
            MoveAlongPath(tracer, tracer_path),
            MoveAlongPath(tracer_glow, tracer_path),
            run_time=0.8,
        )

        # Phase 5: Key points appear sequentially (0.7s)
        self.play(
            LaggedStart(
                *[GrowFromCenter(d) for d in key_dots],
                lag_ratio=0.15,
            ),
            run_time=0.7,
        )

        # Phase 6: Glow rings pulse around key points (0.5s)
        self.play(
            *[Create(ring) for ring in glow_rings],
            run_time=0.5,
        )

        # Phase 7: Final emphasis highlight (0.5s)
        self.play(
            sine_wave.animate.set_stroke_opacity(1.0),
            run_time=0.3,
        )
        self.wait(0.2)

        # Duration check: 0.8 + 0.5 + 1.2 + 0.8 + 0.7 + 0.5 + 0.3 + 0.2 = 5.0 ✓
        # --- Scene 3: Frequency Analysis ---
        self.clear()
        # --- Scene 3: Frequency Analysis ---
        # Color palette (catppuccin mocha)
        pink = "#F38BA8"
        green = "#A6E3A1"
        blue = "#89B4FA"
        orange = "#FAB387"
        teal = "#94E2D5"
        white = "#CDD6F4"

        # --- LEFT SIDE: Complex waveform axes ---
        left_axes = Axes(
            x_range=[0, 8, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=4.5,
            y_length=3.0,
            axis_config={"color": white, "include_tip": False, "stroke_width": 1.5},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        )
        left_axes.shift(LEFT * 3.5 + UP * 0.3)

        # Sum-of-sines complex waveform
        complex_func = left_axes.plot(
            lambda x: 0.5 * np.sin(x) + 0.3 * np.sin(2 * x) + 0.25 * np.sin(3 * x),
            x_range=[0, 8],
            color=pink,
            stroke_width=3,
        )

        # Label above the left axes
        left_label = Text("Input Signal", font_size=28, color=white)
        left_label.next_to(left_axes, UP, buff=0.3)

        # --- MIDDLE: Equals sign ---
        eq_sign = MathTex("=", color=teal, font_size=60)
        eq_sign.shift(LEFT * 0.5 + UP * 0.3)

        # --- RIGHT SIDE: Three small sub-axes ---
        sub_width = 3.5
        sub_height = 1.2

        def make_sub_axes(y_shift, color, freq, label_tex):
            ax = Axes(
                x_range=[0, 8, 1],
                y_range=[-1.2, 1.2, 0.5],
                x_length=sub_width,
                y_length=sub_height,
                axis_config={"color": white, "include_tip": False, "stroke_width": 1},
                x_axis_config={"include_numbers": False},
                y_axis_config={"include_numbers": False},
            )
            ax.shift(RIGHT * 2.2 + y_shift)
            amp = 0.7 if freq == 1 else (0.5 if freq == 2 else 0.4)
            wave = ax.plot(
                lambda x: amp * np.sin(freq * x),
                x_range=[0, 8],
                color=color,
                stroke_width=3,
            )
            label = MathTex(label_tex, color=color, font_size=28)
            label.next_to(ax, UP, buff=0.15)
            return VGroup(ax, wave, label)

        sub1 = make_sub_axes(UP * 1.9, green, 1, "f_1")
        sub2 = make_sub_axes(UP * 0.0, blue, 2, "f_2")
        sub3 = make_sub_axes(DOWN * 1.9, orange, 3, "f_3")

        # Plus signs between sub-axes
        plus1 = MathTex("+", color=teal, font_size=40).move_to(RIGHT * 2.2 + UP * 0.95)
        plus2 = MathTex("+", color=teal, font_size=40).move_to(
            RIGHT * 2.2 + DOWN * 0.95
        )

        # Group for all right-side elements
        right_group = VGroup(sub1, sub2, sub3, plus1, plus2)

        # --- ANIMATION SEQUENCE ---
        # 1. Complex waveform writes in from the left (0.8s)
        self.play(
            Write(left_axes, run_time=0.3),
            FadeIn(left_label, run_time=0.3),
        )
        self.wait(0.1)
        self.play(
            Create(complex_func, run_time=0.8),
            rate_func=smooth,
        )

        # 2. Right-side components, plus signs, and equals sign appear (1.0s)
        self.play(
            FadeIn(eq_sign, run_time=0.3),
            FadeIn(sub1, shift=LEFT * 0.3, run_time=0.8),
            FadeIn(sub2, shift=LEFT * 0.3, run_time=0.8),
            FadeIn(sub3, shift=LEFT * 0.3, run_time=0.8),
            FadeIn(plus1, shift=LEFT * 0.3, run_time=0.8),
            FadeIn(plus2, shift=LEFT * 0.3, run_time=0.8),
            rate_func=smooth,
        )

        # 3. Each component wave + label highlighted in sequence (3 x 0.35s)
        for mob in [sub1, sub2, sub3]:
            self.play(
                Indicate(mob, color=WHITE, scale_factor=1.08, run_time=0.35),
                rate_func=smooth,
            )

        # 4. Teal surrounding rectangle groups all right-side elements (0.7s)
        rect = SurroundingRectangle(right_group, color=teal, buff=0.15, stroke_width=2)
        rect.set_stroke(opacity=0.7)
        self.play(
            Create(rect, run_time=0.7),
            rate_func=smooth,
        )

        # 5. The = sign gets a circumscribe flash (0.7s)
        self.play(
            Circumscribe(eq_sign, color=teal, run_time=0.7),
            rate_func=smooth,
        )

        # 6. Final flash on the original complex waveform (0.75s)
        self.play(
            Circumscribe(complex_func, color=orange, run_time=0.75),
            rate_func=smooth,
        )

        self.wait(0.5)
        # --- Scene 4: Sine Waves as Building Blocks ---
        self.clear()

        # Color palette matching the style guidelines
        bg = "#181825"
        green = "#A6E3A1"
        blue = "#89B4FA"
        orange = "#FAB387"
        purple = "#CBA6F7"
        white = "#CDD6F4"

        self.camera.background_color = bg

        # ---- CREATE AXES FOR THE THREE SINE WAVES ----
        ax_config = {
            "x_range": [0, 2 * PI, PI / 2],
            "y_range": [-1.5, 1.5, 1],
            "x_length": 3.5,
            "y_length": 1.2,
        }

        axes1 = Axes(
            **ax_config, axis_config={"color": "#585B70", "include_tip": False}
        )
        axes2 = Axes(
            **ax_config, axis_config={"color": "#585B70", "include_tip": False}
        )
        axes3 = Axes(
            **ax_config, axis_config={"color": "#585B70", "include_tip": False}
        )

        # Position them vertically on the left
        axes1.move_to(LEFT * 3 + UP * 2.5)
        axes2.move_to(LEFT * 3 + ORIGIN)
        axes3.move_to(LEFT * 3 + DOWN * 2.5)

        # Create the sine curves
        sine1 = axes1.plot(lambda x: np.sin(x), color=green, stroke_width=3)
        sine2 = axes2.plot(lambda x: np.sin(2 * x), color=blue, stroke_width=3)
        sine3 = axes3.plot(lambda x: np.sin(3 * x), color=orange, stroke_width=3)

        # Labels
        label1 = MathTex("f=1", color=green, font_size=24).next_to(axes1, RIGHT)
        label2 = MathTex("f=2", color=blue, font_size=24).next_to(axes2, RIGHT)
        label3 = MathTex("f=3", color=orange, font_size=24).next_to(axes3, RIGHT)

        # Title at top
        title = Text(
            "Sine Waves as Building Blocks", font_size=32, color=white
        ).to_edge(UP)

        # ---- COMBINED WAVE (sum) on the right ----
        sum_ax_config = {
            "x_range": [0, 2 * PI, PI / 2],
            "y_range": [-3.5, 3.5, 1],
            "x_length": 3.5,
            "y_length": 2.5,
        }
        sum_axes = Axes(
            **sum_ax_config, axis_config={"color": "#585B70", "include_tip": False}
        )
        sum_axes.move_to(RIGHT * 2.5 + DOWN * 0.5)

        # The combined wave: sin(x) + sin(2x) + sin(3x)
        sum_curve = sum_axes.plot(
            lambda x: np.sin(x) + np.sin(2 * x) + np.sin(3 * x),
            color=purple,
            stroke_width=4,
        )
        sum_label = MathTex(r"\text{Sum}", color=purple, font_size=24).next_to(
            sum_axes, RIGHT
        )

        # Narration text
        narration = Text(
            "Any periodic signal can be built\nby adding sine and cosine waves",
            font_size=22,
            color=white,
            line_spacing=1.2,
        ).to_edge(DOWN)

        # ---- ANIMATIONS ----
        # Total duration must be 6.0s

        # Phase 1: Show title and axes (1.5s total)
        self.play(Write(title), run_time=0.5)
        self.play(
            AnimationGroup(
                Create(axes1), Create(axes2), Create(axes3), lag_ratio=0.3, run_time=0.7
            )
        )
        self.wait(0.3)

        # Phase 2: Draw sine curves with labels (1.5s)
        self.play(
            AnimationGroup(
                Create(sine1), Create(sine2), Create(sine3), lag_ratio=0.2, run_time=0.8
            ),
            AnimationGroup(
                Write(label1), Write(label2), Write(label3), lag_ratio=0.2, run_time=0.8
            ),
        )
        self.wait(0.7)

        # Phase 3: Show combined wave axes and curve (1.5s)
        self.play(Create(sum_axes), run_time=0.5)
        self.play(Create(sum_curve), Write(sum_label), run_time=0.7)
        self.wait(0.3)

        # Phase 4: Visualize addition - ghosts move to sum area (1.5s)
        ghost1 = sine1.copy().set_opacity(0.8).set_stroke_width(2)
        ghost2 = sine2.copy().set_opacity(0.8).set_stroke_width(2)
        ghost3 = sine3.copy().set_opacity(0.8).set_stroke_width(2)

        sum_center = sum_axes.get_center()

        self.play(
            ghost1.animate.move_to(sum_center + UP * 0.8)
            .set_opacity(0.2)
            .set_color(purple),
            ghost2.animate.move_to(sum_center).set_opacity(0.2).set_color(purple),
            ghost3.animate.move_to(sum_center + DOWN * 0.8)
            .set_opacity(0.2)
            .set_color(purple),
            run_time=0.6,
        )

        # Highlight the sum curve
        self.play(Indicate(sum_curve, scale_factor=1.05, color=WHITE), run_time=0.5)

        # Show narration
        self.play(Write(narration), run_time=0.4)
        # --- Scene 5: Introducing the Fourier Transform ---
        self.clear()

        # Colors from the style guidelines
        blue = "#89b4fa"
        gold = "#fab387"
        green = "#a6e3a1"
        pink = "#f38ba8"
        teal = "#94e2d5"

        # ============================================================
        # 1. LEFT THIRD: Time-Domain Axes + Waveform
        # ============================================================
        time_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=4.5,
            y_length=2.5,
            axis_config={
                "color": blue,
                "include_tip": True,
                "tip_length": 0.15,
                "stroke_width": 2,
            },
            x_axis_config={
                "numbers_to_include": [-2, -1, 0, 1, 2],
                "numbers_with_elongated_ticks": [-2, -1, 0, 1, 2],
            },
            y_axis_config={
                "numbers_to_include": [-1, 0, 1],
            },
        )
        time_axes.shift(LEFT * 4 + DOWN * 0.3)

        time_label = Text("Time Domain", font_size=22, color=blue)
        time_label.next_to(time_axes, UP, buff=0.3)

        # Time-domain waveform: composite sine wave
        time_wave = time_axes.plot(
            lambda x: 0.8 * np.sin(2 * x) + 0.4 * np.sin(4.5 * x),
            x_range=[-3, 3],
            color=blue,
            stroke_width=3,
        )

        # ============================================================
        # 2. CENTER: Glowing Circular Portal (Golden)
        # ============================================================
        portal_circle = Circle(
            radius=1.2,
            color=gold,
            stroke_width=5,
        )
        portal_circle.shift(ORIGIN)

        inner_ring = Circle(
            radius=0.8,
            color=gold,
            stroke_width=2,
            stroke_opacity=0.5,
        )
        inner_ring.shift(ORIGIN)

        outer_ring = Circle(
            radius=1.5,
            color=gold,
            stroke_width=2,
            stroke_opacity=0.3,
        )
        outer_ring.shift(ORIGIN)

        center_dot = Dot(
            point=ORIGIN,
            radius=0.12,
            color=gold,
        )

        # Transform label
        ft_label = MathTex(r"\mathcal{F}", font_size=48, color=gold)
        ft_label.next_to(portal_circle, DOWN, buff=0.3)

        subtitle = Text("Fourier Transform", font_size=18, color=gold, opacity=0.8)
        subtitle.next_to(ft_label, DOWN, buff=0.15)

        # ============================================================
        # 3. RIGHT THIRD: Frequency Spectrum Axes + Spikes
        # ============================================================
        freq_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 2, 0.5],
            x_length=4.5,
            y_length=2.5,
            axis_config={
                "color": green,
                "include_tip": True,
                "tip_length": 0.15,
                "stroke_width": 2,
            },
            x_axis_config={
                "numbers_to_include": [1, 2, 3, 4],
                "numbers_with_elongated_ticks": [1, 2, 3, 4],
            },
            y_axis_config={
                "numbers_to_include": [0.5, 1.0, 1.5],
            },
        )
        freq_axes.shift(RIGHT * 4 + DOWN * 0.3)

        freq_label = Text("Frequency Spectrum", font_size=22, color=green)
        freq_label.next_to(freq_axes, UP, buff=0.3)

        # Create frequency spikes
        spike_data = [
            (1, 1.6, green),
            (2, 0.9, blue),
            (3, 1.8, gold),
            (4, 0.5, pink),
            (5, 1.2, teal),
        ]

        spikes = VGroup()
        spike_dots = VGroup()

        for x_val, height, color in spike_data:
            bottom = freq_axes.c2p(x_val, 0)
            top = freq_axes.c2p(x_val, height)
            spike = Line(
                start=bottom,
                end=top,
                color=color,
                stroke_width=8,
            )
            spikes.add(spike)
            dot = Dot(point=top, radius=0.07, color=color)
            spike_dots.add(dot)

        # ============================================================
        # ANIMATION SEQUENCE (Total: 6.5s)
        # ============================================================

        # Phase 1: Time domain appears (1.5s total)
        self.play(
            Write(time_axes, run_time=1.0),
            FadeIn(time_label, run_time=0.8),
        )
        self.play(
            Create(time_wave, run_time=1.2),
        )

        # Phase 2: Portal emerges (1.4s total)
        self.play(
            GrowFromCenter(outer_ring, run_time=0.5),
            GrowFromCenter(portal_circle, run_time=0.7),
            GrowFromCenter(inner_ring, run_time=0.5),
            FadeIn(center_dot, run_time=0.4),
        )

        # Portal pulse (0.8s)
        self.play(
            portal_circle.animate.scale(1.08).set_stroke_opacity(0.7),
            run_time=0.4,
        )
        self.play(
            portal_circle.animate.scale(1 / 1.08).set_stroke_opacity(1.0),
            run_time=0.4,
        )

        # Phase 3: Label appears (0.5s)
        self.play(
            Write(ft_label, run_time=0.35),
            FadeIn(subtitle, run_time=0.35),
        )

        # Phase 4: Frequency axes + spikes (2.2s total)
        self.play(
            Write(freq_axes, run_time=0.6),
            FadeIn(freq_label, run_time=0.5),
        )

        # Spikes one by one (5 * 0.18s = 0.9s)
        for i in range(len(spikes)):
            self.play(
                GrowFromCenter(spikes[i], run_time=0.18),
                FadeIn(spike_dots[i], run_time=0.12),
            )

        # Phase 5: Hold (0.95s)
        self.wait(0.95)
        # --- Scene 6: The Integral Formula ---
        self.clear()
        self.camera.background_color = "#181825"

        title = Text("The Integral Formula", font_size=36, color="#CDD6F4")
        title.to_edge(UP, buff=0.5)
        underline = Line(
            title.get_left(), title.get_right(), color="#CBA6F7", stroke_width=2
        ).next_to(title, DOWN, buff=0.08)
        title_group = VGroup(title, underline)
        self.add(title_group)

        formula = MathTex(
            r"F(f) = \int_{-\infty}^{\infty} f(t) e^{-i 2 \pi f t} \, dt",
            font_size=42,
            color="#CDD6F4",
            substrings_to_isolate=[r"\int", r"e^{-i 2 \pi f t}", "dt"],
        )
        formula.move_to(ORIGIN)
        self.add(formula)

        int_part = formula.get_part_by_tex(r"\int")
        exp_part = formula.get_part_by_tex(r"e^{-i 2 \pi f t}")
        dt_part = formula.get_part_by_tex("dt")

        if int_part is None:
            int_part = formula
        if exp_part is None:
            exp_part = formula
        if dt_part is None:
            dt_part = formula

        self.wait(0.3)

        int_highlight = SurroundingRectangle(
            int_part, color="#FAB387", stroke_width=4, buff=0.1, corner_radius=0.05
        )
        int_label = Text("Integral", font_size=24, color="#FAB387")
        int_label.next_to(int_highlight, UP, buff=0.15)
        int_arrow = Arrow(
            start=int_label.get_bottom(),
            end=int_highlight.get_top(),
            color="#FAB387",
            tip_length=0.15,
            stroke_width=2,
        )

        self.play(
            Create(int_highlight), Write(int_label), Create(int_arrow), run_time=1.2
        )
        self.wait(0.3)

        exp_highlight = SurroundingRectangle(
            exp_part, color="#89B4FA", stroke_width=4, buff=0.1, corner_radius=0.05
        )
        exp_label = Text("Complex Exponential", font_size=24, color="#89B4FA")
        exp_label.next_to(exp_highlight, UP, buff=0.15)
        exp_arrow = Arrow(
            start=exp_label.get_bottom(),
            end=exp_highlight.get_top(),
            color="#89B4FA",
            tip_length=0.15,
            stroke_width=2,
        )

        self.play(
            Create(exp_highlight), Write(exp_label), Create(exp_arrow), run_time=1.2
        )
        self.wait(0.3)

        dt_highlight = SurroundingRectangle(
            dt_part, color="#A6E3A1", stroke_width=4, buff=0.1, corner_radius=0.05
        )
        dt_label = Text("differential", font_size=24, color="#A6E3A1")
        dt_label.next_to(dt_highlight, UP, buff=0.15)
        dt_arrow = Arrow(
            start=dt_label.get_bottom(),
            end=dt_highlight.get_top(),
            color="#A6E3A1",
            tip_length=0.15,
            stroke_width=2,
        )

        self.play(Create(dt_highlight), Write(dt_label), Create(dt_arrow), run_time=1.2)
        self.wait(0.3)

        self.play(
            Indicate(int_highlight, color="#FAB387", scale_factor=1.05), run_time=0.8
        )
        self.wait(0.4)

        self.wait(1.0)
        # --- Scene 7: The Complex Exponential ---
        self.clear()

        TEXT_COLOR = "#CDD6F4"
        AXIS_COLOR = "#CDD6F4"
        PHASOR_COLOR = "#FAB387"
        TRACE_COLOR = "#89B4FA"
        SLIDER_COLOR = "#A6E3A1"

        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            axis_config={
                "color": AXIS_COLOR,
                "stroke_width": 2,
                "include_tip": True,
                "numbers_to_include": [],
            },
        )

        x_label = MathTex("\	ext{Real}", color=TEXT_COLOR).next_to(
            axes.x_axis.get_right(), RIGHT, buff=0.15
        )
        y_label = MathTex("\	ext{Imag}", color=TEXT_COLOR).next_to(
            axes.y_axis.get_top(), UP, buff=0.15
        )

        trace_circle = Circle(
            radius=1.5,
            color=TRACE_COLOR,
            stroke_width=2,
            stroke_opacity=0.6,
        )

        freq_tracker = ValueTracker(0.3)

        slider_track = Line(LEFT * 1.5, RIGHT * 1.5, color=SLIDER_COLOR, stroke_width=6)
        slider_track.shift(DOWN * 2.5)

        def get_slider_handle():
            val = freq_tracker.get_value()
            min_val = 0.1
            max_val = 2.0
            prop = (val - min_val) / (max_val - min_val)
            prop = np.clip(prop, 0, 1)
            point = slider_track.point_from_proportion(prop)
            return Dot(point=point, color=SLIDER_COLOR, radius=0.12)

        slider_handle = always_redraw(get_slider_handle)

        slider_label = Text("Frequency", color=TEXT_COLOR, font_size=24)
        slider_label.next_to(slider_track, UP, buff=0.3)

        def get_value_display():
            return DecimalNumber(
                freq_tracker.get_value(),
                num_decimal_places=1,
                color=TEXT_COLOR,
                font_size=20,
            ).next_to(slider_track, DOWN, buff=0.15)

        value_display = always_redraw(get_value_display)

        slider_group = VGroup(slider_track, slider_handle, slider_label, value_display)

        angle_tracker = ValueTracker(0)

        def get_phasor():
            angle = angle_tracker.get_value()
            end_point = axes.c2p(1.5 * np.cos(angle), 1.5 * np.sin(angle))
            arrow = Arrow(
                start=axes.c2p(0, 0),
                end=end_point,
                color=PHASOR_COLOR,
                stroke_width=4,
                tip_length=0.2,
            )
            return arrow

        phasor_arrow = always_redraw(get_phasor)

        def rotate_phasor(mob, dt):
            speed = freq_tracker.get_value() * TAU
            angle_tracker.increment_value(dt * speed)

        phasor_arrow.add_updater(rotate_phasor)

        self.add(axes, x_label, y_label, trace_circle, phasor_arrow, slider_group)
        self.play(freq_tracker.animate.set_value(1.5), run_time=5.0)
        self.wait(1.5)
        # --- Scene 8: Correlation Matching ---
        self.clear()

        # ---- Color Palette (Catppuccin Mocha) ----
        bg = "#1E1E2E"
        blue = "#89B4FA"
        orange = "#FAB387"
        green = "#A6E3A1"
        text_color = "#CDD6F4"

        self.camera.background_color = bg

        # ---- ValueTrackers ----
        phase_tracker = ValueTracker(0.0)
        corr_tracker = ValueTracker(0.0)

        # ---- Wave parameters ----
        wave_amplitude = 0.6
        wave_freq = 2.0
        wave_width = 5.0
        wave_center_x = -2.0

        # ---- Helper to make a sine wave ----
        def make_wave(color, center_y, phase_offset):
            points = []
            n_points = 100
            for i in range(n_points + 1):
                t = i / n_points
                x = wave_center_x - wave_width / 2 + t * wave_width
                y = center_y + wave_amplitude * np.sin(
                    wave_freq * t * TAU - phase_offset
                )
                points.append(np.array([x, y, 0]))
            wave = VMobject(stroke_color=color, stroke_width=3)
            wave.set_points_smoothly(points)
            return wave

        # ---- Signal Wave (top, blue) - fixed ----
        signal_y = 1.5
        signal_wave = always_redraw(lambda: make_wave(blue, signal_y, 0))

        # ---- Template/Phasor Wave (bottom, orange) - slides via phase ----
        template_y = -1.5
        template_wave = always_redraw(
            lambda: make_wave(orange, template_y, phase_tracker.get_value())
        )

        # ---- Labels ----
        signal_label = Text("Signal", font_size=28, color=blue).next_to(
            signal_wave, UP, buff=0.3, aligned_edge=LEFT
        )
        signal_label.add_updater(
            lambda m: m.next_to(signal_wave, UP, buff=0.3, aligned_edge=LEFT)
        )

        template_label = Text("Phasor", font_size=28, color=orange).next_to(
            template_wave, DOWN, buff=0.3, aligned_edge=LEFT
        )
        template_label.add_updater(
            lambda m: m.next_to(template_wave, DOWN, buff=0.3, aligned_edge=LEFT)
        )

        # ---- Correlation Meter (vertical bar on right) ----
        meter_x = 3.2
        meter_height = 3.5
        meter_width = 0.5

        # Background track
        meter_bg = Rectangle(
            height=meter_height,
            width=meter_width,
            color=text_color,
            stroke_width=1.5,
            fill_opacity=0.08,
            fill_color="#45475A",
        ).shift(meter_x)

        # Tick marks
        tick_marks = VGroup()
        tick_labels = VGroup()
        for i in range(5):
            frac = i / 4.0
            y_pos = meter_bg.get_bottom()[1] + frac * meter_height
            tick = Line(
                LEFT * 0.15, RIGHT * 0.15, color="#585B70", stroke_width=1.5
            ).move_to(np.array([meter_x, y_pos, 0]))
            tick_marks.add(tick)
            if i % 2 == 0:
                lbl = Text(
                    f"{int(frac * 100)}%", font_size=10, color="#585B70"
                ).next_to(tick, LEFT, buff=0.1)
                tick_labels.add(lbl)

        # Fill bar
        meter_fill = Rectangle(
            height=0.01,
            width=meter_width * 0.82,
            color=green,
            fill_opacity=0.9,
            fill_color=green,
            stroke_width=0,
        )

        def update_meter_fill(mob):
            val = corr_tracker.get_value()
            h = val * meter_height * 0.95
            if h < 0.02:
                h = 0.02
            mob.set_height(h)
            bottom = meter_bg.get_bottom() + UP * 0.05
            mob.move_to(bottom + UP * h / 2, aligned_edge=DOWN)
            mob.shift(RIGHT * 0.03)
            return mob

        meter_fill.add_updater(update_meter_fill)

        # Labels and percentage
        meter_label = Text("Correlation", font_size=22, color=green).next_to(
            meter_bg, UP, buff=0.3
        )

        perc_sign = Text("%", font_size=18, color=green).next_to(
            meter_label, UP, buff=0.08
        )

        percent_text = DecimalNumber(0, num_decimal_places=0, font_size=26, color=green)

        def update_percent(mob):
            val = int(round(corr_tracker.get_value() * 100))
            mob.set_value(val)
            mob.next_to(perc_sign, LEFT, buff=0.05, aligned_edge=DOWN)

        percent_text.add_updater(update_percent)

        # ---- Vertical alignment guide ----
        align_line = always_redraw(
            lambda: DashedLine(
                np.array([wave_center_x - wave_width / 2, signal_y, 0]),
                np.array([wave_center_x - wave_width / 2, template_y, 0]),
                color="#585B70",
                stroke_width=1.5,
                dash_length=0.06,
            )
        )

        # ---- Correlation function ----
        def update_corr():
            phase = phase_tracker.get_value()
            val = (np.cos(phase) + 1.0) / 2.0
            corr_tracker.set_value(val)

        phase_tracker.add_updater(lambda m, dt: update_corr())

        # ---- Add all objects ----
        self.add(signal_wave, template_wave, signal_label, template_label)
        self.add(meter_bg, tick_marks, tick_labels, meter_fill)
        self.add(meter_label, perc_sign, percent_text)
        self.add(align_line)

        # ---- Animation Sequence ----
        self.play(phase_tracker.animate.set_value(TAU), run_time=4.0, rate_func=smooth)
        self.wait(0.5)
        self.play(
            phase_tracker.animate.set_value(TAU * 1.5), run_time=1.5, rate_func=smooth
        )

        phase_tracker.clear_updaters()
        # --- Scene 9: From Continuous to Discrete: DFT ---
        self.clear()

        # Colors
        bg = "#1A1B26"
        blue = "#7AA2F7"
        purple = "#BB9AF7"
        green = "#9ECE6A"
        orange = "#E0AF68"
        cyan = "#2AC3DE"
        white = "#C0CAF5"
        text_gray = "#565F89"

        self.camera.background_color = bg

        # ===================== LEFT: Continuous Axes =====================
        cont_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=4,
            axis_config={
                "color": text_gray,
                "include_numbers": False,
                "include_tip": False,
            },
        ).shift(LEFT * 3.5)

        cont_label = Text("Continuous", font_size=28, color=white).next_to(
            cont_axes, UP, buff=0.3
        )

        # Decaying sine wave: sin(2.5 t) * exp(-0.15 t)
        def wave_func(t):
            return np.sin(2.5 * t) * np.exp(-0.15 * t)

        cont_wave = cont_axes.plot(
            wave_func,
            x_range=[0.3, 4.8],
            color=blue,
            stroke_width=3,
        )

        # ===================== Sampling ticks + dots =====================
        sample_times = [0.5 + 0.5 * i for i in range(9)]  # 0.5 to 4.5
        tick_lines = VGroup()
        sample_dots = VGroup()

        for t in sample_times:
            y_val = wave_func(t)
            pt = cont_axes.c2p(t, y_val)
            base = cont_axes.c2p(t, 0)
            # Dashed vertical line
            dline = DashedLine(
                start=base,
                end=pt,
                dash_length=0.08,
                color=orange,
                stroke_width=2,
                stroke_opacity=0.7,
            )
            tick_lines.add(dline)
            # Dot at sample point
            dot = Dot(point=pt, radius=0.06, color=orange)
            sample_dots.add(dot)

        # ===================== RIGHT: Discrete / Stem Axes =====================
        stem_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=4,
            axis_config={
                "color": text_gray,
                "include_numbers": False,
                "include_tip": False,
            },
        ).shift(RIGHT * 3.5)

        stem_label = Text("Discrete", font_size=28, color=green).next_to(
            stem_axes, UP, buff=0.3
        )

        # Build stem plot (vertical lines + dots) at same sample times
        stem_lines = VGroup()
        stem_dots = VGroup()

        for t in sample_times:
            y_val = wave_func(t)
            pt = stem_axes.c2p(t, y_val)
            base = stem_axes.c2p(t, 0)
            line = Line(start=base, end=pt, color=orange, stroke_width=2.5)
            stem_lines.add(line)
            dot = Dot(point=pt, radius=0.07, color=cyan)
            stem_dots.add(dot)

        stem_plot = VGroup(stem_lines, stem_dots)
        stem_plot.set_opacity(0)

        # ===================== ANIMATION SEQUENCE =====================
        # Phase 0: Show left axes + wave
        self.play(
            FadeIn(cont_axes, shift=UP * 0.3),
            Write(cont_label),
            run_time=0.8,
        )
        self.play(Create(cont_wave, run_time=1.0))
        self.wait(0.2)

        # Phase 1: Sampling ticks appear sequentially (0–2.0s)
        self.play(
            LaggedStart(
                *[Create(tl, run_time=0.3) for tl in tick_lines],
                lag_ratio=0.15,
            ),
            run_time=2.0,
        )

        # Phase 2: Dots appear at sample points (2.0–3.5s)
        self.play(
            LaggedStart(
                *[FadeIn(sd, scale=0.5, run_time=0.25) for sd in sample_dots],
                lag_ratio=0.1,
            ),
            run_time=1.5,
        )

        # Phase 3: Pause (3.5–4.0s)
        self.wait(0.5)

        # Phase 4: Transition — cross-fade (4.0–5.2s)
        left_group = VGroup(cont_axes, cont_wave, cont_label, tick_lines, sample_dots)
        left_group.generate_target()
        left_group.target.shift(LEFT * 0.5)
        left_group.target.set_opacity(0)

        self.play(
            # Fade out left side with leftward shift
            MoveToTarget(left_group, rate_func=smooth),
            # Fade in right stem plot
            stem_plot.animate.set_opacity(1),
            FadeIn(stem_axes, shift=RIGHT * 0.3),
            Write(stem_label),
            run_time=1.2,
        )

        # Phase 5: Pulse highlight (5.2–6.0s)
        self.play(
            Indicate(stem_plot, color=cyan, scale_factor=1.05),
            run_time=0.6,
        )
        self.wait(0.2)
        # --- Scene 10: The Fast Fourier Transform (FFT) ---
        # Set background
        self.camera.background_color = "#1E1E2E"

        # --- Bar 1: N² (naive / tall bar) ---
        bar_naive = BarChart(
            values=[4.0],
            bar_names=["N²"],
            bar_width=0.6,
            bar_colors=["#F38BA8"],
            y_range=[0, 5, 1],
            x_length=2,
            y_length=4,
        )
        bar_naive.next_to(ORIGIN, LEFT, buff=1.5).shift(DOWN * 0.5)

        # --- Bar 2: N log N (shorter bar) ---
        bar_fft = BarChart(
            values=[2.0],
            bar_names=["N log N"],
            bar_width=0.6,
            bar_colors=["#A6E3A1"],
            y_range=[0, 5, 1],
            x_length=2,
            y_length=4,
        )
        bar_fft.next_to(ORIGIN, RIGHT, buff=1.5).shift(DOWN * 0.5)

        # --- "vs." label ---
        vs_label = Text("vs.", font_size=36, color="#FAB387")
        vs_label.next_to(ORIGIN, UP, buff=2.0)

        # --- Labels below bars ---
        label_naive = Text("N²", font_size=32, color="#F38BA8")
        label_naive.next_to(bar_naive, DOWN, buff=0.3)

        label_fft = Text("N log N", font_size=32, color="#A6E3A1")
        label_fft.next_to(bar_fft, DOWN, buff=0.3)

        # Title
        title = Text("Fast Fourier Transform (FFT)", font_size=42, color="#CDD6F4")
        title.to_edge(UP, buff=0.5)

        # --- Animations ---
        # 1. Show title
        self.play(Write(title), run_time=0.8)

        # 2. Show the two bars and labels
        self.play(
            Create(bar_naive),
            Create(bar_fft),
            Write(vs_label),
            Write(label_naive),
            Write(label_fft),
            run_time=1.2,
        )
        self.wait(0.5)

        # 3. Animate the left bar shrinking down to match the right bar's height
        self.play(
            bar_naive.animate.change_bar_values([2.0]), run_time=1.5, rate_func=smooth
        )

        # 4. Pause to show the match
        self.wait(0.5)

        # 5. Show a label explaining the improvement
        improvement_label = Text("O(N log N) → Fast!", font_size=36, color="#A6E3A1")
        improvement_label.next_to(bar_naive, UP, buff=1.0)
        self.play(Write(improvement_label), run_time=0.8)

        self.wait(1.0)
        # --- Scene 11: Applications ---
        self.clear()
        self.camera.background_color = "#1E1E2E"

        # Colors from Catppuccin Mocha
        TEXT_COLOR = "#CDD6F4"
        PEACH = "#FAB387"
        BLUE = "#89B4FA"
        GREEN = "#A6E3A1"

        # ========== TITLE ==========
        title = Text(
            "Applications of the Fourier Transform", font_size=42, color=TEXT_COLOR
        )
        title.to_edge(UP, buff=0.6)

        # ========== AUDIO COLUMN (LEFT) ==========
        # Music note: ellipse head + stem + arc flag
        note_head = Ellipse(width=0.5, height=0.35, color=PEACH, fill_opacity=0.8)
        note_head.move_to(LEFT * 4 + UP * 1.5)

        stem_top = note_head.get_top() + UP * 0.7
        note_stem = Line(note_head.get_top(), stem_top, color=PEACH, stroke_width=3)

        note_flag = Arc(
            radius=0.3, start_angle=PI / 2, angle=-PI / 1.5, color=PEACH, stroke_width=3
        )
        note_flag.move_to(stem_top, aligned_edge=LEFT)
        note_flag.shift(RIGHT * 0.05)

        music_note = VGroup(note_head, note_stem, note_flag)

        audio_label = Text("Audio", font_size=28, color=PEACH)
        audio_label.next_to(music_note, DOWN, buff=0.3)

        # Audio spectrum - 12 bars with rich varied heights
        audio_heights = [0.5, 1.2, 0.8, 1.5, 0.6, 1.8, 0.4, 1.6, 0.7, 1.3, 0.5, 0.9]

        audio_baseline = Line(LEFT * 1.7, RIGHT * 1.7, color=PEACH, stroke_width=1.5)
        audio_baseline.next_to(audio_label, DOWN, buff=0.5)

        audio_bars = VGroup()
        bar_width = 0.18
        spacing = 0.22
        n_bars = len(audio_heights)
        for i, h in enumerate(audio_heights):
            bar = Rectangle(
                width=bar_width,
                height=h,
                color=PEACH,
                fill_opacity=0.7,
                fill_color=PEACH,
            )
            bar.set_stroke(width=0.5)
            x_pos = (i - (n_bars - 1) / 2) * spacing
            bar.move_to(audio_baseline.get_center() + UP * h / 2 + RIGHT * x_pos)
            audio_bars.add(bar)

        audio_spec_group = VGroup(audio_baseline, audio_bars)
        audio_spec_group.next_to(audio_label, DOWN, buff=0.3)

        audio_freq_label = Text("Frequency", font_size=16, color=PEACH, opacity=0.7)
        audio_freq_label.next_to(audio_spec_group, DOWN, buff=0.15)

        # ========== IMAGE COLUMN (CENTER) ==========
        frame = RoundedRectangle(
            width=0.95,
            height=0.85,
            corner_radius=0.1,
            color=BLUE,
            fill_opacity=0.15,
            fill_color=BLUE,
        )
        frame.set_stroke(width=2)
        frame.move_to(UP * 1.5)

        mountain = Polygon(
            frame.get_corner(DL) + RIGHT * 0.2,
            frame.get_corner(UL) + DOWN * 0.25 + RIGHT * 0.15,
            frame.get_corner(DR) + LEFT * 0.2,
            color=BLUE,
            fill_opacity=0.5,
            fill_color=BLUE,
            stroke_width=1,
        )
        sun = Dot(
            frame.get_corner(UR) + LEFT * 0.3 + DOWN * 0.3,
            radius=0.08,
            color=BLUE,
            fill_opacity=0.9,
        )
        image_icon = VGroup(frame, mountain, sun)

        image_label = Text("Image", font_size=28, color=BLUE)
        image_label.next_to(image_icon, DOWN, buff=0.3)

        img_heights = [1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.5, 0.4, 0.3, 0.25, 0.2, 0.15]
        img_baseline = Line(LEFT * 1.7, RIGHT * 1.7, color=BLUE, stroke_width=1.5)
        img_baseline.next_to(image_label, DOWN, buff=0.5)
        img_bars = VGroup()
        for i, h in enumerate(img_heights):
            bar = Rectangle(
                width=bar_width, height=h, color=BLUE, fill_opacity=0.7, fill_color=BLUE
            )
            bar.set_stroke(width=0.5)
            x_pos = (i - (n_bars - 1) / 2) * spacing
            bar.move_to(img_baseline.get_center() + UP * h / 2 + RIGHT * x_pos)
            img_bars.add(bar)
        image_spec_group = VGroup(img_baseline, img_bars)
        image_spec_group.next_to(image_label, DOWN, buff=0.3)
        image_freq_label = Text("Frequency", font_size=16, color=BLUE, opacity=0.7)
        image_freq_label.next_to(image_spec_group, DOWN, buff=0.15)

        # ========== MATH COLUMN (RIGHT) ==========
        pde_eq = MathTex(
            r"\frac{\partial^2 u}{\partial x^2} = f", color=GREEN, font_size=36
        )
        pde_eq.move_to(RIGHT * 4 + UP * 1.5)

        math_label = Text("Equations", font_size=28, color=GREEN)
        math_label.next_to(pde_eq, DOWN, buff=0.3)

        math_heights = [0.2, 0.3, 0.5, 0.7, 1.0, 1.3, 1.5, 1.3, 1.0, 0.7, 0.5, 0.3]
        math_baseline = Line(LEFT * 1.7, RIGHT * 1.7, color=GREEN, stroke_width=1.5)
        math_baseline.next_to(math_label, DOWN, buff=0.5)
        math_bars = VGroup()
        for i, h in enumerate(math_heights):
            bar = Rectangle(
                width=bar_width,
                height=h,
                color=GREEN,
                fill_opacity=0.7,
                fill_color=GREEN,
            )
            bar.set_stroke(width=0.5)
            x_pos = (i - (n_bars - 1) / 2) * spacing
            bar.move_to(math_baseline.get_center() + UP * h / 2 + RIGHT * x_pos)
            math_bars.add(bar)
        math_spec_group = VGroup(math_baseline, math_bars)
        math_spec_group.next_to(math_label, DOWN, buff=0.3)
        math_freq_label = Text("Frequency", font_size=16, color=GREEN, opacity=0.7)
        math_freq_label.next_to(math_spec_group, DOWN, buff=0.15)

        # ========== ANIMATION (6.0s total) ==========
        # 0.0 - 0.8s: Title
        self.play(Write(title), run_time=0.8)

        # 0.8 - 1.0s: Pause
        self.wait(0.2)

        # 1.0 - 2.2s: Audio column (LaggedStart with 30% overlap)
        self.play(
            LaggedStart(
                GrowFromCenter(music_note),
                Write(audio_label),
                GrowFromCenter(audio_spec_group),
                FadeIn(audio_freq_label, shift=UP * 0.1),
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )

        # 2.2 - 3.4s: Image column
        self.play(
            LaggedStart(
                GrowFromCenter(image_icon),
                Write(image_label),
                GrowFromCenter(image_spec_group),
                FadeIn(image_freq_label, shift=UP * 0.1),
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )

        # 3.4 - 4.6s: Math column
        self.play(
            LaggedStart(
                Write(pde_eq),
                Write(math_label),
                GrowFromCenter(math_spec_group),
                FadeIn(math_freq_label, shift=UP * 0.1),
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )

        # 4.6 - 6.0s: Hold final composition
        self.wait(1.4)
        # --- Scene 12: Summary & Outro ---
        self.clear()

        # --- Colors from style guidelines ---
        bg = "#181825"
        self.camera.background_color = bg

        accent_blue = "#89b4fa"
        accent_peach = "#fab387"
        accent_pink = "#f38ba8"
        accent_green = "#a6e3a1"
        accent_teal = "#94e2d5"
        accent_mauve = "#cba6f7"
        accent_red = "#f38ba8"

        # --- 1. Central Title ---
        title = Text(
            "From Time to Frequency", font_size=44, color=accent_mauve, weight="BOLD"
        )
        title.move_to(UP * 1.5)

        # Underline glow
        underline = Rectangle(
            width=title.width * 1.2, height=0.04, color=accent_mauve, fill_opacity=0.6
        )
        underline.next_to(title, DOWN, buff=0.15)

        # --- 2. Recap Wave (left) ---
        axes_wave = Axes(
            x_range=[0, 2 * PI, PI / 4],
            y_range=[-1.2, 1.2, 0.5],
            x_length=2.5,
            y_length=1.2,
            axis_config={
                "stroke_width": 1,
                "color": "#585b70",
                "include_numbers": False,
                "include_ticks": False,
            },
        )
        axes_wave.move_to(LEFT * 3 + DOWN * 1)

        wave = axes_wave.plot(
            lambda x: 0.8 * np.sin(2 * x) + 0.3 * np.sin(4 * x),
            color=accent_blue,
            stroke_width=2.5,
        )

        wave_label = Text("Wave", font_size=18, color=accent_blue)
        wave_label.next_to(axes_wave, UP, buff=0.15)

        recap_wave_group = VGroup(axes_wave, wave, wave_label)

        # --- 3. Recap Spectrum (right) - using bars via VGroup of Rectangles ---
        bar_values = [0.3, 0.8, 0.2, 0.6, 1.0, 0.4, 0.7, 0.1]
        bars = VGroup()
        n_bars = len(bar_values)
        bar_width = 0.25
        total_width = n_bars * bar_width * 1.6
        start_x = -total_width / 2 + bar_width / 2

        colors_bar = [
            accent_peach,
            accent_green,
            accent_pink,
            accent_teal,
            accent_peach,
            accent_green,
            accent_pink,
            accent_teal,
        ]

        for i, val in enumerate(bar_values):
            bar_height = val * 0.7
            bar = Rectangle(
                width=bar_width,
                height=bar_height,
                fill_color=colors_bar[i % len(colors_bar)],
                fill_opacity=0.85,
                stroke_width=1,
                stroke_color="#585b70",
            )
            bar.move_to(RIGHT * start_x + RIGHT * i * (bar_width * 1.6))
            bar.align_to(ORIGIN, DOWN)
            bars.add(bar)

        bars.move_to(RIGHT * 3 + DOWN * 1)

        # Add a subtle glow beneath
        spectrum_glow = Rectangle(
            width=total_width + 0.5,
            height=0.03,
            color=accent_green,
            fill_opacity=0.4,
            stroke_width=0,
        )
        spectrum_glow.next_to(bars, DOWN, buff=0.02)

        spectrum_label = Text("Spectrum", font_size=18, color=accent_green)
        spectrum_label.next_to(bars, UP, buff=0.15)

        recap_spectrum_group = VGroup(bars, spectrum_glow, spectrum_label)

        # --- 4. Recap Phasor (center left) ---
        phasor_circle = Circle(radius=0.45, color=accent_teal, stroke_width=2)
        phasor_circle.move_to(LEFT * 0.8 + DOWN * 0.2)

        phasor_arrow = Arrow(
            start=phasor_circle.get_center(),
            end=phasor_circle.get_center() + RIGHT * 0.4 + UP * 0.2,
            color=accent_peach,
            tip_length=0.12,
            stroke_width=2.5,
        )

        phasor_label = Text("Phasor", font_size=16, color=accent_teal)
        phasor_label.next_to(phasor_circle, DOWN, buff=0.1)

        recap_phasor = VGroup(phasor_circle, phasor_arrow, phasor_label)

        # --- 5. Recap Formula (center right) ---
        formula = MathTex(
            r"\hat{f}(\xi) = \int f(x) e^{-2\pi i x \xi} dx",
            font_size=28,
            color=accent_peach,
        )
        formula.move_to(RIGHT * 0.8 + DOWN * 0.2)

        formula_bg = BackgroundRectangle(
            formula, color="#181825", fill_opacity=0.8, buff=0.15
        )
        formula_label = Text("Formula", font_size=16, color=accent_peach)
        formula_label.next_to(formula, DOWN, buff=0.1)

        recap_formula = VGroup(formula_bg, formula, formula_label)

        # --- 6. Thank You text ---
        thanks = Text("Thank you", font_size=28, color=accent_peach)
        thanks.move_to(DOWN * 2.2)

        # Decorative dots
        dot1 = Dot(radius=0.06, color=accent_blue)
        dot2 = Dot(radius=0.06, color=accent_green)
        dot3 = Dot(radius=0.06, color=accent_pink)
        dots = VGroup(dot1, dot2, dot3).arrange(RIGHT, buff=0.2)
        dots.next_to(thanks, DOWN, buff=0.2)

        # --- 7. Glowing frequency spectrum background ---
        glow_axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 1.2, 0.5],
            x_length=7,
            y_length=0.4,
            axis_config={
                "stroke_width": 0.5,
                "color": "#585b70",
                "include_numbers": False,
                "include_ticks": False,
            },
        )
        glow_axes.move_to(DOWN * 1.2)

        # Create a spectrum glow using a polygon
        glow_func = glow_axes.plot(
            lambda x: (
                0.3 * np.exp(-0.2 * (x - 2) ** 2)
                + 0.6 * np.exp(-0.15 * (x - 5) ** 2)
                + 0.4 * np.exp(-0.25 * (x - 7) ** 2)
            ),
            color=accent_mauve,
            stroke_width=1,
        )

        # Fill area under the curve
        glow_fill = glow_axes.get_area(glow_func, color=accent_mauve, opacity=0.15)

        glow_bg = VGroup(glow_axes, glow_func, glow_fill)
        glow_bg.set_opacity(0.5)

        # --- Animation sequence ---
        total_duration = 5.0

        # Fade in background glow first
        self.play(FadeIn(glow_bg, scale=0.8), run_time=0.7)

        # Animate title
        self.play(Write(title, reverse=False), run_time=0.6)
        self.play(GrowFromCenter(underline), run_time=0.3)

        # Fade in recap elements
        self.play(
            FadeIn(recap_wave_group, shift=UP * 0.3),
            FadeIn(recap_spectrum_group, shift=UP * 0.3),
            run_time=0.6,
        )

        self.play(
            FadeIn(recap_phasor, shift=UP * 0.3),
            FadeIn(recap_formula, shift=UP * 0.3),
            run_time=0.5,
        )

        # Phasor rotation
        self.play(
            Rotate(phasor_arrow, angle=TAU, about_point=phasor_circle.get_center()),
            run_time=0.6,
        )

        # Thank you
        self.play(Write(thanks), GrowFromCenter(dots), run_time=0.5)

        # Indicate title
        self.play(Indicate(title, color=accent_mauve, scale_factor=1.03), run_time=0.3)

        # Final glow effect on spectrum
        self.play(glow_bg.animate.set_opacity(0.8), run_time=0.4)

        # Hold
        self.wait(0.5)

        # Total: 0.7 + 0.6 + 0.3 + 0.6 + 0.5 + 0.6 + 0.5 + 0.3 + 0.4 + 0.5 = 5.0
