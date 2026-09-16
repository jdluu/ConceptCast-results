from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # =================================================================
        # SCENE 1: What is a wave? (First Principles)
        # We start by explaining what a wave is.
        # =================================================================
        title1 = Text("What is a Wave?", font_size=48).to_edge(UP)
        self.play(Write(title1))
        self.wait(1)

        explanation1 = Text(
            "A wave is a disturbance that travels through\n"
            "a medium, carrying energy from one place to another.",
            font_size=30
        ).next_to(title1, DOWN, buff=0.5)
        self.play(Write(explanation1), run_time=3)
        self.wait(2)

        # Visual: a simple sine wave
        axes1 = Axes(
            x_range=[-PI, 3 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": False, "include_tip": False}
        ).next_to(explanation1, DOWN, buff=0.7)
        wave_plot = axes1.plot(lambda x: np.sin(x), color=BLUE, x_range=[-PI, 3 * PI])
        wave_label = Text("A simple sine wave", font_size=28).next_to(axes1, DOWN, buff=0.3)
        self.play(Create(axes1), run_time=1)
        self.play(Create(wave_plot), Write(wave_label), run_time=2)
        self.wait(3)

        self.clear()
        self.wait(0.5)

        # =================================================================
        # SCENE 2: Wave Properties: Wavelength and Frequency
        # =================================================================
        title2 = Text("Wave Properties", font_size=48).to_edge(UP)
        self.play(Write(title2))
        self.wait(1)

        axes2 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": False}
        ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)
        
        wave2 = axes2.plot(lambda x: np.sin(x), color=BLUE, x_range=[0, 4 * PI])
        self.play(Create(axes2), Create(wave2), run_time=1.5)

        # Wavelength arrow
        wave_len_arrow = DoubleArrow(
            start=axes2.c2p(0, -1.8),
            end=axes2.c2p(2 * PI, -1.8),
            color=YELLOW,
            buff=0.1
        )
        wave_len_label = MathTex(r"\lambda \text{ (Wavelength)}", font_size=32, color=YELLOW).next_to(wave_len_arrow, DOWN)
        
        explanation_wavelength = Text(
            "Wavelength (λ) is the distance between\n"
            "two consecutive crests of a wave.",
            font_size=28
        ).to_edge(RIGHT, buff=0.5).shift(UP)
        
        self.play(GrowArrow(wave_len_arrow), Write(wave_len_label), run_time=1.5)
        self.play(Write(explanation_wavelength), run_time=2)
        self.wait(2)

        # Frequency explanation
        explanation_frequency = Text(
            "Frequency (f) is the number of waves\n"
            "that pass a point per second (Hertz, Hz).",
            font_size=28
        ).next_to(explanation_wavelength, DOWN, buff=0.7)
        
        freq_formula = MathTex(r"f = \frac{v}{\lambda}", font_size=36).next_to(explanation_frequency, DOWN, buff=0.5)
        
        self.play(Write(explanation_frequency), run_time=2)
        self.play(Write(freq_formula))
        self.wait(3)

        self.clear()
        self.wait(0.5)

        # =================================================================
        # SCENE 3: Wave Source at Rest
        # We show a source emitting waves in all directions.
        # =================================================================
        title3 = Text("Source at Rest", font_size=48).to_edge(UP)
        self.play(Write(title3))
        self.wait(1)

        explanation3 = Text(
            "A stationary source emits waves that travel\n"
            "outward equally in all directions.",
            font_size=28
        ).next_to(title3, DOWN, buff=0.5)
        self.play(Write(explanation3), run_time=2)
        self.wait(1)

        source3 = Dot(ORIGIN, color=RED, radius=0.15)
        source_label3 = Text("Source", font_size=24, color=RED).next_to(source3, DOWN, buff=0.2)
        self.play(FadeIn(source3), Write(source_label3))

        # Create expanding circles to represent wavefronts
        waves3 = VGroup()
        for i in range(5):
            wave_circle = Circle(
                radius=0.1,
                color=BLUE,
                stroke_width=2,
                stroke_opacity=0.8
            ).move_arc_center_to(ORIGIN)
            waves3.add(wave_circle)

        wavefronts3 = AnimationGroup(
            *[wave.animate.scale(8).set_stroke(opacity=0) for wave in waves3],
            lag_ratio=0.5,
            run_time=4
        )
        self.play(wavefronts3)
        
        explanation3b = Text(
            "Notice the wavefronts are evenly spaced\n"
            "and form perfect circles.",
            font_size=28
        ).next_to(explanation3, DOWN, buff=1.5)
        self.play(Write(explanation3b), run_time=2)
        self.wait(2)

        self.clear()
        self.wait(0.5)

        # =================================================================
        # SCENE 4: Moving Source - Bunching in Front
        # We show how wavefronts bunch up in front of a moving source.
        # =================================================================
        title4 = Text("Source in Motion", font_size=48).to_edge(UP)
        self.play(Write(title4))
        self.wait(1)

        explanation4 = Text(
            "When a source moves, it 'chases' the wavefronts\n"
            "it emitted earlier, compressing them in front.",
            font_size=28
        ).next_to(title4, DOWN, buff=0.5)
        self.play(Write(explanation4), run_time=2.5)
        self.wait(1)

        # Moving source emitting waves
        source4 = Dot(LEFT * 5 + DOWN * 1, color=RED, radius=0.15)
        source_label4 = Text("Moving Source", font_size=24, color=RED).next_to(source4, UP, buff=0.2)
        self.play(FadeIn(source4), Write(source_label4))

        # Path of the source
        path4 = Line(LEFT * 5 + DOWN * 1, RIGHT * 5 + DOWN * 1, color=WHITE, stroke_opacity=0.3)
        self.play(Create(path4), run_time=0.5)

        # Animate source moving and emitting waves at intervals
        wave_positions = []
        for i in range(6):
            wave_positions.append(source4.get_center())
            self.play(
                source4.animate.shift(RIGHT * (10/5)),
                source_label4.animate.shift(RIGHT * (10/5)),
                run_time=0.5,
                rate_func=linear
            )

        # Now create the static view of the wavefronts
        source_final_pos = source4.get_center()
        wavefronts4 = VGroup()
        colors = [BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E, BLUE]
        
        for i, pos in enumerate(wave_positions):
            circle = Circle(
                radius=(6 - i) * 0.8,
                color=colors[i],
                stroke_width=2,
                stroke_opacity=0.7
            ).move_arc_center_to(pos)
            wavefronts4.add(circle)

        # Clear the moving animation and show the static result
        self.remove(source4, source_label4, path4)
        
        # Redraw source at final position
        source4_static = Dot(source_final_pos, color=RED, radius=0.15)
        source_label4_static = Text("Source (now here)", font_size=24, color=RED).next_to(source4_static, DOWN, buff=0.2)
        
        # Show the wavefronts
        self.play(
            *[Create(w) for w in wavefronts4],
            FadeIn(source4_static),
            Write(source_label4_static),
            run_time=3
        )
        
        # Add labels for front and back
        front_label = Text("Wavefronts bunched\n(shorter wavelength)", font_size=24, color=YELLOW).move_to(RIGHT * 3 + UP * 2)
        back_label = Text("Wavefronts spread\n(longer wavelength)", font_size=24, color=YELLOW).move_to(LEFT * 3 + UP * 2)
        
        front_arrow = Arrow(front_label.get_bottom(), source_final_pos + RIGHT * 3 + DOWN * 0.5, buff=0.1, color=YELLOW)
        back_arrow = Arrow(back_label.get_bottom(), source_final_pos + LEFT * 3 + DOWN * 0.5, buff=0.1, color=YELLOW)
        
        self.play(Write(front_label), GrowArrow(front_arrow), run_time=1.5)
        self.play(Write(back_label), GrowArrow(back_arrow), run_time=1.5)
        self.wait(3)

        self.clear()
        self.wait(0.5)

        # =================================================================
        # SCENE 5: Observer Position Matters
        # We introduce the observer and how their position affects what they hear.
        # =================================================================
        title5 = Text("Observer Position Matters", font_size=48).to_edge(UP)
        self.play(Write(title5))
        self.wait(1)

        explanation5 = Text(
            "What an observer hears depends on whether\n"
            "they are in front of or behind the moving source.",
            font_size=28
        ).next_to(title5, DOWN, buff=0.5)
        self.play(Write(explanation5), run_time=2.5)
        self.wait(1)

        # Central moving source
        source5 = Dot(ORIGIN, color=RED, radius=0.15)
        source_label5 = Text("Moving Source →", font_size=24, color=RED).next_to(source5, LEFT, buff=0.2)
        self.play(FadeIn(source5), Write(source_label5))

        # Observers
        obs_front = Dot(RIGHT * 4, color=GREEN, radius=0.12)
        obs_front_label = Text("Observer A\n(in front)", font_size=22, color=GREEN).next_to(obs_front, UP, buff=0.2)
        
        obs_back = Dot(LEFT * 4, color=ORANGE, radius=0.12)
        obs_back_label = Text("Observer B\n(behind)", font_size=22, color=ORANGE).next_to(obs_back, UP, buff=0.2)
        
        self.play(FadeIn(obs_front), Write(obs_front_label), FadeIn(obs_back), Write(obs_back_label))

        # Show wavefronts moving
        waves_front = VGroup()
        waves_back = VGroup()
        
        for i in range(3):
            wf = Circle(radius=0.3 * (i + 1), color=BLUE, stroke_width=2, stroke_opacity=0.6).move_arc_center_to(ORIGIN)
            waves_front.add(wf)
            waves_back.add(wf.copy())
        
        self.play(
            *[w.animate.move_arc_center_to(RIGHT * 4) for w in waves_front],
            run_time=2,
            rate_func=linear
        )
        
        self.play(
            *[w.animate.move_arc_center_to(LEFT * 4) for w in waves_back],
            run_time=2,
            rate_func=linear
        )

        # Explanation labels
        front_explain = Text(
            "A sees compressed waves\n→ Higher frequency",
            font_size=24, color=YELLOW
        ).move_to(RIGHT * 0 + DOWN * 2.5)
        
        back_explain = Text(
            "B sees stretched waves\n→ Lower frequency",
            font_size=24, color=YELLOW
        ).next_to(front_explain, DOWN, buff=0.3)
        
        self.play(Write(front_explain), run_time=1.5)
        self.play(Write(back_explain), run_time=1.5)
        self.wait(3)

        self.clear()
        self.wait(0.5)

        # =================================================================
        # SCENE 6: The Doppler Effect Formula
        # We present the mathematical formula.
        # =================================================================
        title6 = Text("The Doppler Effect Formula", font_size=48).to_edge(UP)
        self.play(Write(title6))
        self.wait(1)

        explanation6 = Text(
            "The apparent frequency heard by an observer is given by:",
            font_size=30
        ).next_to(title6, DOWN, buff=0.5)
        self.play(Write(explanation6), run_time=2)
        self.wait(1)

        # The main formula
        formula = MathTex(
            r"f' = f \left( \frac{v \pm v_o}{v \mp v_s} \right)",
            font_size=52
        ).move_to(ORIGIN)
        self.play(Write(formula), run_time=2)
        self.wait(1)

        # Variable explanations
        var_box = SurroundingRectangle(formula, color=YELLOW, buff=0.3)
        self.play(Create(var_box))

        variables = VGroup(
            MathTex(r"f' = \text{apparent frequency}", font_size=28),
            MathTex(r"f = \text{actual frequency of source}", font_size=28),
            MathTex(r"v = \text{speed of wave in medium}", font_size=28),
            MathTex(r"v_o = \text{speed of observer}", font_size=28),
            MathTex(r"v_s = \text{speed of source}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(var_box, DOWN, buff=0.5)

        self.play(Write(variables), run_time=3)
        self.wait(3)

        self.clear()
        self.wait(0.5)

        # =================================================================
        # SCENE 7: Signs in the Formula
        # We explain when to use + and when to use -.
        # =================================================================
        title7 = Text("Understanding the Signs", font_size=48).to_edge(UP)
        self.play(Write(title7))
        self.wait(1)

        explanation7 = Text(
            "The signs in the formula depend on the\n"
            "direction of motion relative to the wave.",
            font_size=28
        ).next_to(title7, DOWN, buff=0.5)
        self.play(Write(explanation7), run_time=2)
        self.wait(1)

        # Create a table-like structure
        observer_rules = VGroup(
            Text("Observer:", font_size=30, color=GREEN),
            Text("  → Moving toward source: use +", font_size=26),
            Text("  → Moving away from source: use −", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.5)
        
        source_rules = VGroup(
            Text("Source:", font_size=30, color=RED),
            Text("  → Moving toward observer: use −", font_size=26),
            Text("  → Moving away from observer: use +", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(observer_rules, DOWN, buff=0.7)

        self.play(Write(observer_rules), run_time=2)
        self.wait(1)
        self.play(Write(source_rules), run_time=2)
        self.wait(2)

        # Visual aid: source and observer moving
        source7 = Dot(LEFT * 3, color=RED, radius=0.15)
        obs7 = Dot(RIGHT * 3, color=GREEN, radius=0.12)
        
        source_arrow = Arrow(LEFT * 3, LEFT * 3 + RIGHT * 1.5, color=RED, buff=0)
        obs_arrow = Arrow(RIGHT * 3, RIGHT * 3 + LEFT * 1.5, color=GREEN, buff=0)
        
        self.play(FadeIn(source7), FadeIn(obs7))
        self.play(GrowArrow(source_arrow), GrowArrow(obs_arrow))
        
        towards_label = Text("Both moving toward each other\n→ Higher frequency!", font_size=28, color=YELLOW).move_to(DOWN * 2.5)
        self.play(Write(towards_label), run_time=2)
        self.wait(3)

        self.clear()
        self.wait(0.5)

        # =================================================================
        # SCENE 8: Example Calculation
        # We walk through a concrete example.
        # =================================================================
        title8 = Text("Example: Ambulance Siren", font_size=48).to_edge(UP)
        self.play(Write(title8))
        self.wait(1)

        problem = VGroup(
            Text("An ambulance travels at 30 m/s toward a stationary observer.", font_size=26),
            Text("Its siren has a frequency of 700 Hz.", font_size=26),
            Text("Speed of sound: 340 m/s", font_size=26),
            Text("What frequency does the observer hear?", font_size=26, color=YELLOW),
        ).arrange(DOWN, buff=0.3).next_to(title8, DOWN, buff=0.5)
        
        self.play(Write(problem), run_time=4)
        self.wait(2)

        # Show the calculation
        calc = VGroup(
            MathTex(r"f' = f \left( \frac{v}{v - v_s} \right)", font_size=40),
            MathTex(r"f' = 700 \left( \frac{340}{340 - 30} \right)", font_size=40),
            MathTex(r"f' = 700 \left( \frac{340}{310} \right)", font_size=40),
            MathTex(r"f' \approx 767.7 \text{ Hz}", font_size=40, color=YELLOW),
        ).arrange(DOWN, buff=0.4).next_to(problem, DOWN, buff=0.7)

        for line in calc:
            self.play(Write(line), run_time=1.5)
            self.wait(1)

        # Highlight the result
        result_box = SurroundingRectangle(calc[-1], color=YELLOW, buff=0.2)
        self.play(Create(result_box))
        
        conclusion = Text(
            "The observer hears a higher pitch than the actual siren!",
            font_size=28, color=GREEN
        ).next_to(calc, DOWN, buff=0.5)
        self.play(Write(conclusion), run_time=2)
        self.wait(3)

        self.clear()
        self.wait(0.5)

        # =================================================================
        # SCENE 9: Real-World Applications
        # We show where the Doppler effect is used.
        # =================================================================
        title9 = Text("Real-World Applications", font_size=48).to_edge(UP)
        self.play(Write(title9))
        self.wait(1)

        explanation9 = Text(
            "The Doppler effect has many important applications:",
            font_size=30
        ).next_to(title9, DOWN, buff=0.5)
        self.play(Write(explanation9), run_time=2)
        self.wait(1)

        # Create application cards
        apps = [
            ("Police Radar", "Measures vehicle speed using reflected\nradio waves and Doppler shift"),
            ("Medical Ultrasound", "Measures blood flow velocity\nusing reflected sound waves"),
            ("Astronomy", "Determines if stars/galaxies are\nmoving toward or away from us"),
            ("Weather Radar", "Detects wind speed and direction\ninside storms"),
        ]

        app_groups = VGroup()
        for title, desc in apps:
            card = VGroup(
                Text(title, font_size=26, color=YELLOW),
                Text(desc, font_size=20, color=WHITE)
            ).arrange(DOWN, buff=0.15)
            app_groups.add(card)

        app_groups.arrange_in_grid(rows=2, cols=2, buff=0.8).next_to(explanation9, DOWN, buff=0.7)

        for app in app_groups:
            self.play(FadeIn(app, shift=UP * 0.3), run_time=1)
            self.wait(1.5)

        self.wait(2)

        self.clear()
        self.wait(0.5)

        # =================================================================
        # SCENE 10: Summary and Key Takeaways
        # =================================================================
        title10 = Text("Summary: The Doppler Effect", font_size=48).to_edge(UP)
        self.play(Write(title10))
        self.wait(1)

        takeaways = VGroup(
            Text("1. Waves have wavelength (λ) and frequency (f)", font_size=28),
            Text("2. A moving source compresses waves in front,\n    stretches them behind", font_size=28),
            Text("3. The apparent frequency depends on relative\n    motion between source and observer", font_size=28),
            Text("4. Higher relative approach → Higher frequency\n    (shorter wavelength)", font_size=28),
            Text("5. Higher relative separation → Lower frequency\n    (longer wavelength)", font_size=28),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(title10, DOWN, buff=0.7)

        for point in takeaways:
            self.play(Write(point), run_time=1.5)
            self.wait(0.5)

        # Final formula reminder
        final_formula = MathTex(
            r"f' = f \left( \frac{v \pm v_o}{v \mp v_s} \right)",
            font_size=44, color=YELLOW
        ).next_to(takeaways, DOWN, buff=0.7)
        
        self.play(Write(final_formula), run_time=1.5)
        
        final_box = SurroundingRectangle(final_formula, color=YELLOW, buff=0.2)
        self.play(Create(final_box))
        
        thank_you = Text(
            "The Doppler effect explains many phenomena\n"
            "in our everyday world!",
            font_size=30, color=GREEN
        ).next_to(final_box, DOWN, buff=0.5)
        self.play(Write(thank_you), run_time=2)
        self.wait(4)
