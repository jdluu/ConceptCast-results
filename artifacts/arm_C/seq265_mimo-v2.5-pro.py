import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: The Layered Network ---
        # --- Colors (Catppuccin Mocha) ---
        c_input = "#89B4FA"
        c_hidden = "#A6E3A1"
        c_output = "#CBA6F7"
        c_beam = "#FAB387"

        # --- Background ---
        bg = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-6, 6, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 0.5,
                "stroke_opacity": 0.3,
            },
            axis_config={"stroke_width": 0},
        )
        self.play(FadeIn(bg), run_time=0.6)

        # --- Glass Panes ---
        l1 = Rectangle(
            width=1.5, height=4, color=c_input, fill_opacity=0.1, stroke_width=2
        ).move_to(LEFT * 3)
        l2 = Rectangle(
            width=1.5, height=4, color=c_hidden, fill_opacity=0.1, stroke_width=2
        ).move_to(ORIGIN)
        l3 = Rectangle(
            width=1.5, height=4, color=c_output, fill_opacity=0.1, stroke_width=2
        ).move_to(RIGHT * 3)

        t1 = Text("Input", font_size=20, color=c_input).next_to(l1, DOWN)
        t2 = Text("Hidden", font_size=20, color=c_hidden).next_to(l2, DOWN)
        t3 = Text("Output", font_size=20, color=c_output).next_to(l3, DOWN)

        self.play(
            FadeIn(l1),
            FadeIn(l2),
            FadeIn(l3),
            FadeIn(t1),
            FadeIn(t2),
            FadeIn(t3),
            run_time=1.0,
        )

        # --- Nodes ---
        nodes_1 = VGroup(
            *[
                Dot(
                    l1.get_left() + UP * 1.5 + RIGHT * 0.75 + DOWN * i * 1.0,
                    radius=0.12,
                    color=c_input,
                )
                for i in range(4)
            ]
        )
        nodes_2 = VGroup(
            *[
                Dot(
                    l2.get_left() + UP * 1.5 + RIGHT * 0.75 + DOWN * i * 0.8,
                    radius=0.12,
                    color=c_hidden,
                )
                for i in range(5)
            ]
        )
        nodes_3 = VGroup(
            *[
                Dot(
                    l3.get_left() + UP * 1.5 + RIGHT * 0.75 + DOWN * i * 1.3,
                    radius=0.12,
                    color=c_output,
                )
                for i in range(3)
            ]
        )

        self.play(
            LaggedStart(*[GrowFromCenter(n) for n in nodes_1], lag_ratio=0.1),
            LaggedStart(*[GrowFromCenter(n) for n in nodes_2], lag_ratio=0.1),
            LaggedStart(*[GrowFromCenter(n) for n in nodes_3], lag_ratio=0.1),
            run_time=0.8,
        )

        # --- Connections ---
        lines = VGroup()
        for n1 in nodes_1:
            for n2 in nodes_2:
                lines.add(
                    Line(
                        n1.get_center(),
                        n2.get_center(),
                        stroke_width=0.5,
                        stroke_opacity=0.2,
                        color=c_hidden,
                    )
                )
        for n2 in nodes_2:
            for n3 in nodes_3:
                lines.add(
                    Line(
                        n2.get_center(),
                        n3.get_center(),
                        stroke_width=0.5,
                        stroke_opacity=0.2,
                        color=c_output,
                    )
                )

        self.play(Create(lines), run_time=1.0)

        # --- Data Beam ---
        start_pt = l1.get_left() + LEFT * 2
        end_pt = l3.get_right() + RIGHT * 2

        beam_in = Arrow(start_pt, l1.get_center(), color=c_beam, stroke_width=4, buff=0)
        beam_mid = Arrow(
            l1.get_center(), l3.get_left(), color=c_beam, stroke_width=4, buff=0
        )
        beam_out = Arrow(l3.get_right(), end_pt, color=c_output, stroke_width=4, buff=0)

        self.play(GrowArrow(beam_in), run_time=0.4)
        self.play(GrowArrow(beam_mid), run_time=0.6)

        label_pred = Text("Prediction", font_size=20, color=c_output).next_to(
            beam_out, UP
        )
        self.play(GrowArrow(beam_out), FadeIn(label_pred), run_time=0.3)

        # --- Refraction Effect ---
        arc1 = Arc(
            radius=1.5, start_angle=-PI / 4, angle=PI / 2, color=c_input, stroke_width=3
        ).move_to(l1.get_center())
        arc2 = Arc(
            radius=1.5,
            start_angle=-PI / 4,
            angle=PI / 2,
            color=c_hidden,
            stroke_width=3,
        ).move_to(l2.get_center())
        arc3 = Arc(
            radius=1.5,
            start_angle=-PI / 4,
            angle=PI / 2,
            color=c_output,
            stroke_width=3,
        ).move_to(l3.get_center())

        self.play(
            ShowPassingFlash(arc1),
            ShowPassingFlash(arc2),
            ShowPassingFlash(arc3),
            run_time=1.0,
        )

        # --- Output Glow ---
        self.play(
            l3.animate.set_fill(opacity=0.3),
            nodes_3.animate.set_color(WHITE),
            run_time=1.0,
        )

        self.wait(1.0)
        # --- Scene 2: The Loss Distance ---
        self.clear()

        # Colors (Catppuccin Mocha palette)
        c_line = "#CDD6F4"
        c_pred = "#89B4FA"
        c_true = "#FAB387"
        c_loss = "#F38BA8"

        # 1. Objects
        # NumberLine (prediction space)
        pred_axis = NumberLine(
            x_range=[-3, 3, 1],
            length=10,
            color=c_line,
            include_numbers=True,
            font_size=24,
        )

        # Prediction point (blue dart)
        pred_val = 2.0
        pred_point = Dot(
            point=pred_axis.n2p(pred_val),
            color=c_pred,
            radius=0.12,
        )
        pred_label = Text("Prediction", font_size=24, color=c_pred).next_to(
            pred_point, DOWN, buff=0.2
        )

        # Target point (gold circle with crosshair)
        true_val = -0.5
        target_circle = Circle(
            radius=0.35,
            color=c_true,
            stroke_width=3,
        ).move_to(pred_axis.n2p(true_val))

        target_crosshair = VGroup(
            Line(
                target_circle.get_center() + UP * 0.15,
                target_circle.get_center() + DOWN * 0.15,
                color=c_true,
                stroke_width=2,
            ),
            Line(
                target_circle.get_center() + LEFT * 0.15,
                target_circle.get_center() + RIGHT * 0.15,
                color=c_true,
                stroke_width=2,
            ),
        )
        target_group = VGroup(target_circle, target_crosshair)
        target_label = Text("Target", font_size=24, color=c_true).next_to(
            target_group, DOWN, buff=0.2
        )

        # Loss Brace spanning the distance between prediction and target
        loss_brace = BraceBetweenPoints(
            pred_axis.n2p(pred_val),
            pred_axis.n2p(true_val),
            direction=DOWN,
            color=c_loss,
        )
        # FIX: Create Tex separately and position manually
        # Brace.get_text() was passing font_size to next_to() internally
        loss_text = Tex("Loss", font_size=24).next_to(loss_brace, DOWN, buff=0.1)

        # Loss Arrow (visual indicator above the line)
        loss_arrow = Arrow(
            start=pred_axis.n2p(pred_val) + UP * 0.3,
            end=pred_axis.n2p(true_val) + UP * 0.3,
            color=c_loss,
            stroke_width=4,
            buff=0,
        )

        # 2. Animations (total run_time = 5.0s + 1.0s wait = 6.0s)
        self.play(Create(pred_axis), run_time=1.0)

        self.play(
            FadeIn(target_group, shift=DOWN),
            FadeIn(target_label),
            run_time=1.0,
        )

        self.play(
            FadeIn(pred_point, shift=DOWN),
            FadeIn(pred_label),
            run_time=1.0,
        )

        self.play(
            GrowFromCenter(loss_brace),
            FadeIn(loss_text),
            run_time=1.0,
        )

        self.play(GrowArrow(loss_arrow), run_time=1.0)

        # Hold final frame
        self.wait(1.0)
        # --- Scene 3: The Chain Reaction ---
        # 1. Styles and Colors (Catppuccin Mocha)
        bg_color = "#181825"
        self.camera.background_color = bg_color

        c_input = "#89B4FA"
        c_hidden = "#A6E3A1"
        c_output = "#CBA6F7"
        c_loss = "#F38BA8"
        c_arrow = "#FAB387"
        c_text = "#CDD6F4"

        # 2. Gear Creation Helper
        def create_gear(color, label_tex, position):
            circle = Circle(radius=0.8, color=color, stroke_width=4)
            label = MathTex(label_tex, font_size=36, color=c_text).move_to(
                circle.get_center()
            )
            # Simulate gear teeth with small lines at 45-degree intervals
            teeth = VGroup()
            for i in range(8):
                angle = i * PI / 4
                start_pt = circle.point_at_angle(angle)
                end_pt = start_pt + 0.2 * np.array([np.cos(angle), np.sin(angle), 0])
                tooth = Line(start_pt, end_pt, color=color, stroke_width=4)
                teeth.add(tooth)
            return circle, label, teeth

        # Create all gears
        g1_circ, g1_label, g1_teeth = create_gear(c_input, "x", LEFT * 6)
        g2_circ, g2_label, g2_teeth = create_gear(c_hidden, "h", LEFT * 2)
        g3_circ, g3_label, g3_teeth = create_gear(c_output, "y", RIGHT * 2)
        g4_circ, g4_label, g4_teeth = create_gear(c_loss, "L", RIGHT * 6)

        # Separate rotating parts (circles + teeth) from labels (stay upright)
        gear_1_visual = VGroup(g1_circ, g1_teeth)
        gear_2_visual = VGroup(g2_circ, g2_teeth)
        gear_3_visual = VGroup(g3_circ, g3_teeth)
        gear_4_visual = VGroup(g4_circ, g4_teeth)

        # Full gear groups for fade-in
        gear_1_full = VGroup(gear_1_visual, g1_label)
        gear_2_full = VGroup(gear_2_visual, g2_label)
        gear_3_full = VGroup(gear_3_visual, g3_label)
        gear_4_full = VGroup(gear_4_visual, g4_label)

        # 3. Chain Reaction Arrow (backwards from Loss to Input)
        chain_arrow = Arrow(
            start=g4_circ.get_left() + LEFT * 0.15,
            end=g1_circ.get_right() + RIGHT * 0.15,
            color=c_arrow,
            stroke_width=6,
            buff=0.1,
            max_tip_length_to_length_ratio=0.06,
        )
        chain_label = MathTex(r"	ext{Chain Rule}", font_size=36, color=c_text)
        chain_label.next_to(chain_arrow, UP, buff=0.15)

        # 4. Derivative Labels (positioned above each gear-to-gear gap)
        pos_12 = (g1_circ.get_center() + g2_circ.get_center()) / 2 + UP * 1.5
        pos_23 = (g2_circ.get_center() + g3_circ.get_center()) / 2 + UP * 1.5
        pos_34 = (g3_circ.get_center() + g4_circ.get_center()) / 2 + UP * 1.5

        lbl_dhdx = MathTex(
            r"\frac{\partial h}{\partial x}", font_size=32, color=c_arrow
        ).move_to(pos_12)
        lbl_dydh = MathTex(
            r"\frac{\partial y}{\partial h}", font_size=32, color=c_arrow
        ).move_to(pos_23)
        lbl_dLdy = MathTex(
            r"\frac{\partial L}{\partial y}", font_size=32, color=c_arrow
        ).move_to(pos_34)

        # Small connecting dashed lines from labels to gears
        def make_bracket_line(pos):
            return DashedLine(
                pos + DOWN * 0.3,
                pos + DOWN * 0.6,
                color=c_arrow,
                stroke_width=2,
                dash_length=0.1,
            )

        line_12 = make_bracket_line(pos_12)
        line_23 = make_bracket_line(pos_23)
        line_34 = make_bracket_line(pos_34)

        # ===== ANIMATIONS (Total: 7.0s) =====

        # Phase 1: Gear Intro (1.5s)
        self.play(
            LaggedStart(
                FadeIn(gear_1_full, shift=RIGHT * 0.5),
                FadeIn(gear_2_full, shift=RIGHT * 0.5),
                FadeIn(gear_3_full, shift=RIGHT * 0.5),
                FadeIn(gear_4_full, shift=RIGHT * 0.5),
                lag_ratio=0.2,
            ),
            run_time=1.5,
        )

        # Phase 2: Chain Arrow (2.0s)
        self.play(GrowArrow(chain_arrow), Write(chain_label), run_time=2.0)

        # Phase 3: Derivative Labels Cascade (2.0s)
        self.play(
            LaggedStart(
                Write(lbl_dLdy), Write(lbl_dydh), Write(lbl_dhdx), lag_ratio=0.3
            ),
            FadeIn(line_34),
            FadeIn(line_23),
            FadeIn(line_12),
            run_time=2.0,
        )

        # Phase 4: Gear Rotation (0.5s)
        # Only rotate visuals (circles + teeth), keep labels fixed
        self.play(
            Rotate(gear_4_visual, angle=-PI, about_point=g4_circ.get_center()),
            Rotate(gear_3_visual, angle=PI, about_point=g3_circ.get_center()),
            Rotate(gear_2_visual, angle=-PI, about_point=g2_circ.get_center()),
            Rotate(gear_1_visual, angle=PI, about_point=g1_circ.get_center()),
            run_time=0.5,
        )

        # Phase 5: Final Hold (1.0s)
        self.wait(1.0)
        # --- Scene 4: Gradient Flow ---
        bg_color = "#181825"
        node_color = "#BAC2DE"
        grad_cold = ManimColor("#89B4FA")
        grad_hot = ManimColor("#F38BA8")
        text_color = "#CDD6F4"
        output_color = "#A6E3A1"
        loss_color = "#FAB387"

        self.camera.background_color = bg_color

        # 1. Build Network (0-2.2s)
        layer_sizes = [3, 5, 5, 3]
        layer_names = ["Input", "Hidden 1", "Hidden 2", "Output"]
        nodes, node_positions = [], []

        for i, size in enumerate(layer_sizes):
            layer_nodes, layer_pos = [], []
            x_pos = -3.5 + (i * 2.2)
            for j in range(size):
                y_pos = (size - 1) / 2 - j * 1.0
                pos = np.array([x_pos, y_pos, 0])
                dot = Dot(point=pos, color=node_color, radius=0.18)
                dot.set_stroke(WHITE, width=1.5)
                layer_nodes.append(dot)
                layer_pos.append(pos)
            nodes.append(layer_nodes)
            node_positions.append(layer_pos)

        connections = []
        for i in range(len(layer_sizes) - 1):
            layer_conns = []
            for start in node_positions[i]:
                for end in node_positions[i + 1]:
                    line = Line(
                        start, end, stroke_width=1, color=WHITE, stroke_opacity=0.15
                    )
                    layer_conns.append(line)
            connections.append(layer_conns)

        all_nodes = VGroup(*[dot for layer in nodes for dot in layer])
        all_conns = VGroup(*[line for layer in connections for line in layer])

        self.play(FadeIn(all_nodes, lag_ratio=0.1), run_time=1.2)

        labels = VGroup()
        for i, name in enumerate(layer_names):
            x_pos = -3.5 + (i * 2.2)
            label = Text(name, font_size=24, color=text_color)
            label.move_to([x_pos, 3.5, 0])
            labels.add(label)

        self.play(FadeIn(labels), run_time=0.5)
        self.play(Create(all_conns), run_time=0.5)

        # 2. Loss & Scale (2.2-3.0s)
        loss_box = RoundedRectangle(
            width=1.5,
            height=0.8,
            corner_radius=0.1,
            fill_color=loss_color,
            fill_opacity=0.8,
            stroke_width=0,
        )
        loss_box.move_to([5.5, 0, 0])
        loss_text = Text("Loss", font_size=28, color=bg_color)
        loss_text.move_to(loss_box)
        arrow_to_loss = Arrow(
            start=[4.1, 0, 0], end=[4.8, 0, 0], color=output_color, stroke_width=3
        )

        scale_parts = VGroup()
        for k in range(20):
            t = k / 19
            c = interpolate_color(grad_cold, grad_hot, t)
            rect = Rectangle(
                width=0.4, height=0.15, fill_color=c, fill_opacity=1, stroke_width=0
            )
            rect.move_to([7.0, 1.5 - (k + 0.5) * 0.15, 0])
            scale_parts.add(rect)

        scale_label = Text("Grad Magnitude", font_size=20, color=text_color).move_to(
            [7.0, 2.2, 0]
        )
        low_label = Text("Low", font_size=16, color=grad_cold).move_to([7.0, -1.8, 0])
        high_label = Text("High", font_size=16, color=grad_hot).move_to([7.0, 1.8, 0])

        self.play(
            FadeIn(loss_box), FadeIn(loss_text), Create(arrow_to_loss), run_time=0.4
        )
        self.play(
            FadeIn(scale_parts),
            FadeIn(scale_label),
            FadeIn(low_label),
            FadeIn(high_label),
            run_time=0.4,
        )

        # 3. Thicken Connections (3.0-4.0s)
        gradient_magnitudes = [0.2, 0.6, 0.9]
        thicken_anims = []
        for i, layer_conns in enumerate(connections):
            for line in layer_conns:
                line.generate_target()
                line.target.set_color(
                    interpolate_color(grad_cold, grad_hot, gradient_magnitudes[i])
                )
                line.target.set_stroke(
                    width=1 + gradient_magnitudes[i] * 7, opacity=0.7
                )
                thicken_anims.append(MoveToTarget(line))
        self.play(*thicken_anims, run_time=1.0)

        # 4. Gradient Flow (4.0-7.2s)
        waypoints = [
            loss_box.get_center(),
            np.array([3.1, 0, 0]),
            np.array([1.1, 0, 0]),
            np.array([-1.1, 0, 0]),
            np.array([-3.5, 0, 0]),
        ]

        particles = VGroup()
        for _ in range(20):
            p = Dot(point=waypoints[0], radius=0.08, color=grad_hot, fill_opacity=0)
            p.set_z_index(10)
            particles.add(p)
        self.add(particles)

        flow_tracker = ValueTracker(0)

        def make_updater(p_idx):
            def updater(m):
                local_t = (flow_tracker.get_value() - p_idx * 0.04) % 1.0
                seg_float = local_t * 4
                seg_idx = min(int(seg_float), 3)
                seg_t = seg_float - seg_idx
                pos = waypoints[seg_idx] * (1 - seg_t) + waypoints[seg_idx + 1] * seg_t
                m.move_to(pos)
                m.set_fill(opacity=0.3 + 0.7 * (1 - abs(seg_t - 0.5) * 2))

            return updater

        for idx, p in enumerate(particles):
            p.add_updater(make_updater(idx))

        self.play(flow_tracker.animate.set_value(1), run_time=3.2, rate_func=linear)
        for p in particles:
            p.clear_updaters()

        # 5. Final Flash (7.2-7.5s)
        self.play(
            *[Indicate(line, color=grad_hot, scale_factor=1.1) for line in all_conns],
            run_time=0.3,
        )
        self.wait(0.2)
        # --- Scene 5: Weight Adjustment ---
        # === Color Palette (Catppuccin Mocha) ===
        BG = "#1E1E2E"
        TEXT = "#CDD6F4"
        MUTED = "#A6ADC8"
        PINK = "#F38BA8"
        PEACH = "#FAB387"
        GREEN = "#A6E3A1"
        MAUVE = "#CBA6F7"
        SURFACE = "#45475A"

        self.camera.background_color = BG

        # ============================================
        # 1. Weight Slider Track (0.0s – 1.5s)
        # ============================================
        track = Line(LEFT * 3.5, RIGHT * 3.5, color=MUTED, stroke_width=8)

        ticks = VGroup()
        for i in range(-3, 4):
            tick = Line(UP * 0.12, DOWN * 0.12, color=MUTED, stroke_width=2).move_to(
                RIGHT * i
            )
            ticks.add(tick)

        track_label = Text("Weight Value (w)", font_size=22, color=MUTED).next_to(
            track, DOWN, buff=0.25
        )
        track_group = VGroup(track, ticks, track_label)

        self.play(FadeIn(track_group, shift=UP * 0.2), run_time=1.5)

        # ============================================
        # 2. Error Meter – Two Bars (1.5s – 3.0s)
        # ============================================
        bar_width = 0.7
        bar_max_h = 2.5

        before_bg = Rectangle(
            width=bar_width,
            height=bar_max_h,
            color=SURFACE,
            fill_opacity=0.4,
            stroke_width=1,
        )
        after_bg = Rectangle(
            width=bar_width,
            height=bar_max_h,
            color=SURFACE,
            fill_opacity=0.4,
            stroke_width=1,
        )

        # "Before" bar: 80% height
        before_bar = Rectangle(
            width=bar_width,
            height=bar_max_h * 0.8,
            color=PINK,
            fill_opacity=0.85,
            stroke_width=0,
        )
        before_bar.align_to(before_bg, DOWN)

        # "After" bar: starts at 80% too, will shrink
        after_bar = Rectangle(
            width=bar_width,
            height=bar_max_h * 0.8,
            color=PINK,
            fill_opacity=0.85,
            stroke_width=0,
        )
        after_bar.align_to(after_bg, DOWN)

        before_label = Text("Before", font_size=18, color=PINK).next_to(
            before_bg, DOWN, buff=0.1
        )
        after_label = Text("After", font_size=18, color=PINK).next_to(
            after_bg, DOWN, buff=0.1
        )

        before_group = VGroup(before_bg, before_bar, before_label)
        after_group = VGroup(after_bg, after_bar, after_label)
        bar_pair = (
            VGroup(before_group, after_group)
            .arrange(RIGHT, buff=0.6)
            .to_corner(UR, buff=0.5)
        )

        error_title = Text("Error Level", font_size=20, color=TEXT).next_to(
            bar_pair, UP, buff=0.25
        )

        self.play(FadeIn(bar_pair, shift=DOWN * 0.2), FadeIn(error_title), run_time=1.5)

        # ============================================
        # 3. Current Weight Marker (3.0s – 3.5s)
        # ============================================
        current_pos = RIGHT * 1.5
        current_dot = Dot(current_pos, radius=0.22, color=PEACH, z_index=5)
        current_label = Text("Current w", font_size=18, color=PEACH).next_to(
            current_dot, UP, buff=0.2
        )

        self.play(FadeIn(current_dot, scale=1.5), FadeIn(current_label), run_time=0.5)

        # ============================================
        # 4. Gradient Arrow (3.5s – 4.2s)
        # ============================================
        grad_arrow = Arrow(
            start=current_pos + RIGHT * 0.3,
            end=LEFT * 1.0,
            color=MAUVE,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.15,
            buff=0.0,
        )
        grad_label = MathTex(r"-\nabla \mathcal{L}", font_size=36, color=MAUVE).next_to(
            grad_arrow, UP, buff=0.15
        )

        self.play(
            GrowArrow(grad_arrow), FadeIn(grad_label, shift=LEFT * 0.2), run_time=0.7
        )

        # ============================================
        # 5. Weight Slides to New Position (4.2s – 5.5s)
        # ============================================
        new_pos = LEFT * 0.5
        new_dot = Dot(new_pos, radius=0.22, color=GREEN, z_index=5)
        new_label = Text("New w", font_size=18, color=GREEN).next_to(
            new_dot, UP, buff=0.2
        )

        self.play(
            current_dot.animate.move_to(new_pos).set_color(GREEN),
            current_label.animate.next_to(new_dot, UP, buff=0.2).set_color(GREEN),
            FadeOut(grad_arrow, shift=LEFT * 0.3),
            FadeOut(grad_label, shift=LEFT * 0.3),
            run_time=1.3,
        )

        # ============================================
        # 6. Error Reduction (5.5s – 7.0s)
        # ============================================
        reduced_bar = Rectangle(
            width=bar_width,
            height=bar_max_h * 0.35,
            color=GREEN,
            fill_opacity=0.85,
            stroke_width=0,
        )
        reduced_bar.align_to(after_bg, DOWN)

        self.play(
            Transform(after_bar, reduced_bar),
            after_label.animate.set_color(GREEN),
            run_time=0.8,
        )

        checkmark = Text("✓", font_size=48, color=GREEN).next_to(
            after_bg, RIGHT, buff=0.4
        )
        self.play(FadeIn(checkmark, scale=2), run_time=0.4)

        self.wait(0.8)
