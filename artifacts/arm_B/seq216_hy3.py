from manim import *

class FullScene(Scene):
    def construct(self):
        # Scene 1
        title = Text("Title")
        x1 = MathTex("x_1")
        x2 = MathTex("x_2")
        w1 = MathTex("w_1")
        w2 = MathTex("w_2")
        sum_eq = MathTex("z = x_1 w_1 + x_2 w_2")
        act = MathTex("a = \\sigma(z)")
        arrow1 = Arrow(LEFT, RIGHT)
        arrow2 = Arrow(LEFT, RIGHT)
        arrow3 = Arrow(LEFT, RIGHT)
        self.add(title, x1, x2, w1, w2, sum_eq, act, arrow1, arrow2, arrow3)
        self.play(FadeOut(title, x1, x2, w1, w2, sum_eq, act, arrow1, arrow2, arrow3))

        # Scene 2
        axes = Axes()
        loss_curve = FunctionGraph(lambda x: x**2)
        loss_label = Text("Loss")
        target_dot = Dot()
        title2 = Text("Loss")
        self.add(axes, loss_curve, loss_label, target_dot, title2)
        self.play(FadeOut(axes, loss_curve, loss_label, target_dot, title2))

        # Scene 3
        title3 = Text("Formula")
        formula = MathTex("f")
        part1 = MathTex("a")
        part2 = MathTex("b")
        part3 = MathTex("c")
        self.add(title3, formula, part1, part2, part3)
        self.play(FadeOut(title3, formula, part1, part2, part3))

        # Scene 4
        title4 = Text("Neuron")
        neuron = Circle()
        delta = MathTex("\\delta")
        grad = MathTex("\\nabla")
        self.add(title4, neuron, delta, grad)
        self.play(FadeOut(title4, neuron, delta, grad))

        # Scene 5
        title5 = Text("Hidden to Output")
        hidden = Square()
        out = Square()
        arrow = Arrow(out.get_left(), hidden.get_right(), color=RED)
        label = Text("label")
        self.add(title5, hidden, out, arrow, label)
        self.play(FadeOut(title5, hidden, out, arrow, label))

        # Scene 6
        title6 = Text("Weight Update")
        w_old = MathTex("w")
        arrow = Arrow(LEFT, RIGHT)
        w_new = MathTex("w'")
        self.add(title6, w_old, arrow, w_new)
        self.play(FadeOut(title6, w_old, arrow, w_new))