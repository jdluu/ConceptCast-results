from manim import *


class SceneGen(Scene):
    def construct(self):
        # helper function used throughout the geometric scenes
        def f(x):
            return 0.25 * x ** 2

        # ==================================================================
        # Scene 1 -- Introduction: a function maps inputs to outputs
        # ==================================================================
        title = Text("The Derivative", font_size=60, gradient=(BLUE, TEAL))
        title.move_to(UP * 2.3)
        subtitle = Text(
            "the instantaneous rate of change of a function", font_size=30
        ).next_to(title, DOWN, buff=0.4)

        x_sym = MathTex("x").set_color(YELLOW)
        f_sym = MathTex("f")
        fx_sym = MathTex("f(x)").set_color(TEAL)
        machine = VGroup(x_sym, f_sym, fx_sym).arrange(RIGHT, buff=1.3)
        arrow1 = Arrow(x_sym.get_right(), f_sym.get_left(), buff=0.15)
        arrow2 = Arrow(f_sym.get_right(), fx_sym.get_left(), buff=0.15)
        fbox = SurroundingRectangle(f_sym, color=BLUE)
        in_lab = Text("input", font_size=24).next_to(x_sym, DOWN, buff=0.4)
        out_lab = Text("output", font_size=24).next_to(fx_sym, DOWN, buff=0.4)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(0.5)
        self.play(Write(x_sym), Write(f_sym), Write(fx_sym))
        self.play(GrowArrow(arrow1), GrowArrow(arrow2), Create(fbox))
        self.play(FadeIn(in_lab, shift=UP), FadeIn(out_lab, shift=UP))
        self.wait()

        question = Text(
            "How fast does the output change\nas the input changes?", font_size=34
        ).move_to(DOWN * 1.6)
        self.play(FadeOut(VGroup(machine, arrow1, arrow2, fbox, in_lab, out_lab)))
        self.play(Write(question))
        self.wait()
        answer = MathTex(
            r"\text{rate of change} \;=\; "
            r"\frac{\text{change in output}}{\text{change in input}}"
        ).next_to(question, DOWN, buff=0.7)
        self.play(Write(answer))
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, subtitle, question, answer)))
        self.clear()

        # ==================================================================
        # Scene 2 -- Average rate of change: the secant line
        # ==================================================================
        axes = Axes(
            x_range=[0, 4.5, 1], y_range=[0, 3.5, 1],
            x_length=7.5, y_length=4.6,
        ).shift(DOWN * 0.3)
        axis_labels = axes.get_axis_labels(x_label="x", y_label="y")
        curve = axes.plot(f, x_range=[0, 3.6], color=BLUE)

        p_dot = Dot(axes.c2p(1, f(1)), color=WHITE)
        q_dot = Dot(axes.c2p(3, f(3)), color=WHITE)
        p_lab = MathTex("P").next_to(p_dot, LEFT, buff=0.15)
        q_lab = MathTex("Q").next_to(q_dot, UR, buff=0.15)
        run_line = DashedLine(axes.c2p(1, f(1)), axes.c2p(3, f(1)), color=GRAY)
        rise_line = DashedLine(axes.c2p(3, f(1)), axes.c2p(3, f(3)), color=GRAY)
        run_brace = Brace(run_line, DOWN, color=GRAY)
        rise_brace = Brace(rise_line, RIGHT, color=GRAY)
        run_lab = MathTex(r"\Delta x = 2").next_to(run_brace, DOWN, buff=0.15)
        rise_lab = MathTex(r"\Delta y = 2").next_to(rise_brace, RIGHT, buff=0.15)
        secant = axes.plot(lambda x: x - 0.75, x_range=[0.4, 3.8], color=RED)
        slope_eq = MathTex(
            r"m_{sec} = \frac{\Delta y}{\Delta x}"
            r" = \frac{f(3) - f(1)}{3 - 1} = \frac{2}{2} = 1"
        ).to_corner(UL)
        avg_text = Text(
            "the average rate of change of f on [1, 3]", font_size=26
        ).next_to(slope_eq, DOWN, buff=0.25, aligned_edge=LEFT)

        self.play(Create(axes), Write(axis_labels))
        self.play(Create(curve))
        self.play(FadeIn(p_dot), FadeIn(q_dot), Write(p_lab), Write(q_lab))
        self.play(Create(run_line), Create(rise_line))
        self.play(
            GrowFromCenter(run_brace), GrowFromCenter(rise_brace),
            Write(run_lab), Write(rise_lab),
        )
        self.play(Create(secant))
        self.play(Write(slope_eq), FadeIn(avg_text, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(VGroup(
            axes, axis_labels, curve, p_dot, q_dot, p_lab, q_lab,
            run_line, rise_line, run_brace, rise_brace, run_lab, rise_lab,
            secant, slope_eq, avg_text,
        )))
        self.clear()

        # ==================================================================
        # Scene 3 -- Shrinking the interval: Q slides toward P
        # ==================================================================
        axes = Axes(
            x_range=[0, 4.5, 1], y_range=[0, 3.5, 1],
            x_length=7.5, y_length=4.6,
        ).shift(DOWN * 0.3)
        axis_labels = axes.get_axis_labels(x_label="x", y_label="y")
        curve = axes.plot(f, x_range=[0, 3.6], color=BLUE)
        a = 1.0
        p_dot = Dot(axes.c2p(a, f(a)), color=WHITE)
        p_lab = MathTex("P").next_to(p_dot, LEFT, buff=0.15)

        xq = ValueTracker(3.0)
        secant = always_redraw(
            lambda: axes.plot(
                lambda x: f(a)
                + ((f(xq.get_value()) - f(a)) / (xq.get_value() - a)) * (x - a),
                x_range=[0.2, 4.0], color=RED,
            )
        )
        q_dot = always_redraw(
            lambda: Dot(
                axes.c2p(xq.get_value(), f(xq.get_value())),
                color=YELLOW, radius=0.08,
            )
        )
        slope_text = MathTex(r"m_{sec} =").to_corner(UL)
        slope_val = always_redraw(
            lambda: DecimalNumber(
                (f(xq.get_value()) - f(a)) / (xq.get_value() - a),
                num_decimal_places=3, color=RED,
            ).next_to(slope_text, RIGHT, buff=0.15)
        )
        caption = Text(
            "slide Q toward P: the secant line pivots...", font_size=28
        ).to_edge(DOWN)

        self.play(Create(axes), Write(axis_labels))
        self.play(Create(curve), FadeIn(p_dot), Write(p_lab))
        self.play(FadeIn(secant), FadeIn(q_dot), Write(slope_text), FadeIn(slope_val))
        self.play(Write(caption))
        self.wait(0.5)
        self.play(xq.animate.set_value(2.0), run_time=2)
        self.play(xq.animate.set_value(1.5), run_time=2)
        self.play(xq.animate.set_value(1.2), run_time=2)
        self.play(xq.animate.set_value(1.05), run_time=2)
        self.wait(0.5)

        caption2 = Text(
            "...and settles onto one line: the tangent at P", font_size=28
        ).move_to(caption)
        self.play(Transform(caption, caption2))
        self.wait(1.5)
        self.play(FadeOut(VGroup(
            axes, axis_labels, curve, p_dot, p_lab, secant, q_dot,
            slope_text, slope_val, caption,
        )))
        self.clear()

        # ==================================================================
        # Scene 4 -- The formal definition: a limit of the difference quotient
        # ==================================================================
        lhs = MathTex(r"f'(a) \;=\;")
        lim_part = MathTex(r"\lim_{h \to 0}")
        frac_part = MathTex(r"\frac{f(a+h) - f(a)}{h}")
        eq = VGroup(lhs, lim_part, frac_part).arrange(RIGHT, buff=0.35).shift(UP * 1.7)

        lim_box = SurroundingRectangle(lim_part, color=GREEN)
        frac_box = SurroundingRectangle(frac_part, color=ORANGE)
        ann1 = Text("the step size h shrinks to 0", font_size=28).set_color(GREEN)
        ann1.move_to(UP * 0.5 + LEFT * 2.3)
        ann2 = MathTex(
            r"f(a+h) - f(a)", r"\;\text{: change in output}"
        ).scale(0.8).move_to(DOWN * 0.3 + RIGHT * 1.0)
        ann3 = MathTex(
            r"h", r"\;\text{: change in input}"
        ).scale(0.8).move_to(DOWN * 1.1 + RIGHT * 1.0)
        arr1 = Arrow(
            lim_part.get_bottom() + DOWN * 0.1, ann1.get_top() + UP * 0.1,
            buff=0.1, color=GREEN,
        )
        arr2 = Arrow(
            frac_part.get_bottom() + DOWN * 0.1, ann2.get_top() + UP * 0.1,
            buff=0.1, color=ORANGE,
        )
        arr3 = Arrow(
            ann2.get_bottom(), ann3.get_top(), buff=0.1, color=ORANGE,
        )
        stmt = Text(
            "If the limit exists, f is differentiable at a,\n"
            "and f '(a) is the slope of the tangent line at x = a.",
            font_size=28,
        ).to_edge(DOWN, buff=0.4)

        self.play(Write(lhs), Write(lim_part), Write(frac_part))
        self.play(Create(lim_box), Create(frac_box))
        self.play(GrowArrow(arr1), Write(ann1))
        self.play(GrowArrow(arr2), Write(ann2))
        self.play(GrowArrow(arr3), Write(ann3))
        self.wait(1)
        self.play(FadeOut(VGroup(lim_box, frac_box, arr1, arr2, arr3, ann1, ann2, ann3)))
        self.play(eq.animate.scale(1.1).move_to(UP * 0.8))
        self.play(Write(stmt))
        self.wait(1.5)
        self.play(FadeOut(VGroup(eq, stmt)))
        self.clear()

        # ==================================================================
        # Scene 5 -- The tangent line as the limit of secant lines
        # ==================================================================
        a = 1.0
        axes = Axes(
            x_range=[-1, 3.5, 1], y_range=[-1, 3.2, 1],
            x_length=7.5, y_length=4.8,
        ).shift(DOWN * 0.2)
        axis_labels = axes.get_axis_labels(x_label="x", y_label="y")
        curve = axes.plot(f, x_range=[0, 3.5], color=BLUE)
        p_dot = Dot(axes.c2p(a, f(a)), color=WHITE)
        p_lab = MathTex("P").next_to(p_dot, LEFT, buff=0.15)

        def sec_line(x_q, color=RED):
            m = (f(x_q) - f(a)) / (x_q - a)
            line = axes.plot(
                lambda x: f(a) + m * (x - a),
                x_range=[-0.35, 3.3], color=color,
            )
            return m, line

        m1, line1 = sec_line(2.6)
        m2, line2 = sec_line(1.8)
        m3, line3 = sec_line(1.3)
        tangent = axes.plot(
            lambda x: f(a) + 0.5 * (x - a),
            x_range=[-0.6, 3.2], color=GREEN,
        ).set_stroke(width=6)

        sec = line1
        lab = MathTex(r"m_{sec} \approx " + f"{m1:.3f}").to_corner(UR)
        lab2 = MathTex(r"m_{sec} \approx " + f"{m2:.3f}").move_to(lab)
        lab3 = MathTex(r"m_{sec} \approx " + f"{m3:.3f}").move_to(lab)
        tan_lab = MathTex(r"m = f'(1) = 0.5").set_color(GREEN).move_to(lab)
        caption = Text(
            "the tangent line is the limit of the secant lines", font_size=28
        ).to_edge(DOWN)

        self.play(Create(axes), Write(axis_labels))
        self.play(Create(curve), FadeIn(p_dot), Write(p_lab))
        self.play(Create(sec), Write(lab))
        self.wait(0.5)
        self.play(Transform(sec, line2), Transform(lab, lab2))
        self.wait(0.5)
        self.play(Transform(sec, line3), Transform(lab, lab3))
        self.wait(0.5)
        self.play(Transform(sec, tangent), Transform(lab, tan_lab))
        self.play(Write(caption))
        self.play(Indicate(sec, scale_factor=1.05))
        self.wait(1.5)
        self.play(FadeOut(VGroup(
            axes, axis_labels, curve, p_dot, p_lab, sec, lab, caption,
        )))
        self.clear()

        # ==================================================================
        # Scene 6 -- Worked example: derivative of f(x) = x^2 / 4
        # ==================================================================
        title = MathTex(r"f(x) = \frac{x^2}{4}", font_size=48).to_edge(UP)
        tsub = Text(
            "Example: differentiate from first principles", font_size=28
        ).next_to(title, DOWN, buff=0.3)

        eq = MathTex(r"\frac{f(a+h) - f(a)}{h}").scale(1.2).move_to(UP * 0.2)
        self.play(Write(title), FadeIn(tsub, shift=UP))
        self.play(Write(eq))
        self.wait(0.5)

        steps = [
            r"=\ \frac{(a+h)^2 - a^2}{4h}",
            r"=\ \frac{a^2 + 2ah + h^2 - a^2}{4h}",
            r"=\ \frac{h\,(2a + h)}{4h} \;=\; \frac{2a + h}{4}",
            r"f'(a) \;=\; \lim_{h \to 0}\, \frac{2a + h}{4} \;=\; \frac{a}{2}",
        ]
        for s in steps:
            new_eq = MathTex(s).scale(1.2).move_to(UP * 0.2)
            self.play(TransformMatchingTex(eq, new_eq))
            eq = new_eq
            self.wait(0.7)

        result_box = SurroundingRectangle(eq, color=YELLOW)
        note = MathTex(
            r"\text{for every input } x: \quad f'(x) = \frac{x}{2}"
        ).next_to(result_box, DOWN, buff=0.6)
        check = Text(
            "check: at x = 1 the slope of the curve is 1/2", font_size=26
        ).next_to(note, DOWN, buff=0.4)
        self.play(Create(result_box))
        self.play(Write(note))
        self.play(Write(check))
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, tsub, eq, result_box, note, check)))
        self.clear()

        # ==================================================================
        # Scene 7 -- Notation for the derivative
        # ==================================================================
        n1 = MathTex(r"f'(x)").scale(1.8).move_to(UP * 1.2)
        lab1 = Text("Lagrange's notation", font_size=28).next_to(n1, DOWN, buff=0.5)
        self.play(Write(n1))
        self.play(FadeIn(lab1, shift=UP))
        self.wait(0.5)

        n2 = MathTex(r"\frac{dy}{dx}").scale(1.8).move_to(n1)
        lab2 = Text("Leibniz's notation", font_size=28).move_to(lab1)
        self.play(Transform(n1, n2))
        self.play(FadeOut(lab1), FadeIn(lab2, shift=UP))
        self.wait(0.5)

        n3 = MathTex(r"\frac{d}{dx}\,f(x)").scale(1.8).move_to(n1)
        lab3 = Text("operator notation", font_size=28).move_to(lab1)
        self.play(Transform(n1, n3))
        self.play(FadeOut(lab2), FadeIn(lab3, shift=UP))
        self.wait(0.5)

        row = VGroup(
            MathTex(r"f'(x)"), MathTex("="),
            MathTex(r"\frac{dy}{dx}"), MathTex("="),
            MathTex(r"\frac{d}{dx}\,f(x)"),
        ).arrange(RIGHT, buff=0.4).scale(1.1).move_to(UP * 1.2)
        self.play(FadeOut(n1), FadeOut(lab3), LaggedStart(*[
            Write(part) for part in row
        ], lag_ratio=0.3))

        meaning = MathTex(
            r"\frac{dy}{dx} \;\approx\; \frac{\Delta y}{\Delta x}"
            r" \quad \text{as } \Delta x \to 0"
        ).next_to(row, DOWN, buff=0.8)
        caption = Text(
            "all three mean: the derivative of f with respect to x",
            font_size=26,
        ).next_to(meaning, DOWN, buff=0.5)
        self.play(Write(meaning))
        self.play(FadeIn(caption, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(VGroup(row, meaning, caption)))
        self.clear()

        # ==================================================================
        # Scene 8 -- The derivative as a function, and summary
        # ==================================================================
        axf = Axes(
            x_range=[-2.4, 2.4, 1], y_range=[0, 2, 1],
            x_length=4.8, y_length=3.6,
        ).shift(LEFT * 3.1 + DOWN * 0.2)
        axd = Axes(
            x_range=[-2.4, 2.4, 1], y_range=[-1.4, 1.4, 1],
            x_length=4.8, y_length=3.6,
        ).shift(RIGHT * 3.1 + DOWN * 0.2)
        f_title = MathTex(r"f(x) = \frac{x^2}{4}").next_to(axf, UP, buff=0.25)
        d_title = MathTex(r"f'(x) = \frac{x}{2}").next_to(axd, UP, buff=0.25)
        curve_f = axf.plot(f, x_range=[-2.4, 2.4], color=BLUE)
        curve_d = axd.plot(lambda x: x / 2, x_range=[-2.4, 2.4], color=RED)

        x0 = ValueTracker(-2.0)

        def clip(v, lo, hi):
            return max(lo, min(hi, v))

        tangent_f = always_redraw(
            lambda: axf.plot(
                lambda x: f(x0.get_value())
                + (x0.get_value() / 2) * (x - x0.get_value()),
                x_range=[
                    clip(x0.get_value() - 1.2, -2.4, 2.4),
                    clip(x0.get_value() + 1.2, -2.4, 2.4),
                ],
                color=YELLOW,
            )
        )
        dot_f = always_redraw(
            lambda: Dot(
                axf.c2p(x0.get_value(), f(x0.get_value())),
                color=YELLOW, radius=0.08,
            )
        )
        dot_d = always_redraw(
            lambda: Dot(
                axd.c2p(x0.get_value(), x0.get_value() / 2),
                color=YELLOW, radius=0.08,
            )
        )
        link = always_redraw(
            lambda: DashedLine(
                dot_f.get_center(), dot_d.get_center(),
                stroke_width=2, color=GRAY,
            )
        )
        slope_num = always_redraw(
            lambda: DecimalNumber(
                x0.get_value() / 2, num_decimal_places=2, color=RED,
            ).next_to(dot_d, DOWN, buff=0.3)
        )
        cap = Text(
            "the slope of f at x equals the height of f ' at x",
            font_size=26,
        ).to_edge(DOWN)

        self.play(Create(axf), Create(axd))
        self.play(Write(f_title), Write(d_title))
        self.play(Create(curve_f), Create(curve_d))
        self.play(
            FadeIn(tangent_f), FadeIn(dot_f), FadeIn(dot_d),
            FadeIn(link), FadeIn(slope_num), Write(cap),
        )
        self.wait(0.5)
        self.play(x0.animate.set_value(2.2), run_time=6, rate_func=linear)
        self.play(x0.animate.set_value(-2.0), run_time=6, rate_func=linear)
        self.wait(0.5)

        summary = VGroup(
            Text("The derivative is:", font_size=32),
            MathTex(
                r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}", font_size=44
            ),
            Text("— the limit of the difference quotient", font_size=26),
            Text("— the slope of the tangent line", font_size=26),
            Text("— the instantaneous rate of change", font_size=26),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)

        self.play(FadeOut(VGroup(
            axf, axd, f_title, d_title, curve_f, curve_d,
            tangent_f, dot_f, dot_d, link, slope_num, cap,
        )))
        self.play(FadeIn(summary, shift=UP))
        self.wait(2)
        self.play(FadeOut(summary))
        self.clear()
