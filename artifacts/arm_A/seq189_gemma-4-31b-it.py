from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # --- STEP 1: Static Source Concept ---
        # Goal: Introduce the concept of frequency and wavelength
        title1 = Text("1. Static Source", color=WHITE).to_edge(UP)
        self.add(title1)
        
        source = Dot(color=RED).shift(LEFT * 3)
        source_label = Text("Source", font_size=24).next_to(source, DOWN)
        
        # Create wave crests
        waves = VGroup()
        for i in range(5):
            circle = Circle(radius=0, color=BLUE).move_to(source)
            waves.add(circle)
            
        self.play(Create(source), Write(source_label))
        
        # Animate expanding waves
        for wave in waves:
            self.play(
                wave.animate.scale(4), 
                run_time=1.5, 
                rate_func=linear
            )
            # Small delay between pulses to show frequency
            self.wait(0.2)
        
        self.wait(1)
        self.play(FadeOut(title1), FadeOut(source), FadeOut(source_label), FadeOut(waves))
        self.clear()

        # --- STEP 2: The Observer ---
        # Goal: Introduce the observer and the concept of "relative" movement
        title2 = Text("2. The Observer", color=WHITE).to_edge(UP)
        self.add(title2)
        
        source = Dot(color=RED).shift(LEFT * 3)
        observer = Dot(color=GREEN).shift(RIGHT * 3)
        obs_label = Text("Observer", font_size=24).next_to(observer, DOWN)
        
        self.play(Create(source), Create(observer), Write(obs_label))
        
        # Show distance
        dist_line = Line(source.get_center(), observer.get_center(), color=GRAY)
        dist_text = Text("Distance (d)", font_size=20).next_to(dist_line, UP)
        
        self.play(Create(dist_line), Write(dist_text))
        self.wait(1)
        
        self.play(FadeOut(title2), FadeOut(source), FadeOut(observer), 
                  FadeOut(obs_label), FadeOut(dist_line), FadeOut(dist_text))
        self.clear()

        # --- STEP 3: Source Moving Toward Observer ---
        # Goal: Visualizing wave bunching (Blue Shift)
        title3 = Text("3. Source Moving Toward Observer", color=WHITE).to_edge(UP)
        self.add(title3)
        
        source = Dot(color=RED).shift(LEFT * 4)
        observer = Dot(color=GREEN).shift(RIGHT * 4)
        
        # Track for the source
        track = Line(LEFT * 4, RIGHT * 4, color=GRAY_A)
        
        self.play(Create(source), Create(observer), Create(track))
        
        # Custom animation for waves while moving
        waves = VGroup()
        
        # We animate the source moving and emitting waves simultaneously
        # Use a loop to create pulses at specific time intervals
        for i in range(6):
            # Create a wave at the current source position
            wave = Circle(radius=0, color=BLUE).move_to(source.get_center())
            waves.add(wave)
            
            # Move source and expand previous waves
            self.play(
                source.animate.shift(RIGHT * 1),
                *[w.animate.scale(1.5) for w in waves if w != wave],
                wave.animate.scale(0.1),
                run_time=0.6
            )
            # The wave "grows" from the center of where it was emitted
            self.play(
                *[w.animate.scale(1.2) for w in waves],
                run_time=0.4
            )

        # Highlight the "compressed" region
        rect = Rectangle(width=3, height=2, color=YELLOW).move_to(source.get_center())
        comp_text = Text("Compressed Waves\n(Higher Frequency)", font_size=24).next_to(rect, UP)
        
        self.play(Create(rect), Write(comp_text))
        self.wait(2)
        
        self.play(FadeOut(title3), FadeOut(source), FadeOut(observer), 
                  FadeOut(track), FadeOut(waves), FadeOut(rect), FadeOut(comp_text))
        self.clear()

        # --- STEP 4: Source Moving Away ---
        # Goal: Visualizing wave stretching (Red Shift)
        title4 = Text("4. Source Moving Away", color=WHITE).to_edge(UP)
        self.add(title4)
        
        source = Dot(color=RED).shift(LEFT * 1)
        observer = Dot(color=GREEN).shift(LEFT * 4)
        track = Line(LEFT * 4, RIGHT * 4, color=GRAY_A)
        
        self.play(Create(source), Create(observer), Create(track))
        
        waves = VGroup()
        for i in range(6):
            wave = Circle(radius=0, color=BLUE).move_to(source.get_center())
            waves.add(wave)
            self.play(
                source.animate.shift(RIGHT * 1),
                *[w.animate.scale(1.5) for w in waves if w != wave],
                wave.animate.scale(0.1),
                run_time=0.6
            )
            self.play(
                *[w.animate.scale(1.2) for w in waves],
                run_time=0.4
            )

        rect = Rectangle(width=3, height=2, color=YELLOW).move_to(observer.get_center())
        stretch_text = Text("Stretched Waves\n(Lower Frequency)", font_size=24).next_to(rect, UP)
        
        self.play(Create(rect), Write(stretch_text))
        self.wait(2)
        
        self.play(FadeOut(title4), FadeOut(source), FadeOut(observer), 
                  FadeOut(track), FadeOut(waves), FadeOut(rect), FadeOut(stretch_text))
        self.clear()

        # --- STEP 5: Summary and Equation ---
        # Goal: Synthesize knowledge into the formal concept
        title5 = Text("The Doppler Effect Summary", color=WHITE).to_edge(UP)
        self.add(title5)
        
        # Diagram representation
        left_group = VGroup(
            Dot(color=RED), 
            Arrow(LEFT, RIGHT, color=WHITE),
            Text("Approaching $\\rightarrow$ Higher Pitch", font_size=30)
        ).arrange(DOWN).shift(LEFT * 3)
        
        right_group = VGroup(
            Dot(color=RED), 
            Arrow(RIGHT, LEFT, color=WHITE),
            Text("Receding $\\leftarrow$ Lower Pitch", font_size=30)
        ).arrange(DOWN).shift(RIGHT * 3)
        
        # Formula
        formula = MathTex(
            r"f = \left( \frac{v \pm v_{obs}}{v \mp v_{src}} \right) f_0", 
            color=YELLOW
        ).shift(DOWN * 2)
        
        desc = Text("Frequency shifts based on relative velocity", font_size=24).next_to(formula, DOWN)
        
        self.play(FadeIn(left_group), FadeIn(right_group))
        self.play(Write(formula))
        self.play(Write(desc))
        
        self.wait(3)
        self.play(FadeOut(title5), FadeOut(left_group), FadeOut(right_group), 
                  FadeOut(formula), FadeOut(desc))
