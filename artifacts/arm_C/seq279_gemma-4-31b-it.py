from manim import *
import numpy as np


class SceneGen(Scene):
    def construct(self):
        # Global Style Configuration
        self.camera.background_color = "#181825"
        ACCENT_1 = "#89b4fa"  # Blue
        ACCENT_2 = "#fab387"  # Orange/Peach
        ACCENT_3 = "#f38ba8"  # Red/Pink
        ACCENT_4 = "#a6e3a1"  # Green
        ACCENT_5 = "#94e2d5"  # Teal
        TEXT_COLOR = "#C0CAF5"
        GRID_COLOR = "#565F89"

        # ---------------------------------------------------------------------
        # Scene 1: Sine Waves as Pure Tones (16s)
        # ---------------------------------------------------------------------
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_color": GRID_COLOR, "stroke_width": 1},
        )
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": TEXT_COLOR},
        )
        axes_labels = axes.get_axis_labels(x_label="t", y_label="A")

        sine_wave = axes.plot(lambda x: np.sin(2 * np.pi * 0.5 * x), color=ACCENT_1)

        self.play(Create(grid), run_time=2)
        self.play(Create(axes), Write(axes_labels), run_time=2)
        self.play(Create(sine_wave), run_time=4)
        self.wait(8)  # Total: 16s

        self.play(
            FadeOut(grid), FadeOut(axes), FadeOut(axes_labels), FadeOut(sine_wave)
        )

        # ---------------------------------------------------------------------
        # Scene 2: Superposition of Waves (15s)
        # ---------------------------------------------------------------------
        axes2 = Axes(
            x_range=[0, 10, 1], y_range=[-2, 2, 1], axis_config={"color": TEXT_COLOR}
        )

        w1 = axes2.plot(lambda x: 0.6 * np.sin(2 * np.pi * 0.3 * x), color=ACCENT_1)
        w2 = axes2.plot(lambda x: 0.4 * np.sin(2 * np.pi * 1.2 * x), color=ACCENT_2)
        combined = axes2.plot(
            lambda x: (
                0.6 * np.sin(2 * np.pi * 0.3 * x) + 0.4 * np.sin(2 * np.pi * 1.2 * x)
            ),
            color=ACCENT_4,
        )

        self.play(Create(axes2), run_time=2)
        self.play(Create(w1), run_time=3)
        self.play(Create(w2), run_time=3)
        self.wait(1)
        self.play(
            ReplacementTransform(w1, combined),
            ReplacementTransform(w2, combined),
            run_time=4,
        )
        self.wait(2)  # Total: 15s

        self.play(FadeOut(axes2), FadeOut(combined))

        # ---------------------------------------------------------------------
        # Scene 3: The Goal: Decomposition (14s)
        # ---------------------------------------------------------------------
        # Left side: Complex wave
        axes_l = Axes(
            x_range=[0, 4, 1], y_range=[-1, 1, 1], x_length=4, y_length=2
        ).shift(LEFT * 3)
        complex_wave = axes_l.plot(
            lambda x: (
                0.5 * np.sin(2 * np.pi * 0.5 * x) + 0.3 * np.sin(2 * np.pi * 2 * x)
            ),
            color=ACCENT_4,
        )

        # Right side: Freq stack
        axes_r1 = Axes(
            x_range=[0, 4, 1], y_range=[-0.5, 0.5, 0.5], x_length=4, y_length=1
        ).shift(RIGHT * 3 + UP * 1)
        f1 = axes_r1.plot(lambda x: 0.4 * np.sin(2 * np.pi * 0.5 * x), color=ACCENT_1)

        axes_r2 = Axes(
            x_range=[0, 4, 1], y_range=[-0.5, 0.5, 0.5], x_length=4, y_length=1
        ).shift(RIGHT * 3 + DOWN * 1)
        f2 = axes_r2.plot(lambda x: 0.2 * np.sin(2 * np.pi * 2 * x), color=ACCENT_2)

        arrow = Arrow(LEFT * 1, RIGHT * 1, color=ACCENT_2).shift(ORIGIN)

        self.play(Create(axes_l), Create(complex_wave), run_time=3)
        self.play(GrowFromCenter(arrow), run_time=2)
        self.play(Create(axes_r1), Create(f1), Create(axes_r2), Create(f2), run_time=4)
        self.wait(5)  # Total: 14s

        self.play(
            FadeOut(axes_l),
            FadeOut(complex_wave),
            FadeOut(arrow),
            FadeOut(axes_r1),
            FadeOut(f1),
            FadeOut(axes_r2),
            FadeOut(f2),
        )

        # ---------------------------------------------------------------------
        # Scene 4: The Wrapping Metaphor (18s)
        # ---------------------------------------------------------------------
        circle_path = Circle(radius=2, color=TEXT_COLOR)

        # The signal wrapped around a circle
        # We simulate the "winding" by creating a parametric function
        # x = cos(theta) * radius + offset
        def wrapped_func(t):
            freq = 0.5
            # Magnitude varies based on the sine wave value
            r = 2 + 0.5 * np.sin(2 * np.pi * freq * t)
            return np.array([r * np.cos(2 * np.pi * t), r * np.sin(2 * np.pi * t), 0])

        wrapped_signal = ParametricFunction(
            wrapped_func, t_range=[0, 5], color=ACCENT_1
        )
        cm_dot = Dot(color=ACCENT_3)

        # To animate the center of mass, we use a ValueTracker for the winding frequency
        # But for a static-duration scene, we'll simplify the visual metaphor
        self.play(Create(circle_path), run_time=2)
        self.play(Create(wrapped_signal), run_time=6)

        # Shift CM dot to represent "Off-center"
        self.play(FadeIn(cm_dot), cm_dot.animate.move_to([0.5, 0.3, 0]), run_time=4)
        self.wait(6)  # Total: 18s

        self.play(FadeOut(circle_path), FadeOut(wrapped_signal), FadeOut(cm_dot))

        # ---------------------------------------------------------------------
        # Scene 5: The Correlation Peak (16s)
        # ---------------------------------------------------------------------
        axes_peak = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 2, 1],
            axis_config={"color": TEXT_COLOR},
            x_axis_config={"include_tip": True},
        )
        labels_peak = axes_peak.get_axis_labels(x_label="Frequency", y_label="Strength")

        # A peak function: a sharp Gaussian-like spike
        def peak_fn(x):
            return 1.8 * np.exp(-((x - 2.5) ** 2) / 0.1)

        peak_line = axes_peak.plot(peak_fn, color=ACCENT_4)

        # Scanning line (vertical)
        scan_line = Line(axes_peak.c2p(0, 0), axes_peak.c2p(0, 2), color=ACCENT_2)

        self.play(Create(axes_peak), Write(labels_peak), run_time=3)
        self.play(Create(scan_line), run_time=1)

        # Animate scan line and peak appearing together
        self.play(
            scan_line.animate.shift(RIGHT * 2.5 * 1.5),  # Approx to 2.5 on x axis
            Create(peak_line),
            run_time=6,
        )
        self.wait(6)  # Total: 16s

        self.play(
            FadeOut(axes_peak),
            FadeOut(labels_peak),
            FadeOut(peak_line),
            FadeOut(scan_line),
        )

        # ---------------------------------------------------------------------
        # Scene 6: Time vs Frequency (17s)
        # ---------------------------------------------------------------------
        # Left: Time Domain
        ax_t = Axes(
            x_range=[0, 4, 1], y_range=[-1, 1, 1], x_length=3, y_length=2
        ).shift(LEFT * 3)
        wave_t = ax_t.plot(
            lambda x: np.sin(2 * np.pi * 0.5 * x) + 0.5 * np.sin(2 * np.pi * 2 * x),
            color=ACCENT_1,
        )
        label_t = Text("Time Domain", font="Sans", color=TEXT_COLOR).next_to(ax_t, UP)

        # Right: Frequency Domain (Bar Chart)
        # Using a VGroup of rectangles to simulate a BarChart for better color control
        bars = VGroup()
        bar_colors = [ACCENT_1, ACCENT_2, ACCENT_1]
        for i in range(3):
            b = Rectangle(
                width=0.4,
                height=1.0 + np.random.random(),
                color=bar_colors[i],
                fill_opacity=0.8,
            )
            bars.add(b)
        bars.arrange(RIGHT, buff=0.2).shift(RIGHT * 3)
        label_f = Text("Frequency Domain", font="Sans", color=TEXT_COLOR).next_to(
            bars, UP
        )

        dual_arrow = DoubleArrow(LEFT * 1, RIGHT * 1, color=ACCENT_2).shift(ORIGIN)
        dual_text = Text("FT / IFT", font="Sans", font_size=24, color=ACCENT_2).next_to(
            dual_arrow, UP
        )

        self.play(Create(ax_t), Create(wave_t), Write(label_t), run_time=4)
        self.play(Create(bars), Write(label_f), run_time=4)
        self.play(Create(dual_arrow), Write(dual_text), run_time=3)
        self.play(Indicate(dual_arrow), run_time=2)
        self.wait(4)  # Total: 17s

        # Keep bars and labels for next scene
        self.play(
            FadeOut(ax_t),
            FadeOut(wave_t),
            FadeOut(label_t),
            FadeOut(dual_arrow),
            FadeOut(dual_text),
        )

        # ---------------------------------------------------------------------
        # Scene 7: Practical Application (16s)
        # ---------------------------------------------------------------------
        # The 'noise' bar is the third one
        noise_bar = bars[2]
        self.play(noise_bar.animate.set_color(ACCENT_3), run_time=2)
        self.play(FadeOut(noise_bar), run_time=2)

        # Transition back to smooth wave
        ax_final = Axes(
            x_range=[0, 4, 1], y_range=[-1, 1, 1], x_length=6, y_length=2
        ).shift(DOWN * 2)
        clean_wave = ax_final.plot(
            lambda x: np.sin(2 * np.pi * 0.5 * x), color=ACCENT_1
        )

        self.play(Create(ax_final), Create(clean_wave), run_time=4)
        self.wait(8)  # Total: 16s

        self.play(
            FadeOut(bars), FadeOut(label_f), FadeOut(ax_final), FadeOut(clean_wave)
        )
