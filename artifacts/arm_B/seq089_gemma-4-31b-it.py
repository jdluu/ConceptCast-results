from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # --- SCENE 1: Introduction to Frequency ---
        # Establishing the baseline concept of wave frequency
        title = Text("The Doppler Effect", font_size=48).to_edge(UP)
        subtitle = Text("Step 1: Understanding Frequency", font_size=32, color=GRAY).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))

        source = Dot(color=BLUE).shift(LEFT * 2)
        source_label = Text("Source", font_size=24).next_to(source, DOWN)
        
        waves = VGroup()
        for i in range(5):
            circle = Circle(radius=0, color=BLUE_A).move_to(source)
            waves.add(circle)

        self.play(FadeIn(source), FadeIn(source_label))
        
        # Animate expanding circles to represent stationary sound waves
        animations = []
        for circle in waves:
            animations.append(circle.animate(run_time=2).set_width(6).set_stroke(opacity=0))
        
        # Sequence of wave pulses
        for anim in animations:
            self.play(anim)
            self.wait(0.2)

        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(source), FadeOut(source_label), FadeOut(waves))
        self.clear()

        # --- SCENE 2: Stationary Observer ---
        # Show that if nothing moves, the distance between peaks is constant
        title = Text("Step 2: Stationary Observer", font_size=36).to_edge(UP)
        self.play(Write(title))

        source = Dot(color=BLUE).shift(LEFT * 3)
        observer = Dot(color=RED).shift(RIGHT * 3)
        obs_label = Text("Observer", font_size=24, color=RED).next_to(observer, DOWN)
        
        self.play(FadeIn(source), FadeIn(observer), FadeIn(obs_label))

        # Create waves that reach the observer
        def create_wave():
            return Circle(radius=0, color=BLUE_B).move_to(source)

        wave_group = VGroup()
        for _ in range(4):
            w = create_wave()
            wave_group.add(w)
            self.play(w.animate(run_time=1.5).set_width(12).set_stroke(opacity=0))
        
        # Highlight the constant wavelength
        line = Line(start=source.get_center(), end=observer.get_center(), color=WHITE, stroke_opacity=0.3)
        self.play(Create(line))
        
        dist_text = Text("Constant wavelength (λ)", font_size=24).next_to(line, UP)
        self.play(Write(dist_text))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(source), FadeOut(observer), FadeOut(obs_label), FadeOut(wave_group), FadeOut(line), FadeOut(dist_text))
        self.clear()

        # --- SCENE 3: Source Moving Toward Observer ---
        # Demonstrating the compression of waves (Higher Pitch)
        title = Text("Step 3: Source Moving Toward Observer", font_size=36).to_edge(UP)
        self.play(Write(title))

        observer = Dot(color=RED).shift(RIGHT * 5)
        obs_label = Text("Observer", font_size=24, color=RED).next_to(observer, DOWN)
        source = Dot(color=BLUE).shift(LEFT * 5)
        src_label = Text("Source", font_size=24, color=BLUE).next_to(source, DOWN)

        self.play(FadeIn(observer), FadeIn(obs_label), FadeIn(source), FadeIn(src_label))

        # Move source while emitting waves
        waves = VGroup()
        # Use a ValueTracker to sync movement and wave emission
        move_time = 4
        
        # Custom animation: source moves right, waves expand from where they were emitted
        def emit_wave(t):
            pos = source.get_center() + RIGHT * (t * 3) # Source moves right
            return Circle(radius=0, color=BLUE_B).move_to(pos)

        # We simulate the moving source by iterating through time
        for t in np.linspace(0, move_time, 8):
            w = emit_wave(t)
            # The wave expands while the source continues to move
            self.add(w)
            self.play(
                w.animate(run_time=0.5).set_width(10).set_stroke(opacity=0), 
                source.animate(run_time=0.5).shift(RIGHT * 0.75),
                run_time=0.5
            )

        # Visual feedback: "Compression"
        comp_text = Text("Waves compress in front\nFrequency increases (Higher Pitch)", 
                         font_size=28, color=YELLOW).shift(UP * 1)
        self.play(Write(comp_text))
        self.wait(3)

        self.play(FadeOut(title), FadeOut(observer), FadeOut(obs_label), FadeOut(source), FadeOut(src_label), FadeOut(comp_text))
        self.clear()

        # --- SCENE 4: Source Moving Away from Observer ---
        # Demonstrating the stretching of waves (Lower Pitch)
        title = Text("Step 4: Source Moving Away", font_size=36).to_edge(UP)
        self.play(Write(title))

        observer = Dot(color=RED).shift(LEFT * 5)
        obs_label = Text("Observer", font_size=24, color=RED).next_to(observer, DOWN)
        source = Dot(color=BLUE).shift(LEFT * 0)
        src_label = Text("Source", font_size=24, color=BLUE).next_to(source, DOWN)

        self.play(FadeIn(observer), FadeIn(obs_label), FadeIn(source), FadeIn(src_label))

        for t in np.linspace(0, 4, 8):
            # Wave emission point
            pos = source.get_center() + RIGHT * (t * 3)
            w = Circle(radius=0, color=BLUE_B).move_to(pos)
            self.add(w)
            self.play(
                w.animate(run_time=0.5).set_width(10).set_stroke(opacity=0), 
                source.animate(run_time=0.5).shift(RIGHT * 0.75),
                run_time=0.5
            )

        stretch_text = Text("Waves stretch behind\nFrequency decreases (Lower Pitch)", 
                            font_size=28, color=YELLOW).shift(UP * 1)
        self.play(Write(stretch_text))
        self.wait(3)

        self.play(FadeOut(title), FadeOut(observer), FadeOut(obs_label), FadeOut(source), FadeOut(src_label), FadeOut(stretch_text))
        self.clear()

        # --- SCENE 5: Summary and Formula ---
        # Final wrap up and mathematical relation
        title = Text("Summary: The Doppler Effect", font_size=42).to_edge(UP)
        self.play(Write(title))

        # Visual Comparison
        approaching = Text("Approaching → Higher f", font_size=30, color=BLUE).shift(UP * 1 + LEFT * 2)
        receding = Text("Receding → Lower f", font_size=30, color=RED).shift(UP * 1 + RIGHT * 2)
        
        self.play(Write(approaching), Write(receding))

        # The general formula (simplified version for sound)
        formula = MathTex(
            r"f' = f \left( \frac{v \pm v_{obs}}{v \mp v_{src}} \right)", 
            font_size=60
        ).shift(DOWN * 1)
        
        formula_label = Text("Apparent Frequency = Original Frequency × Shift Factor", 
                             font_size=24, color=GRAY).next_to(formula, DOWN * 1.5)

        self.play(Write(formula))
        self.play(FadeIn(formula_label))
        
        # Final animation: pulsing effect to symbolize sound
        final_circle = Circle(radius=0, color=WHITE).move_to(formula)
        self.play(final_circle.animate(run_time=1).set_width(12).set_stroke(opacity=0))

        self.wait(4)
