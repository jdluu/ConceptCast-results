from manim import *

class SceneGen(Scene):
    def construct(self):
        self.scene1()
        self.clear()
        self.scene2()
        self.clear()
        self.scene3()
        self.clear()
        self.scene4()
        self.clear()
        self.scene5()
        self.clear()
        self.scene6()
        self.clear()
        self.scene7()

    def scene1(self):
        title = Text("Doppler Effect: Stationary Source & Observer", color=WHITE).to_edge(UP)
        source = Dot(point=LEFT*3, color=RED)
        observer = Dot(point=RIGHT*3, color=BLUE)
        s_label = Text("Source", color=RED).next_to(source, DOWN)
        o_label = Text("Observer", color=BLUE).next_to(observer, DOWN)
        self.play(FadeIn(title), FadeIn(source), FadeIn(observer), FadeIn(s_label), FadeIn(o_label))
        for i in range(4):
            wave = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(source.get_center())
            self.add(wave)
            self.play(wave.animate.scale(60).set_opacity(0), run_time=1.5, rate_func=linear)
        self.wait(0.5)
        self.play(FadeOut(title), FadeOut(source), FadeOut(observer), FadeOut(s_label), FadeOut(o_label))

    def scene2(self):
        title = Text("Frequency: waves passing per second", color=WHITE).to_edge(UP)
        source = Dot(LEFT*3, color=RED)
        observer = Dot(RIGHT*3, color=BLUE)
        self.play(FadeIn(title), FadeIn(source), FadeIn(observer))
        tex = MathTex("f = \\frac{1}{T}").next_to(title, DOWN)
        self.play(Write(tex))
        counter = Integer(0, color=YELLOW).next_to(observer, UP)
        self.play(FadeIn(counter))
        for i in range(5):
            wave = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(source.get_center())
            self.add(wave)
            self.play(wave.animate.scale(60).set_opacity(0), run_time=1.0, rate_func=linear)
            self.play(counter.animate.set_value(i+1), run_time=0.2)
        self.wait(0.5)
        self.play(FadeOut(title), FadeOut(source), FadeOut(observer), FadeOut(tex), FadeOut(counter))

    def scene3(self):
        title = Text("Observer moving TOWARDS source", color=WHITE).to_edge(UP)
        source = Dot(LEFT*4, color=RED)
        self.play(FadeIn(title), FadeIn(source))
        observer = Dot(RIGHT*4, color=BLUE)
        arrow = Arrow(observer.get_center(), observer.get_center()+LEFT*1, color=BLUE)
        self.play(FadeIn(observer), FadeIn(arrow))
        for i in range(4):
            wave = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(source.get_center())
            self.add(wave)
            self.play(
                wave.animate.scale(80).set_opacity(0),
                observer.animate.shift(LEFT*0.6),
                arrow.animate.shift(LEFT*0.6),
                run_time=1.4, rate_func=linear
            )
        tex = Text("Higher frequency (higher pitch)", color=GREEN).next_to(title, DOWN)
        self.play(Write(tex))
        self.wait(0.5)
        self.play(FadeOut(title), FadeOut(source), FadeOut(observer), FadeOut(arrow), FadeOut(tex))

    def scene4(self):
        title = Text("Observer moving AWAY from source", color=WHITE).to_edge(UP)
        source = Dot(LEFT*4, color=RED)
        self.play(FadeIn(title), FadeIn(source))
        observer = Dot(RIGHT*2, color=BLUE)
        arrow = Arrow(observer.get_center(), observer.get_center()+RIGHT*1, color=BLUE)
        self.play(FadeIn(observer), FadeIn(arrow))
        for i in range(4):
            wave = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(source.get_center())
            self.add(wave)
            self.play(
                wave.animate.scale(80).set_opacity(0),
                observer.animate.shift(RIGHT*0.6),
                arrow.animate.shift(RIGHT*0.6),
                run_time=1.4, rate_func=linear
            )
        tex = Text("Lower frequency (lower pitch)", color=RED).next_to(title, DOWN)
        self.play(Write(tex))
        self.wait(0.5)
        self.play(FadeOut(title), FadeOut(source), FadeOut(observer), FadeOut(arrow), FadeOut(tex))

    def scene5(self):
        title = Text("Source moving TOWARDS observer", color=WHITE).to_edge(UP)
        observer = Dot(RIGHT*4, color=BLUE)
        self.play(FadeIn(title), FadeIn(observer))
        source = Dot(LEFT*4, color=RED)
        arrow = Arrow(source.get_center(), source.get_center()+RIGHT*1, color=RED)
        self.play(FadeIn(source), FadeIn(arrow))
        for i in range(5):
            wave = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(source.get_center())
            self.add(wave)
            self.play(
                wave.animate.scale(80).set_opacity(0),
                source.animate.shift(RIGHT*0.7),
                arrow.animate.shift(RIGHT*0.7),
                run_time=1.2, rate_func=linear
            )
        tex = Text("Wavefronts compressed -> higher freq", color=GREEN).next_to(title, DOWN)
        self.play(Write(tex))
        self.wait(0.5)
        self.play(FadeOut(title), FadeOut(source), FadeOut(observer), FadeOut(arrow), FadeOut(tex))

    def scene6(self):
        title = Text("Source moving AWAY from observer", color=WHITE).to_edge(UP)
        observer = Dot(RIGHT*4, color=BLUE)
        self.play(FadeIn(title), FadeIn(observer))
        source = Dot(LEFT*2, color=RED)
        arrow = Arrow(source.get_center(), source.get_center()+LEFT*1, color=RED)
        self.play(FadeIn(source), FadeIn(arrow))
        for i in range(5):
            wave = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(source.get_center())
            self.add(wave)
            self.play(
                wave.animate.scale(80).set_opacity(0),
                source.animate.shift(LEFT*0.7),
                arrow.animate.shift(LEFT*0.7),
                run_time=1.2, rate_func=linear
            )
        tex = Text("Wavefronts stretched -> lower freq", color=RED).next_to(title, DOWN)
        self.play(Write(tex))
        self.wait(0.5)
        self.play(FadeOut(title), FadeOut(source), FadeOut(observer), FadeOut(arrow), FadeOut(tex))

    def scene7(self):
        title = Text("Doppler Effect Summary", color=WHITE).to_edge(UP)
        self.play(FadeIn(title))
        formula = MathTex("f' = f \\left( \\frac{v \\pm v_o}{v \\mp v_s} \\right)").scale(1.2)
        self.play(Write(formula))
        explain = Text(
            "Observer towards source: +v_o\nSource towards observer: -v_s\nObserver away: -v_o\nSource away: +v_s",
            color=YELLOW
        ).next_to(formula, DOWN)
        self.play(Write(explain))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(formula), FadeOut(explain))