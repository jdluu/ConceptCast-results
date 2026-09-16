from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # STEP 1: Stationary Source - Basics of Frequency
        self.step_stationary_source()
        self.clear()

        # STEP 2: Stationary Source - Adding an Observer
        self.step_observer_concept()
        self.clear()

        # STEP 3: Moving Source - Compression in front
        self.step_moving_source_compression()
        self.clear()

        # STEP 4: Moving Source - Rarefaction behind
        self.step_moving_source_expansion()
        self.clear()

        # STEP 5: Relative Motion Summary
        self.step_final_summary()
        self.clear()

    def step_stationary_source(self):
        title = Text("1. Stationary Source", color=BLUE).to_edge(UP)
        desc = Text("Waves radiate evenly in all directions.", font_size=24).next_to(title, DOWN)
        self.play(Write(title), Write(desc))

        source = Dot(color=RED)
        source_label = Text("Source", font_size=20).next_to(source, DOWN)
        self.play(Create(source), Write(source_label))

        waves = VGroup()
        for i in range(5):
            circle = Circle(radius=0, color=BLUE_A).move_to(source)
            waves.add(circle)

        for wave in waves:
            self.play(
                wave.animate.set_width(6).set_height(6).set_stroke(opacity=0),
                run_time=1.5,
                rate_func=linear
            )
            # Fade out as they expand
            self.play(wave.animate.set_stroke(opacity=0.2), run_time=0.1)
        
        self.wait(1)
        self.play(FadeOut(title), FadeOut(desc), FadeOut(source), FadeOut(source_label), FadeOut(waves))

    def step_observer_concept(self):
        title = Text("2. The Observer", color=BLUE).to_edge(UP)
        self.play(Write(title))

        source = Dot(color=RED).move_to(LEFT * 3)
        observer = Dot(color=GREEN).move_to(RIGHT * 3)
        obs_label = Text("Observer", font_size=20).next_to(observer, DOWN)
        
        self.play(Create(source), Create(observer), Write(obs_label))

        # Show fixed distance wavefronts
        waves = VGroup()
        for r in range(1, 7):
            c = Circle(radius=r, color=BLUE_B).move_to(source)
            waves.add(c)
        
        self.play(Create(waves), run_time=2)
        
        dist_line = Line(source.get_center(), observer.get_center(), color=WHITE)
        self.play(Create(dist_line))
        
        self.wait(1)
        self.play(FadeOut(title), FadeOut(source), FadeOut(observer), FadeOut(obs_label), FadeOut(waves), FadeOut(dist_line))

    def step_moving_source_compression(self):
        title = Text("3. Moving Source: Compression", color=BLUE).to_edge(UP)
        self.play(Write(title))

        source = Dot(color=RED).move_to(LEFT * 4)
        obs = Dot(color=GREEN).move_to(RIGHT * 4)
        obs_label = Text("Observer", font_size=20).next_to(obs, DOWN)
        
        self.play(Create(source), Create(obs), Write(obs_label))

        # Animation loop to show wavefronts bunching up in front
        wavefronts = VGroup()
        
        def create_wave():
            return Circle(radius=0.1, color=BLUE_B).move_to(source.get_center())

        for i in range(8):
            # Move source forward
            self.play(source.animate.shift(RIGHT * 0.5), run_time=0.5)
            
            # Create a wave at the current source position
            w = create_wave()
            wavefronts.add(w)
            self.add(w)
            
            # Animate existing waves expanding
            self.play(
                *[wave.animate.scale(10).set_stroke(opacity=0.3) for wave in wavefronts],
                run_time=0.5,
                rate_func=linear
            )

        # Highlight the bunched area
        rect = Rectangle(width=2, height=4, color=YELLOW).move_to(source.get_center())
        label = Text("Higher Frequency", font_size=24, color=YELLOW).next_to(rect, UP)
        self.play(Create(rect), Write(label))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(source), FadeOut(obs), FadeOut(obs_label), FadeOut(wavefronts), FadeOut(rect), FadeOut(label))

    def step_moving_source_expansion(self):
        title = Text("4. Moving Source: Expansion", color=BLUE).to_edge(UP)
        self.play(Write(title))

        source = Dot(color=RED).move_to(ORIGIN)
        obs = Dot(color=GREEN).move_to(LEFT * 5)
        obs_label = Text("Observer", font_size=20).next_to(obs, DOWN)
        
        self.play(Create(source), Create(obs), Write(obs_label))

        wavefronts = VGroup()
        
        for i in range(8):
            # Move source AWAY from observer
            self.play(source.animate.shift(RIGHT * 0.6), run_time=0.5)
            
            w = Circle(radius=0.1, color=BLUE_B).move_to(source.get_center())
            wavefronts.add(w)
            self.add(w)
            
            self.play(
                *[wave.animate.scale(10).set_stroke(opacity=0.3) for wave in wavefronts],
                run_time=0.5,
                rate_func=linear
            )

        # Highlight the stretched area
        rect = Rectangle(width=3, height=4, color=RED_A).move_to(LEFT * 3)
        label = Text("Lower Frequency", font_size=24, color=RED_A).next_to(rect, UP)
        self.play(Create(rect), Write(label))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(source), FadeOut(obs), FadeOut(obs_label), FadeOut(wavefronts), FadeOut(rect), FadeOut(label))

    def step_final_summary(self):
        title = Text("Doppler Effect Summary", color=BLUE).to_edge(UP)
        self.play(Write(title))

        # Comparison table/visuals
        left_text = Text("Source moving TOWARDS\nObserver $\\rightarrow$ Higher Pitch", 
                         font_size=30, color=BLUE_A).shift(LEFT * 3 + DOWN * 1)
        right_text = Text("Source moving AWAY\nObserver $\\rightarrow$ Lower Pitch", 
                          font_size=30, color=RED_A).shift(RIGHT * 3 + DOWN * 1)

        self.play(Write(left_text))
        self.play(Write(right_text))

        # Animation of a wave shifting frequency
        wave_line = Line(LEFT * 4, RIGHT * 4, color=GRAY).shift(DOWN * 3)
        self.play(Create(wave_line))

        # High frequency sine wave
        high_f = FunctionGraph(lambda x: 0.5 * np.sin(5 * x), x_range=[-4, 4], color=BLUE)
        self.play(Create(high_f))
        self.play(high_f.animate.shift(UP * 0.5), run_time=1)
        
        # Low frequency sine wave
        low_f = FunctionGraph(lambda x: 0.5 * np.sin(1.5 * x), x_range=[-4, 4], color=RED)
        self.play(Create(low_f))
        
        final_note = Text("$\Delta f = \frac{\Delta v}{v} f_0$", font_size=40).next_to(low_f, DOWN, buff=1)
        self.play(Write(final_note))
        
        self.wait(3)
        self.play(FadeOut(title), FadeOut(left_text), FadeOut(right_text), 
                  FadeOut(wave_line), FadeOut(high_f), FadeOut(low_f), FadeOut(final_note))
