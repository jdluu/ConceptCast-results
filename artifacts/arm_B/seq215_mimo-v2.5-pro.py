from manim import *

class NeuralNetworkScene(Scene):
    def construct(self):
        # Title
        title = Text("Neural Network Activation", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Inputs
        x = [0.5, 0.8, 0.2]
        w = [0.4, -0.6, 0.3]
        b_val = 0.1
        z_val = sum(x[i] * w[i] for i in range(3)) + b_val

        # Create input text
        input_text = Text("Inputs:", font_size=30).shift(LEFT * 3 + UP * 2)
        self.play(Write(input_text))
        self.wait(0.5)

        input_vals = VGroup(*[
            Text(f"x{i+1} = {x[i]}", font_size=25).next_to(input_text, DOWN, buff=0.3 * i)
            for i in range(3)
        ])
        self.play(Write(input_vals))
        self.wait(1)

        # Create weights text
        weight_text = Text("Weights:", font_size=30).shift(RIGHT * 3 + UP * 2)
        self.play(Write(weight_text))
        self.wait(0.5)

        weight_vals = VGroup(*[
            Text(f"w{i+1} = {w[i]}", font_size=25).next_to(weight_text, DOWN, buff=0.3 * i)
            for i in range(3)
        ])
        self.play(Write(weight_vals))
        self.wait(1)

        # Bias
        bias_text = Text(f"Bias: b = {b_val}", font_size=30).shift(LEFT * 3 + DOWN * 1)
        self.play(Write(bias_text))
        self.wait(1)

        # Calculation
        calc_text = Text("Calculation:", font_size=30).shift(RIGHT * 1 + DOWN * 1)
        self.play(Write(calc_text))
        self.wait(0.5)

        # FIX: Escaped backslash for LaTeX command \cdot
        calc_val = MathTex(f"z = ({w[0]} \\cdot {x[0]}) + ({w[1]} \\cdot {x[1]}) + ({w[2]} \\cdot {x[2]}) + {b_val} = {z_val:.2f}").next_to(calc_text, DOWN)
        self.play(Write(calc_val))
        self.wait(2)

        # Activation
        activation_text = Text("Activation Function: ReLU", font_size=30).shift(LEFT * 3 + DOWN * 3)
        self.play(Write(activation_text))
        self.wait(1)

        activation_val = MathTex(f"a = \\max(0, {z_val:.2f}) = {max(0, z_val):.2f}").next_to(activation_text, DOWN)
        self.play(Write(activation_val))
        self.wait(2)

        # Final output
        output_text = Text("Output:", font_size=30).shift(RIGHT * 3 + DOWN * 3)
        self.play(Write(output_text))
        self.wait(0.5)

        output_val = Text(f"y = {max(0, z_val):.2f}", font_size=25).next_to(output_text, DOWN)
        self.play(Write(output_val))
        self.wait(2)
