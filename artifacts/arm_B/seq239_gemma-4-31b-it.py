from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # --- STEP 1: Static Source (Basic Waveform) ---
        # Goal: Establish what a resting wave source looks like.
        title1 = Text("1. Stationary Source", font_size=36).to_edge(UP)
        source = Dot(color=BLUE).shift(ORIGIN)
        source_label = Text("Source", font_size=24).next_to(source, DOWN)
        
        waves = VGroup()
        
        def create_wave(radius):
            return Circle(radius=radius, color=WHITE).set_stroke(opacity=0.6)

        self.add(title1, source, source_label)
        
        # Animate expanding rings to show constant frequency/wavelength
        for r in range(1, 6):
            wave = create_wave(r * 0.5)
            self.play(Create(wave), run_time=0.5)
            waves.add(wave)
        
        self.wait(1)
        self.play(FadeOut(title1), FadeOut(source), FadeOut(source_label), FadeOut(waves))
        self.clear()

        # --- STEP 2: The Concept of Wavelength ---
        # Goal: Define wavelength as the distance between crests.
        title2 = Text("2. Defining Wavelength (λ)", font_size=36).to_edge(UP)
        
        # Two static crests to measure
        c1 = Circle(radius=2, color=WHITE)
        c2 = Circle(radius=3, color=WHITE)
        
        # Measuring line
        line = Line(start=[2, 0, 0], end=[3, 0, 0], color=YELLOW)
        label_lambda = MathTex(r"\lambda", color=YELLOW).next_to(line, UP, buff=0.1)
        
        self.add(title2)
        self.play(Create(c1), Create(c2))
        self.play(Create(line), Write(label_lambda))
        self.play(Indicate(line))
        
        self.wait(1)
        self.play(FadeOut(title2), FadeOut(c1), FadeOut(c2), FadeOut(line), FadeOut(label_lambda))
        self.clear()

        # --- STEP 3: Source Moving Forward (Compression) ---
        # Goal: Show that moving towards the waves bunches them up.
        title3 = Text("3. Source Moving Forward", font_size=36).to_edge(UP)
        
        moving_source = Dot(color=BLUE)
        source_text = Text("Source", font_size=20).next_to(moving_source, DOWN)
        source_group = VGroup(moving_source, source_text)
        
        wave_group = VGroup()
        
        self.add(title3)
        self.add(source_group)
        
        # Animate source moving right while emitting waves
        for i in range(10):
            # Position of source at time of emission
            curr_pos = moving_source.get_center()
            # Create wave centered at emission point
            wave = Circle(radius=0, color=WHITE).move_to(curr_pos)
            
            self.add(wave)
            # Move source forward and expand the wave simultaneously
            self.play(
                moving_source.animate.shift(RIGHT * 0.4),
                source_text.animate.shift(RIGHT * 0.4),
                wave.animate.scale(10), # Expand wave
                run_time=0.4,
                rate_func=linear
            )
            wave_group.add(wave)

        self.wait(1)
        self.play(FadeOut(title3), FadeOut(source_group), FadeOut(wave_group))
        self.clear()

        # --- STEP 4: Frequency Shift (High Pitch) ---
        # Goal: Compare compressed waves (front) vs stretched waves (back).
        title4 = Text("4. Apparent Frequency Shift", font_size=36).to_edge(UP)
        
        # Represent the state after movement
        # Bunched waves in front
        front_waves = VGroup(*[Circle(radius=r*0.4, color=BLUE_A).shift(RIGHT*1) for r in range(1, 5)])
        # Stretched waves behind
        back_waves = VGroup(*[Circle(radius=r*0.8, color=RED_A).shift(LEFT*1) for r in range(1, 4)])
        
        label_high = Text("Higher Frequency (Higher Pitch)", color=BLUE_A, font_size=24).shift(RIGHT*3 + UP*1)
        label_low = Text("Lower Frequency (Lower Pitch)", color=RED_A, font_size=24).shift(LEFT*3 + UP*1)
        
        self.add(title4)
        self.play(FadeIn(front_waves), FadeIn(back_waves))
        self.play(Write(label_high), Write(label_low))
        self.play(Indicate(front_waves), Indicate(back_waves))
        
        self.wait(2)
        self.play(FadeOut(title4), FadeOut(front_waves), FadeOut(back_waves), FadeOut(label_high), FadeOut(label_low))
        self.clear()

        # --- STEP 5: Observer Perspective ---
        # Goal: Show an observer moving toward the source.
        title5 = Text("5. Observer Moving Toward Source", font_size=36).to_edge(UP)
        
        source_dot = Dot(color=BLUE).shift(LEFT * 3)
        observer = Dot(color=YELLOW).shift(RIGHT * 3)
        obs_label = Text("Observer", font_size=20).next_to(observer, DOWN)
        
        # Constant wave emission from source
        waves_group = VGroup()
        
        self.add(title5, source_dot, observer, obs_label)
        
        # Animate observer moving left while waves travel right
        for i in range(6):
            wave = Circle(radius=0, color=WHITE).move_to(source_dot.get_center())
            self.add(wave)
            self.play(
                observer.animate.shift(LEFT * 0.6),
                obs_label.animate.shift(LEFT * 0.6),
                wave.animate.scale(15),
                run_time=0.6,
                rate_func=linear
            )
            waves_group.add(wave)
            
        self.wait(1)
        self.play(FadeOut(title5), FadeOut(source_dot), FadeOut(observer), FadeOut(obs_label), FadeOut(waves_group))
        self.clear()

        # --- STEP 6: Summary Conclusion ---
        # Goal: Final conceptual formula/summary.
        title6 = Text("The Doppler Effect", font_size=48).to_edge(UP)
        
        summary_text = VGroup(
            Text("Moving Toward: Frequency Increases ↑", color=BLUE),
            Text("Moving Away: Frequency Decreases ↓", color=RED),
        ).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        
        formula = MathTex(r"f' = \left( \frac{v \pm v_{obs}}{v \mp v_{source}} \right) f").shift(DOWN * 2.5)
        
        self.add(title6)
        self.play(Write(summary_text))
        self.play(Write(formula))
        self.play(Circumscribe(formula, color=YELLOW))
        
        self.wait(3)
