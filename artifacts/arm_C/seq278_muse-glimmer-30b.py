import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Sinusoids as Building Blocks ---
        # Style
        self.camera.background_color = "#181825"

        # Central time axes
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": "#89b4fa", "stroke_width": 2},
            tips=False,
        )
        axes.add_coordinates()

        x_label = axes.get_x_axis_label("t")
        x_label.set_color("#89b4fa")
        x_label.set_font_size(36)

        # Stacked sine building blocks
        offset_low = 1.2
        offset_mid = 0.0
        offset_high = -1.2

        sine_low = axes.plot(
            lambda x: offset_low + 0.6 * np.sin(1 * x), color="#89b4fa", stroke_width=2
        )
        sine_mid = axes.plot(
            lambda x: offset_mid + 0.4 * np.sin(2 * x), color="#fab387", stroke_width=2
        )
        sine_high = axes.plot(
            lambda x: offset_high + 0.3 * np.sin(4 * x), color="#f38ba8", stroke_width=2
        )

        # Labels
        stack_label = Text("Fundamental building blocks", color="#a6e3a1", font_size=36)
        stack_label.move_to(UP * 3)

        low_label = Text("low freq", color="#89b4fa", font_size=24).next_to(
            sine_low, UP, buff=0.1
        )
        mid_label = Text("mid freq", color="#fab387", font_size=24).next_to(
            sine_mid, UP, buff=0.1
        )
        high_label = Text("high freq", color="#f38ba8", font_size=24).next_to(
            sine_high, UP, buff=0.1
        )

        # Animation
        self.play(Create(axes))
        self.add(x_label)
        self.play(Create(sine_low), Create(sine_mid), Create(sine_high))
        self.play(
            FadeIn(stack_label),
            FadeIn(low_label),
            FadeIn(mid_label),
            FadeIn(high_label),
        )
        self.wait(4.5)
        # --- Scene 2: Fourier Series Harmonics ---
        # Background and style
        self.camera.background_color = "#181825"
        stroke_width = 2.0

        # Harmonic ring
        harmonic_ring = Circle(radius=2.5, color="#a6e3a1", stroke_width=stroke_width)
        harmonic_ring.set_fill(opacity=0)

        # Helper to create a spoke + label
        def make_spoke(angle_deg, color, label_text):
            angle = np.deg2rad(angle_deg)
            unit = np.array([np.cos(angle), np.sin(angle), 0])
            end_point = 2.5 * unit
            arrow = Arrow(
                start=ORIGIN,
                end=end_point,
                color=color,
                stroke_width=stroke_width,
                buff=0,
                max_tip_length_to_length_ratio=0.15,
            )
            label = Text(label_text, font_size=36, color=color)
            label.move_to(end_point + 0.35 * unit)
            return VGroup(arrow, label)

        spoke_1 = make_spoke(0, "#89b4fa", "1×")
        spoke_3 = make_spoke(60, "#fab387", "3×")
        spoke_5 = make_spoke(120, "#f38ba8", "5×")

        # Waveform loop - polar Fourier series
        def waveform_func(t):
            r = 1.2 + 0.15 * np.sin(3 * t) + 0.08 * np.sin(5 * t)
            x = r * np.cos(t)
            y = r * np.sin(t)
            return np.array([x, y, 0])

        waveform_loop = ParametricFunction(
            waveform_func, t_range=[0, TAU], color="#94e2d5", stroke_width=stroke_width
        )
        waveform_label = Text("periodic signal", font_size=28, color="#94e2d5")
        waveform_label.next_to(waveform_loop, DOWN)

        # Assemble
        self.play(Create(harmonic_ring), run_time=1.5)
        self.play(Create(spoke_1[0]), Write(spoke_1[1]), run_time=0.8)
        self.play(Create(spoke_3[0]), Write(spoke_3[1]), run_time=0.8)
        self.play(Create(spoke_5[0]), Write(spoke_5[1]), run_time=0.8)
        self.play(Create(waveform_loop), Write(waveform_label), run_time=1.5)

        self.wait(2)
        # --- Scene 3: From Discrete to Continuous Frequencies ---
        self.camera.background_color = "#181825"

        # Title
        title = Text(
            "From Discrete to Continuous Frequencies", font_size=36, color=WHITE
        )
        title.to_edge(UP)

        # Frequency number line at bottom
        freq_line = NumberLine(
            x_range=[-10, 10, 1],
            length=12,
            include_numbers=False,
            color="#94e2d5",
            stroke_width=2.0,
        )
        freq_line.add_numbers()
        freq_line.move_to(DOWN * 2.5)

        # Frequency label
        freq_label = Text("frequency", font_size=24, color="#94e2d5")
        freq_label.next_to(freq_line, DOWN, buff=0.2)

        # Discrete ticks (dots)
        dot_positions = [-7, -5, -3, -1, 1, 3, 5, 7]
        discrete_dots = VGroup(
            *[
                Dot(radius=0.08, color="#fab387", stroke_width=2.0).move_to(
                    freq_line.n2p(x)
                )
                for x in dot_positions
            ]
        )

        # Continuous density line
        continuous_line = Line(
            start=freq_line.get_left(),
            end=freq_line.get_right(),
            color="#89b4fa",
            stroke_width=8,
            stroke_opacity=0.6,
        )
        continuous_line.move_to(freq_line.get_center())

        # Infinity arrow
        infinity_arrow = Arrow(
            start=RIGHT * 2.5, end=RIGHT * 4.0, color="#f38ba8", stroke_width=2.0
        )
        infinity_label = Text("T → ∞", font_size=36, color="#f38ba8")
        infinity_label.next_to(infinity_arrow, UP)
        infinity_group = VGroup(infinity_arrow, infinity_label).move_to(RIGHT * 3)

        # Animations - total 9.5 s
        self.play(FadeIn(title, shift=UP * 0.2), run_time=1.0)
        self.play(Create(freq_line), run_time=1.5)
        self.play(FadeIn(freq_label), run_time=0.5)
        self.play(
            LaggedStart(
                *[FadeIn(dot, scale=1.5) for dot in discrete_dots], lag_ratio=0.1
            ),
            run_time=2.0,
        )
        self.play(FadeIn(infinity_group, shift=LEFT * 0.3), run_time=1.0)

        # Transition discrete -> continuous
        self.play(
            FadeOut(discrete_dots, shift=DOWN * 0.2),
            FadeIn(continuous_line, scale=0.5),
            run_time=2.0,
        )

        self.wait(1.5)
        # --- Scene 4: Continuous Fourier Transform Integral ---
        self.camera.background_color = "#181825"

        # 1. Objects
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": "#89b4fa", "stroke_width": 2.0},
        )
        axes.move_to(ORIGIN)
        axes_label = Text("t → ω", font_size=36, color="#89b4fa")
        axes_label.next_to(axes, UP)

        # Fixed: use Axes.plot instead of get_graph with x_range keyword
        time_signal = axes.plot(lambda x: np.sin(x), x_range=[-4, 4], color="#a6e3a1")
        time_signal.stroke_width = 2.0
        signal_label = Text("x(t)", font_size=36, color="#a6e3a1")
        signal_label.next_to(time_signal.get_end(), UP)

        phasor_arrow = Arrow(
            start=ORIGIN, end=UP * 1.5, color="#f38ba8", stroke_width=2.0
        )
        phasor_arrow.shift(UP * 2.5)
        phasor_label = MathTex(r"e^{-j\omega t}", color="#f38ba8")
        phasor_label.next_to(phasor_arrow, RIGHT)
        phasor_group = VGroup(phasor_arrow, phasor_label)

        integral_formula = MathTex(
            r"X(\omega)=\int x(t)e^{-j\omega t}\,dt", color="#fab387"
        )
        integral_formula.scale(0.8)
        integral_formula.next_to(axes, RIGHT, buff=1.5)

        # 2. Animations
        self.play(FadeIn(axes, run_time=1), FadeIn(axes_label, run_time=1))
        self.play(Create(time_signal, run_time=1.5), FadeIn(signal_label, run_time=1.5))
        self.play(FadeIn(phasor_group, run_time=1.5))
        self.play(
            Rotate(
                phasor_arrow,
                angle=2 * PI,
                about_point=phasor_arrow.get_start(),
                run_time=2,
            )
        )
        self.play(FadeIn(integral_formula, run_time=1.5))

        # 3. Wait to match 8.0s total
        self.wait(0.5)
        # --- Scene 5: Magnitude and Phase Spectrum ---
        # style
        self.camera.background_color = "#181825"

        title = Text("Magnitude & Phase", font_size=48, color="#89b4fa")
        title.to_edge(UP)
        self.play(FadeIn(title))

        # Magnitude bars
        values = [0.8, 0.5, 0.3, 0.1]
        # Use plain ASCII names to avoid LaTeX compilation in BarChart x-axis labels
        bar_names = ["w1", "w2", "w3", "w4"]
        bar_chart = BarChart(values=values, bar_names=bar_names, y_range=[0, 1, 0.2])
        bar_chart.set_stroke(width=2.0)
        bar_chart.set_fill("#fab387", opacity=0.8)
        bar_chart.set_color("#fab387")
        bar_chart.scale(0.8)
        bar_chart.to_edge(LEFT)

        mag_label = MathTex("|X(\\omega)|", color="#fab387", font_size=36)
        mag_label.next_to(bar_chart, DOWN)

        self.play(Create(bar_chart), FadeIn(mag_label))

        # Phase arrows on top of each bar
        bars = bar_chart.bars
        phase_arrows = VGroup()
        angles = [0.0, 0.5, -0.5, 1.0]  # timing offset per frequency

        for i, bar in enumerate(bars):
            top = bar.get_top()
            start = top + UP * 0.12
            ang = angles[i]
            direction = np.array([0.35 * np.sin(ang), 0.55 * np.cos(ang), 0])
            end = start + direction
            arrow = Arrow(
                start=start, end=end, color="#f38ba8", stroke_width=2.0, buff=0
            )
            phase_arrows.add(arrow)

        phase_label = Text("phase", font_size=28, color="#f38ba8")
        phase_label.next_to(phase_arrows, UP)

        self.play(
            LaggedStart(*[GrowFromCenter(a) for a in phase_arrows], lag_ratio=0.2)
        )
        self.play(FadeIn(phase_label))

        self.wait(2)
        # --- Scene 6: Key Transform Properties ---
        self.camera.background_color = "#181825"

        # Flow start
        start_rect = Rectangle(
            width=2.2,
            height=1.2,
            fill_color="#a6e3a1",
            fill_opacity=0.85,
            stroke_width=2.0,
            stroke_color="#a6e3a1",
        ).move_to(LEFT * 4)
        start_label = Text("x(t)", font_size=36, color=WHITE)
        start_label.move_to(start_rect.get_center())
        flow_start = VGroup(start_rect, start_label)

        # Flow end
        end_rect = Rectangle(
            width=2.2,
            height=1.2,
            fill_color="#f38ba8",
            fill_opacity=0.85,
            stroke_width=2.0,
            stroke_color="#f38ba8",
        ).move_to(RIGHT * 4)
        end_label = Text("X(ω)", font_size=36, color=WHITE)
        end_label.move_to(end_rect.get_center())
        flow_end = VGroup(end_rect, end_label)

        # Arrows
        y_positions = [1.6, 0, -1.6]
        arrow_data = [
            ("linearity", "#89b4fa"),
            ("time shift → phase", "#fab387"),
            ("convolution → multiplication", "#94e2d5"),
        ]

        arrows = VGroup()
        arrow_labels = VGroup()
        for y, (lab, col) in zip(y_positions, arrow_data):
            start_pt = start_rect.get_right() + RIGHT * 0.4 + UP * y
            end_pt = end_rect.get_left() - RIGHT * 0.4 + UP * y
            arr = Arrow(start_pt, end_pt, buff=0, stroke_width=2.5, color=col)
            label = Text(lab, font_size=28, color=WHITE)
            label.next_to(arr, UP if y >= 0 else DOWN, buff=0.15)
            arrows.add(arr)
            arrow_labels.add(label)

        narration = (
            Text(
                "Key properties simplify analysis: linearity preserves sums, time shift adds phase, convolution becomes multiplication in frequency.",
                font_size=26,
                color=WHITE,
            )
            .scale(0.9)
            .move_to(DOWN * 3)
        )

        # Animations
        self.play(FadeIn(flow_start), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(arrows[0]), run_time=0.7)
        self.play(FadeIn(arrow_labels[0]), run_time=0.3)
        self.play(FadeIn(arrows[1]), run_time=0.7)
        self.play(FadeIn(arrow_labels[1]), run_time=0.3)
        self.play(FadeIn(arrows[2]), run_time=0.7)
        self.play(FadeIn(arrow_labels[2]), run_time=0.3)
        self.play(FadeIn(flow_end), run_time=1.0)
        self.play(FadeIn(narration), run_time=1.5)
        self.wait(1.9)
        # --- Scene 7: Discrete Fourier Transform ---
        self.camera.background_color = "#181825"

        # Sample grid left
        sample_dots = VGroup()
        color_samples = "#89b4fa"
        for i in range(4):
            for j in range(8):
                dot = Dot(radius=0.05, color=color_samples)
                dot.move_to(LEFT * 3 + RIGHT * 0.4 * j + UP * 0.3 * i)
                sample_dots.add(dot)
        sample_dots.set_stroke(width=2.0)
        sample_label = Text("samples", font_size=24, color=color_samples)
        sample_label.next_to(sample_dots, DOWN)
        sample_group = VGroup(sample_dots, sample_label)

        # Sampling arrow
        arrow_start = sample_dots.get_right() + RIGHT * 0.5
        arrow_end = np.array([0, 0, 0]) + LEFT * 0.5
        sampling_arrow = Arrow(
            arrow_start, arrow_end, color="#a6e3a1", stroke_width=2.0
        )
        arrow_label = Text("sampled → DFT", font_size=24, color="#a6e3a1")
        arrow_label.next_to(sampling_arrow, UP)

        # Butterfly network center
        butterfly_color = "#94e2d5"
        nodes = VGroup()
        lines = VGroup()
        cols = [-1.5, 0, 1.5]
        rows = [-1.2, -0.4, 0.4, 1.2]
        positions = {}
        for ci, cx in enumerate(cols):
            for ri, y in enumerate(rows):
                d = Dot(radius=0.07, color=butterfly_color)
                d.move_to(np.array([cx, y, 0]))
                nodes.add(d)
                positions[(ci, ri)] = d
        for ci in range(len(cols) - 1):
            for ri in range(len(rows)):
                start = positions[(ci, ri)]
                end1 = positions[(ci + 1, ri)]
                lines.add(
                    Line(
                        start.get_center(),
                        end1.get_center(),
                        color=butterfly_color,
                        stroke_width=2,
                    )
                )
                ri2 = ri ^ 1 if ci == 0 else ri
                end2 = positions[(ci + 1, ri2)]
                if end2 != end1:
                    lines.add(
                        CurvedArrow(
                            start.get_center(),
                            end2.get_center(),
                            angle=0.6,
                            color=butterfly_color,
                            stroke_width=2,
                        )
                    )
        butterfly_network = VGroup(nodes, lines)
        butterfly_label = Text("FFT butterfly", font_size=24, color=butterfly_color)
        butterfly_label.next_to(butterfly_network, DOWN)

        # Frequency bins right
        bar_color = "#fab387"
        values = [0.6, 0.9, 0.4, 0.7, 0.3, 0.8, 0.5, 0.2]
        bar_names = ["0", "1", "2", "3", "4", "5", "6", "7"]
        bar_chart = BarChart(
            values=values,
            bar_names=bar_names,
            y_range=[0, 1, 0.2],
            x_length=4,
            y_length=3,
        )
        bar_chart.to_edge(RIGHT)
        bar_chart.set_stroke(width=2.0)
        bar_chart.set_fill(bar_color, opacity=0.8)
        bar_chart.set_color(bar_color)
        freq_label = Text("X[k]", font_size=28, color=bar_color)
        freq_label.next_to(bar_chart, UP)

        # Animations total 9.0s
        self.play(FadeIn(sample_group), run_time=1.5)
        self.wait(0.5)
        self.play(Create(sampling_arrow), FadeIn(arrow_label), run_time=1.0)
        self.wait(0.5)
        self.play(Create(butterfly_network), FadeIn(butterfly_label), run_time=2.0)
        self.wait(0.5)
        self.play(GrowFromCenter(bar_chart), FadeIn(freq_label), run_time=2.0)
        self.wait(1.0)
