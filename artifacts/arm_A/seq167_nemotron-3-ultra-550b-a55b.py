from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Introduction - Function Composition
        title = Text("Backpropagation", font_size=60).to_edge(UP)
        subtitle = Text("Computing Gradients via the Chain Rule", font_size=36).next_to(title, DOWN)
        
        self.play(Write(title), FadeIn(subtitle, shift=UP))
        self.wait(1)
        
        # Simple composition: f(g(x))
        eq = MathTex("y = f(g(x))", font_size=72).move_to(ORIGIN)
        self.play(Write(eq))
        self.wait(1)
        
        # Break it down
        brace_g = Brace(eq[0][4:7], DOWN, buff=0.2)
        text_g = brace_g.get_text("Inner function: g(x)").scale(0.7)
        brace_f = Brace(eq[0][2:4], DOWN, buff=0.2)
        text_f = brace_f.get_text("Outer function: f(u)").scale(0.7)
        
        self.play(GrowFromCenter(brace_g), Write(text_g))
        self.play(GrowFromCenter(brace_f), Write(text_f))
        self.wait(2)
        
        # Chain rule formula
        chain_rule = MathTex(r"\frac{dy}{dx} = \frac{df}{du} \cdot \frac{du}{dx}", font_size=60).next_to(text_g, DOWN, buff=1)
        self.play(Write(chain_rule))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()
        
        # Scene 2: Computational Graph Representation
        title2 = Text("Computational Graph View", font_size=50).to_edge(UP)
        self.play(Write(title2))
        
        # Nodes
        x_node = Circle(radius=0.5, color=BLUE, fill_opacity=0.3).shift(LEFT*4)
        x_label = MathTex("x").move_to(x_node)
        
        u_node = Circle(radius=0.5, color=GREEN, fill_opacity=0.3).shift(LEFT*1)
        u_label = MathTex("u = g(x)").move_to(u_node)
        
        y_node = Circle(radius=0.5, color=RED, fill_opacity=0.3).shift(RIGHT*2)
        y_label = MathTex("y = f(u)").move_to(y_node)
        
        # Edges
        edge_xu = Arrow(x_node.get_right(), u_node.get_left(), buff=0.1)
        edge_uy = Arrow(u_node.get_right(), y_node.get_left(), buff=0.1)
        
        # Labels on edges
        label_g = MathTex(r"\frac{\partial u}{\partial x}").next_to(edge_xu, UP, buff=0.1).scale(0.7)
        label_f = MathTex(r"\frac{\partial y}{\partial u}").next_to(edge_uy, UP, buff=0.1).scale(0.7)
        
        graph = VGroup(x_node, x_label, u_node, u_label, y_node, y_label, edge_xu, edge_uy, label_g, label_f)
        self.play(LaggedStart(*[Create(m) for m in [x_node, x_label, u_node, u_label, y_node, y_label]], lag_ratio=0.2))
        self.play(LaggedStart(*[GrowArrow(m) for m in [edge_xu, edge_uy]], lag_ratio=0.2))
        self.play(LaggedStart(*[Write(m) for m in [label_g, label_f]], lag_ratio=0.2))
        self.wait(2)
        
        # Forward pass values
        forward_vals = VGroup(
            MathTex("x = 2").next_to(x_node, DOWN),
            MathTex("u = 3").next_to(u_node, DOWN),
            MathTex("y = 9").next_to(y_node, DOWN)
        )
        self.play(LaggedStart(*[FadeIn(v, shift=UP) for v in forward_vals], lag_ratio=0.2))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()
        
        # Scene 3: Loss Function and Gradient Flow
        title3 = Text("Adding a Loss Function", font_size=50).to_edge(UP)
        self.play(Write(title3))
        
        # Extend graph with loss
        y_node2 = Circle(radius=0.5, color=RED, fill_opacity=0.3).shift(LEFT*1)
        y_label2 = MathTex("y").move_to(y_node2)
        
        target_node = Circle(radius=0.5, color=YELLOW, fill_opacity=0.3).shift(RIGHT*1)
        target_label = MathTex("\\hat{y}").move_to(target_node)
        
        loss_node = Circle(radius=0.5, color=PURPLE, fill_opacity=0.3).shift(RIGHT*3)
        loss_label = MathTex("L").move_to(loss_node)
        
        edge_yt = Arrow(y_node2.get_right(), target_node.get_left(), buff=0.1)
        edge_tl = Arrow(target_node.get_right(), loss_node.get_left(), buff=0.1)
        
        # Loss derivative
        dL_dy = MathTex(r"\frac{\partial L}{\partial y}").next_to(edge_yt, UP).scale(0.7)
        
        loss_graph = VGroup(y_node2, y_label2, target_node, target_label, loss_node, loss_label, edge_yt, edge_tl, dL_dy)
        self.play(LaggedStart(*[Create(m) for m in loss_graph], lag_ratio=0.15))
        self.wait(1)
        
        # Show loss computation (MSE)
        loss_eq = MathTex("L = \\frac{1}{2}(y - \\hat{y})^2", font_size=48).next_to(loss_node, DOWN, buff=0.5)
        grad_eq = MathTex(r"\frac{\partial L}{\partial y} = y - \hat{y}", font_size=48).next_to(loss_eq, DOWN)
        
        self.play(Write(loss_eq))
        self.play(Write(grad_eq))
        self.wait(2)
        
        # Numerical example
        num_example = VGroup(
            MathTex("y = 9").next_to(y_node2, DOWN),
            MathTex("\\hat{y} = 5").next_to(target_node, DOWN),
            MathTex(r"\frac{\partial L}{\partial y} = 4").next_to(dL_dy, DOWN).set_color(YELLOW)
        )
        self.play(LaggedStart(*[FadeIn(v) for v in num_example], lag_ratio=0.2))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()
        
        # Scene 4: Backward Pass - Chain Rule in Action
        title4 = Text("Backward Pass: Propagating Gradients", font_size=45).to_edge(UP)
        self.play(Write(title4))
        
        # Full graph with gradients
        nodes = VGroup()
        edges = VGroup()
        grad_labels = VGroup()
        
        # Create nodes
        positions = [LEFT*5, LEFT*2.5, ORIGIN, RIGHT*2.5, RIGHT*5]
        labels = ["x", "u = g(x)", "y = f(u)", "\\hat{y}", "L"]
        colors = [BLUE, GREEN, RED, YELLOW, PURPLE]
        
        for pos, label, color in zip(positions, labels, colors):
            node = Circle(radius=0.5, color=color, fill_opacity=0.3).move_to(pos)
            node_label = MathTex(label).move_to(node)
            nodes.add(VGroup(node, node_label))
        
        # Create edges (forward)
        for i in range(len(nodes)-1):
            edge = Arrow(nodes[i][0].get_right(), nodes[i+1][0].get_left(), buff=0.1, color=GREY)
            edges.add(edge)
        
        # Gradient labels (backward)
        grad_texts = [
            r"\frac{\partial L}{\partial x}",
            r"\frac{\partial L}{\partial u}",
            r"\frac{\partial L}{\partial y}",
            r"\frac{\partial L}{\partial \hat{y}}"
        ]
        
        for i, text in enumerate(grad_texts):
            grad_label = MathTex(text, font_size=36).next_to(edges[i], DOWN, buff=0.2)
            grad_labels.add(grad_label)
        
        # Animate graph construction
        self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.1))
        self.play(LaggedStart(*[GrowArrow(e) for e in edges], lag_ratio=0.1))
        self.wait(1)
        
        # Show backward pass animation
        backward_arrows = VGroup()
        for i in range(len(edges)-1, -1, -1):
            back_arrow = Arrow(edges[i].get_end(), edges[i].get_start(), buff=0.1, color=YELLOW, stroke_width=4)
            backward_arrows.add(back_arrow)
        
        # Animate gradient flow
        self.play(LaggedStart(*[GrowArrow(ba) for ba in backward_arrows], lag_ratio=0.3))
        self.play(LaggedStart(*[Write(gl) for gl in grad_labels], lag_ratio=0.2))
        self.wait(2)
        
        # Chain rule expansion
        chain_expansion = VGroup(
            MathTex(r"\frac{\partial L}{\partial u} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial u}", font_size=40),
            MathTex(r"\frac{\partial L}{\partial x} = \frac{\partial L}{\partial u} \cdot \frac{\partial u}{\partial x}", font_size=40)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=1)
        
        self.play(LaggedStart(*[Write(ce) for ce in chain_expansion], lag_ratio=0.3))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()
        
        # Scene 5: Neural Network Layer Visualization
        title5 = Text("Neural Network Layer: Vectorized Backprop", font_size=45).to_edge(UP)
        self.play(Write(title5))
        
        # Layer diagram
        # Input vector
        input_vec = VGroup(*[Square(side_length=0.6, color=BLUE, fill_opacity=0.3) for _ in range(3)]).arrange(DOWN, buff=0.1).shift(LEFT*4)
        input_labels = VGroup(*[MathTex(f"x_{i}").move_to(input_vec[i]) for i in range(3)])
        input_group = VGroup(input_vec, input_labels)
        input_title = Text("Input", font_size=24).next_to(input_vec, UP)
        
        # Weight matrix
        weight_matrix = VGroup(*[
            VGroup(*[Square(side_length=0.5, color=GREEN, fill_opacity=0.2) for _ in range(3)]).arrange(RIGHT, buff=0.05)
            for _ in range(2)
        ]).arrange(DOWN, buff=0.05).shift(LEFT*0.5)
        weight_labels = VGroup(*[
            VGroup(*[MathTex(f"W_{j}{i}", font_size=16).move_to(weight_matrix[j][i]) for i in range(3)])
            for j in range(2)
        ])
        weight_group = VGroup(weight_matrix, weight_labels)
        weight_title = Text("Weights W", font_size=24).next_to(weight_matrix, UP)
        
        # Output vector
        output_vec = VGroup(*[Square(side_length=0.6, color=RED, fill_opacity=0.3) for _ in range(2)]).arrange(DOWN, buff=0.1).shift(RIGHT*3)
        output_labels = VGroup(*[MathTex(f"y_{j}").move_to(output_vec[j]) for j in range(2)])
        output_group = VGroup(output_vec, output_labels)
        output_title = Text("Output", font_size=24).next_to(output_vec, UP)
        
        # Connections (sample)
        connections = VGroup()
        for i in range(3):
            for j in range(2):
                line = Line(input_vec[i].get_right(), weight_matrix[j][i].get_left(), stroke_width=0.5, color=GREY)
                connections.add(line)
        for j in range(2):
            for k in range(2):
                line = Line(weight_matrix[j][k].get_right(), output_vec[k].get_left(), stroke_width=0.5, color=GREY)
                connections.add(line)
        
        layer_diagram = VGroup(input_group, weight_group, output_group, input_title, weight_title, output_title, connections)
        self.play(LaggedStart(*[FadeIn(g, shift=RIGHT) for g in [input_group, weight_group, output_group]], lag_ratio=0.2))
        self.play(Write(input_title), Write(weight_title), Write(output_title))
        self.play(Create(connections), run_time=2)
        self.wait(1)
        
        # Forward pass equation
        forward_eq = MathTex(r"\mathbf{y} = \mathbf{W}\mathbf{x}", font_size=48).next_to(weight_matrix, DOWN, buff=0.5)
        self.play(Write(forward_eq))
        self.wait(1)
        
        # Gradient equations
        grad_eqs = VGroup(
            MathTex(r"\frac{\partial L}{\partial \mathbf{W}} = \frac{\partial L}{\partial \mathbf{y}} \mathbf{x}^T", font_size=36),
            MathTex(r"\frac{\partial L}{\partial \mathbf{x}} = \mathbf{W}^T \frac{\partial L}{\partial \mathbf{y}}", font_size=36)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=1)
        
        self.play(LaggedStart(*[Write(ge) for ge in grad_eqs], lag_ratio=0.3))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()
        
        # Scene 6: Activation Functions and Non-linearity
        title6 = Text("Activation Functions: Non-linear Gradients", font_size=45).to_edge(UP)
        self.play(Write(title6))
        
        # ReLU visualization
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 3, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": WHITE}
        ).shift(LEFT*2)
        
        relu_graph = axes.plot(lambda x: max(0, x), color=BLUE, stroke_width=4)
        relu_label = MathTex(r"\sigma(z) = \max(0, z)", font_size=36).next_to(relu_graph, UP)
        
        # Derivative
        relu_grad_graph = axes.plot(lambda x: 1 if x > 0 else 0, color=RED, stroke_width=4)
        relu_grad_label = MathTex(r"\sigma'(z) = \mathbb{1}_{z>0}", font_size=36, color=RED).next_to(relu_grad_graph, DOWN)
        
        self.play(Create(axes), Write(relu_label))
        self.play(Create(relu_graph))
        self.wait(1)
        self.play(Create(relu_grad_graph), Write(relu_grad_label))
        self.wait(1)
        
        # Chain rule with activation
        chain_with_act = MathTex(
            r"\frac{\partial L}{\partial z} = \frac{\partial L}{\partial a} \cdot \sigma'(z)",
            font_size=48
        ).shift(RIGHT*3)
        self.play(Write(chain_with_act))
        self.wait(2)
        
        # Show gradient masking
        mask_demo = VGroup(
            Text("Gradient flows only where z > 0", font_size=28, color=YELLOW),
            Text("Dead neurons: gradient = 0", font_size=24, color=RED)
        ).arrange(DOWN).to_edge(DOWN, buff=1)
        self.play(FadeIn(mask_demo))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()
        
        # Scene 7: Full Network Backpropagation
        title7 = Text("Multi-Layer Network: Complete Backprop", font_size=45).to_edge(UP)
        self.play(Write(title7))
        
        # 3-layer network
        layer_sizes = [4, 3, 2]
        layers = VGroup()
        layer_positions = [LEFT*4, ORIGIN, RIGHT*4]
        
        for i, (size, pos) in enumerate(zip(layer_sizes, layer_positions)):
            layer = VGroup(*[Circle(radius=0.3, color=BLUE, fill_opacity=0.3) for _ in range(size)]).arrange(DOWN, buff=0.3).move_to(pos)
            layers.add(layer)
            
            # Connections
            if i > 0:
                prev_layer = layers[i-1]
                connections = VGroup()
                for n1 in prev_layer:
                    for n2 in layer:
                        connections.add(Line(n1.get_right(), n2.get_left(), stroke_width=0.3, color=GREY))
                layers.add(connections)
        
        layer_labels = VGroup(
            Text("Input", font_size=20).next_to(layers[0], UP),
            Text("Hidden", font_size=20).next_to(layers[2], UP),
            Text("Output", font_size=20).next_to(layers[4], UP)
        )
        
        self.play(LaggedStart(*[FadeIn(l) for l in layers[::2]], lag_ratio=0.3))
        self.play(LaggedStart(*[Create(c) for c in layers[1::2]], lag_ratio=0.2))
        self.play(Write(layer_labels))
        self.wait(1)
        
        # Forward/Backward pass labels
        forward_arrow = Arrow(LEFT*2, RIGHT*2, color=GREEN, stroke_width=4).shift(UP*2)
        forward_label = Text("Forward Pass", font_size=24, color=GREEN).next_to(forward_arrow, UP)
        
        backward_arrow = Arrow(RIGHT*2, LEFT*2, color=RED, stroke_width=4).shift(UP*3)
        backward_label = Text("Backward Pass", font_size=24, color=RED).next_to(backward_arrow, UP)
        
        self.play(GrowArrow(forward_arrow), Write(forward_label))
        self.wait(1)
        self.play(GrowArrow(backward_arrow), Write(backward_label))
        self.wait(1)
        
        # Algorithm steps
        algo_steps = VGroup(
            Text("1. Forward pass: Compute all activations", font_size=24),
            Text("2. Compute loss gradient at output", font_size=24),
            Text("3. Backward pass: Propagate gradients layer by layer", font_size=24),
            Text("4. Compute weight gradients using chain rule", font_size=24),
            Text("5. Update weights: W ← W - η·∇W", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=0.5).shift(LEFT*2)
        
        self.play(LaggedStart(*[FadeIn(step, shift=RIGHT) for step in algo_steps], lag_ratio=0.2))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()
        
        # Scene 8: Summary and Key Insights
        title8 = Text("Backpropagation: Key Insights", font_size=50).to_edge(UP)
        self.play(Write(title8))
        
        insights = VGroup(
            Text("• Chain rule applied recursively through computational graph", font_size=32),
            Text("• Dynamic programming: reuse computations (no redundant calc)", font_size=32),
            Text("• Gradient flows backward; information flows forward", font_size=32),
            Text("• Enables training deep networks with millions of parameters", font_size=32),
            Text("• Automatic differentiation frameworks automate this process", font_size=32)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(LEFT*2)
        
        self.play(LaggedStart(*[FadeIn(insight, shift=RIGHT) for insight in insights], lag_ratio=0.2))
        self.wait(2)
        
        # Final equation summary
        final_eq = MathTex(
            r"\nabla_{\theta} L = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial \theta}",
            font_size=60
        ).to_edge(DOWN, buff=1)
        self.play(Write(final_eq))
        self.wait(3)
        
        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)
