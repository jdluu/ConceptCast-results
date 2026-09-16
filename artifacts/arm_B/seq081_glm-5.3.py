from manim import *


class SceneGen(Scene):
    def construct(self):
        # ------------------------------------------------------------
        # Scene 1: What is a wave? (source at rest, circular wavefronts)
        # ------------------------------------------------------------
        title = Text("The Doppler Effect", font_size=40).to_edge(UP)
        subtitle = Text("Part 1: Waves from a stationary source", font_size=24).next_to(title, DOWN)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3))

        source = Dot(radius=0.12, color=RED).move_to(ORIGIN)
        source_label = Text("Source", font_size=22, color=RED).next_to(source, DOWN, buff=0.3)
        self.play(FadeIn(source, scale=2), Write(source_label))

        waves = VGroup()
        for i in range(5):
            c = Circle(radius=0.4 + i * 0.7, color=BLUE, stroke_opacity=0.9)
            waves.add(c)
        self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.2), run_time=3)
        self.play(
            waves.animate.set(stroke_opacity=0.3),
            run_time=1,
        )
        note = Text(
            "Each circle is a wavefront emitted at a regular period T",
            font_size=22,
        ).to_edge(DOWN)
        self.play(Write(note), run_time=1.5)
        self.wait(1.5)
        self.clear()

        # ------------------------------------------------------------
        # Scene 2: Wavelength and frequency
        # ------------------------------------------------------------
        t2 = Text("Part 2: Wavelength and frequency", font_size=32).to_edge(UP)
        self.play(Write(t2))

        c1 = Circle(radius=1.0, color=BLUE).move_to(LEFT * 3)
        c2 = Circle(radius=2.0, color=BLUE).move_to(LEFT * 3)
        src = Dot(radius=0.12, color=RED).move_to(LEFT * 3)
        self.play(Create(c1), Create(c2), FadeIn(src, scale=2))

        brace = Brace(VGroup(c1, c2), RIGHT, buff=0.1)
        lam = MathTex(r"\lambda", font_size=44)
        brace_label = brace.get_tex(r"\lambda")
        self.play(GrowFromCenter(brace), Write(brace_label))

        eq = MathTex(r"f = \frac{1}{T} = \frac{v}{\lambda}", font_size=44).to_edge(DOWN)
        self.play(Write(eq), run_time=1.5)

        lam_def = Text(
            "λ = distance between successive wavefronts",
            font_size=22,
        ).next_to(eq, UP, buff=0.5).to_edge(RIGHT)
        self.play(FadeIn(lam_def, shift=LEFT))
        self.wait(1.5)
        self.play(FadeOut(VGroup(t2, c1, c2, src, brace, brace_label, eq, lam_def)))
        self.clear()

        # ------------------------------------------------------------
        # Scene 3: The source starts moving
        # ------------------------------------------------------------
        t3 = Text("Part 3: Now the source moves", font_size=32).to_edge(UP)
        self.play(Write(t3))

        moving_src = Dot(radius=0.12, color=RED).move_to(LEFT * 4)
        label = Text("moving source", font_size=22, color=RED).next_to(moving_src, DOWN, buff=0.3)
        self.play(FadeIn(moving_src, scale=2), Write(label))

        front_waves = VGroup()
        for i in range(4):
            c = Circle(radius=0.5 + i * 0.8, color=BLUE, stroke_opacity=0.8)
            c.move_to(LEFT * 4 + RIGHT * (0.6 * i))
            front_waves.add(c)
        self.play(LaggedStart(*[Create(c) for c in front_waves], lag_ratio=0.2), run_time=2.5)

        crowded = Text(
            "Wavefronts bunch up ahead, spread out behind",
            font_size=22,
        ).to_edge(DOWN)
        self.play(Write(crowded))

        arrow = Arrow(LEFT * 4 + DOWN * 2.2, LEFT * 4 + DOWN * 2.2 + RIGHT * 2, color=YELLOW)
        self.play(GrowArrow(arrow))
        self.wait(1.5)
        self.clear()

        # ------------------------------------------------------------
        # Scene 4: Shorter wavelength ahead (blueshift)
        # ------------------------------------------------------------
        t4 = Text("Part 4: Ahead of the source — shorter λ", font_size=32).to_edge(UP)
        self.play(Write(t4))

        s = Dot(radius=0.12, color=RED).move_to(ORIGIN)
        self.play(FadeIn(s, scale=2))

        tight = VGroup()
        for i in range(4):
            c = Circle(radius=0.4 + i * 0.45, color=BLUE, stroke_opacity=0.9)
            tight.add(c)
        self.play(LaggedStart(*[Create(c) for c in tight], lag_ratio=0.15), run_time=2)

        b1 = Brace(tight[0], RIGHT, buff=0.05, color=BLUE)
        l1 = b1.get_tex(r"\lambda_{\text{short}}")
        self.play(GrowFromCenter(b1), Write(l1))

        obs = Dot(radius=0.1, color=GREEN).move_to(RIGHT * 2.5)
        obs_label = Text("Observer", font_size=22, color=GREEN).next_to(obs, UP, buff=0.2)
        self.play(FadeIn(obs, scale=2), Write(obs_label))

        msg = MathTex(
            r"\lambda' < \lambda \;\Rightarrow\; f' > f",
            font_size=40,
        ).to_edge(DOWN)
        blue = Text("Higher pitch (blueshift)", font_size=22, color=BLUE).next_to(msg, UP, buff=0.4)
        self.play(Write(msg), run_time=1.5)
        self.play(FadeIn(blue, shift=UP * 0.3))
        self.wait(1.5)
        self.clear()

        # ------------------------------------------------------------
        # Scene 5: Longer wavelength behind (redshift)
        # ------------------------------------------------------------
        t5 = Text("Part 5: Behind the source — longer λ", font_size=32).to_edge(UP)
        self.play(Write(t5))

        s2 = Dot(radius=0.12, color=RED).move_to(ORIGIN)
        self.play(FadeIn(s2, scale=2))

        wide = VGroup()
        for i in range(4):
            c = Circle(radius=0.6 + i * 1.1, color=BLUE, stroke_opacity=0.9)
            wide.add(c)
        self.play(LaggedStart(*[Create(c) for c in wide], lag_ratio=0.15), run_time=2)

        b2 = Brace(wide[0], LEFT, buff=0.05, color=BLUE)
        l2 = b2.get_tex(r"\lambda_{\text{long}}")
        self.play(GrowFromCenter(b2), Write(l2))

        obs2 = Dot(radius=0.1, color=GREEN).move_to(LEFT * 3.5)
        obs2_label = Text("Observer", font_size=22, color=GREEN).next_to(obs2, UP, buff=0.2)
        self.play(FadeIn(obs2, scale=2), Write(obs2_label))

        msg2 = MathTex(
            r"\lambda' > \lambda \;\Rightarrow\; f' < f",
            font_size=40,
        ).to_edge(DOWN)
        red = Text("Lower pitch (redshift)", font_size=22, color=RED).next_to(msg2, UP, buff=0.4)
        self.play(Write(msg2), run_time=1.5)
        self.play(FadeIn(red, shift=UP * 0.3))
        self.wait(1.5)
        self.clear()

        # ------------------------------------------------------------
        # Scene 6: The Doppler formula
        # ------------------------------------------------------------
        t6 = Text("Part 6: The Doppler formula", font_size=32).to_edge(UP)
        self.play(Write(t6))

        formula = MathTex(
            r"f' = f \,\frac{v \pm v_o}{v \mp v_s}",
            font_size=56,
        ).shift(UP * 1)
        self.play(Write(formula), run_time=2)

        legend = VGroup(
            MathTex(r"v = \text{wave speed}", font_size=30),
            MathTex(r"v_s = \text{source speed}", font_size=30),
            MathTex(r"v_o = \text{observer speed}", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN * 1)
        box = SurroundingRectangle(legend, color=YELLOW, buff=0.3)
        self.play(FadeIn(legend, shift=RIGHT * 0.5), Create(box))

        hint = Text(
            "Top signs: motion toward each other (f' > f)",
            font_size=22,
        ).to_edge(DOWN)
        self.play(Write(hint))
        self.wait(1.5)
        self.play(FadeOut(VGroup(t6, formula, legend, box, hint)))
        self.clear()

        # ------------------------------------------------------------
        # Scene 7: Everyday examples and summary
        # ------------------------------------------------------------
        t7 = Text("Part 7: The Doppler effect in daily life", font_size=32).to_edge(UP)
        self.play(Write(t7))

        car = VGroup(
            Rectangle(width=1.2, height=0.5, color=GREY),
            Circle(radius=0.15, color=BLACK).move_to(LEFT * 0.35 + DOWN * 0.35),
            Circle(radius=0.15, color=BLACK).move_to(RIGHT * 0.35 + DOWN * 0.35),
        ).move_to(LEFT * 4 + DOWN * 1)
        self.play(FadeIn(car, shift=UP))

        approaching = Text("f' > f  (higher pitch)", font_size=24, color=BLUE).move_to(RIGHT * 2.5 + UP * 0.5)
        receding = Text("f' < f  (lower pitch)", font_size=24, color=RED).move_to(RIGHT * 2.5 + DOWN * 0.5)
        self.play(Write(approaching), Write(receding))

        self.play(car.animate.shift(RIGHT * 8), run_time=3)
        self.play(
            approaching.animate.set(color=BLUE),
            receding.animate.set(color=RED),
        )

        summary = VGroup(
            Text("Summary", font_size=28, color=YELLOW),
            Text("• Motion toward → compressed wavefronts → higher f", font_size=22),
            Text("• Motion away → stretched wavefronts → lower f", font_size=22),
            Text("• Applies to sound, light, and all waves", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN).shift(UP * 0.3)
        self.play(FadeIn(summary, shift=UP))
        self.wait(2.5)
        self.clear()
