from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Introduction and forward pass
        title1 = Text("Backpropagation", font_size=72)
        subtitle1 = Text("Training Neural Networks with Gradient Descent", font_size=36)
        subtitle1.next_to(title1, DOWN)
        self.play(Write(title1), Write(subtitle1))
        self.wait(1)
        
        self.play(FadeOut(title1), FadeOut(subtitle1))
        
        input_node = Circle(radius=0.4, color=BLUE).shift(LEFT*4)
        hidden_node = Circle(radius=0.4, color=GREEN).shift(ORIGIN)
        output_node = Circle(radius=0.4, color=RED).shift(RIGHT*4)
        input_label = Text("x").next_to(input_node)
        hidden_label = Text("h").next_to(hidden_node)
        output_label = Text("ŷ").next_to(output_node)
        
        line1 = Line(input_node.get_right(), hidden_node.get_left(), color=WHITE)
        line2 = Line(hidden_node.get_right(), output_node.get_left(), color=WHITE)
        
        forward_text = Text("Forward Pass: x → h → ŷ", font_size=36).to_edge(UP)
        self.play(Create(input_node), Write(input_label))
        self.play(Create(line1), Create(hidden_node), Write(hidden_label))
        self.play(Create(line2), Create(output_node), Write(output_label))
        self.play(Write(forward_text))
        self.wait(1.5)
        self.play(*[FadeOut(mob) for mob in [input_node, hidden_node, output_node, input_label, hidden_label, output_label, line1, line2, forward_text]])

        self.clear()

        # Scene 2: Loss definition
        title2 = Text("Step 1: Compute Loss", font_size=48)
        y_true = MathTex("y").scale(1.2).shift(LEFT*2)
        y_hat = MathTex("\\hat{y}").scale(1.2).shift(RIGHT*2)
        loss_eq = MathTex("L = \\frac12 (y - \\hat{y})^2").scale(1.5).to_edge(UP)
        arrow = Arrow(y_true.get_right(), y_hat.get_left(), color=YELLOW)
        
        self.play(Write(title2))
        self.play(Write(y_true), Write(y_hat), Create(arrow))
        self.play(Write(loss_eq))
        self.play(Indicate(loss_eq, color=RED))
        self.wait(1)
        self.play(FadeOut(title2), FadeOut(y_true), FadeOut(y_hat), FadeOut(arrow), FadeOut(loss_eq))

        self.clear()

        # Scene 3: Chain rule intuition
        title3 = Text("Step 2: Chain Rule", font_size=48)
        chain = MathTex("\\frac{dL}{dw}=\\frac{dL}{d\\hat{y}}\\frac{d\\hat{y}}{dh}\\frac{dh}{dw}").scale(1.2).to_edge(UP)
        bullet1 = Text("Gradients flow backward", font_size=32).next_to(chain, DOWN)
        bullet2 = Text("Each layer multiplies local derivatives", font_size=32).next_to(bullet1, DOWN)
        
        self.play(Write(title3))
        self.play(Write(chain))
        self.play(Write(bullet1), Write(bullet2))
        self.play(chain.animate.set_color(YELLOW))
        self.wait(1)
        self.play(FadeOut(title3), FadeOut(chain), FadeOut(bullet1), FadeOut(bullet2))

        self.clear()

        # Scene 4: Computation graph
        title4 = Text("Step 3: Computation Graph", font_size=48)
        nodes = VGroup(*[Circle(radius=0.35, color=WHITE) for _ in range(4)])
        nodes.arrange(RIGHT, buff=2)
        labels = VGroup(MathTex("x"), MathTex("w"), MathTex("h"), MathTex("L")).arrange(RIGHT, buff=2)
        labels.next_to(nodes, DOWN, buff=0.1)
        graph = VGroup(nodes, labels)
        
        edges = VGroup(Line(nodes[0].get_right(), nodes[1].get_left()),
                       Line(nodes[1].get_right(), nodes[2].get_left()),
                       Line(nodes[2].get_right(), nodes[3].get_left()))
        
        self.play(Write(title4))
        self.play(Create(graph), Create(edges))
        self.play(Indicate(nodes[0]), Indicate(nodes[3]))
        self.wait(1)
        self.play(FadeOut(title4), FadeOut(graph), FadeOut(edges))

        self.clear()

        # Scene 5: Backward pass
        title5 = Text("Step 4: Backpropagate Errors", font_size=48)
        h_node = Circle(radius=0.5, color=GREEN).shift(LEFT*2)
        o_node = Circle(radius=0.5, color=RED).shift(RIGHT*2)
        w_text = Text("w").scale(1.5).shift(UP*1.5)
        grad_arrow1 = Arrow(o_node.get_left(), h_node.get_right(), color=ORANGE, buff=0.5)
        grad_arrow2 = Arrow(h_node.get_left(), h_node.get_left(), color=ORANGE)
        grad_label = MathTex("\\frac{\\partial L}{\\partial w}").next_to(w_text, DOWN)
        
        self.play(Write(title5))
        self.play(Create(h_node), Create(o_node), Write(w_text))
        self.play(Create(grad_arrow1))
        self.play(Create(grad_arrow2))
        self.play(Write(grad_label))
        self.play(grad_arrow1.animate.set_color(YELLOW), grad_arrow2.animate.set_color(YELLOW))
        self.wait(1)
        self.play(FadeOut(title5), FadeOut(h_node), FadeOut(o_node), FadeOut(w_text), FadeOut(grad_arrow1), FadeOut(grad_arrow2), FadeOut(grad_label))

        self.clear()

        # Scene 6: Weight update
        title6 = Text("Step 5: Update Weights", font_size=48)
        update_eq = MathTex("w_{new} = w_{old} - \\eta \\frac{\\partial L}{\\partial w}").scale(1.2).to_edge(UP)
        eta = MathTex("\\eta = \\text{learning rate}").next_to(update_eq, DOWN)
        down_arrow = Arrow(update_eq.get_bottom(), update_eq.get_bottom()+DOWN*0.5, color=GREEN)
        self.play(Write(title6))
        self.play(Write(update_eq))
        self.play(Write(eta), Create(down_arrow))
        self.play(Indicate(update_eq, color=GREEN))
        self.wait(1)
        self.play(FadeOut(title6), FadeOut(update_eq), FadeOut(eta), FadeOut(down_arrow))

        self.clear()

        # Scene 7: Summary loop
        title7 = Text("Backpropagation Loop", font_size=60)
        loop_text = VGroup(
            Text("1. Forward pass", font_size=36),
            Text("2. Compute loss", font_size=36),
            Text("3. Backward pass", font_size=36),
            Text("4. Update weights", font_size=36)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title7, DOWN)
        
        self.play(Write(title7))
        for i, line in enumerate(loop_text):
            self.play(Write(line), run_time=0.5)
        self.play(loop_text.animate.set_color(BLUE))
        self.wait(2)
        self.play(FadeOut(title7), FadeOut(loop_text))
