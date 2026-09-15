import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Introduction to Fourier transform ---
        self.camera.background_color = "#181825"

        # Title at the top
        title = Text("Introduction to Fourier Transform", font_size=36, color="#89b4fa")
        title.move_to(UP * 3)

        # Create a visual metaphor: decomposing a complex wave into simple sines
        # Main complex wave
        complex_wave = FunctionGraph(
            lambda x: (
                0.4 * np.sin(2 * x) + 0.25 * np.sin(6 * x) + 0.15 * np.sin(10 * x)
            ),
            x_range=[-3.5, 3.5],
            color="#f38ba8",
        )
        complex_wave.move_to(ORIGIN + UP * 0.5)
        complex_wave.set_stroke(width=3)

        # Individual sine waves (frequency components)
        sine1 = FunctionGraph(
            lambda x: 0.3 * np.sin(2 * x), x_range=[-3, 3], color="#a6e3a1"
        )
        sine1.move_to(ORIGIN + DOWN * 1.2)
        sine1.set_stroke(width=2)

        sine2 = FunctionGraph(
            lambda x: 0.2 * np.sin(6 * x), x_range=[-3, 3], color="#fab387"
        )
        sine2.move_to(ORIGIN + DOWN * 2.0)
        sine2.set_stroke(width=2)

        sine3 = FunctionGraph(
            lambda x: 0.1 * np.sin(10 * x), x_range=[-3, 3], color="#94e2d5"
        )
        sine3.move_to(ORIGIN + DOWN * 2.8)
        sine3.set_stroke(width=2)

        # Labels for the components
        label1 = Text("Frequency 1", font_size=20, color="#a6e3a1")
        label1.next_to(sine1, RIGHT, buff=0.5)

        label2 = Text("Frequency 2", font_size=20, color="#fab387")
        label2.next_to(sine2, RIGHT, buff=0.5)

        label3 = Text("Frequency 3", font_size=20, color="#94e2d5")
        label3.next_to(sine3, RIGHT, buff=0.5)

        # Build intro animation
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # Show the complex wave
        self.play(Create(complex_wave), run_time=2.0)
        self.wait(0.5)

        # Show the decomposition into simple frequencies
        self.play(Create(sine1), Create(sine2), Create(sine3), run_time=1.5)

        self.play(FadeIn(label1), FadeIn(label2), FadeIn(label3), run_time=1.0)

        self.wait(1.0)
        # --- Scene 2: Step 2: Why Fourier transform matters ---
        self.clear()
        self.camera.background_color = "#181825"

        # --- Objects ---
        # Main Axes centered at origin
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=4,
            axis_config={
                "color": "#fab387",
                "include_tip": True,
                "stroke_width": 2.0,
            },
        )

        # Title at top
        title = Text(
            "Why Fourier transform matters",
            font_size=36,
            color="WHITE",
        )
        title.move_to(UP * 3)

        # Time-domain signal (sine wave) representing the raw data
        sine_graph = axes.plot(
            lambda x: 1.2 * np.sin(2 * x),
            color="#89b4fa",
            stroke_width=2.5,
        )

        # Frequency-domain extraction visual
        freq_x = 0.6
        spike_start = axes.c2p(freq_x, 0)
        spike_end = axes.c2p(freq_x, 1.3)

        freq_arrow = Arrow(
            start=spike_start,
            end=spike_end,
            color="#f38ba8",
            stroke_width=2,
            buff=0.05,
        )

        dot = Dot(axes.c2p(freq_x, 1.5), color="#f38ba8")

        freq_label = MathTex(r"\omega", color="#f38ba8").next_to(
            freq_arrow.get_end(), UP, buff=0.15
        )

        dot_label = MathTex(r"\hat{f}(\omega)", color="#f38ba8").next_to(
            dot, UR, buff=0.1
        )

        # --- Animations (Total = 1.5 + 1.0 + 1.3 + 0.6 + 0.6 + 0.5 + 0.5 = 6.0 s) ---

        # 1. Introduce the question
        self.play(Write(title), run_time=1.5)

        # 2. Build the foundation
        self.play(Create(axes), run_time=1.0)

        # 3. Show the complex signal
        self.play(Create(sine_graph), run_time=1.3)

        # 4. Extract the frequency component
        self.play(
            FadeIn(freq_arrow, shift=UP * 0.2),
            FadeIn(dot, scale=2),
            run_time=0.6,
        )

        # 5. Label the discovery
        self.play(
            FadeIn(freq_label, shift=UP * 0.2),
            FadeIn(dot_label, shift=RIGHT * 0.2),
            run_time=0.6,
        )

        # 6. Briefly emphasize the relationship between signal and spectrum
        self.play(
            Indicate(sine_graph, color="#a6e3a1", scale_factor=1.02),
            run_time=0.5,
        )
        self.play(
            Indicate(dot, color="#a6e3a1", scale_factor=1.5),
            run_time=0.5,
        )
        # --- Scene 3: Step 3: Core mechanics of Fourier transform ---
        self.clear()
        self.camera.background_color = "#181825"

        # Title
        title = Text("Core mechanics of Fourier transform", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # Main NumberLine (Frequency domain representation)
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            color="#f38ba8",
            include_numbers=True,
            include_tip=True,
        )
        number_line.move_to(DOWN * 0.5)

        # Supporting labels for pedagogical visual metaphor
        time_label = Text("Time domain", font_size=24, color="#89b4fa")
        time_label.move_to(DOWN * 2.5 + LEFT * 2.5)

        freq_label = Text("Frequency domain", font_size=24, color="#a6e3a1")
        freq_label.move_to(DOWN * 2.5 + RIGHT * 2.5)

        arrow_between = CurvedArrow(
            time_label.get_top(), freq_label.get_top(), angle=PI / 4, color="#fab387"
        )

        # Step-by-step creative animations (total 6.0s)
        self.play(Write(title), run_time=1.5)
        self.play(Create(number_line), run_time=2.0)
        self.play(FadeIn(time_label), FadeIn(freq_label), run_time=1.5)
        self.play(GrowFromCenter(arrow_between), run_time=1.0)
        self.wait(1.0)
        # --- Scene 4: Step 4: Common pitfalls in Fourier transform ---
        self.clear()

        # Background color from style guidelines
        self.camera.background_color = "#181825"

        # Color palette
        blue = "#89b4fa"
        peach = "#fab387"
        pink = "#f38ba8"
        green = "#a6e3a1"
        teal = "#94e2d5"

        # --- TITLE ---
        title = Text(
            "Common pitfalls in Fourier transform", font_size=36, color=WHITE
        ).shift(UP * 3)

        # --- PITFALL 1: Aliasing / Sampling ---
        c1 = Circle(radius=0.6, color=pink, stroke_width=3)
        wave1 = (
            FunctionGraph(
                lambda x: 0.3 * np.sin(5 * x), x_range=[-TAU / 2, TAU / 2], color=pink
            )
            .scale(0.8)
            .move_to(c1.get_center())
        )
        dots1 = VGroup(
            *[
                Dot(point=wave1.point_from_proportion(i / 6), color=pink, radius=0.06)
                for i in range(7)
            ]
        )
        icon1 = VGroup(c1, wave1, dots1)
        lbl1 = Text("Aliasing / Sampling", font_size=24, color=pink)
        card1 = VGroup(icon1, lbl1).arrange(DOWN, buff=0.4)

        # --- PITFALL 2: Spectral Leakage ---
        s2 = Square(side_length=1.2, color=peach, stroke_width=3)
        line2 = Line(
            start=s2.get_left(), end=s2.get_right(), color=peach, stroke_width=4
        )
        spike_l = Triangle(color=peach, fill_opacity=1).scale(0.2).stretch(1.5, 0)
        spike_l.move_to(line2.get_start()).shift(LEFT * 0.1 + UP * 0.15)
        spike_r = Triangle(color=peach, fill_opacity=1).scale(0.2).stretch(1.5, 0)
        spike_r.move_to(line2.get_end()).shift(RIGHT * 0.1 + DOWN * 0.05)
        icon2 = VGroup(s2, line2, spike_l, spike_r)
        lbl2 = Text("Spectral Leakage", font_size=24, color=peach)
        card2 = VGroup(icon2, lbl2).arrange(DOWN, buff=0.4)

        # --- PITFALL 3: Wrong Amplitude ---
        r3 = Rectangle(height=1.0, width=1.5, color=blue, stroke_width=3)
        bar3a = Rectangle(
            height=0.6, width=0.25, fill_opacity=0.8, color=blue, stroke_width=0
        )
        bar3a.move_to(r3.get_center()).shift(LEFT * 0.4)
        bar3b = Rectangle(
            height=0.3, width=0.25, fill_opacity=0.8, color=blue, stroke_width=0
        )
        bar3b.move_to(r3.get_center()).shift(RIGHT * 0.4)
        x3 = (
            VGroup(
                Line(
                    start=LEFT * 0.15 + UP * 0.15,
                    end=RIGHT * 0.15 + DOWN * 0.15,
                    color=pink,
                    stroke_width=4,
                ),
                Line(
                    start=LEFT * 0.15 + DOWN * 0.15,
                    end=RIGHT * 0.15 + UP * 0.15,
                    color=pink,
                    stroke_width=4,
                ),
            )
            .move_to(r3.get_top())
            .shift(UP * 0.2)
        )
        icon3 = VGroup(r3, bar3a, bar3b, x3)
        lbl3 = Text("Wrong Amplitude", font_size=24, color=blue)
        card3 = VGroup(icon3, lbl3).arrange(DOWN, buff=0.4)

        # --- MAIN VGROUP (positioned at ORIGIN, colored green) ---
        main_group = VGroup(card1, card2, card3)
        main_group.arrange(RIGHT, buff=1.2)
        main_group.move_to(ORIGIN)
        main_group.set_color(green)

        # === ANIMATIONS: Total runtime = 6.0 seconds ===
        # 1. Title write-in
        self.play(Write(title), run_time=1.0)
        self.wait(0.2)

        # 2. Icons grow from center
        self.play(
            GrowFromCenter(card1[0]),
            GrowFromCenter(card2[0]),
            GrowFromCenter(card3[0]),
            run_time=1.0,
        )

        # 3. Labels fade in with upward drift
        self.play(
            FadeIn(card1[1], shift=UP * 0.3),
            FadeIn(card2[1], shift=UP * 0.3),
            FadeIn(card3[1], shift=UP * 0.3),
            run_time=0.8,
        )
        self.wait(0.2)

        # 4. Sequential emphasis on each pitfall
        self.play(Indicate(card1, color=pink, scale_factor=1.15), run_time=0.6)
        self.play(Indicate(card2, color=peach, scale_factor=1.15), run_time=0.6)
        self.play(Indicate(card3, color=blue, scale_factor=1.15), run_time=0.6)

        # 5. Hold for comprehension
        self.wait(1.0)
        # 1.0 + 0.2 + 1.0 + 0.8 + 0.2 + 0.6 + 0.6 + 0.6 + 1.0 = 6.0 ✓
        # --- Scene 5: Step 5: Practical application of Fourier transform ---
        self.clear()
        # --- Scene 5: Step 5: Practical application of Fourier transform ---
        self.camera.background_color = "#181825"

        # -- 1. Objects --

        title = Text(
            "Practical application of Fourier transform", font_size=36, color=WHITE
        )
        title.to_edge(UP, buff=0.5)

        table_data = [
            ["Field", "Real-World Use"],
            ["Audio", "Noise filtering, EQ"],
            ["Image", "JPEG compression"],
            ["Telecom", "Signal modulation"],
            ["Medical", "MRI reconstruction"],
        ]

        table = Table(
            table_data,
            include_outer_lines=True,
            line_config={"stroke_width": 2, "color": "#94e2d5"},
        )
        table.scale(0.65)
        table.set_color("#94e2d5")
        table.move_to(ORIGIN)

        # Highlight header row
        header_row = table.get_rows()[0]
        header_row.set_color("#fab387")

        # Color individual cells for visual richness
        for i in range(1, len(table.get_rows())):
            row = table.get_rows()[i]
            row[0].set_color("#89b4fa")
            row[1].set_color("#a6e3a1")

        # Supporting label: small caption at bottom
        caption = Text(
            "Fourier transform powers modern signal processing",
            font_size=20,
            color="#94e2d5",
        )
        caption.to_edge(DOWN, buff=0.5)

        # -- 2. Animations (Total target: 6.0s )--

        self.play(Write(title), run_time=1.5)

        self.play(
            LaggedStart(
                GrowFromCenter(table.get_rows()[0]),
                FadeIn(table.get_rows()[1], shift=RIGHT * 0.3),
                FadeIn(table.get_rows()[2], shift=RIGHT * 0.3),
                FadeIn(table.get_rows()[3], shift=RIGHT * 0.3),
                FadeIn(table.get_rows()[4], shift=RIGHT * 0.3),
                lag_ratio=0.25,
            ),
            run_time=2.5,
        )

        self.play(FadeIn(caption, shift=UP * 0.3), run_time=1.0)

        self.wait(1.0)
