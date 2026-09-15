import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Network structure and forward pass ---
        self.clear()
        self.camera.background_color = "#181825"

        # Palette (from style guidelines)
        BLUE = "#89b4fa"
        ORANGE = "#fab387"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"

        # --- Title ---
        title = Text("Network structure and forward pass", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.8)

        # --- Node positions (network sits in upper region, main text at ORIGIN) ---
        input_pos = [np.array([-3.4, y, 0]) for y in [0.6, 1.35, 2.1]]
        hidden_pos = [np.array([0.0, y, 0]) for y in [0.6, 1.05, 1.5, 1.95]]
        output_pos = [np.array([3.4, y, 0]) for y in [1.05, 1.5]]

        input_nodes = VGroup(*[Dot(p, radius=0.18, color=BLUE) for p in input_pos])
        hidden_nodes = VGroup(*[Dot(p, radius=0.18, color=ORANGE) for p in hidden_pos])
        output_nodes = VGroup(*[Dot(p, radius=0.18, color=GREEN) for p in output_pos])

        # --- Layer labels ---
        in_label = Text("Input", font_size=24, color=BLUE).move_to([-3.4, 2.55, 0])
        hid_label = Text("Hidden", font_size=24, color=ORANGE).move_to([0.0, 2.55, 0])
        out_label = Text("Output", font_size=24, color=GREEN).move_to([3.4, 2.55, 0])
        labels = VGroup(in_label, hid_label, out_label)

        # --- Weighted edges (fully connected) ---
        ih_edges = VGroup()
        for p1 in input_pos:
            for p2 in hidden_pos:
                ih_edges.add(
                    Line(p1, p2, stroke_width=1.5, color=TEAL, stroke_opacity=0.5)
                )
        ho_edges = VGroup()
        for p1 in hidden_pos:
            for p2 in output_pos:
                ho_edges.add(
                    Line(p1, p2, stroke_width=1.5, color=TEAL, stroke_opacity=0.5)
                )
        all_edges = VGroup(ih_edges, ho_edges)

        # --- Main forward-pass formula at ORIGIN ---
        main_1 = MathTex(
            r"	ext{Input}",
            r"\;\xrightarrow{\;W,\,b\;}\;",
            r"	ext{Hidden}",
            r"\;\xrightarrow{\;\sigma\;}\;",
            r"	ext{Output}",
            font_size=48,
        )
        main_1.move_to(ORIGIN)
        main_1.set_color(WHITE)
        main_1.set_color_by_tex("Input", BLUE)
        main_1.set_color_by_tex("Hidden", ORANGE)
        main_1.set_color_by_tex("Output", GREEN)

        # ================= ANIMATIONS =================
        # 1. Title (1.0s)
        self.play(Write(title), run_time=1.0)

        # 2. Nodes fade in, staggered (1.5s)
        all_node_list = list(input_nodes) + list(hidden_nodes) + list(output_nodes)
        self.play(
            LaggedStart(*[FadeIn(n) for n in all_node_list], lag_ratio=0.15),
            run_time=1.5,
        )

        # 3. Edges drawn (1.5s)
        self.play(Create(all_edges), run_time=1.5)

        # 4. Labels + formula (1.0s)
        self.play(FadeIn(labels), Write(main_1), run_time=1.0)

        # 5. Forward pass: Input -> Hidden (1.5s)
        self.play(
            ShowPassingFlash(ih_edges, time_width=0.3),
            Indicate(hidden_nodes, color=ORANGE, scale_factor=1.3),
            run_time=1.5,
        )

        # 6. Forward pass: Hidden -> Output (1.5s)
        self.play(
            ShowPassingFlash(ho_edges, time_width=0.3),
            Indicate(output_nodes, color=GREEN, scale_factor=1.3),
            run_time=1.5,
        )

        # 7. Full network pulse + emphasize formula (1.5s)
        self.play(
            ShowPassingFlash(all_edges, time_width=0.3),
            Indicate(input_nodes, color=BLUE, scale_factor=1.3),
            Circumscribe(main_1, color=TEAL, time_width=2),
            run_time=1.5,
        )

        # 8. Hold (1.0s) -> total 10.5s
        self.wait(1.0)
        # --- Scene 2: Step 2: Weighted sum and activation ---
        self.clear()
        self.camera.background_color = "#181825"

        palette_blue = "#89b4fa"
        palette_orange = "#fab387"
        palette_red = "#f38ba8"
        palette_green = "#a6e3a1"
        palette_teal = "#94e2d5"

        # 1. Title
        title_2 = Text("Weighted sum and activation", font_size=36, color=WHITE)
        title_2.move_to(UP * 3)
        self.play(FadeIn(title_2), run_time=1.0)

        # 2. Axes (weighted sum z on x, activation a on y)
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=4.5,
            axis_config={
                "color": palette_orange,
                "include_tip": True,
                "include_numbers": True,
                "tip_length": 0.2,
            },
        )
        self.play(Create(axes), run_time=1.5)

        # 3. Axis labels
        x_label = axes.get_x_axis_label(MathTex(r"z 	ext{ (weighted sum)}"))
        y_label = axes.get_y_axis_label(MathTex(r"a = \phi(z)"))
        self.play(FadeIn(x_label), FadeIn(y_label), run_time=1.0)

        # 4. Nonlinear activation curve (tanh)
        curve = axes.plot(
            lambda z: np.tanh(z),
            x_range=[-3, 3],
            color=palette_green,
        )
        self.play(Create(curve), run_time=2.0)

        # 5. Equation reminder at the bottom
        eq = MathTex(r"a = \phi(w_1 x_1 + w_2 x_2 + \dots) = \phi(z)", color=WHITE)
        eq.scale(0.8).next_to(axes, DOWN, buff=0.5)
        self.play(FadeIn(eq), run_time=0.5)

        # 6. Tracking dot that moves along x (the weighted sum) and maps to output
        z_tracker = ValueTracker(-3)

        input_dot = Dot(color=palette_blue, radius=0.1)
        output_dot = Dot(color=palette_red, radius=0.1)
        vline = DashedLine(
            axes.c2p(-3, 0),
            axes.c2p(-3, np.tanh(-3)),
            color=palette_teal,
            dash_length=0.15,
        )

        z_label = MathTex("z", color=palette_blue)
        a_label = MathTex("a", color=palette_red)

        def update_input(mob):
            mob.move_to(axes.c2p(z_tracker.get_value(), 0))

        def update_output(mob):
            z = z_tracker.get_value()
            mob.move_to(axes.c2p(z, np.tanh(z)))

        def update_line(mob):
            z = z_tracker.get_value()
            mob.put_start_and_end_on(axes.c2p(z, 0), axes.c2p(z, np.tanh(z)))

        def update_z_label(mob):
            mob.next_to(input_dot, DOWN, buff=0.2)

        def update_a_label(mob):
            mob.next_to(output_dot, LEFT, buff=0.2)

        input_dot.add_updater(update_input)
        output_dot.add_updater(update_output)
        vline.add_updater(update_line)
        z_label.add_updater(update_z_label)
        a_label.add_updater(update_a_label)

        self.add(input_dot, output_dot, vline, z_label, a_label)
        self.play(z_tracker.animate.set_value(3), run_time=2.5)

        self.wait(1.5)
        # --- Scene 3: Step 3: Loss function ---
        self.clear()
        self.camera.background_color = "#181825"

        # --- Title ---
        title = Text("Loss function", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # --- Number line (the "value axis") ---
        number_line = NumberLine(
            x_range=[-5, 5],
            length=10,
            color="#f38ba8",
            stroke_width=2.0,
            include_numbers=True,
        )
        number_line.move_to(DOWN * 1.5)

        # --- True target point ---
        true_dot = Dot(number_line.n2p(2), radius=0.12, color="#a6e3a1")
        true_label = Text("True target", font_size=24, color="#a6e3a1")
        true_label.next_to(true_dot, UP, buff=0.3)

        # --- Prediction point ---
        pred_dot = Dot(number_line.n2p(-2), radius=0.12, color="#89b4fa")
        pred_label = Text("Prediction", font_size=24, color="#89b4fa")
        pred_label.next_to(pred_dot, UP, buff=0.3)

        # --- Error / distance visualization (span on the line + brace below) ---
        error_span = Line(
            pred_dot.get_center(),
            true_dot.get_center(),
            color="#fab387",
            stroke_width=6,
        )
        brace = BraceBetweenPoints(
            pred_dot.get_center(),
            true_dot.get_center(),
            direction=DOWN,
            color="#fab387",
        )
        brace_label = brace.get_tex("|y_{pred} - y_{true}|")
        brace_label.set_color("#fab387").scale(0.7)

        # --- Loss formula summary ---
        loss_formula = MathTex(
            "L = |y_{pred} - y_{true}|",
            font_size=32,
            color="#94e2d5",
        )
        loss_formula.move_to(UP * 0.8)

        # === Animation timeline (total 9.0s) ===
        self.play(Write(title), run_time=1.5)
        self.play(Create(number_line), run_time=1.5)
        self.play(FadeIn(true_dot), Write(true_label), run_time=1.0)
        self.play(FadeIn(pred_dot), Write(pred_label), run_time=1.0)
        self.play(
            Create(brace),
            Write(brace_label),
            GrowFromCenter(error_span),
            run_time=1.0,
        )
        self.play(Write(loss_formula), run_time=1.5)
        self.play(
            Indicate(loss_formula, color="#fab387", scale_factor=1.15),
            run_time=0.75,
        )
        self.wait(0.75)
        # --- Scene 4: Step 4: Chain rule for gradients ---
        self.clear()
        self.camera.background_color = "#181825"

        # --- Palette (catppuccin-style) ---
        c_blue = "#89b4fa"
        c_orange = "#fab387"
        c_pink = "#f38ba8"
        c_green = "#a6e3a1"
        c_teal = "#94e2d5"

        # --- Title ---
        title_4 = Text("Chain rule for gradients", font_size=36, color=WHITE)
        title_4.move_to(UP * 3)
        self.play(Write(title_4), run_time=1.5)
        self.wait(0.4)

        # --- Node positions (a horizontal computational chain) ---
        pos_L = LEFT * 4.5 + UP * 0.5
        pos_a = LEFT * 1.5 + UP * 0.5
        pos_z = RIGHT * 1.5 + UP * 0.5
        pos_w = RIGHT * 4.5 + UP * 0.5

        def make_node(tex_str, pos):
            circle = Circle(radius=0.6, color=c_green, stroke_width=2.0)
            label = MathTex(tex_str, color=c_green, font_size=34)
            cell = VGroup(circle, label).move_to(pos)
            return cell

        node_L = make_node(r"L", pos_L)
        node_a = make_node(r"a", pos_a)
        node_z = make_node(r"z", pos_z)
        node_w = make_node(r"w", pos_w)
        node_cells = VGroup(node_L, node_a, node_z, node_w)

        self.play(
            LaggedStart(*[GrowFromCenter(cell) for cell in node_cells], lag_ratio=0.15),
            run_time=1.5,
        )

        # --- Arrows along the path (the main graph VGroup at ~ORIGIN) ---
        arrow1 = Arrow(
            node_L.get_right(),
            node_a.get_left(),
            color=c_blue,
            stroke_width=2.0,
            buff=0.08,
        )
        arrow2 = Arrow(
            node_a.get_right(),
            node_z.get_left(),
            color=c_blue,
            stroke_width=2.0,
            buff=0.08,
        )
        arrow3 = Arrow(
            node_z.get_right(),
            node_w.get_left(),
            color=c_blue,
            stroke_width=2.0,
            buff=0.08,
        )
        arrows = VGroup(arrow1, arrow2, arrow3)
        self.play(Create(arrows), run_time=1.3)

        # --- Local derivative labels above each edge ---
        dLda = MathTex(
            r"\frac{\partial L}{\partial a}", color=c_orange, font_size=26
        ).next_to(arrow1, UP, buff=0.2)
        dada = MathTex(
            r"\frac{\partial a}{\partial z}", color=c_orange, font_size=26
        ).next_to(arrow2, UP, buff=0.2)
        dadw = MathTex(
            r"\frac{\partial z}{\partial w}", color=c_orange, font_size=26
        ).next_to(arrow3, UP, buff=0.2)
        deriv_labels = VGroup(dLda, dada, dadw)
        self.play(
            LaggedStart(*[Write(lbl) for lbl in deriv_labels], lag_ratio=0.3),
            run_time=2.0,
        )

        # --- Chain-rule equation ---
        eq = MathTex(
            r"\frac{\partial L}{\partial w}",
            "=",
            r"\frac{\partial L}{\partial a}",
            r"\cdot",
            r"\frac{\partial a}{\partial z}",
            r"\cdot",
            r"\frac{\partial z}{\partial w}",
            color=c_teal,
            font_size=30,
        )
        eq.move_to(DOWN * 1.6)
        self.play(Write(eq), run_time=2.0)

        # --- Highlight the product of local derivatives ---
        product = VGroup(eq[2], eq[3], eq[4], eq[5], eq[6])
        self.play(
            Circumscribe(
                product, color=c_pink, shape=Rectangle, fade_out=True, buff=0.2
            ),
            run_time=1.3,
        )

        # --- Caption matching the narration ---
        caption = Text(
            "product of local derivatives along the path",
            font_size=24,
            color=c_teal,
        )
        caption.move_to(DOWN * 3.0)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=1.0)
        self.wait(2.0)
        # --- Scene 5: Step 5: Backward pass ---
        config.background_color = "#181825"
        self.clear()

        # ---- Title & subtitle ----
        title = Text("Backward pass", font_size=36, color=WHITE)
        title.move_to(UP * 3.2)
        subtitle = Text(
            "Backpropagation flows gradients backward through the network",
            font_size=20,
            color="#a6e3a1",
        )
        subtitle.next_to(title, DOWN, buff=0.25)

        # ---- Build a styled table manually (robust across manim versions) ----
        col_widths = [1.7, 3.4, 1.9, 1.9]
        row_height = 0.75
        line_color = "#89b4fa"

        def styled_cell(text, is_math, color, w):
            if is_math:
                content = MathTex(text, color=color, font_size=20)
            else:
                content = Text(text, color=color, font_size=20)
            bg = Rectangle(
                width=w,
                height=row_height,
                stroke_color=line_color,
                stroke_width=2.0,
                fill_opacity=0.0,
            )
            content.move_to(bg.get_center())
            return VGroup(bg, content)

        # Header row
        headers = ["Layer", "Computes", "Uses stored", "Produces"]
        header_row = VGroup()
        for h, w in zip(headers, col_widths):
            header_row.add(styled_cell(h, False, "#fab387", w))
        header_row.arrange(RIGHT, buff=0.0, aligned_edge=ORIGIN)

        # Data rows
        rows_data = [
            [
                "Output",
                r"\frac{\partial L}{\partial \hat{y}}",
                r"y,\ \hat{y}",
                r"\delta^{\text{out}}",
            ],
            [
                "Hidden_2",
                r"\frac{\partial L}{\partial W_2}",
                r"a^{(1)}",
                r"\delta^{(1)}",
            ],
            [
                "Hidden_1",
                r"\frac{\partial L}{\partial W_1}",
                r"a^{(0)}=x",
                r"\delta^{(0)}",
            ],
        ]
        math_flags = [False, True, True, True]
        data_rows = []
        for row in rows_data:
            rg = VGroup()
            for val, w, is_m in zip(row, col_widths, math_flags):
                rg.add(styled_cell(val, is_m, "#94e2d5", w))
            rg.arrange(RIGHT, buff=0.0, aligned_edge=ORIGIN)
            data_rows.append(rg)

        table = VGroup(header_row, *data_rows)
        table.arrange(DOWN, buff=0.0, aligned_edge=ORIGIN)
        table.scale(0.8).move_to(ORIGIN)

        # ---- Supporting label: backward gradient-flow arrow ----
        right_x = table.get_right()[0] + 1.1
        top_y = table.get_top()[1] - 0.4
        bot_y = table.get_bottom()[1] + 0.4
        flow_arrow = Arrow(
            start=[right_x, top_y, 0],
            end=[right_x, bot_y, 0],
            color="#f38ba8",
            stroke_width=6,
            buff=0.15,
            tip_length=0.3,
        )
        flow_label = MathTex(r"\nabla_\theta L", color="#f38ba8")
        flow_label.next_to(flow_arrow, RIGHT, buff=0.2)
        flow_text = Text("gradient flow", font_size=16, color="#f38ba8")
        flow_text.next_to(flow_label, DOWN, buff=0.1)
        arrow_group = VGroup(flow_arrow, flow_label, flow_text)

        # ---- Supporting label: update rule ----
        update_rule = MathTex(
            r"\theta \leftarrow \theta - \eta\,\nabla_\theta L",
            color="#a6e3a1",
        )
        update_rule.next_to(table, DOWN, buff=0.6)

        # ---- Animations ----
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)
        self.play(Create(table), run_time=2.5)

        self.play(
            AnimationGroup(
                FadeIn(arrow_group, shift=RIGHT * 0.3),
                FadeIn(update_rule, shift=DOWN * 0.2),
                lag_ratio=0,
            ),
            run_time=1.5,
        )

        # Highlight each layer's row to show backward flow
        self.play(
            LaggedStart(
                *[
                    Indicate(row, color="#fab387", scale_factor=1.12)
                    for row in data_rows
                ]
            ),
            run_time=2.0,
        )

        self.wait(1.5)
        # --- Scene 6: Step 6: Gradient descent update ---
        self.camera.background_color = "#181825"

        # Title
        title = Text("Gradient descent update", font_size=36, color=WHITE)
        title.move_to(UP * 3)

        # Axes / loss landscape
        ax = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 5.5, 1],
            x_length=8,
            y_length=4,
            axis_config={"color": "#94e2d5", "stroke_width": 2},
            tips=False,
        )
        x_label = Text("weight  w", font_size=20, color="#cdd6f4")
        x_label.next_to(ax.x_axis.get_end(), RIGHT, buff=0.15)
        y_label = Text("loss  L", font_size=20, color="#cdd6f4")
        y_label.next_to(ax.y_axis.get_end(), UP, buff=0.1)

        def loss_func(x):
            return 0.5 * x**2 + 0.5

        loss_curve = ax.plot(loss_func, color="#f38ba8", stroke_width=4)

        # Positions on the loss landscape
        x_old = 1.6
        x_new = 0.5
        p_old = ax.c2p(x_old, loss_func(x_old))
        p_new = ax.c2p(x_new, loss_func(x_new))

        # Current weight dot
        w_dot = Dot(point=p_old, radius=0.12, color="#89b4fa")
        w_label = MathTex("w", color="#89b4fa").scale(0.9)
        w_label.next_to(w_dot, UP + RIGHT, buff=0.2)

        # Gradient arrow (points uphill, positive slope on the right flank)
        grad_dir = np.array([1.0, 1.6, 0.0])
        grad_dir = grad_dir / np.linalg.norm(grad_dir) * 1.2
        grad_arrow = Arrow(
            start=p_old,
            end=p_old + grad_dir,
            color="#fab387",
            stroke_width=4,
            buff=0.05,
        )
        grad_label = MathTex(r"\nabla L", color="#fab387").scale(0.9)
        grad_label.next_to(grad_arrow.get_end(), UP + RIGHT, buff=0.1)

        # Update arrow (main_6): the negative-gradient step toward lower loss
        update_arrow = Arrow(
            start=p_old,
            end=p_new,
            color="#cdd6f4",
            stroke_width=4,
            buff=0.05,
        )
        update_label = MathTex(r"-\eta \nabla L", color="#cdd6f4").scale(0.9)
        update_label.next_to(update_arrow.get_center(), DOWN + LEFT, buff=0.2)

        # New weight label + lower loss indicator
        new_label = MathTex("w'", color="#a6e3a1").scale(0.9)
        new_label.next_to(p_new, UP + RIGHT, buff=0.2)
        lower_loss = Text("lower loss", font_size=24, color="#a6e3a1")
        lower_loss.next_to(p_new, DOWN, buff=0.4)
        formula = MathTex(r"w \leftarrow w - \eta \nabla L", color="#cdd6f4").scale(0.9)
        formula.to_edge(DOWN, buff=0.4)

        # Invisible path for the weight to slide down the curve.
        # Sample over an INCREASING x-range (x_new -> x_old) so the path is
        # always well-formed, then reverse the point order so it still runs
        # from p_old (right) to p_new (left) for MoveAlongPath.
        path = ax.plot(loss_func, x_range=[x_new, x_old], color=WHITE, stroke_opacity=0)
        path.reverse_points()

        # Animation timeline (total ~9.5s)
        self.play(Write(title), run_time=1.0)
        self.play(
            Create(ax),
            FadeIn(x_label),
            FadeIn(y_label),
            run_time=0.5,
        )
        self.play(Create(loss_curve), run_time=1.0)
        self.play(GrowFromCenter(w_dot), Write(w_label), run_time=1.0)
        self.play(GrowFromCenter(grad_arrow), Write(grad_label), run_time=1.2)
        self.play(GrowFromCenter(update_arrow), Write(update_label), run_time=1.3)
        self.play(MoveAlongPath(w_dot, path), run_time=1.2)
        self.play(
            FadeOut(w_label),
            FadeIn(new_label),
            w_dot.animate.set_color("#a6e3a1"),
            Write(lower_loss),
            Write(formula),
            run_time=1.3,
        )
        self.wait(1.0)
        # --- Scene 7: Step 7: Iterative training loop ---
        self.clear()
        self.camera.background_color = "#181825"

        # ---- Palette ----
        C_BLUE = "#89b4fa"
        C_PEACH = "#fab387"
        C_PINK = "#f38ba8"
        C_GREEN = "#a6e3a1"
        C_TEAL = "#94e2d5"

        # ---- Title ----
        title_7 = Text("Iterative training loop", color=WHITE, font_size=36)
        title_7.to_edge(UP, buff=0.5)

        # ---- Loop diagram (center-left) ----
        LOOP_C = LEFT * 0.2
        loop_circle = Circle(radius=1.7, color=C_TEAL, stroke_width=2).move_to(LOOP_C)

        angles = [PI / 2, PI / 2 + 2 * PI / 3, PI / 2 + 4 * PI / 3]
        node_pos = [LOOP_C + 1.7 * np.array([np.cos(a), np.sin(a), 0]) for a in angles]
        node_labels = ["Forward", "Backward", "Update"]
        nodes = VGroup(*[Dot(p, radius=0.13, color=C_PEACH) for p in node_pos])
        labels = VGroup()
        for p, txt in zip(node_pos, node_labels):
            lab = Text(txt, color=WHITE, font_size=22)
            direction = np.sign(p - LOOP_C)
            lab.next_to(p, direction, buff=0.35)
            labels.add(lab)

        # Cyclic arrow (near full loop) showing repeated iteration
        start_a = PI / 4 + 0.15
        end_a = start_a + TAU * 0.9
        start_p = LOOP_C + 2.15 * np.array([np.cos(start_a), np.sin(start_a), 0])
        end_p = LOOP_C + 2.15 * np.array([np.cos(end_a), np.sin(end_a), 0])
        cycle_arrow = CurvedArrow(
            start_p,
            end_p,
            angle=TAU * 0.9,
            color=C_BLUE,
            stroke_width=4,
            tip_length=0.28,
        )

        # main_7 text at center of loop
        main_7 = Text("Repeat", color=C_BLUE, font_size=48).move_to(LOOP_C)

        caption = Text(
            "Forward → Backward → Update, repeated", color=WHITE, font_size=22
        )
        caption.to_edge(DOWN, buff=0.4)

        # ---- Loss curve (right) ----
        loss_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 5, 1],
            x_length=4.0,
            y_length=2.8,
            axis_config={"color": WHITE, "stroke_width": 1.5, "include_tip": True},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).shift(RIGHT * 2.7 + DOWN * 0.2)

        curve = loss_axes.plot(
            lambda x: 4.4 * np.exp(-0.45 * x) + 0.4, color=C_PINK, stroke_width=3
        )
        loss_label = Text("Loss over epochs", color=WHITE, font_size=20)
        loss_label.next_to(loss_axes, UP, buff=0.1)

        dot_loss = Dot(loss_axes.c2p(0, 4.8), color=C_GREEN, radius=0.1)
        converge_text = Text("Converged", color=C_GREEN, font_size=24)
        converge_text.next_to(loss_axes.c2p(10, 0.4), RIGHT, buff=0.15)

        # ================= Animation Timeline (total 9.0s) =================
        self.play(Write(title_7), run_time=0.7)

        self.play(Create(loop_circle), run_time=0.9)

        self.play(
            LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.2),
            run_time=1.0,
        )

        self.play(
            FadeIn(labels, shift=UP * 0.2),
            FadeIn(caption, shift=UP * 0.2),
            run_time=0.7,
        )

        self.play(Write(main_7), run_time=0.7)

        self.play(
            Create(loss_axes),
            Create(curve),
            FadeIn(loss_label),
            FadeIn(dot_loss),
            run_time=1.0,
        )

        # Iterative loop: arrow spins twice while loss dot travels down the curve
        self.play(
            Rotate(cycle_arrow, angle=TAU * 2, about_point=LOOP_C, run_time=2.5),
            MoveAlongPath(dot_loss, curve, run_time=2.5),
            labels.animate.set_color(C_BLUE),
            run_time=2.5,
        )

        self.play(
            FadeIn(converge_text),
            Indicate(dot_loss, color=C_GREEN, scale_factor=1.6),
            run_time=0.8,
        )

        self.wait(0.7)
