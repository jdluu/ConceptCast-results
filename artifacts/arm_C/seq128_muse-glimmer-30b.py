import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Periodic signals as sum of sinusoids ---
        self.camera.background_color = "#181825"

        omega = np.pi / 2  # one period over 4 units

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": "#89b4fa", "stroke_width": 2},
            tips=False,
        )
        axes_labels = axes.get_axis_labels(x_label="t")
        axes_labels[0].set_color("#89b4fa")
        axes_group = VGroup(axes, axes_labels)

        title = Text(
            "Periodic signals as sum of sinusoids",
            font="Sans",
            font_size=36,
            color=WHITE,
        )
        title.to_edge(UP)

        fundamental_sine = axes.plot(
            lambda x: 0.6 * np.sin(omega * x), color="#a6e3a1", stroke_width=2
        )
        fundamental_sine.set_opacity(0.6)

        harmonic_cosine = axes.plot(
            lambda x: 0.4 * np.cos(2 * omega * x), color="#94e2d5", stroke_width=2
        )
        harmonic_cosine.set_opacity(0.6)

        third_harmonic = axes.plot(
            lambda x: 0.3 * np.sin(3 * omega * x), color="#fab387", stroke_width=2
        )
        third_harmonic.set_opacity(0.6)

        sum_waveform = axes.plot(
            lambda x: (
                0.6 * np.sin(omega * x)
                + 0.4 * np.cos(2 * omega * x)
                + 0.3 * np.sin(3 * omega * x)
            ),
            color="#f38ba8",
            stroke_width=3,
        )

        self.play(Create(axes_group), Write(title), run_time=1)
        self.wait(0.5)

        self.play(Create(fundamental_sine), run_time=1)
        self.wait(0.5)

        self.play(Create(harmonic_cosine), run_time=1)
        self.wait(0.5)

        self.play(Create(third_harmonic), run_time=1)
        self.wait(0.5)

        self.play(Create(sum_waveform), run_time=1.5)
        self.wait(1.0)
        # --- Scene 2: Complex exponentials via Euler ---
        self.camera.background_color = "#181825"

        # Unit circle left
        unit_circle = Circle(radius=1.5, color="#89b4fa", stroke_width=2)
        unit_circle.move_to(LEFT * 3 + UP * 0.5)

        # Rotating point
        dot = Dot(radius=0.08, color="#fab387")
        dot.move_to(unit_circle.point_at_angle(0))

        # Euler formula text right
        euler_text = MathTex(
            r"e^{i\omega t}= \cos(\omega t) + i\sin(\omega t)",
            color="#94e2d5",
            font_size=48,
        )
        euler_text.move_to(RIGHT * 3 + UP * 2.5)

        # Time plot axes
        axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.2, 1.2, 0.6],
            x_length=6,
            y_length=3,
            axis_config={"color": "#89b4fa", "stroke_width": 2},
        )
        axes.move_to(RIGHT * 2 + DOWN * 1.5)

        cos_graph = axes.plot(lambda x: np.cos(x), color="#a6e3a1", stroke_width=2)
        sin_graph = axes.plot(lambda x: np.sin(x), color="#fab387", stroke_width=2)

        t_label = Text("t →", font_size=28, color="#89b4fa")
        t_label.next_to(axes.x_axis, DOWN)

        # Time tracker
        t = ValueTracker(0)

        # Rotating dot updater
        dot.add_updater(
            lambda m: m.move_to(
                unit_circle.get_center()
                + 1.5 * np.array([np.cos(t.get_value()), np.sin(t.get_value()), 0])
            )
        )

        # Projection lines Re, Im
        h_line = always_redraw(
            lambda: DashedLine(
                start=unit_circle.get_center()
                + 1.5 * np.array([np.cos(t.get_value()), np.sin(t.get_value()), 0]),
                end=unit_circle.get_center()
                + 1.5 * np.array([np.cos(t.get_value()), 0, 0]),
                color="#a6e3a1",
                stroke_width=2,
            )
        )
        v_line = always_redraw(
            lambda: DashedLine(
                start=unit_circle.get_center()
                + 1.5 * np.array([np.cos(t.get_value()), np.sin(t.get_value()), 0]),
                end=unit_circle.get_center()
                + 1.5 * np.array([0, np.sin(t.get_value()), 0]),
                color="#a6e3a1",
                stroke_width=2,
            )
        )

        # Moving points on time plots
        cos_dot = Dot(radius=0.06, color="#a6e3a1")
        sin_dot = Dot(radius=0.06, color="#fab387")
        cos_dot.add_updater(
            lambda m: m.move_to(axes.c2p(t.get_value(), np.cos(t.get_value())))
        )
        sin_dot.add_updater(
            lambda m: m.move_to(axes.c2p(t.get_value(), np.sin(t.get_value())))
        )

        # Intro
        self.play(
            Create(unit_circle),
            GrowFromCenter(dot),
            FadeIn(euler_text, scale=0.5),
            Create(axes),
            Create(cos_graph),
            Create(sin_graph),
            FadeIn(t_label),
            run_time=1.0,
        )

        self.add(h_line, v_line, cos_dot, sin_dot)

        # Rotate and trace over 5 seconds
        self.play(t.animate.set_value(2 * PI), run_time=5.0)
        # --- Scene 3: Fourier series for periodic signals ---
        self.clear()
        self.camera.background_color = "#181825"

        # 1. Frequency axis
        freq_axis = NumberLine(x_range=[0, 5, 1], length=8, include_numbers=True)
        freq_axis.set_color("#89b4fa")
        freq_axis.stroke_width = 2.0
        freq_axis.shift(DOWN * 1.5)
        freq_label = Text("Frequency ω", color="#89b4fa", font_size=28)
        freq_label.next_to(freq_axis, UP)

        # 2. Amplitude bars
        values = [1.2, 0.8, 0.5, 0.3]
        bar_chart = BarChart(
            values,
            bar_names=["1", "2", "3", "4"],
            y_range=[0, 1.5, 0.3],
            x_length=6,
            y_length=3,
        )
        bar_chart.set_fill("#fab387", opacity=0.9)
        bar_chart.set_stroke("#fab387", width=2)
        bar_chart.shift(UP * 0.5)

        # 3. Harmonic labels
        harmonic_labels = Text("k ω₀", color="#a6e3a1", font_size=32)
        harmonic_labels.next_to(bar_chart, DOWN, buff=0.5)

        # 4. Phase markers
        phase_dots = VGroup()
        if hasattr(bar_chart, "bars"):
            for bar in bar_chart.bars:
                dot = Dot(color="#f38ba8", radius=0.07)
                dot.move_to(bar.get_top() + UP * 0.3)
                phase_dots.add(dot)
        else:
            for i in range(4):
                dot = Dot(color="#f38ba8", radius=0.07)
                dot.move_to(bar_chart.get_center() + RIGHT * (i - 1.5) * 1.2 + UP * 1.8)
                phase_dots.add(dot)

        phase_label = Text("φ_k", color="#f38ba8", font_size=28)
        phase_label.next_to(phase_dots, RIGHT, buff=0.3)

        # Animations - total 7.5s
        self.play(Create(freq_axis), Write(freq_label), run_time=1.5)
        self.play(GrowFromCenter(bar_chart), run_time=1.5)
        self.play(FadeIn(harmonic_labels), run_time=1.0)
        self.play(FadeIn(phase_dots), FadeIn(phase_label), run_time=1.5)
        self.wait(2.0)
        # --- Scene 4: From discrete harmonics to continuous spectrum ---
        self.clear()
        self.camera.background_color = "#181825"

        # Discrete bars on a frequency line (LEFT)
        bar_values = [0.8, 0.5, 0.9, 0.4, 0.7, 0.3, 0.6, 0.5]
        bars = VGroup()
        for i, val in enumerate(bar_values):
            h = val * 1.5
            w = 0.45
            rect = Rectangle(
                height=h, width=w, color="#fab387", fill_opacity=0.9, stroke_width=2
            )
            x = -3.0 + i * 0.9
            rect.move_to([x, -1 + h / 2, 0])
            bars.add(rect)

        baseline = Line(start=LEFT * 3.5, end=RIGHT * 3.5, color=WHITE, stroke_width=1)
        baseline.move_to(DOWN * 1.5)
        bars.add(baseline)
        bars.move_to(LEFT * 2.5)

        # Continuous spectrum line (RIGHT)
        xs = np.linspace(-3, 3, 400)
        points = [[x, 0.5 + 0.35 * np.sin(2.5 * x) * np.exp(-x * x / 8), 0] for x in xs]
        curve = VMobject()
        curve.set_points_smoothly(points)
        curve.set_stroke(color="#94e2d5", width=3)
        curve.set_fill(opacity=0)
        curve.move_to(RIGHT * 2.5)

        line_label = MathTex(r"S(\omega)", color="#94e2d5")
        line_label.next_to(curve, UP, buff=0.3)

        # Period arrow center
        arrow = Arrow(
            start=LEFT * 2, end=RIGHT * 2, color="#89b4fa", stroke_width=3, buff=0
        )
        arrow_label = Text("T → ∞", color="#89b4fa", font_size=36)
        arrow_label.next_to(arrow, UP, buff=0.2)

        # Animations – total 6.0s
        self.play(FadeIn(bars, shift=UP), run_time=1.5)
        self.play(FadeIn(arrow), run_time=0.5)
        self.play(FadeIn(arrow_label), run_time=0.5)
        self.wait(0.5)

        self.play(FadeOut(bars, shift=RIGHT), FadeIn(curve, shift=LEFT), run_time=1.5)
        self.play(FadeIn(line_label), run_time=0.5)
        self.wait(1.0)
        # --- Scene 5: Continuous Fourier transform integral ---
        self.camera.background_color = "#181825"

        input_color = "#a6e3a1"
        funnel_color = "#f38ba8"
        output_color = "#89b4fa"
        arrow_color = "#94e2d5"

        # Input waveform
        input_graph = FunctionGraph(
            lambda x: np.sin(x), x_range=[-3, 3], color=input_color, stroke_width=2
        )
        input_label = MathTex(r"x(t)", color=input_color).scale(0.8)
        input_label.next_to(input_graph, UP, buff=0.3)
        input_group = VGroup(input_graph, input_label).shift(LEFT * 3.5)

        # Integrator funnel
        funnel_points = [
            np.array([-1.5, 1.0, 0]),
            np.array([-1.5, -1.0, 0]),
            np.array([0.0, -0.4, 0]),
            np.array([0.0, 0.4, 0]),
        ]
        funnel = Polygon(
            *funnel_points, color=funnel_color, fill_opacity=0.15, stroke_width=2
        )
        integral_label = MathTex(
            r"\int x(t) e^{-i\omega t}\, dt", color=funnel_color
        ).scale(0.7)
        integral_label.move_to(funnel.get_center())
        funnel_group = VGroup(funnel, integral_label)

        # Flow arrows
        arrow1 = Arrow(
            start=input_group.get_right() + RIGHT * 0.5,
            end=funnel.get_left() + LEFT * 0.2,
            color=arrow_color,
            stroke_width=2.5,
        )
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 2, 0.5],
            x_length=4,
            y_length=2.5,
            axis_config={"color": output_color, "stroke_width": 2},
        ).shift(RIGHT * 3.5)

        arrow2 = Arrow(
            start=funnel.get_right() + RIGHT * 0.2,
            end=axes.get_left() + LEFT * 0.3,
            color=arrow_color,
            stroke_width=2.5,
        )
        flow_group = VGroup(arrow1, arrow2)

        # Output spectrum
        spectrum = axes.plot(
            lambda x: np.exp(-(x**2)), color=output_color, stroke_width=2
        )
        output_label = MathTex(r"X(\omega)", color=output_color).scale(0.8)
        output_label.next_to(axes, UP, buff=0.2)
        output_group = VGroup(axes, spectrum, output_label)

        self.play(FadeIn(input_group, shift=UP), run_time=1.5)
        self.play(GrowFromCenter(funnel), FadeIn(integral_label), run_time=1.5)
        self.play(Create(flow_group), run_time=1.5)
        self.play(FadeIn(output_group, shift=DOWN), run_time=2.0)
        self.wait(1.0)
        # --- Scene 6: Magnitude and phase in frequency domain ---
        self.camera.background_color = "#181825"

        # Shared frequency range
        x_range = [0, 10, 1]

        # Magnitude axes (top)
        mag_axes = Axes(
            x_range=x_range,
            y_range=[0, 1.2, 0.3],
            x_length=10,
            y_length=3,
            axis_config={"color": "#89b4fa", "stroke_width": 2},
            tips=False,
        )
        mag_axes.move_to(UP * 2.5)
        mag_label = MathTex(r"|X(\omega)|", color="#89b4fa").next_to(
            mag_axes, UP, buff=0.3
        )
        mag_axes_label = VGroup(mag_axes, mag_label)

        # Magnitude spectrum - mountain range
        def magnitude_func(x):
            return (
                0.8 * np.exp(-(((x - 3) / 0.6) ** 2))
                + 0.5 * np.exp(-(((x - 6.5) / 0.5) ** 2))
                + 0.3 * np.exp(-(((x - 8.5) / 0.4) ** 2))
            )

        magnitude_plot = mag_axes.plot(magnitude_func)
        magnitude_plot.set_color("#a6e3a1")
        magnitude_plot.set_stroke(width=2)

        # Phase axes (bottom)
        phase_axes = Axes(
            x_range=x_range,
            y_range=[-4, 4, 1],
            x_length=10,
            y_length=3,
            axis_config={"color": "#94e2d5", "stroke_width": 2},
            tips=False,
        )
        phase_axes.move_to(DOWN * 2.5)
        phase_label = MathTex(r"\angle X(\omega)", color="#94e2d5").next_to(
            phase_axes, DOWN, buff=0.3
        )
        phase_axes_label = VGroup(phase_axes, phase_label)

        # Phase winding line
        def phase_func(x):
            return np.sin(1.2 * x) + 0.5 * np.sin(3 * x)

        phase_plot = phase_axes.plot(phase_func)
        phase_plot.set_color("#fab387")
        phase_plot.set_stroke(width=2)

        # Animations - total 7.0s
        self.play(FadeIn(mag_axes_label), run_time=0.8)
        self.play(Create(magnitude_plot), run_time=1.2)
        self.play(FadeIn(phase_axes_label), run_time=0.8)
        self.play(Create(phase_plot), run_time=1.2)
        self.wait(3.0)
        # --- Scene 7: Inverse transform reconstructs time signal ---
        self.camera.background_color = "#181825"

        # Spectrum bars on LEFT
        values = [0.3, 1.2, 0.8, 1.5, 0.6, 0.9, 0.4]
        bar_names = [f"{i}" for i in range(len(values))]
        spectrum_bars = BarChart(
            values=values,
            bar_names=bar_names,
            y_range=[0, 2, 0.5],
            x_length=3,
            y_length=3,
        )
        spectrum_bars.set_fill("#fab387", opacity=0.9)
        spectrum_bars.set_stroke(width=2)
        spectrum_bars.shift(LEFT * 3.5 + UP * 0.5)
        spectrum_label = MathTex("X(\\omega)", color="#fab387").scale(0.8)
        spectrum_label.next_to(spectrum_bars, UP, buff=0.3)
        spectrum_group = VGroup(spectrum_bars, spectrum_label)

        # Synthesis mixer at CENTER
        mixer_shape = RegularPolygon(n=6, radius=0.9, color="#f38ba8", fill_opacity=0.8)
        mixer_shape.set_stroke(width=2)
        mixer_label = MathTex("\\sum", color="#f38ba8").scale(1.2)
        mixer_label.move_to(mixer_shape.get_center())
        mixer_group = VGroup(mixer_shape, mixer_label).move_to(ORIGIN)

        # Reconstructed wave on RIGHT
        axes = Axes(
            x_range=[-2 * np.pi, 2 * np.pi, np.pi],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5,
            y_length=3,
            axis_config={"color": "#94e2d5", "stroke_width": 2},
        )
        axes.shift(RIGHT * 3 + UP * 0.5)
        wave_func = lambda x: np.sin(x) + 0.3 * np.sin(3 * x)
        wave_graph = axes.plot(wave_func, color="#a6e3a1")
        wave_graph.set_stroke(width=2)
        wave_label = MathTex("x(t)\\ \	ext{recovered}", color="#a6e3a1").scale(0.7)
        wave_label.next_to(axes, UP, buff=0.2)
        wave_group = VGroup(axes, wave_graph, wave_label)

        # Feedback arrows
        arrow_start = spectrum_bars.get_right() + RIGHT * 0.3
        arrow_mid = mixer_shape.get_left() + LEFT * 0.1
        arrow1 = Arrow(arrow_start, arrow_mid, buff=0, color="#89b4fa", stroke_width=2)
        arrow_label1 = MathTex("\\frac{1}{2\\pi}\\int", color="#89b4fa").scale(0.6)
        arrow_label1.next_to(arrow1, UP, buff=0.1)

        arrow2_start = mixer_shape.get_right() + RIGHT * 0.2
        arrow2_end = wave_group.get_left() + LEFT * 0.3
        arrow2 = Arrow(
            arrow2_start, arrow2_end, buff=0, color="#89b4fa", stroke_width=2
        )

        feedback_group = VGroup(arrow1, arrow_label1, arrow2)

        # Animation sequence – total 7.0 s
        self.play(FadeIn(spectrum_group, shift=UP * 0.3), run_time=1.5)
        self.play(Create(arrow1), Write(arrow_label1), run_time=1.0)
        self.play(GrowFromCenter(mixer_group), run_time=1.0)
        self.play(Create(arrow2), run_time=1.0)
        self.play(FadeIn(wave_group, shift=RIGHT * 0.3), run_time=1.5)
        self.wait(1.0)
