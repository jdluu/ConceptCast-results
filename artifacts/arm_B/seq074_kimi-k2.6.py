from manim import *
import numpy as np


class SceneGen(Scene):
    def construct(self):
        # SCENE 1: A signal in time domain
        self.scene1_time_domain_signal()
        
        # SCENE 2: The building blocks - pure sinusoids
        self.scene2_pure_sinusoids()
        
        # SCENE 3: Adding frequencies - synthesis
        self.scene3_synthesis()
        
        # SCENE 4: The inner product - measuring similarity
        self.scene4_inner_product()
        
        # SCENE 5: The Fourier integral - continuous probing
        self.scene5_fourier_integral()
        
        # SCENE 6: Frequency domain representation
        self.scene6_frequency_domain()
        
        # SCENE 7: Inverse Fourier transform - reconstruction
        self.scene7_inverse_transform()
        
        # SCENE 8: Real-world analogy and summary
        self.scene8_summary()

    def scene1_time_domain_signal(self):
        # Title
        title = Text("Signals in Time", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait(0.5)
        
        # Subtitle explaining time domain
        subtitle = Text("A signal varies over time", font_size=28, color=GRAY).next_to(title, DOWN, buff=0.3)
        self.play(Write(subtitle))
        self.wait(0.5)
        
        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=4,
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": np.arange(-4, 5, 1)},
            y_axis_config={"numbers_to_include": np.arange(-2, 3, 1)},
        ).shift(DOWN * 0.5)
        
        # Labels
        x_label = MathTex("t", color=WHITE).next_to(axes.x_axis, RIGHT, buff=0.2)
        y_label = MathTex("f(t)", color=WHITE).next_to(axes.y_axis, UP, buff=0.2)
        
        self.play(
            FadeOut(title, shift=UP),
            FadeOut(subtitle, shift=UP),
            Create(axes),
            Write(x_label),
            Write(y_label)
        )
        
        # Animate drawing a complex signal
        complex_signal = axes.plot(
            lambda t: 0.8 * np.sin(2 * t) + 0.4 * np.cos(5 * t) + 0.2 * np.sin(8 * t),
            x_range=[-4, 4],
            color=YELLOW,
            stroke_width=3
        )
        
        # Draw the signal progressively
        self.play(Create(complex_signal), run_time=3)
        self.wait(0.5)
        
        # Question: what's inside this signal?
        question = Text("What frequencies make up this signal?", font_size=32, color=GREEN).shift(UP * 3)
        self.play(Write(question))
        self.wait(1)
        
        # Store for removal
        self.scene1_objects = [axes, x_label, y_label, complex_signal, question]
        self.play(*[FadeOut(obj) for obj in self.scene1_objects])
        self.clear()

    def scene2_pure_sinusoids(self):
        # Title
        title = Text("The Building Blocks: Pure Frequencies", font_size=42, color=BLUE)
        self.play(Write(title))
        self.wait(0.5)
        
        subtitle = MathTex("\\cos(2\\pi f t)", "\\text{ and }", "\\sin(2\\pi f t)", font_size=36)
        subtitle.arrange(RIGHT, buff=0.3)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(Write(subtitle))
        self.wait(0.5)
        
        self.play(FadeOut(title, shift=UP), FadeOut(subtitle, shift=UP))
        
        # Create three axes showing different frequencies
        axes_group = VGroup()
        signals_group = VGroup()
        labels_group = VGroup()
        
        colors = [RED, GREEN, BLUE]
        frequencies = [1, 2, 3]
        descs = ["f = 1 Hz", "f = 2 Hz", "f = 3 Hz"]
        
        for i, (freq, color, desc) in enumerate(zip(frequencies, colors, descs)):
            ax = Axes(
                x_range=[0, 4, 1],
                y_range=[-1.5, 1.5, 1],
                x_length=3,
                y_length=1.5,
                axis_config={"color": WHITE, "stroke_width": 1},
            ).shift(LEFT * 4 + RIGHT * i * 4 + DOWN * 0.5)
            
            signal = ax.plot(
                lambda t, f=freq: np.cos(2 * np.pi * f * t),
                x_range=[0, 4],
                color=color,
                stroke_width=2.5
            )
            
            desc_text = Text(desc, font_size=24, color=color).next_to(ax, DOWN, buff=0.2)
            
            axes_group.add(ax)
            signals_group.add(signal)
            labels_group.add(desc_text)
            
            self.play(Create(ax), run_time=0.7)
            self.play(Create(signal), run_time=1.2)
            self.play(Write(desc_text), run_time=0.5)
        
        # Highlight: any signal = sum of these
        idea = Text("Any signal = sum of cosines & sines", font_size=32, color=YELLOW).shift(UP * 3)
        self.play(Write(idea))
        self.wait(1)
        
        # Remove everything
        all_objs = [axes_group, signals_group, labels_group, idea]
        self.play(*[FadeOut(obj) for obj in all_objs])
        self.clear()

    def scene3_synthesis(self):
        # Title
        title = Text("Synthesis: Building Signals from Frequencies", font_size=40, color=BLUE).shift(UP * 3.2)
        self.play(Write(title))
        
        # Main axes for sum
        main_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=4,
            axis_config={"color": WHITE},
        ).shift(DOWN * 0.3)
        
        main_label = Text("Sum", font_size=28, color=YELLOW).next_to(main_axes, UP, buff=0.1).shift(RIGHT * 3)
        
        # Component axes (smaller, on the side)
        comp_axes_list = []
        comp_signals_list = []
        comp_labels_list = []
        
        freqs = [1, 3]
        amps = [1.5, 0.8]
        colors = [RED, BLUE]
        
        for i, (freq, amp, color) in enumerate(zip(freqs, amps, colors)):
            cax = Axes(
                x_range=[0, 4, 1],
                y_range=[-2, 2, 1],
                x_length=4,
                y_length=1.2,
                axis_config={"color": GRAY, "stroke_width": 1},
            ).shift(LEFT * 3 + UP * (2 - i * 1.8))
            
            csig = cax.plot(
                lambda t, f=freq, a=amp: a * np.cos(2 * np.pi * f * t),
                x_range=[0, 4],
                color=color,
                stroke_width=2
            )
            
            clab = MathTex(f"{amp}" + f"\\cos(2\\pi \\cdot {freq} t)", font_size=22, color=color).next_to(cax, RIGHT, buff=0.2)
            
            comp_axes_list.extend([cax, csig, clab])
        
        # Show components first
        self.play(Create(main_axes))
        self.play(*[Create(obj) for obj in comp_axes_list[::3]], run_time=1)  # axes
        self.wait(0.3)
        
        # Animate signals appearing
        self.play(*[Create(comp_axes_list[i]) for i in [1, 4]], run_time=1.5)  # signals
        self.play(*[Write(comp_axes_list[i]) for i in [2, 5]], run_time=1)  # labels
        
        # Plus signs
        plus = MathTex("+", font_size=40).move_to((comp_axes_list[0].get_center() + comp_axes_list[3].get_center()) / 2 + RIGHT * 2.5)
        equals = MathTex("=", font_size=40).next_to(plus, RIGHT, buff=0.8)
        
        self.play(Write(plus))
        self.play(Write(equals))
        self.wait(0.3)
        
        # Draw the sum
        sum_signal = main_axes.plot(
            lambda t: 1.5 * np.cos(2 * np.pi * t) + 0.8 * np.cos(2 * np.pi * 3 * t),
            x_range=[0, 4],
            color=YELLOW,
            stroke_width=3
        )
        
        self.play(Create(sum_signal), run_time=2)
        self.play(Write(main_label))
        self.wait(1)
        
        # Key insight
        insight = Text("Synthesis: known ingredients → mixture", font_size=28, color=GREEN).shift(DOWN * 3)
        self.play(Write(insight))
        self.wait(0.5)
        
        # Flip to problem
        problem = Text("Analysis: mixture → unknown ingredients?", font_size=28, color=RED).next_to(insight, DOWN, buff=0.2)
        self.play(Write(problem))
        self.wait(1.5)
        
        all_objs = [title, main_axes, sum_signal, main_label, plus, equals, insight, problem] + comp_axes_list
        self.play(*[FadeOut(obj) for obj in all_objs])
        self.clear()

    def scene4_inner_product(self):
        # Title
        title = Text("The Core Idea: Measuring Similarity", font_size=40, color=BLUE).shift(UP * 3.2)
        self.play(Write(title))
        
        # Two signals to compare
        ax = Axes(
            x_range=[0, 2, 0.5],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=3,
            axis_config={"color": WHITE},
        ).shift(UP * 0.3)
        
        self.play(Create(ax))
        
        # Signal f(t)
        f_signal = ax.plot(
            lambda t: 1.2 * np.cos(2 * np.pi * t),
            x_range=[0, 2],
            color=YELLOW,
            stroke_width=2.5
        )
        f_label = MathTex("f(t)", color=YELLOW, font_size=28).next_to(ax, UR, buff=0.1)
        
        self.play(Create(f_signal), Write(f_label))
        self.wait(0.5)
        
        # Test signal g(t) = probe frequency
        g_signal = ax.plot(
            lambda t: np.cos(2 * np.pi * t),
            x_range=[0, 2],
            color=BLUE,
            stroke_width=2.5
        )
        g_label = MathTex("g(t) = \\cos(2\\pi t)", color=BLUE, font_size=28).next_to(f_label, DOWN, aligned_edge=LEFT)
        
        self.play(Create(g_signal), Write(g_label))
        self.wait(0.5)
        
        # Show product
        product = ax.plot(
            lambda t: 1.2 * np.cos(2 * np.pi * t) * np.cos(2 * np.pi * t),
            x_range=[0, 2],
            color=GREEN,
            stroke_width=2.5
        )
        product_label = MathTex("f(t) \\cdot g(t)", color=GREEN, font_size=28).next_to(g_label, DOWN, aligned_edge=LEFT)
        
        # Transform to product visualization
        self.play(
            f_signal.animate.set_stroke(opacity=0.3),
            g_signal.animate.set_stroke(opacity=0.3)
        )
        self.play(Create(product), Write(product_label))
        
        # Show area under curve (integral)
        area = ax.get_area(product, x_range=[0, 2], color=GREEN, opacity=0.3)
        self.play(FadeIn(area))
        
        # The integral value
        integral_box = SurroundingRectangle(product_label, buff=0.15)
        integral_text = MathTex("\\int_0^T f(t) g(t) \\, dt = \\text{large!}", font_size=32, color=GREEN).shift(DOWN * 2.8)
        
        self.play(Create(integral_box))
        self.play(Write(integral_text))
        self.wait(1)
        
        # Now show MISMATCH case - different frequency
        self.play(
            FadeOut(integral_box),
            FadeOut(integral_text),
            FadeOut(area),
            FadeOut(product),
            FadeOut(product_label)
        )
        
        # Change probe to wrong frequency
        g_signal_new = ax.plot(
            lambda t: np.cos(2 * np.pi * 3 * t),
            x_range=[0, 2],
            color=RED,
            stroke_width=2.5
        )
        g_label_new = MathTex("g(t) = \\cos(2\\pi \\cdot 3 t)", color=RED, font_size=28).move_to(g_label)
        
        self.play(Transform(g_signal, g_signal_new), Transform(g_label, g_label_new))
        
        # Product with mismatch
        product_mismatch = ax.plot(
            lambda t: 1.2 * np.cos(2 * np.pi * t) * np.cos(2 * np.pi * 3 * t),
            x_range=[0, 2],
            color=ORANGE,
            stroke_width=2.5
        )
        product_label_new = MathTex("f(t) \\cdot g(t)", color=ORANGE, font_size=28).move_to(product_label)
        
        self.play(Create(product_mismatch), Write(product_label_new))
        
        area_mismatch = ax.get_area(product_mismatch, x_range=[0, 2], color=ORANGE, opacity=0.3)
        self.play(FadeIn(area_mismatch))
        
        # Show cancels out
        integral_text_new = MathTex("\\int_0^T f(t) g(t) \\, dt \\approx 0", font_size=32, color=RED).shift(DOWN * 2.8)
        
        # Show cancellation with arrows
        self.play(Write(integral_text_new))
        self.wait(1.5)
        
        key_idea = Text("Matching frequency → large integral", font_size=28, color=YELLOW).shift(DOWN * 3.5)
        self.play(Write(key_idea))
        self.wait(1)
        
        all_objs = [title, ax, f_signal, f_label, g_signal, g_label, product_mismatch, 
                   product_label_new, area_mismatch, integral_text_new, key_idea]
        self.play(*[FadeOut(obj) for obj in all_objs])
        self.clear()

    def scene5_fourier_integral(self):
        # Title
        title = Text("The Fourier Transform Integral", font_size=40, color=BLUE).shift(UP * 3.2)
        self.play(Write(title))
        
        # Mathematical formula
        formula = MathTex(
            "\\hat{f}(\\xi) = \\int_{-\\infty}^{\\infty} f(t) \\, e^{-2\\pi i \\xi t} \\, dt",
            font_size=42
        ).shift(UP * 1.5)
        
        self.play(Write(formula))
        self.wait(1)
        
        # Break down components with annotations
        f_t = MathTex("f(t)", color=YELLOW, font_size=32)
        f_t.shift(LEFT * 3.5 + DOWN * 0.5)
        
        annotate1 = Text("input signal", font_size=22, color=YELLOW).next_to(f_t, DOWN, buff=0.3)
        
        self.play(formula[0][5:8].animate.set_color(YELLOW), run_time=0.5)
        self.play(Write(f_t), Write(annotate1))
        self.wait(0.5)
        
        # The complex exponential
        exp_part = MathTex("e^{-2\\pi i \\xi t}", color=BLUE, font_size=32)
        exp_part.shift(LEFT * 0.5 + DOWN * 0.5)
        
        annotate2a = Text("probe frequency", font_size=22, color=BLUE).next_to(exp_part, DOWN, buff=0.2)
        annotate2b = Text("= cos + i·sin", font_size=20, color=BLUE).next_to(annotate2a, DOWN, buff=0.1)
        
        self.play(formula[0][9:23].animate.set_color(BLUE), run_time=0.5)
        self.play(Write(exp_part), Write(annotate2a), Write(annotate2b))
        self.wait(0.5)
        
        # The integration
        integral_sign = MathTex("\\int dt", color=GREEN, font_size=32)
        integral_sign.shift(RIGHT * 3 + DOWN * 0.5)
        
        annotate3 = Text("measure total", font_size=22, color=GREEN).next_to(integral_sign, DOWN, buff=0.2)
        annotate3b = Text("similarity", font_size=22, color=GREEN).next_to(annotate3, DOWN, buff=0.1)
        
        self.play(formula[0][3:5].animate.set_color(GREEN), formula[0][23:25].animate.set_color(GREEN), run_time=0.5)
        self.play(Write(integral_sign), Write(annotate3), Write(annotate3b))
        self.wait(0.5)
        
        # The result
        result = MathTex("\\hat{f}(\\xi)", color=RED, font_size=32)
        result.shift(RIGHT * 4.5 + UP * 0.5)
        
        annotate4 = Text("Fourier coefficient", font_size=22, color=RED).next_to(result, UP, buff=0.3)
        
        self.play(formula[0][0:4].animate.set_color(RED), run_time=0.5)
        self.play(Write(result), Write(annotate4))
        
        # Visual demonstration: sweeping frequency
        self.wait(0.5)
        self.play(
            FadeOut(f_t), FadeOut(annotate1),
            FadeOut(exp_part), FadeOut(annotate2a), FadeOut(annotate2b),
            FadeOut(integral_sign), FadeOut(annotate3), FadeOut(annotate3b),
            FadeOut(result), FadeOut(annotate4),
            FadeOut(formula),
            FadeOut(title)
        )
        
        # Sweep demonstration
        demo_title = Text("Sweeping Through Frequencies...", font_size=32, color=WHITE).shift(UP * 3)
        self.play(Write(demo_title))
        
        # Axes for signal and for frequency response
        time_ax = Axes(
            x_range=[0, 4, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=2.5,
            axis_config={"color": WHITE},
        ).shift(LEFT * 2.5 + UP * 0.3)
        
        freq_ax = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 3, 1],
            x_length=6,
            y_length=2.5,
            axis_config={"color": WHITE},
        ).shift(LEFT * 2.5 + DOWN * 2.5)
        
        time_label = Text("Time domain", font_size=20, color=WHITE).next_to(time_ax, UP, buff=0.1)
        freq_label = Text("Frequency response |f̂(ξ)|", font_size=20, color=WHITE).next_to(freq_ax, UP, buff=0.1)
        
        self.play(Create(time_ax), Create(freq_ax), Write(time_label), Write(freq_label))
        
        # Input signal: sum of two frequencies
        input_signal = time_ax.plot(
            lambda t: np.cos(2 * np.pi * t) + 0.6 * np.cos(2 * np.pi * 3 * t),
            x_range=[0, 4],
            color=YELLOW,
            stroke_width=2
        )
        
        self.play(Create(input_signal))
        
        # Animated probe
        probe_si = 0  # will be updated
        probe_signal = always_redraw(
            lambda: time_ax.plot(
                lambda t, xi=probe_si: np.cos(2 * np.pi * xi * t),
                x_range=[0, 4],
                color=BLUE,
                stroke_width=1.5
            )
        )
        
        self.play(Create(probe_signal))
        
        # Build up frequency response
        freq_points = []
        freqs_to_test = np.linspace(0.1, 4.5, 150)
        
        # Pre-compute actual response
        def compute_response(xi):
            # Numerical integral of product
            ts = np.linspace(0, 4, 500)
            dt = ts[1] - ts[0]
            prod = (np.cos(2 * np.pi * ts) + 0.6 * np.cos(2 * np.pi * 3 * ts)) * np.cos(2 * np.pi * xi * ts)
            return abs(np.trapezoid(prod, ts)) * 0.3  # scale for visibility
        
        response_values = [compute_response(xi) for xi in freqs_to_test]
        
        # Animate the sweep
        moving_dot = Dot(color=RED, radius=0.08)
        
        for i, (xi, resp) in enumerate(zip(freqs_to_test[:60], response_values[:60])):
            probe_si = xi
            new_dot = Dot(freq_ax.c2p(xi, resp), color=RED, radius=0.06)
            
            if i == 0:
                moving_dot.move_to(freq_ax.c2p(xi, resp))
                self.add(moving_dot)
            else:
                self.play(
                    moving_dot.animate.move_to(freq_ax.c2p(xi, resp)),
                    run_time=0.05, rate_func=linear
                )
            
            if i % 3 == 0:
                freq_points.append(new_dot)
                self.add(new_dot)
        
        # Finish quickly
        remaining_freqs = freqs_to_test[60:]
        remaining_resps = response_values[60:]
        
        for xi, resp in zip(remaining_freqs[::2], remaining_resps[::2]):
            dot = Dot(freq_ax.c2p(xi, resp), color=RED, radius=0.06)
            freq_points.append(dot)
        
        self.play(*[FadeIn(p) for p in freq_points[len(freq_points)//2:]], run_time=1)
        
        # Connect with line
        response_line = VMobject()
        points = [freq_ax.c2p(f, r) for f, r in zip(freqs_to_test, response_values)]
        response_line.set_points_as_corners(points)
        response_line.set_color(GREEN)
        response_line.set_stroke(width=2)
        
        self.play(
            FadeOut(probe_signal),
            Create(response_line),
            run_time=2
        )
        
        # Highlight peaks
        peak1 = Dot(freq_ax.c2p(1, response_values[29]), color=YELLOW, radius=0.12)
        peak2 = Dot(freq_ax.c2p(3, response_values[89]), color=YELLOW, radius=0.12)
        
        self.play(FadeIn(peak1), FadeIn(peak2))
        
        reveal = Text("Peaks at f = 1 Hz and f = 3 Hz!", font_size=26, color=YELLOW).shift(RIGHT * 3.5)
        self.play(Write(reveal))
        self.wait(1.5)
        
        all_objs = [demo_title, time_ax, freq_ax, time_label, freq_label, 
                   input_signal, moving_dot] + freq_points + [response_line, peak1, peak2, reveal]
        self.play(*[FadeOut(obj) for obj in all_objs])
        self.clear()

    def scene6_frequency_domain(self):
        # Title
        title = Text("The Frequency Domain", font_size=40, color=BLUE).shift(UP * 3.2)
        self.play(Write(title))
        
        # Side by side: time and frequency
        time_ax = Axes(
            x_range=[0, 4, 1],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=2.5,
            axis_config={"color": WHITE},
        ).shift(LEFT * 3 + UP * 0.3)
        
        freq_ax = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 2.5, 1],
            x_length=5,
            y_length=2.5,
            axis_config={"color": WHITE},
        ).shift(RIGHT * 3 + UP * 0.3)
        
        time_title = Text("Time Domain", font_size=24, color=YELLOW).next_to(time_ax, UP, buff=0.2)
        freq_title = Text("Frequency Domain", font_size=24, color=GREEN).next_to(freq_ax, UP, buff=0.2)
        
        arrow = Arrow(LEFT * 0.8, RIGHT * 0.8, buff=0.1, color=WHITE)
        arrow_label = MathTex("\\mathcal{F}", font_size=36, color=WHITE).next_to(arrow, UP, buff=0.1)
        
        self.play(
            Create(time_ax),
            Create(freq_ax),
            Write(time_title),
            Write(freq_title),
            Write(arrow),
            Write(arrow_label)
        )
        
        # Draw signal in time domain
        time_signal = time_ax.plot(
            lambda t: np.cos(2 * np.pi * t) + 0.7 * np.cos(2 * np.pi * 2.5 * t),
            x_range=[0, 4],
            color=YELLOW,
            stroke_width=2.5
        )
        
        self.play(Create(time_signal))
        self.wait(0.5)
        
        # Transform to frequency domain (animate bars growing)
        freq_bars = VGroup()
        bar1 = Rectangle(height=1.8, width=0.3, fill_color=GREEN, fill_opacity=0.7, stroke_color=GREEN).move_to(freq_ax.c2p(1, 0.9))
        bar2 = Rectangle(height=1.2, width=0.3, fill_color=GREEN, fill_opacity=0.7, stroke_color=GREEN).move_to(freq_ax.c2p(2.5, 0.6))
        
        self.play(
            GrowFromEdge(bar1, DOWN),
            GrowFromEdge(bar2, DOWN),
            run_time=2
        )
        
        # Labels for frequency components
        label1 = MathTex("1\\text{ Hz}", font_size=20, color=GREEN).next_to(bar1, DOWN, buff=0.1)
        label2 = MathTex("2.5\\text{ Hz}", font_size=20, color=GREEN).next_to(bar2, DOWN, buff=0.1)
        amp1 = MathTex("1.0", font_size=20, color=WHITE).next_to(bar1, UP, buff=0.1)
        amp2 = MathTex("0.7", font_size=20, color=WHITE).next_to(bar2, UP, buff=0.1)
        
        self.play(Write(label1), Write(label2), Write(amp1), Write(amp2))
        
        # Show phase information too
        phase_box = Text("Phase also stored in f̂(ξ)\n(complex number!)", font_size=22, color=BLUE).shift(DOWN * 3)
        self.play(Write(phase_box))
        self.wait(1)
        
        # Reveal: two representations of SAME information
        self.wait(0.5)
        same_info = Text("Same signal, different view", font_size=28, color=RED).shift(DOWN * 2.5)
        self.play(Write(same_info))
        self.wait(1.5)
        
        all_objs = [title, time_ax, freq_ax, time_title, freq_title, arrow, arrow_label,
                   time_signal, bar1, bar2, label1, label2, amp1, amp2, phase_box, same_info]
        self.play(*[FadeOut(obj) for obj in all_objs])
        self.clear()

    def scene7_inverse_transform(self):
        # Title
        title = Text("Reconstruction: The Inverse Fourier Transform", font_size=38, color=BLUE).shift(UP * 3.2)
        self.play(Write(title))
        
        # Forward and inverse formulas
        forward = MathTex(
            "\\hat{f}(\\xi) = \\int f(t) e^{-2\\pi i \\xi t} dt",
            font_size=30,
            color=GREEN
        ).shift(UP * 1.8)
        
        inverse = MathTex(
            "f(t) = \\int \\hat{f}(\\xi) e^{2\\pi i \\xi t} d\\xi",
            font_size=30,
            color=YELLOW
        ).shift(UP * 1)
        
        self.play(Write(forward))
        self.wait(0.5)
        self.play(Write(inverse))
        self.wait(0.5)
        
        # Highlight symmetry
        self.play(
            forward[0][9:12].animate.set_color(BLUE),  # e^-...
            inverse[0][9:12].animate.set_color(BLUE),   # e^+...
        )
        
        note = Text("Sign flip in exponent = forward vs inverse", font_size=24, color=BLUE).next_to(inverse, DOWN, buff=0.4)
        self.play(Write(note))
        self.wait(1)
        
        self.play(FadeOut(forward), FadeOut(inverse), FadeOut(note))
        
        # Visual reconstruction demo
        demo_title = Text("Reconstructing from frequency peaks", font_size=28, color=WHITE).shift(UP * 2.5)
        self.play(Write(demo_title))
        
        # Show partial sums building up
        ax = Axes(
            x_range=[0, 4, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=4,
            axis_config={"color": WHITE},
        ).shift(DOWN * 0.3)
        
        self.play(Create(ax))
        
        # Start with one component
        s1 = ax.plot(
            lambda t: np.cos(2 * np.pi * t),
            x_range=[0, 4],
            color=RED,
            stroke_width=2
        )
        label1 = MathTex("\\cos(2\\pi t)", font_size=22, color=RED).shift(UP * 3 + LEFT * 3)
        
        self.play(Create(s1), Write(label1))
        self.wait(0.5)
        
        # Add second
        s2 = ax.plot(
            lambda t: np.cos(2 * np.pi * t) + 0.5 * np.cos(2 * np.pi * 3 * t),
            x_range=[0, 4],
            color=ORANGE,
            stroke_width=2
        )
        label2 = MathTex("+ 0.5\\cos(2\\pi \\cdot 3t)", font_size=22, color=ORANGE).next_to(label1, RIGHT, buff=0.3)
        
        self.play(
            Transform(s1, s2),
            Write(label2)
        )
        self.wait(0.5)
        
        # Add third
        s3 = ax.plot(
            lambda t: np.cos(2 * np.pi * t) + 0.5 * np.cos(2 * np.pi * 3 * t) + 0.3 * np.cos(2 * np.pi * 5 * t),
            x_range=[0, 4],
            color=YELLOW,
            stroke_width=2.5
        )
        label3 = MathTex("+ 0.3\\cos(2\\pi \\cdot 5t)", font_size=22, color=YELLOW).next_to(label2, RIGHT, buff=0.3)
        
        self.play(
            Transform(s1, s3),
            Write(label3)
        )
        
        # More components = better approximation
        more = Text("More frequencies → better approximation", font_size=24, color=GREEN).shift(DOWN * 3)
        self.play(Write(more))
        self.wait(1)
        
        # Exactly invertible!
        exact = Text("Fourier Transform is perfectly invertible!", font_size=26, color=RED).next_to(more, DOWN, buff=0.2)
        self.play(Write(exact))
        self.wait(1.5)
        
        all_objs = [title, demo_title, ax, s1, label1, label2, label3, more, exact]
        self.play(*[FadeOut(obj) for obj in all_objs])
        self.clear()

    def scene8_summary(self):
        # Title
        title = Text("Fourier Transform: Summary", font_size=44, color=BLUE).shift(UP * 3.2)
        self.play(Write(title))
        
        # Key points as numbered list
        points = VGroup()
        
        p1 = Text("1. Any signal can be decomposed into sinusoids", font_size=26, color=YELLOW)
        p2 = Text("2. The FT measures similarity with probe frequencies", font_size=26, color=GREEN)
        p3 = Text("3. Result: frequency domain representation f̂(ξ)", font_size=26, color=BLUE)
        p4 = Text("4. The inverse FT perfectly reconstructs the signal", font_size=26, color=RED)
        p5 = Text("5. Applications: audio, image compression, MRI, solving PDEs", font_size=26, color=WHITE)
        
        all_points = [p1, p2, p3, p4, p5]
        for i, p in enumerate(all_points):
            p.shift(UP * (1.5 - i * 0.9))
            points.add(p)
        
        for p in all_points:
            self.play(Write(p), run_time=1.2)
            self.wait(0.3)
        
        self.wait(0.5)
        
        # Final formula
        final_formula = MathTex(
            "\\hat{f}(\\xi) = \\int_{-\\infty}^{\\infty} f(t) e^{-2\\pi i \\xi t} dt",
            font_size=40,
            color=YELLOW
        ).shift(DOWN * 2.5)
        
        box = SurroundingRectangle(final_formula, buff=0.3, color=YELLOW)
        
        self.play(Write(final_formula))
        self.play(Create(box))
        
        # Pulse effect
        self.play(
            box.animate.set_color(WHITE),
            rate_func=there_and_back,
            run_time=1.5
        )
        
        self.wait(2)
        
        # Credits
        thanks = Text("Now you know the Fourier Transform!", font_size=32, color=GREEN).shift(UP * 3.5)
        self.play(
            FadeOut(title),
            Write(thanks),
            *[p.animate.set_opacity(0.3) for p in all_points],
            final_formula.animate.set_opacity(0.3),
            box.animate.set_opacity(0.3)
        )
        
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()
