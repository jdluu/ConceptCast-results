from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Function as input-output relation ---
        self.camera.background_color = "#181825"

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 4, 1],
            axis_config={"stroke_width": 2, "color": "#89b4fa"},
        )
        axes.set_color("#89b4fa")

        curve = FunctionGraph(lambda x: x**2 / 2, x_range=[-2.5, 2.5])
        curve.set_color("#a6e3a1")
        curve.set_stroke_width(2)

        input_belt = Arrow(start=[-5, 0, 0], end=[-2, 0, 0], buff=0)
        input_belt.set_color("#94e2d5")
        input_belt.set_stroke_width(2)

        machine_box = Rectangle(width=1.2, height=1.2)
        machine_box.set_fill("#fab387", opacity=0.35)
        machine_box.set_stroke("#fab387")
        machine_box.set_stroke_width(2)
        machine_box.move_to(LEFT * 3.2)

        output_dot = Dot(radius=0.07, color="#f38ba8")
        t = ValueTracker(-2.5)
        output_dot.move_to(axes.coords_to_point(t.get_value(), t.get_value() ** 2 / 2))
        output_dot.add_updater(
            lambda d: d.move_to(
                axes.coords_to_point(t.get_value(), t.get_value() ** 2 / 2)
            )
        )

        self.play(Create(axes), run_time=1)
        self.wait(0.5)
        self.play(Create(curve), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(input_belt), FadeIn(machine_box), run_time=1)
        self.play(t.animate.set_value(2.5), run_time=3.5)
        output_dot.clear_updaters()
        # --- Scene 2: Average rate of change as secant slope ---
        self.camera.background_color = "#181825"

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 4, 1],
            axis_config={"color": "#89b4fa", "stroke_width": 2},
        )
        axes.move_to(ORIGIN)

        graph = axes.plot(lambda x: x**2 / 2, color="#a6e3a1")
        graph.set_stroke(width=2)

        dot_a_pos = axes.c2p(-1.5, 1.125)
        dot_b_pos = axes.c2p(1, 0.5)

        dot_a = Dot(radius=0.08, color="#fab387")
        dot_a.move_to(dot_a_pos)
        label_a = Text("x", font="Sans", color="#fab387", font_size=24)
        label_a.next_to(dot_a, DOWN)

        dot_b = Dot(radius=0.08, color="#fab387")
        dot_b.move_to(dot_b_pos)
        label_b = Text("x+h", font="Sans", color="#fab387", font_size=24)
        label_b.next_to(dot_b, DOWN)

        secant_line = Line(
            start=dot_a_pos, end=dot_b_pos, color="#f38ba8", stroke_width=2
        )

        slope_label = Text(
            "m_sec = [f(x+h)-f(x)]/h", font="Sans", color="#94e2d5", font_size=36
        ).to_edge(UP)

        self.play(Create(axes), run_time=1)
        self.play(Create(graph), run_time=1)
        self.play(
            FadeIn(dot_a), FadeIn(label_a), FadeIn(dot_b), FadeIn(label_b), run_time=0.8
        )
        self.play(Create(secant_line), run_time=1)
        self.play(Write(slope_label), run_time=1)
        self.wait(3.7)
        # --- Scene 3: Shrinking interval to approach local behavior ---
        self.camera.background_color = "#181825"

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-0.5, 4, 1],
            x_length=8,
            y_length=5,
            axis_config={"color": "#89b4fa", "stroke_width": 2.0},
        )
        axes.add_coordinates()
        axes.move_to(ORIGIN)

        # Use plot / get_graph with positional x_range to avoid keyword mismatch
        graph = axes.plot(
            lambda x: x**2 / 2, x_range=[-2.5, 2.5], color="#a6e3a1", stroke_width=2.0
        )

        x0 = 0.5
        h = ValueTracker(1.5)

        dot_a = always_redraw(
            lambda: Dot(
                axes.coords_to_point(x0, x0**2 / 2), radius=0.08, color="#fab387"
            )
        )
        dot_b = always_redraw(
            lambda: Dot(
                axes.coords_to_point(x0 + h.get_value(), (x0 + h.get_value()) ** 2 / 2),
                radius=0.08,
                color="#fab387",
            )
        )

        secant = always_redraw(
            lambda: Line(
                axes.coords_to_point(x0, x0**2 / 2),
                axes.coords_to_point(x0 + h.get_value(), (x0 + h.get_value()) ** 2 / 2),
                color="#f38ba8",
                stroke_width=2.0,
            )
        )

        label_a = Text("x", font_size=24, color="#fab387")
        label_b = Text("x+h", font_size=24, color="#fab387")
        label_a.add_updater(lambda m: m.next_to(dot_a, UP))
        label_b.add_updater(lambda m: m.next_to(dot_b, UP))

        brace = always_redraw(
            lambda: BraceBetweenPoints(
                axes.coords_to_point(x0, 0),
                axes.coords_to_point(x0 + h.get_value(), 0),
                direction=DOWN,
                color="#94e2d5",
            )
        )
        brace_label = Text("h → 0", font_size=24, color="#94e2d5")
        brace_label.add_updater(lambda m: m.next_to(brace, DOWN))

        self.play(Create(axes), Create(graph), run_time=1.5)
        self.play(
            FadeIn(dot_a),
            FadeIn(dot_b),
            Create(secant),
            FadeIn(label_a),
            FadeIn(label_b),
            run_time=1.0,
        )
        self.play(h.animate.set_value(0.3), run_time=5.0, rate_func=smooth)
        self.play(FadeIn(brace), FadeIn(brace_label), run_time=0.5)
        self.wait(0.5)
        # --- Scene 4: Instantaneous rate as limit ---
        self.camera.background_color = "#181825"

        axes = Axes(
            x_range=(-0.5, 0.5, 0.1),
            y_range=(-0.2, 0.5, 0.1),
            axis_config={"color": "#89b4fa"},
            tips=False,
        )
        axes.add_coordinates()
        axes.move_to(ORIGIN)
        axes.set_stroke(width=2)

        graph = axes.plot(lambda x: x**2 / 2, x_range=[-0.5, 0.5])
        graph.set_stroke(color="#a6e3a1", width=2)

        delta = ValueTracker(0.4)
        secant_line = always_redraw(
            lambda: Line(
                axes.c2p(-delta.get_value(), (-delta.get_value()) ** 2 / 2),
                axes.c2p(delta.get_value(), (delta.get_value()) ** 2 / 2),
                color="#fab387",
            )
        )
        secant_line.set_stroke(width=2)

        tangent_line = Line(axes.c2p(-0.4, 0.04), axes.c2p(0.4, 0.24), color="#f38ba8")
        tangent_line.set_stroke(width=2)

        limit_arrow = Arrow(
            start=axes.c2p(0.3, 0.1), end=axes.c2p(0.5, 0.1), color="#94e2d5"
        )
        limit_arrow.set_stroke(width=2)

        title = Text("Instantaneous rate as limit", font_size=36, color=WHITE)
        title.to_edge(UP)

        self.play(FadeIn(title), run_time=0.5)
        self.play(Create(axes), run_time=1)
        self.play(Create(graph), run_time=1)
        self.play(Create(secant_line), run_time=0.5)
        self.play(delta.animate.set_value(0.02), run_time=4)
        self.play(FadeIn(tangent_line), run_time=1)
        self.play(FadeIn(limit_arrow), run_time=0.5)
        self.wait(0.5)
        # --- Scene 5: Formal definition of derivative ---
        self.camera.background_color = "#181825"

        # Formula card
        card = Rectangle(
            width=8,
            height=3,
            fill_color="#181825",
            fill_opacity=0.8,
            stroke_color="#89b4fa",
            stroke_width=2,
        )
        card.move_to(ORIGIN)

        # Limit definition
        limit_tex = MathTex(
            r"f'(x)=\lim_{h	o 0}\frac{f(x+h)-f(x)}{h}", color="#89b4fa"
        )
        limit_tex.scale(1.2)
        limit_tex.move_to(ORIGIN)

        # Number line for h
        number_line = NumberLine(
            x_range=[-0.5, 0.5, 0.1], length=8, include_numbers=False, color="#fab387"
        )
        number_line.add_numbers()
        number_line.set_stroke(width=2)
        number_line.next_to(card, DOWN, buff=1.2)

        # h dot shrinking toward zero
        h_dot = Dot(radius=0.06, color="#f38ba8")
        h_dot.move_to(number_line.n2p(0.4))
        h_dot.target = Dot(radius=0.06, color="#f38ba8")
        h_dot.target.move_to(number_line.n2p(0))

        # Animations - total 11s
        self.play(Create(card), run_time=1)
        self.play(Write(limit_tex), run_time=2)
        self.play(FadeIn(number_line), run_time=1)
        self.play(MoveToTarget(h_dot), run_time=3)
        self.wait(4)
        # --- Scene 6: Geometric interpretation as tangent slope ---
        self.camera.background_color = "#181825"

        # Axes
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-0.5, 4],
            x_length=8,
            y_length=6,
            axis_config={"color": "#89b4fa", "stroke_width": 2},
        )
        axes.set_stroke(width=2)
        axes.shift(UP * 0.3)

        # Function curve f(x)=x^2/2
        # get_graph caused a keyword-argument mismatch in this Manim build,
        # axes.plot is the compatible plotting API
        graph = axes.plot(lambda x: x**2 / 2, x_range=[-2.5, 2.5])
        graph.set_stroke(color="#a6e3a1", width=2)

        # Point of interest x0
        x0 = 1.0
        y0 = x0**2 / 2
        point_coord = axes.c2p(x0, y0)
        point = Dot(point_coord, radius=0.08, color="#f38ba8")
        label = MathTex("x_0").next_to(point, UP).set_color("#f38ba8")
        point_group = VGroup(point, label)

        # Tangent line at x0  f'(x)=x
        slope = x0
        start_x = -2.5
        end_x = 2.5
        start_point = axes.c2p(start_x, y0 + slope * (start_x - x0))
        end_point = axes.c2p(end_x, y0 + slope * (end_x - x0))
        tangent_line = Line(start_point, end_point, color="#fab387", stroke_width=2)

        # Slope indicator arrow along the tangent
        arrow_start = axes.c2p(x0 + 0.6, y0 + slope * 0.6)
        arrow_end = axes.c2p(x0 + 1.4, y0 + slope * 1.4)
        slope_arrow = Arrow(
            arrow_start, arrow_end, color="#94e2d5", stroke_width=2, buff=0
        )

        narration = (
            Text(
                "Geometrically the derivative is the slope of the tangent line at that point on the curve.",
                font_size=28,
            )
            .to_edge(DOWN)
            .set_color(WHITE)
        )

        self.play(Create(axes), run_time=1)
        self.play(Create(graph), run_time=1.5)
        self.play(FadeIn(point_group), run_time=1)
        self.play(Create(tangent_line), run_time=1.5)
        self.play(GrowFromCenter(slope_arrow), run_time=1)
        self.play(FadeIn(narration), run_time=1)
        self.wait(1)
        # --- Scene 7: Derivative as a new function ---
        self.camera.background_color = "#181825"

        # Top axes
        top_axes = Axes(
            x_range=[-2.5, 2.5, 0.5],
            y_range=[-0.5, 4, 0.5],
            x_length=8,
            y_length=3,
            axis_config={"color": "#89b4fa", "stroke_width": 2},
            tips=False,
        )
        top_axes.shift(UP * 2.5)

        # Top curve f(x)=x^2/2
        top_curve = top_axes.plot(lambda x: x**2 / 2, x_range=[-2.5, 2.5])
        top_curve.set_stroke(color="#a6e3a1", width=2)

        # Bottom axes
        bottom_axes = Axes(
            x_range=[-2.5, 2.5, 0.5],
            y_range=[-3, 3, 0.5],
            x_length=8,
            y_length=3,
            axis_config={"color": "#89b4fa", "stroke_width": 2},
            tips=False,
        )
        bottom_axes.shift(DOWN * 2.5)

        # Derivative curve f'(x)=x
        derivative_curve = bottom_axes.plot(lambda x: x, x_range=[-2.5, 2.5])
        derivative_curve.set_stroke(color="#f38ba8", width=2)

        # Link arrow
        link_arrow = Arrow(
            start=[0, 1, 0],
            end=[0, -1, 0],
            color="#94e2d5",
            stroke_width=2,
            buff=0,
        )

        # Animations - total 7.5s
        self.play(Create(top_axes), run_time=1.0)
        self.play(Create(top_curve), run_time=1.5)
        self.play(Create(bottom_axes), run_time=1.0)
        self.play(Create(derivative_curve), run_time=1.5)
        self.play(Create(link_arrow), run_time=1.0)
        self.wait(1.5)
