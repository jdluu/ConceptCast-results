import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Time Domain Representation ---
        self.clear()
        # Set background color to match style guidelines
        self.camera.background_color = "#181825"

        # 1. Objects
        title_1 = Text("Time Domain Representation", font_size=36, color=WHITE).move_to(
            UP * 3
        )
        main_1 = Text(
            "We begin with a signal in the time domain. This is a wave oscillating over time.",
            font_size=48,
            color="#89b4fa",
        ).move_to(ORIGIN)

        # 2. Animations
        self.play(Write(title_1), run_time=1.5)
        self.play(Write(main_1), run_time=2.5)

        # 3. Wait to match total duration of 5.0 seconds
        self.wait(1.0)
        # --- Scene 2: Step 2: Frequency Domain Concept ---
        # Set background color
        self.camera.background_color = "#181825"

        # 1. Create Objects
        # Title
        title_2 = Text("Frequency Domain Concept", font_size=36, color=WHITE).move_to(
            UP * 3
        )

        # Axes
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-2, 2],
            x_length=10,
            y_length=6,
            axis_config={"color": "#fab387", "stroke_width": 2},
            tips=False,
        ).move_to(ORIGIN)

        # Axis Labels
        x_label = axes.get_x_axis_label(
            "Frequency", edge=DOWN, direction=DOWN, buff=0.3
        )
        y_label = axes.get_y_axis_label(
            "Amplitude", edge=LEFT, direction=LEFT, buff=0.3
        )
        x_label.set_color(WHITE)
        y_label.set_color(WHITE)

        # Frequency Peaks Visualization (Conceptual)
        # Two peaks at -1 and 1
        peak1 = axes.plot(
            lambda x: 1.5 * np.exp(-((x + 1) ** 2) * 10),
            x_range=[-2, 0],
            color="#a6e3a1",
            stroke_width=4,
        )
        peak2 = axes.plot(
            lambda x: 1.5 * np.exp(-((x - 1) ** 2) * 10),
            x_range=[0, 2],
            color="#a6e3a1",
            stroke_width=4,
        )
        peaks = VGroup(peak1, peak2)

        # Peak Labels
        label1 = MathTex("f_1", color="#94e2d5", font_size=28).next_to(
            axes.c2p(-1, 1.5), UP
        )
        label2 = MathTex("f_2", color="#94e2d5", font_size=28).next_to(
            axes.c2p(1, 1.5), UP
        )

        # 2. Animations
        # Title Fade In
        self.play(FadeIn(title_2, shift=UP * 0.5), run_time=1.0)

        # Axes Creation
        self.play(Create(axes), run_time=1.5)
        self.play(FadeIn(x_label), FadeIn(y_label), run_time=0.5)

        # Peaks Grow/Write
        self.play(Create(peaks, lag_ratio=0.5), run_time=1.5)
        self.play(
            FadeIn(label1, shift=UP * 0.2), FadeIn(label2, shift=UP * 0.2), run_time=0.5
        )

        # 3. Wait to match duration (Total animation time = 5.0s)
        self.wait(0.5)
        # --- Scene 3: Step 3: Decomposition into Sinusoids ---
        self.clear()
        # 1. Create the title
        title = Text("Decomposition into Sinusoids", font_size=36)
        title.to_edge(UP, buff=1.0)

        # 2. Create the NumberLine
        number_line = NumberLine(
            x_range=[-5, 5, 1], length=10, color="#f38ba8", include_numbers=True
        )
        number_line.to_edge(DOWN, buff=1.0)

        # 3. Create frequency labels
        freq_labels = VGroup()
        frequencies = [1, 2, 3]
        colors = ["#89b4fa", "#fab387", "#a6e3a1"]

        for i, freq in enumerate(frequencies):
            label = MathTex(f"f_{freq}", font_size=24, color=colors[i])
            label.next_to(number_line.n2p(freq), UP, buff=0.3)
            freq_labels.add(label)

        # 4. Create sinusoid curves
        sinusoids = VGroup()
        for i, freq in enumerate(frequencies):
            # Create a sine wave using parametric function
            curve = ParametricFunction(
                lambda t: number_line.n2p(t) + UP * 0.5 * np.sin(freq * 2 * PI * t),
                t_range=[-5, 5],
                color=colors[i],
                stroke_width=2,
            )
            sinusoids.add(curve)

        # 5. Create combined wave
        combined_curve = ParametricFunction(
            lambda t: (
                number_line.n2p(t)
                + UP
                * 0.3
                * (
                    np.sin(2 * PI * t)
                    + 0.5 * np.sin(4 * PI * t)
                    + 0.3 * np.sin(6 * PI * t)
                )
            ),
            t_range=[-5, 5],
            color="#f38ba8",
            stroke_width=3,
        )

        # Animation sequence
        self.play(Write(title), run_time=1.0)
        self.play(Create(number_line), run_time=1.5)
        self.play(
            LaggedStart(*[FadeIn(label) for label in freq_labels], lag_ratio=0.3),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[Create(curve) for curve in sinusoids], lag_ratio=0.3),
            run_time=1.5,
        )
        self.play(Create(combined_curve), run_time=1.0)
        self.wait(0.5)  # Total: 6.5 seconds
        # --- Scene 4: Step 4: The Fourier Integral ---
        self.clear()
        self.camera.background_color = "#181825"

        # 1. Objects
        title = Text("The Fourier Integral", font_size=36, color=WHITE).move_to(UP * 3)

        # Main VGroup representing the integral components
        integral_sign = MathTex(r"\int", font_size=72, color="#a6e3a1")
        limits = MathTex(r"_{-\infty}^{\infty}", font_size=48, color="#a6e3a1").next_to(
            integral_sign, RIGHT, buff=0.1
        )
        integrand = MathTex(
            r"f(t) e^{-i \omega t}", font_size=48, color="#89b4fa"
        ).next_to(limits, RIGHT, buff=0.1)
        dt = MathTex(r"\, dt", font_size=48, color="#a6e3a1").next_to(
            integrand, RIGHT, buff=0.1
        )

        main_group = (
            VGroup(integral_sign, limits, integrand, dt)
            .arrange(RIGHT, buff=0.1)
            .move_to(ORIGIN)
        )

        # Supporting labels
        label_correlation = Text(
            "Correlation with complex exponential", font_size=24, color="#fab387"
        ).next_to(main_group, DOWN, buff=0.5)
        label_freq = MathTex(
            r"\omega 	ext{ (Frequency)}", font_size=28, color="#94e2d5"
        ).next_to(label_correlation, DOWN, buff=0.3)

        # 2. Animations
        # Total duration: 6.0 seconds
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(main_group, shift=UP * 0.5), run_time=2.0)
        self.play(Write(label_correlation), run_time=1.0)
        self.play(FadeIn(label_freq, shift=UP * 0.2), run_time=1.0)

        # 3. Wait to match duration (1.0 + 2.0 + 1.0 + 1.0 = 5.0) + 1.0 wait = 6.0
        self.wait(1.0)
        # --- Scene 5: Step 5: Magnitude and Phase Spectrum ---
        self.clear()
        # Set background color to match theme
        self.camera.background_color = "#181825"

        # 1. Create Title
        title = Text("Magnitude and Phase Spectrum", font_size=36, color=WHITE).move_to(
            UP * 3
        )

        # 2. Create Table Data
        # Represents the Frequency, Magnitude, and Phase relationship
        table_data = [
            ["Frequency", "Magnitude", "Phase"],
            ["$f_1$", "$|X(f_1)|$", "$\\angle X(f_1)$"],
            ["$f_2$", "$|X(f_2)|$", "$\\angle X(f_2)$"],
            ["$f_3$", "$|X(f_3)|$", "$\\angle X(f_3)$"],
        ]

        # 3. Create Table Object
        # Styled with the specified teal color (#94e2d5)
        table = (
            Table(
                table_data,
                include_outer_lines=True,
                line_config={"stroke_color": "#94e2d5", "stroke_width": 2.0},
                element_to_mobject_config={"color": "#94e2d5"},
            )
            .scale(0.8)
            .move_to(ORIGIN)
        )

        # 4. Animations (Total Duration: 6.0s)
        # Write Title: 1.0s
        self.play(Write(title), run_time=1.0)
        # Draw Table: 2.0s
        self.play(Create(table), run_time=2.0)

        # Highlight each frequency component sequentially: 3.0s total
        rows = table.get_rows()
        # Row 0 is header, Rows 1, 2, 3 are data
        self.play(Indicate(rows[1], color="#fab387", scale_factor=1.1), run_time=1.0)
        self.play(Indicate(rows[2], color="#fab387", scale_factor=1.1), run_time=1.0)
        self.play(Indicate(rows[3], color="#fab387", scale_factor=1.1), run_time=1.0)

        # Final wait to ensure exact duration compliance (1+2+1+1+1 = 6.0)
        self.wait(0.01)
        # --- Scene 6: Step 6: Inverse Transform ---
        self.camera.background_color = "#181825"

        # Create title
        title = Text("Inverse Transform", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # Create main arrow pointing right (reconstruction direction)
        main_arrow = Arrow(
            start=LEFT * 3, end=RIGHT * 3, color="#cdd6f4", stroke_width=4
        )

        # Add label on arrow
        arrow_label = MathTex(r"\mathcal{F}^{-1}", font_size=48, color="#cdd6f4")
        arrow_label.next_to(main_arrow, UP, buff=0.3)

        # Domain labels
        freq_label = Text("Frequency Domain", font_size=24, color="#89b4fa")
        freq_label.next_to(main_arrow.get_start(), DOWN, buff=0.5)

        time_label = Text("Time Domain", font_size=24, color="#a6e3a1")
        time_label.next_to(main_arrow.get_end(), DOWN, buff=0.5)

        # Frequency components (dots on left)
        freq_dots = VGroup(
            *[
                Dot(point=LEFT * 3 + UP * (i - 1) * 0.5, radius=0.08, color="#fab387")
                for i in range(5)
            ]
        )

        # Reconstructed wave (on right)
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=4,
            y_length=3,
            axis_config={"color": "#6c7086", "stroke_width": 1},
        ).move_to(RIGHT * 3 + DOWN * 0.5)

        wave = axes.plot(
            lambda x: np.sin(2 * x) + 0.5 * np.sin(4 * x) + 0.3 * np.sin(6 * x),
            x_range=[0, 4],
            color="#f38ba8",
            stroke_width=3,
        )

        # Animation sequence (total 5.0 seconds)
        self.play(Write(title), run_time=1.0)
        self.play(GrowFromCenter(main_arrow), run_time=1.0)
        self.play(Write(arrow_label), run_time=0.5)
        self.play(FadeIn(freq_label), FadeIn(time_label), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(dot, scale=0.5) for dot in freq_dots], lag_ratio=0.1),
            run_time=1.0,
        )
        self.play(Create(axes), Create(wave), run_time=1.0)
        self.wait(0.01)  # Minimal wait to satisfy Manim's positive duration requirement
