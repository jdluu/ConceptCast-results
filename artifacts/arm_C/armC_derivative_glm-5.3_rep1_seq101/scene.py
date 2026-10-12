import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Functions as Mappings ---
        self.clear()
        self.camera.background_color = "#181825"
        C_TEXT = "#CDD6F4"
        C_BLUE = "#89B4fa"
        C_PEACH = "#fab387"
        C_CURVE = "#CBA6F7"
        C_GREEN = "#a6e3a1"
        C_TEAL = "#94e2d5"

        # ---------- Objects ----------
        title = Text("Functions as Mappings", font_size=40, color=C_TEXT).move_to(
            UP * 3.5
        )

        # Axes + function curve
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 4, 1],
            x_length=9,
            y_length=5.5,
            axis_config={"stroke_width": 2, "color": C_TEXT},
        ).shift(UP * 0.3)

        curve = axes.plot(lambda x: x**2 / 3, color=C_CURVE, stroke_width=4)
        curve_label = MathTex(r"y = f(x)", font_size=36, color=C_CURVE)
        curve_label.move_to(axes.c2p(2.35, 2.9))

        # Input number line
        number_line = NumberLine(
            x_range=[-3, 3, 1],
            length=9,
            stroke_width=2,
            color=C_BLUE,
            include_numbers=True,
            font_size=24,
        ).shift(DOWN * 2.9)
        nl_label = Text("x (input)", font_size=26, color=C_BLUE)
        nl_label.next_to(number_line, DOWN, buff=0.2)

        # Mapping arrows: number line -> curve
        x_vals = [-2, -1, 0, 1, 2]
        mapping_arrows = VGroup()
        input_dots = VGroup()
        output_dots = VGroup()
        for x in x_vals:
            start = number_line.n2p(x)
            end = axes.c2p(x, x**2 / 3)
            arrow = CurvedArrow(
                start,
                end,
                angle=TAU / 8,
                color=C_PEACH,
                stroke_width=2,
                tip_length=0.15,
            )
            mapping_arrows.add(arrow)
            input_dots.add(Dot(start, radius=0.07, color=C_GREEN))
            output_dots.add(Dot(end, radius=0.07, color=C_TEAL))

        map_label = Text("input \u2192 output", font_size=26, color=C_PEACH)
        map_label.move_to(RIGHT * 5.5 + DOWN * 1.2)
        map_note = MathTex(
            r"	ext{every } x \mapsto 	ext{ one } y", font_size=30, color=C_TEXT
        )
        map_note.move_to(RIGHT * 5.5 + DOWN * 1.8)

        # ---------- Animations (total = 10.0s) ----------
        self.play(Write(title), run_time=0.8)  # 0.8
        self.play(Create(number_line), Write(nl_label), run_time=1.5)  # 2.3
        self.play(FadeIn(input_dots, scale=0.5), run_time=0.7)  # 3.0
        self.play(Create(axes), run_time=1.2)  # 4.2
        self.play(Create(curve), Write(curve_label), run_time=1.5)  # 5.7
        self.play(  # 7.7
            LaggedStart(
                *[ShowPassingFlash(a, time_width=0.6) for a in mapping_arrows],
                lag_ratio=0.2,
            ),
            FadeIn(map_label, shift=LEFT * 0.4),
            run_time=2.0,
        )
        self.play(  # 8.5
            LaggedStart(
                *[GrowFromCenter(d) for d in output_dots],
                lag_ratio=0.15,
            ),
            run_time=0.8,
        )
        self.play(  # 9.5
            Indicate(curve, color=C_PEACH, scale_factor=1.02),
            FadeIn(map_note, shift=UP * 0.3),
            run_time=1.0,
        )
        self.wait(0.5)  # 10.0
        # --- Scene 2: Rate of Change as Slope ---
        self.clear()
        self.camera.background_color = "#181825"

        CATPPUCCIN_BLUE = "#89b4fa"
        CATPPUCCIN_PEACH = "#fab387"
        CATPPUCCIN_RED = "#f38ba8"
        CATPPUCCIN_TEAL = "#94e2d5"
        CATPPUCCIN_GRAY = "#A6ADC8"

        # ---------- 1. Axes ----------
        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-0.5, 3.5, 1],
            x_length=9,
            y_length=5,
            axis_config={
                "color": CATPPUCCIN_GRAY,
                "stroke_width": 2,
                "include_tip": False,
                "include_ticks": True,
            },
        )
        x_label = axes.get_x_axis_label(MathTex("x")).set_color(CATPPUCCIN_GRAY)
        y_label = axes.get_y_axis_label(MathTex("f(x)")).set_color(CATPPUCCIN_GRAY)
        axes_group = VGroup(axes, x_label, y_label)

        # ---------- 2. Parabola ----------
        parabola = axes.plot(lambda x: x**2 / 3, x_range=[-3, 3])
        parabola.set_stroke(color=CATPPUCCIN_BLUE, width=4)
        parabola_label = MathTex("f(x) = \\frac{x^2}{3}", font_size=30)
        parabola_label.set_color(CATPPUCCIN_BLUE)
        parabola_label.move_to(axes.c2p(-2.4, 2.9))

        self.play(Create(axes_group), run_time=1.2)
        self.play(Create(parabola), FadeIn(parabola_label), run_time=1.2)

        # ---------- 3. Points P and Q ----------
        a, b = 0.8, 2.6
        pP = axes.c2p(a, a**2 / 3)
        pQ = axes.c2p(b, b**2 / 3)

        point_p = Dot(pP, radius=0.08, color=CATPPUCCIN_RED)
        point_q = Dot(pQ, radius=0.08, color=CATPPUCCIN_RED)
        label_p = MathTex("P", font_size=32).set_color(CATPPUCCIN_RED)
        label_p.next_to(point_p, DL, buff=0.15)
        label_q = MathTex("Q", font_size=32).set_color(CATPPUCCIN_RED)
        label_q.next_to(point_q, UL, buff=0.15)

        self.play(
            GrowFromCenter(point_p),
            FadeIn(label_p, shift=UP * 0.2),
            run_time=0.5,
        )
        self.play(
            GrowFromCenter(point_q),
            FadeIn(label_q, shift=UP * 0.2),
            run_time=0.5,
        )

        # ---------- 4. Rise-over-run triangle ----------
        corner = axes.c2p(b, a**2 / 3)

        triangle = Polygon(pP, corner, pQ)
        triangle.set_stroke(color=CATPPUCCIN_TEAL, width=2)
        triangle.set_fill(color=CATPPUCCIN_TEAL, opacity=0.25)

        self.play(Create(triangle), run_time=1.0)

        run_brace = BraceBetweenPoints(pP, corner, DOWN)
        rise_brace = BraceBetweenPoints(corner, pQ, RIGHT)
        run_text = MathTex("\	ext{run}", font_size=28)
        run_text.set_color(CATPPUCCIN_TEAL)
        run_text.next_to(run_brace, DOWN, buff=0.1)
        rise_text = MathTex("\	ext{rise}", font_size=28)
        rise_text.set_color(CATPPUCCIN_TEAL)
        rise_text.next_to(rise_brace, RIGHT, buff=0.1)

        self.play(
            FadeIn(run_brace, shift=DOWN * 0.2),
            FadeIn(rise_brace, shift=RIGHT * 0.2),
            FadeIn(run_text),
            FadeIn(rise_text),
            run_time=0.8,
        )

        # ---------- 5. Secant line through P and Q ----------
        slope = (b**2 / 3 - a**2 / 3) / (b - a)  # = 1.13...
        intercept = a**2 / 3 - slope * a
        secant = Line(
            axes.c2p(0.0, slope * 0.0 + intercept),
            axes.c2p(3.3, slope * 3.3 + intercept),
        )
        secant.set_stroke(color=CATPPUCCIN_PEACH, width=3)

        self.play(Create(secant), run_time=1.0)

        # ---------- 6. Slope conclusion ----------
        slope_eq = MathTex(
            r"	ext{slope}",
            "=",
            r"\frac{	ext{rise}}{	ext{run}}",
            "= \\frac{2.25 - 0.21}{2.6 - 0.8}",
            r"\approx 1.13",
            font_size=30,
        )
        slope_eq.set_color_by_tex("slope", CATPPUCCIN_PEACH)
        slope_eq.set_color_by_tex("rise", CATPPUCCIN_TEAL)
        slope_bg = BackgroundRectangle(slope_eq, color="#181825", fill_opacity=0.85)
        slope_group = VGroup(slope_bg, slope_eq)
        slope_group.move_to(axes.c2p(-2.0, 3.2))

        self.play(FadeIn(slope_group), run_time=0.8)
        self.play(Indicate(secant, color=YELLOW), run_time=0.8)
        self.wait(0.7)
        # --- Scene 3: The Secant Line Approximation ---
        self.clear()

        # Palette (Catppuccin Mocha)
        BG = "#181825"
        BLUE = "#89B4FA"
        PEACH = "#FAB387"
        RED = "#F38BA8"
        GREEN = "#A6E3A1"
        TEAL = "#94E2D5"
        TXT = "#CDD6F4"
        GRAY = "#A6ADC8"

        self.camera.background_color = BG

        # ---------- Objects ----------
        axes = Axes(
            x_range=[0, 5.5, 1],
            y_range=[0, 4.5, 1],
            x_length=10,
            y_length=5.5,
            axis_config={
                "stroke_color": GRAY,
                "stroke_width": 2.0,
                "include_ticks": True,
                "tick_size": 0.08,
            },
            tips=False,
        ).shift(DOWN * 0.5)

        f = lambda x: x**2 / 6
        curve = axes.plot(f, x_range=[0.3, 5.1], color=BLUE, stroke_width=4)
        curve_label = MathTex("f(x)", color=BLUE, font_size=36).next_to(
            curve.get_end(), UR, buff=0.15
        )

        x_a = 1.0
        b = ValueTracker(4.5)

        def make_secant(bv):
            p1 = np.array(axes.c2p(x_a, f(x_a)))
            p2 = np.array(axes.c2p(bv, f(bv)))
            v = p2 - p1
            return Line(p1 - 0.18 * v, p2 + 0.18 * v, color=PEACH, stroke_width=4)

        def make_dx_brace(bv):
            return BraceBetweenPoints(
                axes.c2p(x_a, 0), axes.c2p(bv, 0), direction=DOWN, color=TEAL
            )

        def make_dy_brace(bv):
            return BraceBetweenPoints(
                axes.c2p(bv, 0), axes.c2p(bv, f(bv)), direction=RIGHT, color=TEAL
            )

        # Static (intro) versions at b = 4.5
        dotP = Dot(axes.c2p(x_a, f(x_a)), color=RED, radius=0.09)
        dotQ = Dot(axes.c2p(4.5, f(4.5)), color=RED, radius=0.09)
        secant = make_secant(4.5)
        sec_label = Text("secant", font_size=28, color=PEACH).move_to(
            secant.get_center() + UP * 0.35
        )
        dash_a = DashedLine(
            axes.c2p(x_a, 0),
            axes.c2p(x_a, f(x_a)),
            color=GRAY,
            stroke_width=2.0,
            dash_length=0.12,
        )
        dash_b = DashedLine(
            axes.c2p(4.5, 0),
            axes.c2p(4.5, f(4.5)),
            color=GRAY,
            stroke_width=2.0,
            dash_length=0.12,
        )
        dx_brace = make_dx_brace(4.5)
        dx_label = MathTex("\\Delta x", color=TEAL, font_size=34).next_to(
            dx_brace, DOWN, buff=0.12
        )
        dy_brace = make_dy_brace(4.5)
        dy_label = MathTex("\\Delta y", color=TEAL, font_size=34).next_to(
            dy_brace, RIGHT, buff=0.12
        )

        formula = MathTex(
            r"	ext{slope} = \frac{\Delta y}{\Delta x}",
            color=TXT,
            font_size=44,
        )
        sub = Text("average rate of change", font_size=24, color=GRAY)
        formula_group = VGroup(formula, sub).arrange(DOWN, buff=0.2).move_to(UP * 3)

        # ---------- Animations ----------
        # 1) Setup: axes and curve (1.5s)
        self.play(Create(axes), Create(curve), Write(curve_label), run_time=1.5)

        # 2) Secant through two points (1.0s)
        self.play(
            FadeIn(dotP, scale=0.5),
            FadeIn(dotQ, scale=0.5),
            Create(secant),
            FadeIn(sec_label),
            run_time=1.0,
        )

        # 3) Construction lines (0.8s)
        self.play(Create(dash_a), Create(dash_b), run_time=0.8)

        # 4) Delta braces (1.2s)
        self.play(
            LaggedStart(
                GrowFromCenter(dx_brace),
                FadeIn(dx_label, shift=UP * 0.1),
                GrowFromCenter(dy_brace),
                FadeIn(dy_label, shift=LEFT * 0.1),
                lag_ratio=0.25,
            ),
            run_time=1.2,
        )

        # 5) Formula (1.0s)
        self.play(Write(formula), FadeIn(sub, shift=UP * 0.2), run_time=1.0)

        # 6) Swap in dynamic tracker-driven versions and slide (2.5s)
        secant_d = always_redraw(lambda: make_secant(b.get_value()))
        dotQ_d = always_redraw(
            lambda: Dot(
                axes.c2p(b.get_value(), f(b.get_value())),
                color=RED,
                radius=0.09,
            )
        )
        dash_b_d = always_redraw(
            lambda: DashedLine(
                axes.c2p(b.get_value(), 0),
                axes.c2p(b.get_value(), f(b.get_value())),
                color=GRAY,
                stroke_width=2.0,
                dash_length=0.12,
            )
        )
        dx_brace_d = always_redraw(lambda: make_dx_brace(b.get_value()))
        dx_label_d = always_redraw(
            lambda: MathTex("\\Delta x", color=TEAL, font_size=34).next_to(
                dx_brace_d, DOWN, buff=0.12
            )
        )
        dy_brace_d = always_redraw(lambda: make_dy_brace(b.get_value()))
        dy_label_d = always_redraw(
            lambda: MathTex("\\Delta y", color=TEAL, font_size=34).next_to(
                dy_brace_d, RIGHT, buff=0.12
            )
        )
        sec_label_d = always_redraw(
            lambda: Text("secant", font_size=28, color=PEACH).move_to(
                secant_d.get_center() + UP * 0.35
            )
        )

        self.remove(
            secant, dotQ, dash_b, dx_brace, dx_label, dy_brace, dy_label, sec_label
        )
        self.add(
            secant_d,
            dotQ_d,
            dash_b_d,
            dx_brace_d,
            dx_label_d,
            dy_brace_d,
            dy_label_d,
            sec_label_d,
        )

        self.play(b.animate.set_value(2.0), run_time=2.5, rate_func=smooth)

        # 7) "Misses what happens in between": flash the curve segment (1.0s)
        seg = axes.plot(f, x_range=[x_a, b.get_value()], color=GREEN, stroke_width=9)
        self.play(
            ShowPassingFlash(seg, time_width=0.4),
            Indicate(sub, scale_factor=1.15, color=GREEN),
            run_time=1.0,
        )

        # 8) Hold (1.0s)
        self.wait(1.0)
        # --- Scene 4: Limit and Shrinking the Interval ---
        self.clear()
        self.camera.background_color = "#181825"

        # ---- Palette (Catppuccin Mocha) ----
        curve_col = "#89B4FA"
        secant_col = "#FAB387"
        point_col = "#F38BA8"
        label_col = "#CBA6F7"
        axes_col = "#A6ADC8"
        text_col = "#CDD6F4"
        green_col = "#A6E3A1"

        # ---- Objects ----
        axes = Axes(
            x_range=[-2.5, 3.5, 1],
            y_range=[-1.5, 3.5, 1],
            x_length=9,
            y_length=5.5,
            axis_config={"color": axes_col, "stroke_width": 2.0},
            tips=False,
        ).shift(DOWN * 0.3)

        f = lambda x: 0.3 * x**2 + 0.2
        curve = axes.plot(f, x_range=[-2.5, 3.3], color=curve_col, stroke_width=4)

        a = 1.5  # x-coordinate of the fixed point P
        p_pt = axes.c2p(a, f(a))
        P = Dot(p_pt, color=point_col, radius=0.1)
        p_label = MathTex("P", color=point_col, font_size=42)
        p_label.next_to(P, UL, buff=0.12)

        limit_label = MathTex("h \	o 0", color=label_col, font_size=64)
        limit_label.to_edge(UP, buff=0.35)

        # Legend for the secant family (storyboard label)
        legend_line = Line(
            ORIGIN,
            RIGHT * 0.6,
            color=secant_col,
            stroke_width=4,
            stroke_opacity=0.7,
        )
        legend_text = Text("secants as h shrinks", color=secant_col, font_size=28)
        legend = VGroup(legend_line, legend_text).arrange(RIGHT, buff=0.2)
        legend.to_corner(UL, buff=0.5)

        # ---- Secant helper: line through P and (a+h, f(a+h)), extended ----
        def secant(h):
            q = axes.c2p(a + h, f(a + h))
            d = q - p_pt
            line = Line(p_pt - d * 0.55, p_pt + d * 1.25, color=secant_col)
            line.set_stroke(opacity=0.7, width=4)
            return line, q

        # ---- 1) Setup: axes, curve, fixed point P (1.9 s) ----
        self.play(FadeIn(axes, run_time=1.0), Create(curve, run_time=1.4))
        self.play(
            GrowFromCenter(P, run_time=0.5),
            FadeIn(p_label, run_time=0.5),
        )

        # ---- 2) Successive secants as h shrinks (3 x 1.2 = 3.6 s) ----
        # h = 0.5
        line0, q0 = secant(0.5)
        h_text = MathTex("h = 0.5", color=secant_col, font_size=44)
        h_text.next_to(q0, UR, buff=0.15)
        self.play(
            Create(line0, run_time=1.0),
            Write(h_text, run_time=0.8),
            FadeIn(legend, run_time=0.5),
        )
        self.play(GrowFromCenter(Dot(q0, color=secant_col, radius=0.07), run_time=0.2))

        # h = 0.25
        line1, q1 = secant(0.25)
        h_text1 = MathTex("h = 0.25", color=secant_col, font_size=44)
        h_text1.next_to(q1, UR, buff=0.15)
        self.play(
            ReplacementTransform(line0, line1, run_time=1.0),
            Transform(h_text, h_text1, run_time=0.8),
        )
        self.play(GrowFromCenter(Dot(q1, color=secant_col, radius=0.07), run_time=0.2))

        # h = 0.1
        line2, q2 = secant(0.1)
        h_text2 = MathTex("h = 0.1", color=secant_col, font_size=44)
        h_text2.next_to(q2, UR, buff=0.15)
        self.play(
            ReplacementTransform(line1, line2, run_time=1.0),
            Transform(h_text, h_text2, run_time=0.8),
        )
        self.play(GrowFromCenter(Dot(q2, color=secant_col, radius=0.07), run_time=0.2))

        # ---- 3) Limit: the secant converges to the tangent (1.5 s) ----
        m = 0.6 * a  # slope of f at a (derivative)
        tangent = Line(
            axes.c2p(a - 1.8, f(a) - m * 1.8),
            axes.c2p(a + 1.9, f(a) + m * 1.9),
            color=green_col,
            stroke_width=5,
        )
        self.play(
            ReplacementTransform(line2, tangent, run_time=1.2),
            Write(limit_label, run_time=1.2),
        )
        slope_label = MathTex("f'(a)", color=green_col, font_size=44)
        slope_label.next_to(tangent.get_end(), UR, buff=0.12)
        self.play(FadeIn(slope_label, run_time=0.3))

        # ---- 4) Formal statement of the limit (1.7 s) ----
        limit_def = MathTex(
            r"f'(a)",
            r"= \lim_{h 	o 0}",
            r"\frac{f(a+h) - f(a)}{h}",
        )
        limit_def[0].set_color(green_col)
        limit_def[1].set_color(label_col)
        limit_def[2].set_color(text_col)
        limit_def.scale(0.9).to_edge(DOWN, buff=0.3)
        self.play(Write(limit_def, run_time=1.7))

        # ---- 5) Hold on the final picture ----
        self.wait(2.3)
        # --- Scene 5: The Tangent Line and Instantaneous Rate ---
        self.clear()
        self.camera.background_color = "#181825"

        BLUE_C = "#89b4fa"
        ORANGE_C = "#fab387"
        RED_C = "#f38ba8"
        GREEN_C = "#a6e3a1"
        TEAL_C = "#94e2d5"
        GRAY_C = "#A6ADC8"

        # ---------- Objects ----------
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={
                "color": GRAY_C,
                "stroke_width": 2.0,
                "include_tip": True,
                "tip_length": 0.2,
            },
        )
        axes.shift(DOWN * 0.4)
        x_label = axes.get_x_axis_label("x", direction=UR).set_color(GRAY_C)
        y_label = axes.get_y_axis_label("f(x)", direction=UR).set_color(GRAY_C)

        f = lambda x: 0.3 * x**2 - 0.5 * x + 1.2
        fprime = lambda x: 0.6 * x - 0.5
        curve = axes.plot(f, x_range=[0, 4.4], color=BLUE_C, stroke_width=4)

        x0 = 2.0
        p0 = axes.c2p(x0, f(x0))

        glow = Circle(
            radius=0.3, color=RED_C, stroke_width=0, fill_opacity=0.35
        ).move_to(p0)
        point = Dot(p0, radius=0.12, color=RED_C)
        glow_group = VGroup(glow, point)

        # Secant helper: line through (x0, f(x0)) and (x0+h, f(x0+h))
        def secant_line(h):
            p1 = axes.c2p(x0 + h, f(x0 + h))
            d = p1 - p0
            return Line(
                p0 - 0.4 * d,
                p0 + 2.2 * d,
                color=ORANGE_C,
                stroke_width=3,
                stroke_opacity=0.8,
            )

        tangent = TangentLine(
            curve, alpha=x0 / 4.4, length=7, color=ORANGE_C, stroke_width=4
        )
        tang_label = Text("tangent", font_size=30, color=ORANGE_C)
        tang_label.next_to(tangent.get_end(), UL, buff=0.1)

        # Slope triangle riding on the tangent
        dx = 1.2
        pA = p0
        pB = axes.c2p(x0 + dx, f(x0))
        pC = axes.c2p(x0 + dx, f(x0) + fprime(x0) * dx)
        triangle = Polygon(
            pA,
            pB,
            pC,
            color=GREEN_C,
            stroke_width=3,
            fill_color=GREEN_C,
            fill_opacity=0.25,
        )
        br_dx = BraceBetweenPoints(pA, pB, DOWN).set_color(TEAL_C)
        br_dy = BraceBetweenPoints(pB, pC, RIGHT).set_color(TEAL_C)
        dx_lab = MathTex("dx", font_size=32, color=TEAL_C).next_to(
            br_dx, DOWN, buff=0.1
        )
        dy_lab = MathTex("dy", font_size=32, color=TEAL_C).next_to(
            br_dy, RIGHT, buff=0.1
        )

        slope_text = MathTex(
            r"	ext{slope} = \frac{dy}{dx} = f'(2)", font_size=42, color=GREEN_C
        )
        slope_text.to_edge(UP, buff=0.4).shift(LEFT * 2)

        caption = Text("one touch, one slope", font_size=28, color=GRAY_C)
        caption.to_edge(UP, buff=0.15).shift(RIGHT * 3)

        # ---------- Animations ----------
        self.play(Create(axes), run_time=0.8)
        self.play(Create(curve), FadeIn(x_label), FadeIn(y_label), run_time=0.9)
        self.play(FadeIn(glow_group, scale=0.3), run_time=0.6)

        # Secant line slides toward tangency -> becomes the tangent
        sec1 = secant_line(2.0)
        self.play(GrowFromCenter(sec1), run_time=0.5)
        self.play(Transform(sec1, secant_line(1.0)), run_time=0.5)
        self.play(Transform(sec1, secant_line(0.4)), run_time=0.5)
        self.play(Transform(sec1, tangent), run_time=0.6)

        self.play(FadeIn(tang_label, shift=0.3 * UR), run_time=0.6)

        # Instantaneous slope triangle
        self.play(Create(triangle), run_time=0.9)
        self.play(
            FadeIn(br_dx), FadeIn(dx_lab), FadeIn(br_dy), FadeIn(dy_lab), run_time=0.8
        )
        self.play(Write(slope_text), run_time=1.1)

        # Glow pulse on the point of tangency
        pulse = Circle(radius=0.55, color=RED_C, stroke_width=3).move_to(p0)
        self.play(Create(pulse), run_time=0.4)
        self.play(FadeOut(pulse), FadeOut(glow), run_time=0.4)

        self.play(FadeIn(caption, shift=0.3 * DOWN), run_time=0.4)
        self.wait(0.5)
        # --- Scene 6: The Derivative Definition ---
        self.clear()
        self.camera.background_color = "#181825"

        TEXT = "#CDD6F4"
        BLUE = "#89B4FA"
        PEACH = "#FAB387"
        RED = "#F38BA8"
        GREEN = "#A6E3A1"
        TEAL = "#94E2D5"
        PURPLE = "#CBA6F7"
        GREY = "#A6ADC8"

        # ---------- geometry (mini axes, right side) ----------
        x0 = 1.4
        f = lambda t: 0.25 * t * t
        fx0 = f(x0)
        slope = 0.5 * x0

        h_tracker = ValueTracker(1.8)

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=3,
            y_length=2.6,
            axis_config={
                "stroke_color": BLUE,
                "stroke_width": 2,
                "include_ticks": False,
                "include_tip": False,
            },
        ).shift(RIGHT * 3.5 + DOWN * 0.1)

        curve = axes.plot(f, x_range=[0, 3.7], color=GREEN, stroke_width=3)

        p_pt = axes.c2p(x0, fx0)

        def q_pt():
            hv = h_tracker.get_value()
            return axes.c2p(x0 + hv, f(x0 + hv))

        def r_pt():
            hv = h_tracker.get_value()
            return axes.c2p(x0 + hv, fx0)

        def secant_endpoints():
            q = q_pt()
            v = q - p_pt
            return p_pt - 0.3 * v, q + 0.22 * v

        dot_p = Dot(p_pt, radius=0.055, color=TEAL)
        dot_q = Dot(q_pt(), radius=0.055, color=PEACH)

        run_seg = Line(p_pt, r_pt(), color=PURPLE, stroke_width=4)
        rise_seg = Line(r_pt(), q_pt(), color=PEACH, stroke_width=4)

        s0, e0 = secant_endpoints()
        secant = Line(s0, e0, color=RED, stroke_width=2.5)

        run_label = MathTex("h", font_size=30, color=PURPLE).next_to(
            run_seg, DOWN, buff=0.12
        )
        rise_label = MathTex("f(x+h)-f(x)", font_size=26, color=PEACH).next_to(
            rise_seg, RIGHT, buff=0.15
        )
        p_label = MathTex("f(x)", font_size=26, color=TEAL).next_to(
            dot_p, LEFT, buff=0.15
        )
        q_label = MathTex("f(x+h)", font_size=26, color=PEACH).next_to(
            dot_q, UL, buff=0.1
        )

        # ---------- the difference quotient formula ----------
        lhs = MathTex("f'(x)", "=", color=TEXT)
        lim_part = MathTex(
            r"\lim_{h	o 0}", substrings_to_isolate=[r"h	o 0"], color=TEXT
        )
        lim_part.set_color_by_tex(r"h	o 0", PURPLE)
        num = MathTex("f(x+h)", "-", "f(x)", color=TEXT)
        num.get_part_by_tex("f(x+h)").set_color(PEACH)
        num.get_part_by_tex("f(x)").set_color(TEAL)
        den = MathTex("h", color=PURPLE)
        bar = Line(LEFT, RIGHT, color=GREY, stroke_width=2).set_width(num.width * 0.9)
        frac = VGroup(num, bar, den).arrange(DOWN, buff=0.18)
        formula = (
            VGroup(lhs, lim_part, frac)
            .arrange(RIGHT, buff=0.3)
            .move_to(UP * 2 + LEFT * 0.4)
        )

        # ---------- terms + linking arrows ----------
        fxh_term = MathTex("f(x+h)", color=PEACH).move_to(LEFT * 2.5 + DOWN * 2)
        fx_term = MathTex("f(x)", color=TEAL).move_to(DOWN * 2)
        h_term = MathTex(r"h 	o 0", color=PURPLE).move_to(RIGHT * 2.5 + DOWN * 2)

        fxh_part = num.get_part_by_tex("f(x+h)")
        fx_part = num.get_part_by_tex("f(x)")

        a1 = Arrow(
            fxh_term.get_top() + UP * 0.05,
            fxh_part.get_bottom() + DOWN * 0.12,
            buff=0.1,
            color=GREY,
            stroke_width=2,
            tip_length=0.18,
        )
        a2 = Arrow(
            fx_term.get_top() + UP * 0.05,
            fx_part.get_bottom() + DOWN * 0.12,
            buff=0.1,
            color=GREY,
            stroke_width=2,
            tip_length=0.18,
        )
        a3 = Arrow(
            h_term.get_top() + UP * 0.05,
            den.get_bottom() + DOWN * 0.12,
            buff=0.1,
            color=GREY,
            stroke_width=2,
            tip_length=0.18,
        )

        # ---------- timeline (total 11.0 s) ----------
        self.play(
            LaggedStart(
                FadeIn(axes, shift=DOWN * 0.3),
                Create(curve),
                Create(secant),
                FadeIn(dot_p, scale=0.5),
                FadeIn(dot_q, scale=0.5),
                Create(run_seg),
                Create(rise_seg),
                LaggedStart(
                    FadeIn(run_label),
                    FadeIn(rise_label),
                    FadeIn(p_label),
                    FadeIn(q_label),
                    lag_ratio=0.1,
                ),
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )
        self.wait(0.3)

        self.play(
            LaggedStart(
                Write(lhs), Write(lim_part), GrowFromCenter(frac), lag_ratio=0.5
            ),
            run_time=2.0,
        )
        self.wait(0.2)

        self.play(
            LaggedStart(
                FadeIn(fxh_term, shift=UP * 0.3),
                FadeIn(fx_term, shift=UP * 0.3),
                FadeIn(h_term, shift=UP * 0.3),
                Create(a1),
                Create(a2),
                Create(a3),
                lag_ratio=0.2,
            ),
            run_time=1.5,
        )

        self.play(
            Indicate(h_term, color=PURPLE, scale_factor=1.3),
            Indicate(run_label, color=PURPLE, scale_factor=1.3),
            run_time=0.8,
        )

        # ---------- shrink h -> 0: secant becomes tangent ----------
        dot_q.add_updater(lambda m: m.move_to(q_pt()))
        run_seg.add_updater(lambda m: m.put_start_and_end_on(p_pt, r_pt()))
        rise_seg.add_updater(lambda m: m.put_start_and_end_on(r_pt(), q_pt()))
        secant.add_updater(lambda m: m.put_start_and_end_on(*secant_endpoints()))
        run_label.add_updater(lambda m: m.next_to(run_seg, DOWN, buff=0.12))
        rise_label.add_updater(lambda m: m.next_to(rise_seg, RIGHT, buff=0.15))
        q_label.add_updater(lambda m: m.next_to(dot_q, UL, buff=0.1))

        self.play(h_tracker.animate.set_value(0.01), run_time=3.0, rate_func=smooth)

        tangent = Line(
            axes.c2p(x0 - 1.5, fx0 - 1.5 * slope),
            axes.c2p(x0 + 1.2, fx0 + 1.2 * slope),
            color=RED,
            stroke_width=4,
        )

        tri_group = VGroup(run_seg, rise_seg, dot_q, run_label, rise_label, q_label)
        for mob in tri_group:
            mob.clear_updaters()
        self.play(Create(tangent), FadeOut(tri_group), run_time=0.8)

        self.play(Circumscribe(formula, color=GREEN, buff=0.15), run_time=1.0)
        self.wait(0.4)
        # --- Scene 7: Derivative as a New Function ---
        self.clear()
        self.camera.background_color = "#181825"

        # Palette (style guidelines)
        COL_AXES = "#a6adc8"
        COL_F = "#89b4fa"
        COL_TAN = "#fab387"
        COL_DF = "#a6e3a1"
        COL_DOT = "#f38ba8"
        COL_ACCENT = "#94e2d5"

        # Functions
        f = lambda x: x**2 / 4
        df = lambda x: x / 2

        # --- Top axes: f(x) ---
        top_axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-1, 4, 1],
            x_length=8.0,
            y_length=2.6,
            axis_config={
                "color": COL_AXES,
                "stroke_width": 2.0,
                "include_tip": False,
                "include_ticks": False,
            },
        ).move_to(UP * 1.75)

        # --- Bottom axes: f'(x) ---
        bottom_axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=8.0,
            y_length=2.6,
            axis_config={
                "color": COL_AXES,
                "stroke_width": 2.0,
                "include_tip": False,
                "include_ticks": False,
            },
        ).move_to(DOWN * 1.95)

        top_labels = top_axes.get_axis_labels(
            MathTex("x").set_color(COL_AXES),
            MathTex("f(x)").set_color(COL_F),
        ).scale(0.6)

        bottom_labels = bottom_axes.get_axis_labels(
            MathTex("x").set_color(COL_AXES),
            MathTex("f'(x)").set_color(COL_DF),
        ).scale(0.6)

        # --- Curves ---
        top_curve = top_axes.plot(f, x_range=[-4, 4], color=COL_F, stroke_width=4)
        derivative_curve = bottom_axes.plot(
            df, x_range=[-5, 5], color=COL_DF, stroke_width=4
        )

        # --- Tangent family at regular intervals + slope dots ---
        x_vals = [-3, -1.5, 0, 1.5, 3]
        tangents = VGroup()
        slope_dots = VGroup()
        for x0 in x_vals:
            m = df(x0)
            y0 = f(x0)
            dx = 0.7
            tangents.add(
                Line(
                    top_axes.c2p(x0 - dx, y0 - dx * m),
                    top_axes.c2p(x0 + dx, y0 + dx * m),
                    color=COL_TAN,
                    stroke_width=3,
                )
            )
            slope_dots.add(Dot(bottom_axes.c2p(x0, m), radius=0.09, color=COL_DOT))

        # Equations
        f_eq = MathTex("f(x) = \\frac{x^2}{4}", color=COL_F).scale(0.55)
        f_eq.move_to(top_axes.c2p(-3.4, 3.1))
        df_eq = MathTex("f'(x) = \\frac{x}{2}", color=COL_DF).scale(0.55)
        df_eq.move_to(bottom_axes.c2p(-3.7, 1.7))

        # --- Animation sequence (total = 9.0 s) ---
        # 1) Both coordinate systems fade in (1.2 s)
        self.play(
            Create(top_axes),
            Create(bottom_axes),
            Write(top_labels),
            Write(bottom_labels),
            run_time=1.2,
        )

        # 2) Original curve drawn (1.0 s)
        self.play(
            Create(top_curve),
            FadeIn(f_eq, shift=RIGHT * 0.2),
            run_time=1.0,
        )

        # 3) Tangents appear at regular intervals while their slope values
        #    land as dots on the lower plot (2.8 s)
        pairs = [
            AnimationGroup(Create(t), GrowFromCenter(d))
            for t, d in zip(tangents, slope_dots)
        ]
        self.play(LaggedStart(*pairs, lag_ratio=0.25), run_time=2.8)

        # 4) The derivative curve emerges through the slope dots (1.2 s)
        self.play(
            Create(derivative_curve),
            FadeIn(df_eq, shift=RIGHT * 0.2),
            run_time=1.2,
        )

        # 5) Emphasize: the slopes form a brand-new function (0.8 s)
        self.play(
            AnimationGroup(
                Indicate(derivative_curve, color=COL_ACCENT, scale_factor=1.05),
                Indicate(slope_dots, color=COL_ACCENT, scale_factor=1.4),
            ),
            run_time=0.8,
        )

        self.wait(2.0)
        # --- Scene 8: Power Rule Example ---
        self.clear()
        self.camera.background_color = "#181825"

        SURFACE = "#A6ADC8"
        BLUE_C = "#89B4FA"
        PEACH = "#FAB387"
        ROSE = "#F38BA8"
        GREEN = "#A6E3A1"
        MAUVE = "#CBA6F7"

        # ---------- top plot: f(x) = x^2 ----------
        top_axes = Axes(
            x_range=[-0.8, 4.2, 1],
            y_range=[-0.6, 4.6, 1],
            x_length=7.0,
            y_length=3.2,
            axis_config={"color": SURFACE, "stroke_width": 2.0, "include_tip": False},
        ).shift(UP * 1.8)
        top_axes.get_x_axis().add_numbers([1, 3], font_size=22)

        top_label = MathTex("f(x) = x^2", font_size=34, color=BLUE_C)
        top_label.move_to(top_axes.c2p(1.05, 4.0))

        x_sq = top_axes.plot(
            lambda x: x**2 / 3,
            x_range=[-0.75, 3.62],
            color=BLUE_C,
            stroke_width=3.5,
        )

        # tangent at x = 1 (slope 2x/3 in the scaled coordinates)
        p1 = top_axes.c2p(1, 1.0 / 3.0)
        tan1 = Line(
            top_axes.c2p(1 - 1.05, 1.0 / 3.0 - 1.05 * (2.0 / 3.0)),
            top_axes.c2p(1 + 1.05, 1.0 / 3.0 + 1.05 * (2.0 / 3.0)),
            color=PEACH,
            stroke_width=3.5,
        )
        dot_t1 = Dot(p1, radius=0.07, color=PEACH)
        tan1_label = Text("slope = 2", font_size=24, color=PEACH)
        tan1_label.next_to(p1, UL, buff=0.2)

        # tangent at x = 3
        p2 = top_axes.c2p(3, 3.0)
        tan2 = Line(
            top_axes.c2p(3 - 0.55, 3.0 - 0.55 * 2.0),
            top_axes.c2p(3 + 0.55, 3.0 + 0.55 * 2.0),
            color=ROSE,
            stroke_width=3.5,
        )
        dot_t2 = Dot(p2, radius=0.07, color=ROSE)
        tan2_label = Text("slope = 6", font_size=24, color=ROSE)
        tan2_label.next_to(p2, RIGHT, buff=0.2)

        # ---------- bottom plot: f'(x) = 2x ----------
        bot_axes = Axes(
            x_range=[-0.8, 4.2, 1],
            y_range=[-0.6, 3.0, 1],
            x_length=7.0,
            y_length=2.4,
            axis_config={"color": SURFACE, "stroke_width": 2.0, "include_tip": False},
        ).shift(DOWN * 2.2)
        bot_axes.get_x_axis().add_numbers([1, 3], font_size=22)

        bot_label = MathTex("f'(x) = 2x", font_size=34, color=GREEN)
        bot_label.move_to(bot_axes.c2p(1.35, 2.35))

        derived = bot_axes.plot(
            lambda x: 2 * x / 3,
            x_range=[-0.5, 3.7],
            color=GREEN,
            stroke_width=3.5,
        )

        # value dots on the derived line: (1, 2) and (3, 6)
        d1 = Dot(bot_axes.c2p(1, 2.0 / 3.0), radius=0.08, color=MAUVE)
        l1 = MathTex("(1,\\,2)", font_size=28, color=MAUVE)
        l1.next_to(d1, UL, buff=0.15)
        g1 = VGroup(d1, l1)

        d2 = Dot(bot_axes.c2p(3, 2.0), radius=0.08, color=MAUVE)
        l2 = MathTex("(3,\\,6)", font_size=28, color=MAUVE)
        l2.next_to(d2, UR, buff=0.15)
        g2 = VGroup(d2, l2)

        # dashed connectors aligning the x-values between the two plots
        dashes = VGroup()
        for xv in (1, 3):
            sx = top_axes.c2p(xv, 0)[0]
            dashes.add(
                DashedLine(
                    [sx, 0.38, 0],
                    [sx, -0.92, 0],
                    dash_length=0.12,
                    stroke_width=2,
                    color=SURFACE,
                    stroke_opacity=0.6,
                )
            )

        # verification chip
        check_group = VGroup(
            MathTex("\\checkmark", font_size=36, color=GREEN),
            Text("geometry matches the rule", font_size=22, color=GREEN),
        ).arrange(RIGHT, buff=0.2)
        check_group.move_to([2.1, -3.55, 0])

        # ---------- animation ----------
        self.play(Create(top_axes), Write(top_label), run_time=1.0)
        self.play(Create(x_sq), run_time=0.9)
        self.wait(0.3)

        self.play(Create(tan1), FadeIn(dot_t1), Write(tan1_label), run_time=1.0)
        self.wait(0.3)
        self.play(Create(tan2), FadeIn(dot_t2), Write(tan2_label), run_time=1.0)
        self.wait(0.7)

        self.play(Create(bot_axes), Write(bot_label), run_time=1.0)
        self.play(Create(derived), run_time=0.8)

        self.play(
            LaggedStart(
                GrowFromCenter(g1),
                GrowFromCenter(g2),
                Create(dashes[0]),
                Create(dashes[1]),
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )

        self.play(
            LaggedStart(
                Indicate(g1, scale_factor=1.15),
                Indicate(g2, scale_factor=1.15),
                lag_ratio=0.3,
            ),
            FadeIn(check_group, shift=UP * 0.2),
            run_time=0.9,
        )
        self.wait(1.1)
        # --- Scene 9: Applications of Derivatives ---
        self.clear()
        self.camera.background_color = "#181825"

        TEXT_MAIN = "#CDD6F4"
        CURVE = "#89B4FA"
        PEAK = "#F38BA8"
        VALLEY = "#A6E3A1"
        TEAL = "#94E2D5"
        FOOTER = "#CBA6F7"
        AXES_GRAY = "#A6ADC8"

        f = lambda x: x**3 / 12.0 - x

        # --- 1. Title + axes (1.0s) ---
        title = Text(
            "Applications of Derivatives", font_size=38, weight=BOLD, color=TEXT_MAIN
        )
        title.move_to(UP * 3.4)

        axes = Axes(
            x_range=[-5.2, 5.2, 1],
            y_range=[-4.2, 4.2, 1],
            x_length=9.6,
            y_length=5.2,
            axis_config={
                "color": AXES_GRAY,
                "stroke_width": 2.0,
                "include_ticks": False,
            },
        )
        axes_label = MathTex("f(x)", font_size=32, color=AXES_GRAY)
        axes_label.next_to(axes.y_axis.get_top(), RIGHT, buff=0.2)

        self.play(FadeIn(title, shift=DOWN * 0.3), Create(axes), run_time=1.0)
        self.play(FadeIn(axes_label), run_time=0.3)

        # --- 2. Cubic curve (1.3s) ---
        curve = axes.plot(f, x_range=[-4.8, 4.8], color=CURVE, stroke_width=5)
        self.play(Create(curve), run_time=1.3)
        self.wait(0.2)

        # --- 3. Maximum (0.9s): true critical point x = -2, f(-2) = 4/3 ---
        x_max, x_min = -2.0, 2.0
        y_max, y_min = f(x_max), f(x_min)

        peak_dot = Dot(axes.coords_to_point(x_max, y_max), radius=0.11, color=PEAK)
        peak_tan = DashedLine(
            axes.coords_to_point(x_max - 1.4, y_max),
            axes.coords_to_point(x_max + 1.4, y_max),
            color=PEAK,
            stroke_width=3,
            dash_length=0.14,
        )
        peak_label = MathTex(r"	ext{maximum: } f'(x)=0", font_size=30, color=PEAK)
        peak_label.next_to(peak_tan, UP, buff=0.15)

        self.play(GrowFromCenter(peak_dot), Create(peak_tan), run_time=0.7)
        self.play(FadeIn(peak_label, shift=UP * 0.15), run_time=0.2)

        # --- 4. Minimum (0.9s): x = +2, f(2) = -4/3 ---
        valley_dot = Dot(axes.coords_to_point(x_min, y_min), radius=0.11, color=VALLEY)
        valley_tan = DashedLine(
            axes.coords_to_point(x_min - 1.4, y_min),
            axes.coords_to_point(x_min + 1.4, y_min),
            color=VALLEY,
            stroke_width=3,
            dash_length=0.14,
        )
        valley_label = MathTex(
            r"	ext{minimum: } f'(x)=0", font_size=30, color=VALLEY
        )
        valley_label.next_to(valley_tan, DOWN, buff=0.15)

        self.play(GrowFromCenter(valley_dot), Create(valley_tan), run_time=0.7)
        self.play(FadeIn(valley_label, shift=DOWN * 0.15), run_time=0.2)

        # --- 5. Rising arrows (0.8s): f' > 0 on outer branches ---
        arrow_l = Arrow(
            axes.coords_to_point(-4.6, f(-4.6)),
            axes.coords_to_point(-3.9, f(-3.9)),
            buff=0,
            color=TEAL,
            stroke_width=6,
        ).shift(LEFT * 0.25 + UP * 0.1)
        arrow_r = Arrow(
            axes.coords_to_point(3.9, f(3.9)),
            axes.coords_to_point(4.6, f(4.6)),
            buff=0,
            color=TEAL,
            stroke_width=6,
        ).shift(RIGHT * 0.25 + UP * 0.1)
        rising_label = MathTex(r"f' > 0", font_size=32, color=TEAL)
        rising_label.next_to(arrow_l, LEFT, buff=0.25)

        self.play(GrowFromCenter(arrow_l), GrowFromCenter(arrow_r), run_time=0.6)
        self.play(FadeIn(rising_label), run_time=0.2)

        # --- 6. Falling arrow (0.8s): f' < 0 through the middle branch ---
        arrow_mid = Arrow(
            axes.coords_to_point(-0.6, f(-0.6)),
            axes.coords_to_point(0.6, f(0.6)),
            buff=0,
            color=TEAL,
            stroke_width=6,
        ).shift(UP * 0.3)
        falling_label = MathTex(r"f' < 0", font_size=32, color=TEAL)
        falling_label.next_to(arrow_mid, RIGHT, buff=0.3)

        self.play(GrowFromCenter(arrow_mid), run_time=0.6)
        self.play(FadeIn(falling_label), run_time=0.2)

        # --- 7. Footer (0.9s) ---
        footer = Text("Optimization • Physics • Economics", font_size=34, color=FOOTER)
        footer.move_to(DOWN * 3.2)
        self.play(FadeIn(footer, shift=UP * 0.2), run_time=0.7)
        self.play(Indicate(footer, color=WHITE, scale_factor=1.06), run_time=0.9)
        self.wait(2.7)
