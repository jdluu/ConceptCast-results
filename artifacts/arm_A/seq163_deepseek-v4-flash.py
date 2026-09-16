#!/usr/bin/env python3
from manim import *

class SceneGen(Scene):
    def construct(self):
        # ---------- Scene 1: Motivation - Loss Landscape ----------
        title = Text("Backpropagation: Teaching Neural Networks", font_size=36).to_edge(UP)
        self.play(Write(title))
        
        loss_label = MathTex("\\text{Loss} = L(\\hat{y}, y)", font_size=40).shift(LEFT*3)
        loss_curve = VGroup(
            DashedLine(UP*2, DOWN*0.5, color=GREY),
            ParametricFunction(
                lambda t: np.array([t, -0.8*np.sin(3*t) - 0.3, 0]),
                t_range=[-3, 3], color=BLUE
            ).shift(DOWN*0.5 + RIGHT*3)
        ).shift(RIGHT)
        loss_curve_label = Text("Loss surface", font_size=24).next_to(loss_curve, DOWN)
        
        # A simple point on the curve
        point = Dot(color=RED).move_to(loss_curve[1].point_from_proportion(0.6))
        point_label = MathTex("\\theta", color=RED, font_size=30).next_to(point, UR)
        
        self.play(Write(loss_label), Create(loss_curve), Write(loss_curve_label))
        self.play(Create(point), Write(point_label))
        self.wait(1)
        self.play(
            point.animate.move_to(loss_curve[1].point_from_proportion(0.3)),
            point_label.animate.next_to(point, UR)
        )
        self.play(FadeOut(point, point_label, loss_label, loss_curve, loss_curve_label, title))
        self.clear()

        # ---------- Scene 2: Chain Rule Intuition ----------
        chain_title = Text("Chain Rule: How errors flow", font_size=36).to_edge(UP)
        self.play(Write(chain_title))
        
        # Composite function diagram
        f = MathTex("f(x) = g(h(x))", font_size=40).shift(UP*2)
        self.play(Write(f))
        
        # Error gradient propagation
        chain_arrow = Arrow(LEFT*2, RIGHT*2, color=YELLOW).next_to(f, DOWN, buff=0.5)
        chain_text = MathTex("\\frac{\\partial f}{\\partial x} = \\frac{\\partial g}{\\partial h} \\cdot \\frac{\\partial h}{\\partial x}", font_size=34).next_to(chain_arrow, DOWN)
        
        self.play(Create(chain_arrow), Write(chain_text))
        self.wait(1.5)
        
        # Simple numeric example
        box1 = Square(0.6, color=BLUE).shift(LEFT*3.5 + DOWN*1.5)
        box2 = Square(0.6, color=BLUE).shift(DOWN*1.5)
        box3 = Square(0.6, color=BLUE).shift(RIGHT*3.5 + DOWN*1.5)
        labels = VGroup(
            MathTex("x", font_size=28).move_to(box1),
            MathTex("h=x^2", font_size=28).move_to(box2),
            MathTex("g=e^h", font_size=28).move_to(box3)
        )
        arrows = VGroup(
            Arrow(box1.get_right(), box2.get_left(), buff=0.1),
            Arrow(box2.get_right(), box3.get_left(), buff=0.1)
        )
        self.play(Create(box1), Create(box2), Create(box3), Write(labels), Create(arrows))
        self.wait(1.2)
        self.play(FadeOut(chain_title, f, chain_arrow, chain_text, box1, box2, box3, labels, arrows))
        self.clear()

        # ---------- Scene 3: Simple Network Forward Pass ----------
        forward_title = Text("Forward pass: compute output", font_size=36).to_edge(UP)
        self.play(Write(forward_title))
        
        # Tiny network: input -> hidden -> output
        input_neuron = Circle(0.3, color=GREEN).shift(LEFT*4)
        hidden_neuron = Circle(0.3, color=GREEN).shift(LEFT*1.2)
        output_neuron = Circle(0.3, color=GREEN).shift(RIGHT*2.5)
        neurons = VGroup(input_neuron, hidden_neuron, output_neuron)
        
        # Connections
        w1 = Arrow(input_neuron.get_right(), hidden_neuron.get_left(), buff=0.1, color=GREY)
        w2 = Arrow(hidden_neuron.get_right(), output_neuron.get_left(), buff=0.1, color=GREY)
        
        # Labels
        x_label = MathTex("x=1.2", font_size=28).next_to(input_neuron, DOWN)
        h_label = MathTex("h=\\sigma(wx)", font_size=28).next_to(hidden_neuron, DOWN)
        y_label = MathTex("\\hat{y}=w_2\\sigma(wx)", font_size=28).next_to(output_neuron, DOWN)
        
        self.play(Create(neurons), Create(w1), Create(w2), Write(x_label), Write(h_label), Write(y_label))
        self.wait(1.5)
        
        # Highlight weights
        weight_boxes = VGroup(
            SurroundingRectangle(w1, color=RED, buff=0.1),
            SurroundingRectangle(w2, color=RED, buff=0.1)
        )
        self.play(Create(weight_boxes))
        self.wait(1)
        self.play(FadeOut(forward_title, neurons, w1, w2, x_label, h_label, y_label, weight_boxes))
        self.clear()

        # ---------- Scene 4: Loss and Gradient at Output ----------
        grad_title = Text("Compute loss gradient at output", font_size=36).to_edge(UP)
        self.play(Write(grad_title))
        
        # Output neuron with loss
        out = Circle(0.4, color=ORANGE).shift(RIGHT*3)
        loss_eq = MathTex("L = (\\hat{y} - y)^2", font_size=32).next_to(out, DOWN)
        grad_out = MathTex("\\frac{\\partial L}{\\partial \\hat{y}} = 2(\\hat{y} - y)", font_size=28).next_to(out, UP)
        
        self.play(Create(out), Write(loss_eq))
        self.play(Write(grad_out))
        self.wait(1.5)
        
        # Show numeric value
        num_val = MathTex("\\text{Example: } \\hat{y}=0.8, y=1 \\Rightarrow \\frac{\\partial L}{\\partial \\hat{y}} = -0.4", font_size=28).shift(DOWN*2)
        self.play(Write(num_val))
        self.wait(1)
        self.play(FadeOut(grad_title, out, loss_eq, grad_out, num_val))
        self.clear()

        # ---------- Scene 5: Backpropagate to Hidden Neuron ----------
        back_title = Text("Backprop: propagate error to hidden layer", font_size=36).to_edge(UP)
        self.play(Write(back_title))
        
        # Network with gradients
        n_input = Circle(0.3, color=GREEN).shift(LEFT*4)
        n_hidden = Circle(0.3, color=GREEN).shift(LEFT*1)
        n_output = Circle(0.3, color=GREEN).shift(RIGHT*2)
        conn = Arrow(n_hidden.get_right(), n_output.get_left(), buff=0.1, color=YELLOW)
        
        grad_out_label = MathTex("\\delta_{out} = 2(\\hat{y}-y)", font_size=26).next_to(n_output, UP, buff=0.3)
        grad_hidden_label = MathTex("\\delta_h = w_2 \\cdot \\delta_{out}", font_size=26).next_to(n_hidden, UP, buff=0.3)
        
        self.play(Create(VGroup(n_input, n_hidden, n_output)), Create(conn))
        self.play(Write(grad_out_label))
        self.wait(0.5)
        # Animate the gradient flowing backward
        backward_arrow = Arrow(n_output.get_left(), n_hidden.get_right(), buff=0.2, color=RED)
        self.play(Create(backward_arrow))
        self.play(Write(grad_hidden_label))
        self.wait(1.5)
        
        weight_update = MathTex("w_2 \\leftarrow w_2 - \\eta \\frac{\\partial L}{\\partial w_2}", font_size=28).shift(DOWN*2.5)
        self.play(Write(weight_update))
        self.wait(1.5)
        self.play(FadeOut(back_title, n_input, n_hidden, n_output, conn, grad_out_label, grad_hidden_label, backward_arrow, weight_update))
        self.clear()

        # ---------- Scene 6: Full Chain for One Weight ----------
        full_title = Text("Full chain: from output to input weight", font_size=36).to_edge(UP)
        self.play(Write(full_title))
        
        eq1 = MathTex("\\frac{\\partial L}{\\partial w_1} = \\frac{\\partial L}{\\partial \\hat{y}} \\cdot \\frac{\\partial \\hat{y}}{\\partial h} \\cdot \\frac{\\partial h}{\\partial w_1}", font_size=30).shift(UP*0.5)
        self.play(Write(eq1))
        self.wait(1)
        
        # Decompose each term
        terms = VGroup(
            MathTex("\\frac{\\partial L}{\\partial \\hat{y}} = 2(\\hat{y}-y)", font_size=28, color=RED),
            MathTex("\\frac{\\partial \\hat{y}}{\\partial h} = w_2", font_size=28, color=BLUE),
            MathTex("\\frac{\\partial h}{\\partial w_1} = x \\cdot \\sigma'(z)", font_size=28, color=GREEN)
        ).arrange(DOWN, buff=0.4).shift(DOWN*1.2)
        
        for eq in terms:
            self.play(Write(eq))
            self.wait(1)
        
        final_eq = MathTex("\\frac{\\partial L}{\\partial w_1} = 2(\\hat{y}-y) \\cdot w_2 \\cdot x \\cdot \\sigma'(z)", font_size=28, color=YELLOW).shift(DOWN*3.2)
        self.play(Write(final_eq))
        self.wait(2)
        self.play(FadeOut(full_title, eq1, terms, final_eq))
        self.clear()

        # ---------- Scene 7: Multiple Layers Visualization ----------
        multi_title = Text("Deep network: gradients flow through all layers", font_size=36).to_edge(UP)
        self.play(Write(multi_title))
        
        # 4-layer network
        layers = []
        colors = [BLUE, GREEN, YELLOW, RED]
        for i, col in enumerate(colors):
            layer = VGroup(*[Circle(0.2, color=col) for _ in range(4-i)])
            layer.arrange(DOWN, buff=0.4).shift(RIGHT*(i*2 - 3))
            layers.append(layer)
        
        connections = VGroup()
        for i in range(len(layers)-1):
            for left_neuron in layers[i]:
                for right_neuron in layers[i+1]:
                    connections.add(Line(left_neuron.get_right(), right_neuron.get_left(), stroke_width=1, color=GREY))
        
        self.play(Create(connections), *[Create(layer) for layer in layers])
        self.wait(1)
        
        # Animate backward flow
        backward_arrows = VGroup()
        for i in reversed(range(len(layers)-1)):
            for left_n in layers[i]:
                for right_n in layers[i+1]:
                    arr = Arrow(right_n.get_left(), left_n.get_right(), buff=0.05, color=RED, stroke_width=2)
                    backward_arrows.add(arr)
        self.play(Create(backward_arrows), run_time=2)
        self.wait(1.5)
        self.play(FadeOut(multi_title, connections, *layers, backward_arrows))
        self.clear()

        # ---------- Scene 8: Weight Update Rule ----------
        update_title = Text("Gradient Descent: update each weight", font_size=36).to_edge(UP)
        self.play(Write(update_title))
        
        update = MathTex("\\theta_{t+1} = \\theta_t - \\eta \\nabla_\\theta L", font_size=40).shift(UP*0.5)
        self.play(Write(update))
        self.wait(1)
        
        # Show weight changes
        weight_example = VGroup(
            MathTex("w_1: 0.5 \\rightarrow 0.48", font_size=28, color=BLUE),
            MathTex("w_2: -0.3 \\rightarrow -0.29", font_size=28, color=GREEN),
            MathTex("w_3: 0.1 \\rightarrow 0.09", font_size=28, color=RED)
        ).arrange(DOWN, buff=0.3).shift(DOWN*1.5)
        
        for w in weight_example:
            self.play(Write(w))
            self.wait(0.8)
        
        self.wait(1.5)
        self.play(FadeOut(update_title, update, weight_example))
        self.clear()

        # ---------- Scene 9: Complete Backprop Loop ----------
        loop_title = Text("Backpropagation Algorithm Summary", font_size=36).to_edge(UP)
        self.play(Write(loop_title))
        
        steps = VGroup(
            Text("1. Forward pass: compute predictions", font_size=26),
            Text("2. Compute loss", font_size=26),
            Text("3. Compute gradient at output", font_size=26),
            Text("4. Propagate gradient backward layer by layer", font_size=26),
            Text("5. Update all weights using gradient descent", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(LEFT*1.5)
        
        for step in steps:
            self.play(Write(step), run_time=0.6)
        
        self.wait(1)
        
        # Animated cycle
        cycle_arrows = VGroup(
            Arrow(steps[0].get_left() + LEFT*0.5, steps[1].get_left() + LEFT*0.5, buff=0.1, color=YELLOW),
            Arrow(steps[1].get_left() + LEFT*0.5, steps[2].get_left() + LEFT*0.5, buff=0.1, color=YELLOW),
            Arrow(steps[2].get_left() + LEFT*0.5, steps[3].get_left() + LEFT*0.5, buff=0.1, color=YELLOW),
            Arrow(steps[3].get_left() + LEFT*0.5, steps[4].get_left() + LEFT*0.5, buff=0.1, color=YELLOW),
            CurvedArrow(steps[4].get_left() + LEFT*0.5, steps[0].get_left() + LEFT*0.5, angle=-PI/2, color=YELLOW)
        )
        self.play(Create(cycle_arrows))
        self.wait(2)
        self.play(FadeOut(loop_title, steps, cycle_arrows))
        self.clear()

        # ---------- Scene 10: Final Intuition & Recap ----------
        final_title = Text("Key Insight: Local Gradients × Chain Rule", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(final_title))
        
        insight = VGroup(
            Text("Each neuron only needs:", font_size=28),
            Text("• Its own local gradient", font_size=28, color=BLUE),
            Text("• The gradient from the neuron above", font_size=28, color=GREEN),
            Text("→ Multiply them and pass backward", font_size=28, color=RED)
        ).arrange(DOWN, buff=0.4).shift(UP*0.5)
        
        for line in insight:
            self.play(Write(line), run_time=0.8)
        
        self.wait(1)
        
        # Final network with gradient flow
        fin_net = VGroup(
            Circle(0.25, color=GREEN).shift(LEFT*3.5 + DOWN*0.5),
            Circle(0.25, color=GREEN).shift(DOWN*0.5),
            Circle(0.25, color=GREEN).shift(RIGHT*3.5 + DOWN*0.5),
            Line(LEFT*3.25 + DOWN*0.5, LEFT*0.25 + DOWN*0.5, color=GREY),
            Line(RIGHT*0.25 + DOWN*0.5, RIGHT*3.25 + DOWN*0.5, color=GREY)
        )
        grad_flow = Text("∇", font_size=40, color=RED).move_to(DOWN*0.5)
        
        self.play(Create(fin_net), Write(grad_flow))
        self.wait(1.5)
        
        # Final message
        final_msg = Text("That's backpropagation!", font_size=34, color=YELLOW).shift(DOWN*2.5)
        self.play(Write(final_msg))
        self.wait(2)
        
        # Fade out everything
        self.play(FadeOut(final_title, insight, fin_net, grad_flow, final_msg))
        self.clear()
