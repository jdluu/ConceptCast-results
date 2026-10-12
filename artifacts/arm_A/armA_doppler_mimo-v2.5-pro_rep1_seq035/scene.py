import numpy as np
from manim import *

class SceneGen(Scene):
    def construct(self):
        # --- SCENE 1: Introduction to Waves ---
        title = Text("Understanding Waves", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Create a static wave
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=4,
            tips=False,
        ).shift(DOWN * 0.5)
        wave_graph = axes.plot(
            lambda x: 1.5 * np.sin(2 * x),
            x_range=[0, 10],
            color=BLUE,
        )
        wave_label = Text("Wave: alternating high and low pressure", font_size=28).next_to(axes, DOWN)

        self.play(Create(axes), run_time=1)
        self.play(Create(wave_graph), run_time=2)
        self.play(Write(wave_label))
        self.wait(2)

        # Highlight crests and troughs
        crest = Dot(axes.c2p(np.pi / 2, 1.5), color=YELLOW, radius=0.1)
        trough = Dot(axes.c2p(3 * np.pi / 2, -1.5), color=YELLOW, radius=0.1)
        crest_label = Text("Crest (high)", font_size=24, color=YELLOW).next_to(crest, UP)
        trough_label = Text("Trough (low)", font_size=24, color=YELLOW).next_to(trough, DOWN)

        self.play(FadeIn(crest), Write(crest_label))
        self.play(FadeIn(trough), Write(trough_label))
        self.wait(2)

        # Show wavelength
        brace = BraceBetweenPoints(axes.c2p(0, 0), axes.c2p(np.pi, 0), direction=DOWN, color=GREEN)
        lambda_label = MathTex(r"\lambda \text{ (wavelength)}", color=GREEN).next_to(brace, DOWN)
        self.play(GrowFromCenter(brace), Write(lambda_label))
        self.wait(2)

        self.clear()
        self.wait(0.5)

        # --- SCENE 2: Frequency ---
        title2 = Text("Frequency: Waves Per Second", font_size=48).to_edge(UP)
        self.play(Write(title2))
        self.wait(1)

        # Show two waves with different frequencies
        ax_low = Axes(
            x_range=[0, 6, 1], y_range=[-2, 2, 1], x_length=6, y_length=3, tips=False
        ).to_edge(LEFT).shift(DOWN * 0.5)
        ax_high = Axes(
            x_range=[0, 6, 1], y_range=[-2, 2, 1], x_length=6, y_length=3, tips=False
        ).to_edge(RIGHT).shift(DOWN * 0.5)

        wave_low = ax_low.plot(lambda x: 1.5 * np.sin(x), x_range=[0, 6], color=BLUE)
        wave_high = ax_high.plot(lambda x: 1.5 * np.sin(3 * x), x_range=[0, 6], color=RED)

        low_label = Text("Low Frequency", font_size=28, color=BLUE).next_to(ax_low, DOWN)
        high_label = Text("High Frequency", font_size=28, color=RED).next_to(ax_high, DOWN)
        f_low = MathTex(r"f = \frac{\text{cycles}}{\text{second}}", font_size=36).next_to(low_label, DOWN)
        f_high = MathTex(r"f = \frac{\text{more cycles}}{\text{second}}", font_size=36).next_to(high_label, DOWN)

        self.play(Create(ax_low), Create(ax_high), run_time=1)
        self.play(Create(wave_low), Create(wave_high), run_time=2)
        self.play(Write(low_label), Write(high_label))
        self.play(Write(f_low), Write(f_high))
        self.wait(3)

        # Animated dot showing cycles
        dot_low = Dot(ax_low.c2p(0, 0), color=YELLOW)
        dot_high = Dot(ax_high.c2p(0, 0), color=YELLOW)
        self.play(FadeIn(dot_low), FadeIn(dot_high))
        self.play(
            MoveAlongPath(dot_low, wave_low, rate_func=linear),
            MoveAlongPath(dot_high, wave_high, rate_func=linear),
            run_time=4,
        )
        self.wait(1)

        self.clear()
        self.wait(0.5)

        # --- SCENE 3: Wave Source at Rest ---
        title3 = Text("Source at Rest", font_size=48).to_edge(UP)
        self.play(Write(title3))

        source = Dot(ORIGIN, color=RED, radius=0.15)
        source_label = Text("Source", font_size=28, color=RED).next_to(source, DOWN)
        self.play(FadeIn(source), Write(source_label))

        # Expanding circles (wavefronts)
        circles = VGroup()
        for i in range(8):
            circle = Circle(radius=0.1, color=BLUE, stroke_opacity=0.7).move_to(source.get_center())
            circles.add(circle)

        self.play(
            *[
                circle.animate.scale(3 + i * 0.8).set_stroke(opacity=0.3 + 0.05 * i)
                for i, circle in enumerate(circles)
            ],
            run_time=4,
            rate_func=linear,
        )

        # Place observers
        obs1 = Dot([-3, -2, 0], color=GREEN, radius=0.1)
        obs2 = Dot([3, -2, 0], color=YELLOW, radius=0.1)
        obs1_label = Text("Observer A", font_size=24, color=GREEN).next_to(obs1, DOWN)
        obs2_label = Text("Observer B", font_size=24, color=YELLOW).next_to(obs2, DOWN)
        self.play(FadeIn(obs1), FadeIn(obs2), Write(obs1_label), Write(obs2_label))

        explanation = Text(
            "When source is still,\nboth observers hear the SAME frequency.",
            font_size=28,
        ).to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(3)

        self.clear()
        self.wait(0.5)

        # --- SCENE 4: Source Moving Toward Observer (High Pitch) ---
        title4 = Text("Source Moving Toward Observer", font_size=44).to_edge(UP)
        self.play(Write(title4))

        observer = Dot([5, 0, 0], color=GREEN, radius=0.15)
        obs_label = Text("Observer", font_size=28, color=GREEN).next_to(observer, RIGHT)
        self.play(FadeIn(observer), Write(obs_label))

        # Moving source emitting wavefronts at regular time intervals
        source_moving = Dot([-5, 0, 0], color=RED, radius=0.15)
        src_label_m = Text("Moving Source →", font_size=28, color=RED).next_to(source_moving, UP)
        self.play(FadeIn(source_moving), Write(src_label_m))

        wavefronts = VGroup()
        positions = [-5, -3.5, -2, -0.5, 1, 2.5]  # source positions when emitting

        for i, pos in enumerate(positions):
            circle = Circle(radius=0.1, color=BLUE, stroke_opacity=0.7).move_to([pos, 0, 0])
            wavefronts.add(circle)

        # Animate source movement
        self.play(source_moving.animate.move_to([3, 0, 0]), run_time=5, rate_func=linear)

        # Simultaneously expand wavefronts from their emission points
        anims = []
        for i, circle in enumerate(wavefronts):
            target_radius = 5.5 - positions[i]  # distance to observer at x=5
            anims.append(circle.animate.scale(target_radius / 0.1).set_stroke(opacity=0.3))

        self.play(*anims, run_time=3, rate_func=linear)

        # Explanation
        explanation4 = Text(
            "Wavefronts bunch up ahead of the source →\nShorter wavelength → Higher frequency heard!",
            font_size=26,
        ).to_edge(DOWN)
        self.play(Write(explanation4))
        self.wait(3)

        # Show wavelength comparison
        brace_compressed = BraceBetweenPoints(
            [1, 0, 0], [2.5, 0, 0], direction=UP, color=YELLOW
        )
        brace_normal = BraceBetweenPoints(
            [-5, 0, 0], [-3.5, 0, 0], direction=UP, color=GREEN
        )
        comp_label = Text("Compressed λ", font_size=22, color=YELLOW).next_to(brace_compressed, UP)
        norm_label = Text("Normal λ", font_size=22, color=GREEN).next_to(brace_normal, UP)
        self.play(GrowFromCenter(brace_compressed), Write(comp_label))
        self.play(GrowFromCenter(brace_normal), Write(norm_label))
        self.wait(2)

        self.clear()
        self.wait(0.5)

        # --- SCENE 5: Source Moving Away from Observer (Low Pitch) ---
        title5 = Text("Source Moving Away from Observer", font_size=44).to_edge(UP)
        self.play(Write(title5))

        observer2 = Dot([-5, 0, 0], color=GREEN, radius=0.15)
        obs_label2 = Text("Observer", font_size=28, color=GREEN).next_to(observer2, LEFT)
        self.play(FadeIn(observer2), Write(obs_label2))

        source_away = Dot([3, 0, 0], color=RED, radius=0.15)
        src_label_a = Text("← Moving Source", font_size=28, color=RED).next_to(source_away, UP)
        self.play(FadeIn(source_away), Write(src_label_a))

        wavefronts2 = VGroup()
        positions2 = [3, 1.5, 0, -1.5]

        for pos in positions2:
            circle = Circle(radius=0.1, color=BLUE, stroke_opacity=0.7).move_to([pos, 0, 0])
            wavefronts2.add(circle)

        # Animate source moving away from observer
        self.play(source_away.animate.move_to([-3, 0, 0]), run_time=4, rate_func=linear)

        anims2 = []
        for i, circle in enumerate(wavefronts2):
            target_radius = abs(positions2[i] + 5) + 2  # distance to observer at x=-5
            anims2.append(circle.animate.scale(target_radius / 0.1).set_stroke(opacity=0.3))

        self.play(*anims2, run_time=3, rate_func=linear)

        explanation5 = Text(
            "Wavefronts spread out behind the source →\nLonger wavelength → Lower frequency heard!",
            font_size=26,
        ).to_edge(DOWN)
        self.play(Write(explanation5))
        self.wait(3)

        brace_stretched = BraceBetweenPoints(
            [-1.5, 0, 0], [0, 0, 0], direction=DOWN, color=YELLOW
        )
        stretch_label = Text("Stretched λ", font_size=22, color=YELLOW).next_to(brace_stretched, DOWN)
        self.play(GrowFromCenter(brace_stretched), Write(stretch_label))
        self.wait(2)

        self.clear()
        self.wait(0.5)

        # --- SCENE 6: The Doppler Formula ---
        title6 = Text("The Doppler Formula", font_size=48).to_edge(UP)
        self.play(Write(title6))
        self.wait(1)

        formula = MathTex(
            r"f' = f \cdot \frac{v \pm v_o}{v \mp v_s}",
            font_size=60,
        ).shift(UP * 0.5)
        self.play(Write(formula))
        self.wait(1)

        # Legend
        legend_items = [
            (r"f'", "observed frequency"),
            (r"f", "source frequency"),
            (r"v", "speed of wave in medium"),
            (r"v_o", "observer speed"),
            (r"v_s", "source speed"),
        ]

        legend_group = VGroup()
        for sym, desc in legend_items:
            tex_sym = MathTex(sym, font_size=36, color=YELLOW)
            desc_text = Text(f" = {desc}", font_size=28)
            row = VGroup(tex_sym, desc_text).arrange(RIGHT, buff=0.2)
            legend_group.add(row)

        legend_group.arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(DOWN * 1.5)
        for row in legend_group:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.6)
        self.wait(2)

        # Highlight the sign choices
        sign_note = Text(
            "Upper signs: source approaching, observer receding\n"
            "Lower signs: source receding, observer approaching",
            font_size=24,
            color=GREEN,
        ).to_edge(DOWN)
        self.play(Write(sign_note))
        self.wait(3)

        self.clear()
        self.wait(0.5)

        # --- SCENE 7: Everyday Examples ---
        title7 = Text("Doppler Effect in Everyday Life", font_size=48).to_edge(UP)
        self.play(Write(title7))

        # Ambulance example
        road = Line([-7, -1, 0], [7, -1, 0], color=GRAY, stroke_width=6)
        self.play(Create(road))

        ambulance = Square(side_length=0.8, color=RED, fill_opacity=0.8).move_to([-5, -0.6, 0])
        siren_text = Text("🚑", font_size=36).move_to(ambulance.get_center())
        amb_group = VGroup(ambulance, siren_text)

        observer_person = Dot([0, -1, 0], color=GREEN, radius=0.15)
        person_label = Text("You", font_size=24, color=GREEN).next_to(observer_person, DOWN)
        self.play(FadeIn(amb_group), FadeIn(observer_person), Write(person_label))

        # Approaching: higher pitch waves
        high_waves = VGroup()
        for i in range(5):
            w = MathTex(r"\sim\sim\sim", font_size=30, color=BLUE).move_to([-2 - i * 0.4, 0.5, 0])
            high_waves.add(w)
        high_label = Text("High pitch!", font_size=28, color=BLUE).move_to([0, 1.5, 0])

        self.play(amb_group.animate.move_to([0, -0.6, 0]), run_time=3, rate_func=linear)
        self.play(FadeIn(high_waves), Write(high_label))
        self.wait(1)
        self.play(FadeOut(high_waves), FadeOut(high_label))

        # Receding: lower pitch waves
        low_waves = VGroup()
        for i in range(3):
            w = MathTex(r"\sim\ \ \sim\ \ \sim", font_size=30, color=ORANGE).move_to([2 + i * 0.8, 0.5, 0])
            low_waves.add(w)
        low_label = Text("Low pitch!", font_size=28, color=ORANGE).move_to([4, 1.5, 0])

        self.play(amb_group.animate.move_to([6, -0.6, 0]), run_time=3, rate_func=linear)
        self.play(FadeIn(low_waves), Write(low_label))
        self.wait(1)

        # Combined effect note
        combined = Text(
            "As the ambulance passes you, the pitch drops!\nThis is the Doppler shift in action.",
            font_size=26,
        ).to_edge(DOWN)
        self.play(Write(combined))
        self.wait(3)

        self.clear()
        self.wait(0.5)

        # --- SCENE 8: Redshift and Blueshift (Light) ---
        title8 = Text("Doppler Effect with Light", font_size=48).to_edge(UP)
        self.play(Write(title8))

        # Spectrum
        spectrum_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        spectrum_labels = ["Red", "Orange", "Yellow", "Green", "Blue", "Violet"]
        spectrum = VGroup()
        for i, (color, label) in enumerate(zip(spectrum_colors, spectrum_labels)):
            rect = Rectangle(width=1, height=1.2, fill_opacity=0.9, color=color, stroke_width=1)
            text = Text(label, font_size=18, color=WHITE).move_to(rect.get_center())
            group = VGroup(rect, text)
            spectrum.add(group)
        spectrum.arrange(RIGHT, buff=0.05).shift(UP * 0.5)

        self.play(FadeIn(spectrum))
        self.wait(1)

        # Blueshift arrow
        blue_arrow = Arrow(
            spectrum[0].get_left() + LEFT * 2,
            spectrum[0].get_left(),
            color=BLUE,
            buff=0.1,
        )
        blue_text = Text("Approaching:\nBlueshift", font_size=26, color=BLUE).next_to(blue_arrow, LEFT)
        self.play(GrowArrow(blue_arrow), Write(blue_text))
        self.wait(1)

        # Redshift arrow
        red_arrow = Arrow(
            spectrum[-1].get_right() + RIGHT * 2,
            spectrum[-1].get_right(),
            color=RED,
            buff=0.1,
        )
        red_text = Text("Receding:\nRedshift", font_size=26, color=RED).next_to(red_arrow, RIGHT)
        self.play(GrowArrow(red_arrow), Write(red_text))
        self.wait(2)

        # Galaxy example
        galaxy = Text("🌌", font_size=60).shift(DOWN * 1.5)
        galaxy_info = Text(
            "Astronomers use redshift to discover\nthat the universe is expanding!",
            font_size=26,
        ).next_to(galaxy, DOWN)
        self.play(FadeIn(galaxy), Write(galaxy_info))
        self.wait(3)

        self.clear()
        self.wait(0.5)

        # --- SCENE 9: Numerical Example ---
        title9 = Text("Let's Solve a Problem!", font_size=48).to_edge(UP)
        self.play(Write(title9))
        self.wait(1)

        problem = VGroup(
            Text("An ambulance siren emits f = 700 Hz.", font_size=28),
            Text("Speed of sound: v = 340 m/s", font_size=28),
            Text("Ambulance speed: v_s = 30 m/s (toward you)", font_size=28),
            Text("You are stationary: v_o = 0 m/s", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(UP * 1)

        for line in problem:
            self.play(Write(line), run_time=0.8)
        self.wait(1)

        # Apply formula
        formula_apply = MathTex(
            r"f' = 700 \cdot \frac{340}{340 - 30}",
            font_size=48,
        ).shift(DOWN * 1)
        self.play(Write(formula_apply))
        self.wait(1)

        formula_calc = MathTex(
            r"f' = 700 \cdot \frac{340}{310}",
            font_size=48,
        ).shift(DOWN * 1)
        self.play(Transform(formula_apply, formula_calc))
        self.wait(1)

        result = MathTex(
            r"f' \approx 767.7 \text{ Hz}",
            font_size=52,
            color=YELLOW,
        ).shift(DOWN * 2)
        self.play(Write(result))

        conclusion = Text(
            "The pitch rises by about 68 Hz — you can hear the difference!",
            font_size=26,
            color=GREEN,
        ).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(4)

        self.clear()
        self.wait(0.5)

        # --- SCENE 10: Summary ---
        title10 = Text("Summary: The Doppler Effect", font_size=48).to_edge(UP)
        self.play(Write(title10))

        summary_points = VGroup(
            Text("✓ Waves bunch up when source approaches → higher frequency", font_size=26),
            Text("✓ Waves spread out when source recedes → lower frequency", font_size=26),
            Text("✓ Applies to sound, light, and all types of waves", font_size=26),
            Text("✓ Formula:  f' = f · (v ± v₀) / (v ∓ vₛ)", font_size=26),
            Text("✓ Key insight: frequency depends on relative motion", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN * 0.3)

        for point in summary_points:
            self.play(FadeIn(point, shift=RIGHT * 0.5), run_time=0.8)
            self.wait(0.5)

        self.wait(1)

        # Final animated wavefronts
        final_source = Dot([-3, -2.5, 0], color=RED, radius=0.12)
        final_observer = Dot([3, -2.5, 0], color=GREEN, radius=0.12)
        self.play(FadeIn(final_source), FadeIn(final_observer))

        final_waves = VGroup()
        for i in range(6):
            c = Circle(
                radius=0.5 + i * 0.7,
                color=BLUE,
                stroke_width=2,
                stroke_opacity=0.6 - i * 0.08,
            ).move_to(final_source.get_center())
            final_waves.add(c)

        self.play(
            *[Create(c) for c in final_waves],
            run_time=3,
        )

        thanks = Text("Thank you for learning about the Doppler Effect!", font_size=32, color=YELLOW).to_edge(DOWN)
        self.play(Write(thanks))
        self.wait(3)
