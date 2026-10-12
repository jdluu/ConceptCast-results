from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # ==================================================
        # SCENE 1: The Time Domain Signal
        # ==================================================
        title1 = Text("Step 1: A Signal in Time", font_size=48).to_edge(UP)
        self.play(Write(title1))

        axes_time = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=4,
            axis_config={"include_numbers": False},
            tips=False
        ).shift(DOWN*0.5)
        x_label = axes_time.get_x_axis_label("Time (t)")
        y_label = axes_time.get_y_axis_label("Amplitude")

        # Define a composite signal: f(t) = sin(t) + 0.5*sin(3t)
        def signal_func(t):
            return np.sin(t) + 0.5 * np.sin(3*t)

        graph = axes_time.plot(signal_func, color=BLUE, stroke_width=3)
        graph_label = MathTex("f(t) = \\sin(t) + \\frac{1}{2}\\sin(3t)", font_size=36).next_to(axes_time, UP, buff=0.5)

        self.play(Create(axes_time), Write(x_label), Write(y_label))
        self.play(Create(graph), run_time=3)
        self.play(Write(graph_label))
        self.wait(2)

        # Highlight complexity
        brace = Brace(graph, UP, buff=0.2)
        brace_text = brace.get_text("Complex Waveform").scale(0.8)
        self.play(GrowFromCenter(brace), Write(brace_text))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()

        # ==================================================
        # SCENE 2: Building Blocks - Pure Sines
        # ==================================================
        title2 = Text("Step 2: The Building Blocks (Sinusoids)", font_size=48).to_edge(UP)
        self.play(Write(title2))

        axes_sines = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            y_length=3,
            tips=False
        ).shift(DOWN*0.5)

        # Component 1: Fundamental
        g1 = axes_sines.plot(lambda t: np.sin(t), color=YELLOW)
        l1 = MathTex("\\sin(t)", color=YELLOW).next_to(axes_sines, UP, buff=0.5).shift(LEFT*4)

        # Component 2: 3rd Harmonic
        g2 = axes_sines.plot(lambda t: 0.5*np.sin(3*t), color=GREEN)
        l2 = MathTex("\\frac{1}{2}\\sin(3t)", color=GREEN).next_to(axes_sines, UP, buff=0.5).shift(RIGHT*4)

        self.play(Create(axes_sines))
        self.play(Create(g1), Write(l1))
        self.wait(1)
        self.play(Create(g2), Write(l2))
        self.wait(2)

        # Show superposition
        sum_text = Text("Superposition (Addition)", font_size=36).to_edge(DOWN)
        self.play(Write(sum_text))
        self.play(FadeOut(g1, g2, l1, l2, axes_sines, sum_text))
        self.clear()

        # ==================================================
        # SCENE 3: The Frequency Domain Concept
        # ==================================================
        title3 = Text("Step 3: The Frequency Domain View", font_size=48).to_edge(UP)
        self.play(Write(title3))

        axes_freq = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1.2, 0.5],
            x_length=10,
            y_length=4,
            axis_config={"include_numbers": True},
            tips=False
        ).shift(DOWN*0.5)
        x_label_f = axes_freq.get_x_axis_label("Frequency (\\omega)")
        y_label_f = axes_freq.get_y_axis_label("Magnitude")

        # Bars for frequencies 1 and 3
        bars = VGroup()
        # Freq 1, Mag 1
        bar1 = Rectangle(width=0.5, height=axes_freq.y_axis.get_unit_size()*1, fill_color=YELLOW, fill_opacity=0.8, stroke_width=0)
        bar1.move_to(axes_freq.c2p(1, 0.5), DOWN)
        label1 = MathTex("1", font_size=24).next_to(bar1, UP, buff=0.1)
        
        # Freq 3, Mag 0.5
        bar3 = Rectangle(width=0.5, height=axes_freq.y_axis.get_unit_size()*0.5, fill_color=GREEN, fill_opacity=0.8, stroke_width=0)
        bar3.move_to(axes_freq.c2p(3, 0.25), DOWN)
        label3 = MathTex("0.5", font_size=24).next_to(bar3, UP, buff=0.1)

        bars.add(bar1, label1, bar3, label3)

        self.play(Create(axes_freq), Write(x_label_f), Write(y_label_f))
        self.play(FadeIn(bar1), Write(label1))
        self.play(FadeIn(bar3), Write(label3))
        self.wait(2)

        eq_text = MathTex("f(t) \\xrightarrow{\\mathcal{F}} F(\\omega)", font_size=48).next_to(axes_freq, UP, buff=1)
        self.play(Write(eq_text))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()

        # ==================================================
        # SCENE 4: The Fourier Transform Integral
        # ==================================================
        title4 = Text("Step 4: The Mathematical Operation", font_size=48).to_edge(UP)
        self.play(Write(title4))

        ft_formula = MathTex(
            "F(\\omega) = \\int_{-\\infty}^{\\infty} f(t) e^{-i\\omega t} dt",
            font_size=60
        ).move_to(ORIGIN)

        self.play(Write(ft_formula))
        self.wait(1)

        # Breakdown labels
        parts = VGroup(
            Text("Signal", font_size=24).next_to(ft_formula[0][11:13], DOWN, buff=0.5),
            Text("Complex", font_size=24).next_to(ft_formula[0][14:20], DOWN, buff=0.5),
            Text("Rotation", font_size=24).next_to(ft_formula[0][14:20], DOWN, buff=0.9),
            Text("Integration", font_size=24).next_to(ft_formula[0][20:], DOWN, buff=0.5),
        )
        parts[0].set_color(BLUE)
        parts[1].set_color(RED)
        parts[2].set_color(RED)
        parts[3].set_color(GREEN)

        brace1 = Brace(ft_formula[0][11:13], DOWN, buff=0.3)
        brace2 = Brace(ft_formula[0][14:20], DOWN, buff=0.3)
        brace3 = Brace(ft_formula[0][20:], DOWN, buff=0.3)

        self.play(GrowFromCenter(brace1), Write(parts[0]))
        self.play(GrowFromCenter(brace2), Write(parts[1]), Write(parts[2]))
        self.play(GrowFromCenter(brace3), Write(parts[3]))
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()

        # ==================================================
        # SCENE 5: Visualizing Correlation (The "Unwinding")
        # ==================================================
        title5 = Text("Step 5: Detecting Frequencies (Correlation)", font_size=48).to_edge(UP)
        self.play(Write(title5))

        # Left: Time domain signal
        axes_t = Axes(x_range=[0, 4*PI, PI], y_range=[-2,2], x_length=6, y_length=3, tips=False).shift(LEFT*3.5 + DOWN*0.5)
        sig_graph = axes_t.plot(signal_func, color=BLUE)
        
        # Right: Rotating phasor / Complex plane
        axes_c = ComplexPlane(x_range=[-1.5,1.5], y_range=[-1.5,1.5], x_length=4, y_length=4).shift(RIGHT*3.5 + DOWN*0.5)
        axes_c_labels = axes_c.get_axis_labels("Re", "Im")
        
        # Center of mass dot
        com_dot = Dot(color=RED).move_to(axes_c.c2p(0,0))
        com_trace = TracedPath(com_dot.get_center, stroke_color=RED, stroke_width=2)

        self.play(Create(axes_t), Create(sig_graph), Create(axes_c), Write(axes_c_labels))
        self.add(com_trace)
        self.play(FadeIn(com_dot))

        # Animation: "Unwinding" at frequency omega=1
        tracker = ValueTracker(0)
        def get_com_position():
            t_vals = np.linspace(0, 4*PI, 200)
            dt = t_vals[1] - t_vals[0]
            omega = 1.0 # Target frequency
            # Sum f(t) * e^{-i omega t}
            integral_sum = np.sum([signal_func(t) * np.exp(-1j * omega * t) * dt for t in t_vals])
            return axes_c.c2p(integral_sum.real, integral_sum.imag)

        # Animate the "winding" process conceptually
        # We simulate the integral accumulating
        winding_line = ParametricFunction(
            lambda u: axes_c.c2p(
                np.sum([signal_func(t) * np.exp(-1j * 1.0 * t) * (4*PI/200) for t in np.linspace(0, u, 50)]).real,
                np.sum([signal_func(t) * np.exp(-1j * 1.0 * t) * (4*PI/200) for t in np.linspace(0, u, 50)]).imag
            ),
            t_range=[0, 4*PI],
            color=RED
        )
        
        self.play(Create(winding_line), run_time=4, rate_func=linear)
        self.wait(1)

        result_text = MathTex("\\text{Peak at } \\omega=1 \\rightarrow \\text{Magnitude } \\approx \\pi", font_size=36).to_edge(DOWN)
        self.play(Write(result_text))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()

        # ==================================================
        # SCENE 6: The Full Spectrum
        # ==================================================
        title6 = Text("Step 6: The Complete Spectrum", font_size=48).to_edge(UP)
        self.play(Write(title6))

        axes_final = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 3.5, 1],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True},
            tips=False
        ).shift(DOWN*0.5)
        labels_f = axes_final.get_axis_labels("\\omega", "|F(\\omega)|")

        # Theoretical FT of sin(t) + 0.5sin(3t) -> peaks at 1 and 3 (Dirac deltas approximated as sharp bars)
        # Magnitude pi at 1, pi/2 at 3 (approx 3.14 and 1.57)
        bars_final = VGroup()
        freqs = [1, 3]
        mags = [PI, PI/2]
        colors = [YELLOW, GREEN]

        for freq, mag, col in zip(freqs, mags, colors):
            bar = Rectangle(width=0.2, height=axes_final.y_axis.get_unit_size()*mag, fill_color=col, fill_opacity=1, stroke_width=0)
            bar.move_to(axes_final.c2p(freq, mag/2), DOWN)
            label = MathTex(f"\\omega={freq}", font_size=28).next_to(bar, UP, buff=0.2)
            bars_final.add(bar, label)

        self.play(Create(axes_final), Write(labels_f))
        self.play(LaggedStart(*[FadeIn(b) for b in bars_final], lag_ratio=0.2))
        self.wait(2)

        summary = Text("Fourier Transform: Recipe of Frequencies", font_size=36, color=GOLD).to_edge(DOWN)
        self.play(Write(summary))
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()

        # ==================================================
        # SCENE 7: Conclusion
        # ==================================================
        title7 = Text("Summary", font_size=60).move_to(UP*2)
        bullets = VGroup(
            Text("1. Time Domain: How a signal changes over time.", font_size=32),
            Text("2. Frequency Domain: How much of each frequency exists.", font_size=32),
            Text("3. Fourier Transform: The bridge between them.", font_size=32),
            Text("4. Applications: Audio, Images, Compression, Physics.", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(DOWN*0.5)

        self.play(Write(title7))
        self.play(LaggedStart(*[Write(b) for b in bullets], lag_ratio=0.3))
        self.wait(3)
