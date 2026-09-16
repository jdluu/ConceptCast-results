from manim import *


class SceneGen(Scene):
    def construct(self):
        # Scene One
        title = Text("Scene One", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Scene Two
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle))
        self.wait(1)
        square = Square(side_length=2, color=RED)
        self.play(Transform(circle, square))
        self.wait(1)
        self.play(FadeOut(circle))

        # Scene Three
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5,
        )
        graph = axes.plot(lambda x: np.sin(x), color=YELLOW)
        labels = axes.get_axis_labels(x_label="x", y_label="sin(x)")
        self.play(Create(axes), Write(labels))
        self.play(Create(graph))
        self.wait(2)
        self.play(FadeOut(axes), FadeOut(graph), FadeOut(labels))

        # Scene Four
        formula = MathTex(r"\int_{0}^{\infty} e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}")
        self.play(Write(formula))
        self.wait(2)
        self.play(FadeOut(formula))

        # Scene Five
        dots = VGroup(*[Dot(point=[-4 + i, np.sin(i), 0]) for i in np.linspace(0, 8, 9)])
        self.play(Create(dots), run_time=2)
        self.wait(1)
        self.play(dots.animate.arrange(RIGHT, buff=0.5))
        self.wait(2)
        self.play(FadeOut(dots))
