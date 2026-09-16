from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Introduction
        title = Text("The Doppler Effect", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        src = Dot(color=RED).shift(LEFT * 3)
        src_label = Text("Source", font_size=24, color=RED).next_to(src, DOWN)
        obs = Dot(color=BLUE).shift(RIGHT * 3)
        obs_label = Text("Observer", font_size=24, color=BLUE).next_to(obs, DOWN)
        self.play(Create(src), Create(obs), Write(src_label), Write(obs_label))
        for _ in range(3):
            c = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(src.get_center())
            self.add(c)
            self.play(c.animate.scale(60), run_time=2)
            self.remove(c)
        self.wait()
        self.clear()

        # Scene 2: Stationary source and observer, constant frequency
        self.play(FadeIn(Text("Stationary source & observer: constant frequency", font_size=28)))
        src = Dot(color=RED).shift(LEFT * 3)
        obs = Dot(color=BLUE).shift(RIGHT * 3)
        eq = MathTex("f = \\frac{1}{T}", font_size=36).next_to(src, UP)
        self.add(src, obs, eq)
        for _ in range(4):
            c = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(src.get_center())
            self.add(c)
            self.play(c.animate.scale(60), run_time=2)
            self.play(obs.animate.scale(1.5).set_color(WHITE), run_time=0.1)
            self.play(obs.animate.scale(1 / 1.5).set_color(BLUE), run_time=0.1)
            self.remove(c)
        self.wait()
        self.clear()

        # Scene 3: Observer moving towards source
        self.play(FadeIn(Text("Observer moves towards source: higher frequency", font_size=28)))
        src = Dot(color=RED).shift(LEFT * 3)
        obs = Dot(color=BLUE).shift(RIGHT * 4)
        self.add(src, obs)
        for _ in range(5):
            c = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(src.get_center())
            self.add(c)
            self.play(c.animate.scale(60), obs.animate.shift(LEFT * 0.6), run_time=1.2)
            self.remove(c)
            self.play(obs.animate.scale(1.3).set_color(WHITE), run_time=0.05)
            self.play(obs.animate.scale(1 / 1.3).set_color(BLUE), run_time=0.05)
        self.wait()
        self.clear()

        # Scene 4: Observer moving away from source
        self.play(FadeIn(Text("Observer moves away: lower frequency", font_size=28)))
        src = Dot(color=RED).shift(LEFT * 3)
        obs = Dot(color=BLUE).shift(RIGHT * 1)
        self.add(src, obs)
        for _ in range(5):
            c = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(src.get_center())
            self.add(c)
            self.play(c.animate.scale(60), obs.animate.shift(RIGHT * 0.6), run_time=1.2)
            self.remove(c)
            self.play(obs.animate.scale(1.3).set_color(WHITE), run_time=0.05)
            self.play(obs.animate.scale(1 / 1.3).set_color(BLUE), run_time=0.05)
        self.wait()
        self.clear()

        # Scene 5: Source moving towards stationary observer
        self.play(FadeIn(Text("Source moves towards observer: wavefronts bunch up", font_size=28)))
        src = Dot(color=RED).shift(LEFT * 5)
        obs = Dot(color=BLUE).shift(RIGHT * 3)
        self.add(src, obs)
        for _ in range(5):
            c = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(src.get_center())
            self.add(c)
            self.play(c.animate.scale(80), src.animate.shift(RIGHT * 0.8), run_time=1.5)
            self.remove(c)
            self.play(obs.animate.scale(1.3).set_color(WHITE), run_time=0.05)
            self.play(obs.animate.scale(1 / 1.3).set_color(BLUE), run_time=0.05)
        self.wait()
        self.clear()

        # Scene 6: Source moving away from stationary observer
        self.play(FadeIn(Text("Source moves away: wavefronts spread out", font_size=28)))
        src = Dot(color=RED).shift(LEFT * 1)
        obs = Dot(color=BLUE).shift(RIGHT * 4)
        self.add(src, obs)
        for _ in range(5):
            c = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(src.get_center())
            self.add(c)
            self.play(c.animate.scale(80), src.animate.shift(LEFT * 0.8), run_time=1.5)
            self.remove(c)
            self.play(obs.animate.scale(1.3).set_color(WHITE), run_time=0.05)
            self.play(obs.animate.scale(1 / 1.3).set_color(BLUE), run_time=0.05)
        self.wait()
        self.clear()

        # Scene 7: Summary
        self.play(FadeIn(Text("Doppler Effect Summary", font_size=40, color=YELLOW).to_edge(UP)))
        formula = MathTex("f' = f \\frac{v}{v \\mp v_s}", font_size=36).shift(UP)
        self.play(Write(formula))
        blue_txt = Text("Approaching: higher frequency (blue shift)", color=BLUE, font_size=28).shift(DOWN * 0.5)
        red_txt = Text("Receding: lower frequency (red shift)", color=RED, font_size=28).shift(DOWN * 1.5)
        self.play(Write(blue_txt), Write(red_txt))
        src = Dot(color=RED).shift(LEFT * 3)
        obs = Dot(color=BLUE).shift(RIGHT * 3)
        self.add(src, obs)
        for _ in range(3):
            c = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(src.get_center())
            self.add(c)
            self.play(c.animate.scale(60), run_time=1.5)
            self.remove(c)
        self.wait()