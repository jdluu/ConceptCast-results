from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Introduction - Forward Pass Intuition
        self.scene1_forward_pass()
        self.clear()
        
        # Scene 2: The Problem - Need for Learning
        self.scene2_learning_problem()
        self.clear()
        
        # Scene 3: Chain Rule Foundations
        self.scene3_chain_rule()
        self.clear()
        
        # Scene 4: One Neuron - Local Gradient
        self.scene4_local_gradient()
        self.clear()
        
        # Scene 5: Backprop Through One Layer
        self.scene5_one_layer_backprop()
        self.clear()
        
        # Scene 6: Multi-Layer Network Structure
        self.scene6_multilayer_structure()
        self.clear()
        
        # Scene 7: Full Backpropagation Algorithm
        self.scene7_full_algorithm()
        self.clear()
        
        # Scene 8: Weight Update and Summary
        self.scene8_weight_update_summary()
    
    def scene1_forward_pass(self):
        # Title
        title = Text("Neural Networks: Forward Pass", font_size=36)
        title.to_edge(UP)
        
        # Input layer
        input_nodes = VGroup(*[Dot(color=BLUE).scale(1.5) for _ in range(3)])
        input_nodes.arrange(DOWN, buff=1)
        input_nodes.shift(LEFT * 4)
        
        input_labels = VGroup(*[MathTex(f"x_{i+1}", color=BLUE) for i in range(3)])
        for label, node in zip(input_labels, input_nodes):
            label.next_to(node, LEFT)
        
        # Hidden layer
        hidden_nodes = VGroup(*[Dot(color=GREEN).scale(1.5) for _ in range(4)])
        hidden_nodes.arrange(DOWN, buff=0.8)
        hidden_nodes.shift(LEFT * 0.5)
        
        # Output layer
        output_nodes = VGroup(*[Dot(color=RED).scale(1.5) for _ in range(2)])
        output_nodes.arrange(DOWN, buff=1.2)
        output_nodes.shift(RIGHT * 3)
        
        output_labels = VGroup(*[MathTex(f"\\hat{{y}}_{i+1}", color=RED) for i in range(2)])
        for label, node in zip(output_labels, output_nodes):
            label.next_to(node, RIGHT)
        
        # Input-to-hidden connections
        ih_edges = VGroup()
        for i_node in input_nodes:
            for h_node in hidden_nodes:
                edge = Line(i_node.get_right(), h_node.get_left(), color=GRAY, stroke_width=2)
                ih_edges.add(edge)
        
        # Hidden-to-output connections
        ho_edges = VGroup()
        for h_node in hidden_nodes:
            for o_node in output_nodes:
                edge = Line(h_node.get_right(), o_node.get_left(), color=GRAY, stroke_width=2)
                ho_edges.add(edge)
        
        # Weight labels (sample)
        w1 = MathTex("w_1", color=YELLOW).scale(0.7)
        w1.move_to(Line(input_nodes[0].get_right(), hidden_nodes[0].get_left()).get_center() + UP * 0.2)
        
        # Build the network
        self.play(Write(title), run_time=1)
        self.play(FadeIn(input_nodes, input_labels), run_time=1)
        self.play(Create(ih_edges), FadeIn(w1), run_time=1.5)
        self.play(FadeIn(hidden_nodes), run_time=1)
        self.play(Create(ho_edges), run_time=1.5)
        self.play(FadeIn(output_nodes, output_labels), run_time=1)
        
        # Animate forward pass with data flow
        forward_arrows = VGroup()
        for edge in ih_edges[:4]:  # sample subset
            arrow = Arrow(edge.get_start(), edge.get_end(), color=YELLOW, buff=0.1, stroke_width=3)
            forward_arrows.add(arrow)
        
        self.play(LaggedStart(*[Create(a) for a in forward_arrows], lag_ratio=0.3), run_time=2)
        self.play(forward_arrows.animate.set_opacity(0.3), run_time=0.5)
        
        # Activation function indicator
        activation = MathTex("\\sigma(\\sum w_i x_i + b)", color=GREEN)
        activation.next_to(hidden_nodes, UP, buff=0.5)
        self.play(Write(activation), run_time=1)
        
        # Output computation
        output_compute = MathTex("\\hat{y} = \\sigma(W^{[2]} \\cdot a^{[1]} + b^{[2]})", color=RED)
        output_compute.next_to(output_nodes, UP, buff=0.8)
        self.play(Write(output_compute), run_time=1)
        
        self.wait(1.5)
        
        # Fade out forward-specific elements
        self.play(FadeOut(forward_arrows, activation, output_compute, w1, output_compute), run_time=0.5)
        
        # Keep network structure for next scene
        self.network_base = VGroup(title, input_nodes, input_labels, hidden_nodes, 
                                   output_nodes, output_labels, ih_edges, ho_edges)
    
    def scene2_learning_problem(self):
        # Rebuild network without full recreation
        title = Text("The Learning Problem", font_size=36)
        title.to_edge(UP)
        
        # Simpler network for clarity
        x = MathTex("x", color=BLUE).scale(1.5).shift(LEFT * 4)
        y_true = MathTex("y_{\\text{true}}", color=GREEN).scale(1.2).shift(RIGHT * 4 + UP * 2)
        y_pred = MathTex("\\hat{y}", color=RED).scale(1.2).shift(RIGHT * 4 + DOWN * 2)
        
        # Network in middle
        neuron = Circle(radius=0.5, color=YELLOW, fill_opacity=0.2).shift(LEFT * 0.5)
        sigma = MathTex("\\sigma").scale(0.8).move_to(neuron)
        
        # Connections
        in_edge = Arrow(x.get_right(), neuron.get_left(), color=GRAY, buff=0.1)
        out_edge = Arrow(neuron.get_right(), y_pred.get_left(), color=GRAY, buff=0.1)
        
        w_label = MathTex("w, b", color=YELLOW).next_to(in_edge, UP, buff=0.1)
        
        # Target vs Prediction visualization
        target_box = Square(side_length=1, color=GREEN, fill_opacity=0.3).move_to(y_true.get_center())
        pred_box = Square(side_length=0.7, color=RED, fill_opacity=0.3).move_to(y_pred.get_center())
        
        # Loss function
        loss_eq = MathTex("L = \\frac{1}{2}(y_{\\text{true}} - \\hat{y})^2", color=WHITE)
        loss_eq.shift(DOWN * 2.5)
        
        # Build scene
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(x), run_time=0.5)
        self.play(Create(in_edge), Write(w_label), FadeIn(neuron, sigma), run_time=1)
        self.play(Create(out_edge), FadeIn(y_pred, pred_box), run_time=0.8)
        self.play(FadeIn(y_true, target_box), run_time=0.8)
        
        # Show gap between target and prediction
        gap_arrow = DoubleArrow(target_box.get_bottom(), pred_box.get_top(), color=ORANGE, buff=0.1)
        gap_label = Text("Error!", color=ORANGE, font_size=24)
        gap_label.next_to(gap_arrow, RIGHT)
        
        self.play(Create(gap_arrow), Write(gap_label), run_time=1)
        
        # Introduce loss
        self.play(Write(loss_eq), run_time=1)
        
        # Highlight that we need to adjust w, b
        question = Text("How to adjust w, b to reduce L?", color=YELLOW, font_size=28)
        question.next_to(loss_eq, DOWN, buff=0.5)
        
        self.play(Write(question), run_time=1)
        
        # Need gradient
        gradient_text = MathTex("\\frac{\\partial L}{\\partial w} = ?", color=YELLOW)
        gradient_text.next_to(question, RIGHT, buff=0.5)
        self.play(Write(gradient_text), run_time=1)
        
        self.wait(1.5)
        
        # Transition: need chain rule
        self.play(FadeOut(gap_arrow, gap_label, question, gradient_text), run_time=0.5)
        
        self.key_elements = VGroup(title, x, y_true, y_pred, neuron, sigma, in_edge, out_edge,
                                   w_label, target_box, pred_box, loss_eq)
    
    def scene3_chain_rule(self):
        # Chain rule from calculus - the mathematical foundation
        title = Text("The Chain Rule", font_size=36, color=BLUE)
        title.to_edge(UP)
        
        # Basic chain rule
        chain_basic = MathTex("\\frac{dz}{dx} = \\frac{dz}{dy} \\cdot \\frac{dy}{dx}", color=WHITE)
        chain_basic.scale(1.5)
        
        # Visual decomposition
        x_box = RoundedRectangle(corner_radius=0.2, width=1.5, height=1, color=BLUE, fill_opacity=0.2)
        x_box.shift(LEFT * 4)
        x_label = MathTex("x").move_to(x_box)
        
        y_box = RoundedRectangle(corner_radius=0.2, width=1.5, height=1, color=GREEN, fill_opacity=0.2)
        y_box.shift(ORIGIN)
        y_label = MathTex("y").move_to(y_box)
        
        z_box = RoundedRectangle(corner_radius=0.2, width=1.5, height=1, color=RED, fill_opacity=0.2)
        z_box.shift(RIGHT * 4)
        z_label = MathTex("z").move_to(z_box)
        
        # Functions
        f_arrow = Arrow(x_box.get_right(), y_box.get_left(), color=YELLOW, buff=0.2)
        f_label = MathTex("y = f(x)", color=YELLOW).next_to(f_arrow, UP, buff=0.1)
        
        g_arrow = Arrow(y_box.get_right(), z_box.get_left(), color=ORANGE, buff=0.2)
        g_label = MathTex("z = g(y)", color=ORANGE).next_to(g_arrow, UP, buff=0.1)
        
        # Gradients on arrows
        dy_dx = MathTex("\\frac{dy}{dx}", color=YELLOW).scale(0.8).next_to(f_arrow, DOWN, buff=0.1)
        dz_dy = MathTex("\\frac{dz}{dy}", color=ORANGE).scale(0.8).next_to(g_arrow, DOWN, buff=0.1)
        
        # Build chain rule visualization
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(x_box, x_label), run_time=0.5)
        self.play(Create(f_arrow), Write(f_label), FadeIn(y_box, y_label), run_time=1)
        self.play(Create(g_arrow), Write(g_label), FadeIn(z_box, z_label), run_time=1)
        
        # Show basic chain rule
        self.play(Write(chain_basic), run_time=1)
        self.chain_basic = chain_basic  # store for later
        
        self.wait(0.5)
        self.play(chain_basic.animate.scale(0.7).to_corner(DR), run_time=0.8)
        
        # Add gradient labels
        self.play(Write(dy_dx), run_time=0.5)
        self.play(Write(dz_dy), run_time=0.5)
        
        # Final composition
        full_chain = MathTex("\\frac{dz}{dx} = \\frac{dz}{dy} \\cdot \\frac{dy}{dx}", color=WHITE)
        full_chain.scale(1.2)
        full_chain.next_to(VGroup(x_box, y_box, z_box), DOWN, buff=0.8)
        
        # Highlight the multiplication
        self.play(Write(full_chain), run_time=1)
        
        # Animate the multiplication visually
        first = full_chain[0][7:12]  # dz/dy part
        second = full_chain[0][13:]  # dy/dx part
        
        self.play(Indicate(first, color=ORANGE), run_time=0.8)
        self.play(Indicate(second, color=YELLOW), run_time=0.8)
        
        # Extend to longer chains (crucial for deep networks)
        extended = MathTex("\\frac{\\partial L}{\\partial w} = \\frac{\\partial L}{\\partial \\hat{y}} \\cdot \\frac{\\partial \\hat{y}}{\\partial z} \\cdot \\frac{\\partial z}{\\partial w}", color=WHITE)
        extended.scale(1)
        extended.next_to(full_chain, DOWN, buff=0.6)
        
        extend_text = Text("For neural networks:", font_size=24, color=YELLOW)
        extend_text.next_to(extended, UP, buff=0.2)
        
        self.play(FadeIn(extend_text), Write(extended), run_time=1.5)
        
        # Color code the terms
        self.play(extended[0][5:10].animate.set_color(RED), run_time=0.5)  # dL/dyhat
        self.play(extended[0][11:17].animate.set_color(GREEN), run_time=0.5)  # dyhat/dz
        self.play(extended[0][18:].animate.set_color(BLUE), run_time=0.5)  # dz/dw
        
        self.wait(1.5)
        
        # Store for transition
        self.chain_elements = VGroup(title, x_box, x_label, y_box, y_label, z_box, z_label,
                                      f_arrow, g_arrow, f_label, g_label, dy_dx, dz_dy,
                                      full_chain, extend_text, extended, self.chain_basic)
    
    def scene4_local_gradient(self):
        # Single neuron with all components visible
        title = Text("Local Gradients: One Neuron", font_size=36, color=GREEN)
        title.to_edge(UP)
        
        # Neuron components spread out vertically
        x_val = MathTex("x = 2.0", color=BLUE).shift(UP * 2.5 + LEFT * 3)
        w_val = MathTex("w = 3.0", color=YELLOW).shift(UP * 2.5 + RIGHT * 3)
        
        # Weight multiplication
        mult_box = Rectangle(width=2, height=1, color=YELLOW, fill_opacity=0.2)
        mult_box.shift(UP * 0.5)
        mult_label = MathTex("z = w \\cdot x", color=YELLOW).scale(0.9).move_to(mult_box)
        mult_result = MathTex("= 6.0", color=WHITE).scale(0.8).next_to(mult_box, RIGHT)
        
        # Addition with bias
        b_val = MathTex("b = 1.0", color=PURPLE).shift(DOWN * 0.5 + LEFT * 3.5)
        
        add_box = Rectangle(width=2, height=1, color=PURPLE, fill_opacity=0.2)
        add_box.shift(DOWN * 2)
        add_label = MathTex("a = z + b", color=PURPLE).scale(0.9).move_to(add_box)
        add_result = MathTex("= 7.0", color=WHITE).scale(0.8).next_to(add_box, RIGHT)
        
        # Activation
        sigma_box = Rectangle(width=2, height=1, color=RED, fill_opacity=0.2)
        sigma_box.shift(DOWN * 4)
        sigma_label = MathTex("\\hat{y} = \\sigma(a)", color=RED).scale(0.9).move_to(sigma_box)
        sigma_result = MathTex("= 0.999", color=WHITE).scale(0.8).next_to(sigma_box, RIGHT)
        
        # Arrows showing computation flow
        arrow1 = Arrow(x_val.get_bottom(), mult_box.get_top(), color=GRAY, buff=0.2)
        arrow_w = Arrow(w_val.get_bottom(), mult_box.get_top(), color=GRAY, buff=0.2)
        arrow2 = Arrow(mult_box.get_bottom(), add_box.get_top(), color=GRAY, buff=0.2)
        arrow_b = Arrow(b_val.get_right(), add_box.get_left(), color=GRAY, buff=0.2)
        arrow3 = Arrow(add_box.get_bottom(), sigma_box.get_top(), color=GRAY, buff=0.2)
        
        # Build forward computation
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(x_val), FadeIn(w_val), run_time=0.6)
        self.play(Create(arrow1), Create(arrow_w), FadeIn(mult_box, mult_label), run_time=0.8)
        self.play(Write(mult_result), run_time=0.5)
        self.play(FadeIn(b_val), Create(arrow2), Create(arrow_b), FadeIn(add_box, add_label), run_time=0.8)
        self.play(Write(add_result), run_time=0.5)
        self.play(Create(arrow3), FadeIn(sigma_box, sigma_label), run_time=0.8)
        self.play(Write(sigma_result), run_time=0.5)
        
        self.wait(0.5)
        
        # Now show backward gradients
        grad_title = Text("Backward: Compute local gradients", font_size=28, color=GREEN)
        grad_title.to_edge(DOWN)
        
        # Loss at output
        loss_val = MathTex("L = \\frac{1}{2}(1.0 - 0.999)^2 \\approx 5 \\times 10^{-7}", color=ORANGE)
        loss_val.next_to(sigma_box, RIGHT, buff=1)
        
        # Backprop arrows (going up)
        back_arrow1 = Arrow(sigma_box.get_top(), add_box.get_bottom(), color=RED, buff=0.2)
        dL_da = MathTex("\\frac{\\partial L}{\\partial a}", color=RED).scale(0.7)
        dL_da.next_to(back_arrow1, RIGHT)
        
        back_arrow2 = Arrow(add_box.get_top(), mult_box.get_bottom(), color=PURPLE, buff=0.2)
        dL_dz = MathTex("\\frac{\\partial L}{\\partial z}", color=PURPLE).scale(0.7)
        dL_dz.next_to(back_arrow2, LEFT)
        
        back_arrow3_left = Arrow(mult_box.get_top(), x_val.get_bottom(), color=BLUE, buff=0.2)
        dL_dx = MathTex("\\frac{\\partial L}{\\partial x}", color=BLUE).scale(0.7)
        dL_dx.next_to(back_arrow3_left, LEFT)
        
        back_arrow3_right = Arrow(mult_box.get_top(), w_val.get_bottom(), color=YELLOW, buff=0.2)
        dL_dw = MathTex("\\frac{\\partial L}{\\partial w}", color=YELLOW).scale(0.7)
        dL_dw.next_to(back_arrow3_right, RIGHT)
        
        # Animate backward pass
        self.play(Write(grad_title), run_time=0.8)
        self.play(FadeIn(loss_val), run_time=0.5)
        
        # Chain rule application step by step
        self.play(Create(back_arrow1), Write(dL_da), run_time=0.8)
        
        # Local gradient for sigmoid
        sigmoid_grad = MathTex("\\sigma'(a) = \\sigma(a)(1-\\sigma(a))", color=RED).scale(0.7)
        sigmoid_grad.next_to(dL_da, UP, buff=0.3)
        self.play(Write(sigmoid_grad), run_time=0.8)
        
        self.play(Create(back_arrow2), Write(dL_dz), run_time=0.8)
        
        # Local gradient for addition (pass-through)
        add_grad = MathTex("\\frac{\\partial a}{\\partial z} = 1", color=PURPLE).scale(0.7)
        add_grad.next_to(dL_dz, UP, buff=0.2)
        self.play(Write(add_grad), run_time=0.6)
        
        self.play(Create(back_arrow3_left), Write(dL_dx), run_time=0.6)
        self.play(Create(back_arrow3_right), Write(dL_dw), run_time=0.6)
        
        # Show multiplication
        mult_local = MathTex("\\frac{\\partial z}{\\partial w} = x = 2.0", color=YELLOW).scale(0.7)
        mult_local.next_to(dL_dw, UP, buff=0.3)
        self.play(Write(mult_local), run_time=0.8)
        
        self.wait(1.5)
        
        self.neuron_elements = VGroup(title, x_val, w_val, b_val, mult_box, mult_label, mult_result,
                                      add_box, add_label, add_result, sigma_box, sigma_label, sigma_result,
                                      arrow1, arrow_w, arrow2, arrow_b, arrow3,
                                      grad_title, loss_val, back_arrow1, back_arrow2, back_arrow3_left, back_arrow3_right,
                                      dL_da, dL_dz, dL_dx, dL_dw, sigmoid_grad, add_grad, mult_local)
    
    def scene5_one_layer_backprop(self):
        # Network with multiple inputs and outputs for one layer
        title = Text("Backprop Through a Layer", font_size=36, color=YELLOW)
        title.to_edge(UP)
        
        # Input vector
        input_rect = RoundedRectangle(corner_radius=0.2, width=1.2, height=2.5, color=BLUE, fill_opacity=0.2)
        input_rect.shift(LEFT * 5)
        input_label = MathTex("\\mathbf{x}", color=BLUE).move_to(input_rect)
        x1 = MathTex("x_1").scale(0.7).next_to(input_rect, LEFT).shift(UP * 0.6)
        x2 = MathTex("x_2").scale(0.7).next_to(input_rect, LEFT).shift(DOWN * 0.6)
        
        # Weight matrix
        W_rect = RoundedRectangle(corner_radius=0.2, width=1.5, height=2, color=YELLOW, fill_opacity=0.3)
        W_rect.shift(LEFT * 2.5)
        W_label = MathTex("\\mathbf{W}", color=YELLOW).move_to(W_rect)
        W_size = MathTex("^{2 \\times 3}", color=GRAY).scale(0.6).next_to(W_label, UR, buff=0.05)
        
        # Output vector (pre-activation)
        z_rect = RoundedRectangle(corner_radius=0.2, width=1.2, height=2, color=GREEN, fill_opacity=0.2)
        z_rect.shift(RIGHT * 0.5)
        z_label = MathTex("\\mathbf{z}", color=GREEN).move_to(z_rect)
        
        # Activation output
        a_rect = RoundedRectangle(corner_radius=0.2, width=1.2, height=2, color=RED, fill_opacity=0.2)
        a_rect.shift(RIGHT * 3)
        a_label = MathTex("\\mathbf{a}", color=RED).move_to(a_rect)
        
        # Sigma for activation
        sigma_circ = Circle(radius=0.4, color=RED, fill_opacity=0.2).shift(RIGHT * 2)
        sigma_in = MathTex("\\sigma").scale(0.7).move_to(sigma_circ)
        
        # Arrows
        arrow_xW = Arrow(input_rect.get_right(), W_rect.get_left(), color=GRAY, buff=0.2)
        arrow_Wz = Arrow(W_rect.get_right(), z_rect.get_left(), color=GRAY, buff=0.2)
        arrow_z_sigma = Arrow(z_rect.get_right(), sigma_circ.get_left(), color=GRAY, buff=0.2)
        arrow_sigma_a = Arrow(sigma_circ.get_right(), a_rect.get_left(), color=GRAY, buff=0.2)
        
        # Matrix multiplication formula
        matmul = MathTex("\\mathbf{z} = \\mathbf{W}\\mathbf{x} + \\mathbf{b}", color=WHITE)
        matmul.next_to(VGroup(W_rect, z_rect), UP, buff=0.5)
        
        # Build forward
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(input_rect, input_label, x1, x2), run_time=0.6)
        self.play(Create(arrow_xW), FadeIn(W_rect, W_label, W_size), run_time=0.8)
        self.play(Create(arrow_Wz), FadeIn(z_rect, z_label), run_time=0.6)
        self.play(Write(matmul), run_time=0.8)
        self.play(Create(arrow_z_sigma), FadeIn(sigma_circ, sigma_in), run_time=0.6)
        self.play(Create(arrow_sigma_a), FadeIn(a_rect, a_label), run_time=0.6)
        
        self.wait(0.5)
        
        # Backprop: gradient of loss w.r.t. outputs
        dL_da_label = MathTex("\\frac{\\partial L}{\\partial \\mathbf{a}}", color=RED)
        dL_da_label.next_to(a_rect, RIGHT, buff=0.5)
        
        # Coming from next layer (assume known)
        self.play(Write(dL_da_label), run_time=0.8)
        
        # Backprop through activation (element-wise)
        back_act = Arrow(a_rect.get_left(), z_rect.get_right(), color=RED, buff=0.2)
        dL_dz = MathTex("\\frac{\\partial L}{\\partial \\mathbf{z}}", color=GREEN)
        dL_dz.next_to(z_rect, LEFT, buff=0.5)
        
        act_grad = MathTex("\\odot \\sigma'(\\mathbf{z})", color=RED).scale(0.8)
        act_grad.next_to(back_act, UP, buff=0.1)
        
        self.play(Create(back_act), Write(act_grad), run_time=0.8)
        self.play(Write(dL_dz), run_time=0.6)
        
        # Backprop through linear layer: key insight!
        back_linear = Arrow(z_rect.get_left(), W_rect.get_right(), color=GREEN, buff=0.2)
        dL_dW = MathTex("\\frac{\\partial L}{\\partial \\mathbf{W}}", color=YELLOW)
        dL_dW.next_to(W_rect, LEFT, buff=0.5)
        
        # The core formula for weight gradients
        weight_grad = MathTex("\\frac{\\partial L}{\\partial W_{ij}} = \\frac{\\partial L}{\\partial z_i} \\cdot x_j", color=WHITE)
        weight_grad.scale(0.9)
        weight_grad.shift(DOWN * 2.5)
        
        # Outer product visualization
        outer = MathTex("\\frac{\\partial L}{\\partial \\mathbf{W}} = \\frac{\\partial L}{\\partial \\mathbf{z}} \\cdot \\mathbf{x}^\\top", color=YELLOW)
        outer.scale(0.9)
        outer.next_to(weight_grad, DOWN, buff=0.3)
        
        self.play(Create(back_linear), run_time=0.6)
        self.play(Write(weight_grad), run_time=1)
        self.play(Write(outer), run_time=1)
        
        # Highlight: gradient for input (to propagate further back)
        dL_dx = MathTex("\\frac{\\partial L}{\\partial \\mathbf{x}} = \\mathbf{W}^\\top \\frac{\\partial L}{\\partial \\mathbf{z}}", color=BLUE)
        dL_dx.scale(0.9)
        dL_dx.next_to(outer, DOWN, buff=0.3)
        
        self.play(Write(dL_dx), run_time=1)
        
        # Visual emphasis on W transpose
        emphasize = outer[0][19:21]  # x^T part
        self.play(Indicate(emphasize, color=YELLOW, scale_factor=1.5), run_time=0.8)
        
        # Emphasize that same梯度 flows backward
        flow_arrow = Arrow(dL_dx.get_left(), input_rect.get_bottom(), color=BLUE, buff=0.3, 
                          path_arc=-PI/4)
        self.play(Create(flow_arrow), run_time=0.6)
        
        self.wait(1.5)
        
        self.layer_elements = VGroup(title, input_rect, input_label, x1, x2, W_rect, W_label, W_size,
                                     z_rect, z_label, a_rect, a_label, sigma_circ, sigma_in,
                                     arrow_xW, arrow_Wz, arrow_z_sigma, arrow_sigma_a, matmul,
                                     dL_da_label, back_act, dL_dz, act_grad, back_linear, dL_dW,
                                     weight_grad, outer, dL_dx, flow_arrow)
    
    def scene6_multilayer_structure(self):
        # Multi-layer network showing where gradients flow
        title = Text("Multi-Layer Network", font_size=36, color=WHITE)
        title.to_edge(UP)
        
        # Three layer network: input -> hidden -> hidden -> output
        layers = []
        layer_colors = [BLUE, GREEN, PURPLE, RED]
        layer_sizes = [3, 4, 4, 2]
        layer_names = ["\\mathbf{x}", "\\mathbf{h}^{[1]}", "\\mathbf{h}^{[2]}", "\\mathbf{\\hat{y}}"]
        x_positions = [-5, -1.5, 2, 5]
        
        for i, (size, color, name, x_pos) in enumerate(zip(layer_sizes, layer_colors, layer_names, x_positions)):
            nodes = VGroup(*[Dot(color=color, radius=0.2) for _ in range(min(size, 4))])
            if size > 4:
                nodes = VGroup(*[Dot(color=color, radius=0.2) for _ in range(3)])
                dots = MathTex("\\vdots").scale(0.8)
                nodes.add(dots)
            nodes.arrange(DOWN, buff=0.6)
            nodes.shift(RIGHT * x_pos)
            
            label = MathTex(name, color=color).scale(0.9)
            label.next_to(nodes, UP if i < 2 else DOWN, buff=0.3)
            
            layers.append((nodes, label))
        
        # Connections between layers
        all_connections = VGroup()
        layer_connections = []
        for i in range(len(layers) - 1):
            conns = VGroup()
            for n1 in layers[i][0]:
                if n1 == layers[i][0][-1] and len(layers[i][0]) > 3 and isinstance(n1, (MathTex, Tex)):
                    continue
                for n2 in layers[i+1][0]:
                    if n2 == layers[i+1][0][-1] and len(layers[i+1][0]) > 3 and isinstance(n2, (MathTex, Tex)):
                        continue
                    conn = Line(n1.get_center(), n2.get_center(), color=GRAY, stroke_width=1.5)
                    conns.add(conn)
            layer_connections.append(conns)
            all_connections.add(conns)
        
        # Weight labels for layers
        W_labels = []
        for i in range(3):
            W_l = MathTex(f"\\mathbf{{W}}^{{[{i+1}]}}", color=YELLOW).scale(0.8)
            mid_x = (x_positions[i] + x_positions[i+1]) / 2
            W_l.shift(RIGHT * mid_x + UP * 1.5)
            W_labels.append(W_l)
        
        # Build network
        self.play(Write(title), run_time=0.8)
        
        for (nodes, label), W_l in zip(layers[:3], W_labels[:3]):
            self.play(FadeIn(nodes), Write(label), run_time=0.6)
            self.play(FadeIn(W_l), run_time=0.4)
        
        self.play(FadeIn(layers[3][0]), Write(layers[3][1]), run_time=0.6)
        
        # Add connections with animation
        for conns, W_l in zip(layer_connections[:3], W_labels[:3]):
            self.play(Create(conns), run_time=0.8)
        
        # Add activation labels
        sigma1 = MathTex("\\sigma", color=GREEN).scale(0.7).next_to(W_labels[0], RIGHT)
        sigma2 = MathTex("\\sigma", color=PURPLE).scale(0.7).next_to(W_labels[1], RIGHT)
        sigma3 = MathTex("\\sigma", color=RED).scale(0.7).next_to(W_labels[2], RIGHT)
        
        self.play(Write(sigma1), Write(sigma2), Write(sigma3), run_time=0.8)
        
        self.wait(0.5)
        
        # Now show backward flow
        backprop_title = Text("Backward Flow of Gradients", font_size=28, color=ORANGE)
        backprop_title.next_to(title, DOWN, buff=0.3)
        
        # Loss at output
        loss_node = MathTex("L", color=ORANGE).scale(1.5).shift(RIGHT * 5 + UP * 2)
        loss_arrow = Arrow(loss_node.get_bottom(), layers[3][0].get_top(), color=ORANGE, buff=0.2)
        
        self.play(FadeIn(loss_node), Create(loss_arrow), run_time=0.8)
        self.play(Write(backprop_title), run_time=0.6)
        
        # Gradient flow visualization (animated along paths)
        backward_colors = [ORANGE, PURPLE, GREEN]
        backward_labels_text = ["\\delta^{[3]}", "\\delta^{[2]}", "\\delta^{[1]}"]
        
        for i in range(2, -1, -1):  # From output to input
            # Create flowing arrows for gradients
            grad_arrows = VGroup()
            if i == 2:  # Output layer
                for n in layers[3][0]:
                    if isinstance(n, (MathTex, Tex)):
                        continue
                    for m in layers[2][0]:
                        if isinstance(m, (MathTex, Tex)):
                            continue
                        arr = Arrow(n.get_center(), m.get_center(), color=backward_colors[2-i], 
                                   buff=0.3, stroke_width=2)
                        grad_arrows.add(arr)
            elif i == 1:
                for n in layers[2][0]:
                    if isinstance(n, (MathTex, Tex)):
                        continue
                    for m in layers[1][0]:
                        if isinstance(m, (MathTex, Tex)):
                            continue
                        arr = Arrow(n.get_center(), m.get_center(), color=backward_colors[2-i],
                                   buff=0.3, stroke_width=2)
                        grad_arrows.add(arr)
            else:
                for n in layers[1][0]:
                    if isinstance(n, (MathTex, Tex)):
                        continue
                    for m in layers[0][0]:
                        if isinstance(m, (MathTex, Tex)):
                            continue
                        arr = Arrow(n.get_center(), m.get_center(), color=backward_colors[2-i],
                                   buff=0.3, stroke_width=2)
                        grad_arrows.add(arr)
            
            delta_label = MathTex(backward_labels_text[2-i], color=backward_colors[2-i])
            mid_x = (x_positions[i] + x_positions[i+1]) / 2
            delta_label.shift(RIGHT * mid_x + DOWN * 1.8)
            
            self.play(LaggedStart(*[GrowArrow(a) for a in grad_arrows[:8]], lag_ratio=0.1), 
                     run_time=1.2)
            self.play(Write(delta_label), run_time=0.6)
        
        # Key insight: gradients flow backward through transpose weights
        insight = Text("Key: Transpose weight matrices to propagate backward!", 
                      font_size=24, color=YELLOW)
        insight.to_edge(DOWN)
        
        # Show transpose notation
        W_transpose = MathTex("(\\mathbf{W}^{[l]})^\\top", color=YELLOW).scale(1.2)
        W_transpose.next_to(insight, UP, buff=0.2)
        
        self.play(Write(insight), run_time=1)
        self.play(FadeIn(W_transpose), run_time=0.6)
        
        self.wait(1.5)
        
        self.multilayer_elements = VGroup(title, *[n for nodes, _ in layers for n in nodes], 
                                         *[l for _, l in layers],
                                         all_connections, *W_labels, sigma1, sigma2, sigma3,
                                         backprop_title, loss_node, loss_arrow, insight, W_transpose)
    
    def scene7_full_algorithm(self):
        # Complete backprop algorithm as pseudocode/steps
        title = Text("The Backpropagation Algorithm", font_size=34, color=RED)
        title.to_edge(UP)
        
        # Step boxes
        steps = VGroup()
        
        # Step 1: Forward pass
        step1_rect = RoundedRectangle(corner_radius=0.2, width=12, height=1.2, color=BLUE, fill_opacity=0.15)
        step1_rect.shift(UP * 2.5)
        step1_num = MathTex("\\mathbf{1}", color=BLUE).scale(1.2)
        step1_num.move_to(step1_rect.get_left() + RIGHT * 0.5)
        step1_text = Text("Forward pass: Compute all", font_size=22, color=WHITE)
        step1_text2 = MathTex("z^{[l]} = W^{[l]}a^{[l-1]} + b^{[l]}, \\quad a^{[l]} = \\sigma(z^{[l]})", color=WHITE)
        step1_text.next_to(step1_num, RIGHT, buff=0.3)
        step1_text2.scale(0.7).next_to(step1_text, DOWN, aligned_edge=LEFT)
        
        step1 = VGroup(step1_rect, step1_num, step1_text, step1_text2)
        steps.add(step1)
        
        # Step 2: Output error
        step2_rect = RoundedRectangle(corner_radius=0.2, width=12, height=1.2, color=GREEN, fill_opacity=0.15)
        step2_rect.shift(UP * 0.8)
        step2_num = MathTex("\\mathbf{2}", color=GREEN).scale(1.2)
        step2_num.move_to(step2_rect.get_left() + RIGHT * 0.5)
        step2_text = Text("Output layer error:", font_size=22, color=WHITE)
        step2_text2 = MathTex("\\delta^{[L]} = \\nabla_a L \\odot \\sigma'(z^{[L]})", color=WHITE)
        step2_text.next_to(step2_num, RIGHT, buff=0.3)
        step2_text2.scale(0.7).next_to(step2_text, DOWN, aligned_edge=LEFT)
        
        step2 = VGroup(step2_rect, step2_num, step2_text, step2_text2)
        steps.add(step2)
        
        # Step 3: Backpropagate error
        step3_rect = RoundedRectangle(corner_radius=0.2, width=12, height=1.2, color=YELLOW, fill_opacity=0.15)
        step3_rect.shift(DOWN * 0.9)
        step3_num = MathTex("\\mathbf{3}", color=YELLOW).scale(1.2)
        step3_num.move_to(step3_rect.get_left() + RIGHT * 0.5)
        step3_text = Text("Backward pass: For", font_size=22, color=WHITE)
        step3_text2 = MathTex("l = L-1, L-2, \\ldots, 1: \\quad \\delta^{[l]} = ((W^{[l+1]})^\\top \\delta^{[l+1]}) \\odot \\sigma'(z^{[l]})", color=WHITE)
        step3_text.next_to(step3_num, RIGHT, buff=0.3)
        step3_text2.scale(0.65).next_to(step3_text, DOWN, aligned_edge=LEFT)
        
        step3 = VGroup(step3_rect, step3_num, step3_text, step3_text2)
        steps.add(step3)
        
        # Step 4: Compute gradients
        step4_rect = RoundedRectangle(corner_radius=0.2, width=12, height=1.2, color=PURPLE, fill_opacity=0.15)
        step4_rect.shift(DOWN * 2.6)
        step4_num = MathTex("\\mathbf{4}", color=PURPLE).scale(1.2)
        step4_num.move_to(step4_rect.get_left() + RIGHT * 0.5)
        step4_text = Text("Compute gradients:", font_size=22, color=WHITE)
        step4_text2 = MathTex("\\frac{\\partial L}{\\partial W^{[l]}} = \\delta^{[l]}(a^{[l-1]})^\\top, \\quad \\frac{\\partial L}{\\partial b^{[l]}} = \\delta^{[l]}", color=WHITE)
        step4_text.next_to(step4_num, RIGHT, buff=0.3)
        step4_text2.scale(0.65).next_to(step4_text, DOWN, aligned_edge=LEFT)
        
        step4 = VGroup(step4_rect, step4_num, step4_text, step4_text2)
        steps.add(step4)
        
        # Build algorithm step by step
        self.play(Write(title), run_time=0.8)
        
        # Animate each step appearing
        for i, step in enumerate(steps):
            self.play(FadeIn(step[0]), run_time=0.5)  # rectangle
            self.play(FadeIn(step[1]), Write(step[2]), run_time=0.5)  # number and text
            self.play(Write(step[3]), run_time=0.8)  # equation
            
            # Brief highlight
            self.play(step[0].animate.set_fill(opacity=0.3), run_time=0.3)
            self.play(step[0].animate.set_fill(opacity=0.15), run_time=0.3)
        
        self.wait(0.5)
        
        # Visual chain connecting the steps
        chain_line = DashedLine(steps[0][0].get_bottom(), steps[1][0].get_top(), color=WHITE)
        chain_line2 = DashedLine(steps[1][0].get_bottom(), steps[2][0].get_top(), color=WHITE)
        chain_line3 = DashedLine(steps[2][0].get_bottom(), steps[3][0].get_top(), color=WHITE)
        
        self.play(Create(chain_line), Create(chain_line2), Create(chain_line3), run_time=0.8)
        
        # KEY INSIGHT box
        insight_box = Rectangle(width=10, height=1, color=RED, fill_opacity=0.2)
        insight_box.to_edge(DOWN)
        insight_text = Text("Repeated application of chain rule + cached forward values", 
                           font_size=22, color=WHITE)
        insight_text.move_to(insight_box)
        
        self.play(FadeIn(insight_box), Write(insight_text), run_time=1)
        
        # Show efficiency: why it's O(network size) not exponential
        efficiency = MathTex("\\text{Time: } O(\\text{network size}) \\quad \\text{vs} \\quad \\text{Naive: } O(e^{\\text{layers}})", color=GREEN)
        efficiency.scale(0.8).next_to(insight_box, UP, buff=0.3)
        
        self.play(Write(efficiency), run_time=1)
        
        # Highlight that forward values are reused
        reuse_arrow = Arrow(steps[0][0].get_right(), steps[2][0].get_right(), color=ORANGE, 
                           buff=0, path_arc=-PI/3)
        reuse_text = Text("Reuse!", color=ORANGE, font_size=18)
        reuse_text.next_to(reuse_arrow, RIGHT)
        
        self.play(Create(reuse_arrow), FadeIn(reuse_text), run_time=0.8)
        
        self.wait(1.5)
        
        self.algorithm_elements = VGroup(title, steps, chain_line, chain_line2, chain_line3,
                                          insight_box, insight_text, efficiency, reuse_arrow, reuse_text)
    
    def scene8_weight_update_summary(self):
        # Final scene: putting it all together with visual weight update
        title = Text("Weight Update & Summary", font_size=36, color=GREEN)
        title.to_edge(UP)
        
        # Gradient descent visualization
        gd_title = Text("Gradient Descent", font_size=28, color=YELLOW)
        gd_title.shift(UP * 2.5 + LEFT * 4)
        
        # Loss landscape (2D paraboloid approximation)
        axes = Axes(x_range=[-3, 3, 1], y_range=[0, 4, 1], 
                   x_length=5, y_length=3,
                   axis_config={"include_tip": False})
        axes.shift(RIGHT * 3.5 + UP * 0.5)
        
        # Parabola for loss
        parabola = axes.plot(lambda x: x**2, color=BLUE, stroke_width=3)
        
        # Current position and gradient direction
        dot = Dot(axes.c2p(-2, 4), color=RED, radius=0.15)
        grad_arrow = Arrow(axes.c2p(-2, 4), axes.c2p(-1, 4), color=RED, buff=0.1)
        grad_label = MathTex("-\\eta \\nabla L", color=RED).scale(0.8).next_to(grad_arrow, UP)
        
        # New position after update
        new_dot = Dot(axes.c2p(-1, 1), color=GREEN, radius=0.15)
        update_arrow = Arrow(axes.c2p(-2, 4), axes.c2p(-1, 1), color=GREEN, buff=0.1)
        
        # Build gradient descent visualization
        self.play(Write(title), run_time=0.8)
        self.play(Write(gd_title), run_time=0.6)
        self.play(Create(axes), Create(parabola), run_time=1.2)
        
        self.play(FadeIn(dot), run_time=0.5)
        self.play(Create(grad_arrow), Write(grad_label), run_time=0.8)
        self.play(Transform(dot, new_dot), Create(update_arrow), run_time=1)
        
        # Weight update formula
        update_formula = MathTex("w_{\\text{new}} = w_{\\text{old}} - \\eta \\frac{\\partial L}{\\partial w}", color=WHITE)
        update_formula.scale(1.2)
        update_formula.shift(LEFT * 3 + DOWN * 0.5)
        
        self.play(Write(update_formula), run_time=1)
        
        # Learning rate importance
        lr_text = Text("Learning rate \\eta: crucial hyperparameter", font_size=22, color=ORANGE)
        lr_text.next_to(update_formula, DOWN, buff=0.5)
        
        self.play(Write(lr_text), run_time=0.8)
        
        self.wait(0.5)
        
        # Summary of full process
        self.play(FadeOut(axes, parabola, dot, grad_arrow, grad_label, new_dot, update_arrow), run_time=0.5)
        
        # Summary diagram: full cycle
        summary_title = Text("Full Training Cycle", font_size=26, color=BLUE)
        summary_title.shift(UP * 1)
        
        # Circular flow
        cycle_center = DOWN * 0.5
        cycle_radius = 2.5
        
        # Four stages in cycle
        stages = [
            ("Forward", BLUE, cycle_radius * np.array([1, 0, 0])),
            ("Compute Loss", RED, cycle_radius * np.array([0, -1, 0])),
            ("Backward", GREEN, cycle_radius * np.array([-1, 0, 0])),
            ("Update", YELLOW, cycle_radius * np.array([0, 1, 0])),
        ]
        
        stage_objects = []
        for name, color, pos in stages:
            circle = Circle(radius=0.8, color=color, fill_opacity=0.2)
            circle.move_to(cycle_center + pos)
            text = Text(name, font_size=20, color=color)
            text.move_to(circle)
            stage_objects.append((circle, text))
        
        # Create cycle
        self.play(Write(summary_title), run_time=0.6)
        for circle, text in stage_objects:
            self.play(FadeIn(circle), Write(text), run_time=0.5)
        
        # Arrows between stages
        cycle_arrows = VGroup()
        for i in range(4):
            start = stage_objects[i][0].get_center()
            end = stage_objects[(i+1) % 4][0].get_center()
            # Arc arrow
            direction = end - start
            perpendicular = np.array([-direction[1], direction[0], 0])
            perpendicular = perpendicular / np.linalg.norm(perpendicular) * 0.5
            
            arc_path = ArcBetweenPoints(start + direction * 0.15, end - direction * 0.15, 
                                      angle=PI/4, radius=1.5)
            # Use CurvedArrow instead
            curved = CurvedArrow(start, end, color=WHITE, angle=PI/6, stroke_width=2)
            cycle_arrows.add(curved)
        
        self.play(LaggedStart(*[Create(a) for a in cycle_arrows], lag_ratio=0.25), run_time=1.5)
        
        # Epoch counter
        epoch_text = MathTex("\\text{Epochs: } 1, 2, 3, \\ldots, N", color=GRAY).scale(0.9)
        epoch_text.next_to(summary_title, UP, buff=0.3)
        
        self.play(Write(epoch_text), run_time=0.6)
        
        # Final key points
        points = VGroup(
            Text("• Efficient gradient computation via chain rule", font_size=22, color=WHITE),
            Text("• Gradients flow backward from output to input", font_size=22, color=WHITE),
            Text("• Enables training of deep neural networks", font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        points.shift(DOWN * 2.5)
        
        self.play(LaggedStart(*[Write(p) for p in points], lag_ratio=0.2), run_time=1.5)
        
        self.wait(2)
        
        # Final fade to end
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
        
        # End card
        end_text = Text("Backpropagation", font_size=48, color=BLUE)
        end_sub = Text("The algorithm that powers deep learning", font_size=28, color=GRAY)
        VGroup(end_text, end_sub).arrange(DOWN, buff=0.5)
        
        self.play(Write(end_text), run_time=1)
        self.play(Write(end_sub), run_time=1)
        self.wait(1)
        self.play(FadeOut(end_text), FadeOut(end_sub), run_time=1)
