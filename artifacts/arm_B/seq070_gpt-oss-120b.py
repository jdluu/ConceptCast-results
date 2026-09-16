from manim import *


class SceneGen(Scene):
    def construct(self):
        # ----------------------------------------------------------------------
        # 1) Title & Simple Neuron
        # ----------------------------------------------------------------------
        title = Text("Backpropagation", font_size=72).to_edge(UP)
        neuron = VGroup(
            Circle(radius=0.6, color=BLUE).set_fill(BLUE, opacity=0.2),
            Text("x", font_size=36).move_to(ORIGIN),
        ).shift(LEFT * 3)

        weight = MathTex(r"w", font_size=36).next_to(neuron, RIGHT, buff=0.5)
        weight_arrow = Arrow(
            start=neuron.get_right(),
            end=weight.get_left(),
            buff=0,
            tip_length=0.2,
            color=YELLOW,
        )
        weighted_sum = MathTex(r"z = w\cdot x", font_size=36).next_to(weight, RIGHT, buff=0.6)

        activation = MathTex(r"\sigma", font_size=36).next_to(weighted_sum, RIGHT, buff=0.8)
        act_arrow = Arrow(
            start=weighted_sum.get_right(),
            end=activation.get_left(),
            buff=0,
            tip_length=0.2,
            color=GREEN,
        )
        output = VGroup(
            Circle(radius=0.6, color=RED).set_fill(RED, opacity=0.2),
            Text("ŷ", font_size=36).move_to(ORIGIN),
        ).next_to(activation, RIGHT, buff=0.8)

        out_arrow = Arrow(
            start=activation.get_right(),
            end=output.get_left(),
            buff=0,
            tip_length=0.2,
            color=YELLOW,
        )

        self.play(FadeIn(title))
        self.play(FadeIn(neuron))
        self.play(GrowArrow(weight_arrow), Write(weight))
        self.play(Write(weighted_sum))
        self.play(GrowArrow(act_arrow), Write(activation))
        self.play(FadeIn(output), GrowArrow(out_arrow))
        self.wait(2)

        self.clear()

        # ----------------------------------------------------------------------
        # 2) Loss Function
        # ----------------------------------------------------------------------
        loss_title = Text("Loss Function", font_size=64).to_edge(UP)

        loss_eq = MathTex(
            r"L(\hat{y}, y) = \frac12(\hat{y} - y)^2",
            font_size=48,
        ).shift(UP)

        target = MathTex(r"y = 1", font_size=36).next_to(loss_eq, DOWN, buff=0.8)
        pred = MathTex(r"\hat{y} = 0.4", font_size=36).next_to(target, DOWN, buff=0.5)

        self.play(FadeIn(loss_title))
        self.play(Write(loss_eq))
        self.play(Write(target), Write(pred))
        self.wait(2)

        self.clear()

        # ----------------------------------------------------------------------
        # 3) Forward Pass (numeric example)
        # ----------------------------------------------------------------------
        fp_title = Text("Forward Pass (numeric)", font_size=60).to_edge(UP)

        # reuse neuron diagram, give concrete numbers
        n = VGroup(
            Circle(radius=0.6, color=BLUE).set_fill(BLUE, opacity=0.2),
            Text("0.5", font_size=36).move_to(ORIGIN),
        ).shift(LEFT * 3)

        w_num = MathTex(r"w = 2", font_size=36).next_to(n, RIGHT, buff=0.5)
        w_arrow = Arrow(
            start=n.get_right(),
            end=w_num.get_left(),
            buff=0,
            tip_length=0.2,
            color=YELLOW,
        )
        sum_num = MathTex(r"z = 2 \times 0.5 = 1", font_size=36).next_to(w_num, RIGHT, buff=0.8)

        act_num = MathTex(r"\sigma(z) = \frac{1}{1+e^{-z}} = 0.73", font_size=36).next_to(sum_num, RIGHT, buff=0.8)
        a_arrow = Arrow(
            start=sum_num.get_right(),
            end=act_num.get_left(),
            buff=0,
            tip_length=0.2,
            color=GREEN,
        )
        out_num = VGroup(
            Circle(radius=0.6, color=RED).set_fill(RED, opacity=0.2),
            Text("0.73", font_size=36).move_to(ORIGIN),
        ).next_to(act_num, RIGHT, buff=0.8)

        out_arrow = Arrow(
            start=act_num.get_right(),
            end=out_num.get_left(),
            buff=0,
            tip_length=0.2,
            color=YELLOW,
        )

        self.play(FadeIn(fp_title))
        self.play(FadeIn(n))
        self.play(GrowArrow(w_arrow), Write(w_num))
        self.play(Write(sum_num))
        self.play(GrowArrow(a_arrow), Write(act_num))
        self.play(FadeIn(out_num), GrowArrow(out_arrow))
        self.wait(2)

        self.clear()

        # ----------------------------------------------------------------------
        # 4) Gradient of Loss w.r.t. Output
        # ----------------------------------------------------------------------
        grad_title = Text("∂L/∂ŷ : Gradient of Loss", font_size=58).to_edge(UP)

        loss_func = MathTex(r"L = \frac12(\hat{y} - y)^2", font_size=44).shift(UP * 1.5)
        dL_dy = MathTex(r"\frac{\partial L}{\partial \hat{y}} = \hat{y} - y", font_size=44).next_to(loss_func, DOWN, buff=0.8)
        plug = MathTex(r"= 0.73 - 1 = -0.27", font_size=44).next_to(dL_dy, DOWN, buff=0.5)

        self.play(FadeIn(grad_title))
        self.play(Write(loss_func))
        self.play(Write(dL_dy))
        self.play(Write(plug))
        self.wait(2)

        self.clear()

        # ----------------------------------------------------------------------
        # 5) Backpropagation through one weight (chain rule)
        # ----------------------------------------------------------------------
        bp_title = Text("Backpropagation: Chain Rule", font_size=58).to_edge(UP)

        # show the derivative expression
        chain_eq = MathTex(
            r"\frac{\partial L}{\partial w} = "
            r"\frac{\partial L}{\partial \hat{y}}"
            r"\frac{\partial \hat{y}}{\partial z}"
            r"\frac{\partial z}{\partial w}",
            font_size=36,
        ).shift(UP)

        # individual terms
        term1 = MathTex(r"\frac{\partial L}{\partial \hat{y}} = -0.27", font_size=32).next_to(chain_eq, DOWN, buff=0.6)
        term2 = MathTex(r"\frac{\partial \hat{y}}{\partial z} = \hat{y}(1-\hat{y}) = 0.73(0.27)=0.1971", font_size=32).next_to(term1, DOWN, buff=0.3)
        term3 = MathTex(r"\frac{\partial z}{\partial w} = x = 0.5", font_size=32).next_to(term2, DOWN, buff=0.3)

        total = MathTex(r"\frac{\partial L}{\partial w} = (-0.27)(0.1971)(0.5) = -0.0266", font_size=36).next_to(term3, DOWN, buff=0.6)

        self.play(FadeIn(bp_title))
        self.play(Write(chain_eq))
        self.wait(0.5)
        self.play(Write(term1))
        self.wait(0.5)
        self.play(Write(term2))
        self.wait(0.5)
        self.play(Write(term3))
        self.wait(0.5)
        self.play(Write(total))
        self.wait(2)

        self.clear()

        # ----------------------------------------------------------------------
        # 6) Full Two‑Layer Network & Gradient Flow
        # ----------------------------------------------------------------------
        full_title = Text("Full Network & Gradient Flow", font_size=58).to_edge(UP)

        # create two layers
        input_node = Circle(radius=0.3, color=BLUE).set_fill(BLUE, opacity=0.2)
        input_label = Text("x", font_size=24).move_to(input_node)

        hidden_node = Circle(radius=0.3, color=GREEN).set_fill(GREEN, opacity=0.2)
        hidden_label = Text("h", font_size=24).move_to(hidden_node)

        output_node = Circle(radius=0.3, color=RED).set_fill(RED, opacity=0.2)
        output_label = Text("ŷ", font_size=24).move_to(output_node)

        # positions
        input_node.shift(LEFT * 4)
        hidden_node.shift(LEFT * 1)
        output_node.shift(RIGHT * 2)

        # arrows (weights)
        w1 = Arrow(start=input_node.get_right(), end=hidden_node.get_left(), buff=0, tip_length=0.15, color=YELLOW)
        w2 = Arrow(start=hidden_node.get_right(), end=output_node.get_left(), buff=0, tip_length=0.15, color=YELLOW)

        # gradient arrows (backward)
        g2 = Arrow(start=output_node.get_left(), end=hidden_node.get_right(), buff=0, tip_length=0.15, color=PURPLE)
        g1 = Arrow(start=hidden_node.get_left(), end=input_node.get_right(), buff=0, tip_length=0.15, color=PURPLE)

        # group for forward diagram
        forward = VGroup(input_node, input_label, w1, hidden_node, hidden_label, w2, output_node, output_label)

        self.play(FadeIn(full_title))
        self.play(FadeIn(forward))
        self.wait(0.5)

        # show forward pass numbers
        forward_nums = VGroup(
            MathTex(r"x=0.5", font_size=28).next_to(input_node, DOWN),
            MathTex(r"w_1=2", font_size=28).next_to(w1, UP),
            MathTex(r"w_2=1.5", font_size=28).next_to(w2, UP),
            MathTex(r"h=0.73", font_size=28).next_to(hidden_node, UP),
            MathTex(r"\hat{y}=0.82", font_size=28).next_to(output_node, UP),
        )
        self.play(Write(forward_nums))
        self.wait(1)

        # now reveal backward gradients
        grad_text = Text("Back‑propagation: error gradients flow backward", font_size=32).next_to(full_title, DOWN, buff=0.5)
        self.play(FadeIn(grad_text))
        self.play(GrowArrow(g2), GrowArrow(g1))
        # annotate gradients
        grad_labels = VGroup(
            MathTex(r"\frac{\partial L}{\partial w_2}", font_size=28).next_to(g2, LEFT),
            MathTex(r"\frac{\partial L}{\partial w_1}", font_size=28).next_to(g1, LEFT),
        )
        self.play(Write(grad_labels))
        self.wait(3)

        self.clear()
