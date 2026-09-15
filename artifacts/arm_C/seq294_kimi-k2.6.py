import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Vectors as arrows in a coordinate plane ---
        self.clear()

        # ------------------------------------------------------------------
        # 1. Objects
        # ------------------------------------------------------------------

        # Coordinate grid – custom background line style emphasizes the plane
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=7,
            y_length=7,
            background_line_style={
                "stroke_color": "#89b4fa",
                "stroke_width": 1,
            },
        )

        # Vector v = (3, 2): an arrow from the origin to the point (3, 2)
        # Use grid.c2p(0, 0) and grid.c2p(3, 2) so the arrow stays locked
        # to the grid even if the layout shifts.
        vector_arrow = Arrow(
            start=grid.c2p(0, 0),
            end=grid.c2p(3, 2),
            color="#f38ba8",
            stroke_width=2.5,
            buff=0,
        )

        # Label v = (3, 2) positioned near the arrow tip
        vector_label = MathTex(
            r"\vec{v} = \langle 3, 2 \rangle", color="#f38ba8"
        ).scale(0.9)
        vector_label.next_to(vector_arrow.get_end(), UR, buff=0.2)

        # ------------------------------------------------------------------
        # 2. Animations
        # ------------------------------------------------------------------

        # Draw the coordinate plane into existence
        self.play(Create(grid), run_time=2.5)

        # Reveal the vector arrow
        self.play(FadeIn(vector_arrow), run_time=1.5)

        # Bring in the label after the arrow is visible
        self.play(FadeIn(vector_label), run_time=1.0)

        # ------------------------------------------------------------------
        # 3. Hold to match narration duration
        # ------------------------------------------------------------------
        self.wait(4.0)
        # --- Scene 2: Matrix as a transformation that stretches and rotates space ---
        self.camera.background_color = "#181825"

        # Original grid - "Before"
        original_grid = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            background_line_style={
                "stroke_color": "#89b4fa",
                "stroke_width": 1,
            },
        ).shift(LEFT * 3.5)

        original_label = Text("Before", font_size=36, color="#89b4fa")
        original_label.move_to([-3.5, -3, 0])

        # Transformed grid - "After A"
        transformed_grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=5.5,
            y_length=5,
            background_line_style={
                "stroke_color": "#fab387",
                "stroke_width": 1,
            },
        ).shift(RIGHT * 3.5)

        transformed_label = Text("After A", font_size=36, color="#fab387")
        transformed_label.move_to([3.5, -3, 0])

        # Transformation arrow with label
        arrow = Arrow(
            start=[-1.5, 0, 0], end=[1.5, 0, 0], color="#a6e3a1", stroke_width=2
        )
        arrow_label = MathTex("A", color="#a6e3a1", font_size=48)
        arrow_label.next_to(arrow, UP, buff=0.15)

        # Add vectors at grid points for visual richness (Before)
        vectors_before = VGroup()
        for x in [-2, -1, 0, 1, 2]:
            for y in [-2, -1, 0, 1, 2]:
                vec = Arrow(
                    start=original_grid.c2p(x, y),
                    end=original_grid.c2p(x + 0.5, y + 0.2),
                    color="#89b4fa",
                    stroke_width=1.5,
                    buff=0,
                )
                vectors_before.add(vec)

        # Corresponding transformed vectors (After)
        vectors_after = VGroup()
        for x in [-2, -1, 0, 1, 2]:
            for y in [-2, -1, 0, 1, 2]:
                # Simple linear transformation: shear + stretch
                t_start = (x * 1.2, y * 0.8 + x * 0.3)
                t_end = ((x + 0.5) * 1.2, (y + 0.2) * 0.8 + (x + 0.5) * 0.3)
                vec = Arrow(
                    start=transformed_grid.c2p(t_start[0], t_start[1]),
                    end=transformed_grid.c2p(t_end[0], t_end[1]),
                    color="#fab387",
                    stroke_width=1.5,
                    buff=0,
                )
                vectors_after.add(vec)

        # Animation sequence
        self.play(FadeIn(original_grid), FadeIn(original_label), run_time=1.5)

        self.play(
            LaggedStart(*[GrowFromCenter(v) for v in vectors_before], lag_ratio=0.02),
            run_time=1.5,
        )
        self.wait(0.5)

        self.play(GrowFromCenter(arrow), FadeIn(arrow_label), run_time=1.5)
        self.wait(0.5)

        self.play(FadeIn(transformed_grid), FadeIn(transformed_label), run_time=2.0)

        self.play(
            LaggedStart(*[GrowFromCenter(v) for v in vectors_after], lag_ratio=0.02),
            run_time=1.5,
        )

        # Brief pulse/highlight to emphasize the transformation concept
        highlight_box = SurroundingRectangle(
            VGroup(transformed_grid, transformed_label, vectors_after),
            color="#f38ba8",
            buff=0.2,
        )
        self.play(Create(highlight_box), run_time=0.5)
        self.play(FadeOut(highlight_box), run_time=0.5)

        self.wait(0.5)
        # --- Scene 3: How most vectors change direction under transformation ---
        self.clear()
        self.camera.background_color = "#181825"

        # --- Define Objects ---

        # Before arrow v (blue)
        before_arrow = Arrow(
            start=(-0.5, -1, 0),
            end=(0.5, 1, 0),
            stroke_width=2.5,
            buff=0,
            color="#89b4fa",
        )
        before_label = MathTex("v", color="#89b4fa").next_to(
            before_arrow.get_end(), UL, buff=0.15
        )
        before_group = VGroup(before_arrow, before_label)

        # After arrow Av (orange)
        after_arrow = Arrow(
            start=(2.5, -1, 0),
            end=(4.2, 0.3, 0),
            stroke_width=2.5,
            buff=0,
            color="#fab387",
        )
        after_label = MathTex("Av", color="#fab387").next_to(
            after_arrow.get_end(), UR, buff=0.15
        )
        after_group = VGroup(after_arrow, after_label)

        # Angle indicator (pink) showing change in direction on the after-arrow
        angle_arc = Arc(
            radius=1.2, start_angle=0.9, angle=0.8, color="#f38ba8", stroke_width=2.5
        )
        angle_arc.move_to(after_arrow.get_start())

        # Label for the arc
        angle_label = Text("changed direction", font_size=24, color="#f38ba8")
        angle_label.next_to(angle_arc, DOWN, buff=0.15)

        # --- Animations ---

        self.play(GrowFromCenter(before_arrow), FadeIn(before_label), run_time=1.0)
        self.wait(0.5)

        # Show the transformation concept
        transform_text = Text("Transformation", font_size=36, color="#94e2d5")
        transform_text.move_to((1.85, 0, 0))
        self.play(FadeIn(transform_text), run_time=0.8)
        self.wait(0.5)

        # Fade out text, reveal after_arrow then angle indicator
        self.play(
            FadeOut(transform_text),
            GrowFromCenter(after_arrow),
            FadeIn(after_label),
            run_time=1.5,
        )
        self.wait(0.5)

        self.play(Create(angle_arc), FadeIn(angle_label), run_time=1.0)
        self.wait(1.0)

        # Highlight the difference between before and after
        self.play(
            before_arrow.animate.set_stroke_width(4),
            after_arrow.animate.set_stroke_width(4),
            run_time=0.5,
        )
        self.play(
            before_arrow.animate.set_stroke_width(2.5),
            after_arrow.animate.set_stroke_width(2.5),
            run_time=0.5,
        )
        self.wait(1.2)

        # Ensure total duration matches 9.5
        # 1.0 + 0.5 + 0.8 + 0.5 + 1.5 + 0.5 + 1.0 + 1.0 + 0.5 + 0.5 + 1.2 = 9.0
        # Adding 0.5 more wait at end to match 9.5
        self.wait(0.5)
        # --- Scene 4: Eigenvectors: special vectors that preserve their direction ---
        self.camera.background_color = "#181825"

        # Define colors
        BLUE_COLOR = "#89b4fa"
        ORANGE_COLOR = "#fab387"
        PINK_COLOR = "#f38ba8"
        TEAL_COLOR = "#94e2d5"
        WHITE_COLOR = "#ECEFF4"

        # --- 1. Create the two NumberPlanes ---
        # Left: original grid (blue tinted)
        original_plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=6,
            y_length=6,
            background_line_style={
                "stroke_color": BLUE_COLOR,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "stroke_color": BLUE_COLOR,
                "stroke_width": 2,
            },
        ).shift(LEFT * 3.5)

        # Right: transformed grid (orange tinted)
        transformed_plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=6,
            y_length=6,
            background_line_style={
                "stroke_color": ORANGE_COLOR,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "stroke_color": ORANGE_COLOR,
                "stroke_width": 2,
            },
        ).shift(RIGHT * 3.5)

        # --- 2. Create the eigenvector arrows ---
        # Original eigenvector on left plane
        v_start = original_plane.c2p(-0.75, -1.125)
        v_end = original_plane.c2p(0.75, 1.125)

        original_eigenvector = Arrow(
            start=v_start,
            end=v_end,
            color=BLUE_COLOR,
            stroke_width=2.5,
            buff=0,
        )

        # Transformed eigenvector on right plane
        Av_start = transformed_plane.c2p(-1.5, -2.25)
        Av_end = transformed_plane.c2p(1.5, 2.25)

        transformed_eigenvector = Arrow(
            start=Av_start,
            end=Av_end,
            color=ORANGE_COLOR,
            stroke_width=2.5,
            buff=0,
        )

        # --- 3. Dashed line showing same direction ---
        # The line passes through both arrows, showing they lie on same line
        same_line = DashedLine(
            start=original_plane.c2p(-3, -4.5),
            end=transformed_plane.c2p(3, 4.5),
            color=TEAL_COLOR,
            stroke_width=1.5,
        )

        # --- 4. Labels ---
        v_label = MathTex("v", color=BLUE_COLOR).next_to(
            original_eigenvector.get_end(), RIGHT
        )
        Av_label = MathTex("Av", color=ORANGE_COLOR).next_to(
            transformed_eigenvector.get_center(), RIGHT * 0.5 + UP * 0.2
        )

        # --- 5. Background grid labels ---
        original_label = Text("Original Space", font_size=24, color=BLUE_COLOR)
        original_label.to_edge(UP).shift(LEFT * 3.5)

        transformed_label = Text("Transformed Space", font_size=24, color=ORANGE_COLOR)
        transformed_label.to_edge(UP).shift(RIGHT * 3.5)

        # --- Animations ---
        # Show grids
        self.play(
            Create(original_plane),
            Create(transformed_plane),
            FadeIn(original_label),
            FadeIn(transformed_label),
            run_time=2.0,
        )

        # Show the same line (the key insight!)
        self.play(Create(same_line), run_time=1.5)

        # Show arrows emerging from the line
        self.play(
            GrowFromCenter(original_eigenvector),
            GrowFromCenter(transformed_eigenvector),
            run_time=1.25,
        )

        # Show labels
        self.play(
            Write(v_label),
            Write(Av_label),
            run_time=0.75,
        )

        # Highlight that they are on the same line
        self.play(
            Indicate(same_line, scale_factor=1.05, color=PINK_COLOR),
            run_time=1.0,
        )

        # Pause to let the concept sink in
        self.wait(1.0)

        # Emphasis animation: pulse the transformed eigenvector
        # to show only length changed (direction stayed same)
        self.play(
            transformed_eigenvector.animate.scale(
                1.2, about_point=transformed_plane.c2p(0, 0)
            ),
            run_time=1.0,
            rate_func=there_and_back,
        )

        # Final wait
        self.wait(1.5)
        # --- Scene 5: Eigenvalue as the scalar stretch or shrink factor ---
        self.clear()
        self.camera.background_color = "#181825"

        C_BLUE = "#89b4fa"
        C_ORANGE = "#fab387"
        C_PINK = "#f38ba8"

        # Eigenvector before transformation: v
        before_arrow = Arrow(
            start=(-2.5, -0.75, 0),
            end=(-1.5, 0.75, 0),
            color=C_BLUE,
            stroke_width=2.5,
            buff=0,
            tip_length=0.3,
        )

        # Eigenvector after transformation: Av = 2v
        after_arrow = Arrow(
            start=(1.5, -1.5, 0),
            end=(3.5, 1.5, 0),
            color=C_ORANGE,
            stroke_width=2.5,
            buff=0,
            tip_length=0.3,
        )

        # Origin reference dots
        dot_before = Dot(before_arrow.get_start(), radius=0.06, color=C_BLUE)
        dot_after = Dot(after_arrow.get_start(), radius=0.06, color=C_ORANGE)

        # Vector labels
        label_v = MathTex("v", color=C_BLUE).next_to(
            before_arrow.get_end(), UL, buff=0.15
        )
        label_Av = MathTex("Av", color=C_ORANGE).next_to(
            after_arrow.get_end(), UR, buff=0.15
        )

        # Brace between arrow tips indicating scalar factor
        scale_brace = (
            BraceBetweenPoints(
                before_arrow.get_end(), after_arrow.get_end(), direction=UP
            )
            .set_color(C_PINK)
            .set_stroke(width=2)
        )

        brace_label = scale_brace.get_tex(r"\lambda = 2").set_color(C_PINK)

        # --- Animations ---

        # Phase 1: Original eigenvector v
        self.play(FadeIn(dot_before), run_time=0.3)
        self.play(Create(before_arrow), run_time=1.0)
        self.play(Write(label_v), run_time=0.5)
        self.wait(0.5)

        # Phase 2: Transformed eigenvector Av
        self.play(FadeIn(dot_after), run_time=0.3)
        self.play(Create(after_arrow), run_time=1.0)
        self.play(Write(label_Av), run_time=0.5)
        self.wait(0.5)

        # Phase 3: Reveal scaling relationship
        self.play(GrowFromCenter(scale_brace), run_time=1.0)
        self.play(Write(brace_label), run_time=0.5)
        self.wait(0.5)

        # Phase 4: Emphasize eigenvalue
        self.play(
            Indicate(brace_label, scale_factor=1.3),
            Indicate(after_arrow, scale_factor=1.05),
            run_time=1.5,
        )
        self.wait(2.4)
        # --- Scene 6: The eigenvalue equation: Av equals lambda v ---
        self.clear()
        self.camera.background_color = "#181825"

        # --- Objects ---

        # Matrix A (colored entries + brackets)
        matrix_A = Matrix([["2", "1"], ["1", "3"]], h_buff=0.8, v_buff=0.8)
        matrix_A.set_color("#89b4fa")
        matrix_A.move_to([-4, 0, 0])

        label_A = MathTex(r"A", color="#89b4fa", font_size=48)
        label_A.next_to(matrix_A, UP, buff=0.2)

        # Original eigenvector v
        eigenvector_v = Arrow(
            start=[-0.5, -0.75, 0],
            end=[0.5, 0.75, 0],
            buff=0,
            stroke_width=2.5,
            color="#a6e3a1",
        )
        eigenvector_v.shift([-1.5, 0, 0])

        label_v = MathTex(r"\mathbf{v}", color="#a6e3a1", font_size=48)
        label_v.next_to(eigenvector_v, UP, buff=0.2)

        # Equals sign
        equals_sign = MathTex(r"=", color="#94e2d5", font_size=72)
        equals_sign.move_to([0.5, 0, 0])

        # Scalar lambda
        scalar_lambda = MathTex(r"\lambda = 2", color="#f38ba8", font_size=48)
        scalar_lambda.move_to([2, 0.5, 0])

        # Left result arrow Av
        result_arrow_left = Arrow(
            start=[-0.5, -0.75, 0],
            end=[1, 1.5, 0],
            buff=0,
            stroke_width=2.5,
            color="#fab387",
        )
        result_arrow_left.shift([-1.5, -1.5, 0])

        label_Av = MathTex(r"A\mathbf{v}", color="#fab387", font_size=48)
        label_Av.next_to(result_arrow_left, UP, buff=0.2)

        # Right result arrow lambda v
        result_arrow_right = Arrow(
            start=[-0.5, -0.75, 0],
            end=[1, 1.5, 0],
            buff=0,
            stroke_width=2.5,
            color="#fab387",
        )
        result_arrow_right.shift([3.5, -1.5, 0])

        label_lambda_v = MathTex(r"\lambda \mathbf{v}", color="#fab387", font_size=48)
        label_lambda_v.next_to(result_arrow_right, RIGHT, buff=0.2)

        # Dashed line connecting the tips of the two result arrows
        dashed_connector = DashedLine(
            start=result_arrow_left.get_end(),
            end=result_arrow_right.get_end(),
            color="#94e2d5",
            dash_length=0.15,
        )

        # --- Animations ---
        # Target total: 11.0 seconds

        # Step 1: Show matrix A (1.0s)
        self.play(FadeIn(matrix_A), FadeIn(label_A), run_time=1.0)

        # Step 2: Show eigenvector v (1.0s)
        self.play(FadeIn(eigenvector_v), FadeIn(label_v), run_time=1.0)

        # Step 3: Show equals sign (1.0s)
        self.play(Write(equals_sign), run_time=1.0)

        # Step 4: Show lambda scalar value (1.0s)
        self.play(FadeIn(scalar_lambda), run_time=1.0)

        # Step 5: Show right result arrow (1.0s)
        self.play(FadeIn(result_arrow_right), FadeIn(label_lambda_v), run_time=1.0)

        # Step 6: Show left result arrow (1.0s)
        self.play(FadeIn(result_arrow_left), FadeIn(label_Av), run_time=1.0)

        # Step 7: Draw dashed connector to show they match (1.5s)
        self.play(Create(dashed_connector), run_time=1.5)

        # Step 8: Pulse both arrows to emphasize equality (1.5s)
        self.play(
            Indicate(result_arrow_left, scale_factor=1.1, color="#f38ba8"),
            Indicate(result_arrow_right, scale_factor=1.1, color="#f38ba8"),
            run_time=1.5,
        )

        # Final hold (1.5s)
        self.wait(1.5)
        # --- Scene 7: Finding eigenvalues via the characteristic equation ---
        self.clear()
        # --- Scene 7: Finding eigenvalues via the characteristic equation ---
        # Config
        bg_color = "#181825"
        self.camera.background_color = bg_color
        blue = "#89b4fa"
        peach = "#fab387"
        pink = "#f38ba8"
        green = "#a6e3a1"
        teal = "#94e2d5"
        default_stroke = 2.0

        # === Matrix A - lambda*I ===
        matrix = Matrix(
            [[r"2-\lambda", r"1"], [r"1", r"3-\lambda"]],
            bracket_h_buff=0.25,
            bracket_v_buff=0.25,
        )
        matrix.set_color(blue)
        matrix.shift(np.array([-3.5, 1.5, 0]))

        # === det(...) = 0 label ===
        det_label = MathTex(r"\det(A - \lambda I) = 0", color=teal)
        det_label.scale(1.2)
        det_label.shift(np.array([1, 1.5, 0]))

        # === Characteristic polynomial text ===
        char_eq = MathTex(r"(2-\lambda)(3-\lambda) - 1 = 0", color=peach)
        char_eq.next_to(det_label, DOWN, buff=0.6)
        char_eq.scale(0.9)

        # Expanding
        expanded = MathTex(r"\lambda^2 - 5\lambda + 5 = 0", color=peach)
        expanded.move_to(char_eq.get_center())

        # === Axes for polynomial curve ===
        axes = Axes(
            x_range=[-2, 5, 1],
            y_range=[-3, 6, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": green, "include_tip": True},
            x_axis_config={"numbers_to_include": []},
            y_axis_config={"numbers_to_include": []},
        )
        axes.shift(np.array([0, -1.5, 0]))

        # Axis labels
        x_label = MathTex(r"\lambda", color=green).next_to(axes.x_axis, RIGHT)
        y_label = MathTex(r"p(\lambda)", color=green).next_to(axes.y_axis, UP)

        # === Parabola graph: p(lambda) = lambda^2 - 5lambda + 5 ===
        # Vertices: lambda = 2.5, p=-1.25; roots: (5+-sqrt(5))/2 ~ 1.382, 3.618
        parabola = axes.plot(
            lambda x: x**2 - 5 * x + 5,
            x_range=[-1.2, 4.2],
            color=peach,
            stroke_width=default_stroke,
        )

        # === Eigenvalue dots on x-axis ===
        lambda1_val = (5 - np.sqrt(5)) / 2
        lambda2_val = (5 + np.sqrt(5)) / 2

        dot1 = Dot(axes.c2p(lambda1_val, 0), radius=0.12, color=pink)
        dot2 = Dot(axes.c2p(lambda2_val, 0), radius=0.12, color=pink)

        label1 = MathTex(r"\lambda_1", color=pink).next_to(dot1, DOWN, buff=0.2)
        label2 = MathTex(r"\lambda_2", color=pink).next_to(dot2, DOWN, buff=0.2)

        # === Zero line highlight ===
        zero_line = DashedLine(
            axes.c2p(-2, 0), axes.c2p(5, 0), color=green, stroke_width=1
        )

        # === Animation timing total 11.5s ===
        # Step 1: Fade in matrix and det label (~2s)
        self.play(FadeIn(matrix), FadeIn(det_label), run_time=2.0)
        self.wait(0.5)

        # Step 2: Show characteristic equation (~2s)
        self.play(Write(char_eq), run_time=2.0)
        self.wait(0.5)

        # Step 3: Expand to simplified polynomial (~2s)
        self.play(ReplacementTransform(char_eq, expanded), run_time=2.0)
        self.wait(0.5)

        # Step 4: Transform polynomial text into graph & show axes (~2.5s)
        self.play(
            FadeIn(axes),
            FadeIn(x_label),
            FadeIn(y_label),
            FadeIn(zero_line),
            ReplacementTransform(expanded.copy(), parabola),
            run_time=2.5,
        )
        self.wait(0.5)

        # Step 5: Mark eigenvalues on x-axis (~1s)
        self.play(
            FadeIn(dot1, scale=0.5),
            FadeIn(dot2, scale=0.5),
            FadeIn(label1),
            FadeIn(label2),
            run_time=1.0,
        )

        # Final wait to hit exact duration
        total_used = 2.0 + 0.5 + 2.0 + 0.5 + 2.0 + 0.5 + 2.5 + 0.5 + 1.0
        remaining = 11.5 - total_used
        if remaining > 0:
            self.wait(remaining)
        # --- Scene 8: Solving for eigenvectors by substitution ---
        self.clear()

        # Background
        self.camera.background_color = "#181825"

        # ── Top equation: (A - λI)v = 0 with substituted value ──
        matrix = Matrix(
            [["-2", "1"], ["1", "1"]], bracket_h_buff=0.2, bracket_v_buff=0.2
        )
        matrix.move_to([-3.5, 2, 0])
        matrix.set_color("#89b4fa")

        eigenvector_v = Arrow(
            start=[-0.5, -0.75, 0], end=[0.5, 0.75, 0], buff=0, stroke_width=2.5
        )
        eigenvector_v.move_to([0, 2, 0])
        eigenvector_v.set_color("#a6e3a1")

        equals_zero = MathTex(r"= 0")
        equals_zero.move_to([2.5, 2, 0])
        equals_zero.set_color("#94e2d5")

        # ── Coordinate plane showing the system ──
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": "#94e2d5", "stroke_width": 1.5},
            tips=True,
        )
        axes.move_to([0, -0.8, 0])

        # Line 1: -2x + y = 0  →  y = 2x
        line_1 = Line(start=[-2, -4, 0], end=[2, 4, 0], stroke_width=2.5)
        line_1.set_color("#fab387")

        # Line 2: x + y = 0  →  y = -x
        line_2 = Line(start=[-2.5, 2.5, 0], end=[2.5, -2.5, 0], stroke_width=2.5)
        line_2.set_color("#89b4fa")

        # Eigenvector direction: dashed line showing the solution space
        eigenvector_direction = DashedLine(
            start=[-2, -4, 0], end=[2, 4, 0], stroke_width=3, dashed_ratio=0.15
        )
        eigenvector_direction.set_color("#f38ba8")

        # Labels
        line_1_label = MathTex(r"-2x + y = 0", font_size=26)
        line_1_label.set_color("#fab387")
        line_1_label.move_to([2.2, -1.0, 0])

        line_2_label = MathTex(r"x + y = 0", font_size=26)
        line_2_label.set_color("#89b4fa")
        line_2_label.move_to([2.2, 1.2, 0])

        direction_label = MathTex(r"	ext{eigenvector direction}", font_size=22)
        direction_label.set_color("#f38ba8")
        direction_label.move_to([0, 1.8, 0])

        # ── Animation timing ──
        # Step 1: Show substituted matrix equation (1.5s)
        self.play(FadeIn(matrix), run_time=1.5)

        # Step 2: Show eigenvector and equals zero (1.0s)
        self.play(FadeIn(eigenvector_v), FadeIn(equals_zero), run_time=1.0)
        self.wait(0.5)

        # Step 3: Bring in coordinate plane (1.0s)
        self.play(FadeIn(axes), run_time=1.0)

        # Step 4: Draw first equation line (1.5s)
        self.play(Create(line_1), Write(line_1_label), run_time=1.5)
        self.wait(0.5)

        # Step 5: Draw second equation line (1.5s)
        self.play(Create(line_2), Write(line_2_label), run_time=1.5)
        self.wait(0.5)

        # Step 6: Fade out second (dependent) equation line (0.8s)
        self.play(FadeOut(line_2), FadeOut(line_2_label), run_time=0.8)

        # Step 7: Highlight the eigenvector direction (1.5s)
        self.play(Create(eigenvector_direction), FadeIn(direction_label), run_time=1.5)
        self.wait(0.5)

        # Step 8: Pulse the direction line (1.0s)
        self.play(
            Indicate(eigenvector_direction, color="#f38ba8", scale_factor=1.05),
            run_time=1.0,
        )

        # Final wait to hit exactly 12.0s
        total_used = (
            1.5 + 1.0 + 0.5 + 1.0 + 1.5 + 0.5 + 1.5 + 0.5 + 0.8 + 1.5 + 0.5 + 1.0
        )
        remaining = 12.0 - total_used
        if remaining > 0:
            self.wait(remaining)
