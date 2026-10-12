import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Signals as Waves ---
        self.clear()

        # ── Color palette ──
        BG_COLOR = "#181825"
        AXIS_COLOR = "#CDD6F4"
        WAVE_COLOR = "#89b4fa"
        AMP_BRACE_COLOR = "#fab387"
        WL_BRACE_COLOR = "#f38ba8"
        TEXT_COLOR = "#CDD6F4"
        SUBTLE_COLOR = "#585b70"

        # Set background
        self.camera.background_color = BG_COLOR

        # ── 1. Axes ──
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=5,
            axis_config={
                "color": AXIS_COLOR,
                "stroke_width": 2,
                "include_tip": False,
            },
            tips=False,
        )
        axes.center()

        # Axis labels
        x_label = axes.get_x_axis_label(
            Tex("Time", color=TEXT_COLOR, font_size=36),
            direction=RIGHT,
            buff=0.3,
        )
        y_label = axes.get_y_axis_label(
            Tex("Amplitude", color=TEXT_COLOR, font_size=36),
            direction=UP,
            buff=0.3,
        )

        # ── 2. Sine wave ──
        sine_wave = axes.plot(
            lambda x: np.sin(x),
            x_range=[-4, 4],
            color=WAVE_COLOR,
            stroke_width=3.5,
        )

        # ── 3. Amplitude brace (vertical) ──
        # Brace from trough to peak at x = π/2
        peak_point = axes.c2p(np.pi / 2, 1)
        trough_point = axes.c2p(np.pi / 2, -1)
        amp_brace = BraceBetweenPoints(
            peak_point,
            trough_point,
            direction=RIGHT,
            color=AMP_BRACE_COLOR,
            buff=0.15,
        )
        amp_label = amp_brace.get_tex(r"A").set_color(AMP_BRACE_COLOR)
        amp_text = Text("Amplitude", font_size=28, color=AMP_BRACE_COLOR)
        amp_text.next_to(amp_label, RIGHT, buff=0.15)

        # ── 4. Wavelength brace (horizontal) ──
        # One full cycle from -π to +π
        cycle_start = axes.c2p(-np.pi, 0)
        cycle_end = axes.c2p(np.pi, 0)
        wl_brace = BraceBetweenPoints(
            cycle_start,
            cycle_end,
            direction=DOWN,
            color=WL_BRACE_COLOR,
            buff=0.15,
        )
        wl_label = wl_brace.get_tex(r"\lambda").set_color(WL_BRACE_COLOR)
        wl_text = Text("Wavelength", font_size=28, color=WL_BRACE_COLOR)
        wl_text.next_to(wl_label, DOWN, buff=0.15)

        # ── 5. Title ──
        title = Text(
            "Signals as Waves",
            font_size=42,
            color=TEXT_COLOR,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.4)

        # ── 6. Subtle origin dot ──
        origin_dot = Dot(axes.c2p(0, 0), radius=0.06, color=SUBTLE_COLOR)

        # ══════════════════════════════════════════════
        # ANIMATIONS — total duration: 6.5s
        # ══════════════════════════════════════════════

        # Phase 1: Title (0.8s)
        self.play(Write(title), run_time=0.8)

        # Phase 2: Axes + labels draw in (1.2s)
        self.play(
            Create(axes, run_time=1.0),
            FadeIn(x_label, shift=UP * 0.2, run_time=0.8),
            FadeIn(y_label, shift=RIGHT * 0.2, run_time=0.8),
            FadeIn(origin_dot, run_time=0.6),
            run_time=1.2,
        )

        # Phase 3: Sine wave draws in (1.5s)
        self.play(Create(sine_wave), run_time=1.5)

        # Phase 4: Amplitude brace appears (1.0s)
        self.play(
            GrowFromCenter(amp_brace),
            FadeIn(amp_label, shift=RIGHT * 0.2),
            FadeIn(amp_text, shift=RIGHT * 0.2),
            run_time=1.0,
        )

        # Phase 5: Wavelength brace appears (1.0s)
        self.play(
            GrowFromCenter(wl_brace),
            FadeIn(wl_label, shift=DOWN * 0.2),
            FadeIn(wl_text, shift=DOWN * 0.2),
            run_time=1.0,
        )

        # Phase 6: Hold / settle (1.0s)
        self.wait(1.0)
        # --- Scene 2: Combining Waves ---
        # Style Constants
        BG_COLOR = "#181825"
        COLOR_LOW = "#CBA6F7"
        COLOR_MID = "#89B4FA"
        COLOR_HIGH = "#A6E3A1"
        COLOR_BOX = "#45475A"
        COLOR_RES = "#FAB387"
        COLOR_TITLE = "#CDD6F4"

        self.camera.background_color = BG_COLOR

        # --- 1. Title ---
        title = Text("Combining Waves", font="Sans", font_size=36, color=COLOR_TITLE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.5), run_time=0.7)

        # --- 2. Define Waves and Labels ---
        # Low Frequency
        func_low = FunctionGraph(
            lambda x: np.sin(0.5 * x),
            x_range=[-2, 2, 0.05],
            color=COLOR_LOW,
            stroke_width=2.5,
        )
        label_low = MathTex("f_1", color=COLOR_LOW).next_to(func_low, LEFT, buff=0.2)
        group_low = VGroup(func_low, label_low)

        # Mid Frequency
        func_mid = FunctionGraph(
            lambda x: np.sin(x),
            x_range=[-2, 2, 0.05],
            color=COLOR_MID,
            stroke_width=2.5,
        )
        label_mid = MathTex("f_2", color=COLOR_MID).next_to(func_mid, LEFT, buff=0.2)
        group_mid = VGroup(func_mid, label_mid)

        # High Frequency
        func_high = FunctionGraph(
            lambda x: np.sin(2 * x),
            x_range=[-2, 2, 0.05],
            color=COLOR_HIGH,
            stroke_width=2.5,
        )
        label_high = MathTex("f_3", color=COLOR_HIGH).next_to(func_high, LEFT, buff=0.2)
        group_high = VGroup(func_high, label_high)

        # Position waves on the left
        waves_group = VGroup(group_low, group_mid, group_high)
        waves_group.arrange(DOWN, buff=0.6)
        waves_group.move_to(LEFT * 4)

        # --- 3. Animate Waves Appearing ---
        self.play(
            LaggedStart(
                FadeIn(group_low, shift=RIGHT * 0.2),
                FadeIn(group_mid, shift=RIGHT * 0.2),
                FadeIn(group_high, shift=RIGHT * 0.2),
                lag_ratio=0.6,
            ),
            run_time=2.4,
        )

        # --- 4. Sum Box and Arrows ---
        box = Rectangle(
            width=2.0,
            height=3.2,
            fill_color=COLOR_BOX,
            fill_opacity=1.0,
            stroke_color="#585b70",
            stroke_width=2,
        )
        sigma = MathTex(r"\Sigma", font_size=60, color="#cdd6f4").move_to(
            box.get_center()
        )
        sum_group = VGroup(box, sigma).move_to(ORIGIN)

        # Create arrows from waves to box
        start_l = group_low.get_right()
        start_m = group_mid.get_right()
        start_h = group_high.get_right()
        end_b_l = box.get_left() + DOWN * 0.9
        end_b_m = box.get_left()
        end_b_h = box.get_left() + UP * 0.9

        arrows_in = VGroup(
            Arrow(
                start_l,
                end_b_l,
                buff=0.2,
                color=COLOR_LOW,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15,
            ),
            Arrow(
                start_m,
                end_b_m,
                buff=0.2,
                color=COLOR_MID,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15,
            ),
            Arrow(
                start_h,
                end_b_h,
                buff=0.2,
                color=COLOR_HIGH,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15,
            ),
        )

        self.play(DrawBorderThenFill(box), Write(sigma), run_time=0.8)
        self.play(FadeIn(arrows_in, shift=RIGHT * 0.5), run_time=0.8)

        # --- 5. Combine Animation (Waves flow in) ---
        self.play(
            FadeOut(VGroup(group_low, group_mid, group_high, arrows_in)), run_time=0.8
        )

        # --- 6. Output Arrow and Result Wave ---
        start_out = box.get_right()
        end_out = box.get_right() + RIGHT * 1.5
        arrow_out = Arrow(
            start_out, end_out, buff=0.2, color=COLOR_RES, stroke_width=2.5
        )

        # Result Wave
        func_res = FunctionGraph(
            lambda x: np.sin(0.5 * x) + np.sin(x) + np.sin(2 * x),
            x_range=[-2, 2, 0.01],
            color=COLOR_RES,
            stroke_width=3.5,
        )

        # Position result wave to the right
        func_res.move_to(RIGHT * 4)
        func_res.shift(UP * 0.3)

        self.play(GrowArrow(arrow_out), run_time=0.6)

        # Draw the complex wave
        self.play(Create(func_res), run_time=1.2)

        # Equation Label
        eq_label = MathTex("f_1 + f_2 + f_3", color=COLOR_RES, font_size=30)
        eq_label.next_to(func_res, DOWN, buff=0.5)
        self.play(FadeIn(eq_label), run_time=0.6)

        # --- 7. Highlight and Hold ---
        self.play(Indicate(func_res, color=WHITE, scale_factor=1.05), run_time=0.5)
        self.wait(0.5)
        # --- Scene 3: The Time Domain View ---
        self.clear()

        # 1. Axes: Time vs Amplitude
        time_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=5,
            axis_config={
                "color": "#CDD6F4",
                "include_tip": True,
                "tip_length": 0.2,
                "tip_width": 0.2,
            },
            x_axis_config={
                "include_numbers": True,
                "font_size": 24,
                "color": "#A6ADC8",
            },
            y_axis_config={
                "include_numbers": True,
                "font_size": 24,
                "color": "#A6ADC8",
            },
        )

        # 2. Grid lines for visual clarity
        grid = NumberPlane(
            x_range=[0, 10, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=5,
            background_line_style={
                "stroke_color": "#45475A",
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            },
            axis_config={"stroke_opacity": 0},
        )

        # 3. Complex wave function: sum of sinusoids
        def complex_wave_func(t):
            return np.sin(t) + 0.5 * np.sin(3 * t) + 0.2 * np.sin(5 * t)

        complex_wave = time_axes.plot(
            complex_wave_func,
            x_range=[0, 10, 0.01],
            color="#89B4FA",
            stroke_width=3,
        )

        # 4. Axis labels
        time_label = MathTex(r"t", font_size=36, color="#A6ADC8")
        time_label.next_to(time_axes.x_axis.get_end(), DR, buff=0.15)

        amp_label = MathTex(r"A(t)", font_size=36, color="#A6ADC8")
        amp_label.next_to(time_axes.y_axis.get_end(), UL, buff=0.15)

        # 5. Title
        title = Text(
            "The Time Domain View",
            font_size=36,
            color="#CDD6F4",
        )
        title.to_edge(UP, buff=0.35)

        # 6. Description text
        desc_text = Text(
            "Signal's amplitude at every point in time",
            font_size=22,
            color="#6C7086",
        )
        desc_text.to_edge(DOWN, buff=0.35)

        # 7. A glowing "scope trace" effect
        trace_dot = Dot(
            time_axes.c2p(0, complex_wave_func(0)),
            radius=0.08,
            color="#FAB387",
        )
        trace_dot.set_z_index(2)

        glow = Dot(
            time_axes.c2p(0, complex_wave_func(0)),
            radius=0.2,
            color="#FAB387",
            fill_opacity=0.3,
        )

        # === ANIMATIONS ===
        # Phase 1: Title fade in (0.8s)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)

        # Phase 2: Grid + Axes draw in (1.2s)
        self.play(
            Create(grid, lag_ratio=0.02),
            Create(time_axes, lag_ratio=0.02),
            run_time=1.2,
        )

        # Phase 3: Labels appear (0.7s)
        self.play(
            FadeIn(time_label, shift=RIGHT * 0.2),
            FadeIn(amp_label, shift=UP * 0.2),
            run_time=0.7,
        )

        # Phase 4: Complex wave draws in (1.5s)
        self.play(Create(complex_wave), run_time=1.5)

        # Phase 5: Description text (0.6s)
        self.play(FadeIn(desc_text, shift=UP * 0.15), run_time=0.6)

        # Phase 6: Trace dot traveling across the wave (3.0s)
        self.add(glow)
        self.add(trace_dot)

        trace_tracker = ValueTracker(0)
        trace_dot.add_updater(
            lambda d: d.move_to(
                time_axes.c2p(
                    trace_tracker.get_value(),
                    complex_wave_func(trace_tracker.get_value()),
                )
            )
        )
        glow.add_updater(
            lambda g: g.move_to(
                time_axes.c2p(
                    trace_tracker.get_value(),
                    complex_wave_func(trace_tracker.get_value()),
                )
            )
        )

        self.play(
            trace_tracker.animate.set_value(10),
            run_time=3.0,
            rate_func=linear,
        )

        trace_dot.clear_updaters()
        glow.clear_updaters()

        # Phase 7: Final hold (1.7s)
        self.wait(1.7)
        # --- Scene 4: The Transform Operation ---
        self.clear()

        # --- Setup Colors ---
        color_wave = "#89b4fa"
        color_formula = "#CBA6F7"
        color_arrow = "#EBCB8B"
        color_axes = "#94e2d5"
        color_freq_1 = "#fab387"
        color_freq_2 = "#a6e3a1"
        color_beam = "#f38ba8"

        # 1. Objects
        # Input Wave (Time Domain)
        input_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=4,
            y_length=3,
            tips=False,
            axis_config={"color": color_axes, "stroke_width": 2},
        )
        input_wave = input_axes.plot(
            lambda x: np.sin(x) + 0.5 * np.cos(2 * x), color=color_wave, stroke_width=3
        )
        input_title = Text("Time Domain", font_size=24, color=color_wave).next_to(
            input_axes, UP, buff=0.2
        )
        input_group = VGroup(input_axes, input_wave, input_title)
        input_group.move_to(LEFT * 4.5)

        # FT Formula (Glowing center)
        ft_formula = MathTex(
            r"\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x) e^{-2\pi i x \xi} dx",
            font_size=36,
            color=color_formula,
        )
        ft_formula_background = BackgroundRectangle(
            ft_formula, color=BLACK, fill_opacity=0.6, buff=0.1
        )
        ft_group = VGroup(ft_formula_background, ft_formula)
        ft_group.move_to(ORIGIN)

        # Output Axes (Frequency Domain)
        output_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[-0.2, 1.2, 0.5],
            x_length=4,
            y_length=3,
            tips=False,
            axis_config={"color": color_axes, "stroke_width": 2},
        )
        # Frequency spectrum spikes
        stems = VGroup(
            Line(
                output_axes.c2p(1, 0),
                output_axes.c2p(1, 1),
                color=color_freq_1,
                stroke_width=3,
            ),
            Line(
                output_axes.c2p(2, 0),
                output_axes.c2p(2, 0.5),
                color=color_freq_2,
                stroke_width=3,
            ),
        )
        dots = VGroup(
            Dot(output_axes.c2p(1, 1), color=color_freq_1, radius=0.1),
            Dot(output_axes.c2p(2, 0.5), color=color_freq_2, radius=0.08),
        )
        output_title = Text("Frequency Domain", font_size=24, color=color_axes).next_to(
            output_axes, UP, buff=0.2
        )
        output_group = VGroup(output_axes, stems, dots, output_title)
        output_group.move_to(RIGHT * 4.5)

        # Transform Arrow
        transform_arrow = Arrow(
            start=LEFT * 2.5,
            end=RIGHT * 2.5,
            color=color_arrow,
            stroke_width=4,
            buff=0.1,
        )

        # 2. Animations (Total duration: 8.0s)

        # Part 1: Input Wave moves in (1.5s)
        self.play(FadeIn(input_group, shift=RIGHT * 2), run_time=1.5)

        # Part 2: FT Formula appears and glows (1.5s)
        self.play(FadeIn(ft_formula_background), Write(ft_formula), run_time=1.5)

        # Part 3: Arrow and Output appear (2.0s)
        self.play(
            Create(transform_arrow), FadeIn(output_group, shift=LEFT * 2), run_time=2.0
        )

        # Part 4: Beam of light connecting input → formula → output (1.5s)
        beam_path_1 = Line(
            input_group.get_right(), ft_group.get_left(), color=color_beam
        )
        beam_path_2 = Line(
            ft_group.get_right(), output_group.get_left(), color=color_beam
        )

        self.play(
            ShowPassingFlash(beam_path_1.set_stroke(width=6), time_width=0.5),
            ShowPassingFlash(beam_path_2.set_stroke(width=6), time_width=0.5),
            Indicate(ft_formula, color=color_beam, scale_factor=1.1),
            run_time=1.5,
        )

        # Part 5: Final hold (1.5s)
        self.wait(1.5)
        # --- Scene 5: The Frequency Domain View ---
        self.clear()
        # Color palette
        AXIS_COLOR = "#CDD6F4"
        LABEL_COLOR = "#A6ADC8"
        PEAK1_COLOR = "#CBA6F7"
        PEAK2_COLOR = "#89B4FA"
        PEAK3_COLOR = "#A6E3A1"

        # 1. Axes
        freq_axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 1.5, 0.5],
            x_length=9,
            y_length=4.5,
            axis_config={
                "color": AXIS_COLOR,
                "include_tip": True,
                "tip_length": 0.15,
            },
        ).shift(DOWN * 0.3)

        # 2. Axis labels
        x_label = MathTex(r"	ext{Frequency (Hz)}", font_size=32, color=LABEL_COLOR)
        x_label.next_to(freq_axes.x_axis.get_end(), RIGHT, buff=0.3)
        y_label = MathTex(
            r"	ext{Magnitude } |F(f)|", font_size=32, color=LABEL_COLOR
        )
        y_label.next_to(freq_axes.y_axis.get_end(), UP, buff=0.3)

        # 3. Tick labels
        x_tick_labels = VGroup()
        for freq in range(1, 6):
            lab = MathTex(str(freq), font_size=24, color=LABEL_COLOR)
            lab.next_to(freq_axes.c2p(freq, 0), DOWN, buff=0.15)
            x_tick_labels.add(lab)

        # 4. Peaks
        peak_1 = Line(
            start=freq_axes.c2p(1, 0),
            end=freq_axes.c2p(1, 1.0),
            color=PEAK1_COLOR,
            stroke_width=6,
        )
        peak_1_dot = Dot(freq_axes.c2p(1, 1.0), radius=0.07, color=PEAK1_COLOR)
        peak_1_label = MathTex("1\	ext{ Hz}", font_size=24, color=PEAK1_COLOR)
        peak_1_label.next_to(peak_1_dot, UP, buff=0.15)

        peak_2 = Line(
            start=freq_axes.c2p(3, 0),
            end=freq_axes.c2p(3, 0.5),
            color=PEAK2_COLOR,
            stroke_width=6,
        )
        peak_2_dot = Dot(freq_axes.c2p(3, 0.5), radius=0.07, color=PEAK2_COLOR)
        peak_2_label = MathTex("3\	ext{ Hz}", font_size=24, color=PEAK2_COLOR)
        peak_2_label.next_to(peak_2_dot, UP, buff=0.15)

        peak_3 = Line(
            start=freq_axes.c2p(5, 0),
            end=freq_axes.c2p(5, 0.2),
            color=PEAK3_COLOR,
            stroke_width=6,
        )
        peak_3_dot = Dot(freq_axes.c2p(5, 0.2), radius=0.07, color=PEAK3_COLOR)
        peak_3_label = MathTex("5\	ext{ Hz}", font_size=24, color=PEAK3_COLOR)
        peak_3_label.next_to(peak_3_dot, UP, buff=0.15)

        all_peaks = VGroup(
            peak_1,
            peak_1_dot,
            peak_1_label,
            peak_2,
            peak_2_dot,
            peak_2_label,
            peak_3,
            peak_3_dot,
            peak_3_label,
        )

        # 5. Title
        title = Text("Frequency Domain", font_size=36, color=AXIS_COLOR)
        title.to_edge(UP, buff=0.4)

        # ===== ANIMATIONS: exactly 10.0s =====
        self.play(Create(freq_axes, run_time=1.5))
        self.play(
            Write(x_label, run_time=0.5),
            Write(y_label, run_time=0.5),
            FadeIn(x_tick_labels, run_time=0.5),
        )
        self.play(Write(title, run_time=0.5))
        self.play(Create(peak_1, run_time=1.0))
        self.play(
            FadeIn(peak_1_dot, run_time=0.5),
            Write(peak_1_label, run_time=0.5),
        )
        self.play(Create(peak_2, run_time=1.0))
        self.play(
            FadeIn(peak_2_dot, run_time=0.5),
            Write(peak_2_label, run_time=0.5),
        )
        self.play(Create(peak_3, run_time=1.0))
        self.play(
            FadeIn(peak_3_dot, run_time=0.5),
            Write(peak_3_label, run_time=0.5),
        )
        self.play(Indicate(all_peaks, color=YELLOW, scale_factor=1.05, run_time=1.0))
        self.wait(2.0)
        # --- Scene 6: Magnitude and Phase ---
        # Colors
        PEAK_COLOR = "#89b4fa"
        MAG_COLOR = "#fab387"
        PHASE_CIRCLE_COLOR = "#a6e3a1"
        PHASOR_COLOR = "#f38ba8"

        # 1. Peak Emergence
        baseline = Line(start=LEFT * 2.5, end=RIGHT * 2.5, color=WHITE)
        baseline.to_edge(DOWN, buff=1.5)

        peak = Rectangle(
            width=0.6,
            height=3,
            fill_color=PEAK_COLOR,
            fill_opacity=0.8,
            stroke_width=2,
        )
        peak.move_to(baseline.get_center() + UP * 1.5)

        peak_label = Text("f = 3 Hz", font_size=24, color=PEAK_COLOR)
        peak_label.next_to(peak, DOWN, buff=0.1)

        self.play(Create(baseline), run_time=0.5)
        self.play(GrowFromEdge(peak, DOWN), run_time=1.0)
        self.play(FadeIn(peak_label), run_time=0.4)

        # 2. Magnitude Reveal — fix: create Text separately, then position manually
        mag_brace = Brace(peak, direction=LEFT, color=MAG_COLOR)
        mag_label = Text("Magnitude", font_size=24, color=MAG_COLOR)
        mag_label.next_to(mag_brace, LEFT, buff=0.1)

        self.play(GrowFromCenter(mag_brace), FadeIn(mag_label), run_time=1.2)
        self.play(Indicate(mag_brace, color=MAG_COLOR), run_time=0.6)

        # 3. Phase Demonstration
        phase_circle = Circle(radius=0.8, color=PHASE_CIRCLE_COLOR, stroke_width=2)
        phase_circle.shift(RIGHT * 3)

        tick = Line(ORIGIN, RIGHT * 0.2, color=PHASE_CIRCLE_COLOR, stroke_width=4)
        tick.move_to(phase_circle.get_right() + RIGHT * 0.1)

        phasor = Arrow(
            start=phase_circle.get_center(),
            end=phase_circle.get_center() + UP * 0.6,
            buff=0,
            color=PHASOR_COLOR,
            stroke_width=4,
        )

        phase_label = Text("Phase", font_size=24, color=PHASE_CIRCLE_COLOR)
        phase_label.next_to(phase_circle, DOWN, buff=0.3)

        self.play(FadeIn(phase_circle, scale=0.8), run_time=0.5)
        self.play(FadeIn(tick), run_time=0.3)
        self.play(GrowFromCenter(phasor), run_time=0.4)
        self.play(FadeIn(phase_label), run_time=0.3)

        # Rotate Phasor ~120 degrees
        self.play(
            Rotate(
                phasor,
                angle=2 * PI / 3,
                about_point=phase_circle.get_center(),
            ),
            run_time=1.5,
        )

        # Draw arc to highlight angle
        arc = Arc(
            radius=0.4,
            start_angle=PI / 2,
            angle=2 * PI / 3,
            color=PHASOR_COLOR,
            stroke_width=2,
        )
        arc.move_arc_center_to(phase_circle.get_center())

        self.play(Create(arc), run_time=0.6)
        self.wait(0.4)

        # Final emphasis
        self.play(Circumscribe(mag_brace, color=MAG_COLOR), run_time=0.45)
        self.play(Circumscribe(phase_circle, color=PHASE_CIRCLE_COLOR), run_time=0.45)
        self.wait(0.4)
        # --- Scene 7: Reconstructing the Signal ---
        # === COLORS ===
        BG = "#181825"
        BOX_COLOR = "#45475a"
        WAVE_COLOR = "#fab387"  # accent_3 - warm orange
        SIGMA_COLOR = "#89b4fa"  # accent_5 - blue
        PEAK_COLORS = ["#89b4fa", "#a6e3a1", "#94e2d5", "#f38ba8", "#fab387"]
        TEXT_COLOR = "#cdd6f4"

        self.camera.background_color = BG

        # === OBJECTS ===

        # --- Central Summation Box ---
        sum_box = Rectangle(
            width=1.6,
            height=3.5,
            color=BOX_COLOR,
            fill_color=BOX_COLOR,
            fill_opacity=0.15,
            stroke_width=2.5,
        )
        sigma_symbol = MathTex(r"\Sigma", color=SIGMA_COLOR, font_size=72)
        sum_group = VGroup(sum_box, sigma_symbol).move_to(ORIGIN)

        # --- Frequency Peaks (left side) ---
        num_peaks = 5
        peak_heights = [0.8, 1.2, 2.2, 1.5, 1.0]
        peaks = VGroup()
        for i in range(num_peaks):
            bar = RoundedRectangle(
                corner_radius=0.05,
                width=0.35,
                height=peak_heights[i],
                color=PEAK_COLORS[i],
                fill_opacity=0.85,
                stroke_width=1.5,
            )
            peaks.add(bar)
        peaks.arrange(RIGHT, buff=0.18)
        peaks.move_to(LEFT * 5)

        # Labels
        peaks_label = Text("Frequency Components", font_size=26, color=TEXT_COLOR)
        peaks_label.next_to(peaks, UP, buff=0.35)

        # Dashed guide arrows from peaks to box
        guide_arrows = VGroup()
        for i, peak in enumerate(peaks):
            arrow = Arrow(
                start=peak.get_right(),
                end=sum_box.get_left() + UP * (1.2 - i * 0.6),
                color=PEAK_COLORS[i],
                stroke_width=2,
                tip_length=0.15,
                buff=0.1,
                max_tip_length_to_length_ratio=0.2,
            )
            guide_arrows.add(arrow)

        # --- Reconstructed Wave (right side) ---
        def complex_wave(x):
            return 0.5 * np.sin(2 * x) + 0.3 * np.sin(5 * x) + 0.2 * np.cos(3 * x)

        wave = FunctionGraph(
            complex_wave,
            x_range=[-2.5, 2.5],
            color=WAVE_COLOR,
            stroke_width=4,
        )

        # Subtle axes for wave context
        wave_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1.2, 1.2, 0.5],
            x_length=4.5,
            y_length=2.5,
            axis_config={"color": GREY_D, "stroke_width": 1.5},
            tips=False,
        )
        wave_axes.move_to(RIGHT * 5)
        wave.move_to(RIGHT * 5)

        wave_label = Text("Reconstructed Signal", font_size=26, color=WAVE_COLOR)
        wave_label.next_to(wave_axes, UP, buff=0.3)

        # Output arrow from box to wave area
        output_arrow = Arrow(
            start=sum_box.get_right() + RIGHT * 0.1,
            end=wave_axes.get_left() + LEFT * 0.1,
            color=TEXT_COLOR,
            stroke_width=2,
            buff=0.0,
        )

        # === ANIMATIONS (total: 8.5s) ===

        # Phase 1: Introduce the summation box (0.0s - 0.8s) → 0.8s
        self.play(
            GrowFromCenter(sum_box),
            FadeIn(sigma_symbol, scale=0.5),
            run_time=0.8,
        )

        # Phase 2: Show frequency peaks on left (0.8s - 2.3s) → 1.5s
        self.play(
            LaggedStart(
                *[GrowFromCenter(p) for p in peaks],
                lag_ratio=0.15,
            ),
            FadeIn(peaks_label),
            run_time=1.5,
        )

        # Phase 3a: Show guide arrows briefly (2.3s - 3.0s) → 0.7s
        self.play(
            LaggedStart(
                *[Create(a) for a in guide_arrows],
                lag_ratio=0.12,
            ),
            run_time=0.7,
        )

        # Phase 3b: Peaks fly into the summation box (3.0s - 5.2s) → 2.2s
        fly_animations = []
        for peak in peaks:
            peak.generate_target()
            peak.target.move_to(sum_box.get_center())
            peak.target.scale(0.05)
            peak.target.set_opacity(0)
            fly_animations.append(MoveToTarget(peak))

        self.play(
            LaggedStart(*fly_animations, lag_ratio=0.2, rate_func=smooth),
            FadeOut(guide_arrows, run_time=0.6),
            FadeOut(peaks_label, run_time=0.4),
            run_time=2.2,
        )

        # Phase 4: Box pulses — summation effect (5.2s - 6.1s) → 0.9s
        self.play(
            Flash(
                sum_box.get_center(),
                color=SIGMA_COLOR,
                line_length=0.4,
                num_lines=12,
            ),
            Indicate(sigma_symbol, color=SIGMA_COLOR, scale_factor=1.3),
            run_time=0.9,
        )

        # Phase 4b: Output arrow appears (6.1s - 6.5s) → 0.4s
        self.play(
            FadeIn(output_arrow, shift=LEFT * 0.3),
            run_time=0.4,
        )

        # Phase 5: Wave draws on the right (6.5s - 8.2s) → 1.7s
        self.play(
            FadeIn(wave_axes, run_time=0.5),
            Create(wave, run_time=1.7),
            FadeIn(wave_label, run_time=0.5),
        )

        # Phase 6: Final beat (8.2s - 8.5s) → 0.3s
        self.wait(0.3)
        # --- Scene 8: Real-World Application ---
        # ── Color Palette (Catppuccin Mocha) ──
        BG = "#181825"
        BLUE = "#89b4fa"
        PEACH = "#fab387"
        MAUVE = "#cba6f7"
        GREEN = "#a6e3a1"
        SURFACE = "#585b70"
        TEXT = "#cdd6f4"

        self.camera.background_color = BG

        # ── 1. Music Wave (complex waveform) ──
        music_axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=3.5,
            y_length=2.5,
            axis_config={"color": SURFACE, "stroke_width": 1.5},
            tips=False,
        )
        music_graph = music_axes.plot(
            lambda x: np.sin(x * 3) + 0.5 * np.sin(x * 9) + 0.3 * np.sin(x * 15),
            color=BLUE,
            stroke_width=2.5,
        )
        music_label = Text("Music Signal", font_size=28, color=BLUE)
        music_label.next_to(music_axes, DOWN, buff=0.3)
        music_group = VGroup(music_axes, music_graph, music_label)
        music_group.move_to(LEFT * 4.5)

        # ── 2. FFT Box ──
        fft_box = RoundedRectangle(
            width=2.2,
            height=3.2,
            corner_radius=0.25,
            color=SURFACE,
            fill_color="#1e1e2e",
            fill_opacity=0.85,
            stroke_width=2.5,
        )
        fft_label = Text("FFT", font_size=32, color=TEXT, weight=BOLD)
        fft_box_group = VGroup(fft_box, fft_label).move_to(ORIGIN)

        # ── 3. Arrow from wave to FFT ──
        arrow1 = Arrow(
            start=music_axes.get_right() + RIGHT * 0.15,
            end=fft_box.get_left(),
            buff=0.15,
            color=TEXT,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.12,
        )

        # ── 4. Frequency Spectrum Axes ──
        spectrum_axes = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 1.2, 0.5],
            x_length=5,
            y_length=2.8,
            axis_config={
                "color": SURFACE,
                "stroke_width": 1.5,
                "include_numbers": False,
            },
            tips=False,
        )
        x_nums = VGroup()
        for val in [0, 5, 10, 15, 20]:
            num = Text(str(val), font_size=18, color=TEXT)
            num.next_to(spectrum_axes.c2p(val, 0), DOWN, buff=0.15)
            x_nums.add(num)
        freq_label = Text("Frequency (Hz)", font_size=20, color=TEXT)
        freq_label.next_to(spectrum_axes, DOWN, buff=0.45)

        # Spectrum bars (binned spectrum)
        bar_width = 0.35
        freqs = [1.5, 4, 7, 10, 13, 16.5, 19]
        amps = [0.95, 0.7, 0.55, 0.85, 0.45, 0.6, 0.3]
        bar_colors = [MAUVE, MAUVE, PEACH, PEACH, GREEN, GREEN, GREEN]
        bars = VGroup()
        for f, a, c in zip(freqs, amps, bar_colors):
            bottom = spectrum_axes.c2p(f, 0)
            top = spectrum_axes.c2p(f, a)
            bar = Rectangle(
                width=bar_width,
                height=top[1] - bottom[1],
                fill_color=c,
                fill_opacity=0.85,
                stroke_color=c,
                stroke_width=1.5,
            )
            bar.move_to((bottom + top) / 2)
            bars.add(bar)

        spectrum_group = VGroup(spectrum_axes, x_nums, bars, freq_label)
        spectrum_group.move_to(RIGHT * 4.5)

        # ── 5. Arrow from FFT to spectrum ──
        arrow2 = Arrow(
            start=fft_box.get_right(),
            end=spectrum_axes.get_left() + LEFT * 0.15,
            buff=0.15,
            color=TEXT,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.12,
        )

        # ── 6. Highlight Regions (labeled) ──
        bass_rect = Rectangle(
            width=1.8,
            height=3.4,
            fill_color=MAUVE,
            fill_opacity=0.12,
            stroke_color=MAUVE,
            stroke_width=2,
            stroke_opacity=0.7,
        )
        bass_rect.move_to(spectrum_axes.c2p(2.5, 0.6))
        bass_label = Text("Bass", font_size=24, color=MAUVE, weight=BOLD)
        bass_label.next_to(bass_rect, UP, buff=0.15)

        mid_rect = Rectangle(
            width=2.2,
            height=3.4,
            fill_color=PEACH,
            fill_opacity=0.12,
            stroke_color=PEACH,
            stroke_width=2,
            stroke_opacity=0.7,
        )
        mid_rect.move_to(spectrum_axes.c2p(8.5, 0.6))
        mid_label = Text("Mid", font_size=24, color=PEACH, weight=BOLD)
        mid_label.next_to(mid_rect, UP, buff=0.15)

        treble_rect = Rectangle(
            width=2.6,
            height=3.4,
            fill_color=GREEN,
            fill_opacity=0.12,
            stroke_color=GREEN,
            stroke_width=2,
            stroke_opacity=0.7,
        )
        treble_rect.move_to(spectrum_axes.c2p(15.5, 0.6))
        treble_label = Text("Treble", font_size=24, color=GREEN, weight=BOLD)
        treble_label.next_to(treble_rect, UP, buff=0.15)

        # ── 7. Narration text at bottom ──
        narration = Text(
            "The Fourier Transform splits a signal into its frequency components",
            font_size=24,
            color=TEXT,
        )
        narration.to_edge(DOWN, buff=0.4)

        # ══════════════════════════════════════════
        # ANIMATION SEQUENCE  (total = 11.0s)
        #   Phase 1: 2.0  |  Phase 2: 1.8  |  Phase 3: 2.5
        #   Phase 4: 3.0  |  Phase 5: 1.0  |  Wait: 0.7
        # ══════════════════════════════════════════

        # Phase 1: Show the music wave
        self.play(
            FadeIn(music_axes, shift=RIGHT * 0.3),
            Create(music_graph, run_time=1.5),
            FadeIn(music_label, shift=UP * 0.2),
            run_time=2.0,
        )

        # Phase 2: Arrow + FFT box appear
        self.play(
            GrowArrow(arrow1),
            FadeIn(fft_box_group, scale=0.8),
            run_time=1.8,
        )

        # Phase 3: Arrow out + spectrum appears + bars grow
        self.play(GrowArrow(arrow2), run_time=0.8)
        self.play(
            FadeIn(spectrum_axes),
            FadeIn(x_nums),
            FadeIn(freq_label),
            run_time=0.7,
        )
        self.play(
            LaggedStart(
                *[GrowFromCenter(bar) for bar in bars],
                lag_ratio=0.15,
            ),
            run_time=1.0,
        )

        # Phase 4: Highlight frequency regions
        self.play(
            FadeIn(bass_rect, scale=1.05),
            FadeIn(bass_label, shift=DOWN * 0.15),
            run_time=1.0,
        )
        self.play(
            FadeIn(mid_rect, scale=1.05),
            FadeIn(mid_label, shift=DOWN * 0.15),
            run_time=1.0,
        )
        self.play(
            FadeIn(treble_rect, scale=1.05),
            FadeIn(treble_label, shift=DOWN * 0.15),
            run_time=1.0,
        )

        # Phase 5: Show narration text
        self.play(FadeIn(narration, shift=UP * 0.2), run_time=1.0)

        # Hold final frame to reach 11.0s total
        self.wait(0.7)
