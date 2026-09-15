import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Forward Pass Assembly Line ---
        self.clear()
        self.camera.background_color = "#181825"

        # Input layer
        input_node_a = Circle(radius=0.35, color="#89b4fa", stroke_width=2.0).move_to(
            (-4, 0.8, 0)
        )
        label_a = Text("x1", font="Sans", font_size=20).move_to(
            input_node_a.get_center()
        )
        label_a.set_color("#89b4fa")

        input_node_b = Circle(radius=0.35, color="#89b4fa", stroke_width=2.0).move_to(
            (-4, -0.8, 0)
        )
        label_b = Text("x2", font="Sans", font_size=20).move_to(
            input_node_b.get_center()
        )
        label_b.set_color("#89b4fa")

        layer_label_input = Text("Input", font="Sans", font_size=24).move_to(
            (-4, -1.8, 0)
        )
        layer_label_input.set_color("#89b4fa")

        # Hidden layer
        hidden_node = Circle(radius=0.45, color="#fab387", stroke_width=2.0).move_to(
            (0, 0, 0)
        )
        label_h = Text("h", font="Sans", font_size=28).move_to(hidden_node.get_center())
        label_h.set_color("#fab387")

        layer_label_hidden = Text("Hidden", font="Sans", font_size=24).move_to(
            (0, -1.8, 0)
        )
        layer_label_hidden.set_color("#fab387")

        # Output layer
        output_node = Circle(radius=0.45, color="#a6e3a1", stroke_width=2.0).move_to(
            (4, 0, 0)
        )
        label_y = Text("ŷ", font="Sans", font_size=28).move_to(output_node.get_center())
        label_y.set_color("#a6e3a1")

        layer_label_output = Text("Output", font="Sans", font_size=24).move_to(
            (4, -1.8, 0)
        )
        layer_label_output.set_color("#a6e3a1")

        # Forward arrows assembly line
        forward_arrow1 = Arrow(
            start=[-3, 0, 0], end=[0, 0, 0], color="#94e2d5", stroke_width=2.0
        )
        forward_arrow2 = Arrow(
            start=[0, 0, 0], end=[3, 0, 0], color="#94e2d5", stroke_width=2.0
        )

        # Build forward pass
        self.play(
            GrowFromCenter(input_node_a),
            GrowFromCenter(input_node_b),
            FadeIn(label_a),
            FadeIn(label_b),
            FadeIn(layer_label_input),
            run_time=1.5,
        )
        self.play(
            GrowFromCenter(hidden_node),
            GrowFromCenter(output_node),
            FadeIn(label_h),
            FadeIn(label_y),
            FadeIn(layer_label_hidden),
            FadeIn(layer_label_output),
            run_time=1.5,
        )
        self.play(Create(forward_arrow1), Create(forward_arrow2), run_time=1.0)
        self.play(
            Indicate(forward_arrow1, color="#94e2d5", scale_factor=1.1),
            Indicate(forward_arrow2, color="#94e2d5", scale_factor=1.1),
            run_time=2.0,
        )
        self.wait(2.0)
        # --- Scene 2: Loss as Vertical Gauge ---
        self.camera.background_color = "#181825"

        # Vertical Error gauge
        axis = NumberLine(x_range=[-2, 2, 1], length=6, color="#94e2d5")
        axis.stroke_width = 2.0
        axis.add_numbers()
        axis.rotate(PI / 2)

        axis_label = Text("Error", font_size=36)
        axis_label.set_color("#94e2d5")
        axis_label.next_to(axis, RIGHT)

        axis_group = VGroup(axis, axis_label)

        scale = 1.5  # length / (max-min) = 6 / 4
        target_val = -1.2
        pred_val = 0.8

        target_dot = Dot(point=[0, target_val * scale, 0], color="#89b4fa", radius=0.12)
        target_label = Text("Target", font_size=24, color="#89b4fa").next_to(
            target_dot, LEFT
        )
        target_group = VGroup(target_dot, target_label)

        pred_dot = Dot(point=[0, pred_val * scale, 0], color="#fab387", radius=0.12)
        pred_label = Text("Prediction", font_size=24, color="#fab387").next_to(
            pred_dot, RIGHT
        )
        pred_group = VGroup(pred_dot, pred_label)

        # Loss bar between markers
        mid_y = (target_val + pred_val) / 2 * scale
        bar_height = abs(pred_val - target_val) * scale
        loss_bar = Rectangle(
            width=0.25,
            height=bar_height,
            color="#f38ba8",
            fill_opacity=0.4,
            stroke_width=2.0,
        )
        loss_bar.move_to([0, mid_y, 0])
        loss_label = Text("Loss", font_size=24, color="#f38ba8").next_to(
            loss_bar, RIGHT
        )

        narration = Text(
            "Loss compares the network prediction to the true target, quantifying the error to minimize.",
            font_size=28,
        )
        narration.to_edge(DOWN)
        narration.set_color("#a6e3a1")

        self.play(Create(axis_group), run_time=1.5)
        self.play(FadeIn(target_group), run_time=0.8)
        self.play(FadeIn(pred_group), run_time=0.8)
        self.play(GrowFromCenter(loss_bar), FadeIn(loss_label), run_time=1.2)
        self.play(Write(narration), run_time=1.7)
        self.wait(1.0)
        # --- Scene 3: Chain Rule Domino Chain ---
        self.camera.background_color = "#181825"
        self.clear()

        # Title
        title = Text("Chain Rule Domino Chain", font_size=36, color="#89b4fa")
        title.to_edge(UP)

        def make_domino(label, color, x):
            rect = Rectangle(
                width=0.8, height=1.2, color=color, fill_opacity=0.85, stroke_width=2
            )
            rect.move_to([x, 0, 0])
            txt = Text(label, font_size=36, color=WHITE)
            txt.move_to(rect.get_center())
            return VGroup(rect, txt).set_z_index(1)

        dominoes = [
            make_domino("w", "#89b4fa", -4),
            make_domino("z", "#fab387", -2),
            make_domino("a", "#f38ba8", 0),
            make_domino("y", "#a6e3a1", 2),
            make_domino("L", "#94e2d5", 4),
        ]

        def make_link(left, right, color, label_tex):
            left_rect = left[0]
            right_rect = right[0]
            left_right = left_rect.get_right()[0]
            right_left = right_rect.get_left()[0]
            start_pt = [left_right + 0.15, -0.9, 0]
            end_pt = [right_left - 0.15, -0.9, 0]
            arrow = Arrow(start_pt, end_pt, color=color, stroke_width=2, buff=0)
            label = MathTex(label_tex, color=color)
            label.scale(0.7)
            label.next_to(arrow, UP, buff=0.08)
            return VGroup(arrow, label)

        link1 = make_link(dominoes[0], dominoes[1], "#89b4fa", r"\partial z/\partial w")
        link2 = make_link(dominoes[1], dominoes[2], "#fab387", r"\partial a/\partial z")
        link3 = make_link(dominoes[2], dominoes[4], "#f38ba8", r"\partial L/\partial a")

        equation = MathTex(
            r"\frac{dL}{dw}= \frac{\partial L}{\partial a}\frac{\partial a}{\partial z}\frac{\partial z}{\partial w}",
            color="#a6e3a1",
        )
        equation.scale(0.8)
        equation.to_edge(DOWN)

        self.play(FadeIn(title), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.8) for d in dominoes], lag_ratio=0.15),
            run_time=2.0,
        )
        self.wait(0.5)
        self.play(FadeIn(link1), run_time=0.7)
        self.play(FadeIn(link2), run_time=0.7)
        self.play(FadeIn(link3), run_time=0.7)
        self.wait(0.5)
        self.play(Write(equation), run_time=2.0)
        self.wait(2.4)
        # --- Scene 4: Local Derivative on Activation ---
        self.clear()
        self.camera.background_color = "#181825"

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 1, 0.2],
            x_length=8,
            y_length=5,
            axis_config={"color": "#94e2d5", "stroke_width": 2.0},
            tips=False,
        ).move_to(ORIGIN)

        sigmoid = axes.plot(
            lambda x: 1 / (1 + np.exp(-x)), color="#89b4fa", stroke_width=2.5
        )

        x0 = 1.0
        y0 = 1 / (1 + np.exp(-x0))
        point = Dot(axes.coords_to_point(x0, y0), radius=0.08, color="#fab387")
        point.set_stroke(width=2)

        m = y0 * (1 - y0)
        tangent = axes.plot(
            lambda x: y0 + m * (x - x0),
            x_range=[x0 - 0.9, x0 + 0.9],
            color="#f38ba8",
            stroke_width=2.5,
        )

        vline = DashedLine(
            axes.coords_to_point(x0, 0),
            axes.coords_to_point(x0, y0),
            color="#a6e3a1",
            stroke_width=1.5,
        )

        derivative_text = (
            MathTex(
                r"f'(x_0)=f(x_0)\bigl(1-f(x_0)\bigr)\approx {:.2f}".format(m),
                font_size=36,
            )
            .set_color("#a6e3a1")
            .to_corner(UR, buff=0.5)
        )

        title = Text(
            "Local Derivative on Activation", font_size=36, color="#89b4fa"
        ).to_edge(UP)

        self.play(Create(axes), run_time=1.0)
        self.play(Create(sigmoid), run_time=1.5)
        self.play(FadeIn(point), run_time=0.7)
        self.play(Create(vline), run_time=0.5)
        self.play(Create(tangent), run_time=1.0)
        self.play(FadeIn(derivative_text), run_time=0.8)
        self.play(Write(title), run_time=0.8)
        self.wait(2.2)
        # --- Scene 5: Backward Gradient Flow ---
        self.camera.background_color = "#181825"

        # Palette from style guidelines
        c1 = "#89b4fa"
        c2 = "#fab387"
        c3 = "#f38ba8"  # backward gradient color
        c4 = "#a6e3a1"
        c5 = "#94e2d5"

        input_x = -4
        hidden_x = 0
        output_x = 4
        y_vals = [-1.2, 0, 1.2]

        def make_layer(x):
            nodes = VGroup()
            for y in y_vals:
                circ = Circle(radius=0.22, color=c1, fill_opacity=0.9, stroke_width=2)
                circ.move_to([x, y, 0])
                nodes.add(circ)
            return nodes

        input_nodes = make_layer(input_x)
        hidden_nodes = make_layer(hidden_x)
        output_nodes = make_layer(output_x)

        layer_labels = VGroup(
            Text("Input", font="Sans", color=c4)
            .scale(0.6)
            .next_to(input_nodes, DOWN, buff=0.3),
            Text("Hidden", font="Sans", color=c4)
            .scale(0.6)
            .next_to(hidden_nodes, DOWN, buff=0.3),
            Text("Output", font="Sans", color=c4)
            .scale(0.6)
            .next_to(output_nodes, DOWN, buff=0.3),
        )

        network = VGroup(input_nodes, hidden_nodes, output_nodes, layer_labels)

        # Backward arrows right-to-left
        arrows = VGroup()
        for i, y in enumerate(y_vals):
            start = output_nodes[i].get_center()
            end = hidden_nodes[i].get_center()
            arr = Arrow(start=start, end=end, color=c3, stroke_width=2, buff=0.22)
            arrows.add(arr)

            start2 = hidden_nodes[i].get_center()
            end2 = input_nodes[i].get_center()
            arr2 = Arrow(start=start2, end=end2, color=c3, stroke_width=2, buff=0.22)
            arrows.add(arr2)

        # Specified back_arrow_out
        back_arrow_out = Arrow(
            start=[3, 0, 0], end=[0, 0, 0], color=c3, stroke_width=2, buff=0.1
        )
        arrows.add(back_arrow_out)

        label = MathTex(r"\partial L/\partial \hat{z}", color=c3).scale(0.6)
        label.next_to(back_arrow_out, UP, buff=0.1)
        arrows.add(label)

        self.play(FadeIn(network, shift=UP), run_time=2)
        self.play(FadeIn(arrows, shift=RIGHT), run_time=1)

        # Fixed: ScaleInPlace does not accept about_point; use .animate.scale with about_point
        shrink_anims = [
            arr.animate.scale(0.6, about_point=arr.get_end())
            for arr in arrows
            if isinstance(arr, Arrow)
        ]
        self.play(*shrink_anims, lag_ratio=0.25, run_time=3)
        self.wait(1)
        # --- Scene 6: Weight Dials Update ---
        # Set background and style
        self.camera.background_color = "#181825"

        # Layers
        left_layer = VGroup(*[Dot(radius=0.12, color="#89b4fa") for _ in range(3)])
        left_layer.arrange(DOWN, buff=0.8)
        left_layer.shift(LEFT * 4)

        right_layer = VGroup(*[Dot(radius=0.12, color="#89b4fa") for _ in range(3)])
        right_layer.arrange(DOWN, buff=0.8)
        right_layer.shift(RIGHT * 4)

        # Weight dials between layers
        dials = VGroup()
        gradient_arrows = VGroup()
        update_arrows = VGroup()
        rotation_arcs = VGroup()

        positions = [-2, 0, 2]
        for i, x in enumerate(positions):
            center = RIGHT * x
            circle = Circle(radius=0.6, color="#fab387", stroke_width=2, fill_opacity=0)
            circle.move_to(center)
            label = Text("w", font_size=36, color=WHITE).move_to(circle.get_center())
            dial = VGroup(circle, label)
            dials.add(dial)

            # Gradient arrow pointing right
            g_start = center + RIGHT * 0.8
            g_end = center + RIGHT * 2.0
            g_arrow = Arrow(g_start, g_end, color="#f38ba8", stroke_width=2, buff=0)
            gradient_arrows.add(g_arrow)

            # Update arrow pointing left (opposite)
            u_start = center + LEFT * 0.8
            u_end = center + LEFT * 2.0
            u_arrow = Arrow(u_start, u_end, color="#a6e3a1", stroke_width=2, buff=0)
            update_arrows.add(u_arrow)

            # Rotation indicator arc
            arc = Arc(
                radius=0.9,
                start_angle=-PI / 4,
                angle=PI / 2,
                color="#94e2d5",
                stroke_width=2,
            )
            arc.move_to(center)
            rotation_arcs.add(arc)

        # Narration text
        narration = Text(
            "Weights are updated by subtracting learning rate times gradient, moving the network toward lower loss.",
            font_size=28,
            color=WHITE,
            line_spacing=1.1,
        )
        narration.move_to(DOWN * 3)

        # Animations - total 7.5s
        self.play(FadeIn(left_layer), FadeIn(right_layer), FadeIn(dials), run_time=1.5)
        self.play(Create(gradient_arrows), run_time=1)
        self.play(Create(update_arrows), run_time=1)
        self.play(Rotate(rotation_arcs, angle=-PI / 2), run_time=2)
        self.play(Write(narration), run_time=1)
        self.wait(1)
        # --- Scene 7: Weight Update Rule ---
        self.camera.background_color = "#181825"

        # Formula
        formula = Text("w ← w - η ∂L/∂w", font_size=36, color="#a6e3a1")
        formula.move_to(ORIGIN)

        # Dials
        dial_eta = VGroup(
            Circle(radius=0.8, color="#89b4fa", stroke_width=2, fill_opacity=0),
            Arrow(ORIGIN, UP * 0.7, color="#fab387", stroke_width=2),
        )
        dial_eta.move_to(LEFT * 3)

        dial_grad = VGroup(
            Circle(radius=0.8, color="#94e2d5", stroke_width=2, fill_opacity=0),
            Arrow(ORIGIN, UP * 0.7, color="#f38ba8", stroke_width=2),
        )
        dial_grad.move_to(RIGHT * 3)

        # Loss gauge
        outline = Rectangle(
            height=2.8, width=0.5, color=WHITE, stroke_width=2, fill_opacity=0
        )
        fill_full = Rectangle(
            height=2.5, width=0.4, color="#f38ba8", fill_opacity=0.8, stroke_width=0
        )
        gauge = VGroup(outline, fill_full)
        gauge.move_to(DOWN * 2.5)

        loss_label = Text("Loss", font_size=24, color=WHITE)
        loss_label.next_to(gauge, UP, buff=0.2)

        descent_arrow = Arrow(DOWN * 1.2, DOWN * 2.0, color="#94e2d5", stroke_width=3)

        self.add(dial_eta, dial_grad, outline, fill_full, loss_label, descent_arrow)

        self.play(FadeIn(formula, shift=UP), run_time=1.5)
        self.wait(0.5)

        dial_rot1 = Rotate(dial_eta, angle=PI / 2, run_time=3)
        dial_rot2 = Rotate(dial_grad, angle=-PI / 2, run_time=3)
        # run_time is not a parameter of set_height; it is supplied to self.play
        loss_anim = fill_full.animate.set_height(0.5)

        self.play(AnimationGroup(dial_rot1, dial_rot2, loss_anim), run_time=3)
        self.wait(2.5)
        # --- Scene 8: Weight Update Rule ---
        self.camera.background_color = "#181825"

        # Dial with ticks and hand
        dial_circle = Circle(
            radius=0.6, color="#fab387", stroke_width=2, fill_opacity=0
        )
        ticks = VGroup(
            *[
                Line(ORIGIN, direction * 0.65, color="#fab387", stroke_width=2)
                for direction in [UP, UR, RIGHT, DR, DOWN, DL, LEFT, UL]
            ]
        )
        dial_hand = Arrow(ORIGIN, UP * 0.5, buff=0, color="#89b4fa", stroke_width=3)
        dial_group = VGroup(dial_circle, ticks, dial_hand)
        label_w = Text("w", font_size=36).next_to(dial_circle, DOWN)
        label_w.set_color("#fab387")

        # Gradient direction and learning rate
        grad_arrow = Arrow(ORIGIN, UP * 1.2, buff=0, color="#f38ba8", stroke_width=2)
        grad_arrow.next_to(dial_circle, RIGHT, buff=1.5)
        grad_label = MathTex(r"\frac{\partial L}{\partial w}", color="#f38ba8")
        grad_label.next_to(grad_arrow, UP, buff=0.1)
        eta_label = MathTex(r"\eta", color="#a6e3a1").scale(1.2)
        eta_label.next_to(grad_arrow, RIGHT, buff=0.5)

        # Update rule
        formula = MathTex(
            r"w \leftarrow w - \eta \frac{\partial L}{\partial w}", color="#a6e3a1"
        )
        formula.scale(0.8)
        formula.move_to(DOWN * 2.5)

        self.play(FadeIn(dial_group), FadeIn(label_w), run_time=1.5)
        self.wait(0.5)

        self.play(
            FadeIn(grad_arrow), FadeIn(grad_label), FadeIn(eta_label), run_time=1.0
        )
        self.wait(0.5)

        # Turn the dial opposite to the gradient
        self.play(Rotate(dial_hand, angle=-PI / 2, about_point=ORIGIN, run_time=2.0))

        self.play(FadeIn(formula), run_time=1.0)
        self.wait(1.0)
        # --- Scene 9: Weight Update Rule ---
        self.camera.background_color = "#181825"

        # Weight dial
        dial = Circle(radius=0.6, color="#fab387", stroke_width=2, fill_opacity=0)
        w_label = Text("w", font_size=36)
        w_label.move_to(ORIGIN)

        # Needle that will be turned opposite the gradient
        needle = Line(ORIGIN, UP * 0.5, color="#fab387", stroke_width=3)
        angle_tracker = ValueTracker(0)

        def update_needle(mob):
            angle = angle_tracker.get_value()
            end_point = rotate_vector(UP * 0.5, angle)
            mob.become(Line(ORIGIN, end_point, color="#fab387", stroke_width=3))

        needle.add_updater(update_needle)

        dial_group = VGroup(dial, needle, w_label)

        # Gradient direction
        grad_arrow = Arrow(
            start=UP * 1.2, end=UP * 2.2, color="#f38ba8", stroke_width=2.5
        )
        grad_label = MathTex(r"\nabla L", color="#f38ba8").scale(0.8)
        grad_label.next_to(grad_arrow, UP, buff=0.1)
        grad_group = VGroup(grad_arrow, grad_label)

        # Weight update rule
        formula = MathTex(
            r"w \leftarrow w - \eta \frac{\partial L}{\partial w}", color="#a6e3a1"
        ).scale(0.9)
        formula.next_to(dial_group, DOWN, buff=0.8)

        # 7.5s total: 1.5 + 2 + 3 + 1
        self.play(FadeIn(dial_group), run_time=1.5)
        self.play(FadeIn(grad_group), run_time=2)
        self.play(angle_tracker.animate.set_value(-PI / 2), run_time=3)
        self.play(FadeIn(formula), run_time=1)
