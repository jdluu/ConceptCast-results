#!/usr/bin/env python3
"""
Fourier Transform Educational Animation
Manim CE v0.20.1
Teaches: decomposing a signal into constituent frequencies
"""

from manim import *

class SceneGen(Scene):
    def construct(self):
        # ------------------------------------------------------------
        # Scene 1: The concept of periodic signals (sine waves)
        # ------------------------------------------------------------
        title = Title("1. What is a periodic signal?")
        self.play(Write(title))
        
        # Draw a simple sine wave
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": BLUE},
        )
        labels = axes.get_axis_labels(x_label="t", y_label="f(t)")
        sine_graph = axes.plot(
            lambda x: np.sin(x), 
            x_range=[-5, 5],
            color=YELLOW
        )
        sine_label = MathTex(r"f(t) = \sin(t)", color=YELLOW).next_to(axes, DOWN)
        
        self.play(Create(axes), Write(labels))
        self.play(Create(sine_graph), Write(sine_label))
        self.wait(2)
        
        # Animate the wave moving
        moving_sine = always_redraw(lambda: axes.plot(
            lambda x: np.sin(x + self.time * 2),
            x_range=[-5, 5],
            color=YELLOW
        ))
        self.add(moving_sine)
        self.wait(2)
        self.remove(moving_sine)
        
        self.clear()

        # ------------------------------------------------------------
        # Scene 2: Multiple frequencies – superposition
        # ------------------------------------------------------------
        title2 = Title("2. Complex signals = sum of simple sine waves")
        self.play(Write(title2))
        
        axes2 = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": BLUE},
        )
        labels2 = axes2.get_axis_labels(x_label="t", y_label="f(t)")
        self.play(Create(axes2), Write(labels2))
        
        # Two sine components
        sine1 = axes2.plot(lambda x: np.sin(x), x_range=[-5, 5], color=RED, stroke_opacity=0.6)
        sine2 = axes2.plot(lambda x: 0.5 * np.sin(3*x), x_range=[-5, 5], color=GREEN, stroke_opacity=0.6)
        sum_sine = axes2.plot(lambda x: np.sin(x) + 0.5 * np.sin(3*x), x_range=[-5, 5], color=YELLOW)
        
        label1 = MathTex(r"\sin(t)", color=RED).next_to(axes2, LEFT).shift(UP)
        label2 = MathTex(r"0.5\sin(3t)", color=GREEN).next_to(axes2, LEFT).shift(DOWN)
        label_sum = MathTex(r"\text{sum}", color=YELLOW).next_to(axes2, RIGHT)
        
        self.play(Create(sine1), Write(label1))
        self.wait(0.5)
        self.play(Create(sine2), Write(label2))
        self.wait(0.5)
        self.play(Create(sum_sine), Write(label_sum))
        self.wait(2)
        
        self.clear()

        # ------------------------------------------------------------
        # Scene 3: Time domain vs frequency domain
        # ------------------------------------------------------------
        title3 = Title("3. Two ways to see the same signal")
        self.play(Write(title3))
        
        # Time domain plot (left)
        axes_time = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": BLUE},
        ).shift(LEFT * 3)
        time_label = Text("Time domain", font_size=24).next_to(axes_time, DOWN)
        time_graph = axes_time.plot(
            lambda x: np.sin(x) + 0.5 * np.sin(3*x) + 0.3 * np.sin(5*x),
            x_range=[-5, 5],
            color=YELLOW
        )
        self.play(Create(axes_time), Write(time_label))
        self.play(Create(time_graph))
        
        # Frequency domain (right) – simplified spectrum
        axes_freq = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 1.5, 0.5],
            axis_config={"color": BLUE},
        ).shift(RIGHT * 3)
        freq_label = Text("Frequency domain", font_size=24).next_to(axes_freq, DOWN)
        axes_freq.get_x_axis().label = MathTex(r"\omega")
        axes_freq.get_y_axis().label = MathTex(r"|\hat{f}|")
        
        # Spectrum bars (amplitudes at frequencies 1, 3, 5)
        bars = VGroup()
        for freq, amp in [(1, 1.0), (3, 0.5), (5, 0.3)]:
            x_pos = freq
            bar = Rectangle(
                width=0.4,
                height=amp,
                color=RED,
                fill_opacity=0.8
            ).move_to(axes_freq.c2p(x_pos, amp/2), aligned_edge=DOWN)
            bars.add(bar)
        
        self.play(Create(axes_freq), Write(freq_label))
        self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.3))
        self.wait(2)
        
        self.clear()

        # ------------------------------------------------------------
        # Scene 4: The Fourier Transform formula – intuition
        # ------------------------------------------------------------
        title4 = Title("4. The Fourier Transform formula")
        self.play(Write(title4))
        
        formula = MathTex(
            r"\hat{f}(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt",
            font_size=48
        )
        self.play(Write(formula))
        self.wait(1)
        
        # Explain components
        explanation = VGroup(
            Text(r"$f(t)$: original signal (time)", font_size=28),
            Text(r"$e^{-i\omega t}$: complex sinusoid (frequency probe)", font_size=28),
            Text(r"$\hat{f}(\omega)$: spectrum (frequency content)", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(formula, DOWN, buff=1)
        
        for line in explanation:
            self.play(Write(line), run_time=1)
            self.wait(0.5)
        
        self.wait(2)
        self.clear()

        # ------------------------------------------------------------
        # Scene 5: Probing frequencies – inner product intuition
        # ------------------------------------------------------------
        title5 = Title("5. How it works: correlation with sinusoids")
        self.play(Write(title5))
        
        # Simplified: dot product visualization
        axes_demo = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": BLUE},
        ).scale(0.8)
        labels_demo = axes_demo.get_axis_labels(x_label="t", y_label="f(t)")
        self.play(Create(axes_demo), Write(labels_demo))
        
        # Signal: combination of two frequencies
        signal = axes_demo.plot(
            lambda x: np.sin(x) + 0.7 * np.sin(2.5*x),
            x_range=[0, 10],
            color=YELLOW
        )
        self.play(Create(signal))
        self.wait(1)
        
        # Probe at frequency 1 (matches one component)
        probe = axes_demo.plot(
            lambda x: np.sin(x),
            x_range=[0, 10],
            color=RED,
            stroke_opacity=0.5
        )
        probe_label = MathTex(r"\sin(t)", color=RED).next_to(axes_demo, UP)
        self.play(Create(probe), Write(probe_label))
        self.wait(1)
        
        # Show multiplication
        product = axes_demo.plot(
            lambda x: (np.sin(x) + 0.7 * np.sin(2.5*x)) * np.sin(x),
            x_range=[0, 10],
            color=GREEN
        )
        product_label = MathTex(r"f(t) \cdot \sin(t)", color=GREEN).next_to(axes_demo, DOWN)
        self.play(Create(product), Write(product_label))
        self.wait(2)
        
        self.clear()

        # ------------------------------------------------------------
        # Scene 6: Complex exponentials – Euler's formula
        # ------------------------------------------------------------
        title6 = Title("6. Why complex numbers? Euler's formula")
        self.play(Write(title6))
        
        euler = MathTex(r"e^{i\theta} = \cos\theta + i\sin\theta", font_size=48)
        self.play(Write(euler))
        self.wait(1)
        
        # Show rotation on complex plane
        plane = ComplexPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": BLUE},
        ).scale(0.7).shift(DOWN)
        plane.add_coordinates()
        
        dot = Dot(plane.n2p(1+0j), color=RED)
        circle = Circle(radius=1, color=WHITE, stroke_opacity=0.3)
        angle_tracker = ValueTracker(0)
        
        rotating_dot = always_redraw(lambda: dot.move_to(
            plane.n2p(np.cos(angle_tracker.get_value()) + 1j*np.sin(angle_tracker.get_value()))
        ))
        angle_line = always_redraw(lambda: Line(
            plane.n2p(0+0j),
            plane.n2p(np.cos(angle_tracker.get_value()) + 1j*np.sin(angle_tracker.get_value())),
            color=YELLOW, stroke_opacity=0.6
        ))
        
        self.play(Create(plane), Create(circle))
        self.add(rotating_dot, angle_line)
        self.play(angle_tracker.animate.set_value(2*PI), run_time=3, rate_func=linear)
        self.wait(1)
        
        self.clear()

        # ------------------------------------------------------------
        # Scene 7: Putting it together – full transform animation
        # ------------------------------------------------------------
        title7 = Title("7. The Fourier Transform in action")
        self.play(Write(title7))
        
        # Combine time-domain signal and spectrum side by side
        axes_t = Axes(
            x_range=[-5, 5, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": BLUE},
        ).scale(0.6).shift(LEFT * 3.5 + UP * 0.5)
        axes_t_label = Text("Time", font_size=24).next_to(axes_t, DOWN)
        
        # Create a signal that changes
        signal_t = always_redraw(lambda: axes_t.plot(
            lambda x: np.sin(x + self.time*2) + 0.5*np.sin(3*x + self.time),
            x_range=[-5, 5],
            color=YELLOW
        ))
        
        axes_f = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 1.5, 0.5],
            axis_config={"color": BLUE},
        ).scale(0.6).shift(RIGHT * 3.5 + UP * 0.5)
        axes_f_label = Text("Spectrum", font_size=24).next_to(axes_f, DOWN)
        
        # Spectrum bars (fixed for this example)
        bars_f = VGroup()
        for freq, amp in [(1, 1.0), (3, 0.5)]:
            bar = Rectangle(
                width=0.4,
                height=amp,
                color=RED,
                fill_opacity=0.8
            ).move_to(axes_f.c2p(freq, amp/2), aligned_edge=DOWN)
            bars_f.add(bar)
        
        self.play(
            Create(axes_t), Write(axes_t_label),
            Create(axes_f), Write(axes_f_label)
        )
        self.add(signal_t)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_f]))
        self.wait(3)
        
        self.clear()

        # ------------------------------------------------------------
        # Scene 8: Discrete Fourier Transform (DFT) – real-world connection
        # ------------------------------------------------------------
        title8 = Title("8. DFT: computers work with samples")
        self.play(Write(title8))
        
        # Sampled signal
        axes_s = Axes(
            x_range=[0, 8, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": BLUE},
        ).scale(0.7)
        labels_s = axes_s.get_axis_labels(x_label="sample", y_label="amplitude")
        
        # Create discrete samples
        samples = VGroup()
        for n in range(9):
            x_val = n
            y_val = np.sin(x_val * 0.8) + 0.5 * np.sin(x_val * 2.5)
            dot = Dot(axes_s.c2p(x_val, y_val), color=YELLOW, radius=0.08)
            line = Line(
                axes_s.c2p(x_val, 0),
                axes_s.c2p(x_val, y_val),
                color=RED, stroke_opacity=0.5
            )
            samples.add(dot, line)
        
        self.play(Create(axes_s), Write(labels_s))
        self.play(LaggedStart(*[GrowFromCenter(d) if isinstance(d, Dot) else Create(d) for d in samples], lag_ratio=0.1))
        self.wait(2)
        
        # Show DFT formula
        dft_formula = MathTex(
            r"X_k = \sum_{n=0}^{N-1} x_n e^{-2\pi i k n / N}",
            font_size=36
        ).next_to(axes_s, DOWN)
        self.play(Write(dft_formula))
        self.wait(2)
        
        self.clear()

        # ------------------------------------------------------------
        # Scene 9: Applications – where Fourier is used
        # ------------------------------------------------------------
        title9 = Title("9. Where is Fourier used?")
        self.play(Write(title9))
        
        applications = VGroup(
            Text("🎵 Audio compression (MP3, AAC)", font_size=28),
            Text("📷 Image processing (JPEG)", font_size=28),
            Text("📡 Wireless communications (OFDM)", font_size=28),
            Text("🔬 Medical imaging (MRI)", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).center()
        
        for app in applications:
            self.play(FadeIn(app, shift=UP), run_time=1)
            self.wait(0.5)
        
        self.wait(2)
        self.clear()

        # ------------------------------------------------------------
        # Scene 10: Summary – the big idea
        # ------------------------------------------------------------
        title10 = Title("10. Summary: the essence of Fourier")
        self.play(Write(title10))
        
        summary = VGroup(
            Text("Any signal = sum of sine waves", font_size=32, color=YELLOW),
            Text("Transform extracts the frequencies", font_size=32, color=RED),
            Text("Bridge between time and frequency domains", font_size=32, color=GREEN),
            Text("Fundamental tool in science & engineering", font_size=32, color=BLUE),
        ).arrange(DOWN, buff=0.8).center()
        
        for item in summary:
            self.play(Write(item), run_time=1.5)
            self.wait(0.5)
        
        self.wait(2)
        
        # Final fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.5)
