from manim import *

class FullBackpropAnimation(Scene):
    def construct(self):
        # ------------------------------------------------------------
        # Scene 1: Intro (Neural Network Overview)
        # ------------------------------------------------------------
        title = Text("Backpropagation Visualized", color=BLUE).to_edge(UP)
        self.play(Write(title, run_time=1.5))
        self.wait(0.5)

        # Create a simple neural network diagram
        layers = VGroup()
        layer_colors = [GREEN, YELLOW, BLUE, RED]
        layer_sizes = [3, 4, 4, 2]
        spacing = 2.5
        for l_idx, (n_neurons, color) in enumerate(zip(layer_sizes, layer_colors)):
            layer = VGroup()
            for n_idx in range(n_neurons):
                neuron = Circle(radius=0.25, color=color, fill_opacity=0.3)
                neuron.shift(UP * (n_idx - (n_neurons - 1) / 2) * 0.7)
                layer.add(neuron)
            layer.shift(RIGHT * l_idx * spacing)
            layers.add(layer)

        # Add connections between layers
        connections = VGroup()
        for l_idx in range(len(layers) - 1):
            left_layer = layers[l_idx]
            right_layer = layers[l_idx + 1]
            for left_neuron in left_layer:
                for right_neuron in right_layer:
                    line = Line(left_neuron.get_center(), right_neuron.get_center(), stroke_width=1, color=GRAY)
                    connections.add(line)
        self.play(
            *[Create(layer, run_time=0.5) for layer in layers],
            *[Create(conn, run_time=0.02) for conn in connections]
        )
        self.wait(1)

        # Labels
        input_label = Text("Input", color=GREEN).scale(0.5).next_to(layers[0], DOWN, buff=0.5)
        hidden_label = Text("Hidden", color=YELLOW).scale(0.5).next_to(layers[1], DOWN, buff=0.5)
        output_label = Text("Output", color=RED).scale(0.5).next_to(layers[-1], DOWN, buff=0.5)
        self.play(Write(input_label), Write(hidden_label), Write(output_label))
        self.wait(1.5)

        self.play(*[FadeOut(mob, run_time=0.5) for mob in self.mobjects])
        self.clear()

        # ------------------------------------------------------------
        # Scene 2: Forward Pass
        # ------------------------------------------------------------
        title2 = Text("Forward Pass", color=GREEN).to_edge(UP)
        self.play(Write(title2, run_time=1))
        self.wait(0.3)

        # Simple forward pass diagram: input -> neuron -> output
        input_circle = Circle(radius=0.3, color=GREEN, fill_opacity=0.3).shift(LEFT * 4)
        weight_circle = Circle(radius=0.3, color=YELLOW, fill_opacity=0.3).shift(LEFT * 1.5)
        act_circle = Circle(radius=0.3, color=BLUE, fill_opacity=0.3).shift(RIGHT * 1)
        output_circle = Circle(radius=0.3, color=RED, fill_opacity=0.3).shift(RIGHT * 3.5)

        arrows_forward = VGroup(
            Arrow(input_circle.get_right(), weight_circle.get_left(), color=GRAY),
            Arrow(weight_circle.get_right(), act_circle.get_left(), color=GRAY),
            Arrow(act_circle.get_right(), output_circle.get_left(), color=GRAY)
        )

        self.play(
            Create(input_circle), Create(weight_circle),
            Create(act_circle), Create(output_circle),
            *[GrowArrow(arr, run_time=0.5) for arr in arrows_forward]
        )
        self.wait(0.5)

        # Labels
        x_label = MathTex("x", color=GREEN).next_to(input_circle, DOWN, buff=0.3)
        w_label = MathTex("w", color=YELLOW).next_to(weight_circle, DOWN, buff=0.3)
        a_label = MathTex(r"\sigma(wx)", color=BLUE).next_to(act_circle, DOWN, buff=0.3)
        y_label = MathTex(r"\hat{y}", color=RED).next_to(output_circle, DOWN, buff=0.3)
        self.play(Write(x_label), Write(w_label), Write(a_label), Write(y_label))
        self.wait(1)

        # Forward equation
        forward_eq = MathTex(r"\hat{y} = \sigma(w x)", color=BLUE).shift(DOWN * 2)
        self.play(Write(forward_eq, run_time=1))
        self.wait(1.5)

        self.play(*[FadeOut(mob, run_time=0.5) for mob in self.mobjects])
        self.clear()

        # ------------------------------------------------------------
        # Scene 3: Loss Computation (Gradient Seed)
        # ------------------------------------------------------------
        title3 = Text("Loss Computation: Where Gradients Start", color=RED).to_edge(UP)
        self.play(Write(title3, run_time=1))
        self.wait(0.3)

        # Loss formula
        loss_eq = MathTex(r"\mathcal{L} = (y - \hat{y})^2", color=RED)
        loss_eq.shift(UP * 2)
        self.play(Write(loss_eq, run_time=1))
        self.wait(0.5)

        # Gradient seed
        seed_eq = MathTex(r"\frac{\partial \mathcal{L}}{\partial \hat{y}} = -2(y - \hat{y})", color=ORANGE)
        seed_eq.next_to(loss_eq, DOWN, buff=0.8)
        self.play(Write(seed_eq, run_time=1))
        self.wait(0.8)

        # Visual arrow from loss to output
        arrow_loss = Arrow(loss_eq.get_bottom(), seed_eq.get_top(), color=RED)
        self.play(GrowArrow(arrow_loss, run_time=0.8))
        self.wait(0.5)

        # Emphasize "start here"
        start_label = Text("Gradient flow starts at the loss", color=YELLOW).scale(0.6).to_edge(DOWN)
        self.play(Write(start_label, run_time=0.8))
        self.wait(1)

        self.play(*[FadeOut(mob, run_time=0.5) for mob in self.mobjects])
        self.clear()

        # ------------------------------------------------------------
        # Scene 4: Single Neuron Backprop (Weight Update)
        # ------------------------------------------------------------
        title4 = Text("Backprop Through One Neuron", color=BLUE).to_edge(UP)
        self.play(Write(title4, run_time=1))
        self.wait(0.3)

        # Neuron components: input, weight, activation
        x_sym = MathTex("x", color=GREEN).shift(LEFT * 4 + UP * 1)
        w_sym = MathTex("w", color=YELLOW).shift(LEFT * 2 + UP * 1)
        act_sym = MathTex(r"\sigma(w x)", color=BLUE).shift(RIGHT * 1 + UP * 1)
        loss_sym = MathTex(r"\mathcal{L}", color=RED).shift(RIGHT * 4 + UP * 1)

        arrows_neuron = VGroup(
            Arrow(x_sym.get_right(), w_sym.get_left(), color=GRAY),
            Arrow(w_sym.get_right(), act_sym.get_left(), color=GRAY),
            Arrow(act_sym.get_right(), loss_sym.get_left(), color=GRAY)
        )

        self.play(
            Write(x_sym), Write(w_sym), Write(act_sym), Write(loss_sym),
            *[GrowArrow(arr, run_time=0.4) for arr in arrows_neuron]
        )
        self.wait(0.5)

        # Backward gradients
        dL_da = MathTex(r"\frac{\partial \mathcal{L}}{\partial a}", color=RED).scale(0.7)
        dL_da.next_to(loss_sym, DOWN, buff=0.8)
        self.play(Write(dL_da, run_time=0.8))
        self.wait(0.3)

        da_dw = MathTex(r"\frac{\partial a}{\partial w} = x", color=ORANGE).scale(0.7)
        da_dw.next_to(w_sym, DOWN, buff=0.8)
        self.play(Write(da_dw, run_time=0.8))
        self.wait(0.3)

        # Chain rule for weight
        dL_dw = MathTex(r"\frac{\partial \mathcal{L}}{\partial w} = \frac{\partial \mathcal{L}}{\partial a} \cdot x", color=PURPLE)
        dL_dw.next_to(da_dw, DOWN, buff=0.6)
        self.play(Write(dL_dw, run_time=1))
        self.wait(0.5)

        # Weight update rule
        update_eq = MathTex(r"w_{t+1} = w_t - \eta \frac{\partial \mathcal{L}}{\partial w}", color=PURPLE)
        update_eq.shift(DOWN * 2.5)
        self.play(Write(update_eq, run_time=1.2))
        self.wait(1)

        self.play(*[FadeOut(mob, run_time=0.5) for mob in self.mobjects])
        self.clear()

        # ------------------------------------------------------------
        # Scene 5: Multi-Layer Chain Rule (Deep Network)
        # ------------------------------------------------------------
        title5 = Text("Chain Rule Through Multiple Layers", color=YELLOW).to_edge(UP)
        self.play(Write(title5, run_time=1))
        self.wait(0.3)

        # Deep network representation
        layers_deep = VGroup()
        for i, (n, col) in enumerate([(2, GREEN), (3, YELLOW), (3, BLUE), (2, RED)]):
            layer = VGroup(*[
                Circle(radius=0.2, color=col, fill_opacity=0.3).shift(UP * (j - (n-1)/2) * 0.6)
                for j in range(n)
            ]).shift(RIGHT * i * 2.2)
            layers_deep.add(layer)

        # Connect layers
        conn_deep = VGroup()
        for l_idx in range(len(layers_deep) - 1):
            left = layers_deep[l_idx]
            right = layers_deep[l_idx + 1]
            for ln in left:
                for rn in right:
                    line = Line(ln.get_center(), rn.get_center(), stroke_width=1, color=GRAY)
                    conn_deep.add(line)

        self.play(
            *[Create(layer, run_time=0.5) for layer in layers_deep],
            *[Create(conn, run_time=0.02) for conn in conn_deep]
        )
        self.wait(0.5)

        # Add gradient symbols along arrows
        grad_labels = VGroup(
            MathTex(r"\frac{\partial \mathcal{L}}{\partial h_1}", color=RED).scale(0.4).shift(UP * 1.5 + RIGHT * 0.5),
            MathTex(r"\frac{\partial \mathcal{L}}{\partial h_2}", color=RED).scale(0.4).shift(DOWN * 0.5 + RIGHT * 0.5),
            MathTex(r"\frac{\partial \mathcal{L}}{\partial x_1}", color=RED).scale(0.4).shift(LEFT * 2.5 + UP * 1.2),
        )
        self.play(*[Write(label, run_time=0.6) for label in grad_labels])
        self.wait(0.5)

        # Chain rule summary equation
        summary_eq = MathTex(
            r"\frac{\partial \mathcal{L}}{\partial w_i} = \frac{\partial \mathcal{L}}{\partial a_{out}} \cdot \prod_{k} \frac{\partial a_{k+1}}{\partial a_k}",
            color=BLUE
        ).scale(0.6).to_edge(DOWN)
        self.play(Write(summary_eq, run_time=1.5))
        self.wait(1)

        self.play(*[FadeOut(mob, run_time=0.5) for mob in self.mobjects])
        self.clear()

        # ------------------------------------------------------------
        # Scene 6: Conclusion
        # ------------------------------------------------------------
        conclusion = Text(
            "Backpropagation:\nCompute gradients from loss,\napply chain rule backward,\nupdate weights.",
            color=BLUE,
            line_spacing=1.2
        ).scale(0.8)
        self.play(Write(conclusion, run_time=2))
        self.wait(1)

        final_msg = Text("End", color=YELLOW).scale(0.6).to_edge(DOWN)
        self.play(Write(final_msg, run_time=0.5))
        self.wait(2)
