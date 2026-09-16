#!/usr/bin/env python3
"""
Educational animation: Doppler Effect
Teaches: Apparent shift in frequency of a wave for an observer moving relative to the wave's source.
"""

from manim import *

class SceneGen(Scene):
    def construct(self):
        # ------------------------------------------------------------
        # Scene 1: What is frequency? – Show a simple sinusoidal wave
        # ------------------------------------------------------------
        title = Text("Step 1: What is Frequency?", font_size=36).to_edge(UP)
        # Create axes and a sinusoidal wave representing a constant frequency
        axes = Axes(
            x_range=[-2, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=12,
            y_length=3,
            axis_config={"color": BLUE}
        ).shift(DOWN * 1.5)

        wave = axes.plot(
            lambda x: np.sin(2 * np.pi * x / 2),  # spatial period = 2
            x_range=[-2, 10],
            color=YELLOW
        )

        freq_label = MathTex(r"\text{Frequency} = \frac{\text{number of cycles}}{\text{time}}", color=RED).next_to(axes, DOWN)

        self.play(Write(title), Create(axes))
        self.wait(0.3)
        self.play(Create(wave), run_time=2)
        self.play(Write(freq_label))
        self.wait(1)
        # Animate wave moving to show cycles passing
        moving_wave = axes.plot(
            lambda x: np.sin(2 * np.pi * (x - self.time * 1.5) / 2),
            x_range=[-2, 10],
            color=YELLOW
        )
        self.play(Transform(wave, moving_wave), run_time=2, rate_func=linear)
        self.wait(0.5)
        self.clear()

        # ------------------------------------------------------------
        # Scene 2: Observing wavefronts – a point source emitting circles
        # ------------------------------------------------------------
        title2 = Text("Step 2: Wavefronts From a Source", font_size=36).to_edge(UP)
        source_pos = np.array([0, 0, 0])
        source_dot = Dot(source_pos, color=RED)
        source_label = MathTex("S").next_to(source_dot, DOWN, buff=0.2)

        # Create expanding circle wavefronts
        circles = VGroup()
        for radius in np.arange(0.5, 4.5, 0.5):
            circles.add(Circle(radius=radius, color=BLUE, stroke_opacity=0.5))

        self.play(Write(title2), FadeIn(source_dot), Write(source_label))
        self.wait(0.5)
        # Animate circles expanding
        self.play(
            *[Create(circle) for circle in circles],
            run_time=3,
            rate_func=linear
        )
        self.wait(1)
        self.clear()

        # ------------------------------------------------------------
        # Scene 3: Stationary observer – constant frequency
        # ------------------------------------------------------------
        title3 = Text("Step 3: Stationary Observer – Constant Frequency", font_size=30).to_edge(UP)
        source_dot2 = Dot(LEFT*3, color=RED)
        source_label2 = MathTex("S").next_to(source_dot2, DOWN, buff=0.2)

        # Observer on the right
        obs_pos = RIGHT*3
        observer_dot = Dot(obs_pos, color=GREEN)
        observer_label = MathTex("O").next_to(observer_dot, DOWN, buff=0.2)

        # Show wavefronts arriving at observer
        wf_offsets = np.linspace(0, 2, 5)
        circles_to_obs = VGroup()
        for d in wf_offsets:
            c = Circle(radius=1 + d, color=BLUE, stroke_opacity=0.4).move_to(source_dot2.get_center())
            circles_to_obs.add(c)

        self.play(Write(title3), FadeIn(source_dot2), Write(source_label2),
                  FadeIn(observer_dot), Write(observer_label))
        self.wait(0.5)
        self.play(
            *[Create(c) for c in circles_to_obs],
            run_time=2,
            rate_func=linear
        )
        self.wait(1)
        self.clear()

        # ------------------------------------------------------------
        # Scene 4: Moving observer toward source – higher frequency
        # ------------------------------------------------------------
        title4 = Text("Step 4: Observer Moves Toward Source -> Higher Freq", font_size=28).to_edge(UP)
        source_pos4 = LEFT*4
        source_dot4 = Dot(source_pos4, color=RED)
        source_label4 = MathTex("S").next_to(source_dot4, DOWN, buff=0.2)

        obs_start = RIGHT*3
        obs_end = np.array([1, 0, 0])
        observer_dot4 = Dot(obs_start, color=GREEN)
        observer_label4 = MathTex("O").next_to(observer_dot4, DOWN, buff=0.2)

        # Show wavefronts
        wf_circles = VGroup()
        for rad in np.arange(1, 6, 1):
            c = Circle(radius=rad, color=BLUE, stroke_opacity=0.3)
            c.move_to(source_pos4)
            wf_circles.add(c)

        self.play(Write(title4), FadeIn(source_dot4), Write(source_label4),
                  FadeIn(observer_dot4), Write(observer_label4))
        self.play(*[Create(c) for c in wf_circles], run_time=2)
        # Move observer toward source – they encounter wavefronts faster
        self.play(
            observer_dot4.animate.move_to(obs_end),
            observer_label4.animate.next_to(obs_end, DOWN, buff=0.2),
            run_time=3
        )
        self.wait(1)

        # Add high frequency indicator
        arrow_high = Arrow(start=UP*0.5, end=DOWN*0.5, color=RED).next_to(observer_dot4, UP)
        high_text = Text("High frequency detected!", font_size=24, color=RED).next_to(arrow_high, UP)
        self.play(Write(arrow_high), Write(high_text))
        self.wait(1)
        self.clear()

        # ------------------------------------------------------------
        # Scene 5: Moving observer away from source – lower frequency
        # ------------------------------------------------------------
        title5 = Text("Step 5: Observer Moves Away From Source -> Lower Freq", font_size=28).to_edge(UP)
        source_pos5 = LEFT*4
        source_dot5 = Dot(source_pos5, color=RED)
        source_label5 = MathTex("S").next_to(source_dot5, DOWN, buff=0.2)

        obs_start5 = RIGHT*1
        obs_end5 = RIGHT*3
        observer_dot5 = Dot(obs_start5, color=GREEN)
        observer_label5 = MathTex("O").next_to(observer_dot5, DOWN, buff=0.2)

        wf_circles5 = VGroup()
        for rad in np.arange(1, 6, 1):
            c = Circle(radius=rad, color=BLUE, stroke_opacity=0.3)
            c.move_to(source_pos5)
            wf_circles5.add(c)

        self.play(Write(title5), FadeIn(source_dot5), Write(source_label5),
                  FadeIn(observer_dot5), Write(observer_label5))
        self.play(*[Create(c) for c in wf_circles5], run_time=2)
        # Move observer away – stretches wavefront spacing
        self.play(
            observer_dot5.animate.move_to(obs_end5),
            observer_label5.animate.next_to(obs_end5, DOWN, buff=0.2),
            run_time=3
        )
        arrow_low = Arrow(start=UP*0.5, end=DOWN*0.5, color=BLUE).next_to(observer_dot5, UP)
        low_text = Text("Lower frequency detected!", font_size=24, color=BLUE).next_to(arrow_low, UP)
        self.play(Write(arrow_low), Write(low_text))
        self.wait(1)
        self.clear()

        # ------------------------------------------------------------
        # Scene 6: Moving source toward stationary observer – compression
        # ------------------------------------------------------------
        title6 = Text("Step 6: Source Moving Toward Observer – Compression", font_size=28).to_edge(UP)
        source_start6 = LEFT*4
        source_end6 = LEFT*1
        source_dot6 = Dot(source_start6, color=RED)
        source_label6 = MathTex("S").next_to(source_dot6, DOWN, buff=0.2)

        obs_pos6 = RIGHT*3
        observer_dot6 = Dot(obs_pos6, color=GREEN)
        observer_label6 = MathTex("O").next_to(observer_dot6, DOWN, buff=0.2)

        # Generate sequential wavefronts as source moves
        all_wfs = VGroup()
        for i, rad in enumerate(np.arange(1, 6, 1)):
            center = source_start6 + (source_end6 - source_start6) * (i / 6)
            c = Circle(radius=rad, color=BLUE, stroke_opacity=0.3)
            c.move_to(center)
            all_wfs.add(c)

        self.play(Write(title6), FadeIn(source_dot6), Write(source_label6),
                  FadeIn(observer_dot6), Write(observer_label6))
        self.play(*[Create(c, run_time=0.5) for c in all_wfs])
        # Animate source moving toward observer
        self.play(
            source_dot6.animate.move_to(source_end6),
            source_label6.animate.next_to(source_end6, DOWN, buff=0.2),
            run_time=2
        )
        # Show compression in front of source
        front_text = Text("Compression – Higher frequency ahead", font_size=24, color=RED).next_to(observer_dot6, UP)
        self.play(Write(front_text))
        self.wait(1.5)
        self.clear()

        # ------------------------------------------------------------
        # Scene 7: Moving source away from observer – expansion
        # ------------------------------------------------------------
        title7 = Text("Step 7: Source Moving Away – Expansion", font_size=28).to_edge(UP)
        source_start7 = LEFT*1
        source_end7 = LEFT*4
        source_dot7 = Dot(source_start7, color=RED)
        source_label7 = MathTex("S").next_to(source_dot7, DOWN, buff=0.2)

        obs_pos7 = RIGHT*3
        observer_dot7 = Dot(obs_pos7, color=GREEN)
        observer_label7 = MathTex("O").next_to(observer_dot7, DOWN, buff=0.2)

        all_wfs7 = VGroup()
        for i, rad in enumerate(np.arange(1, 6, 1)):
            center = source_start7 + (source_end7 - source_start7) * (i / 6)
            c = Circle(radius=rad, color=BLUE, stroke_opacity=0.3)
            c.move_to(center)
            all_wfs7.add(c)

        self.play(Write(title7), FadeIn(source_dot7), Write(source_label7),
                  FadeIn(observer_dot7), Write(observer_label7))
        self.play(*[Create(c, run_time=0.5) for c in all_wfs7])
        self.play(
            source_dot7.animate.move_to(source_end7),
            source_label7.animate.next_to(source_end7, DOWN, buff=0.2),
            run_time=2
        )
        back_text = Text("Expansion – Lower frequency behind", font_size=24, color=BLUE).next_to(observer_dot7, UP)
        self.play(Write(back_text))
        self.wait(1.5)
        self.clear()

        # ------------------------------------------------------------
        # Scene 8: Combining both motions – relative velocity matters
        # ------------------------------------------------------------
        title8 = Text("Step 8: Relative Motion – Both Source & Observer Move", font_size=28).to_edge(UP)
        # Both move toward each other – strong compression
        source8 = Dot(LEFT*4, color=RED).shift(UP*0.5)
        obs8 = Dot(RIGHT*4, color=GREEN).shift(UP*0.5)
        s_label = MathTex("S").next_to(source8, DOWN, buff=0.2)
        o_label = MathTex("O").next_to(obs8, DOWN, buff=0.2)

        self.play(Write(title8), FadeIn(source8), Write(s_label), FadeIn(obs8), Write(o_label))
        self.wait(0.5)

        # Animate both moving toward each other
        self.play(
            source8.animate.shift(RIGHT * 2),
            s_label.animate.shift(RIGHT * 2),
            obs8.animate.shift(LEFT * 2),
            o_label.animate.shift(LEFT * 2),
            run_time=2
        )

        result = Text("Higher relative velocity → Higher frequency shift", font_size=24, color=RED).to_edge(DOWN)
        self.play(Write(result))
        self.wait(1.5)
        self.clear()

        # ------------------------------------------------------------
        # Scene 9: Real-world example – ambulance siren
        # ------------------------------------------------------------
        title9 = Text("Step 9: Real World – Ambulance Siren", font_size=30).to_edge(UP)
        ambulance = Text("🚑", font_size=60).move_to(LEFT*3)
        observer9 = Text("👤", font_size=60).move_to(RIGHT*3)

        wf_circles9 = VGroup()
        for rad in np.arange(0.5, 3, 0.5):
            c = Circle(radius=rad, color=BLUE, stroke_opacity=0.2)
            c.move_to(ambulance.get_center())
            wf_circles9.add(c)

        self.play(Write(title9), FadeIn(ambulance), FadeIn(observer9))
        self.play(*[Create(c) for c in wf_circles9], run_time=1.5)
        # Ambulance approaches observer
        self.play(
            ambulance.animate.shift(RIGHT * 2),
            run_time=2
        )
        txt_approaching = Text("Approaching: Higher pitch (eee-ooo)", font_size=24, color=RED).to_edge(DOWN)
        self.play(Write(txt_approaching))
        self.wait(1)
        self.play(
            ambulance.animate.shift(LEFT * 4),
            run_time=2
        )
        txt_retreating = Text("Retreating: Lower pitch (ooo-eee)", font_size=24, color=BLUE).to_edge(DOWN)
        self.play(Transform(txt_approaching, txt_retreating))
        self.wait(1.5)
        self.clear()

        # ------------------------------------------------------------
        # Scene 10: Summary – Formula and final concept
        # ------------------------------------------------------------
        title10 = Text("Step 10: Doppler Shift Formula", font_size=30).to_edge(UP)
        formula = MathTex(
            r"f' = f \frac{v + v_o}{v - v_s}",
            font_size=48
        )
        formula[0][0:2].set_color(RED)    # f'
        formula[0][2:4].set_color(YELLOW) # =
        formula[0][4:6].set_color(RED)    # f

        note1 = Text("f': observed frequency  f: source frequency", font_size=24).next_to(formula, DOWN, buff=0.5)
        note2 = Text("v: wave speed  v_o: observer speed  v_s: source speed", font_size=24).next_to(note1, DOWN)
        note3 = Text("Signs: + toward source, - toward observer", font_size=24, color=BLUE).next_to(note2, DOWN)

        self.play(Write(title10))
        self.wait(0.5)
        self.play(Write(formula))
        self.wait(1)
        self.play(Write(note1), Write(note2), Write(note3))
        self.wait(2)

        # Final emphasis
        final_box = SurroundingRectangle(VGroup(formula, note1, note2, note3), color=GREEN, buff=0.2)
        self.play(Create(final_box))
        self.wait(2)
