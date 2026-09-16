from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Title
        title = Text("The Script Is Fixed").scale(0.9)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Scene 2: Shapes
        circle = Circle(color=BLUE).shift(LEFT * 2)
        square = Square(color=RED).shift(RIGHT * 2)
        self.play(Create(circle), Create(square))
        self.wait(1)

        # Scene 3: Transform
        self.play(Transform(circle, circle.copy().scale(1.5)))
        self.play(Rotate(square, PI / 4))
        self.wait(1)

        # Scene 4: Equation
        equation = MathTex("e^{i\\pi} + 1 = 0").shift(UP)
        self.play(Write(equation))
        self.wait(2)
        self.play(FadeOut(circle), FadeOut(square), FadeOut(equation))
