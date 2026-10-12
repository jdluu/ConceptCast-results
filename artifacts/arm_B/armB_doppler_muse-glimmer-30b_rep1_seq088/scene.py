from manim import *

class SceneGen(Scene):
    def construct(self):
        # WavesRight
        source = Dot()
        self.add(source)
        waves = VGroup(*[Circle(radius=r, color=YELLOW, stroke_width=2).move_to(source.get_center()) for r in [0.3,0.8,1.3]])
        self.play(*[FadeIn(w) for w in waves], run_time=1.5)
        self.play(*[w.animate.scale(1.5) for w in waves], run_time=2)
        front1 = Circle(radius=0.4, color=YELLOW).move_to(source.get_center())
        front2 = Circle(radius=0.4, color=YELLOW).move_to(source.get_center()+RIGHT*1.5)
        front3 = Circle(radius=0.4, color=YELLOW).move_to(source.get_center()+RIGHT*3)
        self.play(front1.animate.move_to(source.get_center()+RIGHT*0.6),
                  front2.animate.move_to(source.get_center()+RIGHT*2.1),
                  front3.animate.move_to(source.get_center()+RIGHT*3.6))
        self.wait()
        self.clear()

        # WavesLeft
        source = Dot()
        self.add(source)
        front1 = Circle(radius=0.4, color=YELLOW).move_to(source.get_center())
        front2 = Circle(radius=0.4, color=YELLOW).move_to(source.get_center()+LEFT*1.5)
        front3 = Circle(radius=0.4, color=YELLOW).move_to(source.get_center()+LEFT*3)
        self.play(front1.animate.move_to(source.get_center()+LEFT*0.6),
                  front2.animate.move_to(source.get_center()+LEFT*2.1),
                  front3.animate.move_to(source.get_center()+LEFT*3.6))
        self.wait()
        self.clear()

        # WavesGeneral
        source = Dot()
        self.add(source)
        waves = VGroup(*[Circle(radius=0.5, color=YELLOW, stroke_width=2).move_to(source.get_center()) for _ in range(3)])
        self.play(*[FadeIn(w) for w in waves], run_time=1.5)
