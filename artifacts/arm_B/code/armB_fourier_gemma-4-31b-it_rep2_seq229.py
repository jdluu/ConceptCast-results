from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # --- STEP 1: Introduction to the Signal ---
        title = Text("The Fourier Transform", color=WHITE).scale(1.2)
        subtitle = Text("Decomposing a signal into frequencies", color=GRAY).scale(0.8).next_to(title, DOWN)
        
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # --- STEP 2: Defining the Base Sine Waves ---
        axes = Axes(x_range=[0, 10, 1], y_range=[-1.5, 1.5, 1], axis_config={"include_tip": False})
        labels = axes.get_axis_labels(x_label="t", y_label="A")
        
        # Wave 1: Low Frequency
        wave1 = axes.plot(lambda x: np.sin(x), color=BLUE)
        label1 = Text("Low Frequency (f1)", color=BLUE).scale(0.6).to_edge(UP).shift(LEFT*3)
        
        # Wave 2: High Frequency
        wave2 = axes.plot(lambda x: np.sin(4 * x), color=RED)
        label2 = Text("High Frequency (f2)", color=RED).scale(0.6).to_edge(UP).shift(RIGHT*3)

        self.play(Create(axes), Write(labels))
        self.play(Create(wave1), Write(label1), run_time=2)
        self.wait(1)
        self.play(Create(wave2), Write(label2), run_time=2)
        self.wait(2)
        self.play(FadeOut(wave1), FadeOut(wave2), FadeOut(label1), FadeOut(label2))
        self.clear()

        # --- STEP 3: Superposition (The Complex Signal) ---
        axes = Axes(x_range=[0, 10, 1], y_range=[-2.5, 2.5, 1], axis_config={"include_tip": False})
        
        w1 = axes.plot(lambda x: np.sin(x), color=BLUE)
        w2 = axes.plot(lambda x: np.sin(4 * x), color=RED)
        combined = axes.plot(lambda x: np.sin(x) + np.sin(4 * x), color=YELLOW)
        
        txt_sum = Text("Complex Signal = f1 + f2", color=YELLOW).to_edge(UP)

        self.play(Create(axes))
        self.play(Create(w1), run_time=1)
        self.play(Create(w2), run_time=1)
        self.play(Transform(w1.copy(), combined), Transform(w2.copy(), combined), run_time=1) 
        # Simplified visual transition to combined wave
        self.play(FadeOut(w1), FadeOut(w2), Create(combined), Write(txt_sum))
        self.wait(2)
        self.play(FadeOut(combined), FadeOut(txt_sum), FadeOut(axes))
        self.clear()

        # --- STEP 4: The "Winding" Intuition (The Circle) ---
        circle = Circle(radius=2, color=WHITE)
        dot = Dot(color=YELLOW).move_to(circle.point_at_angle(0))
        
        # The concept of winding a signal around a circle
        winding_text = Text("Winding the signal around a circle", color=WHITE).to_edge(UP)
        
        # A path that mimics a winding movement
        def update_dot(m, dt):
            m.shift(np.array([0, 0, 0])) # Placeholder for complex logic
            
        self.play(Create(circle), Write(winding_text))
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        self.play(MoveAlongPath(dot, circle), run_time=1, rate_func=linear)
        
        self.wait(1)
        self.play(FadeOut(circle), FadeOut(dot), FadeOut(winding_text))
        self.clear()

        # --- STEP 5: The Center of Mass Concept ---
        # This visualizes the "spike" when the winding frequency matches the signal frequency
        axes_f = Axes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], axis_config={"include_tip": False})
        center_dot = Dot(color=YELLOW)
        
        # Simulate a shifting center of mass
        self.play(Create(axes_f))
        
        # "Off-balance" case (frequency mismatch)
        off_circle = Circle(radius=0.5, color=GRAY).shift(UP*0.5)
        off_dot = Dot(color=RED).move_to(axes_f.c2p(0,0))
        
        txt_mismatch = Text("Frequency Mismatch: Center is near origin", color=GRAY).to_edge(UP)
        self.play(Create(off_circle), Write(txt_mismatch))
        self.play(off_dot.animate.move_to(axes_f.c2p(0.1, 0.1)))
        self.wait(1)
        self.play(FadeOut(off_circle), FadeOut(off_dot), FadeOut(txt_mismatch))

        # "Matched" case (frequency matches)
        match_circle = Circle(radius=0.5, color=BLUE).shift(RIGHT*1.5)
        match_dot = Dot(color=YELLOW).move_to(axes_f.c2p(1.5, 0))
        
        txt_match = Text("Frequency Match: Center of mass shifts!", color=YELLOW).to_edge(UP)
        self.play(Create(match_circle), Write(txt_match))
        self.play(match_dot.animate.move_to(axes_f.c2p(1.5, 0)), run_time=1)
        self.wait(2)
        self.play(FadeOut(match_circle), FadeOut(match_dot), FadeOut(txt_match), FadeOut(axes_f))
        self.clear()

        # --- STEP 6: The Frequency Domain (The Result) ---
        axes_freq = Axes(
            x_range=[0, 5, 1], 
            y_range=[0, 1.2, 1], 
            x_axis_config={"include_tip": True}, 
            y_axis_config={"include_tip": True}
        )
        labels_freq = axes_freq.get_axis_labels(x_label="Frequency", y_label="Magnitude")
        
        # Two spikes corresponding to our original f1 and f2
        spike1 = Line(axes_freq.c2p(1, 0), axes_freq.c2p(1, 1), color=BLUE, stroke_width=6)
        spike2 = Line(axes_freq.c2p(4, 0), axes_freq.c2p(4, 1), color=RED, stroke_width=6)
        
        final_text = Text("The Spectrum: Only the constituent frequencies remain", color=WHITE).to_edge(UP)

        self.play(Create(axes_freq), Write(labels_freq))
        self.play(Create(spike1), run_time=1)
        self.play(Create(spike2), run_time=1)
        self.play(Write(final_text))
        self.wait(3)
        self.play(FadeOut(spike1), FadeOut(spike2), FadeOut(axes_freq), FadeOut(labels_freq), FadeOut(final_text))
        self.clear()

        # --- STEP 7: The Mathematical Formula ---
        formula = MathTex(
            "X(f) = \int_{-\infty}^{\infty} x(t) e^{-i 2\pi f t} dt", 
            color=YELLOW
        ).scale(1.2)
        
        explanation = Text(
            "The integral 'sums' the signal weighted by a complex rotation", 
            color=GRAY, font_size=24
        ).next_to(formula, DOWN, buff=1)

        self.play(Write(formula))
        self.wait(1)
        self.play(FadeIn(explanation))
        self.wait(3)
        self.play(FadeOut(formula), FadeOut(explanation))
        
        # Final Conclusion
        conclusion = Text("Fourier Transform Complete", color=BLUE).scale(1.5)
        self.play(GrowFromCenter(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion))
