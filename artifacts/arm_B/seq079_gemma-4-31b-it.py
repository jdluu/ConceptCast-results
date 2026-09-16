from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # --- STEP 1: Introduction to a Signal ---
        # Goal: Define what a signal is (time domain)
        title = Text("The Fourier Transform", color=WHITE).scale(1.2)
        subtitle = Text("Decomposing signals into frequencies", color=GRAY).scale(0.8).next_to(title, DOWN)
        
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        axes = Axes(
            x_range=[0, 10, 1], y_range=[-2, 2, 1], 
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": np.arange(0, 11, 2)},
        ).scale(0.8).shift(DOWN*0.5)
        
        labels = axes.get_axis_labels(x_label="t (time)", y_label="f(t)")
        
        # A simple sine wave
        sig1 = axes.plot(lambda x: np.sin(2 * np.pi * 0.5 * x), color=BLUE)
        sig1_label = MathTex("f(t) = \sin(0.5 \cdot 2\pi t)", color=BLUE).next_to(axes, UP)

        self.play(Create(axes), Write(labels))
        self.play(Create(sig1), Write(sig1_label))
        self.wait(2)
        self.play(FadeOut(sig1), FadeOut(sig1_label), FadeOut(axes), FadeOut(labels))

        # --- STEP 2: Superposition (Adding Waves) ---
        # Goal: Show that complex signals are just sums of simple ones
        self.clear()
        axes = Axes(x_range=[0, 10, 1], y_range=[-3, 3, 1], x_axis_config={"include_tip": False}).scale(0.8)
        labels = axes.get_axis_labels(x_label="t", y_label="y")
        
        wave1 = axes.plot(lambda x: np.sin(2 * np.pi * 0.5 * x), color=BLUE)
        wave2 = axes.plot(lambda x: 0.5 * np.sin(2 * np.pi * 2 * x), color=GREEN)
        combined = axes.plot(lambda x: np.sin(2 * np.pi * 0.5 * x) + 0.5 * np.sin(2 * np.pi * 2 * x), color=YELLOW)
        
        l1 = MathTex("0.5\text{ Hz}", color=BLUE).next_to(wave1, UP, buff=0.1).shift(RIGHT*2)
        l2 = MathTex("2.0\text{ Hz}", color=GREEN).next_to(wave2, UP, buff=0.1).shift(RIGHT*2)
        l_comb = MathTex("Composite Signal", color=YELLOW).next_to(combined, UP)

        self.play(Create(axes), Write(labels))
        self.play(Create(wave1), Write(l1))
        self.wait(1)
        self.play(Create(wave2), Write(l2))
        self.wait(1)
        self.play(ReplacementTransform(VGroup(wave1, wave2), combined), 
                  ReplacementTransform(VGroup(l1, l2), l_comb))
        self.wait(2)
        self.play(FadeOut(combined), FadeOut(l_comb), FadeOut(axes), FadeOut(labels))

        # --- STEP 3: The Concept of Winding ---
        # Goal: Explain the "winding" mechanism (complex plane)
        self.clear()
        plane = ComplexPlane().add_coordinates()
        circle = Circle(radius=1, color=WHITE)
        dot = Dot(color=RED)
        
        # Animation of a point moving around the circle
        def update_dot(m, dt):
            t = self.time # internal clock
            m.shift(np.array([np.cos(2*np.pi*0.5*t), np.sin(2*np.pi*0.5*t), 0]) * 0.1) # simple mock logic
        
        # We'll use a ValueTracker for precise control
        t_tracker = ValueTracker(0)
        dot.add_updater(lambda m: m.move_to([np.cos(2*np.pi*0.5*t_tracker.get_value()), 
                                            np.sin(2*np.pi*0.5*t_tracker.get_value()), 0]))
        
        winding_text = Text("Winding the signal around a circle", font_size=24).to_edge(UP)
        
        self.play(Write(winding_text), Create(plane), Create(circle))
        self.add(dot)
        self.play(t_tracker.animate.set_value(2), run_time=2, rate_func=linear)
        self.play(t_tracker.animate.set_value(4), run_time=2, rate_func=linear)
        
        self.play(FadeOut(dot), FadeOut(circle), FadeOut(plane), FadeOut(winding_text))

        # --- STEP 4: Resonance (The Center of Mass) ---
        # Goal: Explain that if the frequency matches, the center of mass shifts
        self.clear()
        axes_time = Axes(x_range=[0, 10], y_range=[-1, 1]).scale(0.5).shift(LEFT*3)
        axes_freq = Axes(x_range=[0, 5], y_range=[0, 2]).scale(0.5).shift(RIGHT*3)
        
        sig_complex = axes_time.plot(lambda x: np.sin(2*np.pi*0.5*x) + 0.5*np.sin(2*np.pi*2*x), color=YELLOW)
        
        # Represent the "Frequency Domain"
        bar1 = Rectangle(width=0.2, height=1, fill_opacity=1, color=BLUE).move_to(axes_freq.c2p(0.5, 0.5))
        bar2 = Rectangle(width=0.2, height=0.5, fill_opacity=1, color=GREEN).move_to(axes_freq.c2p(2, 0.25))
        
        t_label = Text("Time Domain", font_size=24).next_to(axes_time, UP)
        f_label = Text("Frequency Domain", font_size=24).next_to(axes_freq, UP)

        self.play(Create(axes_time), Create(axes_freq), Write(t_label), Write(f_label))
        self.play(Create(sig_complex))
        self.wait(1)
        
        self.play(FadeIn(bar1), Write(Text("0.5Hz", font_size=18).next_to(bar1, DOWN)))
        self.play(FadeIn(bar2), Write(Text("2.0Hz", font_size=18).next_to(bar2, DOWN)))
        self.wait(2)
        
        self.play(FadeOut(sig_complex), FadeOut(bar1), FadeOut(bar2), FadeOut(axes_time), FadeOut(axes_freq), FadeOut(t_label), FadeOut(f_label))

        # --- STEP 5: The Mathematical Equation ---
        # Goal: Introduce the Integral formula
        formula = MathTex(
            "F(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt",
            color=WHITE
        ).scale(1.2)
        
        # Annotations
        box_f = SurroundingRectangle(formula[0][2:4], color=BLUE) # f(t)
        box_e = SurroundingRectangle(formula[0][4:9], color=GREEN) # e...
        
        desc1 = Text("Signal in Time", font_size=20, color=BLUE).next_to(box_f, DOWN, buff=0.5)
        desc2 = Text("Winding frequency", font_size=20, color=GREEN).next_to(box_e, DOWN, buff=0.5)

        self.play(Write(formula))
        self.wait(1)
        self.play(Create(box_f), Write(desc1))
        self.wait(1)
        self.play(Create(box_e), Write(desc2))
        self.wait(3)
        self.play(FadeOut(formula), FadeOut(box_f), FadeOut(box_e), FadeOut(desc1), FadeOut(desc2))

        # --- STEP 6: Conclusion / Summary ---
        # Goal: Final take-away
        conclusion = VGroup(
            Text("Fourier Transform Summary:", font_size=36),
            Text("Time Domain $\rightarrow$ Frequency Domain", font_size=30),
            Text("Complex waves $\rightarrow$ Simple sine components", font_size=30),
            Text("Used in: MP3, JPEG, Wi-Fi, MRI", font_size=30),
        ).arrange(DOWN, buff=0.5)

        self.play(Write(conclusion[0]))
        for line in conclusion[1:]:
            self.play(Write(line))
            self.wait(1)
            
        self.wait(3)
        self.play(FadeOut(conclusion))
