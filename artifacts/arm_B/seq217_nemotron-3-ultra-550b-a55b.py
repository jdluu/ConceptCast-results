from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Computational Graph Introduction
        title1 = Text("1. Computational Graph", font_size=48).to_edge(UP)
        self.play(Write(title1))

        # Simple function: f = (x + y) * z
        x_node = Circle(radius=0.5, color=BLUE).shift(LEFT*4 + UP*2)
        x_label = MathTex("x").move_to(x_node)
        y_node = Circle(radius=0.5, color=BLUE).shift(LEFT*4)
        y_label = MathTex("y").move_to(y_node)
        z_node = Circle(radius=0.5, color=BLUE).shift(LEFT*4 + DOWN*2)
        z_label = MathTex("z").move_to(z_node)

        add_node = Circle(radius=0.6, color=GREEN).shift(LEFT*1)
        add_label = Text("+", font_size=36).move_to(add_node)
        mul_node = Circle(radius=0.6, color=RED).shift(RIGHT*2)
        mul_label = Text("\u00d7", font_size=36).move_to(mul_node)
        out_node = Circle(radius=0.5, color=YELLOW).shift(RIGHT*5)
        out_label = MathTex("f").move_to(out_node)

        edges = VGroup(
            Arrow(x_node.get_right(), add_node.get_left(), buff=0.1),
            Arrow(y_node.get_right(), add_node.get_left(), buff=0.1),
            Arrow(z_node.get_right(), mul_node.get_left(), buff=0.1),
            Arrow(add_node.get_right(), mul_node.get_left(), buff=0.1),
            Arrow(mul_node.get_right(), out_node.get_left(), buff=0.1)
        )

        self.play(
            *[Create(m) for m in [x_node, y_node, z_node, add_node, mul_node, out_node]],
            *[Write(m) for m in [x_label, y_label, z_label, add_label, mul_label, out_label]],
            *[Create(e) for e in edges],
            run_time=3
        )
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # Scene 2: Forward Pass Values
        title2 = Text("2. Forward Pass: Compute Values", font_size=48).to_edge(UP)
        self.play(Write(title2))

        # Values: x=2, y=3, z=4 -> q = x+y = 5 -> f = q*z = 20
        val_x = VGroup(Circle(radius=0.5, color=BLUE), MathTex("2")).arrange(DOWN, buff=0.1).shift(LEFT*4 + UP*2)
        val_y = VGroup(Circle(radius=0.5, color=BLUE), MathTex("3")).arrange(DOWN, buff=0.1).shift(LEFT*4)
        val_z = VGroup(Circle(radius=0.5, color=BLUE), MathTex("4")).arrange(DOWN, buff=0.1).shift(LEFT*4 + DOWN*2)
        
        val_add = VGroup(Circle(radius=0.6, color=GREEN), MathTex("5")).arrange(DOWN, buff=0.1).shift(LEFT*1)
        val_mul = VGroup(Circle(radius=0.6, color=RED), MathTex("20")).arrange(DOWN, buff=0.1).shift(RIGHT*2)
        val_out = VGroup(Circle(radius=0.5, color=YELLOW), MathTex("20")).arrange(DOWN, buff=0.1).shift(RIGHT*5)

        self.play(
            *[FadeIn(m) for m in [val_x, val_y, val_z, val_add, val_mul, val_out]],
            run_time=2
        )
        
        eq1 = MathTex("q = x + y = 2 + 3 = 5").next_to(val_add, DOWN)
        eq2 = MathTex("f = q \\times z = 5 \\times 4 = 20").next_to(val_mul, DOWN)
        self.play(Write(eq1), Write(eq2))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # Scene 3: Loss Function & Gradient Start
        title3 = Text("3. Loss Function & Output Gradient", font_size=48).to_edge(UP)
        self.play(Write(title3))

        loss_eq = MathTex("L = \\frac{1}{2}(f - y_{target})^2").scale(1.2)
        self.play(Write(loss_eq))
        self.wait(1)

        target_val = MathTex("y_{target} = 23").next_to(loss_eq, DOWN)
        self.play(Write(target_val))
        self.wait(1)

        loss_calc = MathTex("L = \\frac{1}{2}(20 - 23)^2 = 4.5").next_to(target_val, DOWN)
        self.play(Write(loss_calc))
        self.wait(1)

        grad_eq = MathTex("\\frac{\\partial L}{\\partial f} = (f - y_{target}) = -3").next_to(loss_calc, DOWN)
        self.play(Write(grad_eq))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # Scene 4: Chain Rule Concept
        title4 = Text("4. Chain Rule: The Core Mechanism", font_size=48).to_edge(UP)
        self.play(Write(title4))

        chain_rule = MathTex("\\frac{\\partial L}{\\partial x} = \\frac{\\partial L}{\\partial f} \\cdot \\frac{\\partial f}{\\partial q} \\cdot \\frac{\\partial q}{\\partial x}").scale(1.1)
        self.play(Write(chain_rule))
        self.wait(2)

        explanation = Text("Global gradient = Product of local gradients", font_size=36, color=YELLOW).next_to(chain_rule, DOWN)
        self.play(Write(explanation))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # Scene 5: Backward Pass - Multiplication Gate
        title5 = Text("5. Backward Pass: Multiplication Gate", font_size=48).to_edge(UP)
        self.play(Write(title5))

        mul_gate = VGroup(
            Circle(radius=0.8, color=RED),
            Text("\u00d7", font_size=48)
        ).move_to(ORIGIN)
        
        inputs = VGroup(
            MathTex("q=5").next_to(mul_gate, LEFT*2),
            MathTex("z=4").next_to(mul_gate, DOWN*2)
        )
        output = MathTex("f=20").next_to(mul_gate, RIGHT*2)
        grad_output = MathTex("\\frac{\\partial L}{\\partial f} = -3", color=RED).next_to(output, UP)

        self.play(Create(mul_gate), Write(inputs), Write(output), Write(grad_output))

        local_grads = VGroup(
            MathTex("\\frac{\\partial f}{\\partial q} = z = 4").next_to(mul_gate, UP*2 + LEFT),
            MathTex("\\frac{\\partial f}{\\partial z} = q = 5").next_to(mul_gate, UP*2 + RIGHT)
        )
        self.play(Write(local_grads))
        self.wait(1)

        chain_calc = VGroup(
            MathTex("\\frac{\\partial L}{\\partial q} = -3 \\times 4 = -12", color=BLUE).next_to(inputs[0], UP),
            MathTex("\\frac{\\partial L}{\\partial z} = -3 \\times 5 = -15", color=BLUE).next_to(inputs[1], LEFT)
        )
        self.play(Write(chain_calc))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # Scene 6: Backward Pass - Addition Gate
        title6 = Text("6. Backward Pass: Addition Gate", font_size=48).to_edge(UP)
        self.play(Write(title6))

        add_gate = VGroup(
            Circle(radius=0.8, color=GREEN),
            Text("+", font_size=48)
        ).move_to(ORIGIN)
        
        inputs_add = VGroup(
            MathTex("x=2").next_to(add_gate, LEFT*2 + UP),
            MathTex("y=3").next_to(add_gate, LEFT*2 + DOWN)
        )
        output_add = MathTex("q=5").next_to(add_gate, RIGHT*2)
        grad_output_add = MathTex("\\frac{\\partial L}{\\partial q} = -12", color=RED).next_to(output_add, UP)

        self.play(Create(add_gate), Write(inputs_add), Write(output_add), Write(grad_output_add))

        local_grads_add = VGroup(
            MathTex("\\frac{\\partial q}{\\partial x} = 1").next_to(add_gate, UP*2 + LEFT),
            MathTex("\\frac{\\partial q}{\\partial y} = 1").next_to(add_gate, UP*2 + RIGHT)
        )
        self.play(Write(local_grads_add))
        self.wait(1)

        chain_calc_add = VGroup(
            MathTex("\\frac{\\partial L}{\\partial x} = -12 \\times 1 = -12", color=BLUE).next_to(inputs_add[0], UP),
            MathTex("\\frac{\\partial L}{\\partial y} = -12 \\times 1 = -12", color=BLUE).next_to(inputs_add[1], DOWN)
        )
        self.play(Write(chain_calc_add))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # Scene 7: Parameter Update (Gradient Descent)
        title7 = Text("7. Gradient Descent Update", font_size=48).to_edge(UP)
        self.play(Write(title7))

        update_rule = MathTex("w_{new} = w_{old} - \\eta \\cdot \\nabla L").scale(1.2)
        self.play(Write(update_rule))
        self.wait(1)

        eta = MathTex("\\eta = 0.1 \\text{ (Learning Rate)}").next_to(update_rule, DOWN)
        self.play(Write(eta))
        self.wait(1)

        updates = VGroup(
            MathTex("x_{new} = 2 - 0.1(-12) = 3.2"),
            MathTex("y_{new} = 3 - 0.1(-12) = 4.2"),
            MathTex("z_{new} = 4 - 0.1(-15) = 5.5")
        ).arrange(DOWN, buff=0.5).next_to(eta, DOWN)
        
        self.play(Write(updates))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # Scene 8: Neural Network Context
        title8 = Text("8. Scaling to Neural Networks", font_size=48).to_edge(UP)
        self.play(Write(title8))

        # Simple 2-layer NN diagram
        layer1 = VGroup(*[Circle(radius=0.3, color=BLUE) for _ in range(3)]).arrange(DOWN, buff=0.5).shift(LEFT*3)
        layer2 = VGroup(*[Circle(radius=0.3, color=GREEN) for _ in range(4)]).arrange(DOWN, buff=0.3).shift(RIGHT*0.5)
        layer3 = VGroup(*[Circle(radius=0.3, color=RED) for _ in range(2)]).arrange(DOWN, buff=0.5).shift(RIGHT*4)

        weights1 = VGroup(*[Line(layer1[i].get_right(), layer2[j].get_left(), stroke_width=1, color=GREY) 
                          for i in range(3) for j in range(4)])
        weights2 = VGroup(*[Line(layer2[i].get_right(), layer3[j].get_left(), stroke_width=1, color=GREY) 
                          for i in range(4) for j in range(2)])

        labels = VGroup(
            Text("Input", font_size=24).next_to(layer1, UP),
            Text("Hidden", font_size=24).next_to(layer2, UP),
            Text("Output", font_size=24).next_to(layer3, UP)
        )

        self.play(Create(layer1), Create(layer2), Create(layer3), Create(labels))
        self.play(Create(weights1), Create(weights2), run_time=2)
        self.wait(1)

        bp_arrow = Arrow(RIGHT*5, LEFT*5, color=RED, stroke_width=5).shift(DOWN*2)
        bp_text = Text("Backpropagation", color=RED, font_size=36).next_to(bp_arrow, DOWN)
        self.play(Create(bp_arrow), Write(bp_text))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        # Scene 9: Summary
        title9 = Text("9. Backpropagation Summary", font_size=48).to_edge(UP)
        self.play(Write(title9))

        summary_points = VGroup(
            Text("\u2022 Forward Pass: Compute outputs & cache values", font_size=32),
            Text("\u2022 Compute Loss: Measure error", font_size=32),
            Text("\u2022 Backward Pass: Chain rule from output to input", font_size=32),
            Text("\u2022 Local Gradients: Each gate computes \u2202out/\u2202in", font_size=32),
            Text("\u2022 Global Gradients: Multiply along path", font_size=32),
            Text("\u2022 Update: Gradient descent step", font_size=32)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(title9, DOWN, buff=0.5)

        for point in summary_points:
            self.play(Write(point), run_time=0.5)
        self.wait(3)
