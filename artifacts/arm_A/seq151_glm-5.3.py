from manim import *
import numpy as np


class SceneGen(Scene):
    def construct(self):
        # ------------------------------------------------------------
        # Scene 1: What is a function? (foundation)
        # ------------------------------------------------------------
        title = Text("Derivatives: The Instantaneous Rate of Change", font_size=30)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=6,
            y_length=4.5,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        func = lambda x: 0.4 * x ** 2 + 0.3
        curve = axes.plot(func, color=BLUE)
        curve_label = MathTex("f(x) = 0.4x^2 + 0.3", font_size=36, color=BLUE)
        curve_label.next_to(curve, RIGHT, buff=0.4).shift(UP)

        self.play(Create(axes), Write(labels))
        self.play(Create(curve), run_time=2)
        self.play(Write(curve_label))
        self.wait(1)

        intro_text = Text(
            "A function maps each input to an output.", font_size=26
        ).to_corner(DR)
        self.play(Write(intro_text))
        self.wait(2)

        # Demo a point moving on the curve
        dot = Dot(radius=0.08, color=YELLOW)
        dot.add_updater(lambda d: d.move_to(axes.c2p(2, func(2))))
        self.play(FadeIn(dot))
        tracer = VMobject(color=YELLOW)
        self.play(MoveAlongPath(dot, curve), run_time=2)
        dot.clear_updaters()
        self.wait(1)

        self.play(
            FadeOut(title), FadeOut(axes), FadeOut(labels),
            FadeOut(curve), FadeOut(curve_label),
            FadeOut(intro_text), FadeOut(dot),
        )
        self.clear()

        # ------------------------------------------------------------
        # Scene 2: Average rate of change (secant line)
        # ------------------------------------------------------------
        title2 = Text("Step 1: Average Rate of Change", font_size=34)
        title2.to_edge(UP)
        self.play(Write(title2))

        axes2 = Axes(
            x_range=[0, 5, 1], y_range=[0, 5, 1],
            x_length=6, y_length=4.5,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)
        curve2 = axes2.plot(func, color=BLUE)
        self.play(Create(axes2), Create(curve2))

        a, b = 1.0, 3.5
        pa = axes2.c2p(a, func(a))
        pb = axes2.c2p(b, func(b))

        da = Dot(pa, color=RED, radius=0.08)
        db = Dot(pb, color=RED, radius=0.08)
        secant = Line(pa, pb, color=ORANGE, stroke_width=4)

        slope_val = (func(b) - func(a)) / (b - a)
        formula = MathTex(
            r"\frac{\Delta y}{\Delta x} = "
            r"\frac{f(b)-f(a)}{b-a} \approx " + f"{slope_val:.2f}",
            font_size=36,
        ).to_corner(UR).shift(DOWN * 0.8)

        self.play(FadeIn(da), FadeIn(db))
        self.play(Create(secant))
        self.play(Write(formula))
        self.wait(1)

        explain = Text(
            "The secant slope = average rate of change over [a, b]",
            font_size=24,
        ).to_corner(DR)
        self.play(Write(explain))
        self.wait(2)

        self.play(
            FadeOut(title2), FadeOut(axes2), FadeOut(curve2),
            FadeOut(da), FadeOut(db), FadeOut(secant),
            FadeOut(formula), FadeOut(explain),
        )
        self.clear()

        # ------------------------------------------------------------
        # Scene 3: Shrinking the interval
        # ------------------------------------------------------------
        title3 = Text("Step 2: Shrink the Interval", font_size=34).to_edge(UP)
        self.play(Write(title3))

        axes3 = Axes(
            x_range=[0, 5, 1], y_range=[0, 5, 1],
            x_length=6, y_length=4.5,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)
        curve3 = axes3.plot(func, color=BLUE)
        self.play(Create(axes3), Create(curve3))

        x0 = 2.0
        p0 = Dot(axes3.c2p(x0, func(x0)), color=RED, radius=0.08)
        self.play(FadeIn(p0))

        tracker = ValueTracker(x0 + 2.0)
        sec = always_redraw(
            lambda: Line(
                axes3.c2p(x0, func(x0)),
                axes3.c2p(tracker.get_value(), func(tracker.get_value())),
                color=ORANGE, stroke_width=4,
            )
        )
        moving_dot = always_redraw(
            lambda: Dot(
                axes3.c2p(tracker.get_value(), func(tracker.get_value())),
                color=YELLOW, radius=0.08,
            )
        )
        slope_tex = always_redraw(
            lambda: MathTex(
                r"\frac{\Delta y}{\Delta x} = "
                + f"{(func(tracker.get_value()) - func(x0)) / (tracker.get_value() - x0):.3f}",
                font_size=36,
            ).to_corner(UR).shift(DOWN * 0.9)
        )

        self.play(Create(sec), FadeIn(moving_dot), Write(slope_tex))
        self.play(tracker.animate.set_value(x0 + 1.0), run_time=2)
        self.play(tracker.animate.set_value(x0 + 0.4), run_time=2)
        self.play(tracker.animate.set_value(x0 + 0.1), run_time=2)
        note = Text("The secant approaches the tangent!", font_size=26)
        note.to_corner(DR)
        self.play(Write(note))
        self.wait(2)

        self.play(
            FadeOut(title3), FadeOut(axes3), FadeOut(curve3), FadeOut(p0),
            FadeOut(note),
        )
        self.remove(sec, moving_dot, slope_tex, tracker)
        self.clear()

        # ------------------------------------------------------------
        # Scene 4: The difference quotient and the limit
        # ------------------------------------------------------------
        title4 = Text("Step 3: The Difference Quotient Limit", font_size=34)
        title4.to_edge(UP)
        self.play(Write(title4))

        dq = MathTex(
            r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            font_size=54,
        )
        box = SurroundingRectangle(dq, color=YELLOW, buff=0.4)
        self.play(Write(dq))
        self.play(Create(box))
        self.wait(1)

        parts = VGroup(
            MathTex(r"\frac{f(x+h)-f(x)}{h}", font_size=40),
            Text("= slope of secant through x and x+h", font_size=24),
        ).arrange(DOWN, buff=0.4).shift(LEFT * 3.5 + DOWN * 1.5)
        parts2 = VGroup(
            MathTex(r"\lim_{h \to 0}", font_size=40),
            Text("= let h shrink to zero", font_size=24),
        ).arrange(DOWN, buff=0.4).shift(RIGHT * 3.5 + DOWN * 1.5)

        self.play(Write(parts))
        self.play(Write(parts2))
        self.wait(2)

        self.play(
            FadeOut(title4), FadeOut(dq), FadeOut(box),
            FadeOut(parts), FadeOut(parts2),
        )
        self.clear()

        # ------------------------------------------------------------
        # Scene 5: Computing the derivative of f(x)=0.4x^2+0.3
        # ------------------------------------------------------------
        title5 = Text("Step 4: Compute f'(x) from First Principles", font_size=32)
        title5.to_edge(UP)
        self.play(Write(title5))

        steps = VGroup(
            MathTex(r"f(x) = 0.4x^2 + 0.3", font_size=40),
            MathTex(r"f(x+h) = 0.4(x+h)^2 + 0.3", font_size=40),
            MathTex(
                r"f(x+h)-f(x) = 0.8xh + 0.4h^2", font_size=40
            ),
            MathTex(
                r"\frac{f(x+h)-f(x)}{h} = 0.8x + 0.4h", font_size=40
            ),
            MathTex(
                r"f'(x) = \lim_{h\to 0}(0.8x + 0.4h) = 0.8x",
                font_size=40,
            ),
        ).arrange(DOWN, buff=0.5).shift(DOWN * 0.3)

        for s in steps[:4]:
            self.play(Write(s))
            self.wait(0.7)
        result_box = SurroundingRectangle(steps[4], color=YELLOW, buff=0.2)
        self.play(Write(steps[4]))
        self.play(Create(result_box))
        self.wait(2)

        self.play(FadeOut(title5), FadeOut(steps), FadeOut(result_box))
        self.clear()

        # ------------------------------------------------------------
        # Scene 6: Visualizing f and f' together
        # ------------------------------------------------------------
        title6 = Text("Step 5: f(x) and its Derivative f'(x)", font_size=34)
        title6.to_edge(UP)
        self.play(Write(title6))

        axes6 = Axes(
            x_range=[0, 5, 1], y_range=[0, 5, 1],
            x_length=6, y_length=4.5,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)
        curve6 = axes6.plot(func, color=BLUE)
        deriv = lambda x: 0.8 * x
        dcurve6 = axes6.plot(deriv, x_range=[0, 5, 0.1], color=GREEN)
        lab_f = MathTex("f(x)", color=BLUE, font_size=36).next_to(curve6, UR)
        lab_d = MathTex("f'(x)=0.8x", color=GREEN, font_size=36).to_corner(DL)

        self.play(Create(axes6), Create(curve6))
        self.play(Write(lab_f))
        self.play(Create(dcurve6), run_time=2)
        self.play(Write(lab_d))

        x_demo = 3.0
        tang = axes6.get_secant_slope_group(
            x=x_demo, graph=curve6, dx=0.01,
            secant_line_color=YELLOW, secant_line_length=4,
        )
        self.play(Create(tang))
        note6 = Text(
            "Tangent slope of f at x=3 is f'(3)=2.4", font_size=24
        ).to_corner(DR)
        self.play(Write(note6))
        self.wait(2)

        self.play(
            FadeOut(title6), FadeOut(axes6), FadeOut(curve6),
            FadeOut(dcurve6), FadeOut(lab_f), FadeOut(lab_d),
            FadeOut(tang), FadeOut(note6),
        )
        self.clear()

        # ------------------------------------------------------------
        # Scene 7: Summary
        # ------------------------------------------------------------
        title7 = Text("Summary: The Derivative", font_size=40).to_edge(UP)
        self.play(Write(title7))

        summary = VGroup(
            MathTex(
                r"f'(x) = \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}",
                font_size=44,
            ),
            Text("• Instantaneous rate of change", font_size=28),
            Text("• Slope of the tangent line", font_size=28),
            Text("• Limit of secant slopes as h → 0", font_size=28),
        ).arrange(DOWN, buff=0.5).shift(DOWN * 0.3)

        for item in summary:
            self.play(Write(item))
            self.wait(0.6)

        box7 = SurroundingRectangle(summary, color=BLUE, buff=0.4)
        self.play(Create(box7))
        self.wait(2)

        self.play(FadeOut(summary), FadeOut(box7))
        end = Text("Derivatives measure change.", font_size=32, color=YELLOW)
        self.play(Write(end))
        self.wait(1)
        self.play(FadeOut(title7), FadeOut(end))
        self.wait(0.5)
