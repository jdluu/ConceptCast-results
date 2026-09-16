#!/usr/bin/env python3
"""
Fourier Transform Educational Animation
Teaches the concept from first principles to full visualization.
Manim Community Edition v0.20.1
"""

from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # ------------------------------------------------------------
        # Scene 1: Introduction to signals as functions of time
        # ------------------------------------------------------------
        title = Text("Fourier Transform", font_size=48, color=BLUE)
        subtitle = Text("Decomposing signals into frequencies", font_size=28, color=GREY)
        subtitle.next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        
        # Show a simple time-domain signal
        axes = Axes(
            x_range=[0, 4, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=8,
            y_length=3,
            axis_config={"include_numbers": True}
        ).shift(DOWN)
        axes_labels = axes.get_axis_labels(x_label="t", y_label="f(t)")
        sine_curve = axes.plot(lambda x: 1.5 * np.sin(2 * PI * x), 
                              color=YELLOW, x_range=[0, 4])
        sine_label = MathTex("f(t) = 1.5 \\sin(2\\pi t)", font_size=24, color=YELLOW)
        sine_label.next_to(title, DOWN)
        
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(sine_curve), Write(sine_label))
        self.wait(2)
        self.clear()

        # ------------------------------------------------------------
        # Scene 2: Composite signals (sum of frequencies)
        # ------------------------------------------------------------
        subtitle2 = Text("Real signals contain multiple frequencies", font_size=32, color=BLUE)
        subtitle2.to_edge(UP)
        self.play(Write(subtitle2))
        
        # Create composite signal
        axes2 = Axes(
            x_range=[0, 4, 0.5],
            y_range=[-3, 3, 0.5],
            x_length=8,
            y_length=3.5,
            axis_config={"include_numbers": True}
        ).shift(DOWN)
        axes_labels2 = axes2.get_axis_labels(x_label="t", y_label="f(t)")
        
        # Define component frequencies
        f1 = lambda x: 1.5 * np.sin(2 * PI * x)
        f2 = lambda x: 1.0 * np.sin(4 * PI * x)
        f3 = lambda x: 0.5 * np.sin(6 * PI * x)
        composite = lambda x: f1(x) + f2(x) + f3(x)
        
        # Show components one by one
        curve1 = axes2.plot(f1, color=RED, x_range=[0, 4])
        curve2 = axes2.plot(f2, color=GREEN, x_range=[0, 4])
        curve3 = axes2.plot(f3, color=BLUE, x_range=[0, 4])
        composite_curve = axes2.plot(composite, color=YELLOW, x_range=[0, 4])
        
        self.play(Create(axes2), Write(axes_labels2))
        self.play(Create(curve1))
        self.wait(0.5)
        self.play(Create(curve2))
        self.wait(0.5)
        self.play(Create(curve3))
        self.wait(0.5)
        self.play(
            Transform(curve1, composite_curve),
            FadeOut(curve2),
            FadeOut(curve3)
        )
        legend = VGroup(
            Square(color=YELLOW, fill_opacity=0.5).scale(0.3),
            Text("Composite signal", font_size=20, color=YELLOW)
        ).arrange(RIGHT).to_corner(DR)
        self.play(Write(legend))
        self.wait(2)
        self.clear()

        # ------------------------------------------------------------
        # Scene 3: Frequency spectrum concept
        # ------------------------------------------------------------
        sub3 = Text("Frequency Domain: What frequencies are present?", font_size=32, color=BLUE)
        sub3.to_edge(UP)
        self.play(Write(sub3))
        
        # Create frequency spectrum
        freq_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 2, 0.5],
            x_length=8,
            y_length=3,
            axis_config={"include_numbers": True}
        ).shift(DOWN)
        freq_labels = freq_axes.get_axis_labels(x_label="f (Hz)", y_label="Amplitude")
        
        # Three frequency components
        bars = VGroup()
        freqs = [(1, 1.5), (2, 1.0), (3, 0.5)]
        for f, amp in freqs:
            bar = Rectangle(
                width=0.4,
                height=amp,
                fill_color=YELLOW,
                fill_opacity=0.8,
                stroke_color=WHITE
            ).move_to(freq_axes.c2p(f, amp/2), aligned_edge=DOWN)
            bars.add(bar)
            
            # Label the frequency
            label = MathTex(f"{f}\\:Hz", font_size=20).next_to(bar, DOWN)
            bars.add(label)
        
        self.play(Create(freq_axes), Write(freq_labels))
        self.play(*[Create(bar) for bar in bars[::2]])  # Only draw rectangles first
        self.play(*[Write(label) for label in bars[1::2]])  # Then labels
        self.wait(2)
        
        # Add explanation
        explain = Text("Each bar shows amplitude of a frequency component", 
                      font_size=24, color=GREY).next_to(sub3, DOWN)
        self.play(Write(explain))
        self.wait(2)
        self.clear()

        # ------------------------------------------------------------
        # Scene 4: Inner product / correlation concept
        # ------------------------------------------------------------
        sub4 = Text("How to find frequencies? Use correlation!", font_size=32, color=BLUE)
        sub4.to_edge(UP)
        self.play(Write(sub4))
        
        # Show a test signal and a reference sine
        axes4 = Axes(
            x_range=[0, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=8,
            y_length=3,
            axis_config={"include_numbers": True}
        ).shift(DOWN)
        axes_labels4 = axes4.get_axis_labels(x_label="t", y_label="f(t)")
        
        # Test signal (contains 1Hz and 2Hz)
        test_sig = axes4.plot(lambda x: np.sin(2*PI*x) + 0.5*np.sin(4*PI*x), 
                             color=YELLOW, x_range=[0, 2])
        test_label = Text("Test signal", font_size=20, color=YELLOW).to_corner(DR)
        
        # Reference sine at 1Hz
        ref_sine = axes4.plot(lambda x: np.sin(2*PI*x), color=RED, x_range=[0, 2])
        ref_label = Text("Reference: sin(2πt)", font_size=20, color=RED).to_corner(UR)
        
        self.play(Create(axes4), Write(axes_labels4))
        self.play(Create(test_sig), Write(test_label))
        self.wait(1)
        self.play(Create(ref_sine), Write(ref_label))
        self.wait(2)
        
        # Show product and area (correlation)
        product_text = MathTex("\\text{Correlation} = \\int f(t) \\cdot \\sin(2\\pi t) \\, dt", 
                              font_size=28, color=GREEN)
        product_text.next_to(sub4, DOWN)
        self.play(Write(product_text))
        self.wait(2)
        self.clear()

        # ------------------------------------------------------------
        # Scene 5: Discrete sampling concept
        # ------------------------------------------------------------
        sub5 = Text("Discrete signals: Sampling in time", font_size=32, color=BLUE)
        sub5.to_edge(UP)
        self.play(Write(sub5))
        
        # Show a continuous sine and its samples
        axes5 = Axes(
            x_range=[0, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=8,
            y_length=3,
            axis_config={"include_numbers": True}
        ).shift(DOWN)
        axes_labels5 = axes5.get_axis_labels(x_label="t", y_label="f(t)")
        
        continuous = axes5.plot(lambda x: 1.5 * np.sin(2*PI*x), 
                               color=BLUE, x_range=[0, 2])
        
        # Generate sample points
        sample_points = np.linspace(0, 2, 16)
        samples = [Dot(axes5.c2p(t, 1.5*np.sin(2*PI*t)), color=YELLOW) for t in sample_points]
        
        self.play(Create(axes5), Write(axes_labels5))
        self.play(Create(continuous))
        self.play(*[GrowFromCenter(s) for s in samples])
        
        sample_text = Text("16 samples over 2 seconds", font_size=20).to_corner(DR)
        self.play(Write(sample_text))
        self.wait(2)
        self.clear()

        # ------------------------------------------------------------
        # Scene 6: Discrete Fourier Transform (DFT) visualization
        # ------------------------------------------------------------
        sub6 = Text("Discrete Fourier Transform (DFT)", font_size=32, color=BLUE)
        sub6.to_edge(UP)
        self.play(Write(sub6))
        
        # Show DFT formula
        dft_formula = MathTex(
            "X[k] = \\sum_{n=0}^{N-1} x[n] e^{-i 2\\pi \\frac{k n}{N}}",
            font_size=36, color=GREEN
        )
        self.play(Write(dft_formula))
        self.wait(1)
        
        # Animate moving from time domain to frequency domain
        time_arrow = MathTex("\\xrightarrow[\\text{DFT}]{\\text{Time}}", font_size=28)
        time_arrow.next_to(dft_formula, DOWN)
        freq_result = MathTex("\\text{Frequency Domain}", font_size=32, color=YELLOW)
        freq_result.next_to(time_arrow, DOWN)
        
        self.play(Write(time_arrow))
        self.wait(0.5)
        self.play(Write(freq_result))
        self.wait(2)
        self.clear()

        # ------------------------------------------------------------
        # Scene 7: Real input signal (voice/audio metaphor)
        # ------------------------------------------------------------
        sub7 = Text("Real signals: Audio, sensor data, etc.", font_size=32, color=BLUE)
        sub7.to_edge(UP)
        self.play(Write(sub7))
        
        # Create a more complex signal that looks like speech
        axes7 = Axes(
            x_range=[0, 3, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=8,
            y_length=3,
            axis_config={"include_numbers": True}
        ).shift(DOWN)
        axes_labels7 = axes7.get_axis_labels(x_label="Time", y_label="Amplitude")
        
        # Create a pseudo-random-looking audio-like signal
        t_vals = np.linspace(0, 3, 100)
        audio_signal = (0.3*np.sin(2*PI*5*t_vals) + 
                       0.5*np.sin(2*PI*12*t_vals) + 
                       0.2*np.sin(2*PI*20*t_vals) +
                       0.4*np.sin(2*PI*30*t_vals))
        # Add some random variation
        np.random.seed(42)
        audio_signal += 0.1 * np.random.randn(100)
        
        audio_curve = axes7.plot(lambda x: np.interp(x, t_vals, audio_signal), 
                               color=YELLOW, x_range=[0, 3])
        
        self.play(Create(axes7), Write(axes_labels7))
        self.play(Create(audio_curve))
        
        mic = Text("🎤 Input signal", font_size=24).to_corner(DL)
        self.play(Write(mic))
        self.wait(2)
        self.clear()

        # ------------------------------------------------------------
        # Scene 8: Full transform animation
        # ------------------------------------------------------------
        sub8 = Text("Applying the Fourier Transform", font_size=32, color=BLUE)
        sub8.to_edge(UP)
        self.play(Write(sub8))
        
        # Time domain signal
        axes_t = Axes(
            x_range=[0, 3, 0.5],
            y_range=[-3, 3, 0.5],
            x_length=6,
            y_length=2.5,
            axis_config={"include_numbers": True}
        ).shift(2*LEFT + DOWN)
        label_t = axes_t.get_axis_labels(x_label="Time", y_label="Amp")
        
        # Create composite signal
        sig = lambda x: 1.5*np.sin(2*PI*x) + 1.0*np.sin(4*PI*x + PI/4) + 0.5*np.sin(6*PI*x)
        time_curve = axes_t.plot(sig, color=YELLOW, x_range=[0, 3])
        
        # Frequency domain
        axes_f = Axes(
            x_range=[0, 4, 0.5],
            y_range=[0, 2, 0.5],
            x_length=6,
            y_length=2.5,
            axis_config={"include_numbers": True}
        ).shift(2*RIGHT + DOWN)
        label_f = axes_f.get_axis_labels(x_label="Freq (Hz)", y_label="Mag")
        
        # Frequency bars
        bar_data = [(1, 1.5), (2, 1.0), (3, 0.5)]
        freq_bars = VGroup()
        for f, amp in bar_data:
            bar = Rectangle(
                width=0.35,
                height=0,  # Start from 0 height
                fill_color=GREEN,
                fill_opacity=0.8,
                stroke_color=WHITE
            ).move_to(axes_f.c2p(f, 0), aligned_edge=DOWN)
            freq_bars.add(bar)
        
        # Create both before animation
        self.play(Create(axes_t), Write(label_t))
        self.play(Create(time_curve))
        self.wait(1)
        
        # Transform animation: fade out time, create frequency
        self.play(
            FadeOut(time_curve),
            Create(axes_f),
            Write(label_f)
        )
        
        # Animate bars growing
        animations = []
        for i, (f, amp) in enumerate(bar_data):
            target_bar = Rectangle(
                width=0.35,
                height=amp,
                fill_color=GREEN,
                fill_opacity=0.8,
                stroke_color=WHITE
            ).move_to(axes_f.c2p(f, amp/2), aligned_edge=DOWN)
            animations.append(Transform(freq_bars[i], target_bar))
        
        self.play(*animations)
        
        arrow = Arrow(axes_t.get_right(), axes_f.get_left(), color=BLUE)
        arrow_text = Text("Fourier Transform", font_size=20, color=BLUE).next_to(arrow, UP)
        self.play(Create(arrow), Write(arrow_text))
        self.wait(3)
        self.clear()

        # ------------------------------------------------------------
        # Scene 9: Inverse Fourier Transform
        # ------------------------------------------------------------
        sub9 = Text("Inverse Fourier Transform: Reconstruct signal", font_size=32, color=BLUE)
        sub9.to_edge(UP)
        self.play(Write(sub9))
        
        # Show inverse transform formula
        inv_formula = MathTex(
            "x[n] = \\frac{1}{N} \\sum_{k=0}^{N-1} X[k] e^{i 2\\pi \\frac{k n}{N}}",
            font_size=36, color=GREEN
        )
        self.play(Write(inv_formula))
        
        # Animate reconstruction
        reconstruction_text = Text("Rebuild original signal from frequencies", 
                                  font_size=24).next_to(inv_formula, DOWN)
        self.play(Write(reconstruction_text))
        
        # Show rebuilding process with sine waves adding up
        axes_recon = Axes(
            x_range=[0, 3, 0.5],
            y_range=[-3, 3, 0.5],
            x_length=8,
            y_length=3,
            axis_config={"include_numbers": True}
        ).shift(3*DOWN)
        labels_recon = axes_recon.get_axis_labels(x_label="t", y_label="f(t)")
        
        self.play(Create(axes_recon), Write(labels_recon))
        
        # Sequentially add sine waves
        curves = []
        for i, (freq, amp, phase) in enumerate([(1, 1.5, 0), (2, 1.0, PI/4), (3, 0.5, 0)]):
            curve = axes_recon.plot(
                lambda x, f=freq, a=amp, p=phase: a * np.sin(2*PI*f*x + p),
                color=LIGHT_GREY if i < 2 else YELLOW,
                x_range=[0, 3]
            )
            curves.append(curve)
        
        self.play(Create(curves[0]), Create(curves[1]))
        self.wait(1)
        self.play(Create(curves[2]))
        
        final_text = Text("Original signal reconstructed!", font_size=20, color=YELLOW).to_corner(DR)
        self.play(Write(final_text))
        self.wait(2)
        self.clear()

        # ------------------------------------------------------------
        # Scene 10: Summary and real-world applications
        # ------------------------------------------------------------
        sub10 = Text("Fourier Transform: Summary", font_size=40, color=BLUE)
        sub10.to_edge(UP)
        self.play(Write(sub10))
        
        points = VGroup(
            Text("• Decomposes signals into frequencies", font_size=24, color=WHITE),
            Text("• Converts time → frequency domain", font_size=24, color=WHITE),
            Text("• Discrete version: DFT / FFT algorithm", font_size=24, color=WHITE),
            Text("• Used in: audio processing, image compression," , font_size=24, color=WHITE),
            Text("   communications, medical imaging (MRI)", font_size=24, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(sub10, DOWN, buff=0.8)
        
        for point in points:
            self.play(Write(point, run_time=0.8))
        
        # Final animations: speech processing visualization
        app_axes = Axes(
            x_range=[0, 2, 0.5],
            y_range=[-2, 2, 0.5],
            x_length=5,
            y_length=2,
            axis_config={"include_numbers": False}
        ).shift(3*LEFT + 2*DOWN)
        
        app_axes2 = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1.5, 0.5],
            x_length=5,
            y_length=2,
            axis_config={"include_numbers": False}
        ).shift(3*RIGHT + 2*DOWN)
        
        # Animate a final voice-like signal transforming to spectrum
        voice_sig = app_axes.plot(lambda x: 0.8*np.sin(2*PI*3*x) + 0.4*np.sin(2*PI*7*x), 
                                  color=YELLOW, x_range=[0, 2])
        voice_bars = VGroup(
            Rectangle(width=0.3, height=0.8, fill_color=GREEN, fill_opacity=0.8,
                     stroke_color=WHITE).move_to(app_axes2.c2p(1, 0.4), aligned_edge=DOWN),
            Rectangle(width=0.3, height=0.4, fill_color=GREEN, fill_opacity=0.8,
                     stroke_color=WHITE).move_to(app_axes2.c2p(2, 0.2), aligned_edge=DOWN)
        )
        
        self.play(
            Create(app_axes),
            Create(app_axes2),
            Create(voice_sig),
            Create(voice_bars)
        )
        
        # Final text
        final = Text("Thank you!", font_size=36, color=YELLOW).to_corner(UR)
        self.play(Write(final))
        self.wait(3)
