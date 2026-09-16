from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Introduction - Forward Pass with Simple Network
        self.scene1_forward_pass()
        self.clear()
        
        # Scene 2: The Loss Function - Measuring Error
        self.scene2_loss_function()
        self.clear()
        
        # Scene 3: The Chain Rule - Foundation of Backpropagation
        self.scene3_chain_rule()
        self.clear()
        
        # Scene 4: Computing Gradients for Output Layer
        self.scene4_output_gradients()
        self.clear()
        
        # Scene 5: Backpropagating to Hidden Layer
        self.scene5_hidden_gradients()
        self.clear()
        
        # Scene 6: Weight Update with Gradient Descent
        self.scene6_weight_update()
        self.clear()
        
        # Scene 7: Full Backpropagation Cycle
        self.scene7_full_cycle()
        self.clear()
        
        # Scene 8: Summary and Key Insights
        self.scene8_summary()

    def scene1_forward_pass(self):
        # Title
        title = Text("Neural Network: Forward Pass", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create input layer
        input_nodes = VGroup(*[Circle(radius=0.3, color=GREEN, fill_opacity=0.3) for _ in range(2)])
        input_nodes.arrange(DOWN, buff=0.8)
        input_labels = VGroup(*[MathTex(f"x_{i+1}", font_size=24) for i in range(2)])
        for node, label in zip(input_nodes, input_labels):
            label.move_to(node)
        input_group = VGroup(input_nodes, input_labels)
        input_group.shift(LEFT * 4.5)

        # Create hidden layer
        hidden_nodes = VGroup(*[Circle(radius=0.3, color=YELLOW, fill_opacity=0.3) for _ in range(3)])
        hidden_nodes.arrange(DOWN, buff=0.6)
        hidden_labels = VGroup(*[MathTex(f"h_{i+1}", font_size=24) for i in range(3)])
        for node, label in zip(hidden_nodes, hidden_labels):
            label.move_to(node)
        hidden_group = VGroup(hidden_nodes, hidden_labels)
        hidden_group.shift(LEFT * 1.5)

        # Create output layer
        output_node = Circle(radius=0.3, color=RED, fill_opacity=0.3)
        output_label = MathTex("\\hat{y}", font_size=24).move_to(output_node)
        output_group = VGroup(output_node, output_label)
        output_group.shift(RIGHT * 1.5)

        # Create target
        target = MathTex("y", font_size=28, color=ORANGE)
        target.next_to(output_group, RIGHT, buff=1.5)

        # Draw layers
        self.play(Create(input_nodes), Create(hidden_nodes), Create(output_node))
        self.play(Write(input_labels), Write(hidden_labels), Write(output_label))
        self.wait(0.3)

        # Draw connections with weights
        connections_ih = VGroup()
        weight_labels_ih = VGroup()
        for i, inp in enumerate(input_nodes):
            for j, hid in enumerate(hidden_nodes):
                line = Line(inp.get_right(), hid.get_left(), color=GRAY, stroke_width=1.5)
                connections_ih.add(line)
                w = MathTex(f"w_{{{i+1},{j+1}}}^{{(1)}}", font_size=16, color=BLUE_B)
                w.move_to(line.get_center() + UP * 0.15 + RIGHT * 0.1)
                weight_labels_ih.add(w)

        connections_ho = VGroup()
        weight_labels_ho = VGroup()
        for j, hid in enumerate(hidden_nodes):
            line = Line(hid.get_right(), output_node.get_left(), color=GRAY, stroke_width=1.5)
            connections_ho.add(line)
            w = MathTex(f"w_{{{j+1}}}^{{(2)}}", font_size=16, color=BLUE_B)
            w.move_to(line.get_center() + UP * 0.15)
            weight_labels_ho.add(w)

        self.play(Create(connections_ih), Create(connections_ho))
        self.play(Write(weight_labels_ih), Write(weight_labels_ho))
        self.wait(0.3)

        # Animate forward pass: input -> hidden
        dots_ih = VGroup()
        for i, inp in enumerate(input_nodes):
            for j, hid in enumerate(hidden_nodes):
                dot = Dot(color=GREEN, radius=0.08)
                dot.move_to(inp.get_center())
                dots_ih.add(dot)

        self.play(FadeIn(dots_ih))
        self.play(
            *[dot.animate.move_to(hidden_nodes[j % 3].get_center()) for j, dot in enumerate(dots_ih)],
            run_time=2
        )

        # Show activation at hidden layer
        activation_h = MathTex("h_j = \\sigma\\left(\\sum_i w_{ij}^{(1)} x_i\\right)", font_size=28, color=YELLOW)
        activation_h.to_edge(DOWN)
        self.play(Write(activation_h))
        self.wait(0.3)

        # Hidden -> output
        dots_ho = VGroup(*[Dot(color=YELLOW, radius=0.08) for _ in range(3)])
        for dot, hid in zip(dots_ho, hidden_nodes):
            dot.move_to(hid.get_center())

        self.play(FadeIn(dots_ho))
        self.play(
            *[dot.animate.move_to(output_node.get_center()) for dot in dots_ho],
            run_time=2
        )

        # Show output computation
        activation_o = MathTex("\\hat{y} = \\sigma\\left(\\sum_j w_j^{(2)} h_j\\right)", font_size=28, color=RED)
        activation_o.next_to(activation_h, UP, buff=0.3)
        self.play(Write(activation_o))

        # Show target
        self.play(Write(target))
        self.wait(0.5)

        # Fade out dots
        self.play(FadeOut(dots_ih), FadeOut(dots_ho))
        self.wait(0.5)

        # Store for next scene
        self.network_elements = VGroup(
            input_group, hidden_group, output_group,
            connections_ih, connections_ho,
            weight_labels_ih, weight_labels_ho,
            target, activation_h, activation_o, title
        )

    def scene2_loss_function(self):
        # Title
        title = Text("Step 2: The Loss Function", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # Create prediction and target
        y_hat = MathTex("\\hat{y} = 0.7", font_size=32, color=RED)
        y = MathTex("y = 1.0", font_size=32, color=GREEN)
        y_hat.shift(LEFT * 2 + UP * 1)
        y.shift(RIGHT * 2 + UP * 1)

        self.play(Write(y_hat), Write(y))
        self.wait(0.3)

        # Show error visually
        arrow = DoubleArrow(y_hat.get_right(), y.get_left(), color=YELLOW, buff=0.3)
        error_label = MathTex("\\text{Error}", font_size=24, color=YELLOW)
        error_label.next_to(arrow, UP, buff=0.1)

        self.play(Create(arrow), Write(error_label))
        self.wait(0.3)

        # Introduce MSE loss
        mse_formula = MathTex("L = \\frac{1}{2}(y - \\hat{y})^2", font_size=36, color=WHITE)
        mse_formula.shift(DOWN * 0.5)

        self.play(Write(mse_formula))
        self.wait(0.3)

        # Compute numerical example
        computation = MathTex("= \\frac{1}{2}(1.0 - 0.7)^2 = \\frac{1}{2}(0.3)^2 = 0.045", font_size=32, color=WHITE)
        computation.next_to(mse_formula, DOWN, buff=0.4)

        self.play(Write(computation))
        self.wait(0.3)

        # Highlight that we want to minimize this
        minimize = Text("Goal: Minimize Loss", font_size=28, color=GREEN)
        minimize.to_edge(DOWN)

        self.play(Write(minimize))
        self.wait(0.3)

        # Show gradient direction
        gradient_arrow = Arrow(UP * 2, DOWN * 2, color=RED)
        gradient_arrow.shift(RIGHT * 4)
        gradient_label = MathTex("\\nabla L", font_size=28, color=RED)
        gradient_label.next_to(gradient_arrow, RIGHT)

        self.play(Create(gradient_arrow), Write(gradient_label))
        self.wait(0.5)

        # Transform to show we need to go backward
        backward_text = Text("How does L change with respect to each weight?", font_size=24, color=YELLOW)
        backward_text.to_edge(DOWN)
        backward_text.shift(UP * 0.5)

        self.play(Transform(minimize, backward_text))
        self.wait(0.5)

        self.all_scene2 = VGroup(title, y_hat, y, arrow, error_label, mse_formula, computation, minimize, gradient_arrow, gradient_label)

    def scene3_chain_rule(self):
        # Title
        title = Text("Step 3: The Chain Rule", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # Simple chain rule example
        example = MathTex("z = f(y), \\quad y = g(x)", font_size=32, color=WHITE)
        example.shift(UP * 2)

        self.play(Write(example))
        self.wait(0.3)

        # The chain rule formula
        chain_rule = MathTex("\\frac{dz}{dx} = \\frac{dz}{dy} \\cdot \\frac{dy}{dx}", font_size=40, color=YELLOW)
        chain_rule.shift(UP * 0.5)

        self.play(Write(chain_rule))
        self.wait(0.3)

        # Visual representation: chain of dependencies
        boxes = VGroup()
        labels = VGroup()
        box_colors = [GREEN, BLUE, RED]
        box_labels = ["x", "y", "z"]
        
        for i, (color, label) in enumerate(zip(box_colors, box_labels)):
            box = Rectangle(height=0.8, width=1.2, color=color, fill_opacity=0.3)
            box.shift(LEFT * 2 + i * RIGHT * 2)
            boxes.add(box)
            lab = MathTex(label, font_size=28, color=color)
            lab.move_to(box)
            labels.add(lab)

        self.play(Create(boxes), Write(labels))
        self.wait(0.3)

        # Arrows showing dependencies
        arrows = VGroup()
        for i in range(2):
            arrow = Arrow(boxes[i].get_right(), boxes[i+1].get_left(), color=WHITE, buff=0.2)
            arrows.add(arrow)

        self.play(Create(arrows))
        self.wait(0.3)

        # Show gradients flowing backward
        grad_arrows = VGroup()
        grad_labels = VGroup()
        for i in range(2):
            arrow = Arrow(boxes[i+1].get_bottom(), boxes[i].get_bottom(), color=YELLOW, buff=0.2)
            arrow.shift(DOWN * 0.6)
            grad_arrows.add(arrow)
            if i == 0:
                label = MathTex("\\frac{\\partial z}{\\partial y}", font_size=20, color=YELLOW)
            else:
                label = MathTex("\\frac{\\partial z}{\\partial x}", font_size=20, color=YELLOW)
            label.next_to(arrow, DOWN, buff=0.1)
            grad_labels.add(label)

        self.play(Create(grad_arrows), Write(grad_labels))
        self.wait(0.3)

        # Highlight the multiplication
        multiply = MathTex("\\frac{\\partial z}{\\partial x} = \\frac{\\partial z}{\\partial y} \\cdot \\frac{\\partial y}{\\partial x}", font_size=32, color=GREEN)
        multiply.shift(DOWN * 2)

        self.play(Write(multiply))
        self.wait(0.3)

        # Connect to neural networks
        nn_text = Text("In neural networks: L depends on weights through many intermediate layers", font_size=22, color=ORANGE)
        nn_text.to_edge(DOWN)

        self.play(Write(nn_text))
        self.wait(0.5)

        self.all_scene3 = VGroup(title, example, chain_rule, boxes, labels, arrows, grad_arrows, grad_labels, multiply, nn_text)

    def scene4_output_gradients(self):
        # Title
        title = Text("Step 4: Output Layer Gradients", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # Simple network: one hidden to output
        h = Circle(radius=0.4, color=YELLOW, fill_opacity=0.3)
        h.shift(LEFT * 2)
        h_label = MathTex("h", font_size=28).move_to(h)

        w = MathTex("w", font_size=24, color=BLUE)
        w.next_to(h, RIGHT, buff=0.5)

        z = Circle(radius=0.4, color=GREEN, fill_opacity=0.3)
        z.shift(RIGHT * 1)
        z_label = MathTex("z", font_size=28).move_to(z)

        sigma = MathTex("\\sigma", font_size=24, color=ORANGE)
        sigma.next_to(z, RIGHT, buff=0.5)

        y_hat = Circle(radius=0.4, color=RED, fill_opacity=0.3)
        y_hat.shift(RIGHT * 3)
        y_hat_label = MathTex("\\hat{y}", font_size=28).move_to(y_hat)

        y = MathTex("y", font_size=28, color=GREEN)
        y.next_to(y_hat, RIGHT, buff=0.8)

        # Arrows
        arrow_hw = Arrow(h.get_right(), z.get_left(), color=GRAY)
        arrow_zs = Arrow(z.get_right(), y_hat.get_left(), color=GRAY)
        arrow_y = Arrow(y_hat.get_right(), y.get_left(), color=GRAY)

        self.play(Create(h), Create(z), Create(y_hat))
        self.play(Write(h_label), Write(z_label), Write(y_hat_label), Write(y))
        self.play(Create(arrow_hw), Create(arrow_zs), Create(arrow_y))
        self.play(Write(w), Write(sigma))
        self.wait(0.3)

        # Show the computation path
        path = VGroup(h, h_label, arrow_hw, w, z, z_label, arrow_zs, sigma, y_hat, y_hat_label, arrow_y, y)

        # Loss function
        loss = MathTex("L = \\frac{1}{2}(y - \\hat{y})^2", font_size=32, color=WHITE)
        loss.shift(DOWN * 1.5)

        self.play(Write(loss))
        self.wait(0.3)

        # Compute dL/dy_hat
        dL_dyhat = MathTex("\\frac{\\partial L}{\\partial \\hat{y}} = -(y - \\hat{y}) = \\hat{y} - y", font_size=30, color=YELLOW)
        dL_dyhat.shift(DOWN * 2.5)

        self.play(Write(dL_dyhat))
        self.wait(0.3)

        # Highlight this is the "error signal"
        error_signal = MathTex("\\delta^{(output)} = \\hat{y} - y", font_size=28, color=RED)
        error_signal.to_edge(DOWN)

        self.play(Write(error_signal))
        self.wait(0.3)

        # Now show dL/dw
        self.play(FadeOut(dL_dyhat), FadeOut(error_signal))
        
        chain = MathTex("\\frac{\\partial L}{\\partial w} = \\frac{\\partial L}{\\partial \\hat{y}} \\cdot \\frac{\\partial \\hat{y}}{\\partial z} \\cdot \\frac{\\partial z}{\\partial w}", font_size=28, color=YELLOW)
        chain.shift(DOWN * 2)

        self.play(Write(chain))
        self.wait(0.3)

        # Expand each term
        term1 = MathTex("\\frac{\\partial L}{\\partial \\hat{y}} = \\hat{y} - y", font_size=22, color=GREEN)
        term2 = MathTex("\\frac{\\partial \\hat{y}}{\\partial z} = \\sigma'(z)", font_size=22, color=BLUE)
        term3 = MathTex("\\frac{\\partial z}{\\partial w} = h", font_size=22, color=RED)

        terms = VGroup(term1, term2, term3)
        terms.arrange(RIGHT, buff=0.5)
        terms.shift(DOWN * 3)

        self.play(Write(terms))
        self.wait(0.3)

        # Final combined gradient
        final = MathTex("\\frac{\\partial L}{\\partial w} = (\\hat{y} - y) \\cdot \\sigma'(z) \\cdot h", font_size=28, color=GREEN)
        final.to_edge(DOWN)

        self.play(Write(final))
        self.wait(0.5)

        self.all_scene4 = VGroup(title, path, w, sigma, loss, chain, terms, final)

    def scene5_hidden_gradients(self):
        # Title
        title = Text("Step 5: Hidden Layer Gradients", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # Two-layer network for visualization
        x = Circle(radius=0.35, color=GREEN, fill_opacity=0.3)
        x.shift(LEFT * 4)
        x_label = MathTex("x", font_size=24).move_to(x)

        h = Circle(radius=0.35, color=YELLOW, fill_opacity=0.3)
        h.shift(LEFT * 1.5)
        h_label = MathTex("h", font_size=24).move_to(h)

        y_hat = Circle(radius=0.35, color=RED, fill_opacity=0.3)
        y_hat.shift(RIGHT * 1.5)
        y_hat_label = MathTex("\\hat{y}", font_size=24).move_to(y_hat)

        y = MathTex("y", font_size=24, color=GREEN)
        y.shift(RIGHT * 3.5)

        # Weights
        w1 = MathTex("w^{(1)}", font_size=20, color=BLUE)
        w1.move_to(LEFT * 2.75 + UP * 0.3)
        w2 = MathTex("w^{(2)}", font_size=20, color=BLUE)
        w2.move_to(RIGHT * 0 + UP * 0.3)

        arrows = VGroup(
            Arrow(x.get_right(), h.get_left(), color=GRAY),
            Arrow(h.get_right(), y_hat.get_left(), color=GRAY),
            Arrow(y_hat.get_right(), y.get_left(), color=GRAY)
        )

        self.play(Create(x), Create(h), Create(y_hat))
        self.play(Write(x_label), Write(h_label), Write(y_hat_label), Write(y))
        self.play(Create(arrows))
        self.play(Write(w1), Write(w2))
        self.wait(0.3)

        # Show that gradient at h depends on downstream gradient
        downstream = MathTex("\\frac{\\partial L}{\\partial h} = \\frac{\\partial L}{\\partial \\hat{y}} \\cdot \\frac{\\partial \\hat{y}}{\\partial h}", font_size=28, color=YELLOW)
        downstream.shift(DOWN * 1.5)

        self.play(Write(downstream))
        self.wait(0.3)

        # But we already computed dL/dy_hat! This is the "backward" flow
        known = MathTex("\\text{We know } \\frac{\\partial L}{\\partial \\hat{y}} \\text{ from previous step!}", font_size=24, color=GREEN)
        known.next_to(downstream, DOWN, buff=0.3)

        self.play(Write(known))
        self.wait(0.3)

        # Show backward arrows
        back_arrow1 = Arrow(y_hat.get_bottom(), h.get_bottom(), color=RED, buff=0.2)
        back_arrow1.shift(DOWN * 0.5)
        back_arrow2 = Arrow(h.get_bottom(), x.get_bottom(), color=RED, buff=0.2)
        back_arrow2.shift(DOWN * 0.5)

        back_label1 = MathTex("\\delta^{(2)}", font_size=20, color=RED)
        back_label1.next_to(back_arrow1, DOWN, buff=0.1)
        back_label2 = MathTex("\\delta^{(1)}", font_size=20, color=RED)
        back_label2.next_to(back_arrow2, DOWN, buff=0.1)

        self.play(Create(back_arrow1), Create(back_arrow2))
        self.play(Write(back_label1), Write(back_label2))
        self.wait(0.3)

        # General formula for hidden layer
        general = MathTex("\\delta^{(l)} = \\left((w^{(l+1)})^T \\delta^{(l+1)}\\right) \\odot \\sigma'(z^{(l)})", font_size=26, color=ORANGE)
        general.shift(DOWN * 3)

        self.play(Write(general))
        self.wait(0.3)

        # Key insight: reuse of downstream gradients
        insight = Text("Key: Reuse computed gradients from later layers!", font_size=22, color=GREEN)
        insight.to_edge(DOWN)

        self.play(Write(insight))
        self.wait(0.5)

        self.all_scene5 = VGroup(title, x, x_label, h, h_label, y_hat, y_hat_label, y, w1, w2, arrows, downstream, known, back_arrow1, back_arrow2, back_label1, back_label2, general, insight)

    def scene6_weight_update(self):
        # Title
        title = Text("Step 6: Gradient Descent Update", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # Show weight as a point on a loss landscape
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": False, "numbers_to_exclude": []}
        )
        axes.shift(DOWN * 0.5)

        x_label = MathTex("w", font_size=24)
        x_label.next_to(axes.x_axis, RIGHT)
        y_label = MathTex("L(w)", font_size=24)
        y_label.next_to(axes.y_axis, UP)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.3)

        # Parabolic loss curve
        curve = axes.plot(lambda x: x**2, color=BLUE, x_range=[-2.2, 2.2])
        self.play(Create(curve))
        self.wait(0.3)

        # Current weight position
        w_current = Dot(axes.c2p(1.5, 2.25), color=RED, radius=0.1)
        w_label = MathTex("w_{old}", font_size=20, color=RED)
        w_label.next_to(w_current, UR, buff=0.1)

        self.play(FadeIn(w_current), Write(w_label))
        self.wait(0.3)

        # Show gradient (slope) at this point
        tangent = Line(
            axes.c2p(0.5, 0.25),
            axes.c2p(2.5, 6.25),
            color=YELLOW
        )
        # Clip tangent to visible region
        tangent = axes.plot(lambda x: 3*x - 2.25, color=YELLOW, x_range=[0.8, 2.2])

        grad_label = MathTex("\\frac{\\partial L}{\\partial w} > 0", font_size=20, color=YELLOW)
        grad_label.next_to(w_current, RIGHT, buff=0.3)

        self.play(Create(tangent), Write(grad_label))
        self.wait(0.3)

        # Gradient descent step
        w_new = Dot(axes.c2p(0.9, 0.81), color=GREEN, radius=0.1)
        w_new_label = MathTex("w_{new}", font_size=20, color=GREEN)
        w_new_label.next_to(w_new, UL, buff=0.1)

        # Arrow showing update direction
        update_arrow = Arrow(w_current.get_center(), w_new.get_center(), color=GREEN, buff=0.1)

        self.play(Create(update_arrow))
        self.play(FadeIn(w_new), Write(w_new_label))
        self.wait(0.3)

        # Update rule formula
        update_rule = MathTex("w_{new} = w_{old} - \\eta \\frac{\\partial L}{\\partial w}", font_size=32, color=WHITE)
        update_rule.shift(DOWN * 2.8)

        self.play(Write(update_rule))
        self.wait(0.3)

        # Learning rate explanation
        eta_text = MathTex("\\eta = \\text{learning rate}", font_size=24, color=ORANGE)
        eta_text.next_to(update_rule, DOWN, buff=0.2)

        self.play(Write(eta_text))
        self.wait(0.3)

        # Show negative gradient direction
        neg_grad = MathTex("-\\nabla L \\text{ points toward lower loss}", font_size=22, color=GREEN)
        neg_grad.to_edge(DOWN)

        self.play(Write(neg_grad))
        self.wait(0.5)

        self.all_scene6 = VGroup(title, axes, x_label, y_label, curve, w_current, w_label, tangent, grad_label, update_arrow, w_new, w_new_label, update_rule, eta_text, neg_grad)

    def scene7_full_cycle(self):
        # Title
        title = Text("Step 7: Complete Backpropagation Cycle", font_size=34, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # Create a small network: 2-2-1
        layer1 = VGroup(*[Circle(radius=0.25, color=GREEN, fill_opacity=0.3) for _ in range(2)])
        layer1.arrange(DOWN, buff=0.6)
        layer1.shift(LEFT * 3)

        layer2 = VGroup(*[Circle(radius=0.25, color=YELLOW, fill_opacity=0.3) for _ in range(2)])
        layer2.arrange(DOWN, buff=0.6)
        layer2.shift(LEFT * 0.5)

        layer3 = Circle(radius=0.25, color=RED, fill_opacity=0.3)
        layer3.shift(RIGHT * 2)

        # Labels
        l1_labels = VGroup(*[MathTex(f"x_{i+1}", font_size=18) for i in range(2)])
        for node, label in zip(layer1, l1_labels):
            label.move_to(node)

        l2_labels = VGroup(*[MathTex(f"h_{i+1}", font_size=18) for i in range(2)])
        for node, label in zip(layer2, l2_labels):
            label.move_to(node)

        l3_label = MathTex("\\hat{y}", font_size=18).move_to(layer3)

        # Connections
        conn12 = VGroup()
        for n1 in layer1:
            for n2 in layer2:
                conn12.add(Line(n1.get_right(), n2.get_left(), color=GRAY, stroke_width=1))

        conn23 = VGroup()
        for n2 in layer2:
            conn23.add(Line(n2.get_right(), layer3.get_left(), color=GRAY, stroke_width=1))

        network = VGroup(layer1, layer2, layer3, l1_labels, l2_labels, l3_label, conn12, conn23)
        network.scale(0.9)
        network.shift(UP * 0.5)

        self.play(Create(network))
        self.wait(0.3)

        # Step labels
        step1 = Text("1. Forward Pass", font_size=20, color=GREEN)
        step2 = Text("2. Compute Loss", font_size=20, color=RED)
        step3 = Text("3. Backward Pass", font_size=20, color=YELLOW)
        step4 = Text("4. Update Weights", font_size=20, color=BLUE)

        steps = VGroup(step1, step2, step3, step4)
        steps.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        steps.to_edge(RIGHT)
        steps.shift(LEFT * 0.5)

        # Animate forward pass
        self.play(Write(step1))
        forward_dots = VGroup()
        for n1 in layer1:
            for n2 in layer2:
                dot = Dot(color=GREEN, radius=0.05)
                dot.move_to(n1.get_center())
                forward_dots.add(dot)

        self.play(FadeIn(forward_dots))
        self.play(*[dot.animate.move_to(layer2[i % 2].get_center()) for i, dot in enumerate(forward_dots)], run_time=1.5)

        forward_dots2 = VGroup(*[Dot(color=YELLOW, radius=0.05).move_to(n.get_center()) for n in layer2])
        self.play(FadeIn(forward_dots2))
        self.play(*[dot.animate.move_to(layer3.get_center()) for dot in forward_dots2], run_time=1.5)
        self.wait(0.3)

        # Loss computation
        self.play(Write(step2))
        loss_circle = Circle(radius=0.2, color=RED, fill_opacity=0.5).move_to(layer3.get_center() + RIGHT * 0.8)
        loss_label = MathTex("L", font_size=16, color=RED).move_to(loss_circle)
        self.play(FadeIn(loss_circle), Write(loss_label))
        self.wait(0.3)

        # Backward pass - gradients flow back
        self.play(Write(step3))
        self.play(FadeOut(forward_dots), FadeOut(forward_dots2))

        # Gradient flow visualization
        grad_dots1 = VGroup(*[Dot(color=YELLOW, radius=0.06).move_to(layer3.get_center()) for _ in range(2)])
        self.play(FadeIn(grad_dots1))
        self.play(*[dot.animate.move_to(layer2[i].get_center()) for i, dot in enumerate(grad_dots1)], run_time=1.5)

        grad_dots2 = VGroup()
        for i, n2 in enumerate(layer2):
            for j, n1 in enumerate(layer1):
                dot = Dot(color=YELLOW, radius=0.06)
                dot.move_to(n2.get_center())
                grad_dots2.add(dot)

        self.play(FadeIn(grad_dots2))
        self.play(*[dot.animate.move_to(layer1[i % 2].get_center()) for i, dot in enumerate(grad_dots2)], run_time=1.5)
        self.wait(0.3)

        # Weight update
        self.play(Write(step4))
        
        # Flash weights to show update
        weight_flashes = VGroup()
        for conn in list(conn12) + list(conn23):
            flash = conn.copy().set_color(BLUE).set_stroke(width=3)
            weight_flashes.add(flash)

        self.play(*[Create(flash) for flash in weight_flashes], run_time=0.5)
        self.play(*[FadeOut(flash) for flash in weight_flashes], run_time=0.5)

        # Iteration counter
        iter_text = MathTex("\\text{Repeat for many iterations...}", font_size=22, color=WHITE)
        iter_text.to_edge(DOWN)

        self.play(Write(iter_text))
        self.wait(0.5)

        # Fade out gradient dots
        self.play(FadeOut(grad_dots1), FadeOut(grad_dots2))
        self.wait(0.3)

        self.all_scene7 = VGroup(title, network, steps, loss_circle, loss_label, iter_text)

    def scene8_summary(self):
        # Title
        title = Text("Backpropagation: Key Insights", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # Key points
        points = VGroup(
            Text("1. Forward pass: compute predictions", font_size=24, color=GREEN),
            Text("2. Compute loss: measure error", font_size=24, color=RED),
            Text("3. Backward pass: apply chain rule", font_size=24, color=YELLOW),
            Text("4. Reuse gradients from later layers", font_size=24, color=ORANGE),
            Text("5. Update weights: gradient descent", font_size=24, color=BLUE),
            Text("6. Repeat until convergence", font_size=24, color=PURPLE)
        )
        points.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        points.shift(UP * 0.5)

        for i, point in enumerate(points):
            self.play(Write(point), run_time=0.8)
            self.wait(0.2)

        # Chain rule visualization summary
        chain_visual = MathTex("\\frac{\\partial L}{\\partial w^{(l)}} = \\underbrace{\\delta^{(l+1)}}_{\\text{from later layer}} \\cdot \\underbrace{\\frac{\\partial z^{(l+1)}}{\\partial w^{(l)}}}_{\\text{local gradient}}", font_size=26, color=WHITE)
        chain_visual.to_edge(DOWN)
        chain_visual.shift(UP * 0.5)

        self.play(Write(chain_visual))
        self.wait(0.3)

        # Efficiency highlight
        efficiency = Text("Efficient: O(n) for n connections (not exponential!)", font_size=22, color=GREEN)
        efficiency.next_to(chain_visual, DOWN, buff=0.3)

        self.play(Write(efficiency))
        self.wait(0.5)

        # Final emphasis
        final = Text("Backpropagation = Chain Rule + Dynamic Programming", font_size=26, color=YELLOW)
        final.to_edge(DOWN)

        self.play(Write(final))
        self.wait(1)

        self.all_scene8 = VGroup(title, points, chain_visual, efficiency, final)
