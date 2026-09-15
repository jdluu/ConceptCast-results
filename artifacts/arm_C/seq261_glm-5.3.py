import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Neural network as a chain of functions ---
        self.clear()
        self.camera.background_color = "#181825"

        # ------------------------------------------------------------------
        # 1. Objects
        # ------------------------------------------------------------------
        # Title (top of frame)
        title = Text(
            "Neural network as a chain of functions",
            font="Sans",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # Main statement (center of frame)
        main = Text(
            "A neural network is a chain of functions",
            font="Sans",
            font_size=48,
            color="#89b4fa",
        ).move_to(ORIGIN)
        if main.width > 11.0:
            main.scale_to_fit_width(11.0)

        # Supporting visual: the forward chain  x -> f_1 -> f_2 -> f_3 -> y
        node_data = [
            ("x", "#94e2d5"),
            ("f_1", "#89b4fa"),
            ("f_2", "#fab387"),
            ("f_3", "#f38ba8"),
            ("\\hat{y}", "#a6e3a1"),
        ]
        xs = [-2.8, -1.4, 0.0, 1.4, 2.8]

        nodes = VGroup()
        labels = VGroup()
        for (tex, col), x in zip(node_data, xs):
            circle = Circle(radius=0.32, color=col, stroke_width=2.0)
            circle.move_to([x, -1.8, 0])
            label = MathTex(tex, color=col, font_size=30)
            label.move_to(circle.get_center())
            nodes.add(circle)
            labels.add(label)

        arrows = VGroup()
        for left_circle, right_circle in zip(nodes[:-1], nodes[1:]):
            arrows.add(
                Arrow(
                    left_circle.get_right(),
                    right_circle.get_left(),
                    buff=0.06,
                    stroke_width=2.0,
                    tip_length=0.16,
                    color="#6c7086",
                )
            )

        caption = Text(
            "data flows forward, transformed layer by layer",
            font="Sans",
            font_size=24,
            color="#9399b2",
        ).move_to(DOWN * 2.6)

        # ------------------------------------------------------------------
        # 2. Animations
        # ------------------------------------------------------------------
        self.play(Write(title), run_time=1.2)
        self.play(Write(main), run_time=1.2)

        # Build the chain of function nodes
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(GrowFromCenter(c), FadeIn(l, scale=0.5))
                    for c, l in zip(nodes, labels)
                ],
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )

        # Connect the chain with arrows
        self.play(
            LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.15),
            run_time=0.7,
        )

        # Show data flowing forward through the chain
        self.play(
            LaggedStart(
                *[
                    ShowPassingFlash(a.copy().set_color(WHITE), time_width=0.5)
                    for a in arrows
                ],
                lag_ratio=0.2,
            ),
            FadeIn(caption),
            run_time=1.0,
        )

        # Emphasize the key statement
        self.play(
            Indicate(main, color="#94e2d5", scale_factor=1.05),
            run_time=0.5,
        )

        # 3. Wait to reach the requested duration
        self.wait(0.4)
        # --- Scene 2: Step 2: Loss function ---
        self.clear()
        # --- Scene 2: Step 2: Loss function ---
        self.camera.background_color = "#181825"

        # Palette
        blue = "#89b4fa"
        peach = "#fab387"
        red = "#f38ba8"
        green = "#a6e3a1"
        teal = "#94e2d5"

        # ---------- Title ----------
        title = Text("Loss function", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # ---------- Axes ----------
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=4.5,
            axis_config={"color": peach, "stroke_width": 2.0, "include_tip": True},
        )
        axes.move_to(ORIGIN + DOWN * 0.3)

        x_label = axes.get_x_axis_label(
            MathTex(r"\hat{y}", font_size=32, color=peach)
        ).shift(DOWN * 0.15)
        y_label = axes.get_y_axis_label(
            MathTex(r"L(\hat{y})", font_size=32, color=peach)
        ).shift(UP * 0.15)

        # ---------- Loss curve (parabola) ----------
        curve = axes.plot(lambda x: 0.2 * x**2, x_range=[-3, 3])
        curve.set_stroke(blue, width=4)

        # True target sits at the minimum (y_hat = 0)
        target_x = 0.0
        pred_x = 1.8
        pred_y = 0.2 * pred_x**2

        target_point = axes.c2p(target_x, 0)
        pred_point = axes.c2p(pred_x, pred_y)
        pred_foot = axes.c2p(pred_x, 0)

        target_dot = Dot(target_point, radius=0.09, color=green)
        pred_dot = Dot(pred_point, radius=0.09, color=red)

        # Vertical dashed drop from prediction to x-axis
        drop_line = DashedLine(pred_point, pred_foot, dash_length=0.12)
        drop_line.set_stroke(teal, width=2.0)

        # Horizontal dashed guide from curve to loss axis
        guide_line = DashedLine(pred_point, axes.c2p(0, pred_y), dash_length=0.12)
        guide_line.set_stroke(teal, width=2.0)

        # Error brace on the x-axis between target and prediction
        error_brace = BraceBetweenPoints(target_point, pred_foot, DOWN, buff=0.15)
        error_brace.set_color(peach)
        error_label = Text("error", font_size=24, color=peach)
        error_label.next_to(error_brace, DOWN, buff=0.1)

        # Labels for the dots
        target_label = Text("true target", font_size=22, color=green)
        target_label.next_to(target_dot, DL, buff=0.15)
        pred_label = Text("prediction", font_size=22, color=red)
        pred_label.next_to(pred_dot, UP + RIGHT, buff=0.15)

        # Loss formula
        formula = MathTex(r"L = (\hat{y} - y)^2", font_size=34, color=WHITE)
        formula.to_corner(UR).shift(DOWN * 1.1 + LEFT * 0.2)
        formula_bg = BackgroundRectangle(formula, color=BLACK, fill_opacity=0.6)
        formula_group = VGroup(formula_bg, formula)

        # "loss" annotation near the vertical drop
        loss_label = Text("loss", font_size=22, color=blue)
        loss_label.next_to(drop_line, RIGHT, buff=0.15)

        # ---------- Animations ----------
        self.play(Write(title), Create(axes), run_time=1.2)
        self.play(
            FadeIn(x_label, shift=0.2 * RIGHT),
            FadeIn(y_label, shift=0.2 * DOWN),
            run_time=0.6,
        )
        self.play(Create(curve), run_time=1.0)

        self.play(
            GrowFromCenter(target_dot),
            FadeIn(target_label, shift=0.2 * UP),
            run_time=0.8,
        )
        self.play(
            GrowFromCenter(pred_dot),
            FadeIn(pred_label, shift=0.2 * UP),
            Create(drop_line),
            run_time=0.8,
        )

        self.play(
            Create(guide_line),
            GrowFromCenter(error_brace),
            FadeIn(error_label, shift=0.2 * DOWN),
            FadeIn(formula_group),
            FadeIn(loss_label),
            run_time=1.0,
        )
        self.play(Circumscribe(formula, color=YELLOW, buff=0.1), run_time=0.6)
        self.wait(0.6)
        # --- Scene 3: Step 3: Gradient descent overview ---
        self.clear()
        self.camera.background_color = "#181825"

        # Palette (Catppuccin Mocha accents)
        C_PINK = "#f38ba8"
        C_BLUE = "#89b4fa"
        C_PEACH = "#fab387"
        C_GREEN = "#a6e3a1"
        C_TEAL = "#94e2d5"

        # ------------------------------------------
        # 1. Title
        # ------------------------------------------
        title = Text("Gradient descent overview", font_size=36, color=WHITE)
        title.shift(UP * 3)

        # ------------------------------------------
        # 2. Weight number line (main object)
        # ------------------------------------------
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            include_numbers=True,
            color=C_PINK,
            stroke_width=2.0,
            font_size=28,
        ).shift(DOWN * 2.2)
        w_label = MathTex("w", font_size=36, color=C_PINK)
        w_label.next_to(number_line, DOWN, buff=0.35)
        w_caption = Text("weight value", font_size=22, color=WHITE)
        w_caption.next_to(w_label, DOWN, buff=0.2)

        # ------------------------------------------
        # 3. Loss bowl sitting above the number line
        # ------------------------------------------
        def loss_y(x):
            return 1.2 + 0.15 * x**2

        curve = FunctionGraph(
            lambda x: 0.15 * x**2,
            x_range=[-3.2, 3.2],
            color=C_BLUE,
            stroke_width=4,
        ).shift(UP * 1.2)

        curve_label = MathTex(r"L(w)", font_size=34, color=C_BLUE)
        curve_label.move_to(np.array([-3.1, 2.85, 0]))

        # ------------------------------------------
        # 4. Ball (current weight) high on the bowl
        # ------------------------------------------
        ball = Dot(point=np.array([-3.0, loss_y(-3.0), 0]), radius=0.12, color=C_PEACH)

        # Downhill tangent arrow at the ball's starting point
        arrow_start = np.array([-2.95, loss_y(-2.95), 0])
        arrow_end = np.array([-2.35, loss_y(-2.35), 0])
        downhill_arrow = Arrow(
            arrow_start,
            arrow_end,
            buff=0,
            color=C_GREEN,
            stroke_width=3,
            tip_length=0.2,
            max_tip_length_to_length_ratio=0.5,
        )
        grad_label = MathTex(r"\nabla L", font_size=32, color=C_GREEN)
        grad_label.next_to(downhill_arrow, UP, buff=0.15)
        downhill_text = Text("downhill step", font_size=22, color=C_GREEN)
        downhill_text.next_to(grad_label, UP, buff=0.1)

        # ------------------------------------------
        # 5. Formula and minimum marker
        # ------------------------------------------
        formula = MathTex(
            r"w \;\leftarrow\; w - \eta\,\nabla L(w)",
            font_size=38,
            color=C_TEAL,
        ).move_to(np.array([3.1, 0.6, 0]))

        eta_text = Text("learning rate", font_size=20, color=C_TEAL)
        eta_text.next_to(formula, DOWN, buff=0.15)

        # Dashed line: minimum of the bowl down to w = 0
        min_point = np.array([0.0, loss_y(0.0), 0])
        zero_point = number_line.n2p(0)
        dashed = DashedLine(
            min_point,
            zero_point,
            color=C_TEAL,
            stroke_width=2.0,
            dash_length=0.15,
        )
        min_label = Text("minimum", font_size=22, color=C_TEAL)
        min_label.next_to(dashed, LEFT, buff=0.2)

        # ------------------------------------------
        # Animations
        # ------------------------------------------
        # 0.8 s
        self.play(Write(title), run_time=0.8)

        # 0.8 s
        self.play(
            Create(number_line),
            FadeIn(w_label, shift=DOWN * 0.3),
            FadeIn(w_caption, shift=DOWN * 0.3),
            run_time=0.8,
        )

        # 1.2 s
        self.play(
            Create(curve),
            FadeIn(curve_label, shift=DOWN * 0.2),
            run_time=1.2,
        )

        # 0.8 s
        self.play(
            GrowFromCenter(ball),
            Create(downhill_arrow),
            FadeIn(grad_label, shift=DOWN * 0.2),
            FadeIn(downhill_text, shift=DOWN * 0.2),
            run_time=0.8,
        )

        # 1.4 s : roll the ball downhill along the bowl
        tracker = ValueTracker(-3.0)
        ball.add_updater(
            lambda m: m.move_to(
                np.array([tracker.get_value(), loss_y(tracker.get_value()), 0])
            )
        )
        self.play(
            tracker.animate.set_value(0.0),
            FadeOut(downhill_arrow),
            FadeOut(grad_label),
            FadeOut(downhill_text),
            run_time=1.4,
            rate_func=smooth,
        )
        ball.clear_updaters()

        # 1.0 s
        self.play(
            Create(dashed),
            FadeIn(min_label, shift=RIGHT * 0.2),
            Write(formula),
            FadeIn(eta_text, shift=UP * 0.2),
            run_time=1.0,
        )

        # Final beat: highlight the update rule (0.5 s + 0.5 s wait)
        self.play(Circumscribe(formula, color=YELLOW, buff=0.12), run_time=0.5)
        self.wait(0.5)
        # --- Scene 4: Step 4: Chain rule of calculus ---
        self.clear()
        self.camera.background_color = "#181825"

        BLUE_C = "#89b4fa"
        ORANGE_C = "#fab387"
        PINK_C = "#f38ba8"
        GREEN_C = "#a6e3a1"
        TEAL_C = "#94e2d5"

        # ---------- Title ----------
        title_4 = Text("Chain rule of calculus", font_size=36, color=WHITE)
        title_4.move_to(UP * 3)

        # ---------- Main VGroup: influence pipeline ----------
        node_w = Circle(radius=0.55, color=BLUE_C, stroke_width=2.0)
        label_w = MathTex(r"w", font_size=40, color=BLUE_C)
        node_w_v = VGroup(node_w, label_w)

        node_a = Circle(radius=0.55, color=ORANGE_C, stroke_width=2.0)
        label_a = MathTex(r"a", font_size=40, color=ORANGE_C)
        node_a_v = VGroup(node_a, label_a)

        node_z = Circle(radius=0.55, color=PINK_C, stroke_width=2.0)
        label_z = MathTex(r"z", font_size=40, color=PINK_C)
        node_z_v = VGroup(node_z, label_z)

        node_L = Circle(radius=0.6, color=GREEN_C, stroke_width=2.0)
        label_L = MathTex(r"L", font_size=40, color=GREEN_C)
        node_L_v = VGroup(node_L, label_L)

        node_w_v.move_to(LEFT * 4.2 + DOWN * 0.3)
        node_a_v.move_to(LEFT * 1.4 + DOWN * 0.3)
        node_z_v.move_to(RIGHT * 1.4 + DOWN * 0.3)
        node_L_v.move_to(RIGHT * 4.2 + DOWN * 0.3)

        arrow_wa = Arrow(
            node_w_v.get_right() + 0.08 * RIGHT,
            node_a_v.get_left() - 0.08 * RIGHT,
            buff=0,
            stroke_width=2.0,
            tip_length=0.2,
            color=TEAL_C,
        )
        arrow_az = Arrow(
            node_a_v.get_right() + 0.08 * RIGHT,
            node_z_v.get_left() - 0.08 * RIGHT,
            buff=0,
            stroke_width=2.0,
            tip_length=0.2,
            color=TEAL_C,
        )
        arrow_zL = Arrow(
            node_z_v.get_right() + 0.08 * RIGHT,
            node_L_v.get_left() - 0.08 * RIGHT,
            buff=0,
            stroke_width=2.0,
            tip_length=0.2,
            color=TEAL_C,
        )

        der_wa = MathTex(r"\frac{\partial a}{\partial w}", font_size=30, color=TEAL_C)
        der_wa.next_to(arrow_wa, DOWN, buff=0.15)
        der_az = MathTex(r"\frac{\partial z}{\partial a}", font_size=30, color=TEAL_C)
        der_az.next_to(arrow_az, DOWN, buff=0.15)
        der_zL = MathTex(r"\frac{\partial L}{\partial z}", font_size=30, color=TEAL_C)
        der_zL.next_to(arrow_zL, DOWN, buff=0.15)

        cap_w = Text("early weight", font_size=22, color=BLUE_C)
        cap_w.next_to(node_w_v, DOWN, buff=0.6)
        cap_L = Text("loss", font_size=22, color=GREEN_C)
        cap_L.next_to(node_L_v, DOWN, buff=0.6)

        main_4 = VGroup(
            node_w_v,
            node_a_v,
            node_z_v,
            node_L_v,
            arrow_wa,
            arrow_az,
            arrow_zL,
            der_wa,
            der_az,
            der_zL,
            cap_w,
            cap_L,
        )

        # ---------- Chain-rule formula ----------
        formula = MathTex(
            r"\frac{\partial L}{\partial w}",
            r"=",
            r"\frac{\partial L}{\partial z}",
            r"\cdot",
            r"\frac{\partial z}{\partial a}",
            r"\cdot",
            r"\frac{\partial a}{\partial w}",
            font_size=44,
            color=WHITE,
        )
        formula.move_to(DOWN * 2.4)
        formula[0].set_color(GREEN_C)
        formula[2].set_color(PINK_C)
        formula[4].set_color(ORANGE_C)
        formula[6].set_color(BLUE_C)

        # ---------- Animations ----------
        # 1) Title (0.8s)
        self.play(Write(title_4), run_time=0.8)

        # 2) Nodes grow from center (1.2s)
        self.play(
            LaggedStart(
                GrowFromCenter(node_w_v),
                GrowFromCenter(node_a_v),
                GrowFromCenter(node_z_v),
                GrowFromCenter(node_L_v),
                lag_ratio=0.35,
            ),
            run_time=1.2,
        )

        # 3) Arrows + labels (1.2s)
        self.play(
            Create(arrow_wa),
            Create(arrow_az),
            Create(arrow_zL),
            FadeIn(der_wa),
            FadeIn(der_az),
            FadeIn(der_zL),
            FadeIn(cap_w, shift=0.15 * UP),
            FadeIn(cap_L, shift=0.15 * UP),
            run_time=1.2,
        )

        # 4) Formula writes in (1.6s)
        self.play(Write(formula), run_time=1.6)

        # 5) Influence pulse flows through the chain (2.2s)
        flash_wa = ShowPassingFlash(
            arrow_wa.copy().set_color(YELLOW).set_stroke(width=5), time_width=0.5
        )
        flash_az = ShowPassingFlash(
            arrow_az.copy().set_color(YELLOW).set_stroke(width=5), time_width=0.5
        )
        flash_zL = ShowPassingFlash(
            arrow_zL.copy().set_color(YELLOW).set_stroke(width=5), time_width=0.5
        )
        self.play(
            LaggedStart(flash_wa, flash_az, flash_zL, lag_ratio=0.55),
            Circumscribe(formula, color=YELLOW, buff=0.12),
            run_time=2.2,
        )

        # 6) Final hold
        self.wait(0.1)
        # --- Scene 5: Step 5: Backward pass: output layer gradients ---
        # --- Scene 5: Step 5: Backward pass: output layer gradients ---
        BG = "#181825"
        TEAL = "#94e2d5"
        BLUE = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"

        self.camera.background_color = BG

        # Title
        title = Text("Backward pass: output layer gradients", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # Gradient table: cells are raw LaTeX strings rendered with MathTex,
        # row labels are pre-built (colored) MathTex mobjects.
        table = Table(
            [
                [
                    r"\frac{\partial L}{\partial \hat{y}}",
                    r"=\ \frac{\partial L}{\partial \hat{y}}",
                ],
                [
                    r"\frac{\partial \hat{y}}{\partial z}",
                    r"=\ \sigma'(z)",
                ],
                [
                    r"\frac{\partial z}{\partial w}",
                    r"=\ a^{(L-1)}",
                ],
            ],
            row_labels=[
                MathTex(r"\delta_{\hat{y}}", color=TEAL),
                MathTex(r"\delta_z", color=TEAL),
                MathTex(r"\delta_w", color=TEAL),
            ],
            element_to_mobject=MathTex,
        )

        # Color the first-column gradient terms to match the chain rule below
        table.get_entries((1, 1)).set_color(PINK)
        table.get_entries((2, 1)).set_color(PEACH)
        table.get_entries((3, 1)).set_color(BLUE)

        table.scale(0.85)
        table.move_to(ORIGIN + DOWN * 0.2)

        # Chain rule formula below
        formula = MathTex(
            r"\frac{\partial L}{\partial w}",
            r"=",
            r"\frac{\partial L}{\partial \hat{y}}",
            r"\cdot",
            r"\frac{\partial \hat{y}}{\partial z}",
            r"\cdot",
            r"\frac{\partial z}{\partial w}",
        ).scale(0.8)
        formula.next_to(table, DOWN, buff=0.6)
        formula[0].set_color(TEAL)
        formula[2].set_color(PINK)
        formula[4].set_color(PEACH)
        formula[6].set_color(BLUE)

        # Backward-flowing arrow beside the table
        arrow = CurvedArrow(
            ORIGIN + RIGHT * 4.5 + UP * 1.0,
            ORIGIN + RIGHT * 4.5 + DOWN * 1.0,
            angle=TAU / 3,
        )
        arrow.set_color(GREEN)
        arrow_label = Text("backward", font_size=22, color=GREEN)
        arrow_label.next_to(arrow, RIGHT, buff=0.15)

        # Animations: 1.0 + 1.2 + 1.2 + 1.0 + 2.6 = 7.0s
        self.play(Write(title), run_time=1.0)
        self.play(GrowFromCenter(table), run_time=1.2)
        self.play(
            FadeIn(formula, shift=UP * 0.3),
            Create(arrow),
            FadeIn(arrow_label, shift=LEFT * 0.3),
            run_time=1.2,
        )
        self.play(
            Circumscribe(formula, color=YELLOW, buff=0.1),
            run_time=1.0,
        )
        self.wait(2.6)
        # --- Scene 6: Step 6: Error propagation to hidden layers ---
        self.clear()
        self.camera.background_color = "#181825"

        BLUE_C = "#89b4fa"
        ORANGE_C = "#fab387"
        PINK_C = "#f38ba8"
        GREEN_C = "#a6e3a1"
        TEAL_C = "#94e2d5"
        TEXT_C = "#cdd6f4"

        # ---------------- Title ----------------
        title = Text("Error propagation to hidden layers", font_size=36, color=WHITE)
        title.move_to(UP * 3)
        self.play(Write(title), run_time=1.0)

        # ---------------- Layer labels ----------------
        lay_out_lbl = Text("Output layer", font_size=22, color=BLUE_C)
        lay_hid_lbl = Text("Hidden layer", font_size=22, color=ORANGE_C)
        lay_in_lbl = Text("Input layer", font_size=22, color=TEAL_C)
        lay_out_lbl.move_to(RIGHT * 4.5 + UP * 0.4)
        lay_hid_lbl.move_to(ORIGIN + UP * 0.4)
        lay_in_lbl.move_to(LEFT * 4.5 + UP * 0.4)

        # ---------------- Neurons ----------------
        out_n = Dot(point=RIGHT * 4.5 + DOWN * 1.2, radius=0.16, color=BLUE_C)
        hid_n1 = Dot(point=LEFT * 0.9 + DOWN * 0.4, radius=0.16, color=ORANGE_C)
        hid_n2 = Dot(point=LEFT * 0.9 + DOWN * 2.0, radius=0.16, color=ORANGE_C)
        in_n1 = Dot(point=LEFT * 4.5 + DOWN * 0.4, radius=0.16, color=TEAL_C)
        in_n2 = Dot(point=LEFT * 4.5 + DOWN * 2.0, radius=0.16, color=TEAL_C)

        # Forward connections (faint, already-trained look)
        fwd = VGroup(
            Line(
                hid_n1.get_center(),
                out_n.get_center(),
                stroke_width=1.5,
                stroke_opacity=0.3,
                color=TEXT_C,
            ),
            Line(
                hid_n2.get_center(),
                out_n.get_center(),
                stroke_width=1.5,
                stroke_opacity=0.3,
                color=TEXT_C,
            ),
            Line(
                in_n1.get_center(),
                hid_n1.get_center(),
                stroke_width=1.5,
                stroke_opacity=0.3,
                color=TEXT_C,
            ),
            Line(
                in_n2.get_center(),
                hid_n2.get_center(),
                stroke_width=1.5,
                stroke_opacity=0.3,
                color=TEXT_C,
            ),
            Line(
                in_n2.get_center(),
                hid_n1.get_center(),
                stroke_width=1.5,
                stroke_opacity=0.3,
                color=TEXT_C,
            ),
        )

        network = VGroup(
            lay_out_lbl,
            lay_hid_lbl,
            lay_in_lbl,
            out_n,
            hid_n1,
            hid_n2,
            in_n1,
            in_n2,
            fwd,
        )
        self.play(
            LaggedStart(
                FadeIn(network, lag_ratio=0.15),
                lag_ratio=0.1,
            ),
            run_time=1.5,
        )

        # ---------------- Main backward arrow (storyboard object) ----------------
        main_arrow = Arrow(
            start=RIGHT * 3.0 + DOWN * 1.2,
            end=LEFT * 2.2 + DOWN * 1.2,
            buff=0.0,
            color=TEXT_C,
            stroke_width=6,
            tip_length=0.35,
        )
        arrow_label = Text("error signal flows backward", font_size=22, color=PINK_C)
        arrow_label.next_to(main_arrow, DOWN, buff=0.25)
        self.play(GrowFromCenter(main_arrow), run_time=1.0)
        self.play(FadeIn(arrow_label, shift=UP * 0.2), run_time=0.5)

        # ---------------- Error flash at output ----------------
        err_out = MathTex(
            r"\frac{\partial L}{\partial \hat{y}}", font_size=44, color=PINK_C
        )
        err_out.next_to(out_n, DOWN, buff=0.3)
        self.play(GrowFromCenter(err_out), run_time=0.75)

        # ---------------- Backward gradient arrows (chain rule) ----------------
        back_arrow_1 = Arrow(
            start=out_n.get_center(),
            end=hid_n1.get_center(),
            buff=0.2,
            color=PINK_C,
            stroke_width=3,
            tip_length=0.2,
        )
        back_arrow_2 = Arrow(
            start=out_n.get_center(),
            end=hid_n2.get_center(),
            buff=0.2,
            color=PINK_C,
            stroke_width=3,
            tip_length=0.2,
        )
        self.play(
            LaggedStart(
                Create(back_arrow_1),
                Create(back_arrow_2),
                lag_ratio=0.3,
            ),
            run_time=1.0,
        )

        # Flash the backward signal along the arrows
        self.play(
            ShowPassingFlash(
                back_arrow_1.copy().set_color(YELLOW).set_stroke(width=8),
                time_width=0.4,
            ),
            ShowPassingFlash(
                back_arrow_2.copy().set_color(YELLOW).set_stroke(width=8),
                time_width=0.4,
            ),
            run_time=0.75,
        )

        # ---------------- Chain rule gradient composition ----------------
        grad_txt = MathTex(
            r"\frac{\partial L}{\partial w^{(1)}}",
            r"=",
            r"\frac{\partial L}{\partial h}",
            r"\cdot",
            r"\frac{\partial h}{\partial w^{(1)}}",
            font_size=34,
        )
        grad_txt[0].set_color(ORANGE_C)
        grad_txt[2].set_color(PINK_C)
        grad_txt[4].set_color(GREEN_C)
        grad_txt.move_to(DOWN * 3.1)
        chain_rule_lbl = Text("chain rule", font_size=20, color=GREEN_C)
        chain_rule_lbl.next_to(grad_txt, RIGHT, buff=0.6)
        self.play(Write(grad_txt), run_time=1.0)
        self.play(FadeIn(chain_rule_lbl, shift=LEFT * 0.2), run_time=0.5)

        # Highlight hidden weights
        hidden_weights = VGroup(
            Line(
                in_n1.get_center(), hid_n1.get_center(), stroke_width=4, color=ORANGE_C
            ),
            Line(
                in_n2.get_center(), hid_n2.get_center(), stroke_width=4, color=ORANGE_C
            ),
            Line(
                in_n2.get_center(), hid_n1.get_center(), stroke_width=4, color=ORANGE_C
            ),
        )
        self.play(
            LaggedStart(
                *[Create(w) for w in hidden_weights],
                lag_ratio=0.2,
            ),
            run_time=0.75,
        )

        # Final held beat
        self.wait(0.25)
        # --- Scene 7: Step 7: Weight update rule ---
        self.clear()
        self.camera.background_color = "#181825"

        # Palette (Catppuccin Mocha accents)
        blue = "#89b4fa"
        peach = "#fab387"
        pink = "#f38ba8"
        green = "#a6e3a1"
        teal = "#94e2d5"

        # ---- Title ----
        title = Text("Weight update rule", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # ---- Main formula (the "main_7" content) ----
        formula = MathTex(
            r"w_{\text{new}}",
            r"=",
            r"w",
            r"-",
            r"\eta",
            r"\cdot",
            r"\nabla_w L",
            font_size=48,
        )
        formula.set_color(blue)
        formula[2].set_color(WHITE)
        formula[4].set_color(peach)
        formula[6].set_color(pink)
        formula.move_to(UP * 0.8)

        # ---- Supporting labels ----
        label_eta = MathTex(r"\eta", r"\ \text{(learning rate)}", font_size=28)
        label_eta[0].set_color(peach)
        label_eta[1].set_color(WHITE)

        label_grad = MathTex(r"\nabla_w L", r"\ \text{(gradient)}", font_size=28)
        label_grad[0].set_color(pink)
        label_grad[1].set_color(WHITE)

        labels = VGroup(label_eta, label_grad).arrange(RIGHT, buff=1.4)
        labels.move_to(DOWN * 0.7)

        # ---- Downhill metaphor (loss surface + ball + arrow) ----
        shift_vec = np.array([0.0, -2.2, 0.0])

        def slope_point(t):
            return np.array([t, -0.35 * t**2, 0.0]) + shift_vec

        slope = ParametricFunction(
            lambda t: np.array([t, -0.35 * t**2, 0.0]),
            t_range=[-2.2, 1.2],
            color=teal,
            stroke_width=4,
        )
        slope.shift(shift_vec)

        ball = Dot(point=slope_point(-1.7), radius=0.13, color=peach)
        downhill_arrow = Arrow(
            slope_point(-1.2),
            slope_point(0.9),
            buff=0.3,
            color="#f9e2af",
            stroke_width=4,
        )

        caption = Text("nudging the network downhill", font_size=24, color=teal)
        caption.move_to(DOWN * 1.5)

        # ---- Animations ----
        self.play(Write(title), run_time=0.7)

        self.play(Write(formula), run_time=1.3)

        self.play(FadeIn(labels, shift=UP * 0.2), run_time=0.8)

        self.play(
            LaggedStart(
                Create(slope),
                GrowFromCenter(ball),
                GrowFromCenter(downhill_arrow),
                lag_ratio=0.35,
            ),
            FadeIn(caption, shift=UP * 0.1),
            run_time=1.0,
        )

        self.play(Indicate(formula, color="#f9e2af", scale_factor=1.15), run_time=0.7)

        self.wait(1.5)
        # --- Scene 8: Step 8: Iterative training loop ---
        self.clear()
        self.camera.background_color = "#181825"

        BLUE_ACCENT = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"

        # ---------- Title ----------
        title = Text(
            "Iterative training loop",
            font_size=36,
            color=WHITE,
        )
        title.move_to(UP * 3)

        self.play(Write(title), run_time=1.0)

        # ---------- Axes (main object, at ORIGIN, shifted right for loop diagram) ----------
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=7,
            y_length=4,
            axis_config={
                "color": PEACH,
                "stroke_width": 2.0,
                "include_tip": False,
            },
        )
        axes.shift(RIGHT * 1.6)

        x_label = Text("training steps", font_size=22, color=PEACH)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)
        x_label.to_edge(RIGHT, buff=0.6)

        y_label = Text("loss", font_size=22, color=PEACH)
        y_label.next_to(axes.y_axis, UP, buff=0.2)
        y_label.align_to(axes, LEFT)

        self.play(Create(axes), run_time=1.0)
        self.play(
            FadeIn(x_label, shift=UP * 0.2),
            FadeIn(y_label, shift=RIGHT * 0.2),
            run_time=0.5,
        )

        # ---------- Decreasing loss curve ----------
        loss_curve = axes.plot(
            lambda x: 1.7 * (2.6 ** (-x)) - 0.7,
            x_range=[-3, 3],
            color=GREEN,
            stroke_width=4,
        )
        loss_label = MathTex(r"L(	heta)", font_size=32, color=GREEN)
        loss_label.next_to(axes.c2p(2.4, 1.7 * (2.6 ** (-2.4)) - 0.7), UP, buff=0.3)

        self.play(
            Create(loss_curve), FadeIn(loss_label, shift=DOWN * 0.3), run_time=2.0
        )

        # ---------- Iteration loop: Forward -> Backward -> Update ----------
        loop_center = LEFT * 4.9 + DOWN * 0.4

        fwd_dot = Circle(
            radius=0.16, color=BLUE_ACCENT, fill_opacity=1.0, stroke_width=0
        )
        fwd_text = Text("Forward", font_size=22, color=BLUE_ACCENT)

        bwd_dot = Circle(radius=0.16, color=PINK, fill_opacity=1.0, stroke_width=0)
        bwd_text = Text("Backward", font_size=22, color=PINK)

        upd_dot = Circle(radius=0.16, color=TEAL, fill_opacity=1.0, stroke_width=0)
        upd_text = Text("Update", font_size=22, color=TEAL)

        # Arrange as a triangular cycle
        fwd_group = VGroup(fwd_dot, fwd_text).arrange(RIGHT, buff=0.15)
        bwd_group = VGroup(bwd_dot, bwd_text).arrange(RIGHT, buff=0.15)
        upd_group = VGroup(upd_dot, upd_text).arrange(RIGHT, buff=0.15)

        cycle = VGroup(fwd_group, bwd_group, upd_group)
        cycle.arrange_in_grid(rows=3, cols=1, buff=0.5)
        cycle.move_to(loop_center)

        arrow_1 = CurvedArrow(
            fwd_group.get_bottom(),
            bwd_group.get_top(),
            angle=-TAU / 8,
            color=BLUE_ACCENT,
            stroke_width=2.0,
            tip_length=0.15,
        )
        arrow_2 = CurvedArrow(
            bwd_group.get_bottom(),
            upd_group.get_top(),
            angle=-TAU / 8,
            color=PINK,
            stroke_width=2.0,
            tip_length=0.15,
        )
        arrow_3 = CurvedArrow(
            upd_group.get_left() + LEFT * 0.15,
            fwd_group.get_left() + LEFT * 0.15,
            angle=-TAU / 4,
            color=TEAL,
            stroke_width=2.0,
            tip_length=0.15,
        )

        self.play(
            LaggedStart(
                FadeIn(fwd_group, shift=RIGHT * 0.2),
                FadeIn(arrow_1, shift=DOWN * 0.2),
                FadeIn(bwd_group, shift=RIGHT * 0.2),
                FadeIn(arrow_2, shift=DOWN * 0.2),
                FadeIn(upd_group, shift=RIGHT * 0.2),
                FadeIn(arrow_3, shift=RIGHT * 0.2),
                lag_ratio=0.4,
            ),
            run_time=1.5,
        )

        # ---------- Flash traveling around the cycle ----------
        self.play(
            ShowPassingFlash(arrow_1.copy().set_color(GREEN), time_width=0.5),
            run_time=1.0,
        )
