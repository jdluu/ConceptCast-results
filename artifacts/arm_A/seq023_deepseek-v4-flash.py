from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Sine Wave Introduction - What is a signal?
        title = Text("What is a Signal?", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))
        
        # Create a simple sine wave
        axes1 = Axes(x_range=[0, 2*PI], y_range=[-1.5, 1.5], x_length=6, y_length=3)
        axes_labels1 = axes1.get_axis_labels(x_label="t (time)", y_label="amplitude")
        self.play(Create(axes1), Write(axes_labels1))
        
        sine_wave = axes1.plot(lambda x: np.sin(x), color=YELLOW)
        sine_label = MathTex(r"x(t) = \sin(2\pi f t)", font_size=36, color=YELLOW)
        sine_label.next_to(axes1, DOWN)
        self.play(Create(sine_wave), Write(sine_label))
        self.wait(0.5)
        
        # Animate the wave growing
        growing_sine = always_redraw(lambda: axes1.plot(
            lambda x: np.sin(x + self.time * 2), color=YELLOW
        ))
        self.add(growing_sine)
        self.wait(1)
        self.remove(growing_sine)
        
        # Cleanup
        self.play(FadeOut(title), FadeOut(axes1), FadeOut(axes_labels1), 
                  FadeOut(sine_wave), FadeOut(sine_label))
        self.clear()
        
        # Scene 2: Introducing Frequency - High vs Low
        title2 = Text("What is Frequency?", font_size=48, color=GREEN)
        self.play(Write(title2))
        self.wait(0.5)
        self.play(title2.animate.to_edge(UP))
        
        axes2 = Axes(x_range=[0, 2*PI], y_range=[-1.5, 1.5], x_length=6, y_length=3)
        axes2.shift(LEFT * 3)
        self.play(Create(axes2))
        
        # Low frequency wave
        low_freq = axes2.plot(lambda x: np.sin(0.5*x), color=BLUE)
        low_label = MathTex(r"f_1 = 0.5 \text{ Hz}", font_size=32, color=BLUE)
        low_label.next_to(axes2, DOWN)
        self.play(Create(low_freq), Write(low_label))
        self.wait(0.5)
        
        # High frequency wave on same axes
        high_freq = axes2.plot(lambda x: np.sin(3*x), color=RED)
        high_label = MathTex(r"f_2 = 3 \text{ Hz}", font_size=32, color=RED)
        high_label.next_to(low_label, DOWN)
        self.play(Create(high_freq), Write(high_label))
        self.wait(0.5)
        
        # Show frequency interpretation
        freq_note = Text("Higher frequency = faster oscillation", font_size=28, color=GRAY)
        freq_note.to_edge(DOWN)
        self.play(Write(freq_note))
        self.wait(0.5)
        
        # Cleanup
        self.play(FadeOut(title2), FadeOut(axes2), FadeOut(low_freq), FadeOut(high_freq),
                  FadeOut(low_label), FadeOut(high_label), FadeOut(freq_note))
        self.clear()
        
        # Scene 3: Complex Signal - Adding Frequencies
        title3 = Text("Complex Signals = Sum of Sinusoids", font_size=42, color=ORANGE)
        self.play(Write(title3))
        self.wait(0.5)
        self.play(title3.animate.to_edge(UP))
        
        axes3 = Axes(x_range=[0, 2*PI], y_range=[-2.5, 2.5], x_length=6, y_length=3)
        axes3.shift(LEFT * 3)
        self.play(Create(axes3))
        
        # Build complex signal by adding components
        component1 = axes3.plot(lambda x: 0.5*np.sin(2*x), color=BLUE, stroke_opacity=0.6)
        component2 = axes3.plot(lambda x: 0.3*np.sin(5*x), color=GREEN, stroke_opacity=0.6)
        component3 = axes3.plot(lambda x: 0.2*np.sin(10*x), color=PURPLE, stroke_opacity=0.6)
        
        self.play(Create(component1), Create(component2), Create(component3))
        self.wait(0.5)
        
        # Show the sum
        complex_signal = axes3.plot(lambda x: 0.5*np.sin(2*x) + 0.3*np.sin(5*x) + 0.2*np.sin(10*x), color=RED, stroke_width=4)
        sum_label = MathTex(r"x(t) = \sum A_i \sin(2\pi f_i t)", font_size=36, color=RED)
        sum_label.next_to(axes3, DOWN)
        self.play(Create(complex_signal), Write(sum_label))
        self.wait(1)
        
        # Cleanup
        self.play(FadeOut(title3), FadeOut(axes3), FadeOut(component1), FadeOut(component2),
                  FadeOut(component3), FadeOut(complex_signal), FadeOut(sum_label))
        self.clear()
        
        # Scene 4: The Fourier Transform - Core Idea
        title4 = Text("The Fourier Transform", font_size=48, color=PURPLE)
        self.play(Write(title4))
        self.wait(0.5)
        self.play(title4.animate.to_edge(UP))
        
        # Formula
        ft_formula = MathTex(
            r"X(f) = \int_{-\infty}^{\infty} x(t) e^{-j2\pi ft} dt",
            font_size=44, color=YELLOW
        )
        self.play(Write(ft_formula))
        self.wait(0.5)
        
        # Explanation
        explanation1 = Text("Decomposes signal into frequencies", font_size=28, color=WHITE)
        explanation1.next_to(ft_formula, DOWN * 2)
        explanation2 = Text("Maps time → frequency domain", font_size=28, color=WHITE)
        explanation2.next_to(explanation1, DOWN)
        
        self.play(Write(explanation1), Write(explanation2))
        self.wait(0.5)
        
        # Arrow from time to frequency
        arrow = Arrow(LEFT, RIGHT, color=GREEN)
        arrow.next_to(ft_formula, DOWN)
        time_label = Text("Time Domain", font_size=24, color=BLUE)
        time_label.next_to(arrow, LEFT)
        freq_label = Text("Frequency Domain", font_size=24, color=RED)
        freq_label.next_to(arrow, RIGHT)
        self.play(Create(arrow), Write(time_label), Write(freq_label))
        self.wait(0.5)
        
        # Cleanup
        self.play(FadeOut(title4), FadeOut(ft_formula), FadeOut(explanation1),
                  FadeOut(explanation2), FadeOut(arrow), FadeOut(time_label), FadeOut(freq_label))
        self.clear()
        
        # Scene 5: Inner Product - Measuring Similarity
        title5 = Text("Inner Product: Measuring Similarity", font_size=42, color=TEAL)
        self.play(Write(title5))
        self.wait(0.5)
        self.play(title5.animate.to_edge(UP))
        
        # Two waves to compare
        axes5 = Axes(x_range=[0, 2*PI], y_range=[-1.5, 1.5], x_length=6, y_length=2.5)
        axes5.shift(UP)
        self.play(Create(axes5))
        
        wave_a = axes5.plot(lambda x: np.sin(x), color=BLUE)
        wave_b = axes5.plot(lambda x: np.sin(x + 0.5), color=RED)
        
        label_a = MathTex(r"\sin(x)", font_size=28, color=BLUE)
        label_a.next_to(wave_a, UP)
        label_b = MathTex(r"\sin(x+0.5)", font_size=28, color=RED)
        label_b.next_to(wave_b, DOWN)
        
        self.play(Create(wave_a), Create(wave_b), Write(label_a), Write(label_b))
        self.wait(0.5)
        
        # Dot product formula
        dot_formula = MathTex(
            r"\langle a, b \rangle = \int a(t) b(t) dt",
            font_size=36, color=YELLOW
        )
        dot_formula.shift(DOWN * 1.5)
        self.play(Write(dot_formula))
        self.wait(0.5)
        
        # Integration visualization
        integrand = axes5.plot(lambda x: np.sin(x) * np.sin(x + 0.5), color=GREEN)
        integrand_label = MathTex(r"a(t) \cdot b(t)", font_size=28, color=GREEN)
        integrand_label.next_to(integrand, UP)
        self.play(Create(integrand), Write(integrand_label))
        self.wait(0.5)
        
        # Show correlation result
        result_text = Text("Large overlap → Large inner product → Frequency matches!", 
                          font_size=24, color=GREEN)
        result_text.to_edge(DOWN)
        self.play(Write(result_text))
        self.wait(0.5)
        
        # Cleanup
        self.play(FadeOut(title5), FadeOut(axes5), FadeOut(wave_a), FadeOut(wave_b),
                  FadeOut(label_a), FadeOut(label_b), FadeOut(dot_formula),
                  FadeOut(integrand), FadeOut(integrand_label), FadeOut(result_text))
        self.clear()
        
        # Scene 6: Fourier Transform as Inner Products
        title6 = Text("FT = Inner Product with Complex Exponentials", font_size=38, color=MAROON)
        self.play(Write(title6))
        self.wait(0.5)
        self.play(title6.animate.to_edge(UP))
        
        # Show the matching process
        note = Text(
            "For each frequency f:\n"
            "  1. Create a complex exponential e^{-j2πft}\n"
            "  2. Compute inner product with signal\n"
            "  3. The result X(f) shows how much of that frequency exists",
            font_size=28, color=WHITE, line_spacing=0.8
        )
        note.shift(LEFT * 2)
        self.play(Write(note))
        self.wait(0.5)
        
        # Visual of multiple frequency matching
        freqs = [1, 2, 3, 4]
        bars = VGroup()
        for i, f in enumerate(freqs):
            bar_height = 0.5 + 0.3 * f
            bar = Rectangle(width=0.4, height=bar_height, color=interpolate_color(BLUE, RED, f/4))
            bar.next_to(ORIGIN, RIGHT * 1.2 * i)
            bar.shift(UP * 1.5)
            bars.add(bar)
            freq_label = MathTex(f"{f} Hz", font_size=20, color=WHITE)
            freq_label.next_to(bar, DOWN)
            self.play(Create(bar), Write(freq_label), run_time=0.3)
        
        spectrum_label = Text("Frequency Spectrum", font_size=30, color=YELLOW)
        spectrum_label.shift(DOWN * 0.5)
        self.play(Write(spectrum_label))
        self.wait(0.5)
        
        # Cleanup
        self.play(FadeOut(title6), FadeOut(note), FadeOut(bars), FadeOut(spectrum_label))
        self.clear()
        
        # Scene 7: Example - Decomposing a Real Signal
        title7 = Text("Example: Decompose a Real Signal", font_size=42, color=GOLD)
        self.play(Write(title7))
        self.wait(0.5)
        self.play(title7.animate.to_edge(UP))
        
        # Define a mixed signal
        axes7 = Axes(x_range=[0, 2*PI], y_range=[-2, 2], x_length=6, y_length=3)
        axes7.shift(LEFT * 3 + UP)
        self.play(Create(axes7))
        
        mixed_signal = axes7.plot(lambda x: 0.7*np.sin(2*x) + 0.5*np.cos(5*x) + 0.3*np.sin(8*x), color=RED)
        mixed_label = Text("Input Signal x(t)", font_size=24, color=RED)
        mixed_label.next_to(axes7, DOWN)
        self.play(Create(mixed_signal), Write(mixed_label))
        self.wait(0.5)
        
        # Show frequency domain (simulated)
        spec_axes = Axes(x_range=[0, 10], y_range=[0, 1], x_length=5, y_length=2)
        spec_axes.shift(RIGHT * 3 + UP)
        spec_label = Text("|X(f)|", font_size=30, color=YELLOW)
        spec_label.next_to(spec_axes, UP)
        self.play(Create(spec_axes), Write(spec_label))
        
        # Create frequency peaks
        peak1 = Rectangle(width=0.3, height=0.7, color=BLUE, fill_opacity=0.8)
        peak1.move_to(spec_axes.c2p(2, 0.7))
        peak2 = Rectangle(width=0.3, height=0.5, color=GREEN, fill_opacity=0.8)
        peak2.move_to(spec_axes.c2p(5, 0.5))
        peak3 = Rectangle(width=0.3, height=0.3, color=PURPLE, fill_opacity=0.8)
        peak3.move_to(spec_axes.c2p(8, 0.3))
        
        self.play(Create(peak1), Create(peak2), Create(peak3))
        self.wait(0.5)
        
        # Labels for peaks
        f1 = MathTex("f_1=2", font_size=24, color=BLUE).next_to(peak1, DOWN)
        f2 = MathTex("f_2=5", font_size=24, color=GREEN).next_to(peak2, DOWN)
        f3 = MathTex("f_3=8", font_size=24, color=PURPLE).next_to(peak3, DOWN)
        self.play(Write(f1), Write(f2), Write(f3))
        self.wait(0.5)
        
        # Cleanup
        self.play(FadeOut(title7), FadeOut(axes7), FadeOut(mixed_signal), FadeOut(mixed_label),
                  FadeOut(spec_axes), FadeOut(spec_label), FadeOut(peak1), FadeOut(peak2),
                  FadeOut(peak3), FadeOut(f1), FadeOut(f2), FadeOut(f3))
        self.clear()
        
        # Scene 8: Discrete Fourier Transform (DFT) Introduction
        title8 = Text("Discrete Fourier Transform (DFT)", font_size=44, color=BLUE)
        self.play(Write(title8))
        self.wait(0.5)
        self.play(title8.animate.to_edge(UP))
        
        # Formula for DFT
        dft_formula = MathTex(
            r"X[k] = \sum_{n=0}^{N-1} x[n] e^{-j\frac{2\pi}{N}kn}",
            font_size=38, color=YELLOW
        )
        self.play(Write(dft_formula))
        self.wait(0.5)
        
        # Discrete signal
        axes8 = Axes(x_range=[0, 10], y_range=[-1.5, 1.5], x_length=5, y_length=2.5)
        axes8.shift(LEFT * 2 + DOWN)
        self.play(Create(axes8))
        
        # Sample points
        sample_points = VGroup()
        for n in range(11):
            x_val = n * 0.9
            dot = Dot(axes8.c2p(x_val, np.sin(x_val)), color=RED, radius=0.08)
            sample_points.add(dot)
        self.play(Create(sample_points), run_time=0.5)
        
        discrete_label = Text("x[n] (sampled)", font_size=24, color=RED)
        discrete_label.next_to(axes8, DOWN)
        self.play(Write(discrete_label))
        self.wait(0.5)
        
        # Second part of DFT
        n_note = Text("N = number of samples\nk = frequency index", font_size=26, color=WHITE)
        n_note.shift(RIGHT * 3 + DOWN)
        self.play(Write(n_note))
        self.wait(0.5)
        
        # Cleanup
        self.play(FadeOut(title8), FadeOut(dft_formula), FadeOut(axes8),
                  FadeOut(sample_points), FadeOut(discrete_label), FadeOut(n_note))
        self.clear()
        
        # Scene 9: FFT - Fast Implementation
        title9 = Text("Fast Fourier Transform (FFT)", font_size=44, color=GREEN)
        self.play(Write(title9))
        self.wait(0.5)
        self.play(title9.animate.to_edge(UP))
        
        # Complexity comparison
        complexity_naive = MathTex(r"\text{DFT: } O(N^2)", font_size=36, color=RED)
        complexity_fft = MathTex(r"\text{FFT: } O(N \log N)", font_size=36, color=GREEN)
        complexity_naive.shift(UP * 0.5)
        complexity_fft.shift(DOWN * 0.5)
        self.play(Write(complexity_naive), Write(complexity_fft))
        self.wait(0.5)
        
        # Visual comparison
        n_value = 1024
        naive_val = 1024**2
        fft_val = int(1024 * np.log2(1024))
        
        text_compare = Text(
            f"For N = {n_value}:\n"
            f"DFT: ~{naive_val:,} operations\n"
            f"FFT: ~{fft_val:,} operations",
            font_size=28, color=WHITE, line_spacing=0.8
        )
        text_compare.shift(DOWN * 1.5)
        self.play(Write(text_compare))
        self.wait(0.5)
        
        # Application list
        apps = Text(
            "Applications:\n"
            "• Audio compression (MP3)\n"
            "• Image processing (JPEG)\n"
            "• Wireless communications\n"
            "• Medical imaging (MRI)",
            font_size=24, color=TEAL
        )
        apps.shift(RIGHT * 3 + UP)
        self.play(Write(apps))
        self.wait(0.5)
        
        # Cleanup
        self.play(FadeOut(title9), FadeOut(complexity_naive), FadeOut(complexity_fft),
                  FadeOut(text_compare), FadeOut(apps))
        self.clear()
        
        # Scene 10: Conclusion & Summary
        title10 = Text("Fourier Transform: Summary", font_size=48, color=PURPLE)
        self.play(Write(title10))
        self.wait(0.5)
        self.play(title10.animate.to_edge(UP))
        
        # Key points
        points = VGroup(
            Text("✓ Signals can be decomposed into frequencies", font_size=28, color=WHITE),
            Text("✓ FT maps time domain → frequency domain", font_size=28, color=WHITE),
            Text("✓ Uses inner products with complex exponentials", font_size=28, color=WHITE),
            Text("✓ DFT enables digital computation", font_size=28, color=WHITE),
            Text("✓ FFT makes it fast and practical", font_size=28, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        points.shift(LEFT * 0.5)
        
        for point in points:
            self.play(Write(point), run_time=0.3)
            self.wait(0.2)
        
        # Final message
        final_text = Text("Understanding the frequency content of signals", font_size=32, color=GOLD)
        final_text.to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(1)
        
        # Appreciation
        thanks = Text("is key to modern technology!", font_size=28, color=BLUE)
        thanks.next_to(final_text, DOWN)
        self.play(Write(thanks))
        self.wait(1)
        
        # Final fadeout
        self.play(FadeOut(title10), FadeOut(points), FadeOut(final_text), FadeOut(thanks))
        self.clear()
        self.wait(0.5)
