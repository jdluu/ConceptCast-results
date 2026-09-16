from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Forward Pass
        title = Text("1. Forward Pass of a Neuron", color=BLUE).to_edge(UP)
        self.play(Write(title))
        x = MathTex("x").shift(LEFT * 4)
        w = MathTex("w").shift(UP * 1 + LEFT * 2)
        b = MathTex("b").shift(DOWN * 1 + LEFT * 2)
        neuron = Circle(color=BLUE).shift(RIGHT)
        zlab = MathTex("z = wx + b").next_to(neuron, LEFT)
        alab = MathTex("a = \\sigma(z)").next_to(neuron, RIGHT)
        self.play(FadeIn(x), FadeIn(w), FadeIn(b), Create(neuron))
        self.play(Write(zlab), Write(alab))
        arr_x = Arrow(x, neuron.get_left(), color=WHITE)
        arr_w = Arrow(w, neuron.get_left(), color=WHITE)
        arr_b = Arrow(b, neuron.get_left(), color=WHITE)
        self.play(GrowArrow(arr_x), GrowArrow(arr_w), GrowArrow(arr_b))
        self.wait()
        self.clear()

        # Scene 2: Loss Function
        title2 = Text("2. Loss Function", color=RED).to_edge(UP)
        self.play(Write(title2))
        a = MathTex("a").shift(LEFT * 2)
        y = MathTex("y").shift(RIGHT * 2)
        self.play(FadeIn(a), FadeIn(y))
        diff = MathTex("a - y").shift(DOWN)
        self.play(Write(diff))
        loss = MathTex("L = \\frac{1}{2}(a-y)^2").shift(DOWN * 2)
        self.play(Transform(diff, loss))
        self.wait()
        self.clear()

        # Scene 3: Chain Rule
        title3 = Text("3. Chain Rule", color=GREEN).to_edge(UP)
        self.play(Write(title3))
        chain = MathTex("\\frac{\\partial L}{\\partial w} = \\frac{\\partial L}{\\partial a}\\frac{\\partial a}{\\partial z}\\frac{\\partial z}{\\partial w}")
        self.play(Write(chain))
        p1 = MathTex("\\frac{\\partial L}{\\partial a} = a - y").shift(DOWN * 1.5).set_color(RED)
        p2 = MathTex("\\frac{\\partial a}{\\partial z} = \\sigma'(z)").shift(DOWN * 2.5).set_color(BLUE)
        p3 = MathTex("\\frac{\\partial z}{\\partial w} = x").shift(DOWN * 3.5).set_color(YELLOW)
        self.play(Write(p1))
        self.play(Write(p2))
        self.play(Write(p3))
        self.wait()
        self.clear()

        # Scene 4: Single Neuron Gradient
        title4 = Text("4. Gradient for One Neuron", color=YELLOW).to_edge(UP)
        self.play(Write(title4))
        grad = MathTex("\\frac{\\partial L}{\\partial w} = (a-y)\\sigma'(z)x")
        self.play(Write(grad))
        t1 = MathTex("(a-y)").shift(DOWN * 1.5).set_color(RED)
        t2 = MathTex("\\sigma'(z)").shift(DOWN * 2.5).set_color(BLUE)
        t3 = MathTex("x").shift(DOWN * 3.5).set_color(GREEN)
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(t3))
        self.wait()
        self.clear()

        # Scene 5: Backward Through Layers
        title5 = Text("5. Backward Through Layers", color=PURPLE).to_edge(UP)
        self.play(Write(title5))
        n1 = Circle(color=BLUE).shift(LEFT * 3)
        n2 = Circle(color=RED).shift(RIGHT * 3)
        self.play(Create(n1), Create(n2))
        fwd = Arrow(n1, n2, color=WHITE)
        self.play(GrowArrow(fwd))
        bwd = Arrow(n2, n1, color=YELLOW)
        self.play(GrowArrow(bwd))
        d_out = MathTex("\\delta_{out} = (a-y)\\sigma'(z_2)").next_to(n2, UP)
        d_hid = MathTex("\\delta_{hid} = \\delta_{out} w_2 \\sigma'(z_1)").next_to(n1, UP)
        self.play(Write(d_out))
        self.play(Write(d_hid))
        self.wait()
        self.clear()

        # Scene 6: Vectorized Gradients
        title6 = Text("6. Vectorized Gradients", color=TEAL).to_edge(UP)
        self.play(Write(title6))
        mat = MathTex("\\frac{\\partial L}{\\partial W} = \\delta_{out} h^T")
        self.play(Write(mat))
        mW = Rectangle(width=2, height=1.5, color=BLUE).shift(LEFT * 3)
        mh = Rectangle(width=1.5, height=2, color=RED).shift(RIGHT * 3)
        self.play(Create(mW), Create(mh))
        self.play(Indicate(mW), Indicate(mh))
        self.wait()
        self.clear()

        # Scene 7: Gradient Descent Update
        title7 = Text("7. Gradient Descent Update", color=ORANGE).to_edge(UP)
        self.play(Write(title7))
        axes = Axes(x_range=[-3, 3], y_range=[0, 5], x_length=6, y_length=4).shift(DOWN)
        curve = axes.plot(lambda x: x ** 2, color=BLUE)
        self.play(Create(axes), Create(curve))
        dot = Dot(axes.coords_to_point(2, 4), color=RED)
        self.play(FadeIn(dot))
        self.play(dot.animate.move_to(axes.coords_to_point(1, 1)))
        self.play(dot.animate.move_to(axes.coords_to_point(0, 0)))
        upd = MathTex("w \\leftarrow w - \\eta \\frac{\\partial L}{\\partial w}").shift(UP)
        self.play(Write(upd))
        self.wait()
        self.clear()

        # Scene 8: Summary
        title8 = Text("8. Backpropagation Summary", color=WHITE).to_edge(UP)
        self.play(Write(title8))
        steps = VGroup(
            Text("1. Forward pass: compute activations", color=BLUE),
            Text("2. Compute loss at output", color=RED),
            Text("3. Backward pass: propagate error deltas", color=GREEN),
            Text("4. Compute gradients for each layer", color=YELLOW),
            Text("5. Update weights via gradient descent", color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT).shift(DOWN * 0.5)
        self.play(Write(steps))
        self.wait()