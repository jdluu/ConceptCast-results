import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Neural Network Architecture ---
        self.camera.background_color = "#181825"

        # Title
        title = Text("Neural Network Architecture", font_size=40, color="#cdd6f4")
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.2)
        self.wait(0.5)

        # Input Layer — 3 vertical bars
        input_bars = VGroup()
        input_values = [0.5, 0.8, 0.2]
        for val in input_values:
            bar = Rectangle(
                width=0.35,
                height=val * 3,
                fill_color="#89b4fa",
                fill_opacity=0.85,
                stroke_color="#89b4fa",
                stroke_width=2.0,
            )
            input_bars.add(bar)
        input_bars.arrange(RIGHT, buff=0.35)
        input_bars.move_to(LEFT * 4.5)

        input_label = Text("Input", font_size=24, color="#89b4fa")
        input_label.next_to(input_bars, DOWN, buff=0.3)

        self.play(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in input_bars], lag_ratio=0.2),
            run_time=1.5,
        )
        self.play(FadeIn(input_label), run_time=0.5)

        # Hidden Layer — 4 circles
        hidden_circles = VGroup()
        for _ in range(4):
            c = Circle(
                radius=0.35,
                fill_color="#fab387",
                fill_opacity=0.85,
                stroke_color="#fab387",
                stroke_width=2.0,
            )
            hidden_circles.add(c)
        hidden_circles.arrange(DOWN, buff=0.4)
        hidden_circles.move_to(ORIGIN)

        hidden_label = Text("Hidden", font_size=24, color="#fab387")
        hidden_label.next_to(hidden_circles, DOWN, buff=0.3)

        self.play(
            LaggedStart(*[GrowFromCenter(c) for c in hidden_circles], lag_ratio=0.15),
            run_time=1.5,
        )
        self.play(FadeIn(hidden_label), run_time=0.5)

        # Output Layer — 2 circles
        output_circles = VGroup()
        for _ in range(2):
            c = Circle(
                radius=0.4,
                fill_color="#89b4fa",
                fill_opacity=0.85,
                stroke_color="#89b4fa",
                stroke_width=2.0,
            )
            output_circles.add(c)
        output_circles.arrange(DOWN, buff=0.6)
        output_circles.move_to(RIGHT * 4.5)

        output_label = Text("Output", font_size=24, color="#89b4fa")
        output_label.next_to(output_circles, DOWN, buff=0.3)

        self.play(
            LaggedStart(*[GrowFromCenter(c) for c in output_circles], lag_ratio=0.2),
            run_time=1.5,
        )
        self.play(FadeIn(output_label), run_time=0.5)

        # Connections: Input → Hidden
        for bar in input_bars:
            for circle in hidden_circles:
                line = Line(
                    bar.get_right(),
                    circle.get_left(),
                    stroke_color="#585b70",
                    stroke_width=1.5,
                    stroke_opacity=0.6,
                )
                self.add(line)

        # Connections: Hidden → Output
        for circle in hidden_circles:
            for out_circle in output_circles:
                line = Line(
                    circle.get_right(),
                    out_circle.get_left(),
                    stroke_color="#585b70",
                    stroke_width=1.5,
                    stroke_opacity=0.6,
                )
                self.add(line)

        # Animate all connections appearing
        all_lines = VGroup(*[m for m in self.mobjects if isinstance(m, Line)])
        self.play(
            LaggedStart(*[Create(l) for l in all_lines], lag_ratio=0.03), run_time=2.0
        )

        # Narration
        narration = Text(
            "Data flows through layers, each transforming it step by step.",
            font_size=26,
            color="#a6adc8",
        )
        narration.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(narration, shift=UP * 0.3), run_time=1.5)
        self.wait(2)
        # --- Scene 2: Forward Pass & Loss Calculation ---
        # Color palette
        accent_1 = "#89b4fa"
        accent_2 = "#fab387"
        accent_3 = "#f38ba8"
        accent_4 = "#a6e3a1"
        accent_5 = "#94e2d5"
        bg_color = "#181825"

        self.camera.background_color = bg_color

        # 1. Create the NumberLine for predictions
        prediction_line = NumberLine(
            x_range=[0, 10, 1],
            length=8,
            color=accent_1,
            include_numbers=True,
            numbers_to_include=[0, 2, 4, 6, 8, 10],
        ).shift(UP * 2)

        # Add a label for the prediction line
        prediction_label = Text("Prediction", font_size=24, color=accent_1)
        prediction_label.next_to(prediction_line, LEFT, buff=0.3)

        # 2. Create target dot (at position 7 on the number line)
        target_point = prediction_line.n2p(7)
        target_dot = Dot(point=target_point, radius=0.12, color=accent_4)
        target_label = Text("Target", font_size=20, color=accent_4)
        target_label.next_to(target_dot, UP, buff=0.2)

        # 3. Create prediction dot (at position 3 on the number line)
        pred_point = prediction_line.n2p(3)
        prediction_dot = Dot(point=pred_point, radius=0.12, color=accent_1)
        pred_label = Text("Pred", font_size=20, color=accent_1)
        pred_label.next_to(prediction_dot, UP, buff=0.2)

        # 4. Create loss brace between prediction and target
        loss_brace = BraceBetweenPoints(
            pred_point, target_point, direction=DOWN, color=accent_3
        )

        # Create the text manually to avoid font_size kwarg error
        loss_text = Text("Loss (Error)", font_size=22, color=accent_3)
        loss_text.next_to(loss_brace, DOWN, buff=0.1)

        # 5. Create loss equation
        loss_eq = MathTex(
            r"L = (y - \hat{y})^2",
            font_size=40,
            color=accent_3,
        ).shift(DOWN * 2.5)

        # Highlight parts of equation
        loss_eq.set_color_by_tex(r"\hat{y}", accent_1)
        loss_eq.set_color_by_tex("y", accent_4)

        # Add a subtle background rectangle behind the equation
        eq_bg = BackgroundRectangle(
            loss_eq, color=bg_color, fill_opacity=0.8, buff=0.15
        )

        # ===== ANIMATION SEQUENCE =====

        # 1. Show the prediction line
        self.play(Create(prediction_line), run_time=1.0)
        self.play(FadeIn(prediction_label), run_time=0.5)

        # 2. Show the target dot
        self.play(FadeIn(target_dot, shift=DOWN * 0.3), run_time=0.8)
        self.play(FadeIn(target_label), run_time=0.7)

        # 3. Show the prediction dot
        self.play(FadeIn(prediction_dot, shift=DOWN * 0.3), run_time=0.8)
        self.play(FadeIn(pred_label), run_time=0.7)

        # 4. Show loss brace highlighting the difference
        self.play(GrowFromCenter(loss_brace), run_time=1.2)
        self.play(FadeIn(loss_text, shift=UP * 0.2), run_time=0.8)

        # Brief pause
        self.wait(0.5)

        # 5. Show the loss equation
        self.play(FadeIn(eq_bg), run_time=0.5)
        self.play(Write(loss_eq), run_time=2.0)

        # 6. Indicate the connection - highlight dots
        self.play(
            Indicate(prediction_dot, color=accent_1, scale_factor=1.5),
            run_time=0.75,
        )
        self.play(
            Indicate(target_dot, color=accent_4, scale_factor=1.5),
            run_time=0.75,
        )

        # 7. Final wait
        self.wait(2.0)
        # --- Scene 3: The Goal of Learning ---
        # Define colors based on style guidelines
        bg_color = "#181825"
        target_color = "#585b70"
        min_loss_color = "#a6e3a1"
        error_color = "#f38ba8"
        text_color = "#cdd6f4"

        # Background
        self.camera.background_color = bg_color

        # 1. Target Construction
        target_background = Circle(
            radius=2.5, color=target_color, stroke_width=4
        ).move_to(ORIGIN)

        # Create concentric rings for depth
        # Using set_fill to handle opacity correctly
        ring1 = Circle(radius=2.0, color=target_color, stroke_width=2).set_fill(
            opacity=0
        )
        ring2 = Circle(radius=1.5, color=target_color, stroke_width=2).set_fill(
            opacity=0
        )
        ring3 = Circle(radius=1.0, color=target_color, stroke_width=2).set_fill(
            opacity=0
        )

        # Target center with glow
        target_center = Dot(point=ORIGIN, radius=0.2, color=min_loss_color)
        target_center.set_z_index(1)

        # Add glow effect around center
        glow_circle = Circle(radius=0.4, color=min_loss_color, stroke_width=0).set_fill(
            min_loss_color, opacity=0.3
        )

        # Build target structure
        self.play(Create(target_background), run_time=1.0)
        self.play(
            Create(ring1),
            Create(ring2),
            Create(ring3),
            FadeIn(glow_circle),
            FadeIn(target_center),
            run_time=1.5,
        )

        # Add label for center
        center_label = Text("Min Loss", font_size=20, color=min_loss_color)
        center_label.next_to(target_center, DOWN, buff=0.3)
        self.play(Write(center_label), run_time=0.5)

        # 2. Current Error Visualization
        # Arrow hitting outer ring
        current_error_start = ORIGIN + 3.5 * UP + 2.5 * RIGHT
        current_error_end = ORIGIN + 2 * UP + 1.5 * RIGHT

        current_error_arrow = Arrow(
            start=current_error_start,
            end=current_error_end,
            color=error_color,
            stroke_width=3,
            buff=0,
        )

        # Label for current error
        error_label = Text("Current Error", font_size=24, color=error_color)
        error_label.next_to(current_error_arrow, RIGHT, buff=0.2)

        self.play(GrowArrow(current_error_arrow), run_time=1.0)
        self.play(Write(error_label), run_time=1.5)

        # 3. Goal Visualization
        # Arrow hitting closer to center
        goal_start = ORIGIN + 2 * UP + 0.8 * RIGHT
        goal_end = ORIGIN + 0.5 * UP + 0.3 * RIGHT

        goal_arrow = Arrow(
            start=goal_start, end=goal_end, color=min_loss_color, stroke_width=3, buff=0
        )

        # Label for goal
        goal_label = Text("Goal", font_size=24, color=min_loss_color)
        goal_label.next_to(goal_arrow, LEFT, buff=0.2)

        self.play(GrowArrow(goal_arrow), run_time=1.0)
        self.play(Write(goal_label), run_time=1.5)

        # 4. Narration
        narration_text = Text(
            "The goal of training is to minimize the loss.\nWe need to find adjustments that move predictions closer to the target.",
            font_size=24,
            color=text_color,
        )
        narration_text.to_edge(DOWN, buff=0.5)

        self.play(Write(narration_text), run_time=3.0)
        self.wait(0.5)
        # --- Scene 4: The Chain Rule Foundation ---
        self.clear()

        # Define colors from Catppuccin Mocha palette
        bg_color = "#181825"
        text_color = "#cdd6f4"
        blue = "#89b4fa"
        peach = "#fab387"
        green = "#a6e3a1"

        # Background
        self.camera.background_color = bg_color

        # Gear helper: creates a circle body with rectangular teeth
        def create_gear(radius, color, num_teeth=12):
            gear_body = Circle(
                radius=radius,
                color=color,
                stroke_width=2,
                fill_opacity=0.15,
                fill_color=color,
            )
            teeth = VGroup()
            for i in range(num_teeth):
                angle = i * (TAU / num_teeth)
                # Tooth base points on circle
                p1 = np.array(
                    [np.cos(angle - 0.15) * radius, np.sin(angle - 0.15) * radius, 0]
                )
                p2 = np.array(
                    [np.cos(angle + 0.15) * radius, np.sin(angle + 0.15) * radius, 0]
                )
                # Tooth tip points slightly outside circle
                p3 = np.array(
                    [
                        np.cos(angle + 0.1) * (radius + 0.15),
                        np.sin(angle + 0.1) * (radius + 0.15),
                        0,
                    ]
                )
                p4 = np.array(
                    [
                        np.cos(angle - 0.1) * (radius + 0.15),
                        np.sin(angle - 0.1) * (radius + 0.15),
                        0,
                    ]
                )
                tooth = Polygon(
                    p1,
                    p4,
                    p3,
                    p2,
                    color=color,
                    fill_opacity=0.15,
                    fill_color=color,
                    stroke_width=2,
                )
                teeth.add(tooth)
            return VGroup(gear_body, teeth)

        # Create three interlocking gears
        gear_x = create_gear(1.0, blue, num_teeth=10)
        gear_y = create_gear(1.0, peach, num_teeth=10)
        gear_z = create_gear(1.0, green, num_teeth=10)

        # Position: triangle arrangement (y on top, x bottom-left, z bottom-right)
        gear_y.move_to(UP * 0.6)
        gear_x.move_to(LEFT * 1.4 + DOWN * 0.6)
        gear_z.move_to(RIGHT * 1.4 + DOWN * 0.6)

        # Create gear labels
        label_x = Text("x", color=blue, font_size=40, weight=BOLD).move_to(
            gear_x.get_center()
        )
        label_y = Text("y", color=peach, font_size=40, weight=BOLD).move_to(
            gear_y.get_center()
        )
        label_z = Text("z", color=green, font_size=40, weight=BOLD).move_to(
            gear_z.get_center()
        )

        # Chain rule equation
        chain_rule_eq = MathTex(
            r"\frac{dz}{dx} = \frac{dz}{dy} \cdot \frac{dy}{dx}",
            color=text_color,
            font_size=40,
        ).move_to(DOWN * 2.5)

        # ===== ANIMATION SEQUENCE (total: 12.5s) =====

        # Phase 1: Fade in gears with stagger (3.0s)
        self.play(
            LaggedStart(
                FadeIn(gear_x, shift=RIGHT * 0.5),
                FadeIn(gear_y, shift=DOWN * 0.5),
                FadeIn(gear_z, shift=LEFT * 0.5),
                lag_ratio=0.5,
            ),
            run_time=3,
        )

        # Phase 2: Add labels & rotate gears to show interlocking motion (4.0s)
        self.play(FadeIn(label_x), FadeIn(label_y), FadeIn(label_z), run_time=1)
        self.play(
            Rotate(
                gear_x, angle=-PI, about_point=gear_x.get_center(), rate_func=linear
            ),
            Rotate(gear_y, angle=PI, about_point=gear_y.get_center(), rate_func=linear),
            Rotate(
                gear_z, angle=-PI, about_point=gear_z.get_center(), rate_func=linear
            ),
            run_time=3,
        )

        # Phase 3: Show chain rule equation (3.0s)
        self.play(Write(chain_rule_eq), run_time=3)

        # Phase 4: Highlight equation and pulse gears (2.5s)
        self.play(
            Circumscribe(chain_rule_eq, color=peach, time_width=2.0),
            Flash(chain_rule_eq, color=peach, line_length=0.2, num_lines=8),
            run_time=2.5,
        )

        # Total: 3 + 1 + 3 + 3 + 2.5 = 12.5s
        # --- Scene 5: Error Gradient at the Output ---
        self.clear()

        # ── Colors ──
        bg_color = "#181825"
        loss_color = "#f38ba8"
        output_color = "#89b4fa"
        gradient_color = "#a6e3a1"
        text_color = "#cdd6f4"
        highlight_color = "#fab387"

        self.camera.background_color = bg_color

        # ── Title ──
        title = Text(
            "Error Gradient at the Output",
            font_size=36,
            color=text_color,
        ).to_edge(UP, buff=0.5)

        # ── Nodes ──
        output_node = Circle(
            radius=0.5,
            color=output_color,
            fill_opacity=0.3,
            stroke_width=2.5,
        ).move_to(LEFT * 1.5)

        output_label = Text(
            "Output\nŷ",
            font_size=22,
            color=output_color,
        ).move_to(output_node.get_center())

        loss_node = Circle(
            radius=0.5,
            color=loss_color,
            fill_opacity=0.3,
            stroke_width=2.5,
        ).move_to(RIGHT * 1.5)

        loss_label = Text(
            "Loss\nL",
            font_size=22,
            color=loss_color,
        ).move_to(loss_node.get_center())

        # ── Connection line (forward pass direction) ──
        forward_line = Arrow(
            start=output_node.get_right(),
            end=loss_node.get_left(),
            color=output_color,
            stroke_width=2,
            buff=0.05,
            max_tip_length_to_length_ratio=0.15,
        )

        forward_label = Text(
            "forward →",
            font_size=18,
            color=output_color,
        ).next_to(forward_line, UP, buff=0.15)

        # ── Gradient arrow (backward direction) ──
        gradient_arrow = Arrow(
            start=loss_node.get_bottom(),
            end=output_node.get_bottom(),
            color=gradient_color,
            stroke_width=5,
            buff=0.05,
            max_tip_length_to_length_ratio=0.12,
        ).shift(DOWN * 0.6)

        gradient_eq = MathTex(
            r"\frac{\partial L}{\partial \hat{y}}",
            font_size=36,
            color=gradient_color,
        ).next_to(gradient_arrow, DOWN, buff=0.2)

        gradient_label = Text(
            "Error Gradient",
            font_size=24,
            color=gradient_color,
        ).next_to(gradient_eq, DOWN, buff=0.15)

        # ── Glow rings around gradient arrow ──
        glow1 = Ellipse(
            width=gradient_arrow.get_width() + 0.4,
            height=0.5,
            color=gradient_color,
            fill_opacity=0.08,
            stroke_width=0,
        ).move_to(gradient_arrow.get_center())

        glow2 = Ellipse(
            width=gradient_arrow.get_width() + 0.8,
            height=0.7,
            color=gradient_color,
            fill_opacity=0.04,
            stroke_width=0,
        ).move_to(gradient_arrow.get_center())

        # ── Surface visualization (simplified hill) ──
        surface_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 3, 1],
            x_length=3.5,
            y_length=2.0,
            tips=False,
            axis_config={"color": text_color, "stroke_width": 1.5},
        ).move_to(DOWN * 3.2)

        # Simple curve representing loss surface
        loss_curve = surface_axes.plot(
            lambda x: 0.3 * (x - 2) ** 2 + 0.5,
            x_range=[0.3, 3.7],
            color=loss_color,
            stroke_width=2.5,
        )

        # Current point on the curve
        current_x = 3.0
        current_y = 0.3 * (current_x - 2) ** 2 + 0.5
        current_point = Dot(
            surface_axes.coords_to_point(current_x, current_y),
            radius=0.1,
            color=highlight_color,
        )

        # Gradient direction arrow on the curve
        surface_gradient_arrow = Arrow(
            start=surface_axes.coords_to_point(current_x, current_y),
            end=surface_axes.coords_to_point(current_x - 1.0, current_y - 0.3),
            color=gradient_color,
            stroke_width=3,
            buff=0.0,
            max_tip_length_to_length_ratio=0.2,
        )

        # Axis labels
        x_label = Text("parameters", font_size=16, color=text_color).next_to(
            surface_axes, DOWN, buff=0.15
        )
        y_label = Text("loss", font_size=16, color=text_color).next_to(
            surface_axes, LEFT, buff=0.15
        )

        surface_label = Text(
            "Steepest descent on loss surface",
            font_size=18,
            color=gradient_color,
        ).next_to(surface_axes, RIGHT, buff=0.3)

        # ── Narrative text at bottom ──
        narrative = Text(
            "The gradient tells us which direction\nreduces the error the most.",
            font_size=20,
            color=text_color,
        ).to_edge(DOWN, buff=0.35)

        # ══════════════════════════════════════════
        #  ANIMATION SEQUENCE  (total = 13.5s)
        # ══════════════════════════════════════════

        # 1. Title fade in (1.0s)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.0)

        # 2. Show output node (0.8s)
        self.play(
            GrowFromCenter(output_node),
            FadeIn(output_label),
            run_time=0.8,
        )

        # 3. Show forward connection (1.0s)
        self.play(
            GrowFromCenter(loss_node),
            FadeIn(loss_label),
            Create(forward_line),
            FadeIn(forward_label, shift=LEFT * 0.2),
            run_time=1.0,
        )

        # 4. Brief pause to establish the forward pass (0.5s)
        self.wait(0.5)

        # 5. Indicate the loss to draw attention (0.8s)
        self.play(
            Indicate(loss_node, color=highlight_color, scale_factor=1.3),
            run_time=0.8,
        )

        # 6. Gradient arrow appears with glow (1.2s)
        self.play(
            FadeIn(glow2),
            FadeIn(glow1),
            Create(gradient_arrow),
            run_time=1.2,
        )

        # 7. Gradient equation + label (0.8s)
        self.play(
            FadeIn(gradient_eq, shift=UP * 0.2),
            FadeIn(gradient_label, shift=UP * 0.2),
            run_time=0.8,
        )

        # 8. Gradient label highlight (0.8s)
        self.play(
            Indicate(gradient_eq, color=gradient_color, scale_factor=1.2),
            run_time=0.8,
        )

        # 9. Show axes (0.8s)
        self.play(
            Create(surface_axes),
            FadeIn(x_label),
            FadeIn(y_label),
            run_time=0.8,
        )

        # 10. Show loss curve (0.7s)
        self.play(
            Create(loss_curve),
            run_time=0.7,
        )

        # 11. Current point + gradient arrow on surface (1.2s)
        self.play(
            FadeIn(current_point, scale=2),
            Create(surface_gradient_arrow),
            FadeIn(surface_label, shift=LEFT * 0.2),
            run_time=1.2,
        )

        # 12. Show narrative (1.0s)
        self.play(
            FadeIn(narrative, shift=UP * 0.2),
            run_time=1.0,
        )

        # 13. Pulsing glow effect on gradient arrow (1.5s)
        self.play(
            glow1.animate.set_fill(opacity=0.15).scale(1.1),
            glow2.animate.set_fill(opacity=0.08).scale(1.05),
            run_time=0.75,
            rate_func=there_and_back,
        )
        self.play(
            glow1.animate.set_fill(opacity=0.12).scale(1.05),
            glow2.animate.set_fill(opacity=0.06).scale(1.02),
            run_time=0.75,
            rate_func=there_and_back,
        )

        # 14. Final hold (0.9s)
        self.wait(0.9)
        # --- Scene 6: Propagating Gradients Backward ---
        self.clear()

        # Color palette
        bg_color = "#181825"
        gradient_green = "#a6e3a1"
        hidden_orange = "#fab387"
        output_blue = "#89b4fa"
        input_blue = "#89b4fa"
        text_color = "#cdd6f4"
        connection_color = "#585b70"

        # Set background color
        self.camera.background_color = bg_color

        # ---- Title ----
        title = Text(
            "Propagating Gradients Backward",
            font_size=32,
            color=gradient_green,
        ).to_edge(UP, buff=0.35)

        # ---- Define network nodes ----
        # Input layer nodes (far left)
        input_nodes = (
            VGroup(
                *[
                    Circle(
                        radius=0.35, color=input_blue, fill_opacity=0.3, stroke_width=2
                    )
                    for _ in range(3)
                ]
            )
            .arrange(DOWN, buff=0.6)
            .shift(LEFT * 4.5)
        )

        input_labels = VGroup(
            *[
                Text(f"x{i + 1}", font_size=20, color=text_color).move_to(node)
                for i, node in enumerate(input_nodes)
            ]
        )

        # Hidden layer nodes (middle-left)
        hidden_node_1 = Circle(
            radius=0.4, color=hidden_orange, fill_opacity=0.3, stroke_width=2
        )
        hidden_node_2 = Circle(
            radius=0.4, color=hidden_orange, fill_opacity=0.3, stroke_width=2
        )
        hidden_nodes = (
            VGroup(hidden_node_1, hidden_node_2)
            .arrange(DOWN, buff=0.8)
            .shift(LEFT * 1.5)
        )

        hidden_labels = VGroup(
            Text("h1", font_size=22, color=text_color).move_to(hidden_node_1),
            Text("h2", font_size=22, color=text_color).move_to(hidden_node_2),
        )

        # Output node (middle-right)
        output_node = Circle(
            radius=0.45, color=output_blue, fill_opacity=0.3, stroke_width=2
        ).shift(RIGHT * 2)
        output_label = Text("y_hat", font_size=22, color=text_color).move_to(
            output_node
        )

        # Error/loss box (far right)
        error_box = RoundedRectangle(
            corner_radius=0.15,
            width=1.2,
            height=0.7,
            color=gradient_green,
            fill_opacity=0.2,
            stroke_width=2,
        ).shift(RIGHT * 4.5)
        error_label = Text("Loss", font_size=20, color=gradient_green).move_to(
            error_box
        )

        # ---- Connection lines (forward pass style, dim) ----
        input_to_hidden_lines = VGroup()
        for inp_node in input_nodes:
            for hid_node in hidden_nodes:
                line = Line(
                    inp_node.get_right(),
                    hid_node.get_left(),
                    color=connection_color,
                    stroke_width=1.5,
                    stroke_opacity=0.5,
                )
                input_to_hidden_lines.add(line)

        hidden_to_output_lines = VGroup()
        for hid_node in hidden_nodes:
            line = Line(
                hid_node.get_right(),
                output_node.get_left(),
                color=connection_color,
                stroke_width=1.5,
                stroke_opacity=0.5,
            )
            hidden_to_output_lines.add(line)

        output_to_error_line = Line(
            output_node.get_right(),
            error_box.get_left(),
            color=connection_color,
            stroke_width=1.5,
            stroke_opacity=0.5,
        )

        # ---- Layer labels ----
        layer_labels = VGroup(
            Text("Input", font_size=18, color=BLUE_C).move_to(UP * 2.5 + LEFT * 4.5),
            Text("Hidden", font_size=18, color=hidden_orange).move_to(
                UP * 2.5 + LEFT * 1.5
            ),
            Text("Output", font_size=18, color=output_blue).move_to(
                UP * 2.5 + RIGHT * 2
            ),
            Text("Loss", font_size=18, color=gradient_green).move_to(
                UP * 2.5 + RIGHT * 4.5
            ),
        )

        # ============ ANIMATION SEQUENCE ============
        # Total: 11.5 seconds

        # Phase 1: Draw title and network structure (0–3.0s)
        self.play(Write(title), run_time=0.8)
        self.play(
            FadeIn(input_nodes, shift=RIGHT * 0.3), FadeIn(input_labels), run_time=0.5
        )
        self.play(Create(input_to_hidden_lines), run_time=0.5)
        self.play(
            FadeIn(hidden_nodes, shift=RIGHT * 0.3), FadeIn(hidden_labels), run_time=0.4
        )
        self.play(
            Create(hidden_to_output_lines),
            FadeIn(output_node, shift=RIGHT * 0.3),
            FadeIn(output_label),
            run_time=0.4,
        )
        self.play(
            Create(output_to_error_line),
            FadeIn(error_box, shift=RIGHT * 0.3),
            FadeIn(error_label),
            FadeIn(layer_labels),
            run_time=0.4,
        )

        # Phase 2: Show output gradient arrow (3.0–5.0s)
        output_gradient = Arrow(
            start=error_box.get_left() + LEFT * 0.1,
            end=output_node.get_right() + RIGHT * 0.1,
            color=gradient_green,
            stroke_width=3,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        gradient_label = Text("dL/dy", font_size=18, color=gradient_green)
        gradient_label.next_to(output_gradient, UP, buff=0.15)

        self.play(GrowArrow(output_gradient), FadeIn(gradient_label), run_time=1.0)
        self.wait(1.0)

        # Phase 3: Gradient splits to hidden layer (5.0–8.5s)
        self.play(FadeOut(output_gradient), FadeOut(gradient_label), run_time=0.4)

        split_arrow_1 = Arrow(
            start=output_node.get_left() + LEFT * 0.1,
            end=hidden_node_1.get_right() + RIGHT * 0.1,
            color=gradient_green,
            stroke_width=2.5,
            buff=0,
            max_tip_length_to_length_ratio=0.12,
        )
        split_arrow_2 = Arrow(
            start=output_node.get_left() + LEFT * 0.1,
            end=hidden_node_2.get_right() + RIGHT * 0.1,
            color=gradient_green,
            stroke_width=2.5,
            buff=0,
            max_tip_length_to_length_ratio=0.12,
        )

        split_label_1 = Text("dL/dh1", font_size=16, color=gradient_green)
        split_label_1.next_to(split_arrow_1, UP, buff=0.1)
        split_label_2 = Text("dL/dh2", font_size=16, color=gradient_green)
        split_label_2.next_to(split_arrow_2, DOWN, buff=0.1)

        self.play(GrowArrow(split_arrow_1), GrowArrow(split_arrow_2), run_time=1.0)
        self.play(
            FadeIn(split_label_1),
            FadeIn(split_label_2),
            Indicate(hidden_node_1, color=gradient_green, scale_factor=1.15),
            run_time=0.6,
        )
        self.play(
            Indicate(hidden_node_2, color=gradient_green, scale_factor=1.15),
            run_time=0.5,
        )
        self.wait(1.0)

        # Phase 4: Gradients propagate to input layer (8.5–10.5s)
        input_grad_arrows = VGroup()
        for hid_node in hidden_nodes:
            for inp_node in input_nodes:
                arrow = Arrow(
                    start=hid_node.get_left() + LEFT * 0.1,
                    end=inp_node.get_right() + RIGHT * 0.1,
                    color=gradient_green,
                    stroke_width=1.8,
                    buff=0,
                    max_tip_length_to_length_ratio=0.1,
                    stroke_opacity=0.8,
                )
                input_grad_arrows.add(arrow)

        self.play(
            LaggedStart(*[GrowArrow(a) for a in input_grad_arrows], lag_ratio=0.12),
            run_time=1.5,
        )
        self.play(
            *[Indicate(n, color=gradient_green, scale_factor=1.1) for n in input_nodes],
            run_time=0.5,
        )

        # Phase 5: Contribution text (10.5–11.5s)
        contribution_text = Text(
            "Each connection carries its share of the gradient",
            font_size=22,
            color=text_color,
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(contribution_text, shift=UP * 0.2), run_time=0.6)
        self.wait(0.4)
        # --- Scene 7: Computing Weight Gradients ---
        # Colors from Catppuccin Mocha palette
        BG = "#181825"
        NEURON_IN = "#fab387"
        NEURON_OUT = "#89b4fa"
        LINE_COLOR = "#585b70"
        GRAD_COLOR = "#a6e3a1"
        LABEL_COLOR = "#cdd6f4"
        ACCENT = "#f38ba8"

        self.camera.background_color = BG

        # === 1. Build the neurons and connection ===
        neuron_left = Circle(
            radius=0.5, color=NEURON_IN, fill_opacity=0.15, stroke_width=2.5
        ).move_to(LEFT * 2)

        neuron_right = Circle(
            radius=0.5, color=NEURON_OUT, fill_opacity=0.15, stroke_width=2.5
        ).move_to(RIGHT * 2)

        label_left = Text("Input", font_size=24, color=LABEL_COLOR).next_to(
            neuron_left, DOWN, buff=0.35
        )
        label_right = Text("Output", font_size=24, color=LABEL_COLOR).next_to(
            neuron_right, DOWN, buff=0.35
        )

        weight_line = Line(
            neuron_left.get_right(),
            neuron_right.get_left(),
            color=LINE_COLOR,
            stroke_width=3,
        )

        weight_label = MathTex("w", font_size=30, color=LABEL_COLOR).next_to(
            weight_line, DOWN, buff=0.3
        )

        # === 2. Gradient meter elements ===
        gradient_value = ValueTracker(0.0)

        gradient_display = always_redraw(
            lambda: DecimalNumber(
                gradient_value.get_value(),
                num_decimal_places=3,
                font_size=28,
                color=GRAD_COLOR,
            ).next_to(weight_line, UP, buff=0.5)
        )

        gradient_tex = MathTex(
            r"\frac{\partial L}{\partial w}", font_size=26, color=ACCENT
        ).next_to(weight_line, UP, buff=1.0)

        # Gauge bar background
        gauge_bg = Rectangle(
            width=2.0, height=0.15, color=LINE_COLOR, fill_opacity=0.3, stroke_width=1
        ).next_to(weight_line, UP, buff=0.65)

        # Gauge fill (animated with ValueTracker)
        gauge_fill = always_redraw(
            lambda: Rectangle(
                width=max(0.01, abs(gradient_value.get_value()) / 1.5 * 2.0),
                height=0.15,
                color=GRAD_COLOR,
                fill_opacity=0.7,
                stroke_width=0,
            ).move_to(gauge_bg.get_center())
        )

        # === 3. Animation sequence ===
        # Phase 1: Show neurons and connection (0–3s)
        self.play(
            FadeIn(neuron_left, shift=LEFT * 0.3),
            FadeIn(neuron_right, shift=RIGHT * 0.3),
            run_time=1.0,
        )
        self.play(
            Create(weight_line), FadeIn(label_left), FadeIn(label_right), run_time=1.0
        )
        self.play(FadeIn(weight_label), run_time=0.5)
        self.wait(0.5)

        # Phase 2: Highlight connection and show gradient meter (3–6s)
        self.play(
            weight_line.animate.set_color(GRAD_COLOR).set_stroke(width=5), run_time=0.8
        )
        self.play(FadeIn(gauge_bg), Write(gradient_tex), run_time=1.0)
        self.play(FadeIn(gradient_display), FadeIn(gauge_fill), run_time=0.8)
        self.wait(0.4)

        # Phase 3: Animate gradient computation (6–10.2s)
        self.play(
            gradient_value.animate.set_value(0.742), rate_func=smooth, run_time=2.0
        )
        self.play(
            Indicate(gradient_display, color=GRAD_COLOR, scale_factor=1.3), run_time=0.8
        )

        # Adjustment direction hint
        arrow_hint = Arrow(
            gauge_bg.get_right(),
            gauge_bg.get_right() + RIGHT * 0.6 + UP * 0.3,
            color=GRAD_COLOR,
            buff=0.05,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.3,
        )
        adjust_text = Text("adjust w ↓", font_size=20, color=GRAD_COLOR).next_to(
            arrow_hint, RIGHT, buff=0.1
        )

        self.play(GrowFromCenter(arrow_hint), FadeIn(adjust_text), run_time=1.2)
        self.wait(0.2)

        # Phase 4: Pulse and hold (10.2–12s)
        self.play(
            Circumscribe(gauge_bg, color=GRAD_COLOR, time_width=1.5, stroke_width=2),
            run_time=1.0,
        )
        self.wait(0.8)
        # --- Scene 8: Updating Weights with Learning Rate ---
        # Background
        self.camera.background_color = "#181825"

        # Title
        title = Text(
            "Updating Weights with Learning Rate", font_size=42, color="#89b4fa"
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        # Equation components
        w_old = MathTex("w_{old}", font_size=48, color="#89b4fa")
        minus = MathTex("-", font_size=48, color="#cdd6f4")
        eta = MathTex("\\eta", font_size=48, color="#fab387")
        grad = MathTex(
            "\\frac{\\partial L}{\\partial w}", font_size=48, color="#a6e3a1"
        )
        equals = MathTex("=", font_size=48, color="#cdd6f4")
        w_new = MathTex("w_{new}", font_size=48, color="#89b4fa")

        # Arrange equation
        equation = VGroup(w_old, minus, eta, grad, equals, w_new).arrange(
            RIGHT, buff=0.2
        )
        equation.move_to(ORIGIN)

        # Build equation piece by piece
        self.play(Write(w_old))
        self.wait(0.5)
        self.play(Write(minus))
        self.play(Write(eta))
        self.play(Write(grad))
        self.play(Write(equals))
        self.play(Write(w_new))
        self.wait(0.5)

        # Labels with arrows
        current_label = Text("Current Weight", font_size=28, color="#cdd6f4")
        lr_label = Text("Learning Rate", font_size=28, color="#cdd6f4")
        gradient_label = Text("Gradient", font_size=28, color="#cdd6f4")
        new_label = Text("Updated Weight", font_size=28, color="#cdd6f4")

        # Position labels below
        current_label.next_to(w_old, DOWN, buff=0.8)
        lr_label.next_to(eta, DOWN, buff=0.8)
        gradient_label.next_to(grad, DOWN, buff=0.8)
        new_label.next_to(w_new, DOWN, buff=0.8)

        # Arrows
        arrow1 = Arrow(
            current_label.get_top(),
            w_old.get_bottom(),
            buff=0.1,
            color="#cdd6f4",
            stroke_width=2,
        )
        arrow2 = Arrow(
            lr_label.get_top(),
            eta.get_bottom(),
            buff=0.1,
            color="#cdd6f4",
            stroke_width=2,
        )
        arrow3 = Arrow(
            gradient_label.get_top(),
            grad.get_bottom(),
            buff=0.1,
            color="#cdd6f4",
            stroke_width=2,
        )
        arrow4 = Arrow(
            new_label.get_top(),
            w_new.get_bottom(),
            buff=0.1,
            color="#cdd6f4",
            stroke_width=2,
        )

        # Show labels and arrows
        self.play(FadeIn(current_label), GrowArrow(arrow1))
        self.play(FadeIn(lr_label), GrowArrow(arrow2))
        self.play(FadeIn(gradient_label), GrowArrow(arrow3))
        self.play(FadeIn(new_label), GrowArrow(arrow4))
        self.wait(0.5)

        # Explanation text
        explanation = Text(
            "We update each weight by subtracting a fraction of its gradient.\n"
            "The learning rate controls the step size for stable learning.",
            font_size=24,
            color="#cdd6f4",
        )
        explanation.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(explanation))
        self.wait(1)

        # Highlight learning rate
        lr_box = SurroundingRectangle(eta, color="#fab387", buff=0.1)
        self.play(Create(lr_box))
        self.play(
            Indicate(eta, color="#fab387", scale_factor=1.3),
        )
        self.wait(1)

        # Fade out
        self.play(
            FadeOut(title),
            FadeOut(equation),
            FadeOut(current_label),
            FadeOut(lr_label),
            FadeOut(gradient_label),
            FadeOut(new_label),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(arrow3),
            FadeOut(arrow4),
            FadeOut(explanation),
            FadeOut(lr_box),
        )
        self.wait(0.5)
        # --- Scene 9: The Learning Loop ---
        # Background
        self.camera.background_color = "#181825"

        # Title
        title = Text("The Learning Loop", font_size=36, color="#cdd6f4").to_edge(
            UP, buff=0.4
        )
        self.play(FadeIn(title), run_time=0.5)

        # 1. Objects
        c_forward = "#89b4fa"
        c_loss = "#f38ba8"
        c_backward = "#a6e3a1"
        c_update = "#fab387"
        c_arrow = "#585b70"

        forward_circle = Circle(
            radius=0.65, color=c_forward, fill_opacity=0.15, stroke_width=2.5
        )
        forward_label = Text("Forward\nPass", font_size=22, color=c_forward).move_to(
            forward_circle
        )
        forward_node = VGroup(forward_circle, forward_label).move_to(UP * 1.5)

        loss_circle = Circle(
            radius=0.65, color=c_loss, fill_opacity=0.15, stroke_width=2.5
        )
        loss_label = Text("Loss", font_size=22, color=c_loss).move_to(loss_circle)
        loss_node = VGroup(loss_circle, loss_label).move_to(RIGHT * 3)

        backward_circle = Circle(
            radius=0.65, color=c_backward, fill_opacity=0.15, stroke_width=2.5
        )
        backward_label = Text("Backward\nPass", font_size=22, color=c_backward).move_to(
            backward_circle
        )
        backward_node = VGroup(backward_circle, backward_label).move_to(DOWN * 1.5)

        update_circle = Circle(
            radius=0.65, color=c_update, fill_opacity=0.15, stroke_width=2.5
        )
        update_label = Text("Update\nWeights", font_size=20, color=c_update).move_to(
            update_circle
        )
        update_node = VGroup(update_circle, update_label).move_to(LEFT * 3)

        # 2. Arrows
        arrow_1 = Arrow(
            forward_circle.get_right() + RIGHT * 0.05,
            loss_circle.get_left() + LEFT * 0.05,
            buff=0.15,
            color=c_arrow,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )
        arrow_2 = Arrow(
            loss_circle.get_bottom() + DOWN * 0.05,
            backward_circle.get_right() + RIGHT * 0.05,
            buff=0.15,
            color=c_arrow,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )
        arrow_3 = Arrow(
            backward_circle.get_left() + LEFT * 0.05,
            update_circle.get_bottom() + DOWN * 0.05,
            buff=0.15,
            color=c_arrow,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )
        arrow_4 = Arrow(
            update_circle.get_top() + UP * 0.05,
            forward_circle.get_left() + LEFT * 0.05,
            buff=0.15,
            color=c_arrow,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )

        # 3. Animations (Total: 13s)

        # Phase 1: Title + Nodes appear (3s)
        self.play(
            LaggedStart(
                FadeIn(forward_node, scale=0.8),
                FadeIn(loss_node, scale=0.8),
                FadeIn(backward_node, scale=0.8),
                FadeIn(update_node, scale=0.8),
                lag_ratio=0.3,
            ),
            run_time=3.0,
        )

        # Phase 2: Arrows draw the cycle (6s)
        self.play(GrowArrow(arrow_1), run_time=1.5)
        self.play(GrowArrow(arrow_2), run_time=1.5)
        self.play(GrowArrow(arrow_3), run_time=1.5)
        self.play(GrowArrow(arrow_4), run_time=1.5)

        # Phase 3: Highlight the loop (2s)
        cycle_group = VGroup(
            forward_node,
            loss_node,
            backward_node,
            update_node,
            arrow_1,
            arrow_2,
            arrow_3,
            arrow_4,
        )
        self.play(Indicate(cycle_group, color=YELLOW, scale_factor=1.03), run_time=2.0)

        # Phase 4: Hold for narration (2s)
        self.wait(2.0)
