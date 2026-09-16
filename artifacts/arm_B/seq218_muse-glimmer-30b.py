from manim import *

class BackpropScene(Scene):
    def construct(self):
        # forward pass
        out = Text("output")
        forward_text = MathTex("\\hat{y} = w_2 \\cdot \\sigma(w_1 x)").next_to(out, DOWN)

        chain_eq = MathTex("\\frac{dL}{dw_1} = \\frac{dL}{d\\hat{y}} \\cdot \\frac{d\\hat{y}}{dh} \\cdot \\frac{dh}{dw_1}").scale(0.9)

        y_hat = MathTex("\\hat{y} = 0.7").to_edge(LEFT)
        y_true = MathTex("y = 1.0").next_to(y_hat, DOWN)
        loss_eq = MathTex("L = \\frac12 (y - \\hat{y})^2").scale(1.2).to_edge(DOWN)

        # backward pass
        out2 = Text("output2")
        hid2 = Text("hidden2")
        grad_out = MathTex("\\delta_o = \\frac{dL}{d\\hat{y}}").next_to(out2, DOWN)
        grad_h = MathTex("\\delta_h = \\delta_o \\frac{d\\hat{y}}{dh}").next_to(hid2, DOWN)

        self.play(Write(forward_text))
        self.wait()
