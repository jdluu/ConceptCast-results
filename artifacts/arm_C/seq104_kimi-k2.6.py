import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: The Slope of a Line as Rate of Change ---
        self.camera.background_color = "#181825"

        # 1) Title at the top
        title = Text(
            "The Slope of a Line as Rate of Change", font_size=36, color=WHITE
        ).move_to(UP * 3)

        # 2) Main formula centered
        main_formula = MathTex(r"	ext{Slope} = \frac{	ext{rise}}{	ext{run}}")
        main_formula.set_color("#89b4fa")
        main_formula.move_to(ORIGIN)

        # 3) Right-triangle visual metaphor below the formula
        tri_origin = DOWN * 1.5

        run_line = Line(
            tri_origin, tri_origin + RIGHT * 2, color="#a6e3a1", stroke_width=3
        )
        rise_line = Line(
            tri_origin, tri_origin + UP * 1.2, color="#f38ba8", stroke_width=3
        )
        slope_line = Line(
            tri_origin + RIGHT * 2,
            tri_origin + UP * 1.2,
            color="#fab387",
            stroke_width=3,
        )

        run_label = Text("run", font_size=24, color="#a6e3a1").next_to(
            run_line, DOWN, buff=0.2
        )
        rise_label = Text("rise", font_size=24, color="#f38ba8").next_to(
            rise_line, LEFT, buff=0.2
        )
        slope_label = Text("slope", font_size=24, color="#fab387").next_to(
            slope_line, UP, buff=0.2
        )

        triangle = VGroup(
            run_line, rise_line, slope_line, run_label, rise_label, slope_label
        )

        # 4) Supporting sentence below the triangle
        supporting_text = Text(
            "A straight line has the same steepness at every point.",
            font_size=28,
            color="#94e2d5",
        ).next_to(triangle, DOWN, buff=0.6)

        # --- ANIMATIONS ---
        # Title appears
        self.play(Write(title), run_time=1.0)

        # Main formula grows in
        self.play(GrowFromCenter(main_formula), run_time=1.5)

        # Build the triangle piece by piece
        self.play(Create(run_line), FadeIn(run_label), run_time=0.8)
        self.play(Create(rise_line), FadeIn(rise_label), run_time=0.8)
        self.play(Create(slope_line), FadeIn(slope_label), run_time=0.8)

        # Supporting text fades in
        self.play(FadeIn(supporting_text), run_time=1.0)

        # Wait to hit exactly 6.0 seconds
        self.wait(0.1)
        # --- Scene 2: Step 2: Slope Varies on a Curve ---
        # Set background color to match style guidelines
        self.camera.background_color = "#181825"

        # Create axes with appropriate ranges
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=6,
            axis_config={
                "color": "#fab387",
                "stroke_width": 2,
                "include_tip": True,
            },
        ).move_to(ORIGIN)

        # Curve: a wavy function showing varying slope
        curve = axes.plot(
            lambda x: -0.3 * (x**2) + 0.6 * x,
            color="#89b4fa",
            stroke_width=3,
            x_range=[-3, 3],
        )
        curve_label = MathTex("f(x)", color="#89b4fa", font_size=28).next_to(
            axes.c2p(2.8, -0.3 * (2.8**2) + 0.6 * 2.8), RIGHT, buff=0.2
        )

        # Title
        title = Text(
            "Slope Varies on a Curve", font_size=36, color=WHITE, font="Sans"
        ).move_to(UP * 3)

        # Points on the curve to demonstrate varying slope
        points_x = [-2, 0, 1.5]
        point_dots = VGroup()
        slope_lines = VGroup()
        slope_labels = VGroup()

        for i, px in enumerate(points_x):
            py = -0.3 * (px**2) + 0.6 * px
            point = axes.c2p(px, py)

            # Tangent line slopes computed from derivative f'(x) = -0.6x + 0.6
            slope = -0.6 * px + 0.6

            # Line length for visualization
            dx = 0.8
            dy = slope * dx
            start = point + np.array([-dx, -dy, 0])
            end = point + np.array([dx, dy, 0])

            dot = Dot(point, radius=0.08, color="#f38ba8")
            line = Line(start, end, color="#a6e3a1", stroke_width=2)

            label = MathTex(f"m={slope:.1f}", color="#a6e3a1", font_size=22).next_to(
                end, UP if slope >= 0 else DOWN, buff=0.15
            )

            point_dots.add(dot)
            slope_lines.add(line)
            slope_labels.add(label)

        # Steepness indicator arrows
        steepness_arrow = Arrow(
            axes.c2p(-2.5, -1.5), axes.c2p(-2.5, 1.0), color="#94e2d5", tip_length=0.2
        )
        steepness_label = Text(
            "Steepness\nchanges", font_size=22, color="#94e2d5", font="Sans"
        ).next_to(steepness_arrow, LEFT, buff=0.3)

        # Animation sequence

        # Phase 1: Write title and create axes (0-2s)
        self.play(Write(title), run_time=1.2)
        self.play(Create(axes), run_time=1.2)
        self.wait(0.2)

        # Fade out title slightly to focus on math
        self.play(title.animate.shift(UP * 0.3).set_opacity(0.7), run_time=0.4)

        # Phase 2: Draw the curve (2-3.7s)
        self.play(Create(curve), FadeIn(curve_label), run_time=1.5)

        # Phase 3: Show points and tangent lines (3.7-5.0s)
        self.play(
            LaggedStart(
                AnimationGroup(
                    FadeIn(point_dots[0]),
                    Create(slope_lines[0]),
                    FadeIn(slope_labels[0]),
                ),
                AnimationGroup(
                    FadeIn(point_dots[1]),
                    Create(slope_lines[1]),
                    FadeIn(slope_labels[1]),
                ),
                AnimationGroup(
                    FadeIn(point_dots[2]),
                    Create(slope_lines[2]),
                    FadeIn(slope_labels[2]),
                ),
                lag_ratio=0.4,
            ),
            run_time=1.5,
        )

        # Phase 4: Steepness indicator (5.0-5.8s)
        self.play(
            GrowFromCenter(steepness_arrow), FadeIn(steepness_label), run_time=0.6
        )

        self.wait(0.2)

        # Total: approximately 6.0 seconds
        # --- Scene 3: Step 3: Approximating with Secant Lines ---
        self.camera.background_color = "#181825"

        # TITLE
        title = Text("Approximating with Secant Lines", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)

        # MAIN NUMBERLINE
        main_line = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            include_numbers=True,
            include_tip=True,
            color="#f38ba8",
        )
        main_line.shift(DOWN * 0.5)

        # TWO NEARBY POINTS
        pt_a = Dot(main_line.n2p(-1.5), radius=0.1, color="#89b4fa")
        pt_b = Dot(main_line.n2p(1.5), radius=0.1, color="#fab387")

        # POINT LABELS
        label_a = MathTex("P_1", color="#89b4fa").next_to(pt_a, UP, buff=0.2)
        label_b = MathTex("P_2", color="#fab387").next_to(pt_b, UP, buff=0.2)

        # SECANT LINE (lifted slightly above the axis for visual clarity)
        secant = Line(
            pt_a.get_center(), pt_b.get_center(), color="#a6e3a1", stroke_width=3
        )
        secant.shift(UP * 0.6)

        # CURVED ARROW: "slide them closer together"
        arrow_closer = CurvedArrow(
            start_point=pt_a.get_center() + UP * 1.2 + LEFT * 0.3,
            end_point=pt_b.get_center() + UP * 1.2 + RIGHT * 0.3,
            angle=-PI / 4,
            color="#94e2d5",
        )

        # ─── ANIMATION SEQUENCE ───
        # 1.5s - Title appears
        self.play(Write(title), run_time=1.5)

        # 1.5s - NumberLine draws in
        self.play(Create(main_line), run_time=1.5)

        # 1.0s - Dots and labels pop in
        self.play(
            AnimationGroup(
                GrowFromCenter(pt_a),
                GrowFromCenter(pt_b),
                FadeIn(label_a, shift=UP * 0.3),
                FadeIn(label_b, shift=UP * 0.3),
            ),
            run_time=1.0,
        )

        # 1.0s - Secant line connects the two points
        self.play(Create(secant), run_time=1.0)

        # 1.0s - Curved arrow suggests sliding closer
        self.play(FadeIn(arrow_closer, shift=RIGHT), run_time=1.0)

        # 1.0s - Hold to let the viewer absorb the concept
        self.wait(1.0)
        # --- Scene 4: Step 4: The Tangent Line as Instantaneous Slope ---
        self.camera.background_color = "#181825"

        # 1. Title
        title_4 = Text(
            "The Tangent Line as Instantaneous Slope",
            font_size=36,
            color=WHITE,
        )
        title_4.to_edge(UP, buff=0.5)
        self.add(title_4)

        # 2. Axes & Curve (Parabola visual metaphor)
        ax = (
            Axes(
                x_range=[-1, 5, 1],
                y_range=[-1, 5, 1],
                x_length=6,
                y_length=4,
                axis_config={"color": "#89b4fa"},
                tips=False,
            )
            .scale(1.2)
            .move_to(ORIGIN)
        )

        def func(x):
            return 0.5 * (x - 1) ** 2 + 1

        curve = ax.plot(func, color="#a6e3a1", stroke_width=3)

        # 3. Points on the curve
        x_a = 1.5
        x_b = 3.5
        p_a = ax.c2p(x_a, func(x_a))
        p_b = ax.c2p(x_b, func(x_b))

        dot_a = Dot(point=p_a, color="#f38ba8", radius=0.10)
        dot_b = Dot(point=p_b, color="#fab387", radius=0.10)

        # 4. Secant Line
        secant = Line(p_a, p_b, color="#fab387", stroke_width=2.5)

        # 5. True Tangent line at point A (using infinitesimally small dx)
        tangent_helper = ax.get_secant_slope_group(
            x=x_a,
            graph=curve,
            dx=0.01,
            secant_line_color="#94e2d5",
            secant_line_length=6,
        )
        tangent_line = tangent_helper.secant_line
        tangent_line.set_stroke(width=3)

        # 6. Labels
        secant_label = MathTex(r"	ext{Secant}", color="#fab387", font_size=28)
        secant_label.move_to(secant.get_center() + UP * 0.3)

        tangent_label = MathTex(r"	ext{Tangent}", color="#94e2d5", font_size=28)
        tangent_label.move_to(tangent_line.get_center() + UP * 0.3)

        point_label = MathTex("P", color="#f38ba8", font_size=32)
        point_label.next_to(dot_a, UL, buff=0.12)

        # 7. Main VGroup
        main_4 = VGroup(
            ax,
            curve,
            dot_a,
            dot_b,
            secant,
            tangent_line,
            secant_label,
            tangent_label,
            point_label,
        )

        # ---- ANIMATIONS (Total = 6.0 seconds) ----
        self.play(Create(ax), run_time=1.0)
        self.play(Create(curve), run_time=1.0)
        self.play(GrowFromCenter(dot_a), GrowFromCenter(dot_b), run_time=0.5)
        self.play(Create(secant), FadeIn(secant_label), run_time=0.5)

        # The core visual: points merge, secant becomes tangent
        self.play(
            dot_b.animate.move_to(p_a),
            Transform(secant, tangent_line),
            ReplacementTransform(secant_label, tangent_label),
            run_time=2.0,
        )

        self.play(FadeIn(point_label), run_time=0.5)
        self.wait(0.5)
        # --- Scene 5: Step 5: The Limit Definition of the Derivative ---
        self.clear()

        # ===================================
        # CONFIGURATION
        # ===================================
        self.camera.background_color = "#181825"

        # Aesthetic colors
        teal = "#94e2d5"
        peach = "#fab387"
        pink = "#f38ba8"
        green = "#a6e3a1"

        # ===================================
        # OBJECTS DEFINITION
        # ===================================

        # Title at the top
        title = Text(
            "The Limit Definition of the Derivative", font_size=36, color=WHITE
        ).shift(UP * 3)

        # Main table: progression from average rate to instantaneous rate
        # Table must have all string entries - MathTex cannot be mixed directly in the table data
        row1 = ["Quantity", "Difference Quotient", "Limit as h→0", "Derivative"]
        row2 = ["Δy / Δx", "(f(x+h)−f(x)) / h", "lim h→0", "f '(x)"]

        table = Table(
            [row1, row2],
            include_outer_lines=True,
        ).scale(0.7)

        # Style header row
        for i in range(4):
            table.get_cell((1, i + 1)).set_fill(teal, opacity=0.1)
            table.get_entries((1, i + 1)).set_color(teal)

        # Style data row with color-coded progression
        table.get_entries((2, 1)).set_color(peach)  # Δy/Δx
        table.get_entries((2, 2)).set_color(peach)  # Difference quotient
        table.get_entries((2, 3)).set_color(pink)  # Limit operator
        table.get_entries((2, 4)).set_color(green)  # f'(x)

        table.move_to(ORIGIN)

        # Supporting label: Average Rate of Change
        label_avg = Text("Average Rate of Change", font_size=22, color=peach)
        label_avg.shift(DOWN * 2.2 + LEFT * 2)
        arrow_avg = Arrow(
            start=label_avg.get_top(),
            end=table.get_cell((2, 2)).get_bottom(),
            color=peach,
            stroke_width=2,
            buff=0.15,
        )

        # Supporting label: Limit / Shrinking Interval
        label_limit = Text("Shrinking Interval", font_size=22, color=pink)
        label_limit.shift(UP * 2.2)
        arrow_limit = CurvedArrow(
            start_point=table.get_cell((2, 2)).get_top() + UP * 0.1,
            end_point=table.get_cell((2, 4)).get_top() + UP * 0.1,
            color=pink,
            angle=-PI / 6,
            stroke_width=2,
        )

        # Supporting label: Instantaneous Rate
        label_inst = Text("Instantaneous Rate", font_size=22, color=green)
        label_inst.shift(DOWN * 2.2 + RIGHT * 2)
        arrow_inst = Arrow(
            start=label_inst.get_top(),
            end=table.get_cell((2, 4)).get_bottom(),
            color=green,
            stroke_width=2,
            buff=0.15,
        )

        # ===================================
        # ANIMATIONS (Total: ~6.0 seconds)
        # ===================================

        # Phase 1: Fade in the title (0.75s)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.75)

        # Phase 2: Grow the main Table from center (1.2s)
        self.play(GrowFromCenter(table), run_time=1.2)

        # Phase 3: Reveal "Average Rate" label and arrow (0.8s)
        self.play(
            FadeIn(label_avg, shift=RIGHT * 0.3),
            GrowFromCenter(arrow_avg),
            run_time=0.8,
        )

        # Phase 4: Show limit process with curved arrow flash (1.0s)
        self.play(
            FadeIn(label_limit, shift=DOWN * 0.3),
            ShowPassingFlash(arrow_limit, time_width=0.4),
            run_time=1.0,
        )

        # Phase 5: Reveal "Instantaneous Rate" label and arrow (0.8s)
        self.play(
            FadeIn(label_inst, shift=LEFT * 0.3),
            GrowFromCenter(arrow_inst),
            run_time=0.8,
        )

        # Phase 6: Emphasize the derivative cell with a pulse (1.0s)
        self.play(
            Indicate(table.get_entries((2, 4)), color=green, scale_factor=1.15),
            run_time=1.0,
        )

        # Phase 7: Hold to let concept sink in (0.45s)
        self.wait(0.45)

        # Total: 0.75 + 1.2 + 0.8 + 1.0 + 0.8 + 1.0 + 0.45 = 6.0 seconds
        # --- Scene 6: Step 6: Derivative Notation dy over dx ---
        self.clear()
        self.camera.background_color = "#181825"

        # === Title ===
        title = Text("Derivative Notation dy / dx", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)

        # === Main vertical fraction arrow at ORIGIN ===
        main_arrow = Arrow(
            start=UP * 1.5,
            end=DOWN * 1.5,
            stroke_width=6,
            tip_length=0.35,
            color="#cdd6f4",
        )

        # dy label above arrow
        dy_label = MathTex(r"dy", font_size=48, color="#89b4fa")
        dy_label.next_to(main_arrow.get_start(), UP, buff=0.3)

        # dx label below arrow
        dx_label = MathTex(r"dx", font_size=48, color="#f38ba8")
        dx_label.next_to(main_arrow.get_end(), DOWN, buff=0.3)

        # Supporting notation text below the main fraction
        notation = MathTex(r"\frac{dy}{dx}", font_size=72, color="#cdd6f4")
        notation.next_to(main_arrow, DOWN, buff=1.2)

        # === Explanatory pill on the left ===
        left_pill = RoundedRectangle(
            corner_radius=0.2,
            width=3.8,
            height=1.0,
            stroke_width=2,
            color="#fab387",
            fill_opacity=0.15,
        )
        left_pill.to_corner(LEFT + DOWN, buff=0.8)
        left_text = Text("Not a fraction!", font_size=24, color="#fab387")
        left_text.move_to(left_pill.get_center())

        # === Explanatory pill on the right ===
        right_pill = RoundedRectangle(
            corner_radius=0.2,
            width=4.2,
            height=1.0,
            stroke_width=2,
            color="#a6e3a1",
            fill_opacity=0.15,
        )
        right_pill.to_corner(RIGHT + DOWN, buff=0.8)
        right_text = Text("Limit shorthand", font_size=24, color="#a6e3a1")
        right_text.move_to(right_pill.get_center())

        # === Animations ===
        self.play(Write(title), run_time=0.8)
        self.play(GrowFromCenter(main_arrow), run_time=0.8)
        self.play(
            FadeIn(dy_label, shift=UP * 0.3),
            FadeIn(dx_label, shift=DOWN * 0.3),
            run_time=0.8,
        )
        self.play(Write(notation), run_time=0.8)
        self.play(FadeIn(left_pill, scale=0.8), Write(left_text), run_time=0.8)
        self.play(FadeIn(right_pill, scale=0.8), Write(right_text), run_time=0.8)
        self.wait(2.0)
        # --- Scene 7: Step 7: The Power Rule ---
        self.camera.background_color = "#181825"
        self.clear()

        # Colors
        c_primary = "#89b4fa"  # blue
        c_accent = "#fab387"  # orange
        c_green = "#a6e3a1"  # green
        c_white = "#CDD6F4"  # white

        # 1) Title text at top
        title = Text("The Power Rule", font_size=36, color=c_white).move_to(UP * 3)

        # 2) Main formula: d/dx (x^2) = 2x
        expr = MathTex(r"\frac{d}{dx}(x^2) = 2x", font_size=48, color=c_primary)
        # Split into parts to animate prettier
        expr_part1 = MathTex(r"\frac{d}{dx}(x^2)", font_size=48, color=c_primary)
        equals_sign = MathTex(r"=", font_size=48, color=c_primary)
        expr_part2 = MathTex(r"2x", font_size=48, color=c_primary)

        # Layout horizontally
        expr_group = VGroup(expr_part1, equals_sign, expr_part2).arrange(
            RIGHT, buff=0.3
        )
        expr_group.move_to(ORIGIN)

        # 3) A brace to emphasize the "process"
        brace = Brace(expr_part1, direction=UP, color=c_accent, buff=0.15)
        brace_label = MathTex(r"2 \cdot x^{2-1}", font_size=30, color=c_accent)
        brace_label.next_to(brace, UP, buff=0.2)

        # 4) Explanation label under the equation
        explanation = Text(
            "Bring down the exponent, then subtract one",
            font_size=24,
            color=c_green,
        )
        explanation.next_to(expr_group, DOWN, buff=0.8)

        # --- SCENE TIMELINE (target 6.0 seconds) ---

        # Step 1: Write title & bring in derivative notation
        self.play(Write(title), Write(expr_part1), run_time=1.2)

        # Step 2: Fade in equals sign & result, and the brace with its label
        self.play(Write(equals_sign), Write(expr_part2), run_time=1.0)

        self.play(
            GrowFromCenter(brace), FadeIn(brace_label, shift=UP * 0.3), run_time=1.0
        )

        # Step 3: Show the textual explanation
        self.play(FadeIn(explanation), run_time=1.0)

        # Final hold to hit the 6.0s mark exactly
        self.wait(1.8)
        # --- Scene 8: Step 8: Sign of the Derivative ---
        self.clear()
        self.camera.background_color = "#181825"

        # Title
        title = Text("Sign of the Derivative", font_size=36, color=WHITE).move_to(
            UP * 3
        )

        # Create Axes
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-2, 2],
            axis_config={
                "color": "#fab387",
                "stroke_width": 2.0,
            },
        )
        axes.move_to(ORIGIN)

        # Function: cosine-like curve for clear increasing/peak/decreasing visualization
        curve = axes.plot(
            lambda x: 1.2 * np.cos(x * 0.6),
            x_range=[-3, 3],
            color="#89b4fa",
            stroke_width=3,
        )

        # Peak / zero derivative point
        peak_x = 0
        peak_point = axes.coords_to_point(peak_x, 1.2 * np.cos(peak_x * 0.6))

        # Increasing arrow (bottom left, left-to-right = positive)
        growing_arrow = Arrow(
            start=axes.coords_to_point(-2.5, -1.3),
            end=axes.coords_to_point(-1.0, -1.3),
            color="#a6e3a1",
            buff=0.0,
        )
        growing_label = Text("Positive (↑)", font_size=22, color="#a6e3a1").next_to(
            growing_arrow, UP, buff=0.15
        )

        # Zero marker
        zero_marker = Dot(peak_point, radius=0.1, color="#f38ba8")
        zero_label = Text("Zero", font_size=22, color="#f38ba8").next_to(
            zero_marker, UP * 0.8 + RIGHT * 0.5
        )

        # Decreasing arrow (bottom right, left-to-right pointing down = negative)
        falling_arrow = Arrow(
            start=axes.coords_to_point(1.0, -1.3),
            end=axes.coords_to_point(2.5, -1.3),
            color="#f38ba8",
            buff=0.0,
        )
        falling_label = Text("Negative (↓)", font_size=22, color="#f38ba8").next_to(
            falling_arrow, UP, buff=0.15
        )

        # Curved arrows following the slope along the function
        pos_arrow = CurvedArrow(
            axes.coords_to_point(-2.3, -0.8),
            axes.coords_to_point(-1.3, 0.2),
            angle=PI / 5,
            color="#a6e3a1",
            stroke_width=3,
        )
        neg_arrow = CurvedArrow(
            axes.coords_to_point(1.3, 0.2),
            axes.coords_to_point(2.3, -0.8),
            angle=-PI / 5,
            color="#f38ba8",
            stroke_width=3,
        )

        # Build the scene with creative animations
        # 1. Title and axes appear
        self.play(Write(title), run_time=0.8)
        self.play(Create(axes), run_time=1.0)

        # 2. Draw function from center outward
        self.play(GrowFromCenter(curve), run_time=1.2)

        # 3. Show positive / increasing region
        self.play(Create(pos_arrow), FadeIn(growing_label), run_time=0.8)

        # 4. Mark zero/peak
        self.play(FadeIn(zero_marker), Write(zero_label), run_time=0.6)

        # 5. Show negative / decreasing region
        self.play(Create(neg_arrow), FadeIn(falling_label), run_time=0.8)

        # 6. Remaining dwell time to match 6.0s total
        # Current total: 0.8 + 1.0 + 1.2 + 0.8 + 0.6 + 0.8 = 5.2
        self.wait(0.8)
        # --- Scene 9: Step 9: Higher-Order Derivatives and Concavity ---
        self.camera.background_color = "#181825"
        config.frame_width = 14
        config.frame_height = 8

        # ===== 1. DEFINE OBJECTS =====

        # Main NumberLine representing the real line of possible concavity values
        main_line = NumberLine(
            x_range=[-5, 5],
            length=10,
            color="#f38ba8",
            include_tip=True,
            tip_width=0.2,
            tip_height=0.2,
            include_ticks=True,
            tick_size=0.15,
        ).shift(DOWN)

        # Add tick labels
        tick_labels = main_line.add_numbers(font_size=24, color="#94e2d5")

        # Title at top
        title = Text(
            "Higher-Order Derivatives and Concavity", font_size=36, color=WHITE
        ).to_edge(UP, buff=0.8)

        # Subtitle explaining second derivative
        subtitle = Text(
            "The second derivative measures how the rate of change is itself changing",
            font_size=20,
            color="#89b4fa",
        ).next_to(title, DOWN, buff=0.3)

        # Visual metaphor: curved arrows showing "bending" for concavity
        # Concave up (cup shape, f'' > 0)
        concave_up = Arc(
            radius=1.5,
            start_angle=-PI / 3,
            angle=2 * PI / 3,
            color="#a6e3a1",
            stroke_width=4,
        ).shift(LEFT * 3 + UP * 0.5)

        cup_label = Text("f'' > 0 : Concave Up", font_size=18, color="#a6e3a1").next_to(
            concave_up, DOWN, buff=0.2
        )

        # Concave down (cap shape, f'' < 0)
        concave_down = Arc(
            radius=1.5,
            start_angle=PI / 3,
            angle=-2 * PI / 3,
            color="#fab387",
            stroke_width=4,
        ).shift(RIGHT * 3 + UP * 0.5)

        cap_label = Text(
            "f'' < 0 : Concave Down", font_size=18, color="#fab387"
        ).next_to(concave_down, UP, buff=0.2)

        # Inflection point marker on the number line
        inflection_dot = Dot(point=main_line.n2p(0), color="#94e2d5", radius=0.12)

        inflection_label = Text(
            "Inflection Point\n(f'' = 0)", font_size=16, color="#94e2d5"
        ).next_to(inflection_dot, DOWN, buff=0.3)

        # Arrow labels for positive/negative regions
        pos_arrow = Arrow(
            start=main_line.n2p(1),
            end=main_line.n2p(3.5),
            color="#a6e3a1",
            tip_length=0.18,
            buff=0.1,
        )
        pos_label = MathTex(r"f'' > 0", color="#a6e3a1", font_size=28)
        pos_label.next_to(pos_arrow, UP, buff=0.15)

        neg_arrow = Arrow(
            start=main_line.n2p(-1),
            end=main_line.n2p(-3.5),
            stroke_width=2.0,
            color="#fab387",
            tip_length=0.18,
            buff=0.1,
        )
        neg_label = MathTex(r"f'' < 0", color="#fab387", font_size=28)
        neg_label.next_to(neg_arrow, UP, buff=0.15)

        # ===== 2. ANIMATIONS =====

        # Phase 1: Title and NumberLine appear (0-2s)
        self.play(Write(title), run_time=1.0)
        self.play(
            FadeIn(subtitle, shift=UP * 0.2),
            Create(main_line),
            FadeIn(tick_labels, lag_ratio=0.1),
            run_time=1.0,
        )

        # Phase 2: Add concavity visuals with GrowFromCenter (2-3.5s)
        self.play(
            GrowFromCenter(concave_up),
            Write(cup_label),
            GrowFromCenter(concave_down),
            Write(cap_label),
            run_time=0.8,
            rate_func=rate_functions.ease_out_bounce,
        )

        # Phase 3: Inflection point and arrows (3.5-4.5s)
        self.play(
            GrowFromCenter(inflection_dot),
            FadeIn(inflection_label, scale=1.2),
            run_time=0.5,
        )
        self.play(
            Create(pos_arrow),
            FadeIn(pos_label, shift=LEFT * 0.3),
            Create(neg_arrow),
            FadeIn(neg_label, shift=RIGHT * 0.3),
            run_time=0.5,
        )

        # Phase 4: Highlight inflection point briefly (4.5-5s)
        self.play(
            Indicate(inflection_dot, color="#f38ba8", scale_factor=1.5), run_time=0.5
        )

        # Final wait to pad to exactly 6.0 seconds
        # Time tally: 1 + 1 + 0.8 + 0.5 + 0.5 + 0.5 = 4.3
        # Need additional 1.7s
        self.wait(1.7)
        # --- Scene 10: Step 10: Applications of the Derivative ---
        self.clear()
        self.camera.background_color = "#181825"

        # --- 1. Title ---
        title = Text("Applications of the Derivative", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)

        # --- 2. Domain Application Icons (VGroups) ---
        # Physics
        physics_icon = VGroup(
            Circle(radius=0.4, color="#89b4fa", fill_opacity=0.2),
            Arrow(ORIGIN, UP * 0.6, color="#89b4fa", buff=0.05),
        ).shift(LEFT * 4 + UP * 0.8)
        physics_label = Text("Physics", font_size=24, color="#89b4fa").next_to(
            physics_icon, DOWN, buff=0.3
        )
        physics_desc = Text(
            "Velocity & Acceleration", font_size=18, color=WHITE
        ).next_to(physics_label, DOWN, buff=0.15)

        # Economics
        econ_icon = VGroup(
            Polygon(
                LEFT * 0.4, RIGHT * 0.4, UP * 0.6, color="#fab387", fill_opacity=0.2
            ),
            Dot(UP * 0.2, color="#fab387"),
        ).shift(LEFT * 1.3 + UP * 0.8)
        econ_label = Text("Economics", font_size=24, color="#fab387").next_to(
            econ_icon, DOWN, buff=0.3
        )
        econ_desc = Text("Marginal Cost / Revenue", font_size=18, color=WHITE).next_to(
            econ_label, DOWN, buff=0.15
        )

        # Optimization
        opt_icon = VGroup(
            Rectangle(height=0.5, width=0.5, color="#f38ba8", fill_opacity=0.2),
            Arrow(LEFT * 0.25, RIGHT * 0.25, color="#f38ba8", buff=0.05),
        ).shift(RIGHT * 1.3 + UP * 0.8)
        opt_label = Text("Optimization", font_size=24, color="#f38ba8").next_to(
            opt_icon, DOWN, buff=0.3
        )
        opt_desc = Text("Maxima & Minima", font_size=18, color=WHITE).next_to(
            opt_label, DOWN, buff=0.15
        )

        # Engineering
        eng_icon = VGroup(
            Square(side_length=0.5, color="#94e2d5", fill_opacity=0.2),
            Line(LEFT * 0.25, RIGHT * 0.25, color="#94e2d5"),
        ).shift(RIGHT * 4 + UP * 0.8)
        eng_label = Text("Engineering", font_size=24, color="#94e2d5").next_to(
            eng_icon, DOWN, buff=0.3
        )
        eng_desc = Text("Rates & Slopes", font_size=18, color=WHITE).next_to(
            eng_label, DOWN, buff=0.15
        )

        # --- 3. Central Derivative Symbol ---
        center_deriv = MathTex(r"\frac{d}{dx}", color="#a6e3a1", font_size=56)
        center_deriv.move_to(ORIGIN + DOWN * 2.2)

        # --- 4. Connecting Lines (Dashed) ---
        line_physics = DashedLine(
            physics_icon.get_bottom(), center_deriv.get_top(), color="#89b4fa"
        ).set_opacity(0.6)
        line_econ = DashedLine(
            econ_icon.get_bottom(), center_deriv.get_top(), color="#fab387"
        ).set_opacity(0.6)
        line_opt = DashedLine(
            opt_icon.get_bottom(), center_deriv.get_top(), color="#f38ba8"
        ).set_opacity(0.6)
        line_eng = DashedLine(
            eng_icon.get_bottom(), center_deriv.get_top(), color="#94e2d5"
        ).set_opacity(0.6)

        # --- 5. Main VGroup Assembly ---
        main_group = VGroup(
            physics_icon,
            physics_label,
            physics_desc,
            econ_icon,
            econ_label,
            econ_desc,
            opt_icon,
            opt_label,
            opt_desc,
            eng_icon,
            eng_label,
            eng_desc,
            center_deriv,
            line_physics,
            line_econ,
            line_opt,
            line_eng,
        )

        # --- 6. Animations (Total = 6.0s) ---
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        self.play(
            GrowFromCenter(physics_icon),
            FadeIn(physics_label),
            FadeIn(physics_desc),
            run_time=1,
        )
        self.play(
            GrowFromCenter(econ_icon), FadeIn(econ_label), FadeIn(econ_desc), run_time=1
        )
        self.play(
            GrowFromCenter(opt_icon), FadeIn(opt_label), FadeIn(opt_desc), run_time=1
        )
        self.play(
            GrowFromCenter(eng_icon), FadeIn(eng_label), FadeIn(eng_desc), run_time=1
        )

        self.wait(0.3)

        self.play(
            FadeIn(line_physics),
            FadeIn(line_econ),
            FadeIn(line_opt),
            FadeIn(line_eng),
            run_time=0.7,
        )
        self.play(GrowFromCenter(center_deriv), run_time=1)

        self.wait(1.0)
