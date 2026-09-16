from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Forward Pass
        title = Text("1. Forward Pass: Neuron", color=BLUE).to_edge(UP)
        self.play(Write(title))
        x1 = MathTex("x_1").shift(LEFT*3 + UP)
        x2 = MathTex("x_2").shift(LEFT*3 + DOWN)
        w1 = MathTex("w_1").shift(LEFT*1.5 + UP)
        w2 = MathTex("w_2").shift(LEFT*1.5 + DOWN)
        mul1 = MathTex("x_1 w_1").shift(LEFT*0.2 + UP)
        mul2 = MathTex("x_2 w_2").shift(LEFT*0.2 + DOWN)
        summ = MathTex("z = x_1 w_1 + x_2 w_2 + b").shift(RIGHT*2 + UP*0.5)
        act = MathTex("a = \\sigma(z)").shift(RIGHT*2 + DOWN*0.5)
        a1 = Arrow(x1.get_right(), mul1.get_left(), color=WHITE)
        a2 = Arrow(x2.get_right(), mul2.get_left(), color=WHITE)
        a3 = Arrow(mul1.get_right(), summ.get_left(), color=YELLOW)
        a4 = Arrow(mul2.get_right(), summ.get_left(), color=YELLOW)
        a5 = Arrow(summ.get_right(), act.get_left(), color=GREEN)
        self.play(FadeIn(x1, x2, w1, w2))
        self.play(GrowArrow(a1), GrowArrow(a2))
        self.play(Write(mul1), Write(mul2))
        self.play(GrowArrow(a3), GrowArrow(a4))
        self.play(Write(summ))
        self.play(GrowArrow(a5), Write(act))
        self.wait(0.5)
        self.clear()

        # Scene 2: Loss Function
        title2 = Text("2. Loss Function", color=RED).to_edge(UP)
        self.play(Write(title2))
        pred = MathTex("a = 0.7").shift(LEFT*2)
        target = MathTex("y = 1.0").shift(RIGHT*2)
        err = MathTex("a - y = -0.3").shift(UP*0.5)
        loss = MathTex("L = \\frac{1}{2}(a - y)^2").shift(DOWN*1)
        arr1 = Arrow(pred.get_bottom(), loss.get_left(), color=RED)
        arr2 = Arrow(target.get_bottom(), loss.get_right(), color=RED)
        self.play(Write(pred), Write(target))
        self.play(Write(err))
        self.play(GrowArrow(arr1), GrowArrow(arr2), Write(loss))
        self.wait(0.5)
        self.clear()

        # Scene 3: Chain Rule
        title3 = Text("3. Chain Rule", color=BLUE).to_edge(UP)
        self.play(Write(title3))
        eq = MathTex("\\frac{dL}{dw} = \\frac{dL}{da} \\cdot \\frac{da}{dz} \\cdot \\frac{dz}{dw}").shift(UP)
        f1 = MathTex("\\frac{dL}{da}").shift(LEFT*3 + DOWN)
        f2 = MathTex("\\frac{da}{dz}").shift(DOWN)
        f3 = MathTex("\\frac{dz}{dw}").shift(RIGHT*3 + DOWN)
        ar1 = Arrow(f1.get_right(), f2.get_left(), color=YELLOW)
        ar2 = Arrow(f2.get_right(), f3.get_left(), color=YELLOW)
        self.play(Write(eq))
        self.play(Write(f1), Write(f2), Write(f3))
        self.play(GrowArrow(ar1), GrowArrow(ar2))
        self.wait(0.5)
        self.clear()

        # Scene 4: Local Gradients
        title4 = Text("4. Compute Local Gradients", color=GREEN).to_edge(UP)
        self.play(Write(title4))
        g1 = MathTex("\\frac{dL}{da} = a - y = -0.3").shift(UP)
        g2 = MathTex("\\frac{da}{dz} = \\sigma'(z) = 0.2").shift(LEFT)
        g3 = MathTex("\\frac{dz}{dw} = x = 0.5").shift(RIGHT)
        prod = MathTex("\\frac{dL}{dw} = (-0.3)(0.2)(0.5) = -0.03").shift(DOWN)
        self.play(Write(g1))
        self.play(Write(g2), Write(g3))
        self.play(Write(prod))
        self.wait(0.5)
        self.clear()

        # Scene 5: Backward Propagation
        title5 = Text("5. Backward Propagation", color=ORANGE).to_edge(UP)
        self.play(Write(title5))
        fw1 = MathTex("w").shift(LEFT*3)
        fw2 = MathTex("z").shift(LEFT*1)
        fw3 = MathTex("a").shift(RIGHT*1)
        fw4 = MathTex("L").shift(RIGHT*3)
        af1 = Arrow(fw1.get_right(), fw2.get_left(), color=WHITE)
        af2 = Arrow(fw2.get_right(), fw3.get_left(), color=WHITE)
        af3 = Arrow(fw3.get_right(), fw4.get_left(), color=WHITE)
        self.play(Write(fw1), Write(fw2), Write(fw3), Write(fw4))
        self.play(GrowArrow(af1), GrowArrow(af2), GrowArrow(af3))
        ab3 = Arrow(fw4.get_left(), fw3.get_right(), color=RED)
        ab2 = Arrow(fw3.get_left(), fw2.get_right(), color=RED)
        ab1 = Arrow(fw2.get_left(), fw1.get_right(), color=RED)
        self.play(GrowArrow(ab3))
        self.play(GrowArrow(ab2))
        self.play(GrowArrow(ab1))
        self.wait(0.5)
        self.clear()

        # Scene 6: Multi-Layer Backprop
        title6 = Text("6. Multi-Layer Backprop", color=PURPLE).to_edge(UP)
        self.play(Write(title6))
        inp = VGroup(*[Circle(0.3, color=BLUE) for _ in range(2)]).arrange(DOWN).shift(LEFT*4)
        hid = VGroup(*[Circle(0.3, color=GREEN) for _ in range(2)]).arrange(DOWN).shift(LEFT*1)
        out = Circle(0.3, color=RED).shift(RIGHT*2)
        self.play(FadeIn(inp), FadeIn(hid), FadeIn(out))
        ef = VGroup()
        for i in inp:
            for h in hid:
                ef.add(Line(i.get_right(), h.get_left(), color=WHITE))
        for h in hid:
            ef.add(Line(h.get_right(), out.get_left(), color=WHITE))
        self.play(Create(ef))
        eb = VGroup()
        for h in hid:
            eb.add(Line(out.get_left(), h.get_right(), color=RED))
        for i in inp:
            for h in hid:
                eb.add(Line(h.get_left(), i.get_right(), color=RED))
        self.play(Create(eb))
        upd = MathTex("w \\leftarrow w - \\eta \\frac{dL}{dw}").shift(DOWN*2)
        self.play(Write(upd))
        self.wait(0.5)
        self.clear()

        # Scene 7: Summary
        title7 = Text("7. Backpropagation Summary", color=YELLOW).to_edge(UP)
        self.play(Write(title7))
        eqf = MathTex("\\nabla_w L = \\frac{\\partial L}{\\partial a} \\frac{\\partial a}{\\partial z} \\frac{\\partial z}{\\partial w}").shift(UP*1)
        self.play(Write(eqf))
        bl = BulletedList(
            "Forward pass computes activations",
            "Loss measures prediction error",
            "Chain rule gives gradient w.r.t weights",
            "Gradients flow backward layer by layer",
            "Update weights via gradient descent"
        ).shift(DOWN*0.5)
        self.play(Write(bl))
        self.wait(1)
        self.clear()