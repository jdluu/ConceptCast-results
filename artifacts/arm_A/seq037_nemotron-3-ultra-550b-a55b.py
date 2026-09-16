from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Stationary Source ---
        title1 = Text("1. Stationary Source", font_size=48).to_edge(UP)
        source = Dot(color=YELLOW, radius=0.2).move_to(ORIGIN)
        source_label = Text("Source", font_size=24).next_to(source, DOWN)
        
        waves = VGroup()
        for r in np.arange(0.5, 4.0, 0.5):
            circle = Circle(radius=r, color=BLUE, stroke_width=1.5)
            waves.add(circle)
        
        self.play(Write(title1))
        self.play(FadeIn(source), Write(source_label))
        self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.2), run_time=3)
        self.wait(1)
        self.play(FadeOut(title1, source, source_label, waves))
        self.clear()

        # --- Scene 2: Wavefront Propagation ---
        title2 = Text("2. Wavefronts Propagate Outward", font_size=48).to_edge(UP)
        source = Dot(color=YELLOW, radius=0.2).move_to(ORIGIN)
        
        def create_wavefronts():
            group = VGroup()
            for r in np.arange(0.2, 4.0, 0.5):
                circle = Circle(radius=r, color=BLUE, stroke_width=2)
                group.add(circle)
            return group

        wavefronts = create_wavefronts()
        
        self.play(Write(title2), FadeIn(source))
        
        # Animation loop for expanding waves
        for _ in range(3):
            expanding_waves = VGroup()
            for r in np.linspace(0.1, 4.0, 15):
                expanding_waves.add(Circle(radius=r, color=BLUE, stroke_width=1.5).set_opacity(1 - r/4))
            
            self.play(
                LaggedStart(*[Create(w) for w in expanding_waves[::3]], lag_ratio=0.1),
                run_time=2, rate_func=linear
            )
            self.play(FadeOut(expanding_waves), run_time=0.5)
            
        self.play(FadeOut(title2, source))
        self.clear()

        # --- Scene 3: Moving Source ---
        title3 = Text("3. Source Moving Right", font_size=48).to_edge(UP)
        source = Dot(color=YELLOW, radius=0.2).move_to(LEFT * 4)
        source_label = Text("Source", font_size=24).next_to(source, DOWN)
        velocity_vec = Arrow(LEFT*3.5, LEFT*2.5, color=WHITE, buff=0)
        v_label = Text("v", font_size=24).next_to(velocity_vec, UP)
        
        self.play(Write(title3), FadeIn(source), Write(source_label), GrowArrow(velocity_vec), Write(v_label))
        self.wait(0.5)
        
        # Generate wavefronts at different positions
        emitted_waves = VGroup()
        positions = np.linspace(-4, 4, 9)
        
        for x in positions:
            # Move source
            self.play(source.animate.move_to([x, 0, 0]), 
                      source_label.animate.next_to([x, 0, 0], DOWN),
                      velocity_vec.animate.shift(RIGHT * 1),
                      v_label.animate.shift(RIGHT * 1),
                      run_time=0.5)
            
            # Emit wavefront at current position
            wave = Circle(radius=0.1, color=BLUE, stroke_width=2).move_to([x, 0, 0])
            emitted_waves.add(wave)
            self.play(Create(wave), run_time=0.2)
            
            # Expand all existing waves
            expand_anims = [w.animate.scale(1.5) for w in emitted_waves]
            self.play(*expand_anims, run_time=0.3)
        
        # Show compression/stretching
        brace_left = BraceBetweenPoints(emitted_waves[0].get_left(), emitted_waves[1].get_left(), direction=UP, color=RED)
        text_left = Text("Compressed\n(Higher Freq)", font_size=20).next_to(brace_left, UP)
        
        brace_right = BraceBetweenPoints(emitted_waves[-2].get_right(), emitted_waves[-1].get_right(), direction=UP, color=GREEN)
        text_right = Text("Stretched\n(Lower Freq)", font_size=20).next_to(brace_right, UP)
        
        self.play(GrowFromCenter(brace_left), Write(text_left))
        self.play(GrowFromCenter(brace_right), Write(text_right))
        self.wait(1)
        self.play(FadeOut(title3, source, source_label, velocity_vec, v_label, emitted_waves, brace_left, text_left, brace_right, text_right))
        self.clear()

        # --- Scene 4: Observer Perspective ---
        title4 = Text("4. Observer Perspective", font_size=48).to_edge(UP)
        
        # Left Observer (Approaching)
        obs_left = Dot(color=RED, radius=0.15).move_to(LEFT * 5)
        obs_left_label = Text("Observer A\n(Approaching)", font_size=20).next_to(obs_left, DOWN)
        
        # Right Observer (Receding)
        obs_right = Dot(color=GREEN, radius=0.15).move_to(RIGHT * 5)
        obs_right_label = Text("Observer B\n(Receding)", font_size=20).next_to(obs_right, DOWN)
        
        source = Dot(color=YELLOW, radius=0.2).move_to(ORIGIN)
        
        # Wavefronts compressed on left, stretched on right
        left_waves = VGroup(*[Circle(radius=0.5+i*0.3, color=BLUE).move_to(LEFT*1) for i in range(5)])
        right_waves = VGroup(*[Circle(radius=0.5+i*0.8, color=BLUE).move_to(RIGHT*1) for i in range(5)])
        
        freq_left = Text("High Frequency\nHigh Pitch", font_size=24, color=RED).next_to(obs_left, UP)
        freq_right = Text("Low Frequency\nLow Pitch", font_size=24, color=GREEN).next_to(obs_right, UP)
        
        self.play(Write(title4))
        self.play(FadeIn(source), FadeIn(obs_left), Write(obs_left_label), FadeIn(obs_right), Write(obs_right_label))
        self.play(Create(left_waves), Create(right_waves))
        self.play(Write(freq_left), Write(freq_right))
        self.wait(1)
        self.play(FadeOut(title4, source, obs_left, obs_left_label, obs_right, obs_right_label, left_waves, right_waves, freq_left, freq_right))
        self.clear()

        # --- Scene 5: Mathematical Formulation ---
        title5 = Text("5. The Doppler Formula", font_size=48).to_edge(UP)
        
        formula = MathTex(
            r"f_{observed} = f_{source} \left( \frac{v_{wave} \pm v_{observer}}{v_{wave} \mp v_{source}} \right)",
            font_size=48
        ).move_to(ORIGIN)
        
        explanations = VGroup(
            Text("v_wave: Speed of wave in medium", font_size=24),
            Text("v_source: Velocity of source (+ toward observer)", font_size=24),
            Text("v_observer: Velocity of observer (+ toward source)", font_size=24),
            Text("Top signs: Motion toward each other", font_size=24, color=RED),
            Text("Bottom signs: Motion away from each other", font_size=24, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN).shift(UP)
        
        self.play(Write(title5))
        self.play(Write(formula))
        self.play(LaggedStart(*[FadeIn(exp, shift=UP) for exp in explanations], lag_ratio=0.2), run_time=3)
        self.wait(2)
        self.play(FadeOut(title5, formula, explanations))
        self.clear()

        # --- Scene 6: Sonic Boom (Supersonic) ---
        title6 = Text("6. Supersonic Speed: Sonic Boom", font_size=48).to_edge(UP)
        
        source = Dot(color=YELLOW, radius=0.2).move_to(LEFT * 6)
        mach_cone = VGroup()
        
        # Create Mach cone lines
        line1 = Line(LEFT*6, RIGHT*6 + UP*3, color=RED, stroke_width=3)
        line2 = Line(LEFT*6, RIGHT*6 + DOWN*3, color=RED, stroke_width=3)
        mach_cone.add(line1, line2)
        
        shock_wave_label = Text("Shock Wave (Mach Cone)", font_size=24, color=RED).next_to(line1.get_end(), UR)
        
        self.play(Write(title6), FadeIn(source))
        
        # Move source faster than waves
        self.play(source.animate.move_to(RIGHT * 6), run_time=3, rate_func=linear)
        
        # Show cone formation
        self.play(Create(line1), Create(line2), run_time=1)
        self.play(Write(shock_wave_label))
        self.wait(1)
        self.play(FadeOut(title6, source, mach_cone, shock_wave_label))
        self.clear()

        # --- Scene 7: Real World Applications ---
        title7 = Text("7. Real World Applications", font_size=48).to_edge(UP)
        
        apps = VGroup(
            Text("🚑 Ambulance Siren: Pitch drops as it passes", font_size=32),
            Text("🌌 Redshift/Blueshift: Measuring star velocities", font_size=32),
            Text("🌡️ Weather Radar: Tracking storm movement", font_size=32),
            Text("🏥 Medical Ultrasound: Measuring blood flow", font_size=32),
            Text("🚓 Police Radar: Measuring car speed", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN)
        
        self.play(Write(title7))
        self.play(LaggedStart(*[FadeIn(app, shift=RIGHT) for app in apps], lag_ratio=0.3), run_time=3)
        self.wait(2)
        self.play(FadeOut(title7, apps))
        self.clear()

        # --- Scene 8: Summary ---
        title8 = Text("Summary: The Doppler Effect", font_size=48).to_edge(UP)
        
        summary_points = VGroup(
            Text("• Frequency increases when source/observer approach", font_size=28, color=RED),
            Text("• Frequency decreases when source/observer recede", font_size=28, color=GREEN),
            Text("• Applies to ALL waves: Sound, Light, Radio, Water", font_size=28),
            Text("• Fundamental tool in astronomy, medicine, and radar", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(ORIGIN)
        
        final_eq = MathTex(r"\frac{\Delta f}{f} \approx \frac{v}{c}", font_size=48).to_edge(DOWN)
        
        self.play(Write(title8))
        self.play(LaggedStart(*[Write(p) for p in summary_points], lag_ratio=0.3), run_time=3)
        self.play(Write(final_eq))
        self.wait(2)
        self.play(FadeOut(title8, summary_points, final_eq))
        self.clear()
