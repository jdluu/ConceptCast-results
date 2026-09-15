import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Function as a mapping on the coordinate plane ---
        self.clear()

        # ---- Objects ----
        # Title
        title_1 = Text(
            "Function as a mapping on the coordinate plane",
            font_size=36,
            color=WHITE,
            weight=BOLD,
        ).to_edge(UP, buff=0.4)

        # Coordinate plane
        axes = Axes(
            x_range=[-3.5, 3.5, 0.5],
            y_range=[-1, 4, 1],
            x_length=7,
            y_length=5,
            axis_config={
                "color": "#89b4fa",
                "include_tip": True,
                "include_numbers": True,
                "font_size": 18,
                "tip_length": 0.2,
            },
        ).shift(UP * 0.3)

        x_label = Text("x", font_size=26, color=WHITE).next_to(
            axes.get_x_axis(), RIGHT, buff=0.2
        )
        y_label = Text("f(x)", font_size=26, color=WHITE).next_to(
            axes.get_y_axis(), UP, buff=0.2
        )

        # The smooth function curve
        def f(x):
            return 0.35 * x**2

        curve = axes.plot(f, x_range=[-3.5, 3.5], color="#fab387", stroke_width=4)

        # Highlighted input -> output mapping
        x0 = -2.5
        in_point = axes.c2p(x0, 0)
        out_point = axes.c2p(x0, f(x0))

        input_dot = Dot(in_point, radius=0.1, color="#a6e3a1")
        input_label = Text("x", font_size=24, color="#a6e3a1").next_to(
            input_dot, DOWN, buff=0.2
        )
        v_line = DashedLine(
            in_point, out_point, color="#f38ba8", dash_length=0.15, stroke_width=2
        )
        output_dot = Dot(out_point, radius=0.1, color="#fab387")
        output_label = Text("f(x)", font_size=24, color="#fab387").next_to(
            output_dot, UR, buff=0.1
        )

        # Extra points emphasizing "every input maps"
        extra_xs = [-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]
        extra_dots = VGroup(
            *[Dot(axes.c2p(x, f(x)), radius=0.06, color="#94e2d5") for x in extra_xs]
        )

        # Main explanatory text
        main_1 = Text(
            "f assigns an output f(x)\nto every input x.",
            font_size=48,
            color="#89b4fa",
            line_spacing=0.85,
        ).to_edge(DOWN, buff=0.5)

        # ---- Animations ----
        self.play(Write(title_1), run_time=1.0)
        self.play(Create(axes), run_time=1.0)
        self.play(FadeIn(x_label), FadeIn(y_label), run_time=0.75)
        self.play(FadeIn(input_dot), FadeIn(input_label), run_time=0.75)
        self.play(
            Create(v_line),
            FadeIn(output_dot),
            FadeIn(output_label),
            run_time=1.5,
        )
        self.play(Create(curve), run_time=2.0)
        self.play(Write(main_1), run_time=1.5)
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in extra_dots], lag_ratio=0.12),
            run_time=1.5,
        )
        self.wait(2.5)
        # --- Scene 2: Step 2: Average rate of change via the secant line ---
        self.clear()

        # --- Palette ---
        BLUE_C = "#89b4fa"
        ORANGE = "#fab387"
        RED_C = "#f38ba8"
        GREEN_C = "#a6e3a1"
        TEAL = "#94e2d5"
        BG = "#181825"
        self.camera.background_color = BG

        # --- Title ---
        title = Text(
            "Average rate of change via the secant line", font_size=36, color=WHITE
        ).to_edge(UP, buff=0.6)

        # --- Axes ---
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6.75,
            y_length=4.5,
            axis_config={"color": ORANGE, "include_tip": True},
            x_axis_config={"numbers_to_include": [-2, -1, 0, 1, 2]},
            y_axis_config={"numbers_to_include": [-1, 0, 1]},
        )
        x_label = axes.get_x_axis_label(Text("x", color=ORANGE), edge=DOWN)
        y_label = axes.get_y_axis_label(Text("f(x)", color=ORANGE), edge=LEFT)

        # --- Curve: f(x) = 0.4 x^2 - 0.7 ---
        func = lambda x: 0.4 * x**2 - 0.7
        curve = axes.plot(func, x_range=[-2.6, 2.6], color=BLUE_C, stroke_width=3)

        # --- Two points on the curve ---
        A_pt = axes.c2p(-1.5, 0.2)  # f(-1.5) = 0.2
        B_pt = axes.c2p(2.0, 0.9)  # f(2.0) = 0.9
        dotA = Dot(A_pt, radius=0.09, color=GREEN_C)
        dotB = Dot(B_pt, radius=0.09, color=RED_C)
        labelA = MathTex("A", color=GREEN_C).next_to(dotA, DOWN + LEFT, buff=0.12)
        labelB = MathTex("B", color=RED_C).next_to(dotB, UP + RIGHT, buff=0.12)

        # --- Secant line through A and B ---
        secant = Line(A_pt, B_pt, color=ORANGE, stroke_width=5)

        # --- Rise / Run decomposition triangle ---
        C_pt = axes.c2p(2.0, 0.2)  # directly below B, same height as A
        run_line = DashedLine(A_pt, C_pt, color=TEAL, stroke_width=3)
        rise_line = DashedLine(C_pt, B_pt, color=RED_C, stroke_width=3)
        run_label = MathTex(r"\Delta x", color=TEAL).next_to(run_line, DOWN, buff=0.12)
        rise_label = MathTex(r"\Delta y", color=RED_C).next_to(
            rise_line, RIGHT, buff=0.12
        )

        # --- Bottom formula summary ---
        summary = Text(
            "Average rate of change = slope of secant = rise / run",
            font_size=24,
            color=WHITE,
        )
        formula = MathTex(
            r"\frac{\Delta y}{\Delta x} = \frac{0.7}{3.5} = 0.2",
            font_size=30,
            color=BLUE_C,
        )
        group = VGroup(summary, formula).arrange(DOWN, buff=0.25)
        group.move_to(DOWN * 2.7)

        # ================= ANIMATIONS =================
        self.play(Write(title), run_time=1.5)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.5)
        self.play(Create(curve), run_time=1.5)
        self.play(
            GrowFromCenter(dotA),
            GrowFromCenter(dotB),
            FadeIn(labelA),
            FadeIn(labelB),
            run_time=1.5,
        )
        self.play(Create(secant), run_time=1.5)
        self.play(
            Create(run_line),
            Create(rise_line),
            FadeIn(run_label),
            FadeIn(rise_label),
            run_time=1.5,
        )
        self.play(Write(group), run_time=1.5)
        self.wait(1.5)
        # --- Scene 3: Step 3: Shrinking the horizontal interval h ---
        self.clear()
        # Solid background (matches style guideline color)
        self.camera.background_color = "#181825"
        bg = Rectangle(
            width=30, height=20, fill_color="#181825", fill_opacity=1, stroke_width=0
        )
        self.add(bg)

        # Curated palette
        BLUE = "#89b4fa"
        ORANGE = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"
        WHITE_C = WHITE

        # ---------- Title ----------
        title = Text(
            "Shrinking the horizontal interval h",
            font_size=36,
            color=WHITE_C,
            font="Sans",
        ).move_to(UP * 3.3)
        self.play(Write(title), run_time=1.5)

        # ---------- Number Line (horizontal interval h) ----------
        nl = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            color=PINK,
            stroke_width=2.5,
        ).move_to(DOWN * 2.6)
        nl.add_numbers()
        self.play(GrowFromCenter(nl), run_time=1.0)

        x0_nl = -2.0
        h_tracker = ValueTracker(2.0)

        def nl_p1():
            return nl.n2p(x0_nl)

        def nl_p2():
            return nl.n2p(x0_nl + h_tracker.get_value())

        dot1_nl = Dot(point=nl_p1(), color=GREEN, radius=0.09)
        dot2_nl = Dot(color=GREEN, radius=0.09).add_updater(
            lambda m: m.move_to(nl_p2())
        )
        brace_nl = always_redraw(
            lambda: BraceBetweenPoints(nl_p1(), nl_p2(), direction=DOWN)
        )
        h_label_nl = always_redraw(
            lambda: MathTex("h").next_to(brace_nl, DOWN, buff=0.12).set_color(ORANGE)
        )
        x0_label_nl = MathTex("x_0").next_to(nl_p1(), UP, buff=0.2).set_color(BLUE)
        x0h_label_nl = always_redraw(
            lambda: MathTex("x_0+h").next_to(nl_p2(), UP, buff=0.2).set_color(BLUE)
        )

        self.play(
            FadeIn(dot1_nl),
            FadeIn(dot2_nl),
            FadeIn(brace_nl),
            FadeIn(h_label_nl),
            FadeIn(x0_label_nl),
            FadeIn(x0h_label_nl),
            run_time=1.5,
        )

        # ---------- Axes & curve (secant metaphor) ----------
        X_MIN, X_MAX, X_LEN = -1, 5, 6
        Y_MIN, Y_MAX, Y_LEN = 0, 5, 3.5

        axes = Axes(
            x_range=[X_MIN, X_MAX, 1],
            y_range=[Y_MIN, Y_MAX, 1],
            x_length=X_LEN,
            y_length=Y_LEN,
            axis_config={"color": TEAL, "stroke_width": 1.5},
        ).move_to(UP * 0.3)

        def f(x):
            return 0.15 * x**2

        curve = axes.plot(f, x_range=[X_MIN, X_MAX], color=BLUE, stroke_width=3)

        caption = Text(
            "As h shrinks, the secant rotates toward the tangent",
            font_size=20,
            color=TEAL,
            font="Sans",
        ).move_to(UP * 2.3)

        self.play(Create(axes), run_time=1.0)
        self.play(Create(curve), FadeIn(caption), run_time=0.5)

        # ---------- Dots & secant line ----------
        x0_val = 2.0

        def curve_p_a():
            return axes.coords_to_point(x0_val, f(x0_val))

        def curve_p_b():
            h = h_tracker.get_value()
            return axes.coords_to_point(x0_val + h, f(x0_val + h))

        dot_a = Dot(point=curve_p_a(), color=GREEN, radius=0.1)
        dot_b = Dot(color=GREEN, radius=0.1).add_updater(
            lambda m: m.move_to(curve_p_b())
        )
        secant = always_redraw(
            lambda: Line(curve_p_a(), curve_p_b(), color=ORANGE, stroke_width=4)
        )
        secant_label = always_redraw(
            lambda: (
                MathTex("secant").next_to(curve_p_b(), UR, buff=0.15).set_color(ORANGE)
            )
        )

        self.play(
            FadeIn(dot_a),
            FadeIn(dot_b),
            FadeIn(secant),
            FadeIn(secant_label),
            run_time=1.5,
        )

        # ---------- Shrink h ----------
        self.play(h_tracker.animate.set_value(0.3), run_time=4.0)

        # ---------- Tangent limit (h -> 0) ----------
        p_a = curve_p_a()
        slope_data = 0.3 * x0_val  # f'(x) = 0.3x
        sx = X_LEN / (X_MAX - X_MIN)
        sy = Y_LEN / (Y_MAX - Y_MIN)
        direction = np.array([sx, slope_data * sy, 0.0])
        tangent = Line(
            p_a - direction * 2.5,
            p_a + direction * 2.5,
            color=GREEN,
            stroke_width=4,
        )
        tangent_label = (
            MathTex("tangent\\ (h \	o 0)")
            .next_to(tangent.get_end(), UR, buff=0.15)
            .set_color(GREEN)
        )

        self.play(FadeIn(tangent), FadeIn(tangent_label), run_time=1.0)
        self.wait(1.0)
        # --- Scene 4: Step 4: The limit and the tangent line ---
        self.clear()
        self.camera.background_color = "#181825"

        GREEN = "#a6e3a1"
        BLUE = "#89b4fa"
        ORANGE = "#fab387"
        RED = "#f38ba8"
        TEAL = "#94e2d5"

        def f(x):
            return 0.2 * x**2 - 0.1 * x + 1.0

        # ---- Title ----
        title = Text("The limit and the tangent line", font_size=36, color=WHITE)
        title.move_to(UP * 3)
        self.play(Write(title), run_time=1.5)

        # ---- Axes (centered so fixed point P at x=2 sits at screen center) ----
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": BLUE, "include_tip": True, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [1, 2, 3, 4]},
        )
        self.play(Create(axes), run_time=1.5)

        # ---- Curve ----
        curve = axes.plot(lambda x: f(x), x_range=[0, 4], color=BLUE, stroke_width=4)
        curve_label = MathTex("f(x)").set_color(BLUE)
        curve_label.next_to(axes.c2p(3.7, f(3.7)), UR, buff=0.15)
        self.play(Create(curve), Write(curve_label), run_time=1.5)

        # ---- Fixed point P ----
        x0 = 2.0
        p_point = Dot(axes.c2p(x0, f(x0)), color=TEAL, radius=0.1)
        p_label = MathTex("P").set_color(TEAL)
        p_label.next_to(p_point, UL, buff=0.15)

        # ---- Dynamic secant / Q / h ----
        h_init = 1.8
        h_tracker = ValueTracker(h_init)

        secant = Line(
            axes.c2p(x0, f(x0)),
            axes.c2p(x0 + h_init, f(x0 + h_init)),
            color=ORANGE,
            stroke_width=3,
        )
        secant.set_opacity(0)

        q_dot = Dot(axes.c2p(x0 + h_init, f(x0 + h_init)), color=RED, radius=0.08)
        q_lbl = MathTex("Q").set_color(RED)
        q_lbl.next_to(q_dot, UR, buff=0.1)
        q_group = VGroup(q_dot, q_lbl)
        q_group.set_opacity(0)

        h_arrow = DoubleArrow(
            axes.c2p(x0, 0),
            axes.c2p(x0 + h_init, 0),
            color=RED,
            stroke_width=3,
            tip_length=0.15,
        )
        h_arrow.set_opacity(0)
        h_label = MathTex("h").set_color(RED)
        h_label.next_to(axes.c2p(x0 + h_init / 2, 0), DOWN, buff=0.1)
        h_label.set_opacity(0)

        def update_secant(mob):
            x2 = x0 + h_tracker.get_value()
            mob.put_start_and_end_on(axes.c2p(x0, f(x0)), axes.c2p(x2, f(x2)))

        def update_q(mob):
            x2 = x0 + h_tracker.get_value()
            p = axes.c2p(x2, f(x2))
            mob[0].move_to(p)
            mob[1].next_to(mob[0], UR, buff=0.1)

        def update_harrow(mob):
            x2 = x0 + h_tracker.get_value()
            mob.put_start_and_end_on(axes.c2p(x0, 0), axes.c2p(x2, 0))

        def update_hlabel(mob):
            x2 = x0 + h_tracker.get_value()
            mid = axes.c2p(x0 + x2 / 2, 0)
            mob.move_to(mid + DOWN * 0.3)

        secant.add_updater(update_secant)
        q_group.add_updater(update_q)
        h_arrow.add_updater(update_harrow)
        h_label.add_updater(update_hlabel)

        # ---- Tangent (revealed at end) ----
        m_t = 0.4 * x0 - 0.1  # f'(x0)
        t_p1 = axes.c2p(x0 - 2, f(x0) - 2 * m_t)
        t_p2 = axes.c2p(x0 + 2, f(x0) + 2 * m_t)
        tangent = Line(t_p1, t_p2, color=GREEN, stroke_width=4)
        tangent.set_opacity(0)
        tangent_label = MathTex(r"	ext{tangent line}").set_color(GREEN)
        tangent_label.next_to(t_p2, DR, buff=0.1)
        tangent_label.set_opacity(0)
        self.add(tangent, tangent_label)

        # ---- Main structural VGroup ----
        main_4 = VGroup(
            axes,
            curve,
            curve_label,
            p_point,
            p_label,
            secant,
            q_group,
            h_arrow,
            h_label,
            tangent,
            tangent_label,
        )
        main_4.move_to(ORIGIN)

        # ---- Reveal secant ----
        self.play(
            GrowFromCenter(p_point),
            Write(p_label),
            FadeIn(secant),
            FadeIn(q_group),
            FadeIn(h_arrow),
            FadeIn(h_label),
            run_time=1.0,
        )

        # ---- Limit: h -> 0, secant becomes tangent ----
        self.play(h_tracker.animate.set_value(0.05), run_time=4.0, rate_func=smooth)

        # ---- Reveal tangent ----
        self.play(
            FadeOut(q_group),
            FadeOut(h_arrow),
            FadeOut(h_label),
            FadeOut(secant),
            tangent.animate.set_opacity(1),
            FadeIn(tangent_label),
            run_time=1.0,
        )

        self.wait(2.0)
        # --- Scene 5: Step 5: Formal definition of the derivative ---
        self.clear()
        # --- Scene 5: Step 5: Formal definition of the derivative ---
        self.camera.background_color = "#181825"

        BLUE = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"
        TEXT_LIGHT = "#cdd6f4"

        # Custom element converter so the Table accepts already-built
        # mobjects (MathTex / Text) instead of trying to wrap them in Text(),
        # which previously caused a TypeError.
        def element_to_mobject(item, **kwargs):
            if isinstance(item, Mobject):
                return item
            return Text(str(item), **kwargs)

        # ---------- Title (spec: UP * 3, WHITE, font_size 36) ----------
        title = Text("Formal definition of the derivative", font_size=36, color=WHITE)
        title.move_to(UP * 3.0)
        self.play(Write(title), run_time=2.5)

        # ---------- Main formula ----------
        formula = MathTex(
            r"f'(x) = \lim_{h 	o 0} \frac{f(x+h) - f(x)}{h}",
            color=TEAL,
        ).scale(1.15)
        formula.move_to(UP * 1.8)
        self.play(Write(formula), run_time=3.0)

        # ---------- Supporting label under formula ----------
        sub_label = Text(
            "The limit of the difference quotient defines the derivative",
            font_size=20,
            color=TEXT_LIGHT,
        )
        sub_label.next_to(formula, DOWN, buff=0.35)
        self.play(FadeIn(sub_label, shift=DOWN), run_time=1.0)

        # ---------- Breakdown Table (with supporting labels) ----------
        sym1 = MathTex(r"f'(x)", color=PEACH)
        sym2 = MathTex(r"\lim_{h 	o 0}", color=PINK)
        sym3 = MathTex(r"\frac{f(x+h)-f(x)}{h}", color=GREEN)
        mean1 = Text("Derivative of f at x", font_size=24, color=TEXT_LIGHT)
        mean2 = Text("h approaches zero", font_size=24, color=TEXT_LIGHT)
        mean3 = Text("Difference quotient", font_size=24, color=TEXT_LIGHT)

        table = Table(
            [[sym1, mean1], [sym2, mean2], [sym3, mean3]],
            col_labels=[
                Text("Symbol", color=TEXT_LIGHT),
                Text("Meaning", color=TEXT_LIGHT),
            ],
            include_outer_lines=True,
            line_config={"color": TEAL, "stroke_width": 2},
            element_to_mobject=element_to_mobject,
        )
        table.scale(0.95).move_to(DOWN * 0.7)
        self.play(GrowFromCenter(table), run_time=3.0)

        # ---------- Highlight each data row to connect symbol -> meaning ----------
        # Build row references from the original cell mobjects already placed
        # inside the table. This avoids the unavailable table.get_row() method.
        row1 = VGroup(sym1, mean1)
        row2 = VGroup(sym2, mean2)
        row3 = VGroup(sym3, mean3)

        self.play(Circumscribe(row1, color=PEACH), run_time=1.5)
        self.play(Circumscribe(row2, color=PINK), run_time=1.5)
        self.play(Circumscribe(row3, color=GREEN), run_time=1.5)

        # ---------- Final emphasis on the full definition ----------
        self.play(Circumscribe(formula, color=TEAL), run_time=1.5)

        self.wait(1.5)
        # --- Scene 6: Step 6: Geometric meaning: instantaneous slope ---
        self.clear()
        self.camera.background_color = "#181825"

        # --- Palette ---
        BLUE = "#89b4fa"
        PEACH = "#fab387"
        GREEN = "#a6e3a1"
        LIGHT = "#cdd6f4"

        # --- Title (title_6) ---
        title = Text(
            "Geometric meaning: instantaneous slope", font_size=36, color=WHITE
        )
        title.to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.5)

        # --- Axes and curve ---
        axes = Axes(
            x_range=[-3, 7, 1],
            y_range=[0, 5, 1],
            x_length=10,
            y_length=5,
            axis_config={"color": LIGHT, "stroke_width": 2, "include_tip": True},
        )
        axes.scale(0.85).shift(DOWN * 0.3)

        def f(x):
            return 0.15 * x**2 + 0.3 * x + 1

        curve = axes.plot(f, x_range=[-3, 7], color=BLUE, stroke_width=4)
        self.play(Create(axes), Create(curve), run_time=1.5)

        # --- Point of tangency P ---
        x0 = 2.0
        P = axes.c2p(x0, f(x0))
        fixed_dot = Dot(P, color=BLUE, radius=0.08)
        p_label = MathTex("P", color=LIGHT).next_to(P, LEFT, buff=0.25)
        self.add(p_label)

        # --- Secant line whose ORIENTATION tracks the secant slope ---
        # It stays a fixed visible length but rotates toward the tangent
        # as the second point Q approaches P (h -> 0).
        h_tracker = ValueTracker(2.0)
        SECANT_LEN = 2.6

        def secant_slope():
            h = h_tracker.get_value()
            return (f(x0 + h) - f(x0)) / h

        def secant_dir():
            m = secant_slope()
            d = np.array([1.0, m, 0.0])
            return d / np.linalg.norm(d)

        def get_secant():
            d = secant_dir()
            return Line(
                P - d * SECANT_LEN / 2,
                P + d * SECANT_LEN / 2,
                color=PEACH,
                stroke_width=4,
            )

        secant = always_redraw(get_secant)

        moving_dot = Dot(color=PEACH, radius=0.08)
        moving_dot.add_updater(
            lambda m: m.move_to(
                axes.c2p(x0 + h_tracker.get_value(), f(x0 + h_tracker.get_value()))
            )
        )

        def secant_end():
            return P + secant_dir() * SECANT_LEN / 2

        secant_label = Text("secant (average slope)", font_size=22, color=PEACH)
        secant_label.add_updater(lambda m: m.next_to(secant_end(), UP, buff=0.3))

        h_label = MathTex("h", color=PEACH)
        h_label.add_updater(
            lambda m: m.next_to(moving_dot.get_center(), RIGHT, buff=0.2)
        )

        self.play(
            FadeIn(fixed_dot),
            Create(secant),
            FadeIn(moving_dot),
            FadeIn(secant_label),
            FadeIn(h_label),
            run_time=1.5,
        )

        # Animate h -> 0 : the secant rotates into the tangent
        self.play(h_tracker.animate.set_value(0.02), run_time=3.0)

        # Freeze the final (tangent-aligned) secant before fading it out
        final_secant = get_secant()
        self.remove(secant)
        self.add(final_secant)

        # --- Tangent = instantaneous slope (main_6 Arrow) ---
        slope = 0.3 * x0 + 0.3  # f'(x0)
        dir_vec = np.array([1.0, slope, 0.0])
        dir_vec = dir_vec / np.linalg.norm(dir_vec)
        TAN_LEN = 3.2
        tangent_arrow = Arrow(
            P - dir_vec * TAN_LEN / 2,
            P + dir_vec * TAN_LEN / 2,
            color=LIGHT,
            stroke_width=6,
            tip_length=0.3,
            buff=0,
        )

        tangent_label = Text("tangent (instantaneous slope)", font_size=22, color=LIGHT)
        tangent_label.next_to(tangent_arrow.get_end(), UP + RIGHT, buff=0.2)

        deriv_label = MathTex("f'(x)", color=LIGHT)
        deriv_label.next_to(tangent_arrow, RIGHT, buff=0.35)

        self.play(
            FadeOut(final_secant),
            FadeOut(moving_dot),
            FadeOut(secant_label),
            FadeOut(h_label),
            GrowFromCenter(tangent_arrow),
            FadeIn(tangent_label),
            FadeIn(deriv_label),
            run_time=2.0,
        )

        # --- Caption ---
        caption = Text(
            "At any point, it tells us how steeply\nthe function is rising or falling.",
            font_size=24,
            color=GREEN,
        )
        caption.to_edge(DOWN, buff=0.6)
        self.play(Write(caption), run_time=1.5)

        self.wait(1.0)
        # --- Scene 7: Step 7: Derivative as a new function ---
        self.clear()

        # ---------- Palette ----------
        BLUE = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"
        MUTED = "#6c7086"
        BG = "#181825"

        # ---------- Background ----------
        bg = Rectangle(width=16, height=9, color=BG, fill_opacity=1)
        bg.set_z_index(-10)
        self.add(bg)

        # ---------- Title ----------
        title_7 = Text("Derivative as a new function", font_size=36, color=WHITE)
        title_7.to_edge(UP, buff=0.25)
        self.play(Write(title_7), run_time=1.0)

        # ---------- Upper panel: original function f(x) ----------
        upper_axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1, 5, 1],
            x_length=8,
            y_length=2.6,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
            x_axis_config={"numbers_to_include": [-3, -2, -1, 1, 2, 3]},
            y_axis_config={"include_numbers": False},
        ).shift(UP * 1.9)

        orig_curve = upper_axes.plot(lambda x: 0.25 * x**2, color=BLUE, stroke_width=4)
        f_label = MathTex("f(x) = \\tfrac{1}{4}x^{2}", color=BLUE).scale(0.7)
        f_label.next_to(upper_axes.c2p(3.4, 0.25 * 3.4**2), UR, buff=0.1)

        self.play(Create(upper_axes), run_time=1.2)
        self.play(Create(orig_curve), run_time=1.3)
        self.play(Write(f_label), run_time=0.6)

        # ---------- Lower panel: derivative f'(x) ----------
        lower_axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=2.6,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
            x_axis_config={"numbers_to_include": [-3, -2, -1, 1, 2, 3]},
            y_axis_config={"include_numbers": False},
        ).shift(DOWN * 1.9)

        deriv_curve = lower_axes.plot(lambda x: 0.5 * x, color=PEACH, stroke_width=4)
        df_label = MathTex("f'(x) = \\tfrac{1}{2}x", color=PEACH).scale(0.7)
        df_label.next_to(lower_axes.c2p(3.4, 0.5 * 3.4), UR, buff=0.1)

        self.play(Create(lower_axes), run_time=1.0)
        self.play(Create(deriv_curve), run_time=1.5)
        self.play(Write(df_label), run_time=0.6)

        # ---------- Key concept text (main_7) ----------
        main_7 = Text(
            "f'(x) is a new function:\nthe slope of f(x) at each x",
            font_size=30,
            color=BLUE,
        )
        main_7.move_to(ORIGIN)
        main_bg = BackgroundRectangle(main_7, color=BG, fill_opacity=0.85, buff=0.15)
        main_bg.set_z_index(5)
        main_7.set_z_index(6)
        self.play(FadeIn(main_bg), Write(main_7), run_time=1.0)

        # ---------- Sweep: evaluate derivative at every point ----------
        t = ValueTracker(-3.2)

        dot1 = Dot(color=GREEN, radius=0.09)
        dot1.set_z_index(4)
        dot1.add_updater(
            lambda m: m.move_to(
                upper_axes.c2p(t.get_value(), 0.25 * t.get_value() ** 2)
            )
        )

        tangent = Line(color=PINK, stroke_width=3)
        tangent.set_z_index(3)

        def update_tangent(line):
            x = t.get_value()
            y = 0.25 * x**2
            p = upper_axes.c2p(x, y)
            slope = 0.5 * x
            q = upper_axes.c2p(x + 1, y + slope)
            d = q - p
            d = d / np.linalg.norm(d) * 1.4
            line.put_start_and_end_on(p - d, p + d)

        tangent.add_updater(update_tangent)

        dot2 = Dot(color=GREEN, radius=0.09)
        dot2.set_z_index(4)
        dot2.add_updater(
            lambda m: m.move_to(lower_axes.c2p(t.get_value(), 0.5 * t.get_value()))
        )

        vline = Line(color=TEAL, stroke_width=2, stroke_opacity=0.6)
        vline.set_z_index(1)

        def update_vline(line):
            x = t.get_value()
            top = upper_axes.c2p(x, 0.25 * x**2)
            bot = lower_axes.c2p(x, 0.5 * x)
            line.put_start_and_end_on(bot, top)

        vline.add_updater(update_vline)

        self.play(
            FadeOut(main_bg),
            FadeOut(main_7),
            GrowFromCenter(dot1),
            GrowFromCenter(dot2),
            FadeIn(tangent),
            FadeIn(vline),
            run_time=0.8,
        )
        self.play(t.animate.set_value(3.2), run_time=2.5, rate_func=linear)

        # ---------- Reinforce the takeaway ----------
        self.play(FadeIn(main_bg), FadeIn(main_7), run_time=0.3)
        self.play(Indicate(main_7, color=PEACH), run_time=0.7)
        # --- Scene 8: Step 8: Power rule as a computational shortcut ---
        # --- Scene 8: Step 8: Power rule as a computational shortcut ---
        PEACH = "#fab387"
        BLUE = "#89b4fa"
        GREEN = "#a6e3a1"
        PINK = "#f38ba8"
        TEAL = "#94e2d5"
        GREY = "#6c7086"

        self.camera.background_color = "#181825"

        # ---------- Title ----------
        title_8 = Text(
            "Power rule as a computational shortcut",
            font_size=36,
            color=WHITE,
        ).move_to(UP * 3)

        # ---------- Axes (the stage) ----------
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=7.0,
            y_length=4.0,
            axis_config={
                "color": PEACH,
                "include_tip": True,
                "include_numbers": True,
                "stroke_width": 2.0,
            },
        )
        x_label = axes.get_x_axis_label("x")
        x_label.set_color(PEACH)
        y_label = axes.get_y_axis_label("f(x)")
        y_label.set_color(PEACH)

        # ---------- General formula ----------
        formula = MathTex(
            r"f(x)=x^{n}",
            r"\;\longrightarrow\;",
            r"f'(x)=n\,x^{n-1}",
            font_size=34,
        ).move_to(UP * 2.4)
        formula[0].set_color(BLUE)
        formula[1].set_color(TEAL)
        formula[2].set_color(PINK)

        # ---------- Concrete example (left side) ----------
        ex1 = MathTex(r"f(x)=x^{2}", font_size=30, color=BLUE).move_to([-4.3, 1.0, 0])
        ex2 = MathTex(r"f'(x)=2x", font_size=30, color=GREEN).move_to([-4.3, 0.2, 0])
        ex_arrow = Arrow(
            ex1.get_bottom(),
            ex2.get_top(),
            color=PEACH,
            buff=0.12,
            stroke_width=2.0,
        )

        # ---------- Graphs ----------
        parabola = axes.plot(
            lambda x: x**2, x_range=[-1.4, 1.4], color=BLUE, stroke_width=3.0
        )
        deriv = axes.plot(
            lambda x: 2 * x, x_range=[-1.0, 1.0], color=GREEN, stroke_width=3.0
        )

        # ---------- Tangent / slope demonstration ----------
        # Tangent to x^2 at x=1: point (1,1), slope 2  -> line y = 2x - 1
        tangent_line = Line(
            axes.c2p(0.5, 0.0),
            axes.c2p(1.5, 2.0),
            color=TEAL,
            stroke_width=3.0,
        )
        p_dot = Dot(axes.c2p(1.0, 1.0), radius=0.08, color=BLUE)
        d_dot = Dot(axes.c2p(1.0, 2.0), radius=0.08, color=GREEN)
        v_line = DashedLine(
            axes.c2p(1.0, 0.0), axes.c2p(1.0, 2.0), color=GREY, stroke_width=2.0
        )

        final_note = Text(
            "At x=1: slope of x² is 2, and f'(1) = 2·1 = 2",
            font_size=22,
            color=TEAL,
        ).move_to(DOWN * 2.6)

        # ===================== ANIMATIONS =====================
        # 1. Title appears
        self.play(Write(title_8), run_time=1.5)

        # 2. Axes are drawn as the computational stage
        self.play(
            Create(axes),
            FadeIn(x_label, y_label),
            run_time=2.0,
        )

        # 3. The general power-rule shortcut
        self.play(Write(formula), run_time=2.0)

        # 4. Plot the original function x^2
        self.play(Create(parabola), run_time=1.5)

        # 5. Bring in the concrete example (x^2 -> 2x)
        self.play(
            FadeIn(ex1, ex2, ex_arrow, shift=LEFT * 0.2),
            run_time=1.5,
        )

        # 6. The power rule "computes" the derivative curve 2x
        self.play(Create(deriv), run_time=1.5)

        # 7. Tangent line shows the derivative equals the slope at x=1
        self.play(
            Create(tangent_line),
            GrowFromCenter(p_dot),
            GrowFromCenter(d_dot),
            Create(v_line),
            run_time=2.0,
        )

        # 8. Reinforce the computation
        self.play(Write(final_note), run_time=0.5)
        self.wait(0.5)
