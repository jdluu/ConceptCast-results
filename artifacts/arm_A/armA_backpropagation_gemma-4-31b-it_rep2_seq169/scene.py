from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Introduction to the Network Structure ---
        title = Text("Backpropagation: How Networks Learn", color=BLUE).scale(0.8)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Simple 3-layer network
        layers = [2, 3, 1]
        nodes = VGroup()
        for i, size in enumerate(layers):
            layer_nodes = VGroup(*[Circle(radius=0.3, color=WHITE) for _ in range(size)])
            layer_nodes.arrange(DOWN, buff=0.5)
            layer_nodes.shift(RIGHT * i * 2 - RIGHT * 2)
            nodes.add(layer_nodes)

        connections = VGroup()
        for i in range(len(layers) - 1):
            for start_node in nodes[i]:
                for end_node in nodes[i+1]:
                    line = Line(start_node.get_right(), end_node.get_left(), stroke_width=2, color=GRAY)
                    connections.add(line)

        self.play(Create(nodes), Create(connections))
        self.wait(2)
        self.play(FadeOut(nodes), FadeOut(connections), FadeOut(title))
        self.clear()

        # --- Scene 2: The Forward Pass (Prediction) ---
        title2 = Text("Step 1: The Forward Pass", color=BLUE).to_edge(UP)
        self.play(Write(title2))

        # Simplified graph: Input -> Hidden -> Output
        in_node = Circle(radius=0.4, color=WHITE).shift(LEFT * 3)
        hid_node = Circle(radius=0.4, color=WHITE)
        out_node = Circle(radius=0.4, color=WHITE).shift(RIGHT * 3)
        
        labels = VGroup(
            Text("x", color=YELLOW).next_to(in_node, LEFT),
            Text("h", color=YELLOW).next_to(hid_node, UP),
            Text("ŷ", color=YELLOW).next_to(out_node, RIGHT)
        )

        conn1 = Line(in_node.get_right(), hid_node.get_left(), color=WHITE)
        conn2 = Line(hid_node.get_right(), out_node.get_left(), color=WHITE)
        weight1 = Text("w1", color=GREEN).scale(0.6).next_to(conn1, UP, buff=0.1)
        weight2 = Text("w2", color=GREEN).scale(0.6).next_to(conn2, UP, buff=0.1)

        self.play(Create(in_node), Create(hid_node), Create(out_node))
        self.play(Create(conn1), Create(conn2))
        self.play(Write(labels), Write(weight1), Write(weight2))

        # Animation of data flowing
        dot = Dot(color=YELLOW).move_to(in_node.get_center())
        self.play(FadeIn(dot))
        self.play(dot.animate.move_to(hid_node.get_center()), run_time=1)
        self.play(dot.animate.move_to(out_node.get_center()), run_time=1)
        
        self.wait(1)
        self.play(FadeOut(in_node), FadeOut(hid_node), FadeOut(out_node), 
                  FadeOut(conn1), FadeOut(conn2), FadeOut(labels), 
                  FadeOut(weight1), FadeOut(weight2), FadeOut(dot), FadeOut(title2))
        self.clear()

        # --- Scene 3: The Loss Function (Defining Error) ---
        title3 = Text("Step 2: Calculating Loss (Error)", color=BLUE).to_edge(UP)
        self.play(Write(title3))

        loss_eq = MathTex(
            "L = \\frac{1}{2}(\\hat{y} - y)^2", 
            color=RED
        ).scale(1.5)
        
        desc = Text("Loss measures how far the prediction (ŷ) is from truth (y)", 
                    font_size=24).next_to(loss_eq, DOWN, buff=1)

        self.play(Write(loss_eq))
        self.play(Write(desc))
        self.wait(2)
        
        self.play(FadeOut(loss_eq), FadeOut(desc), FadeOut(title3))
        self.clear()

        # --- Scene 4: The Chain Rule Concept ---
        title4 = Text("Step 3: The Chain Rule", color=BLUE).to_edge(UP)
        self.play(Write(title4))

        chain_eq = MathTex(
            "\\frac{\\partial L}{\\partial w_1} = \\frac{\\partial L}{\\partial \\hat{y}} \\times \\frac{\\partial \\hat{y}}{\\partial h} \\times \\frac{\\partial h}{\\partial w_1}",
            color=WHITE
        ).scale(0.9)

        # Highlight parts of the chain
        box1 = SurroundingRectangle(chain_eq[0][2:5], color=RED) # dL/dy_hat
        box2 = SurroundingRectangle(chain_eq[0][5:8], color=YELLOW) # dy_hat/dh
        box3 = SurroundingRectangle(chain_eq[0][8:], color=GREEN) # dh/dw1

        self.play(Write(chain_eq))
        self.wait(1)
        self.play(Create(box1))
        self.play(Create(box2))
        self.play(Create(box3))
        
        expl = Text("We decompose the total error into small local gradients", font_size=24).to_edge(DOWN)
        self.play(Write(expl))
        self.wait(2)
        self.play(FadeOut(chain_eq), FadeOut(box1), FadeOut(box2), FadeOut(box3), FadeOut(expl), FadeOut(title4))
        self.clear()

        # --- Scene 5: Backpropagating the Gradient ---
        title5 = Text("Step 4: Propagating Backward", color=BLUE).to_edge(UP)
        self.play(Write(title5))

        # Rebuild the simple network
        in_n = Circle(radius=0.3, color=WHITE).shift(LEFT * 3)
        hid_n = Circle(radius=0.3, color=WHITE)
        out_n = Circle(radius=0.3, color=WHITE).shift(RIGHT * 3)
        c1 = Line(in_n.get_right(), hid_n.get_left(), color=GRAY)
        c2 = Line(hid_n.get_right(), out_n.get_left(), color=GRAY)
        
        self.play(Create(in_n), Create(hid_n), Create(out_n), Create(c1), Create(c2))

        # Gradient signals
        grad_out = Text("dL/dy", color=RED).scale(0.5).next_to(out_n, RIGHT)
        grad_hid = Text("dL/dh", color=YELLOW).scale(0.5).next_to(hid_n, UP)
        grad_in = Text("dL/dw", color=GREEN).scale(0.5).next_to(in_n, LEFT)

        self.play(Write(grad_out))
        # Animate gradient moving back
        arrow1 = Arrow(out_n.get_center(), hid_n.get_center(), color=RED)
        self.play(GrowArrow(arrow1))
        self.play(Write(grad_hid))
        self.wait(1)

        arrow2 = Arrow(hid_n.get_center(), in_n.get_center(), color=YELLOW)
        self.play(GrowArrow(arrow2))
        self.play(Write(grad_in))
        self.wait(2)
        
        self.play(FadeOut(in_n), FadeOut(hid_n), FadeOut(out_n), 
                  FadeOut(c1), FadeOut(c2), FadeOut(grad_out), 
                  FadeOut(grad_hid), FadeOut(grad_in), 
                  FadeOut(arrow1), FadeOut(arrow2), FadeOut(title5))
        self.clear()

        # --- Scene 6: Weight Update (The Final Step) ---
        title6 = Text("Step 5: Updating Weights", color=BLUE).to_edge(UP)
        self.play(Write(title6))

        update_eq = MathTex(
            "w_{new} = w_{old} - \\eta \\cdot \\nabla L",
            color=WHITE
        ).scale(1.2)
        
        eta_text = Text("η (Learning Rate)", color=GREEN).scale(0.6).next_to(update_eq, DOWN, buff=1)
        
        self.play(Write(update_eq))
        self.play(Write(eta_text))
        self.wait(1)

        # Visual metaphor: Hill descending
        axis = Axes(x_range=[0, 4], y_range=[0, 4], axis_config={"include_tip": False})
        curve = axis.plot(lambda x: (x-2)**2 + 1, color=BLUE)
        dot_weight = Dot(color=RED).move_to(axis.c2p(0.5, (0.5-2)**2 + 1))
        
        self.play(Create(axis), Create(curve))
        self.play(FadeIn(dot_weight))
        
        # Step down the gradient
        self.play(dot_weight.animate.move_to(axis.c2p(1.2, (1.2-2)**2 + 1)), run_time=1)
        self.play(dot_weight.animate.move_to(axis.c2p(2.0, (2.0-2)**2 + 1)), run_time=1)

        self.wait(2)
        
        # Final Summary
        final_text = Text("Network Trained!", color=YELLOW).scale(1.5).to_edge(UP)
        self.play(FadeOut(title6), FadeOut(update_eq), FadeOut(eta_text), 
                  FadeOut(axis), FadeOut(curve), FadeOut(dot_weight))
        self.play(Write(final_text))
        self.wait(2)
