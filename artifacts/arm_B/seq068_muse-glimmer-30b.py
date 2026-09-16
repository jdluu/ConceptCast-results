from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Title
        self.clear()
        title = Text("Backpropagation", font_size=72)
        subtitle = Text("Gradient Computation via Chain Rule", font_size=36).next_to(title, DOWN)
        intro = VGroup(title, subtitle)
        self.play(FadeIn(intro, shift=UP))
        self.wait(1)
        self.play(FadeOut(intro))

        # Scene 2: Network Architecture
        self.clear()
        title2 = Text("1. Network Architecture", font_size=48).to_edge(UP)
        inputs = VGroup(*[Circle(radius=0.3, color=BLUE).shift(UP*1.5 + LEFT*2 + i*RIGHT*1.5) for i in range(2)])
        hidden = VGroup(*[Circle(radius=0.3, color=GREEN).shift(ORIGIN + i*RIGHT*1.5) for i in range(2)])
        output = Circle(radius=0.4, color=RED).shift(DOWN*1.5)
        labels = VGroup(Text("x1"), Text("x2"), Text("h1"), Text("h2"), Text("ŷ")).arrange()
        # simplify labels
        in_labels = VGroup(Text("x1"), Text("x2")).arrange(DOWN).next_to(inputs, LEFT)
        hid_labels = VGroup(Text("h1"), Text("h2")).arrange(DOWN).next_to(hidden, LEFT)
        out_label = Text("ŷ").next_to(output, RIGHT)

        self.play(FadeIn(title2))
        self.play(*[FadeIn(c) for c in inputs], run_time=0.8)
        self.play(*[FadeIn(c) for c in hidden], run_time=0.8)
        self.play(FadeIn(output))
        arrows1 = VGroup(*[Arrow(inputs[i].get_right(), hidden[i].get_left(), buff=0.1) for i in range(2)])
        arrows2 = VGroup(*[Arrow(hidden[i].get_right(), output.get_left(), buff=0.1) for i in range(2)])
        self.play(Create(arrows1), Create(arrows2))
        self.play(FadeIn(in_labels), FadeIn(hid_labels), FadeIn(out_label))
        self.wait(1)
        self.play(FadeOut(title2), *[FadeOut(c) for c in inputs+hidden+[output]+arrows1+arrows2+in_labels+hid_labels+[out_label]])

        # Scene 3: Forward Pass
        self.clear()
        title3 = Text("2. Forward Pass", font_size=48).to_edge(UP)
        self.play(FadeIn(title3))
        x1 = Text("x1=0.5").next_to(LEFT*3, UP*1.5)
        x2 = Text("x2=1.2").next_to(LEFT*3, UP*0.5)
        z = Text("z = w·x + b").scale(0.8).to_edge(DOWN)
        self.play(FadeIn(x1), FadeIn(x2))
        self.play(Write(z))
        forward_text = Text("Forward: Input → Hidden → Output", font_size=32).next_to(title3, DOWN)
        self.play(FadeIn(forward_text))
        self.wait(1)
        self.play(FadeOut(title3), FadeOut(x1), FadeOut(x2), FadeOut(z), FadeOut(forward_text))

        # Scene 4: Loss
        self.clear()
        title4 = Text("3. Compute Loss", font_size=48).to_edge(UP)
        pred = Text("ŷ = 0.7").to_edge(LEFT)
        target = Text("y = 1.0").next_to(pred, DOWN)
        loss = Text("L = (y - ŷ)² = 0.09").next_to(target, DOWN)
        self.play(FadeIn(title4), FadeIn(pred), FadeIn(target))
        self.play(Write(loss), run_time=1.5)
        grad_text = Text("∂L/∂ŷ = 2(ŷ - y)").next_to(loss, DOWN)
        self.play(Write(grad_text))
        self.wait(1)
        self.play(FadeOut(title4), FadeOut(pred), FadeOut(target), FadeOut(loss), FadeOut(grad_text))

        # Scene 5: Chain Rule Introduction
        self.clear()
        title5 = Text("4. Chain Rule", font_size=48).to_edge(UP)
        chain = MathTex(r"\frac{\partial L}{\partial w} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z} \cdot \frac{\partial z}{\partial w}")
        self.play(FadeIn(title5))
        self.play(Write(chain))
        explain = Text("Error flows backward through each layer", font_size=28).next_to(chain, DOWN)
        self.play(FadeIn(explain))
        self.wait(1.5)
        self.play(FadeOut(title5), FadeOut(chain), FadeOut(explain))

        # Scene 6: Backpropagation
        self.clear()
        title6 = Text("5. Backward Pass", font_size=48).to_edge(UP)
        self.play(FadeIn(title6))
        grad_output = Text("δ = ∂L/∂ŷ = -0.6", color=RED).to_edge(UP)
        arrow_back = Arrow(DOWN*2, UP*2, buff=0.5, color=RED)
        self.play(FadeIn(grad_output), Create(arrow_back))
        grad_hidden = Text("δ_h = δ · σ'(z)", color=GREEN).next_to(grad_output, DOWN*1.5)
        self.play(Write(grad_hidden))
        grad_w = Text("∂L/∂w = δ_h · x", color=YELLOW).next_to(grad_hidden, DOWN)
        self.play(Write(grad_w))
        self.wait(1)
        self.play(FadeOut(title6), FadeOut(grad_output), FadeOut(arrow_back), FadeOut(grad_hidden), FadeOut(grad_w))

        # Scene 7: Weight Update
        self.clear()
        title7 = Text("6. Update Weights", font_size=48).to_edge(UP)
        update = MathTex(r"w_{\text{new}} = w_{\text{old}} - \eta \frac{\partial L}{\partial w}")
        self.play(FadeIn(title7), Write(update))
        desc = Text("Gradient descent moves weights downhill", font_size=28).next_to(update, DOWN)
        self.play(FadeIn(desc))
        summary = Text("Backpropagation = Chain Rule applied backward", font_size=36, color=BLUE).to_edge(DOWN)
        self.play(FadeIn(summary))
        self.wait(2)
        self.play(FadeOut(title7), FadeOut(update), FadeOut(desc), FadeOut(summary))
