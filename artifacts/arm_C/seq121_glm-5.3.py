import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Signals as waves in the time domain ---
        self.camera.background_color = "#181825"

        blue = "#89b4fa"
        peach = "#fab387"
        rose = "#f38ba8"
        mint = "#a6e3a1"
        teal = "#94e2d5"

        # ---------------- Title ----------------
        title = Text("Signals as waves in the time domain", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        self.play(Write(title), run_time=1.5)  # 0.0 -> 1.5
        self.wait(0.5)  # 2.0s

        # ---------------- Three example signals ----------------
        def make_panel(func, color, name):
            ax = Axes(
                x_range=[0, 1, 0.25],
                y_range=[-1.4, 1.4, 1],
                x_length=3.4,
                y_length=1.5,
                tips=False,
                axis_config={"stroke_width": 2.0},
            )
            wave = ax.plot(func, x_range=[0, 1], color=color, stroke_width=3)
            label = Text(name, font_size=24, color=color)
            return VGroup(ax, wave, label).arrange(DOWN, buff=0.18)

        def note_func(x):
            # Clean sine: a musical note
            return np.sin(TAU * 2 * x)

        def radio_func(x):
            # Amplitude modulation: envelope * carrier
            env = 1.0 - 0.7 * (0.5 + 0.5 * np.sin(TAU * x))
            return env * np.sin(TAU * 8 * x)

        def heart_func(x):
            # ECG-like spike-dip from gaussian bumps
            v = 1.1 * np.exp(-((x - 0.30) ** 2) / 0.0009)
            v -= 0.32 * np.exp(-((x - 0.40) ** 2) / 0.0016)
            v += 0.22 * np.exp(-((x - 0.47) ** 2) / 0.0040)
            return v

        panel_specs = [
            (note_func, peach, "Musical note"),
            (radio_func, teal, "Radio broadcast"),
            (heart_func, rose, "Heartbeat"),
        ]
        panels = VGroup(*[make_panel(f, c, n) for (f, c, n) in panel_specs]).arrange(
            RIGHT, buff=0.7
        )
        panels.shift(UP * 0.3)

        panel_anims = []
        for panel in panels:
            ax, wave, label = panel
            panel_anims.append(
                AnimationGroup(
                    Create(ax),
                    Create(wave),
                    FadeIn(label),
                    lag_ratio=0.3,
                )
            )

        self.play(LaggedStart(*panel_anims, lag_ratio=0.4), run_time=3.5)  # 5.5s
        self.wait(1.5)  # 7.0s

        self.play(FadeOut(panels), run_time=1.0)  # 8.0s

        # ---------------- Main time-domain graph ----------------
        main_axes = Axes(
            x_range=[0, 10, 2],
            y_range=[-1.8, 1.8, 1],
            x_length=10.0,
            y_length=3.6,
            tips=True,
            axis_config={"stroke_width": 2.0},
        ).shift(UP * 0.7)

        # Superposition: subtly structured, foreshadowing hidden structure
        main_wave = main_axes.plot(
            lambda x: 1.1 * np.sin(x) + 0.45 * np.sin(2.7 * x),
            x_range=[0, 10],
            color=blue,
            stroke_width=3.5,
        )

        self.play(GrowFromCenter(main_axes), run_time=1.5)  # 9.5s
        self.play(Create(main_wave), run_time=2.0)  # 11.5s

        # Axis labels
        value_label = Text("value", font_size=28, color=WHITE)
        value_label.rotate(PI / 2)
        value_label.next_to(main_axes.y_axis, LEFT, buff=0.25)

        time_label = Text("time", font_size=28, color=WHITE)
        time_label.next_to(main_axes.x_axis.get_end(), DOWN, buff=0.2)

        self.play(FadeIn(value_label), FadeIn(time_label), run_time=1.0)  # 12.5s

        # ---------------- Caption: the time domain ----------------
        main_1 = Text("The Time Domain", font_size=48, color=blue)
        main_1.move_to(DOWN * 1.9)

        self.play(Write(main_1), run_time=1.5)  # 14.0s
        self.wait(0.5)  # 14.5s

        # ---------------- The caveat ----------------
        cap1 = Text("shows when things happen", font_size=26, color=mint)
        cap1.move_to(DOWN * 2.9 + LEFT * 3.5)

        cap2 = Text("hides the underlying structure", font_size=26, color=rose)
        cap2.move_to(DOWN * 2.9 + RIGHT * 3.5)

        self.play(
            Circumscribe(main_wave, color=mint, buff=0.15),
            FadeIn(cap1, shift=UP * 0.2),
            run_time=1.25,
        )  # 15.75s

        self.play(
            Indicate(main_wave, color=rose, scale_factor=1.1),
            FadeIn(cap2, shift=UP * 0.2),
            run_time=1.25,
        )  # 17.0s

        self.wait(2.0)  # 19.0s
        # --- Scene 2: Step 2: Sine waves as atomic building blocks: amplitude, frequency, phase ---
        self.clear()
        self.camera.background_color = "#181825"

        ORANGE = "#fab387"
        BLUE = "#89b4fa"
        GREEN = "#a6e3a1"
        PINK = "#f38ba8"
        TEAL = "#94e2d5"
        TEXT_C = "#CDD6F4"
        SUB_C = "#A6ADC8"

        # ---------- Title ----------
        title = Text("Sine waves as atomic building blocks", font_size=36, color=WHITE)
        subtitle = Text(
            "amplitude  \u00b7  frequency  \u00b7  phase", font_size=26, color=ORANGE
        )
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.2).move_to(UP * 3)

        self.play(FadeIn(title_group, shift=DOWN * 0.3), run_time=1.2)

        # ---------- Axes ----------
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=7,
            y_length=3.2,
            axis_config={
                "color": ORANGE,
                "stroke_width": 2.0,
                "include_tip": False,
            },
        )
        x_label = Text("time (s)", font_size=22, color=SUB_C)
        x_label.next_to(axes.get_x_axis(), RIGHT, buff=0.2).shift(UP * 0.15)

        self.play(Create(axes), FadeIn(x_label), run_time=1.0)

        # ---------- Base sine wave ----------
        base_wave = axes.plot(
            lambda x: np.sin(x), x_range=[-3, 3], color=BLUE, stroke_width=4
        )
        wave = base_wave.copy()
        self.play(Create(wave), run_time=1.5)

        # ---------- Amplitude ----------
        peak_x = np.pi / 2
        p_zero = axes.c2p(peak_x, 0.0)
        p_peak = axes.c2p(peak_x, 1.0)

        amp_line = DashedLine(p_zero, p_peak, color=BLUE, stroke_width=2.0)
        amp_dot = Dot(p_peak, radius=0.06, color=BLUE)
        amp_brace = BraceBetweenPoints(p_zero, p_peak, RIGHT * 0.1)
        amp_brace.set_color(BLUE)
        # FIX: create the label manually instead of brace.get_text(font_size=...),
        # which leaked the kwarg into next_to()
        amp_label = MathTex("A", font_size=30, color=BLUE)
        amp_label.next_to(amp_brace, RIGHT, buff=0.15)
        amp_caption = Text("amplitude: its height", font_size=26, color=TEXT_C)
        amp_caption.next_to(amp_label, RIGHT, buff=0.3)

        self.play(
            FadeIn(amp_line),
            GrowFromCenter(amp_brace),
            FadeIn(amp_dot),
            Write(amp_label),
            Write(amp_caption),
            run_time=1.3,
        )

        tall_wave = axes.plot(
            lambda x: 1.5 * np.sin(x), x_range=[-3, 3], color=BLUE, stroke_width=4
        )
        self.play(Transform(wave, tall_wave), run_time=1.2)
        self.play(Transform(wave, base_wave.copy()), run_time=0.8)

        # ---------- Frequency ----------
        freq_wave = axes.plot(
            lambda x: np.sin(2 * x), x_range=[-3, 3], color=BLUE, stroke_width=4
        )
        self.play(
            Transform(wave, freq_wave),
            FadeOut(VGroup(amp_line, amp_brace, amp_label, amp_caption, amp_dot)),
            run_time=1.2,
        )

        cycle_arrow = DoubleArrow(
            axes.c2p(-np.pi / 4, -1.35),
            axes.c2p(3 * np.pi / 4, -1.35),
            color=GREEN,
            stroke_width=2.5,
            buff=0.0,
        )
        cycle_label = Text("one cycle", font_size=22, color=GREEN)
        cycle_label.next_to(cycle_arrow, DOWN, buff=0.15)
        freq_caption = Text("frequency: cycles per second", font_size=26, color=TEXT_C)
        freq_caption.next_to(cycle_label, DOWN, buff=0.2)

        self.play(
            FadeIn(cycle_arrow),
            FadeIn(cycle_label),
            Write(freq_caption),
            run_time=1.0,
        )
        self.wait(0.6)

        # ---------- Phase ----------
        phase_wave = axes.plot(
            lambda x: np.sin(2 * x - PI / 2),
            x_range=[-3, 3],
            color=BLUE,
            stroke_width=4,
        )
        self.play(Transform(wave, phase_wave), run_time=1.2)

        shift_arrow = CurvedArrow(
            axes.c2p(np.pi / 4, 1.2),
            axes.c2p(np.pi / 2, 1.2),
            color=PINK,
            angle=-PI / 2,
            stroke_width=2.5,
        )
        phase_caption = Text("phase: its horizontal shift", font_size=26, color=TEXT_C)
        phase_caption.next_to(shift_arrow, UP, buff=0.2)

        self.play(FadeIn(shift_arrow), Write(phase_caption), run_time=0.8)

        # ---------- Cleanup of feature annotations ----------
        features = VGroup(
            cycle_arrow, cycle_label, freq_caption, shift_arrow, phase_caption
        )
        self.play(FadeOut(features), run_time=0.7)

        # ---------- "Primary colors" mixing metaphor ----------
        def mini_wave(freq_mult, amp, color):
            return FunctionGraph(
                lambda x: amp * np.sin(freq_mult * x),
                x_range=[-0.75, 0.75],
                color=color,
                stroke_width=3,
            )

        wave_1 = mini_wave(2.0, 0.32, GREEN)
        wave_2 = mini_wave(4.0, 0.22, PINK)
        wave_3 = mini_wave(6.0, 0.14, TEAL)
        plus_1 = MathTex("+", font_size=36, color=SUB_C)
        plus_2 = MathTex("+", font_size=36, color=SUB_C)
        building_row = VGroup(wave_1, plus_1, wave_2, plus_2, wave_3)
        building_row.arrange(RIGHT, buff=0.25)
        building_row.move_to(DOWN * 2.3)

        self.play(FadeIn(building_row, shift=UP * 0.3), run_time=1.3)

        mixed_wave = axes.plot(
            lambda x: np.sin(x) + 0.5 * np.sin(2 * x) + 0.3 * np.sin(3 * x),
            x_range=[-3, 3],
            color=TEXT_C,
            stroke_width=4,
        )
        self.play(Transform(wave, mixed_wave), run_time=1.5)

        mix_caption = Text(
            "any complex signal = a mix of simple waves", font_size=26, color=TEXT_C
        )
        mix_caption.move_to(DOWN * 3.35)
        self.play(FadeIn(mix_caption, shift=UP * 0.2), run_time=0.8)

        self.wait(2.4)
        # --- Scene 3: Step 3: Superposition: summing sine waves into complex waveforms ---
        self.clear()
        self.camera.background_color = "#181825"

        # palette
        C_BLUE = "#89b4fa"
        C_ORANGE = "#fab387"
        C_TEAL = "#94e2d5"
        C_GREEN = "#a6e3a1"
        C_PINK = "#f38ba8"
        C_TEXT = "#cdd6f4"

        # ----------------------------------------------------------------
        # objects
        # ----------------------------------------------------------------
        title_3 = Text(
            "Superposition: summing sine waves into complex waveforms",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        main_3 = NumberLine(
            x_range=[-5, 5],
            length=11,
            color=C_PINK,
            stroke_width=2.0,
            font_size=24,
        ).to_edge(DOWN, buff=0.7)
        main_3.add_numbers()
        for num in main_3.numbers:
            num.set_color(C_PINK)

        X_MIN, X_MAX = -5.0, 5.0
        SCALE = 0.5

        def x_to_scene(xv):
            return main_3.n2p(xv)[0]

        def h1(xv):
            return 1.0 * np.sin(1.0 * xv)

        def h2(xv):
            return 0.6 * np.sin(2.0 * xv)

        def h3(xv):
            return 0.4 * np.sin(4.0 * xv)

        def hsum(xv):
            return h1(xv) + h2(xv) + h3(xv)

        def make_wave(func, center_y, color, stroke=2.0):
            pts = []
            for i in range(241):
                xv = X_MIN + (X_MAX - X_MIN) * i / 240.0
                pts.append(np.array([x_to_scene(xv), center_y + SCALE * func(xv), 0.0]))
            curve = VMobject(stroke_color=color, stroke_width=stroke)
            curve.set_points_as_corners(pts)
            return curve

        wave1 = make_wave(h1, 1.4, C_BLUE)
        wave2 = make_wave(h2, 0.4, C_ORANGE)
        wave3 = make_wave(h3, -0.6, C_TEAL)
        sum_wave = make_wave(hsum, 0.4, C_GREEN, stroke=3.0)

        lbl1 = MathTex("y_1", font_size=34, color=C_BLUE).move_to([6.3, 1.4, 0])
        lbl2 = MathTex("y_2", font_size=34, color=C_ORANGE).move_to([6.3, 0.4, 0])
        lbl3 = MathTex("y_3", font_size=34, color=C_TEAL).move_to([6.3, -0.6, 0])
        sum_label = MathTex("y = y_1 + y_2 + y_3", font_size=36, color=C_GREEN).move_to(
            [0, 2.35, 0]
        )

        # "single instant" demo: heights add at one moment in time
        x0 = 2.0
        px = x_to_scene(x0)
        dash = DashedLine(
            start=np.array([px, -1.1, 0.0]),
            end=np.array([px, 2.15, 0.0]),
            dash_length=0.15,
            stroke_width=2.0,
            color=WHITE,
        ).set_stroke(opacity=0.45)
        dot1 = Dot(np.array([px, 1.4 + SCALE * h1(x0), 0.0]), radius=0.07, color=C_BLUE)
        dot2 = Dot(
            np.array([px, 0.4 + SCALE * h2(x0), 0.0]), radius=0.07, color=C_ORANGE
        )
        dot3 = Dot(
            np.array([px, -0.6 + SCALE * h3(x0), 0.0]), radius=0.07, color=C_TEAL
        )
        dot_sum = Dot(
            np.array([px, 0.4 + SCALE * hsum(x0), 0.0]), radius=0.09, color=C_GREEN
        )
        instant_caption = Text(
            "at every instant, heights add", font_size=26, color=C_TEXT
        ).move_to([0, -1.9, 0])
        final_caption = Text(
            "complex waveform = pure tones stacked", font_size=26, color=C_TEXT
        ).move_to([0, -1.9, 0])

        # translucent "merged" targets (overlapping colors = superposition)
        ghost1 = sum_wave.copy().set_stroke(color=C_BLUE, width=3.0, opacity=0.55)
        ghost2 = sum_wave.copy().set_stroke(color=C_ORANGE, width=3.0, opacity=0.55)
        ghost3 = sum_wave.copy().set_stroke(color=C_TEAL, width=3.0, opacity=0.55)

        # ----------------------------------------------------------------
        # animation  (plays total 17.0s + wait 1.0s = 18.0s)
        # ----------------------------------------------------------------
        self.play(Write(title_3), run_time=1.5)
        self.play(Create(main_3), run_time=1.5)

        self.play(GrowFromCenter(wave1), FadeIn(lbl1), run_time=2.0)
        self.play(GrowFromCenter(wave2), FadeIn(lbl2), run_time=2.0)
        self.play(GrowFromCenter(wave3), FadeIn(lbl3), run_time=2.0)

        self.play(
            Create(dash),
            FadeIn(dot1),
            FadeIn(dot2),
            FadeIn(dot3),
            FadeIn(dot_sum),
            FadeIn(instant_caption),
            run_time=2.0,
        )

        self.play(
            Transform(wave1, ghost1),
            Transform(wave2, ghost2),
            Transform(wave3, ghost3),
            FadeOut(lbl1),
            FadeOut(lbl2),
            FadeOut(lbl3),
            FadeOut(dot1),
            FadeOut(dot2),
            FadeOut(dot3),
            FadeOut(dash),
            FadeOut(instant_caption),
            run_time=3.0,
        )

        self.play(
            Transform(wave1, sum_wave),
            FadeOut(wave2),
            FadeOut(wave3),
            FadeIn(sum_label),
            run_time=1.5,
        )

        self.play(
            ShowPassingFlash(
                wave1.copy().set_stroke(color=C_GREEN, width=7, opacity=0.9),
                time_width=0.35,
            ),
            FadeIn(final_caption),
            run_time=1.5,
        )

        self.wait(1.0)
        # --- Scene 4: Step 4: The Fourier question: decomposing a signal into its frequencies ---
        self.camera.background_color = "#181825"

        # Palette (per style guidelines)
        blue = "#89b4fa"
        peach = "#fab387"
        pink = "#f38ba8"
        green = "#a6e3a1"
        teal = "#94e2d5"

        # ---------- Title ----------
        title_4 = Text(
            "The Fourier question: decomposing a signal into its frequencies",
            font_size=36,
            color=WHITE,
        )
        if title_4.width > 12.5:
            title_4.scale(12.5 / title_4.width)
        title_4.move_to(UP * 3)
        self.play(Write(title_4), run_time=1.4)

        # ---------- The messy composite signal ----------
        sig_axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-2, 2, 1],
            x_length=5.4,
            y_length=2.4,
            tips=False,
            axis_config={
                "stroke_color": teal,
                "stroke_width": 2.0,
                "include_ticks": False,
            },
        )
        sig_axes.move_to(LEFT * 3.6 + UP * 0.5)

        messy = sig_axes.plot(
            lambda t: (
                1.0 * np.sin(1.0 * t) + 0.6 * np.sin(2.3 * t) + 0.35 * np.sin(4.0 * t)
            ),
            x_range=[0, 4 * PI],
            color=green,
            stroke_width=2.0,
        )

        main_4 = VGroup(sig_axes, messy)

        self.play(Create(sig_axes), run_time=0.8)
        self.play(Create(messy), run_time=1.6)

        q_text = Text(
            "Which pure frequencies are inside — and how strong is each?",
            font_size=22,
            color=teal,
        )
        q_text.next_to(title_4, DOWN, buff=0.2)
        self.play(FadeIn(q_text, shift=DOWN * 0.3), run_time=1.0)
        self.wait(0.3)

        # ---------- Decomposition: the three pure ingredients ----------
        freqs = [1.0, 2.3, 4.0]
        amps = [1.0, 0.6, 0.35]
        amp_strs = ["1.0", "0.6", "0.35"]
        comp_colors = [blue, pink, peach]
        y_positions = [-1.5, -2.35, -3.2]

        components = VGroup()
        for i in range(3):
            curve = ParametricFunction(
                lambda t, a=amps[i], f=freqs[i]: np.array([t, a * np.sin(f * t), 0.0]),
                t_range=[0, 4 * PI, 0.05],
                color=comp_colors[i],
                stroke_width=2.0,
            )
            curve.stretch_to_fit_width(5.4)
            curve.move_to(LEFT * 3.6 + UP * y_positions[i])
            components.add(curve)

        comp_labels = VGroup()
        for i, curve in enumerate(components):
            label = MathTex("f_" + str(i + 1), font_size=28, color=comp_colors[i])
            label.next_to(curve, LEFT, buff=0.25)
            comp_labels.add(label)

        split_arrows = VGroup()
        for i, curve in enumerate(components):
            start_pt = sig_axes.c2p(4 * PI, 0)
            end_pt = curve.get_end()
            arrow = Arrow(
                start_pt,
                end_pt,
                buff=0.2,
                stroke_width=2.0,
                color=comp_colors[i],
                max_tip_length_to_length_ratio=0.35,
            )
            split_arrows.add(arrow)

        self.play(
            LaggedStart(
                *[Create(a) for a in split_arrows],
                lag_ratio=0.4,
            ),
            run_time=0.9,
        )
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        GrowFromCenter(components[i]),
                        FadeIn(comp_labels[i], shift=RIGHT * 0.2),
                    )
                    for i in range(3)
                ],
                lag_ratio=0.5,
            ),
            run_time=2.4,
        )
        self.wait(0.4)

        # ---------- The spectrum: how strong each frequency is ----------
        spec_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1.1, 0.5],
            x_length=5.0,
            y_length=3.2,
            tips=False,
            axis_config={
                "stroke_color": teal,
                "stroke_width": 2.0,
            },
        )
        spec_axes.move_to(RIGHT * 3.6 + UP * 0.4)

        spec_caption = Text(
            "strength of each frequency",
            font_size=24,
            color=teal,
        )
        spec_caption.next_to(spec_axes, DOWN, buff=0.35)

        bridge_arrow = Arrow(
            LEFT * 0.7 + UP * 0.4,
            RIGHT * 0.9 + UP * 0.4,
            buff=0.1,
            stroke_width=2.0,
            color=teal,
        )
        bridge_label = Text(
            "the Fourier transform",
            font_size=22,
            color=teal,
        )
        bridge_label.next_to(bridge_arrow, UP, buff=0.15)

        bars = VGroup()
        bar_labels = VGroup()
        amp_labels = VGroup()
        for i in range(3):
            f = freqs[i]
            a = amps[i]
            bottom = spec_axes.c2p(f, 0)
            top = spec_axes.c2p(f, a)
            bar_height = top[1] - bottom[1]
            bar = Rectangle(
                width=0.45,
                height=bar_height,
                fill_color=comp_colors[i],
                fill_opacity=0.85,
                stroke_color=comp_colors[i],
                stroke_width=2.0,
            )
            bar.move_to(np.array([bottom[0], bottom[1] + bar_height / 2, 0]))
            bars.add(bar)

            flabel = MathTex("f_" + str(i + 1), font_size=26, color=comp_colors[i])
            flabel.next_to(bar, DOWN, buff=0.15)
            bar_labels.add(flabel)

            alabel = MathTex(amp_strs[i], font_size=24, color=comp_colors[i])
            alabel.next_to(bar, UP, buff=0.12)
            amp_labels.add(alabel)

        self.play(
            FadeIn(bridge_arrow, scale=0.6),
            FadeIn(bridge_label, shift=UP * 0.2),
            Create(spec_axes),
            FadeIn(spec_caption, shift=UP * 0.2),
            run_time=1.2,
        )
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        GrowFromCenter(bars[i]),
                        FadeIn(bar_labels[i], shift=UP * 0.2),
                        FadeIn(amp_labels[i], shift=DOWN * 0.2),
                    )
                    for i in range(3)
                ],
                lag_ratio=0.5,
            ),
            run_time=2.2,
        )

        # ---------- Final emphasis: whole -> ingredients ----------
        self.play(
            Circumscribe(main_4, color=WHITE, buff=0.15, run_time=1.0),
            Circumscribe(bars, color=WHITE, buff=0.15, run_time=1.0),
        )
        self.wait(1.3)
        # --- Scene 5: Step 5: Correlation: multiplying by a test sinusoid and averaging ---
        self.clear()
        self.camera.background_color = "#181825"

        # Palette (Catppuccin Mocha)
        BLUE_C = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"
        GRAY_C = "#6c7086"

        # ---------------- Title ----------------
        title = Text(
            "Correlation: multiplying by a test sinusoid and averaging",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # ---------------- Legend ----------------
        def legend_item(label, color):
            dot = Dot(radius=0.06, color=color)
            return VGroup(dot, label).arrange(RIGHT, buff=0.12)

        legend = (
            VGroup(
                legend_item(Text("signal s(t)", font_size=24, color=WHITE), BLUE_C),
                legend_item(
                    MathTex(r"\sin(2\pi f t)", font_size=30, color=WHITE), PEACH
                ),
                legend_item(Text("product", font_size=24, color=WHITE), GREEN),
                legend_item(Text("average", font_size=24, color=WHITE), PINK),
            )
            .arrange(RIGHT, buff=0.7)
            .move_to(UP * 2.35)
        )

        # ---------------- Axes: match vs mismatch ----------------
        axes_cfg = dict(
            x_range=[0, TAU, TAU / 2],
            y_range=[-1.3, 1.3, 1],
            x_length=5.4,
            y_length=2.2,
            tips=False,
            axis_config={"include_ticks": False},
        )
        axes_l = Axes(**axes_cfg).move_to(LEFT * 3.6 + UP * 0.75)
        axes_r = Axes(**axes_cfg).move_to(RIGHT * 3.6 + UP * 0.75)
        for ax in (axes_l, axes_r):
            ax.set_stroke(color=GRAY_C, width=2)
        axes_pair = VGroup(axes_l, axes_r)

        sig_l = axes_l.plot(lambda x: np.sin(3 * x), x_range=[0, TAU]).set_stroke(
            color=BLUE_C, width=4
        )
        sig_r = axes_r.plot(lambda x: np.sin(3 * x), x_range=[0, TAU]).set_stroke(
            color=BLUE_C, width=4
        )

        test_l = DashedVMobject(
            axes_l.plot(lambda x: np.sin(3 * x), x_range=[0, TAU]), num_dashes=32
        ).set_stroke(color=PEACH, width=3)
        test_r = DashedVMobject(
            axes_r.plot(lambda x: np.sin(4 * x), x_range=[0, TAU]), num_dashes=32
        ).set_stroke(color=PEACH, width=3)

        prod_l = axes_l.plot(lambda x: np.sin(3 * x) ** 2, x_range=[0, TAU]).set_stroke(
            color=GREEN, width=4
        )
        prod_r = axes_r.plot(
            lambda x: np.sin(3 * x) * np.sin(4 * x), x_range=[0, TAU]
        ).set_stroke(color=GREEN, width=4)

        avg_l = DashedLine(
            axes_l.c2p(0, 0.5), axes_l.c2p(TAU, 0.5), dash_length=0.12, color=PINK
        )
        avg_r = DashedLine(
            axes_r.c2p(0, 0), axes_r.c2p(TAU, 0), dash_length=0.12, color=PINK
        )

        avg_lab_l = Text("avg = 0.5", font_size=24, color=PINK).next_to(
            avg_l, UP, buff=0.1
        )
        avg_lab_r = Text("avg \u2248 0", font_size=24, color=PINK).next_to(
            avg_r, UP, buff=0.1
        )

        cap_l = Text("f = 3 Hz: aligned", font_size=26, color=GREEN).next_to(
            axes_l, DOWN, buff=0.18
        )
        cap_r = Text("f = 4 Hz: misaligned", font_size=26, color=PINK).next_to(
            axes_r, DOWN, buff=0.18
        )

        # ---------------- Table (pre-built mobjects passed through unchanged) ----------------
        def passthrough(mob):
            return mob

        header = [
            Text("f (Hz)", font_size=24, color=WHITE),
            MathTex(
                r"\langle\, s \cdot \sin(2\pi f t)\, \rangle", font_size=32, color=WHITE
            ),
            Text("verdict", font_size=24, color=WHITE),
        ]
        data_rows = [
            [
                MathTex("1", font_size=32),
                MathTex("0.03", font_size=32),
                Text("cancels out", font_size=24, color=TEAL),
            ],
            [
                MathTex("3", font_size=32, color=GREEN),
                MathTex("0.50", font_size=32, color=GREEN),
                Text("MATCH!", font_size=24, color=GREEN),
            ],
            [
                MathTex("4", font_size=32),
                MathTex("-0.01", font_size=32),
                Text("cancels out", font_size=24, color=TEAL),
            ],
        ]
        table = Table(
            [header] + data_rows,
            element_to_mobject=passthrough,
            include_outer_lines=True,
            h_buff=0.55,
            v_buff=0.13,
            line_config={"stroke_width": 2, "color": TEAL},
        ).move_to(DOWN * 2.3)

        # entries are laid out row-major: 0-2 header, 3-5 row "1", 6-8 row "3", 9-11 row "4"
        entries = table.get_entries()
        match_row = VGroup(entries[6], entries[7], entries[8])

        # ---------------- Animation timeline (total = 20.5s) ----------------
        self.play(Write(title), run_time=1.5)  # 1.5
        self.play(
            FadeIn(axes_pair, shift=UP * 0.2), FadeIn(legend), run_time=1.0
        )  # 2.5
        self.play(Create(sig_l), Create(sig_r), run_time=1.3)  # 3.8
        self.wait(0.4)  # 4.2
        self.play(Create(test_l), Create(test_r), run_time=1.3)  # 5.5
        self.wait(0.5)  # 6.0
        self.play(
            Create(prod_l), Create(prod_r), FadeIn(cap_l), FadeIn(cap_r), run_time=1.6
        )  # 7.6
        self.play(
            Create(avg_l),
            Create(avg_r),
            FadeIn(avg_lab_l),
            FadeIn(avg_lab_r),
            run_time=1.2,
        )  # 8.8
        self.wait(0.6)  # 9.4
        self.play(
            Indicate(avg_lab_l, color=GREEN, scale_factor=1.3), run_time=0.9
        )  # 10.3
        self.play(
            Indicate(avg_lab_r, color=PINK, scale_factor=1.3), run_time=0.9
        )  # 11.2
        self.play(FadeIn(table, shift=UP * 0.2), run_time=1.8)  # 13.0
        self.wait(0.5)  # 13.5
        self.play(Circumscribe(match_row, color=PINK, buff=0.08), run_time=1.3)  # 14.8
        self.wait(0.7)  # 15.5
        self.play(
            ShowPassingFlash(avg_l.copy().set_stroke(width=7), time_width=0.4),
            run_time=1.5,
        )  # 17.0
        self.wait(3.5)  # 20.5
        # --- Scene 6: Step 6: Complex exponentials: winding the signal around a circle ---
        self.camera.background_color = "#181825"

        # Title
        title = Text(
            "Complex exponentials: winding the signal around a circle",
            font_size=36,
            color=WHITE,
        )
        title.to_edge(UP, buff=0.4)

        # Euler's formula
        euler = MathTex(
            r"e^{i\omega t} = \cos(\omega t) + i\,\sin(\omega t)",
            font_size=48,
            color="#94e2d5",
        )
        euler.next_to(title, DOWN, buff=0.8)

        self.play(Write(title), run_time=2)
        self.play(Write(euler), run_time=2)
        self.wait(0.5)
        self.play(FadeOut(euler), run_time=0.5)

        # Sine wave (left side): the signal to be wound
        axes = Axes(
            x_range=[0, TAU, TAU / 4],
            y_range=[-1.5, 1.5, 1],
            x_length=4.5,
            y_length=2.2,
            axis_config={
                "stroke_color": "#cdd6f4",
                "stroke_width": 2.0,
                "include_ticks": False,
            },
        )
        axes.move_to(LEFT * 4.2 + DOWN * 1.4)
        sine = axes.plot(lambda x: np.sin(x), color="#fab387", stroke_width=3)
        sig_label = Text("signal", font_size=26, color="#fab387")
        sig_label.next_to(axes, UP, buff=0.15)

        self.play(Create(axes), run_time=1)
        self.play(Create(sine), Write(sig_label), run_time=1.5)

        # Circle with rotating arrow (right side)
        circle = Circle(radius=1.6, color="#cdd6f4", stroke_width=2.0)
        circle.move_to(RIGHT * 3.2 + DOWN * 1.4)
        center = circle.get_center()
        center_dot = Dot(center, radius=0.06, color="#cdd6f4")

        main_6 = Arrow(
            center, center + RIGHT * 1.6, buff=0, color="#cdd6f4", stroke_width=4
        )
        tip_dot = Dot(main_6.get_end(), radius=0.09, color="#89b4fa")
        spinner = VGroup(main_6, tip_dot)

        wind_label = Text("wind around a circle", font_size=26, color="#89b4fa")
        wind_label.next_to(circle, UP, buff=0.2)

        self.play(GrowFromCenter(circle), FadeIn(center_dot), run_time=1)
        self.play(GrowFromCenter(main_6), FadeIn(tip_dot), run_time=1)
        self.play(Write(wind_label), run_time=1)

        # Trace the spinning tip
        trail = TracedPath(tip_dot.get_center, stroke_color="#89b4fa", stroke_width=3)
        self.add(trail)
        self.play(Rotate(spinner, angle=TAU, about_point=center), run_time=2.5)

        # Wound signal: unbalanced at true frequency
        theta = np.linspace(0, TAU * 2, 40, endpoint=False)
        r = 1.6 * (1 + 0.28 * np.sin(theta))
        wound = VGroup(
            *[
                Dot(
                    center + r[k] * np.array([np.cos(theta[k]), np.sin(theta[k]), 0]),
                    radius=0.05,
                    color="#fab387",
                )
                for k in range(40)
            ]
        )

        self.play(FadeOut(trail), FadeOut(spinner), FadeOut(wind_label), run_time=0.5)
        self.play(FadeIn(wound, scale=0.5), run_time=2)

        # Center of mass: nonzero at true frequency
        com = Dot(center + DOWN * 0.55, radius=0.12, color="#a6e3a1")
        com_label = Text("center of mass \u2260 0", font_size=26, color="#a6e3a1")
        com_label.next_to(circle, DOWN, buff=0.3)
        com_arrow = Arrow(
            center, com.get_center(), buff=0.1, color="#a6e3a1", stroke_width=3
        )

        self.play(GrowFromCenter(com), run_time=1)
        self.play(GrowFromCenter(com_arrow), Write(com_label), run_time=1.5)

        # Highlight: only at the true frequency
        highlight = Text("Only at the true frequency!", font_size=30, color=YELLOW)
        highlight.next_to(com_label, DOWN, buff=0.5)
        self.play(Write(highlight), run_time=1.5)

        self.play(Circumscribe(wound, color=YELLOW), run_time=1)
        self.wait(2)
        # --- Scene 7: Step 7: The spectrum: plotting strength versus frequency ---
        self.clear()
        self.camera.background_color = "#181825"

        # ---------- Palette ----------
        BLUE = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"

        # ---------- Title & main text ----------
        title_7 = Text(
            "The spectrum: plotting strength versus frequency",
            font_size=36,
            color=WHITE,
        )
        title_7.move_to(UP * 3)

        main_7 = Text("The Spectrum", font_size=48, color=BLUE)
        main_7.move_to(ORIGIN)

        self.play(FadeIn(title_7), Write(main_7), run_time=1.0)
        self.wait(0.5)

        # ---------- Axes (frequency horizontal, strength vertical) ----------
        axis_origin = np.array([-4.4, -2.2, 0.0])
        x_axis = Arrow(
            axis_origin,
            axis_origin + RIGHT * 9.0,
            buff=0,
            stroke_width=2.0,
            tip_length=0.25,
            color=WHITE,
        )
        y_axis = Arrow(
            axis_origin,
            axis_origin + UP * 3.6,
            buff=0,
            stroke_width=2.0,
            tip_length=0.25,
            color=WHITE,
        )

        x_label = Text("frequency", font_size=26, color=TEAL)
        x_label.next_to(x_axis.get_end(), DOWN, buff=0.2)
        y_label = Text("strength", font_size=26, color=TEAL)
        y_label.rotate(PI / 2)
        y_label.next_to(y_axis.get_end(), RIGHT, buff=0.2)

        self.play(main_7.animate.scale(0.75).move_to(UP * 1.7), run_time=0.8)
        self.play(
            Create(x_axis),
            Create(y_axis),
            FadeIn(x_label),
            FadeIn(y_label),
            run_time=1.2,
        )

        # ---------- Bars: strengths at each tested frequency ----------
        y_base = -2.2
        heights = [0.2, 0.28, 0.35, 0.5, 1.7, 0.6, 0.3, 0.4, 1.45, 1.85, 0.5, 0.25]
        peak_indices = [4, 8, 9]
        bars = VGroup()
        for i, h in enumerate(heights):
            x_center = -3.85 + i * 0.7
            if i in peak_indices:
                bar_color = PEACH
            else:
                bar_color = BLUE
            bar = Rectangle(
                width=0.5,
                height=max(h, 0.05),
                fill_opacity=0.85,
                stroke_width=2.0,
                color=bar_color,
            )
            bar.move_to(np.array([x_center, y_base + h / 2, 0.0]))
            bars.add(bar)

        # A probe that sweeps the frequency axis while each test is "recorded"
        scan = DashedLine(
            np.array([-4.0, y_base, 0.0]),
            np.array([-4.0, y_base + 2.5, 0.0]),
            color=TEAL,
            stroke_width=2.0,
        )
        self.play(FadeIn(scan), run_time=0.4)
        self.play(
            scan.animate.shift(RIGHT * 8.2),
            LaggedStart(
                *[GrowFromPoint(bar, bar.get_bottom()) for bar in bars],
                lag_ratio=0.1,
            ),
            run_time=3.5,
        )

        # ---------- Caption: this bar graph IS the spectrum ----------
        caption = Text(
            "This bar graph is the spectrum — the frequency domain.",
            font_size=28,
            color=TEAL,
        )
        caption.move_to(DOWN * 3.1)
        self.play(FadeOut(scan), FadeIn(caption), run_time=0.8)
        self.wait(0.4)

        # ---------- Sharp peaks mark dominant frequencies ----------
        peaks = VGroup(*[bars[i] for i in peak_indices])
        self.play(Indicate(peaks, color=PINK, scale_factor=1.12), run_time=1.5)

        peak_label = Text(
            "sharp peaks → dominant frequencies", font_size=28, color=PEACH
        )
        peak_label.move_to(np.array([1.9, 0.95, 0.0]))
        arrow_a = Arrow(
            peak_label.get_bottom() + LEFT * 0.6,
            bars[9].get_top() + UP * 0.1,
            buff=0.05,
            stroke_width=2.0,
            color=PEACH,
            tip_length=0.2,
        )
        arrow_b = Arrow(
            peak_label.get_bottom() + RIGHT * 0.8,
            bars[4].get_top() + UP * 0.1,
            buff=0.05,
            stroke_width=2.0,
            color=PEACH,
            tip_length=0.2,
        )
        self.play(
            FadeIn(peak_label),
            GrowFromCenter(arrow_a),
            GrowFromCenter(arrow_b),
            run_time=1.0,
        )

        self.play(
            LaggedStart(
                *[Circumscribe(bar, color=PINK, buff=0.08) for bar in peaks],
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )
        self.wait(4.2)
        # --- Scene 8: Step 8: Duality: inverse transform and real-world applications ---
        self.clear()
        self.camera.background_color = "#181825"

        C_TEXT = "#CDD6F4"
        C_TIME = "#fab387"
        C_FREQ = "#94e2d5"
        C_WAVE = "#89b4fa"
        C_PINK = "#f38ba8"
        C_GREEN = "#a6e3a1"
        C_PURPLE = "#CBA6F7"

        # ---------------- Title ----------------
        title = Text(
            "Duality: inverse transform and real-world applications",
            font_size=36,
            color=WHITE,
        )
        title.move_to(UP * 3)

        # ---------------- Time domain (left) ----------------
        main_8 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=4.4,
            y_length=2.6,
            axis_config={
                "color": C_TIME,
                "stroke_width": 2.0,
                "include_tip": False,
            },
        )
        main_8.shift(LEFT * 3.3 + UP * 0.6)
        time_label = Text("Time domain", font_size=24, color=C_TIME)
        time_label.next_to(main_8, DOWN, buff=0.15)
        t_label = main_8.get_x_axis_label(MathTex("t", font_size=30))

        wave = main_8.plot(
            lambda x: (
                0.8 * np.sin(2 * x)
                + 0.5 * np.sin(4.7 * x + 0.6)
                + 0.35 * np.sin(8.9 * x + 1.3)
            ),
            color=C_WAVE,
            stroke_width=3.5,
        )

        comp_specs = [
            (lambda x: 0.8 * np.sin(2 * x), C_GREEN),
            (lambda x: 0.5 * np.sin(4.7 * x + 0.6), C_PINK),
            (lambda x: 0.35 * np.sin(8.9 * x + 1.3), C_PURPLE),
        ]
        components = VGroup(
            *[
                main_8.plot(func, color=col, stroke_width=2.0).set_opacity(0.8)
                for func, col in comp_specs
            ]
        )

        # ---------------- Frequency domain (right) ----------------
        freq_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=4.4,
            y_length=2.6,
            axis_config={
                "color": C_FREQ,
                "stroke_width": 2.0,
                "include_tip": False,
            },
        )
        freq_axes.shift(RIGHT * 3.3 + UP * 0.6)
        freq_label = Text("Frequency domain", font_size=24, color=C_FREQ)
        freq_label.next_to(freq_axes, DOWN, buff=0.15)
        f_label = freq_axes.get_x_axis_label(MathTex("f", font_size=30))

        stems = VGroup()
        spec_data = [(-1.7, 1.5, C_GREEN), (-0.2, 1.0, C_PINK), (1.4, 0.7, C_PURPLE)]
        for x_pos, hgt, col in spec_data:
            stems.add(
                VGroup(
                    Line(
                        freq_axes.c2p(x_pos, 0),
                        freq_axes.c2p(x_pos, hgt),
                        color=col,
                        stroke_width=5,
                    ),
                    Dot(freq_axes.c2p(x_pos, hgt), color=col, radius=0.07),
                )
            )

        # ---------------- Duality arrows ----------------
        top_arrow = Arc(
            radius=1.6,
            start_angle=62 * DEGREES,
            angle=56 * DEGREES,
            color=C_WAVE,
            stroke_width=3,
        )
        top_arrow.shift(UP * 0.6)
        top_arrow.reverse_points()
        top_arrow.add_tip(tip_length=0.2)
        top_arrow.set_color(C_WAVE)

        analysis_label = VGroup(
            MathTex(r"\mathcal{F}", font_size=32, color=C_WAVE),
            Text("analysis", font_size=20, color=C_TEXT),
        ).arrange(RIGHT, buff=0.18)
        analysis_label.next_to(top_arrow, UP, buff=0.08)

        bottom_arrow = Arc(
            radius=1.1,
            start_angle=240 * DEGREES,
            angle=60 * DEGREES,
            color=C_GREEN,
            stroke_width=3,
        )
        bottom_arrow.shift(DOWN * 0.9)
        bottom_arrow.reverse_points()
        bottom_arrow.add_tip(tip_length=0.2)
        bottom_arrow.set_color(C_GREEN)

        synth_label = VGroup(
            MathTex(r"\mathcal{F}^{-1}", font_size=32, color=C_GREEN),
            Text("synthesis", font_size=20, color=C_TEXT),
        ).arrange(RIGHT, buff=0.18)
        synth_label.next_to(bottom_arrow, DOWN, buff=0.08)

        same_info = VGroup(
            Text("same", font_size=22, color=C_TEXT),
            Text("information", font_size=22, color=C_TEXT),
        ).arrange(DOWN, buff=0.08)
        same_info.move_to(UP * 0.6)

        # ---------------- Inverse transform formula ----------------
        equation = MathTex(
            r"x(t) \;=\; \sum_{k} X_k \, e^{\, i\, 2 \pi k t / N}",
            font_size=32,
            color=C_TEXT,
        )
        equation.move_to(DOWN * 2.72)

        # ---------------- Application cards ----------------
        app_data = [
            ("Filtering", C_WAVE),
            ("Compression", C_TIME),
            ("Communications", C_PINK),
        ]
        cards = VGroup()
        for name, col in app_data:
            box = RoundedRectangle(
                corner_radius=0.12,
                width=3.3,
                height=0.7,
                stroke_color=col,
                stroke_width=2.0,
                fill_color="#1E1E2E",
                fill_opacity=1.0,
            )
            row = VGroup(
                Dot(radius=0.07, color=col),
                Text(name, font_size=22, color=C_TEXT),
            ).arrange(RIGHT, buff=0.15)
            row.move_to(box.get_center())
            cards.add(VGroup(box, row))
        cards.arrange(RIGHT, buff=0.35)
        cards.move_to(DOWN * 3.5)

        # ---------------- Animations ----------------
        self.play(Write(title), run_time=1.5)

        self.play(
            FadeIn(main_8),
            FadeIn(t_label),
            FadeIn(time_label, shift=UP * 0.2),
            run_time=0.8,
        )

        self.play(Create(wave), run_time=1.5)

        self.play(
            FadeIn(freq_axes),
            FadeIn(f_label),
            FadeIn(freq_label, shift=UP * 0.2),
            run_time=0.8,
        )

        self.play(
            Create(top_arrow),
            FadeIn(analysis_label, shift=UP * 0.1),
            FadeIn(same_info, scale=0.7),
            run_time=1.0,
        )

        self.play(
            LaggedStart(
                *[GrowFromCenter(stem) for stem in stems],
                lag_ratio=0.4,
            ),
            run_time=1.4,
        )

        self.play(
            LaggedStart(
                *[Create(comp) for comp in components],
                lag_ratio=0.3,
            ),
            run_time=1.4,
        )

        self.play(
            FadeOut(components),
            Indicate(wave, scale_factor=1.08),
            run_time=1.0,
        )

        self.play(
            Create(bottom_arrow),
            FadeIn(synth_label, shift=DOWN * 0.1),
            run_time=1.0,
        )

        self.play(ShowPassingFlash(top_arrow, time_width=0.35), run_time=0.7)
        self.play(ShowPassingFlash(bottom_arrow, time_width=0.35), run_time=0.7)

        self.play(Write(equation), run_time=1.2)

        self.play(
            LaggedStart(
                *[FadeIn(card, shift=UP * 0.2) for card in cards],
                lag_ratio=0.35,
            ),
            run_time=1.4,
        )

        self.play(
            LaggedStart(
                *[Indicate(card, scale_factor=1.1) for card in cards],
                lag_ratio=0.4,
            ),
            run_time=1.1,
        )

        self.play(
            Circumscribe(main_8, color=C_TIME),
            Circumscribe(freq_axes, color=C_FREQ),
            run_time=1.0,
        )

        self.wait(2.5)
