#!/usr/bin/env python3
from manim import *

class SceneGen(Scene):
    def construct(self):
        # ========== SCENE 1: Basic Wave Representation ==========
        title1 = Text("Step 1: Understanding Waves", font_size=36, color=YELLOW)
        self.play(Write(title1))
        self.wait(0.5)
        self.play(title1.animate.to_edge(UP))

        # Create a simple sine wave
        axes = Axes(x_range=[-6, 6, 1], y_range=[-1.5, 1.5, 0.5],
                    x_length=12, y_length=3, axis_config={"color": BLUE})
        axes.next_to(title1, DOWN, buff=0.3)

        sine_wave = axes.plot(lambda x: np.sin(x), color=YELLOW)
        wave_label = Text("Wave: oscillation in space/time", font_size=24, color=WHITE)
        wave_label.next_to(axes, DOWN, buff=0.3)

        self.play(Create(axes), Create(sine_wave))
        self.play(Write(wave_label))
        self.wait(1.5)

        # Animate wave propagation (phase shift)
        moving_wave = always_redraw(lambda: axes.plot(
            lambda x: np.sin(x - 2 * self.time), color=YELLOW
        ))
        self.play(
            Create(moving_wave),
            FadeOut(sine_wave),
            run_time=0.5
        )
        self.wait(2)
        self.clear()

        # ========== SCENE 2: Source and Observer ==========
        title2 = Text("Step 2: Source and Observer", font_size=36, color=YELLOW)
        self.play(Write(title2))
        self.wait(0.3)
        self.play(title2.animate.to_edge(UP))

        # Source (circle) and Observer (triangle)
        source = Circle(radius=0.4, color=RED, fill_opacity=0.8)
        source_label = Text("Source", font_size=24, color=RED).next_to(source, UP)
        source_group = VGroup(source, source_label).shift(LEFT * 3)

        observer = RegularPolygon(n=3, color=BLUE, fill_opacity=0.8).scale(0.4)
        observer_label = Text("Observer", font_size=24, color=BLUE).next_to(observer, UP)
        observer_group = VGroup(observer, observer_label).shift(RIGHT * 3)

        # Show standing source emitting waves
        self.play(FadeIn(source_group), FadeIn(observer_group))
        self.wait(1)

        # Animate circular waves from source
        circles = VGroup()
        for i in range(5):
            circle = Circle(radius=0.5 + i*0.8, color=RED, stroke_opacity=0.5)
            circle.move_to(source.get_center())
            circles.add(circle)

        self.play(
            *[Create(c, run_time=0.3) for c in circles],
            lag_ratio=0.2
        )
        self.wait(1.5)
        self.clear()

        # ========== SCENE 3: Stationary Source & Observer ==========
        title3 = Text("Step 3: Stationary Case - No Shift", font_size=36, color=YELLOW)
        self.play(Write(title3))
        self.wait(0.3)
        self.play(title3.animate.to_edge(UP))

        # Setup with wave crest visualization
        src = Dot(color=RED, radius=0.2).shift(LEFT * 4)
        obs = Dot(color=BLUE, radius=0.2).shift(RIGHT * 4)
        src_label = Text("S", color=RED, font_size=20).next_to(src, DOWN)
        obs_label = Text("O", color=BLUE, font_size=20).next_to(obs, DOWN)
        self.play(FadeIn(src), FadeIn(obs), Write(src_label), Write(obs_label))

        # Evenly spaced wavefronts
        wavefronts = VGroup()
        for i in range(1, 8):
            wf = Circle(radius=i*0.7, color=RED, stroke_opacity=0.6)
            wf.move_to(src.get_center())
            wavefronts.add(wf)
            self.play(Create(wf, run_time=0.2))

        # Add time measurement lines
        line = DashedLine(start=src.get_center(), end=obs.get_center(), color=GRAY)
        self.play(Create(line))

        # Show constant wavelength
        arrow1 = Arrow(LEFT*0.5, RIGHT*0.5, color=GREEN, buff=0)
        arrow1.next_to(obs, DOWN*2 + LEFT*0.5)
        arrow_label = Text("λ = constant", font_size=20, color=GREEN).next_to(arrow1, DOWN)
        self.play(Write(arrow1), Write(arrow_label))
        self.wait(2)
        self.clear()

        # ========== SCENE 4: Source Moving Toward Observer ==========
        title4 = Text("Step 4: Source Moving Toward Observer", font_size=36, color=YELLOW)
        self.play(Write(title4))
        self.wait(0.3)
        self.play(title4.animate.to_edge(UP))

        # Animate source moving right while emitting waves
        moving_src = Dot(color=RED, radius=0.2).shift(LEFT * 5)
        static_obs = Dot(color=BLUE, radius=0.2).shift(RIGHT * 4)
        self.play(FadeIn(moving_src), FadeIn(static_obs))

        # Compressed wavefronts in front, stretched behind
        for i in range(7):
            # Simulate moving source: emit wave when source is at various positions
            pos_x = -5 + i * 1.3  # source moves right
            moving_src.set_x(pos_x)

            # Waves in front (compressed)
            front_wave = Circle(radius=(7-i)*0.4, color=RED, stroke_opacity=0.5)
            front_wave.move_to([pos_x, 0, 0])

            # Waves behind (stretched) only for later i values
            if i > 2:
                back_wave = Circle(radius=(i-2)*0.6, color=ORANGE, stroke_opacity=0.3)
                back_wave.move_to([pos_x, 0, 0])

            self.play(
                Create(front_wave, run_time=0.3),
                Create(back_wave, run_time=0.3) if i > 2 else Wait(),
                moving_src.animate.set_x(pos_x + 1.3) if i < 6 else Wait(),
                run_time=0.5
            )

        # Highlight compressed waves
        annotation = Text("Compressed wavelength → Higher frequency", font_size=24, color=YELLOW)
        annotation.shift(DOWN * 2.5)
        self.play(Write(annotation))
        self.wait(2)
        self.clear()

        # ========== SCENE 5: Source Moving Away ==========
        title5 = Text("Step 5: Source Moving Away", font_size=36, color=YELLOW)
        self.play(Write(title5))
        self.wait(0.3)
        self.play(title5.animate.to_edge(UP))

        # Moving left (away from observer on right)
        src_away = Dot(color=RED, radius=0.2).shift(RIGHT * 3)
        obs_away = Dot(color=BLUE, radius=0.2).shift(RIGHT * 5)
        self.play(FadeIn(src_away), FadeIn(obs_away))

        for i in range(6):
            pos_x = 3 - i * 1.2  # moving left
            src_away.set_x(pos_x)

            # Waves to the right (toward observer) are stretched
            right_wave = Circle(radius=(6-i)*0.7, color=ORANGE, stroke_opacity=0.4)
            right_wave.move_to([pos_x, 0, 0])

            # Waves to left (compressed)
            if i > 1:
                left_wave = Circle(radius=(i-1)*0.4, color=RED, stroke_opacity=0.3)
                left_wave.move_to([pos_x, 0, 0])

            self.play(
                Create(right_wave, run_time=0.3),
                Create(left_wave, run_time=0.3) if i > 1 else Wait(),
                src_away.animate.set_x(pos_x - 1.2) if i < 5 else Wait(),
                run_time=0.5
            )

        annotation2 = Text("Stretched wavelength → Lower frequency", font_size=24, color=ORANGE)
        annotation2.shift(DOWN * 2.5)
        self.play(Write(annotation2))
        self.wait(2)
        self.clear()

        # ========== SCENE 6: Observer Moving Toward Source ==========
        title6 = Text("Step 6: Observer Moving Toward Source", font_size=36, color=YELLOW)
        self.play(Write(title6))
        self.wait(0.3)
        self.play(title6.animate.to_edge(UP))

        # Stationary source, moving observer
        src_stat = Dot(color=RED, radius=0.3).shift(LEFT * 4)
        obs_move = Dot(color=BLUE, radius=0.3).shift(RIGHT * 3)
        self.play(FadeIn(src_stat), FadeIn(obs_move))

        # Emit waves and show observer hitting them faster
        for i in range(5):
            wave = Circle(radius=0.5 + i*0.8, color=RED, stroke_opacity=0.5)
            wave.move_to(src_stat.get_center())
            self.play(
                Create(wave, run_time=0.2),
                obs_move.animate.shift(LEFT * 0.5) if i < 4 else Wait(),
                run_time=0.4
            )

        # Visualize observer encountering wavefronts more frequently
        encounter_dots = VGroup()
        for x in np.linspace(3, -2, 6):
            dot = Dot([x, 0, 0], color=GREEN, radius=0.1)
            encounter_dots.add(dot)
        self.play(LaggedStartMap(FadeIn, encounter_dots, lag_ratio=0.2))
        arrow3 = Arrow(LEFT * 2, RIGHT * 2, color=GREEN, buff=0).shift(DOWN * 2)
        arrow3_label = Text("Observer encounters wavefronts more often", font_size=20, color=GREEN)
        arrow3_label.next_to(arrow3, DOWN)
        self.play(Write(arrow3), Write(arrow3_label))
        self.wait(2)
        self.clear()

        # ========== SCENE 7: Universal Formula Introduction ==========
        title7 = Text("Step 7: The Doppler Shift Formula", font_size=36, color=YELLOW)
        self.play(Write(title7))
        self.wait(0.3)
        self.play(title7.animate.to_edge(UP))

        # Formula: f' = f * (v ± v_o) / (v ∓ v_s)
        formula = MathTex(
            r"f' = f \frac{v \pm v_o}{v \mp v_s}",
            font_size=48, color=BLUE
        )
        self.play(Write(formula))
        self.wait(1)

        # Explain terms
        terms = VGroup(
            Text("f = emitted frequency", font_size=24, color=RED).shift(LEFT*3 + DOWN*1.5),
            Text("v = wave speed", font_size=24, color=GREEN).shift(DOWN*2.2),
            Text("vo/s = observer/source speed", font_size=24, color=ORANGE).shift(RIGHT*3 + DOWN*1.5)
        )
        self.play(*[Write(t) for t in terms], lag_ratio=0.3)
        self.wait(2)

        # Apply to moving source case
        example = MathTex(
            r"\text{Source toward: } f' = f \frac{v}{v - v_s} > f",
            font_size=30, color=YELLOW
        ).shift(DOWN * 3)
        self.play(Write(example))
        self.wait(2)
        self.clear()

        # ========== SCENE 8: Real-World Application - Siren ==========
        title8 = Text("Step 8: Real World Example - Police Siren", font_size=36, color=YELLOW)
        self.play(Write(title8))
        self.wait(0.3)
        self.play(title8.animate.to_edge(UP))

        # Animate car with siren
        car = Rectangle(width=2, height=0.8, color=RED, fill_opacity=0.7)
        car_wheels = VGroup(
            Circle(radius=0.15, color=DARK_GREY).shift(LEFT*0.6 + DOWN*0.5),
            Circle(radius=0.15, color=DARK_GREY).shift(RIGHT*0.6 + DOWN*0.5)
        )
        car_group = VGroup(car, car_wheels).shift(LEFT * 5)

        # Observer stands on right
        person = Circle(radius=0.3, color=BLUE, fill_opacity=0.8).shift(RIGHT * 4.5)
        person_label = Text("You", font_size=20, color=BLUE).next_to(person, UP)

        self.play(FadeIn(car_group), FadeIn(person), Write(person_label))
        self.wait(0.5)

        # Siren wave animation
        siren_waves = VGroup()
        for i in range(8):
            pos_offset = i * 1.2
            wave = Circle(radius=0.3 + i*0.4, color=RED, stroke_opacity=0.6)
            wave.move_to(car_group.get_center())
            siren_waves.add(wave)

        self.play(
            car_group.animate.shift(RIGHT * 9),
            *[Create(w, run_time=0.15) for w in siren_waves],
            lag_ratio=0.1,
            run_time=3
        )

        # Show perceived pitch change
        pitch_text = Text("Sound pitch decreases as car passes!", font_size=28, color=WHITE)
        pitch_text.shift(DOWN * 2.5)
        self.play(Write(pitch_text))
        self.wait(2)
        self.clear()

        # ========== SCENE 9: Light Waves - Redshift/Blueshift ==========
        title9 = Text("Step 9: Light Waves - Redshift & Blueshift", font_size=36, color=YELLOW)
        self.play(Write(title9))
        self.wait(0.3)
        self.play(title9.animate.to_edge(UP))

        # Show light spectrum
        spectrum = VGroup(
            Rectangle(width=1, height=0.5, color=RED, fill_opacity=0.8).shift(LEFT*4),
            Rectangle(width=1, height=0.5, color=ORANGE, fill_opacity=0.8).shift(LEFT*2.5),
            Rectangle(width=1, height=0.5, color=YELLOW, fill_opacity=0.8).shift(LEFT*1),
            Rectangle(width=1, height=0.5, color=GREEN, fill_opacity=0.8).shift(RIGHT*0.5),
            Rectangle(width=1, height=0.5, color=BLUE, fill_opacity=0.8).shift(RIGHT*2),
            Rectangle(width=1, height=0.5, color=PURPLE, fill_opacity=0.8).shift(RIGHT*3.5)
        )
        spectrum_label = Text("Visible spectrum", font_size=20, color=WHITE).next_to(spectrum, DOWN)
        self.play(Create(spectrum), Write(spectrum_label))
        self.wait(1)

        # Animate redshift
        shift_arrow = Arrow(LEFT*3, RIGHT*3, color=RED, buff=0).shift(DOWN*1.5)
        shift_text = Text("Moving away: Redshift (longer λ)", font_size=24, color=RED).shift(DOWN*2.5)
        self.play(Write(shift_arrow), Write(shift_text))
        self.wait(1.5)

        # Blueshift
        shift_text2 = Text("Moving toward: Blueshift (shorter λ)", font_size=24, color=BLUE).shift(DOWN*3.5)
        self.play(Write(shift_text2))
        self.wait(2)
        self.clear()

        # ========== SCENE 10: Summary & Interactive Thought ==========
        title10 = Text("Step 10: Summary", font_size=36, color=YELLOW)
        self.play(Write(title10))
        self.wait(0.3)
        self.play(title10.animate.to_edge(UP))

        summary_points = VGroup(
            Text("• Relative motion changes perceived frequency", font_size=24, color=GREEN),
            Text("• Approaching → Higher pitch/shorter λ (Blueshift)", font_size=24, color=BLUE),
            Text("• Receding → Lower pitch/longer λ (Redshift)", font_size=24, color=RED),
            Text("• Applies to sound, light, and all waves", font_size=24, color=ORANGE),
            Text("• Formula: f' = f (v ± v_o)/(v ∓ v_s)", font_size=24, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        summary_points.shift(DOWN*1.5)
        for point in summary_points:
            self.play(Write(point), run_time=0.5)

        self.wait(1)

        # Final thought
        final_q = Text("Can you think of other Doppler effect examples?", font_size=28, color=YELLOW)
        final_q.shift(DOWN * 3.5)
        self.play(Write(final_q))
        self.wait(2)
        self.clear()
