from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Introduction
        title = Text("The Doppler Effect", font_size=64)
        subtitle = Text("Apparent frequency shift due to relative motion", font_size=32).next_to(title, DOWN)
        intro = VGroup(title, subtitle)
        self.play(FadeIn(intro, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(intro))
        self.clear()

        # Scene 2: First principles - wave propagation
        title2 = Text("Wavefronts from a stationary source", font_size=48)
        source = Dot(radius=0.15, color=YELLOW).shift(LEFT*3)
        source_label = Text("Source", font_size=24).next_to(source, DOWN)
        wave_group = VGroup()
        for i in range(4):
            ring = Circle(radius=0.5 + i*0.8, color=BLUE, stroke_width=2).move_to(source.get_center())
            wave_group.add(ring)
        self.play(Write(title2), FadeIn(source), Write(source_label))
        self.play(Create(wave_group[0]), run_time=0.8)
        self.play(Transform(wave_group[0], Circle(radius=1.3, color=BLUE, stroke_width=2).move_to(source.get_center())))
        self.play(Create(wave_group[1]), run_time=0.8)
        self.play(Transform(wave_group[1], Circle(radius=1.3, color=BLUE, stroke_width=2).move_to(source.get_center())))
        self.play(Create(wave_group[2]), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(title2), FadeOut(source), FadeOut(source_label), FadeOut(wave_group))
        self.clear()

        # Scene 3: Moving source - wave compression
        title3 = Text("Source moving to the right", font_size=48)
        source_m = Dot(radius=0.15, color=YELLOW).shift(LEFT*4)
        source_label_m = Text("Source", font_size=24).next_to(source_m, DOWN)
        self.play(Write(title3), FadeIn(source_m), Write(source_label_m))
        path = Line(LEFT*4, RIGHT*2)
        wave_positions = [LEFT*4 + RIGHT*i*0.5 for i in range(6)]
        rings = VGroup()
        for i in range(6):
            r = Circle(radius=0.2, color=BLUE, stroke_width=2).move_to(wave_positions[i])
            rings.add(r)
        self.play(MoveAlongPath(source_m, path), run_time=4, rate_func=linear)
        self.play(*[Create(r) for r in rings], lag_ratio=0.3)
        self.play(*[GrowFromCenter(r) for r in rings], run_time=2)
        self.wait(0.5)
        self.play(FadeOut(title3), FadeOut(source_m), FadeOut(source_label_m), FadeOut(rings))
        self.clear()

        # Scene 4: Observer sees higher frequency ahead
        title4 = Text("Observer ahead receives waves more often", font_size=44)
        observer = Dot(radius=0.15, color=RED).shift(RIGHT*3)
        obs_label = Text("Observer", font_size=24).next_to(observer, DOWN)
        source2 = Dot(radius=0.15, color=YELLOW).shift(LEFT*3)
        self.play(Write(title4), FadeIn(source2), FadeIn(observer), Write(obs_label))
        arrow = Arrow(source2.get_center(), observer.get_center(), color=GREEN)
        self.play(Create(arrow))
        freq_text = MathTex("f' > f_0", color=GREEN).next_to(observer, UP)
        self.play(Write(freq_text))
        self.play(source2.animate.shift(RIGHT*0.5), run_time=1)
        self.play(source2.animate.shift(RIGHT*0.5), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(title4), FadeOut(source2), FadeOut(observer), FadeOut(obs_label), FadeOut(arrow), FadeOut(freq_text))
        self.clear()

        # Scene 5: Observer moving towards source
        title5 = Text("Moving observer: frequency increases when approaching", font_size=44)
        source_s = Dot(radius=0.15, color=YELLOW).shift(LEFT*3)
        observer_m = Dot(radius=0.15, color=RED).shift(RIGHT*3)
        label_s = Text("Source", font_size=24).next_to(source_s, DOWN)
        label_o = Text("Observer →", font_size=24).next_to(observer_m, DOWN)
        self.play(Write(title5), FadeIn(source_s), FadeIn(observer_m), Write(label_s), Write(label_o))
        wave_line = VGroup(*[Line(source_s.get_center(), RIGHT*4, color=BLUE, stroke_width=3).set_opacity(0.3) for _ in range(5)])
        self.play(FadeIn(wave_line))
        self.play(observer_m.animate.shift(LEFT*2), run_time=2)
        freq_text2 = MathTex("f' = f_0 \\frac{v + v_o}{v}", color=GREEN).next_to(observer_m, UP)
        self.play(Write(freq_text2))
        self.wait(1)
        self.play(FadeOut(title5), FadeOut(source_s), FadeOut(observer_m), FadeOut(label_s), FadeOut(label_o), FadeOut(wave_line), FadeOut(freq_text2))
        self.clear()

        # Scene 6: Summary
        title6 = Text("Doppler Effect Summary", font_size=56)
        eq = MathTex(r"f' = f_0 \frac{v \pm v_o}{v \mp v_s}", font_size=48).next_to(title6, DOWN)
        note1 = Text("Upper signs: observer/source approaching", font_size=28).next_to(eq, DOWN, buff=0.5)
        note2 = Text("Lower signs: receding", font_size=28).next_to(note1, DOWN)
        summary = VGroup(title6, eq, note1, note2)
        self.play(FadeIn(summary))
        self.wait(2)
        self.play(FadeOut(summary))
