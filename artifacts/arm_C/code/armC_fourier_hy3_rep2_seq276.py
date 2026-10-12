import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Signals as functions of time ---
        self.camera.background_color = "#181825"

        # Title
        title = Text("Signals as functions of time", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.6)

        # Main text
        main_text = Text(
            "A signal is a function of time", font_size=48, color="#89b4fa"
        )
        main_text.move_to(ORIGIN + UP * 1.0)

        # Axes (Time vs Amplitude)
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-1.2, 1.2, 0.6],
            x_length=8,
            y_length=2.4,
            axis_config={"color": "#94e2d5", "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 1.1)

        x_label = Text("Time →", font_size=24, color="#94e2d5")
        x_label.next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = Text("Amplitude", font_size=24, color="#94e2d5")
        y_label.next_to(axes.y_axis.get_top(), UP, buff=0.1)

        # Signal waveform: amplitude as a function of time
        signal = axes.plot(
            lambda x: np.sin(x * 1.5) * 0.85, color="#fab387", stroke_width=4
        )

        # Tracking dot + vertical reference line
        dot = Dot(color="#a6e3a1", radius=0.1).move_to(axes.c2p(0, 0))
        vline = always_redraw(
            lambda: DashedLine(
                start=axes.c2p(axes.point_to_coords(dot.get_center())[0], 0),
                end=dot.get_center(),
                color="#a6e3a1",
                stroke_width=1.5,
                dash_length=0.12,
            )
        )

        # Supporting caption
        caption = Text(
            "Amplitude changes as time passes", font_size=28, color="#fab387"
        )
        caption.to_edge(DOWN, buff=0.5)

        # ---- Animations ----
        self.play(Write(title), run_time=1.5)
        self.play(Write(main_text), run_time=1.5)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.0)
        self.add(vline)
        self.play(GrowFromCenter(dot), Create(signal), run_time=1.0)
        self.play(MoveAlongPath(dot, signal), run_time=1.0)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(0.5)
        # --- Scene 2: Step 2: Complex waves built from simple ones ---
        self.clear()
        # --- Scene 2: Step 2: Complex waves built from simple ones ---
        self.clear()
        self.camera.background_color = "#181825"

        # --- Title ---
        title = Text(
            "Complex waves built from simple ones",
            font_size=36,
            color="#CDD6F4",
            font="Sans",
        ).to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.0)

        # --- Axes ---
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=9,
            y_length=6,
            axis_config={
                "color": "#fab387",
                "include_tip": True,
                "stroke_width": 2.0,
            },
            x_axis_config={"numbers_to_include": [-2, -1, 1, 2]},
            y_axis_config={"numbers_to_include": [-1, 1]},
        )
        # FIX: color is set on the MathTex object, not via get_*_axis_label kwargs
        x_label = axes.get_x_axis_label(MathTex(r"x", color="#fab387"))
        y_label = axes.get_y_axis_label(MathTex(r"f(x)", color="#fab387"))
        self.play(
            Create(axes),
            FadeIn(x_label),
            FadeIn(y_label),
            run_time=1.0,
        )

        # --- Subtitle for simple waves ---
        subtitle = Text(
            "Simple sine waves of different frequencies",
            font_size=22,
            color="#A6ADC8",
            font="Sans",
        ).next_to(axes, UP, buff=0.3)
        self.play(FadeIn(subtitle), run_time=0.5)

        # --- Simple sine waves (fundamental + harmonics) ---
        wave1 = axes.plot(lambda x: np.sin(PI * x), color="#a6e3a1", x_range=[-3, 3])
        wave2 = axes.plot(
            lambda x: 0.5 * np.sin(3 * PI * x), color="#89b4fa", x_range=[-3, 3]
        )
        wave3 = axes.plot(
            lambda x: 0.3 * np.sin(5 * PI * x), color="#f38ba8", x_range=[-3, 3]
        )

        label1 = Text("1x", font_size=16, color="#a6e3a1").move_to(axes.c2p(2.6, 0.9))
        label2 = Text("3x", font_size=16, color="#89b4fa").move_to(axes.c2p(2.4, 0.55))
        label3 = Text("5x", font_size=16, color="#f38ba8").move_to(axes.c2p(2.2, 0.25))

        self.play(Create(wave1), FadeIn(label1), run_time=1.5)
        self.play(Create(wave2), FadeIn(label2), run_time=1.0)
        self.play(Create(wave3), FadeIn(label3), run_time=1.0)

        # --- Combine simple waves into the complex wave ---
        complex_wave = axes.plot(
            lambda x: (
                np.sin(PI * x) + 0.5 * np.sin(3 * PI * x) + 0.3 * np.sin(5 * PI * x)
            ),
            color="#fab387",
            x_range=[-3, 3],
        )
        sum_label = Text(
            "Sum  →  Complex wave",
            font_size=24,
            color="#fab387",
            font="Sans",
        ).move_to(axes.c2p(0, -1.7))

        simple_group = VGroup(wave1, wave2, wave3, label1, label2, label3, subtitle)
        self.play(
            FadeOut(simple_group),
            Create(complex_wave),
            FadeIn(sum_label),
            run_time=1.0,
        )

        self.wait(0.5)
        # --- Scene 3: Step 3: Sine waves as building blocks ---
        self.clear()
        # --- Scene 3: Step 3: Sine waves as building blocks ---
        config.background_color = "#181825"

        axis_y = -2.8
        k = PI / 2.0  # frequency: period = 2*PI/k = 4 units
        A = 1.0  # amplitude

        # --- Title ---
        title = Text(
            "Sine waves as building blocks",
            font_size=36,
            color=WHITE,
        ).shift(UP * 3)

        # --- NumberLine as the x-axis ---
        number_line = NumberLine(
            x_range=[-5, 5],
            length=10,
            color="#f38ba8",
            include_numbers=False,
        )
        number_line.shift(DOWN * 2.8)

        # --- The sine wave built on the axis ---
        wave = ParametricFunction(
            lambda t: np.array([t, axis_y + A * np.sin(k * t), 0.0]),
            t_range=[-5, 5],
            color="#89b4fa",
            stroke_width=3,
        )

        # --- Frequency: a brace spanning exactly one period (4 units) ---
        freq_brace = BraceBetweenPoints(
            point_1=np.array([-5.0, axis_y, 0.0]),
            point_2=np.array([-1.0, axis_y, 0.0]),
            direction=DOWN,
            color="#fab387",
        )
        freq_label = Text("Frequency", font_size=26, color="#fab387")
        freq_label.next_to(freq_brace, DOWN, buff=0.15)

        # --- Amplitude: vertical arrow from axis to peak (x = 1) ---
        amp_arrow = Arrow(
            start=np.array([1.0, axis_y, 0.0]),
            end=np.array([1.0, axis_y + A, 0.0]),
            color="#a6e3a1",
            stroke_width=4,
            buff=0.0,
        )
        amp_label = Text("Amplitude", font_size=26, color="#a6e3a1")
        amp_label.next_to(amp_arrow, RIGHT, buff=0.2)

        # --- Phase shift: horizontal arrow showing horizontal displacement ---
        phase_arrow = Arrow(
            start=np.array([0.0, axis_y + A + 0.8, 0.0]),
            end=np.array([2.0, axis_y + A + 0.8, 0.0]),
            color="#94e2d5",
            stroke_width=4,
            buff=0.0,
        )
        phase_label = Text("Phase shift", font_size=26, color="#94e2d5")
        phase_label.next_to(phase_arrow, UP, buff=0.15)

        # --- Animations ---
        self.play(Write(title), run_time=1.0)
        self.play(GrowFromCenter(number_line), run_time=1.2)
        self.play(Create(wave), run_time=1.3)
        self.play(
            Create(freq_brace),
            Write(freq_label),
            run_time=0.8,
        )
        self.play(
            FadeIn(amp_arrow),
            Write(amp_label),
            run_time=0.8,
        )
        self.play(
            FadeIn(phase_arrow),
            Write(phase_label),
            run_time=0.8,
        )
        self.play(Indicate(wave, color="#89b4fa"), run_time=0.6)
        self.wait(0.5)
        # --- Scene 4: Step 4: Superposition of waves ---
        self.clear()
        self.camera.background_color = "#181825"

        # --- Title ---
        title = Text("Superposition of waves", font_size=36, color=WHITE, font="Sans")
        title.move_to(UP * 3)

        # --- Axes ---
        axes = Axes(
            x_range=[-PI, PI, PI / 2],
            y_range=[-2.5, 2.5, 1],
            x_length=9,
            y_length=4,
            axis_config={"color": "#94e2d5", "stroke_width": 2},
            tips=False,
        )

        x_label = axes.get_x_axis_label(MathTex("x"), edge=RIGHT, direction=DOWN)
        y_label = axes.get_y_axis_label(MathTex("y"), edge=UP)

        # --- Wave functions ---
        wave1_func = lambda x: np.sin(x)
        wave2_func = lambda x: 0.6 * np.sin(2 * x)
        comb_func = lambda x: wave1_func(x) + wave2_func(x)

        wave1 = axes.plot(wave1_func, color="#f38ba8", stroke_width=3)
        wave2 = axes.plot(wave2_func, color="#89b4fa", stroke_width=3)
        combined = axes.plot(comb_func, color="#a6e3a1", stroke_width=4)

        w1_label = MathTex("y_1=\\sin x", color="#f38ba8").next_to(
            wave1.get_end(), UP, buff=0.2
        )
        w2_label = MathTex("y_2=0.6\\sin 2x", color="#89b4fa").next_to(
            wave2.get_start(), DOWN, buff=0.2
        )
        comb_label = MathTex("y_1+y_2", color="#a6e3a1").next_to(
            combined.get_top(), UP, buff=0.1
        )

        # main_4 : the superposition VGroup (combined wave + its label)
        main_4 = VGroup(combined, comb_label)
        main_4.set_color("#a6e3a1")

        # --- Stacking visualization at a sample x ---
        sample_x = 1.0
        base = axes.c2p(sample_x, 0)
        p1 = axes.i2gp(sample_x, wave1)
        pC = axes.i2gp(sample_x, combined)

        vline = DashedLine(base, pC, color="#94e2d5", dash_length=0.12)
        seg1 = Line(base, p1, color="#f38ba8", stroke_width=6)
        seg2 = Line(p1, pC, color="#89b4fa", stroke_width=6)
        arrow_add = Arrow(p1, pC, color="#89b4fa", buff=0.1, tip_length=0.2)
        label_add = MathTex("+y_2", color="#89b4fa").next_to(arrow_add, RIGHT, buff=0.1)
        dot1 = Dot(p1, color="#f38ba8", radius=0.09)
        dotC = Dot(pC, color="#a6e3a1", radius=0.09)

        # ================= ANIMATIONS =================
        self.play(Write(title), run_time=0.8)

        self.play(GrowFromCenter(axes), run_time=0.8)

        self.play(FadeIn(x_label), FadeIn(y_label), run_time=0.4)

        self.play(Create(wave1), run_time=1.0)

        self.play(Create(wave2), run_time=1.0)

        self.play(FadeIn(w1_label), FadeIn(w2_label), run_time=0.4)

        # Show point-by-point stacking of heights
        self.play(
            GrowFromCenter(seg1),
            GrowFromCenter(seg2),
            Create(vline),
            GrowFromCenter(dot1),
            GrowFromCenter(dotC),
            GrowFromCenter(arrow_add),
            Write(label_add),
            run_time=1.2,
        )

        # Draw the combined (superposed) wave
        self.play(Create(combined), FadeIn(comb_label), run_time=1.2)

        # Emphasize the resulting superposed wave
        self.play(Indicate(combined, color="#fab387", scale_factor=1.05), run_time=0.8)

        self.wait(0.4)
        # --- Scene 5: Step 5: The frequency domain ---
        self.clear()
        # --- Scene 5: Step 5: The frequency domain ---
        C_BG = "#181825"
        C_BLUE = "#89b4fa"
        C_PEACH = "#fab387"
        C_PINK = "#f38ba8"
        C_GREEN = "#a6e3a1"
        C_TEAL = "#94e2d5"
        C_WHITE = "#cdd6f4"

        self.camera.background_color = C_BG
        self.clear()

        # --- Title and subtitle (Write) ---
        title = Text("The frequency domain", font_size=36, color=C_WHITE)
        title.to_edge(UP, buff=0.5)
        subtitle = Text(
            "A signal seen as a spectrum of frequency bars",
            font_size=22,
            color=C_GREEN,
        ).next_to(title, DOWN, buff=0.25)

        # --- Main Table: the frequency domain (GrowFromCenter) ---
        col_labels = [
            Text("Frequency", font_size=24, color=C_BLUE),
            Text("Amplitude", font_size=24, color=C_PEACH),
            Text("Meaning", font_size=24, color=C_TEAL),
        ]
        freq_table = (
            Table(
                [
                    ["50 Hz", "1.0", "Loud fundamental tone"],
                    ["120 Hz", "0.4", "Softer harmonic"],
                    ["300 Hz", "0.2", "Faint overtone"],
                ],
                col_labels=col_labels,
                include_outer_lines=True,
                color=C_BLUE,
                element_to_mobject=Text,
                element_to_mobject_config={"font_size": 22, "color": C_WHITE},
            )
            .scale(0.8)
            .shift(UP * 0.2)
        )

        # --- Amplitude spectrum bars (supporting visual metaphor) ---
        amps = [1.0, 0.4, 0.2]
        freqs = ["50", "120", "300"]
        colors = [C_BLUE, C_PEACH, C_PINK]
        bar_units = VGroup()
        for a, f, c in zip(amps, freqs, colors):
            h = a * 1.3
            bar = Rectangle(
                width=0.7,
                height=h,
                fill_color=c,
                fill_opacity=0.85,
                stroke_color=C_WHITE,
                stroke_width=2,
            )
            lab = Text(f"{f} Hz", font_size=18, color=c).next_to(bar, DOWN, buff=0.2)
            bar_units.add(VGroup(bar, lab))
        bar_units.arrange(RIGHT, buff=0.9).shift(DOWN * 1.9)

        bars = VGroup(*[u[0] for u in bar_units])
        labels = VGroup(*[u[1] for u in bar_units])

        spectrum_title = Text("Amplitude spectrum", font_size=20, color=C_TEAL).next_to(
            bar_units, UP, buff=0.35
        )

        # --- Connector arrow from table to spectrum ---
        arrow = Arrow(
            freq_table.get_bottom() + DOWN * 0.05,
            bar_units.get_top() + UP * 0.05,
            color=C_TEAL,
            buff=0.1,
            stroke_width=3,
        )

        # --- Animation sequence (total run_time = 8.5) ---
        self.play(Write(title), run_time=1.0)
        self.play(Write(subtitle), run_time=0.8)
        self.play(GrowFromCenter(freq_table), run_time=2.0)
        self.play(FadeIn(arrow, scale=0.5), run_time=0.6)
        self.play(
            LaggedStart(*[GrowFromCenter(b) for b in bars], lag_ratio=0.3),
            run_time=1.3,
        )
        self.play(Write(labels), Write(spectrum_title), run_time=1.0)
        self.play(Indicate(bars[0], color=C_TEAL, scale_factor=1.15), run_time=0.8)
        self.wait(1.0)
        # --- Scene 6: Step 6: The Fourier transform operation ---
        self.clear()
        self.camera.background_color = "#181825"

        # Palette
        c_blue = "#89b4fa"
        c_orange = "#fab387"
        c_pink = "#f38ba8"
        c_green = "#a6e3a1"
        c_teal = "#94e2d5"
        c_white = "#cdd6f4"

        # --- Title (title_6) ---
        title_6 = Text("The Fourier transform operation", font_size=36, color=WHITE)
        title_6.to_edge(UP, buff=0.6)
        self.play(Write(title_6), run_time=1.0)

        # --- Time Domain (left) ---
        time_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=4.0,
            y_length=2.0,
            axis_config={"color": c_white, "include_tip": True},
        ).shift(LEFT * 3.2 + DOWN * 0.3)
        time_label = Text("Time Domain", font_size=24, color=c_blue)
        time_label.next_to(time_axes, UP, buff=0.3)

        # Composite wave: sum of two sine components
        composite = time_axes.plot(
            lambda x: (
                0.9 * np.sin(2 * np.pi * x) + 0.45 * np.sin(2 * np.pi * 2 * x + 0.5)
            ),
            color=c_pink,
            x_range=[0, 4],
        )
        self.play(
            FadeIn(time_axes, time_label, shift=UP * 0.2),
            run_time=0.8,
        )
        self.play(Create(composite), run_time=1.2)

        # --- Main arrow (main_6) ---
        main_6 = Arrow(
            start=LEFT * 1.0 + DOWN * 0.3,
            end=RIGHT * 1.0 + DOWN * 0.3,
            color=c_white,
            stroke_width=4,
            buff=0.2,
        )
        ft_label = (
            MathTex(r"\mathcal{F}", color=c_teal)
            .scale(1.1)
            .next_to(main_6, UP, buff=0.15)
        )
        self.play(GrowFromCenter(main_6), FadeIn(ft_label), run_time=0.8)

        # --- Frequency Domain (right) ---
        freq_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1.2, 1],
            x_length=4.0,
            y_length=2.0,
            axis_config={"color": c_white, "include_tip": True},
        ).shift(RIGHT * 3.2 + DOWN * 0.3)
        freq_label = Text("Frequency Domain", font_size=24, color=c_orange)
        freq_label.next_to(freq_axes, UP, buff=0.3)

        self.play(
            FadeIn(freq_axes, freq_label, shift=UP * 0.2),
            run_time=0.8,
        )

        # Spectrum bars (one per component frequency)
        def make_bar(axes, x, value, color):
            bottom = axes.c2p(x, 0)
            top = axes.c2p(x, value)
            height = top[1] - bottom[1]
            bar = Rectangle(width=0.35, height=height, color=color, fill_opacity=0.85)
            bar.move_to([top[0], (top[1] + bottom[1]) / 2, 0])
            return bar

        bar1 = make_bar(freq_axes, 1, 0.9, c_green)
        bar2 = make_bar(freq_axes, 2, 0.45, c_green)
        self.play(GrowFromCenter(bar1), GrowFromCenter(bar2), run_time=1.0)

        f1 = MathTex("f_1", color=c_white).scale(0.7).next_to(bar1, DOWN, buff=0.1)
        f2 = MathTex("f_2", color=c_white).scale(0.7).next_to(bar2, DOWN, buff=0.1)
        self.play(FadeIn(f1, f2), run_time=0.6)

        # Highlight the transform mapping
        self.play(Indicate(main_6, color=c_teal), run_time=0.5)

        # Total animation time = 1.0+0.8+1.2+0.8+0.8+1.0+0.6+0.5 = 6.7
        self.wait(0.8)
        # --- Scene 7: Step 7: The inverse Fourier transform ---
        self.camera.background_color = "#181825"
        self.clear()

        # --- Title ---
        title = Text("The inverse Fourier transform", font_size=36, color=WHITE)
        title.move_to(UP * 3.3)

        # --- Frequency spectrum (left) ---
        freq_label = Text("Frequency spectrum", font_size=24, color="#fab387")
        freq_label.move_to(LEFT * 3.0 + UP * 2.0)

        bars = VGroup()
        heights = [0.5, 1.2, 0.8, 1.5, 0.6, 1.0, 0.4]
        for i, h in enumerate(heights):
            bar = Rectangle(
                width=0.34,
                height=h,
                color="#a6e3a1",
                stroke_width=2,
                fill_opacity=0.85,
            )
            bar.move_to(LEFT * 4.4 + i * 0.5 * RIGHT + UP * (h / 2))
            bars.add(bar)
        spectrum = VGroup(freq_label, bars)

        # --- Transform arrow (center) ---
        arrow = Arrow(
            start=LEFT * 1.2 + UP * 0.9,
            end=RIGHT * 1.2 + UP * 0.9,
            color="#94e2d5",
            buff=0.15,
            stroke_width=5,
            tip_length=0.3,
        )

        # --- Time wave (right) ---
        time_label = Text("Time wave", font_size=24, color="#f38ba8")
        time_label.move_to(RIGHT * 3.5 + UP * 1.4)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=3,
            y_length=2,
            axis_config={"color": "#89b4fa", "stroke_width": 2},
        )
        axes.move_to(RIGHT * 3.5)

        def wave_func(x):
            return 0.8 * np.sin(x) + 0.35 * np.sin(3 * x) + 0.18 * np.sin(5 * x)

        wave = axes.plot(wave_func, color="#f38ba8", stroke_width=4)
        time_group = VGroup(time_label, axes, wave)

        # --- Main text (center) ---
        main = Text("Frequency  →  Time", font_size=46, color="#89b4fa")
        main.move_to(ORIGIN)

        # --- Caption ---
        caption = Text(
            "Rebuild the original time wave from its frequency spectrum",
            font_size=24,
            color="#cdd6f4",
        )
        caption.move_to(DOWN * 2.2)

        # --- Animations ---
        self.play(Write(title), run_time=1.0)
        self.play(
            LaggedStart(*[GrowFromCenter(b) for b in bars], lag_ratio=0.12),
            FadeIn(freq_label, shift=UP * 0.2),
            run_time=1.5,
        )
        self.play(FadeIn(arrow), run_time=0.8)
        self.play(
            FadeIn(time_label, shift=UP * 0.2),
            Create(axes),
            Create(wave),
            run_time=1.5,
        )
        self.play(Write(main), run_time=1.2)
        self.play(FadeIn(caption), run_time=1.0)
        self.wait(1.0)
        # --- Scene 8: Step 8: Applications in filtering ---
        self.camera.background_color = "#181825"
        self.clear()

        # --- Title ---
        title = Text("Applications in filtering", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # --- Axes ---
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": "#fab387", "include_tip": True},
        )

        x_label = Text("Frequency", font_size=22, color="#94e2d5")
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Magnitude", font_size=22, color="#94e2d5")
        y_label.next_to(axes.y_axis, LEFT, buff=0.2)

        # --- Frequency spectrum bars ---
        xs = np.arange(-2.5, 2.51, 0.5)
        bars = VGroup()
        signal_bars = VGroup()
        noise_bars = VGroup()
        for x in xs:
            h = 1.8 * np.exp(-((x / 1.5) ** 2))
            bar = Rectangle(
                width=0.35,
                height=h,
                stroke_width=1.5,
                fill_opacity=0.85,
            )
            bar.move_to(axes.c2p(x, h / 2))
            if abs(x) >= 2:
                bar.set_color("#f38ba8")
                noise_bars.add(bar)
            else:
                bar.set_color("#89b4fa")
                signal_bars.add(bar)
            bars.add(bar)

        # --- Noise annotation ---
        noise_label = Text(
            "Unwanted\nhigh frequencies",
            font_size=20,
            color="#f38ba8",
            line_spacing=1.2,
        )
        noise_label.move_to(axes.c2p(1.7, 2.4))
        arrow = Arrow(
            axes.c2p(2.2, 2.1),
            axes.c2p(2.4, 0.6),
            color="#f38ba8",
            buff=0.05,
            stroke_width=2.5,
        )

        # --- Filtered result annotation ---
        clean_label = Text(
            "Filtered: clean low-frequency signal",
            font_size=20,
            color="#a6e3a1",
        )
        clean_label.next_to(x_label, DOWN, buff=0.3)
        surround = SurroundingRectangle(signal_bars, color="#a6e3a1", buff=0.2)

        # --- Animation sequence ---
        self.play(Write(title), run_time=1.0)
        self.play(Create(axes), run_time=1.0)
        self.play(
            LaggedStart(*[FadeIn(bar) for bar in bars], lag_ratio=0.06),
            FadeIn(x_label),
            FadeIn(y_label),
            run_time=1.5,
        )
        self.play(
            FadeIn(noise_label),
            FadeIn(arrow),
            Indicate(noise_bars, color="#f38ba8"),
            run_time=1.0,
        )
        self.play(
            FadeOut(noise_bars),
            FadeOut(noise_label),
            FadeOut(arrow),
            run_time=1.5,
        )
        self.play(
            GrowFromCenter(surround),
            FadeIn(clean_label),
            run_time=1.0,
        )
        self.wait(1.0)
