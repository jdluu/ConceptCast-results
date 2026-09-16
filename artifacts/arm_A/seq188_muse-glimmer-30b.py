from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Introduction
        title = Text("Doppler Effect", font_size=72)
        subtitle = Text("Apparent shift in frequency due to relative motion", font_size=36).next_to(title, DOWN)
        self.play(FadeIn(title, shift=UP), run_time=1)
        self.play(FadeIn(subtitle, shift=UP), run_time=1)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))
        self.clear()

        # Scene 2: Wave concept from stationary source
        source = Dot(color=RED, radius=0.15).shift(LEFT*3)
        source_label = Text("Source", font_size=24).next_to(source, DOWN)
        wave1 = Circle(radius=0.5, color=BLUE).move_to(source)
        wave2 = Circle(radius=1.0, color=BLUE).move_to(source)
        wave3 = Circle(radius=1.5, color=BLUE).move_to(source)
        label = Text("Stationary source emits regular wavefronts", font_size=28).to_edge(UP)
        self.play(FadeIn(source), Write(source_label), FadeIn(label))
        self.play(Create(wave1), Create(wave2), Create(wave3))
        self.play(wave1.animate.scale(1.5), wave2.animate.scale(1.5), wave3.animate.scale(1.5), run_time=2)
        self.wait(0.5)
        self.play(FadeOut(source), FadeOut(source_label), FadeOut(wave1), FadeOut(wave2), FadeOut(wave3), FadeOut(label))
        self.clear()

        # Scene 3: Source moving towards observer
        observer = Dot(color=GREEN, radius=0.15).shift(RIGHT*3)
        obs_label = Text("Observer", font_size=24).next_to(observer, DOWN)
        src_move = Dot(color=RED, radius=0.15).shift(LEFT*4)
        src_label = Text("Moving Source", font_size=24).next_to(src_move, DOWN)
        wave_a = Circle(radius=0.6, color=YELLOW).move_to(src_move)
        wave_b = Circle(radius=0.6, color=YELLOW).move_to(src_move)
        text_front = Text("Waves compressed in front", font_size=28).to_edge(UP)
        self.play(FadeIn(observer), Write(obs_label), FadeIn(src_move), Write(src_label), FadeIn(text_front))
        self.play(src_move.animate.shift(RIGHT*0.8), run_time=1)
        self.play(Create(wave_a))
        self.play(src_move.animate.shift(RIGHT*0.8), run_time=1)
        self.play(Create(wave_b))
        self.play(wave_a.animate.scale(1.8).move_to(src_move), wave_b.animate.scale(1.8).move_to(src_move), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(observer), FadeOut(obs_label), FadeOut(src_move), FadeOut(src_label), FadeOut(wave_a), FadeOut(wave_b), FadeOut(text_front))
        self.clear()

        # Scene 4: Observer moving towards source
        src_stationary = Dot(color=RED, radius=0.15).shift(LEFT*3)
        obs_move = Dot(color=GREEN, radius=0.15).shift(RIGHT*4)
        waves = VGroup(*[Circle(radius=r, color=BLUE).move_to(src_stationary) for r in [0.5,1.0,1.5]])
        text_obs = Text("Observer moving toward source", font_size=28).to_edge(UP)
        self.play(FadeIn(src_stationary), FadeIn(obs_move), FadeIn(text_obs))
        self.play(*[Create(w) for w in waves])
        self.play(obs_move.animate.shift(LEFT*1.5), run_time=2)
        self.play(obs_move.animate.shift(LEFT*1.5), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(src_stationary), FadeOut(obs_move), FadeOut(waves), FadeOut(text_obs))
        self.clear()

        # Scene 5: Frequency change visualization
        freq_low = Text("f_observed < f_emitted", font_size=36, color=RED).shift(DOWN*1)
        freq_high = Text("f_observed > f_emitted", font_size=36, color=GREEN).shift(DOWN*1)
        arrow = Arrow(LEFT*3, RIGHT*3, color=WHITE)
        self.play(FadeIn(arrow))
        self.play(FadeIn(Text("Source moving away", font_size=32).next_to(arrow, UP)))
        self.play(Write(freq_low), run_time=1)
        self.wait(1)
        self.play(FadeOut(freq_low), FadeOut(arrow))
        self.play(FadeIn(Arrow(RIGHT*3, LEFT*3, color=WHITE)))
        self.play(FadeIn(Text("Source moving toward", font_size=32).next_to(arrow, UP)))
        self.play(Write(freq_high), run_time=1)
        self.wait(1)
        self.play(FadeOut(freq_high))
        self.clear()

        # Scene 6: Formula
        formula = MathTex(r"f' = f \frac{v \pm v_o}{v \mp v_s}", font_size=72)
        expl1 = Text("v = wave speed", font_size=28).next_to(formula, DOWN)
        expl2 = Text("v_o = observer speed, v_s = source speed", font_size=28).next_to(expl1, DOWN)
        self.play(Write(formula))
        self.play(Write(expl1), Write(expl2))
        self.wait(2)
        self.play(FadeOut(formula), FadeOut(expl1), FadeOut(expl2))
        self.clear()

        # Scene 7: Real world summary
        examples = VGroup(
            Text("Sirens", font_size=36, color=YELLOW),
            Text("Redshift of galaxies", font_size=36, color=BLUE),
            Text("Bat echolocation", font_size=36, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).shift(UP*0.5)
        title2 = Text("Real World Applications", font_size=48).to_edge(UP)
        self.play(FadeIn(title2))
        for ex in examples:
            self.play(Write(ex), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(title2), FadeOut(examples))
