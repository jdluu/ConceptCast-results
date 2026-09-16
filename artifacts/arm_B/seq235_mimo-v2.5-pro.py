import numpy as np
from manim import *

class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: What is a Wave? ---
        title1 = Text("What is a Wave?", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title1))
        
        # Show a single wave pulse
        wave_eq = MathTex(r"y(x, t) = A \sin(kx - \omega t)", font_size=36).to_edge(DOWN)
        self.play(Write(wave_eq))
        
        wave = FunctionGraph(
            lambda x: np.sin(2 * x),
            x_range=[-6, 6, 0.01],
            color=BLUE
        )
        self.play(Create(wave), run_time=2)
        
        # Show wavelength
        brace = Brace(wave, DOWN, color=GREEN)
        brace_text = brace.get_text("Wavelength ($\\lambda$)")
        self.play(GrowFromCenter(brace), Write(brace_text))
        
        # Show frequency
        freq_text = MathTex(r"Frequency (f) = \frac{1}{T}", font_size=36, color=ORANGE).next_to(brace_text, DOWN)
        self.play(Write(freq_text))
        
        self.wait(2)
        self.clear()

        # --- Scene 2: Wave Propagation ---
        title2 = Text("Waves Propagate Outward", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title2))
        
        # Static source emitting circular waves
        source = Dot(ORIGIN, color=RED, radius=0.2)
        source_label = Text("Source", font_size=30, color=RED).next_to(source, DOWN)
        self.play(FadeIn(source), Write(source_label))
        
        # Emission animation
        rings = VGroup()
        for i in range(5):
            ring = Circle(radius=0.1, color=BLUE, stroke_width=2)
            ring.move_to(source)
            rings.add(ring)
        
        self.play(
            *[
                ring.animate.scale(3 + i).set_opacity(0)
                for i, ring in enumerate(rings)
            ],
            run_time=3,
            lag_ratio=0.5
        )
        
        # Show wavefronts
        wavefronts = VGroup(*[
            Circle(radius=r, color=BLUE, stroke_width=2, stroke_opacity=0.7 - 0.1*i)
            for i, r in enumerate(np.arange(0.5, 4, 0.5))
        ]).move_to(source)
        self.play(Create(wavefronts), run_time=2)
        
        note = Text("Wavefronts expand at speed $v$", font_size=30, color=GREEN).to_edge(DOWN)
        self.play(Write(note))
        
        self.wait(2)
        self.clear()

        # --- Scene 3: Stationary Source, Stationary Observer ---
        title3 = Text("Stationary Source & Observer", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title3))
        
        # Source and observer
        src = Dot(LEFT * 3, color=RED, radius=0.2)
        src_label = Text("Source", font_size=30, color=RED).next_to(src, UP)
        obs = Dot(RIGHT * 3, color=GREEN, radius=0.2)
        obs_label = Text("Observer", font_size=30, color=GREEN).next_to(obs, UP)
        
        self.play(FadeIn(src), Write(src_label), FadeIn(obs), Write(obs_label))
        
        # Emission of wavefronts from source to observer
        wavefronts_still = VGroup()
        for i in range(6):
            wf = Circle(radius=0.1, color=BLUE, stroke_width=3, stroke_opacity=0.8)
            wf.move_to(src)
            wavefronts_still.add(wf)
        
        self.play(
            LaggedStart(*[
                wf.animate.scale(10).set_opacity(0.2)
                for wf in wavefronts_still
            ], lag_ratio=0.4),
            run_time=4
        )
        
        received_freq = MathTex(r"f_{observed} = f_{source}", font_size=36, color=BLUE).to_edge(DOWN)
        self.play(Write(received_freq))
        
        self.wait(2)
        self.clear()

        # --- Scene 4: Source Moves Toward Observer ---
        title4 = Text("Source Moves Toward Observer", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title4))
        
        # Moving source and stationary observer
        src_moving = Dot(LEFT * 5, color=RED, radius=0.2)
        src_m_label = Text("Moving Source", font_size=30, color=RED).next_to(src_moving, UP)
        obs_still = Dot(RIGHT * 3, color=GREEN, radius=0.2)
        obs_s_label = Text("Observer", font_size=30, color=GREEN).next_to(obs_still, UP)
        
        self.play(FadeIn(src_moving), Write(src_m_label), FadeIn(obs_still), Write(obs_s_label))
        
        # Move source and emit waves at each position
        positions = np.linspace(-5, -1, 5)
        wavefronts_compressed = VGroup()
        
        for pos in positions:
            self.play(src_moving.animate.move_to(LEFT * pos), run_time=0.5)
            wf = Circle(radius=0.1, color=BLUE, stroke_width=3, stroke_opacity=0.7)
            wf.move_to(src_moving.get_center())
            wavefronts_compressed.add(wf)
            self.play(wf.animate.scale(6).set_opacity(0.3), run_time=0.8)
        
        # Show compressed wavefronts toward observer
        compression_arrow = Arrow(LEFT * 2, RIGHT * 2, color=YELLOW)
        compression_label = Text("Wavelengths compressed\n(frequency increases)", font_size=28, color=YELLOW).next_to(compression_arrow, DOWN)
        self.play(GrowArrow(compression_arrow), Write(compression_label))
        
        bluehift_eq = MathTex(r"f' = f \frac{v}{v - v_s}", font_size=36, color=BLUE).to_edge(DOWN)
        self.play(Write(bluehift_eq))
        
        self.wait(2)
        self.clear()

        # --- Scene 5: Source Moves Away from Observer ---
        title5 = Text("Source Moves Away from Observer", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title5))
        
        # Moving source AWAY from observer
        src_away = Dot(RIGHT * 1, color=RED, radius=0.2)
        src_a_label = Text("Moving Source", font_size=30, color=RED).next_to(src_away, UP)
        obs_away = Dot(RIGHT * 5, color=GREEN, radius=0.2)
        obs_a_label = Text("Observer", font_size=30, color=GREEN).next_to(obs_away, UP)
        
        self.play(FadeIn(src_away), Write(src_a_label), FadeIn(obs_away), Write(obs_a_label))
        
        # Move source away and emit waves
        positions_away = np.linspace(1, 4, 5)
        wavefronts_expanded = VGroup()
        
        for pos in positions_away:
            self.play(src_away.animate.move_to(RIGHT * pos), run_time=0.5)
            wf = Circle(radius=0.1, color=BLUE, stroke_width=3, stroke_opacity=0.7)
            wf.move_to(src_away.get_center())
            wavefronts_expanded.add(wf)
            self.play(wf.animate.scale(6).set_opacity(0.3), run_time=0.8)
        
        # Show expanded wavefronts
        expansion_arrow = Arrow(RIGHT * 2, LEFT * 2, color=YELLOW)
        expansion_label = Text("Wavelengths stretched\n(frequency decreases)", font_size=28, color=YELLOW).next_to(expansion_arrow, DOWN)
        self.play(GrowArrow(expansion_arrow), Write(expansion_label))
        
        redshift_eq = MathTex(r"f' = f \frac{v}{v + v_s}", font_size=36, color=RED).to_edge(DOWN)
        self.play(Write(redshift_eq))
        
        self.wait(2)
        self.clear()

        # --- Scene 6: Observer Moves Toward Source ---
        title6 = Text("Observer Moves Toward Source", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title6))
        
        # Stationary source and moving observer
        src_stationary = Dot(LEFT * 4, color=RED, radius=0.2)
        src_s_label = Text("Stationary Source", font_size=30, color=RED).next_to(src_stationary, UP)
        obs_moving = Dot(RIGHT * 2, color=GREEN, radius=0.2)
        obs_m_label = Text("Moving Observer", font_size=30, color=GREEN).next_to(obs_moving, UP)
        
        self.play(FadeIn(src_stationary), Write(src_s_label), FadeIn(obs_moving), Write(obs_m_label))
        
        # Stationary source emits waves
        wavefronts_obs = VGroup(*[
            Circle(radius=r, color=BLUE, stroke_width=2, stroke_opacity=0.7 - 0.1*i)
            for i, r in enumerate(np.arange(0.5, 5, 0.5))
        ]).move_to(src_stationary)
        self.play(Create(wavefronts_obs), run_time=2)
        
        # Move observer toward source
        self.play(obs_moving.animate.move_to(LEFT * 1), run_time=3)
        
        # Show observer encountering wavefronts more quickly
        encounter_text = Text("Observer meets wavefronts\nmore frequently", font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(Write(encounter_text))
        
        obs_eq = MathTex(r"f' = f \frac{v + v_o}{v}", font_size=36, color=GREEN).next_to(encounter_text, UP)
        self.play(Write(obs_eq))
        
        self.wait(2)
        self.clear()

        # --- Scene 7: Observer Moves Away from Source ---
        title7 = Text("Observer Moves Away from Source", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title7))
        
        # Stationary source and moving observer away
        src_stat = Dot(LEFT * 4, color=RED, radius=0.2)
        src_st_label = Text("Stationary Source", font_size=30, color=RED).next_to(src_stat, UP)
        obs_away = Dot(LEFT * 1, color=GREEN, radius=0.2)
        obs_aw_label = Text("Moving Observer", font_size=30, color=GREEN).next_to(obs_away, UP)
        
        self.play(FadeIn(src_stat), Write(src_st_label), FadeIn(obs_away), Write(obs_aw_label))
        
        # Stationary source emits waves
        wavefronts_away = VGroup(*[
            Circle(radius=r, color=BLUE, stroke_width=2, stroke_opacity=0.7 - 0.1*i)
            for i, r in enumerate(np.arange(0.5, 5, 0.5))
        ]).move_to(src_stat)
        self.play(Create(wavefronts_away), run_time=2)
        
        # Move observer away
        self.play(obs_away.animate.move_to(RIGHT * 3), run_time=3)
        
        # Show observer encountering wavefronts less frequently
        recede_text = Text("Observer meets wavefronts\nless frequently", font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(Write(recede_text))
        
        obs_away_eq = MathTex(r"f' = f \frac{v - v_o}{v}", font_size=36, color=GREEN).next_to(recede_text, UP)
        self.play(Write(obs_away_eq))
        
        self.wait(2)
        self.clear()

        # --- Scene 8: General Doppler Formula ---
        title8 = Text("The General Doppler Formula", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title8))
        
        # Show the general formula
        general_formula = MathTex(
            r"f' = f \frac{v \pm v_o}{v \mp v_s}",
            font_size=48,
            color=WHITE
        ).shift(UP * 2)
        
        # Explanation of signs
        signs_explanation = VGroup(
            MathTex(r"\text{Top: } + \text{ if observer moves toward source}", font_size=28, color=GREEN),
            MathTex(r"\text{Top: } - \text{ if observer moves away from source}", font_size=28, color=GREEN),
            MathTex(r"\text{Bottom: } - \text{ if source moves toward observer}", font_size=28, color=RED),
            MathTex(r"\text{Bottom: } + \text{ if source moves away from observer}", font_size=28, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(general_formula, DOWN, buff=0.8)
        
        self.play(Write(general_formula))
        self.wait(1)
        
        for explanation in signs_explanation:
            self.play(Write(explanation), run_time=1.5)
            self.wait(0.5)
        
        self.wait(2)
        self.clear()

        # --- Scene 9: Real-World Examples ---
        title9 = Text("Real-World Examples of Doppler Effect", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title9))
        
        # Example 1: Ambulance siren
        ambulance = SVGMobject("ambulance").scale(0.5) if False else Rectangle(color=WHITE, width=2, height=1)  # Simplified
        ambulance.set_color(RED).shift(LEFT * 3)
        siren_text = Text("Siren", font_size=24, color=YELLOW).next_to(ambulance, UP)
        
        observer_icon = Dot(RIGHT * 3, color=GREEN, radius=0.3)
        obs_text = Text("You", font_size=24, color=GREEN).next_to(observer_icon, UP)
        
        self.play(FadeIn(ambulance), Write(siren_text), FadeIn(observer_icon), Write(obs_text))
        
        # Move ambulance toward observer
        self.play(ambulance.animate.shift(RIGHT * 2), run_time=2)
        high_pitch = Text("Higher pitch!", font_size=32, color=YELLOW).to_edge(DOWN)
        self.play(Write(high_pitch))
        self.wait(1)
        
        # Move ambulance away
        self.play(ambulance.animate.shift(RIGHT * 5), run_time=2)
        low_pitch = Text("Lower pitch!", font_size=32, color=YELLOW).next_to(high_pitch, UP)
        self.play(Write(low_pitch))
        
        self.wait(2)
        self.clear()

        # --- Scene 10: Summary ---
        title10 = Text("Summary: Doppler Effect", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title10))
        
        # Key points
        points = VGroup(
            Text("• Waves are compressed when source and observer\n  approach each other", font_size=28, color=BLUE),
            Text("• Waves are stretched when source and observer\n  move apart", font_size=28, color=BLUE),
            Text("• Frequency increases when approaching", font_size=28, color=GREEN),
            Text("• Frequency decreases when receding", font_size=28, color=RED),
            MathTex(r"f' = f \frac{v \pm v_o}{v \mp v_s}", font_size=36, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(title10, DOWN, buff=0.8)
        
        for point in points:
            self.play(Write(point), run_time=1.5)
            self.wait(0.5)
        
        # Final animation: source and observer moving
        final_src = Dot(LEFT * 4, color=RED, radius=0.2)
        final_obs = Dot(RIGHT * 4, color=GREEN, radius=0.2)
        self.play(FadeIn(final_src), FadeIn(final_obs))
        
        # Create wavefronts as they move
        for _ in range(3):
            wf = Circle(radius=0.1, color=BLUE, stroke_width=2, stroke_opacity=0.6)
            wf.move_to(final_src)
            self.play(
                final_src.animate.shift(RIGHT * 1.5),
                final_obs.animate.shift(LEFT * 1.5),
                wf.animate.scale(8).set_opacity(0.1),
                run_time=1
            )
        
        final_text = Text("Thank you for learning!", font_size=36, color=YELLOW).to_edge(DOWN)
        self.play(Write(final_text))
        
        self.wait(3)
