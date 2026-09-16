import numpy as np
from manim import *

class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: The Superposition Principle ---
        title1 = Text("1. What is a Signal?", font_size=48, color=YELLOW)
        self.play(Write(title1))
        self.wait(1)
        self.play(title1.animate.to_edge(UP))

        # Create simple sine waves
        ax1 = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=4,
            axis_config={"color": BLUE},
        ).add_coordinates()

        wave1 = ax1.plot(np.sin, color=RED, x_range=[0, 2 * PI])
        wave2 = ax1.plot(lambda x: 0.5 * np.sin(3 * x), color=GREEN, x_range=[0, 2 * PI])

        label1 = MathTex(r"\sin(x)", color=RED).next_to(ax1, UP)
        label2 = MathTex(r"0.5\sin(3x)", color=GREEN).next_to(ax1, DOWN)

        self.play(Create(ax1))
        self.play(Create(wave1), Write(label1))
        self.wait(1)
        self.play(Create(wave2), Write(label2))
        self.wait(1)

        # Superpose them
        combined_label = MathTex(r"\sin(x) + 0.5\sin(3x)", color=PURPLE).next_to(ax1, UP)
        combined_wave = ax1.plot(lambda x: np.sin(x) + 0.5 * np.sin(3 * x), color=PURPLE, x_range=[0, 2 * PI])

        self.play(
            FadeOut(label1), FadeOut(label2),
            ReplacementTransform(VGroup(wave1, wave2), combined_wave),
            ReplacementTransform(title1, combined_label),
        )
        self.wait(2)

        insight1 = Text("Most signals are a sum of simple waves!", font_size=36).to_edge(DOWN)
        self.play(Write(insight1))
        self.wait(2)
        self.clear()

        # --- Scene 2: The Goal of Fourier Transform ---
        title2 = Text("2. The Big Question", font_size=48, color=YELLOW)
        self.play(Write(title2))
        self.play(title2.animate.to_edge(UP))

        q_text = Text("Given a complex wave...\n...what are its simple components?", font_size=36)
        self.play(Write(q_text))
        self.wait(2)

        forward = Text("Simple Waves", font_size=40, color=GREEN)
        arrow_forward = Arrow(LEFT * 3, RIGHT * 3, color=WHITE)
        backward = Text("Complex Wave", font_size=40, color=PURPLE)
        synth_group = VGroup(forward, arrow_forward, backward).arrange(RIGHT, buff=0.5)
        synth_group.move_to(ORIGIN)
        self.play(ReplacementTransform(q_text, synth_group))
        self.wait(1)

        arrow_backward = Arrow(RIGHT * 3, LEFT * 3, color=YELLOW).move_to(arrow_forward)
        ft_label = Text("Fourier Transform", font_size=36, color=YELLOW).next_to(arrow_backward, UP)

        self.play(
            ReplacementTransform(arrow_forward, arrow_backward),
            Write(ft_label),
            Swap(forward, backward)
        )
        self.wait(2)
        self.clear()

        # --- Scene 3: Frequency and Time Domains ---
        title3 = Text("3. Two Ways to Look at a Signal", font_size=40, color=YELLOW)
        self.play(Write(title3))
        self.play(title3.animate.to_edge(UP))

        # Time Domain View
        time_title = Text("Time Domain", font_size=36, color=BLUE)
        ax_time = Axes(x_range=[0, 2 * PI], y_range=[-2, 2], x_length=5, y_length=3).add_coordinates()
        time_wave = ax_time.plot(lambda x: np.sin(x) + 0.5 * np.sin(3 * x), color=PURPLE)
        time_group = VGroup(time_title, ax_time, time_wave).arrange(DOWN, buff=0.2)

        # Frequency Domain View
        freq_title = Text("Frequency Domain", font_size=36, color=RED)
        ax_freq = Axes(x_range=[0, 5, 1], y_range=[0, 1.2, 1], x_length=5, y_length=3).add_coordinates()
        bars = VGroup(
            Rectangle(width=0.4, height=1.0, color=RED).move_to(ax_freq.c2p(1, 0.5)),
            Rectangle(width=0.4, height=0.5, color=GREEN).move_to(ax_freq.c2p(3, 0.25)),
        )
        freq_group = VGroup(freq_title, ax_freq, bars).arrange(DOWN, buff=0.2)

        scene_group = VGroup(time_group, freq_group).arrange(RIGHT, buff=1)
        self.play(FadeIn(scene_group))
        self.wait(1)

        # Highlight components
        self.play(bars[0].animate.set_fill(RED, opacity=1), run_time=0.5)
        wave_alone = ax_time.plot(np.sin, color=RED, x_range=[0, 2 * PI])
        self.play(Create(wave_alone))
        self.play(FadeOut(wave_alone))

        self.play(bars[1].animate.set_fill(GREEN, opacity=1), run_time=0.5)
        wave_alone2 = ax_time.plot(lambda x: 0.5 * np.sin(3 * x), color=GREEN, x_range=[0, 2 * PI])
        self.play(Create(wave_alone2))
        self.play(FadeOut(wave_alone2))
        self.wait(2)
        self.clear()

        # --- Scene 4: The Dot Product Analogy ---
        title4 = Text("4. How do we detect a frequency?", font_size=36, color=YELLOW)
        self.play(Write(title4))
        self.play(title4.animate.to_edge(UP))

        explanation = Text("We use the 'Dot Product' to test similarity.", font_size=30)
        self.play(Write(explanation))
        self.wait(1)

        ax_test = Axes(x_range=[0, 2 * PI], y_range=[-1.5, 1.5], x_length=8, y_length=3)
        signal = ax_test.plot(lambda x: np.sin(x), color=BLUE)
        probe = ax_test.plot(lambda x: np.sin(x), color=YELLOW, stroke_opacity=0.5)

        self.play(Create(ax_test), Create(signal))
        self.play(Create(probe))

        dot_prod = MathTex(r"\int \sin(x) \cdot \sin(x) \, dx = \text{High}", font_size=36).next_to(ax_test, DOWN)
        self.play(Write(dot_prod))
        self.wait(2)

        # Change probe to different frequency
        probe2 = ax_test.plot(lambda x: np.sin(3 * x), color=YELLOW, stroke_opacity=0.5)
        dot_prod2 = MathTex(r"\int \sin(x) \cdot \sin(3x) \, dx \approx 0", font_size=36).next_to(ax_test, DOWN)

        self.play(ReplacementTransform(probe, probe2), ReplacementTransform(dot_prod, dot_prod2))
        self.wait(2)
        self.clear()

        # --- Scene 5: Euler's Formula and the Kernel ---
        title5 = Text("5. The Magic Ingredient: Euler's Formula", font_size=40, color=YELLOW)
        self.play(Write(title5))
        self.play(title5.animate.to_edge(UP))

        euler = MathTex(r"e^{ix} = \cos(x) + i\sin(x)", font_size=60)
        self.play(Write(euler))
        self.wait(2)

        circle = Circle(radius=1.5, color=BLUE)
        dot = Dot(color=YELLOW)
        radius = Line(ORIGIN, RIGHT * 1.5, color=YELLOW)
        angle_tracker = ValueTracker(0)

        def update_radius(m):
            angle = angle_tracker.get_value()
            new_end = 1.5 * np.array([np.cos(angle), np.sin(angle), 0])
            m.become(Line(ORIGIN, new_end, color=YELLOW))

        radius.add_updater(update_radius)
        self.play(Create(circle), Create(dot), Create(radius))

        # Spin the radius
        self.play(angle_tracker.animate.set_value(2 * PI), run_time=3, rate_func=linear)
        self.wait(1)

        # Move to the kernel definition
        kernel_title = Text("The Fourier Kernel", font_size=36, color=GREEN).to_edge(UP)
        kernel_eq = MathTex(r"e^{-i 2\pi f t}", font_size=50).next_to(kernel_title, DOWN)
        self.play(
            FadeOut(circle), FadeOut(dot), FadeOut(radius),
            ReplacementTransform(title5, kernel_title),
            ReplacementTransform(euler, kernel_eq),
        )
        self.wait(2)
        self.clear()

        # --- Scene 6: Building the Transform Formula ---
        title6 = Text("6. The Fourier Transform Equation", font_size=40, color=YELLOW)
        self.play(Write(title6))
        self.play(title6.animate.to_edge(UP))

        # Build it piece by piece
        integral = MathTex(r"\mathcal{F}\{f(t)\} = ", font_size=48)
        self.play(Write(integral))
        self.wait(0.5)

        integral_sym = MathTex(r"\int_{-\infty}^{\infty}", font_size=48)
        self.play(integral.animate.shift(LEFT * 1.5), Write(integral_sym.next_to(integral, RIGHT, buff=0.1)))
        self.wait(0.5)

        func = MathTex(r"f(t)", font_size=48)
        self.play(integral_sym.animate.shift(LEFT * 0.5), Write(func.next_to(integral_sym, RIGHT, buff=0.1)))
        self.wait(0.5)

        kernel = MathTex(r"e^{-i 2\pi f t}", font_size=48)
        self.play(func.animate.shift(LEFT * 0.5), Write(kernel.next_to(func, RIGHT, buff=0.1)))
        self.wait(0.5)

        dt = MathTex(r"dt", font_size=48)
        self.play(kernel.animate.shift(LEFT * 0.2), Write(dt.next_to(kernel, RIGHT, buff=0.1)))
        self.wait(1)

        full_eq = VGroup(integral, integral_sym, func, kernel, dt)
        self.play(full_eq.animate.scale(1.2).set_color(GREEN))
        self.wait(2)

        explanation2 = Text("It calculates how much of each frequency 'f' is in the signal 'f(t)'", font_size=30).to_edge(DOWN)
        self.play(Write(explanation2))
        self.wait(2)
        self.clear()

        # --- Scene 7: Visualizing the Result ---
        title7 = Text("7. Putting it all together", font_size=40, color=YELLOW)
        self.play(Write(title7))
        self.play(title7.animate.to_edge(UP))

        # Complex signal: fundamental + 3rd harmonic + 5th harmonic
        def complex_signal(t):
            return np.sin(t) + 0.7 * np.sin(3 * t) + 0.3 * np.sin(5 * t)

        ax_main = Axes(x_range=[0, 2 * PI], y_range=[-2.5, 2.5], x_length=8, y_length=4).add_coordinates()
        wave_main = ax_main.plot(complex_signal, color=PURPLE)
        signal_label = Text("Time Domain", font_size=30, color=PURPLE).next_to(ax_main, UP)

        self.play(Create(ax_main), Create(wave_main), Write(signal_label))
        self.wait(1)

        # Create the frequency domain result
        ax_spec = Axes(x_range=[0, 6, 1], y_range=[0, 1.2, 1], x_length=6, y_length=3).add_coordinates()
        spec_label = Text("Frequency Domain", font_size=30, color=ORANGE).next_to(ax_spec, UP)

        # Approximate the Fourier Transform result manually for these frequencies
        bar1 = Rectangle(width=0.3, height=1.0, color=RED).move_to(ax_spec.c2p(1, 0.5))
        bar3 = Rectangle(width=0.3, height=0.7, color=GREEN).move_to(ax_spec.c2p(3, 0.35))
        bar5 = Rectangle(width=0.3, height=0.3, color=BLUE).move_to(ax_spec.c2p(5, 0.15))

        result_group = VGroup(spec_label, ax_spec, bar1, bar3, bar5).arrange(DOWN, buff=0.2)
        full_scene = VGroup(
            VGroup(ax_main, wave_main, signal_label),
            result_group
        ).arrange(RIGHT, buff=1)

        self.play(
            VGroup(ax_main, wave_main, signal_label).animate.move_to(LEFT * 3.5),
            FadeIn(result_group.move_to(RIGHT * 3.5))
        )
        self.wait(1)

        # Highlight connections
        self.play(
            bar1.animate.set_fill(RED, opacity=1),
            Indicate(ax_main, color=RED),
        )
        self.wait(0.5)

        self.play(
            bar3.animate.set_fill(GREEN, opacity=1),
            Indicate(ax_main, color=GREEN),
        )
        self.wait(0.5)

        self.play(
            bar5.animate.set_fill(BLUE, opacity=1),
            Indicate(ax_main, color=BLUE),
        )
        self.wait(2)
        self.clear()

        # --- Scene 8: Conclusion ---
        title8 = Text("8. The Fourier Transform", font_size=48, color=YELLOW)
        self.play(Write(title8))
        self.play(title8.animate.to_edge(UP))

        summary_points = [
            "• Decomposes complex signals into simple sine waves",
            "• Each bar in the frequency domain represents a component",
            "• The height shows the strength (amplitude) of that frequency",
            "• Applications: Music, Images, Quantum Mechanics, Data Compression"
        ]

        summary_group = VGroup()
        for i, point in enumerate(summary_points):
            text = Text(point, font_size=28, color=WHITE)
            summary_group.add(text)

        summary_group.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN)

        for point in summary_group:
            self.play(Write(point))
            self.wait(0.5)

        final_eq = MathTex(r"\mathcal{F}\{f(t)\} = \int_{-\infty}^{\infty} f(t) e^{-i 2\pi f t} dt", font_size=50, color=GREEN).to_edge(DOWN)
        self.play(Write(final_eq))
        self.wait(3)
        self.clear()
