from manim import *

class SceneGen(Scene):
    def construct(self):
        # --- SCENE 1: The High Level Goal ---
        title = Text("Backpropagation: How Neural Networks Learn", color=WHITE).scale(0.8)
        subtitle = Text("Goal: Minimize the Error (Loss)", color=BLUE).scale(0.6).next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        
        concept_box = RoundedRectangle(corner_radius=0.2, height=2, width=6, color=WHITE)
        concept_text = Text("Input -> Weights -> Output -> Error", font_size=30).move_to(concept_box.get_center())
        
        self.play(Create(concept_box), Write(concept_text))
        self.play(title.animate.to_edge(UP), subtitle.animate.next_to(title, DOWN))
        self.wait(3)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(concept_box), FadeOut(concept_text))

        self.clear()

        # --- SCENE 2: The Forward Pass (The Setup) ---
        # Creating a simple 2-layer network
        input_nodes = VGroup(*[Dot(color=BLUE) for _ in range(2)]).arrange(DOWN, buff=1.5).shift(LEFT * 3)
        hidden_nodes = VGroup(*[Dot(color=GREEN) for _ in range(3)]).arrange(DOWN, buff=1).shift(ORIGIN)
        output_node = Dot(color=RED).shift(RIGHT * 3)
        
        labels = VGroup(
            Text("Input x", font_size=24).next_to(input_nodes, LEFT),
            Text("Hidden h", font_size=24).next_to(hidden_nodes, LEFT),
            Text("Output y", font_size=24).next_to(output_node, RIGHT)
        )

        connections = VGroup()
        for i in input_nodes:
            for j in hidden_nodes:
                connections.add(Line(i.get_center(), j.get_center(), stroke_width=2, color=GRAY))
        for j in hidden_nodes:
            connections.add(Line(j.get_center(), output_node.get_center(), stroke_width=2, color=GRAY))

        self.play(FadeIn(input_nodes), FadeIn(hidden_nodes), FadeIn(output_node), Write(labels))
        self.play(Create(connections))
        
        # Animate signal flow
        flow_dots = VGroup()
        for line in connections:
            dot = Dot(color=YELLOW, radius=0.05).move_to(line.get_start())
            flow_dots.add(dot)
        
        self.play(
            AnimationGroup(
                *[MoveAlongPath(dot, line) for dot, line in zip(flow_dots, connections)],
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.wait(1)
        self.play(FadeOut(input_nodes), FadeOut(hidden_nodes), FadeOut(output_node), FadeOut(labels), FadeOut(connections), FadeOut(flow_dots))

        self.clear()

        # --- SCENE 3: The Loss Function (The Error) ---
        loss_text = Text("The Loss Function L", color=RED).shift(UP * 2)
        formula = MathTex(r"L = \frac{1}{2}(\text{target} - \text{predicted})^2").scale(1.2)
        
        target_val = Text("Target: 1.0", color=GREEN).shift(LEFT * 3 + DOWN * 1)
        pred_val = Text("Predicted: 0.4", color=RED).shift(RIGHT * 3 + DOWN * 1)
        
        diff_arrow = Arrow(pred_val.get_left(), target_val.get_right(), color=YELLOW)
        diff_label = Text("Error (Gap)", font_size=20, color=YELLOW).next_to(diff_arrow, UP)

        self.play(Write(loss_text))
        self.play(Write(formula))
        self.play(Write(target_val), Write(pred_val))
        self.play(Create(diff_arrow), Write(diff_label))
        self.wait(2)
        
        # Transition: We need to know how to change weights to close this gap
        expl_text = Text("How do we change weights to reduce L?", font_size=30).shift(DOWN * 3)
        self.play(Write(expl_text))
        self.wait(3)
        self.play(FadeOut(loss_text), FadeOut(formula), FadeOut(target_val), FadeOut(pred_val), FadeOut(diff_arrow), FadeOut(diff_label), FadeOut(expl_text))

        self.clear()

        # --- SCENE 4: The Chain Rule (The Math Engine) ---
        chain_title = Text("The Chain Rule", color=BLUE).to_edge(UP)
        
        # Variables: L -> y -> w
        var_l = Text("L (Loss)").shift(RIGHT * 3 + UP * 1)
        var_y = Text("y (Output)").shift(ORIGIN)
        var_w = Text("w (Weight)").shift(LEFT * 3 + DOWN * 1)
        
        arrow1 = Arrow(var_y.get_center(), var_l.get_center(), color=WHITE)
        arrow2 = Arrow(var_w.get_center(), var_y.get_center(), color=WHITE)
        
        self.play(Write(chain_title))
        self.play(Write(var_l), Write(var_y), Write(var_w))
        self.play(Create(arrow1), Create(arrow2))
        
        # Derivatives
        grad1 = MathTex(r"\frac{\partial L}{\partial y}").next_to(arrow1, UP, buff=0.1).scale(0.8)
        grad2 = MathTex(r"\frac{\partial y}{\partial w}").next_to(arrow2, UP, buff=0.1).scale(0.8)
        
        self.play(Write(grad1))
        self.play(Write(grad2))
        self.wait(1)
        
        final_grad = MathTex(r"\frac{\partial L}{\partial w} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial w}", color=YELLOW).shift(DOWN * 3)
        self.play(Write(final_grad))
        self.play(Indicate(final_grad))
        self.wait(3)
        self.play(FadeOut(chain_title), FadeOut(var_l), FadeOut(var_y), FadeOut(var_w), FadeOut(arrow1), FadeOut(arrow2), FadeOut(grad1), FadeOut(grad2), FadeOut(final_grad))

        self.clear()

        # --- SCENE 5: Propagating Backwards (Visualizing the Flow) ---
        # Re-create the network
        input_nodes = VGroup(*[Dot(color=BLUE) for _ in range(2)]).arrange(DOWN, buff=1.5).shift(LEFT * 3)
        hidden_nodes = VGroup(*[Dot(color=GREEN) for _ in range(3)]).arrange(DOWN, buff=1).shift(ORIGIN)
        output_node = Dot(color=RED).shift(RIGHT * 3)
        
        connections = VGroup()
        for i in input_nodes:
            for j in hidden_nodes:
                connections.add(Line(i.get_center(), j.get_center(), stroke_width=2, color=GRAY))
        for j in hidden_nodes:
            connections.add(Line(j.get_center(), output_node.get_center(), stroke_width=2, color=GRAY))

        self.play(FadeIn(input_nodes), FadeIn(hidden_nodes), FadeIn(output_node), Create(connections))
        
        # Backprop animation
        back_dots = VGroup()
        # Output to Hidden
        for j in hidden_nodes:
            dot = Dot(color=ORANGE, radius=0.08).move_to(output_node.get_center())
            back_dots.add(dot)
        
        # Corrected: Wrapped Text in Write()
        backprop_text = Text("Backpropagating Gradients...", font_size=30).to_edge(UP)
        self.play(Write(backprop_text))
        
        # Wave 1: Output -> Hidden
        wave1_anims = [MoveAlongPath(dot, Line(output_node.get_center(), j.get_center())) for dot, j in zip(back_dots, hidden_nodes)]
        self.play(*wave1_anims, run_time=1.5)
        
        # Wave 2: Hidden -> Input
        wave2_dots = VGroup()
        for h in hidden_nodes:
            for i in input_nodes:
                dot = Dot(color=ORANGE, radius=0.08).move_to(h.get_center())
                wave2_dots.add(dot)
        
        # Match dots to specific lines
        wave2_anims = []
        dot_idx = 0
        for h in hidden_nodes:
            for i in input_nodes:
                wave2_anims.append(MoveAlongPath(wave2_dots[dot_idx], Line(h.get_center(), i.get_center())))
                dot_idx += 1
        
        self.play(*wave2_anims, run_time=1.5)
        self.wait(2)
        
        self.play(FadeOut(input_nodes), FadeOut(hidden_nodes), FadeOut(output_node), FadeOut(connections), FadeOut(back_dots), FadeOut(wave2_dots), FadeOut(backprop_text))

        self.clear()

        # --- SCENE 6: Gradient Descent (The Final Step) ---
        final_text = Text("The Result: Weight Update", color=WHITE).to_edge(UP)
        update_rule = MathTex(r"w_{new} = w_{old} - \eta \cdot \frac{\partial L}{\partial w}", color=YELLOW).scale(1.5)
        
        eta_expl = Text("η (Eta) = Learning Rate", font_size=30, color=BLUE).next_to(update_rule, DOWN, buff=0.5)
        
        self.play(Write(final_text))
        self.play(Write(update_rule))
        self.play(Write(eta_expl))
        
        conclusion = Text("Error is reduced, the network learns!", font_size=35).shift(DOWN * 2)
        self.play(Write(conclusion))
        self.play(Indicate(conclusion))
        self.wait(4)
        
        self.play(FadeOut(final_text), FadeOut(update_rule), FadeOut(eta_expl), FadeOut(conclusion))
