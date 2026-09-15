import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Vectors and Transformations ---
        self.clear()
        # --- Scene 1: Vectors and Transformations ---

        # Define colors
        COLOR_GRID = "#7AA2F7"
        COLOR_GRID_LINES = "#565F89"
        COLOR_INPUT_ARROW = "#F7768E"
        COLOR_TRANSFORMED_GRID = "#BB9AF7"
        COLOR_OUTPUT_ARROW = "#E0AF68"
        COLOR_LABEL_TEXT = "#C0CAF5"

        # Create the original number plane on the left
        original_grid = NumberPlane(
            x_range=(-5, 5, 1),
            y_range=(-4, 4, 1),
            x_length=7,
            y_length=6,
            background_line_style={"stroke_color": COLOR_GRID_LINES, "stroke_width": 1},
        )
        original_grid.set_color(COLOR_GRID)
        original_grid.move_to(LEFT * 3.5)

        # Create the input arrow (originates at origin of left grid)
        input_arrow = Arrow(
            start=LEFT * 3.5 + DOWN * 1,
            end=LEFT * 1 + UP * 1,
            color=COLOR_INPUT_ARROW,
            stroke_width=3,
        )

        # Create labels
        original_label = Text("Original Space", font_size=24, color=COLOR_GRID_LINES)
        original_label.next_to(original_grid, UP, buff=0.5)

        input_label = MathTex(r"\mathbf{v}", color=COLOR_INPUT_ARROW, font_size=36)
        input_label.next_to(input_arrow, UP, buff=0.2)

        # Create the output arrow (horizontal stretch)
        # Start and end points maintain logical coordinates
        output_arrow = Arrow(
            start=RIGHT * 3.5 + DOWN * 1,
            end=RIGHT * 6 + UP * 1,
            color=COLOR_OUTPUT_ARROW,
            stroke_width=3,
        )

        # Create labels for transformed side
        transformed_label = Text(
            "Transformed Space", font_size=24, color=COLOR_GRID_LINES
        )
        transformed_label.next_to(original_grid, UP, buff=0.5)
        transformed_label.shift(RIGHT * 7)

        output_label = MathTex(r"A\mathbf{v}", color=COLOR_OUTPUT_ARROW, font_size=36)
        output_label.next_to(output_arrow, UP, buff=0.2)

        # Create the tranformation label at top center
        transformation_label = Text(
            "Linear Transformation", font_size=28, color=COLOR_LABEL_TEXT
        )
        transformation_label.move_to(UP * 3.2)

        # --- Animation sequence ---

        # Fade in the background grid
        self.play(FadeIn(original_grid))
        self.play(Write(original_label))
        self.wait(0.5)

        # Grow the input arrow from its tail
        self.play(GrowFromCenter(input_arrow))
        self.play(FadeIn(input_label))
        self.wait(0.5)

        # Show the transformation label
        self.play(Write(transformation_label))
        self.wait(0.5)

        # Animate the transformation: morph original grid
        # Stretch horizontally (dim=0), move to right side position
        self.play(
            original_grid.animate.stretch(1.4, dim=0).move_to(RIGHT * 3.5),
            input_arrow.animate.stretch(1.4, dim=0).move_to(RIGHT * 3.5 + UP * 0.5),
            run_time=2.5,
        )
        self.wait(0.5)

        # Show the transformed labels
        self.play(
            Transform(original_label, transformed_label),
            FadeIn(output_label),
            run_time=1.0,
        )
        self.wait(0.5)

        # Highlight the arrows to show input/output journey
        self.play(
            Indicate(input_arrow, scale_factor=1.2),
            Indicate(output_arrow, scale_factor=1.2),
            run_time=1.0,
        )
        self.wait(1.0)
        # --- Scene 2: Eigenvectors Stay on Their Span ---
        self.clear()
        # 1. Setup background
        self.camera.background_color = "#181825"

        # 2. Objects
        # Shared coordinate grid
        grid = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-5, 5, 1],
            x_length=12,
            y_length=8,
            background_line_style={
                "stroke_color": "#565F89",
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            axis_config={
                "stroke_color": "#A6ADC8",
                "stroke_width": 2,
            },
        )

        # Dashed span line for the eigenvector
        span_line = DashedLine(
            start=[-6, -1, 0],
            end=[6, -1, 0],
            dash_length=0.15,
            color="#C0CAF5",
            stroke_width=2,
        )

        # Normal arrows that will rotate during the stretch
        normal_arrow_1 = Arrow(
            start=[0, 0, 0],
            end=[1, -1, 0],
            buff=0,
            color="#7AA2F7",
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )
        normal_arrow_2 = Arrow(
            start=[0, 0, 0],
            end=[2, 1, 0],
            buff=0,
            color="#7AA2F7",
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )

        # Eigenvector arrow (points in the eigen direction)
        eigen_arrow_start = Arrow(
            start=[0, 0, 0],
            end=[-4, -1, 0],
            buff=0,
            color="#F7768E",
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15,
        )
        eigen_arrow_end = Arrow(
            start=[0, 0, 0],
            end=[6, -1, 0],
            buff=0,
            color="#F7768E",
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15,
        )

        # Top label
        label = Text(
            "Eigenvector: direction unchanged",
            font="Sans",
            font_size=26,
            color="#F7768E",
        ).move_to([0, 3.8, 0])

        # 3. Animations (~9.0s total)
        # Start with grid visible
        self.add(grid)
        self.wait(0.2)

        # Fade in span line and title
        self.play(
            FadeIn(span_line),
            Write(label),
            run_time=1.0,
        )
        self.wait(0.3)

        # Grow all arrows from the origin
        self.play(
            GrowFromCenter(normal_arrow_1),
            GrowFromCenter(normal_arrow_2),
            GrowFromCenter(eigen_arrow_start),
            run_time=1.0,
        )
        self.wait(0.5)

        # Horizontal stretch: normal arrows rotate, eigenvector scales on its line
        self.play(
            Rotate(normal_arrow_1, angle=PI / 6, about_point=ORIGIN, rate_func=smooth),
            Rotate(normal_arrow_2, angle=-PI / 8, about_point=ORIGIN, rate_func=smooth),
            Transform(eigen_arrow_start, eigen_arrow_end, rate_func=smooth),
            run_time=2.5,
        )
        self.wait(0.5)

        # Emphasize the eigenvector
        self.play(
            Indicate(eigen_arrow_start, color="#FCD4D4", scale_factor=1.15),
            run_time=0.8,
        )
        self.wait(0.2)

        # Final dwell
        self.wait(1.0)
        # --- Scene 3: Eigenvalues as Scaling Factors ---
        self.clear()

        # ── Scene Config ──────────────────────────────
        self.camera.background_color = "#181825"

        # ── Objects ───────────────────────────────────

        # Horizontal NumberLine centered on screen with tick marks
        number_line = NumberLine(
            x_range=[-3, 3, 0.5],
            length=12,
            stroke_width=2,
        )
        number_line.set_color("#C0CAF5")
        number_line.add_numbers()

        # Title
        title = Text(
            "Eigenvalue = Scaling Factor", font_size=28, color="#C0CAF5"
        ).to_edge(UP, buff=1.0)

        # Original unit arrow fixed on the line
        unit_arrow = Arrow(
            start=[-4, 0, 0],
            end=[-3, 0, 0],
            stroke_width=4,
            color="#C0CAF5",
            buff=0,
        )
        unit_label = MathTex("1", font_size=28, color="#C0CAF5")
        unit_label.next_to(unit_arrow, UP, buff=0.25)

        # Target arrow: λ = 2 (green, double length)
        scaled_arrow_2 = Arrow(
            start=[-4, 0, 0],
            end=[-2, 0, 0],
            stroke_width=4,
            color="#9ECE6A",
            buff=0,
        )
        lambda_label_2 = MathTex(r"\lambda = 2", font_size=32, color="#9ECE6A")
        lambda_label_2.next_to(scaled_arrow_2, UP, buff=0.3)

        # Target arrow: λ = -1 (red, flipped direction)
        scaled_arrow_neg1 = Arrow(
            start=[-4, 0, 0],
            end=[-5, 0, 0],
            stroke_width=4,
            color="#F7768E",
            buff=0,
        )
        lambda_label_neg1 = MathTex(r"\lambda = -1", font_size=32, color="#F7768E")
        lambda_label_neg1.next_to(scaled_arrow_neg1, UP, buff=0.3)

        # Floating scalar labels above the line
        label_scale = Text("Scale: +2", font_size=24, color="#A6E3A1")
        label_scale.to_edge(RIGHT, buff=1.5).shift(UP * 0.5)

        label_reflect = Text("Scale: -1", font_size=24, color="#F38BA8")
        label_reflect.next_to(label_scale, DOWN, buff=0.4)

        # ── Animations ────────────────────────────────
        # Timeline sums to exactly 8.0 seconds

        # 0.0–1.5s: Fade in infrastructure and original vector
        self.play(
            FadeIn(number_line),
            FadeIn(title),
            run_time=1.0,
        )
        self.play(
            FadeIn(unit_arrow),
            FadeIn(unit_label),
            run_time=0.5,
        )

        # 1.5–2.0s: Hold, let viewer absorb
        self.wait(0.5)

        # 2.0–2.5s: Show positive scalar label hint
        self.play(FadeIn(label_scale), run_time=0.5)

        # 2.5–4.5s: Stretch to λ = 2 and display label
        self.play(
            ReplacementTransform(unit_arrow, scaled_arrow_2),
            Transform(unit_label, lambda_label_2),
            run_time=2.0,
        )

        # 4.5–5.5s: Pause on the doubled vector
        self.wait(1.0)

        # 5.5–7.0s: Shrink through zero, flip to λ = -1, switch scalar labels
        self.play(
            ReplacementTransform(scaled_arrow_2, scaled_arrow_neg1),
            Transform(lambda_label_2, lambda_label_neg1),
            FadeOut(label_scale),
            FadeIn(label_reflect),
            run_time=1.5,
        )

        # 7.0–8.0s: Final hold, reinforce negative scaling
        self.wait(1.0)
        # --- Scene 4: The Eigenvector Equation ---
        # Scene 4: The Eigenvector Equation
        self.camera.background_color = "#181825"

        # Color palette
        purple = "#BB9AF7"
        pink = "#F7768E"
        teal = "#2AC3DE"
        text_color = "#C0CAF5"

        # --- 1. Objects ---

        # Title
        title = Text("The Defining Equation", font_size=28, color=text_color)
        title.move_to([0, 3, 0])

        # Matrix A (2x2)
        matrix_A = Matrix([[2, 1], [0, 3]], h_buff=0.8)
        matrix_A.set_color(purple)
        matrix_A.move_to([-4, 0.25, 0])

        # Vector v (left side)
        vector_v_left = Matrix([["x"], ["y"]])
        vector_v_left.set_color(pink)
        vector_v_left.move_to([-2, 0, 0])

        # Multiplication dot (between A and v)
        dot_left = MathTex(r"\cdot", font_size=52, color=text_color)
        dot_left.move_to([-3, 0, 0])

        # Equals sign
        equals_sign = MathTex("=", font_size=52, color=text_color)
        equals_sign.move_to([0, 0, 0])

        # Lambda scalar
        lambda_scalar = MathTex(r"\lambda", font_size=40, color=teal)
        lambda_scalar.move_to([1.5, 0.5, 0])

        # Multiplication dot (between lambda and v)
        dot_right = MathTex(r"\cdot", font_size=52, color=text_color)
        dot_right.move_to([1.5, -0.5, 0])

        # Vector v (right side)
        vector_v_right = Matrix([["x"], ["y"]])
        vector_v_right.set_color(pink)
        vector_v_right.move_to([2.5, 0, 0])

        # Prepare brace over the full equation row
        full_eq_row = VGroup(
            matrix_A,
            dot_left,
            vector_v_left,
            equals_sign,
            lambda_scalar,
            dot_right,
            vector_v_right,
        )
        equation_brace = Brace(full_eq_row, direction=DOWN, color=text_color)
        equation_brace_label = MathTex(
            r"Av = \lambda v", color=text_color, font_size=28
        )
        equation_brace_label.next_to(equation_brace, DOWN)

        # --- 2. Animations ---

        # Title appears
        self.play(FadeIn(title), run_time=0.5)

        # Build left side: matrix A, dot, vector v
        self.play(FadeIn(matrix_A), run_time=0.5)
        self.play(FadeIn(dot_left), run_time=0.3)
        self.play(FadeIn(vector_v_left), run_time=0.5)

        # Show equals sign
        self.play(FadeIn(equals_sign), run_time=0.5)

        # Build right side: lambda, dot, vector v
        self.play(FadeIn(lambda_scalar), run_time=0.5)
        self.play(FadeIn(dot_right), run_time=0.3)
        self.play(FadeIn(vector_v_right), run_time=0.5)

        # Brief pause to let the audience absorb
        self.wait(1.0)

        # Align all elements on a shared baseline (y = 0)
        self.play(
            matrix_A.animate.move_to([-4, 0, 0]),
            dot_left.animate.move_to([-3, 0, 0]),
            vector_v_left.animate.move_to([-2, 0, 0]),
            equals_sign.animate.move_to([0, 0, 0]),
            lambda_scalar.animate.move_to([1.25, 0, 0]),
            dot_right.animate.move_to([1.75, 0, 0]),
            vector_v_right.animate.move_to([2.75, 0, 0]),
            run_time=1.5,
        )

        # Add brace and label underneath
        self.play(FadeIn(equation_brace), FadeIn(equation_brace_label), run_time=0.9)

        # Hold final frame
        self.wait(2.0)
        # --- Scene 5: Natural Axes of Transformation ---
        self.clear()
        self.camera.background_color = "#181825"

        # Colors
        BLUE_SOFT = "#7AA2F7"
        PURPLE_SOFT = "#BB9AF7"
        TEAL = "#2AC3DE"
        TEXT_COLOR = "#C0CAF5"

        # Title
        title_text = Text(
            "Natural Axes of the Transformation", font_size=28, color=TEXT_COLOR
        )
        title_text.move_to([0, 3.5, 0])

        # Unit circle (input)
        unit_circle = Circle(radius=2, color=BLUE_SOFT, stroke_width=3)
        unit_circle.move_to(ORIGIN)

        # Transformed ellipse (output)
        transformed_ellipse = Ellipse(
            width=5, height=2.5, color=PURPLE_SOFT, stroke_width=3
        )
        transformed_ellipse.move_to(ORIGIN)

        # Eigenvector arrows (natural axes) — these ONLY SCALE
        major_axis_arrow = Arrow(
            start=[-2.5, 0, 0], end=[2.5, 0, 0], color=TEAL, stroke_width=4, buff=0
        )
        minor_axis_arrow = Arrow(
            start=[0, -1.25, 0], end=[0, 1.25, 0], color=TEAL, stroke_width=4, buff=0
        )

        # Lambda labels for eigenvalues
        label_lambda1 = MathTex(r"\lambda_1", font_size=28, color=TEAL)
        label_lambda1.move_to([3, 0.5, 0])
        label_lambda2 = MathTex(r"\lambda_2", font_size=28, color=TEAL)
        label_lambda2.move_to([0.8, 1.5, 0])

        # Non-eigenvector arrows (show ROTATION) — these change direction
        input_vec1 = Arrow(
            start=[0, 0, 0],
            end=[1.41, 1.41, 0],
            color=BLUE_SOFT,
            stroke_width=2,
            buff=0,
        )
        output_vec1 = Arrow(
            start=[0, 0, 0], end=[2.5, 1.0, 0], color=BLUE_SOFT, stroke_width=2, buff=0
        )

        input_vec2 = Arrow(
            start=[0, 0, 0], end=[-1, 1.73, 0], color=BLUE_SOFT, stroke_width=2, buff=0
        )
        output_vec2 = Arrow(
            start=[0, 0, 0], end=[-2.2, 1.5, 0], color=BLUE_SOFT, stroke_width=2, buff=0
        )

        # === Animation Sequence (Total: 9.0s) ===

        # 0.0 - 0.5s: Title fades in
        self.play(FadeIn(title_text), run_time=0.5)

        # 0.5 - 1.5s: Circle appears
        self.play(Create(unit_circle), run_time=1.0)

        # 1.5 - 3.0s: Circle morphs into ellipse
        self.play(Transform(unit_circle, transformed_ellipse), run_time=1.5)

        # 3.0 - 3.8s: Eigenvector axes appear (natural axes — only scaling happens here!)
        self.play(
            GrowFromCenter(major_axis_arrow),
            GrowFromCenter(minor_axis_arrow),
            run_time=0.8,
        )

        # 3.8 - 4.5s: Eigenvalue labels appear
        self.play(Write(label_lambda1), Write(label_lambda2), run_time=0.7)

        # 4.5 - 5.5s: First non-eigenvector transforms (visibly rotates)
        self.play(FadeIn(input_vec1), run_time=0.5)
        self.play(Transform(input_vec1, output_vec1), run_time=1.0)

        # 5.5 - 6.5s: Second non-eigenvector transforms (visibly rotates)
        self.play(FadeIn(input_vec2), run_time=0.5)
        self.play(Transform(input_vec2, output_vec2), run_time=1.0)

        # 6.5 - 7.1s: Emphasize eigenvectors (flash teal to white and back)
        self.play(
            major_axis_arrow.animate.set_color(WHITE),
            minor_axis_arrow.animate.set_color(WHITE),
            run_time=0.3,
        )
        self.play(
            major_axis_arrow.animate.set_color(TEAL),
            minor_axis_arrow.animate.set_color(TEAL),
            run_time=0.3,
        )

        # 7.1 - 9.0s: Hold final composition
        self.wait(1.9)
        # --- Scene 6: Characteristic Equation ---
        self.clear()
        self.camera.background_color = "#181825"

        # --- Title ---
        title = Text("Characteristic Equation", font_size=28, color="#C0CAF5")
        title.move_to([0, 3.2, 0])

        # --- Characteristic Matrix (A - λI) ---
        char_matrix = Matrix(
            [[r"2-\lambda", r"1"], [r"0", r"3-\lambda"]], h_buff=1.2, v_buff=0.8
        )
        char_matrix.move_to([0, 1, 0])
        char_matrix.set_color("#BB9AF7")

        # --- Determinant bars ---
        det_bars_left = Line(
            start=[-1.8, -0.5, 0], end=[-1.8, 2.5, 0], color="#C0CAF5", stroke_width=3
        )
        det_bars_right = Line(
            start=[1.8, -0.5, 0], end=[1.8, 2.5, 0], color="#C0CAF5", stroke_width=3
        )

        # --- Expanded determinant equation ---
        equation_line = MathTex(r"(2-\lambda)(3-\lambda) = 0", font_size=34)
        equation_line.move_to([0, -0.8, 0])
        equation_line.set_color("#C0CAF5")

        # --- Root icons (eigenvalues) ---
        root_icon_1 = MathTex(r"\lambda = 2", font_size=30)
        root_icon_1.move_to([-1.5, -2, 0])
        root_icon_1.set_color("#E0AF68")

        root_icon_2 = MathTex(r"\lambda = 3", font_size=30)
        root_icon_2.move_to([0.5, -2, 0])
        root_icon_2.set_color("#E0AF68")

        # === ANIMATIONS ===
        # 1. Title fades in
        self.play(FadeIn(title), run_time=1.0)

        # 2. Matrix draws itself
        self.play(Create(char_matrix), run_time=1.5)

        # 3. Determinant bars paint vertically
        self.play(Create(det_bars_left), Create(det_bars_right), run_time=1.0)

        # 4. Equation expands below
        self.play(Write(equation_line), run_time=1.5)

        # 5. Roots pop into view from the equation
        self.play(
            FadeIn(root_icon_1, shift=UP * 0.3),
            FadeIn(root_icon_2, shift=UP * 0.3),
            run_time=1.0,
        )

        # 6. Roots drift upward (visual metaphor for solutions being extracted)
        self.play(
            root_icon_1.animate.shift(UP * 1.5).set_opacity(0.6),
            root_icon_2.animate.shift(UP * 1.5).set_opacity(0.6),
            run_time=2.0,
            rate_func=rate_functions.ease_out_sine,
        )

        # Final hold
        self.wait(1.0)
        # --- Scene 7: Null Space Yields Eigenvectors ---
        self.camera.background_color = "#181825"

        # Title at top
        title = Text(
            "Finding Eigenvectors from Eigenvalues", font_size=28, color="#C0CAF5"
        )
        title.move_to([0, 3.2, 0])

        # Matrix A - lambda I (substituted with a specific eigenvalue)
        substituted_matrix = Matrix([["0", "1"], ["0", "1"]], h_buff=0.8, v_buff=0.8)
        substituted_matrix.set_color("#BB9AF7")
        substituted_matrix.move_to([-4, 1.5, 0])

        # Eigenvector v
        null_vector = Matrix([["x"], ["y"]], h_buff=0.8, v_buff=0.8)
        null_vector.set_color("#F7768E")
        null_vector.move_to([-2.5, 1.5, 0])

        # = 0
        equals_zero = MathTex("= 0", font_size=36, color="#C0CAF5")
        equals_zero.move_to([-1, 1.5, 0])

        # Display matrix equation first
        self.play(FadeIn(title, shift=UP), run_time=0.5)
        self.play(
            Write(substituted_matrix),
            Write(null_vector),
            Write(equals_zero),
            run_time=1.5,
        )
        self.wait(0.5)

        # Eigenspace dashed line (directed dashed line through origin extending both directions)
        eigenspace_dashed = DashedLine(
            start=[-4, -1.5, 0],
            end=[4, 1.5, 0],
            stroke_width=3,
            color="#9ECE6A",
            dash_length=0.2,
        )

        # Example arrows on the line (representing eigenvectors)
        example_arrow_1 = Arrow(
            start=[-2, -0.75, 0],
            end=[2, 0.75, 0],
            stroke_width=2,
            buff=0.1,
            color="#9ECE6A",
        )

        example_arrow_2 = Arrow(
            start=[3, 1.125, 0],
            end=[-3, -1.125, 0],
            stroke_width=2,
            buff=0.1,
            color="#9ECE6A",
        )

        # Animate the matrix equation collapsing into the line
        self.play(
            FadeOut(substituted_matrix, shift=DOWN, scale=0.5),
            FadeOut(null_vector, shift=DOWN, scale=0.5),
            FadeOut(equals_zero, shift=DOWN, scale=0.5),
            Create(eigenspace_dashed),
            run_time=1.5,
        )

        # Bring in arrows to show eigenvectors traveling along the line
        self.play(
            GrowFromCenter(example_arrow_1),
            GrowFromCenter(example_arrow_2),
            run_time=1.0,
        )

        # Animate arrows traveling to show scalar multiples
        self.play(
            example_arrow_1.animate.scale(1.5),
            example_arrow_2.animate.scale(0.7),
            run_time=1.5,
        )

        self.play(
            example_arrow_1.animate.scale(0.67),
            example_arrow_2.animate.scale(1.43),
            run_time=1.0,
        )

        # Label
        null_space_label = Text(
            "Eigenspace = Null Space(A - λI)", font_size=24, color="#9ECE6A"
        )
        null_space_label.move_to([0, -2.2, 0])

        # Pass flash along the line to reinforce the eigenspace concept
        self.play(
            FadeIn(null_space_label, shift=UP),
            ShowPassingFlash(
                eigenspace_dashed.copy().set_stroke(width=8, opacity=0.8),
                time_width=0.5,
            ),
            run_time=1.0,
        )

        self.wait(0.5)
        # --- Scene 8: Decoupling and Diagonalization ---
        self.camera.background_color = "#181825"

        # === ORIGIN DOT ===
        origin_dot = Dot(point=ORIGIN, radius=0.1, color="#C0CAF5")

        # === 3 AXES (3D-style on 2D canvas) ===
        x_axis = Arrow(start=[-3, 0, 0], end=[3, 0, 0], stroke_width=3, color="#F7768E")
        y_axis = Arrow(start=[0, -3, 0], end=[0, 3, 0], stroke_width=3, color="#9ECE6A")
        z_axis = Arrow(
            start=[-1.5, -1.5, 0], end=[1.5, 1.5, 0], stroke_width=3, color="#2AC3DE"
        )

        # === AXIS LABELS ===
        lambda_1_label = MathTex(r"\lambda_1", font_size=26, color="#F7768E")
        lambda_1_label.move_to([3.3, 0, 0])

        lambda_2_label = MathTex(r"\lambda_2", font_size=26, color="#9ECE6A")
        lambda_2_label.move_to([0, 3.3, 0])

        lambda_3_label = MathTex(r"\lambda_3", font_size=26, color="#2AC3DE")
        lambda_3_label.move_to([1.8, 1.8, 0])

        # === TEXT ===
        decouple_text = Text(
            "Decoupled: each axis scales independently", font_size=24, color="#C0CAF5"
        )
        decouple_text.move_to([0, -3.5, 0])

        title_text = Text(
            "Diagonalization: Working in Eigen-basis", font_size=28, color="#C0CAF5"
        )
        title_text.move_to([0, 3.5, 0])

        # === SCALING BAR MARKERS ===
        # Tick-like marks along each axis to show independent scaling
        def make_bar(pos, axis_dir, color_hex, width=0.2):
            perp = np.array([-axis_dir[1], axis_dir[0], 0]) * width
            return Line(pos + perp, pos - perp, color=color_hex, stroke_width=2)

        x_bars = VGroup(
            *[make_bar([x, 0, 0], [1, 0, 0], "#F7768E", 0.15) for x in [-2, -1, 1, 2]]
        )

        y_bars = VGroup(
            *[make_bar([0, y, 0], [0, 1, 0], "#9ECE6A", 0.15) for y in [-2, -1, 1, 2]]
        )

        z_bars = VGroup(
            *[
                make_bar([p, p, 0], [1, 1, 0], "#2AC3DE", 0.12)
                for p in [-1, -0.5, 0.5, 1]
            ]
        )

        # === ANIMATION SEQUENCE ===

        # Phase 1: Origin dot and title appear (0.5s)
        self.play(FadeIn(origin_dot), FadeIn(title_text), run_time=0.5)

        # Phase 2: Axes and labels draw in (1.5s)
        self.play(
            Create(x_axis),
            Create(y_axis),
            Create(z_axis),
            FadeIn(lambda_1_label),
            FadeIn(lambda_2_label),
            FadeIn(lambda_3_label),
            run_time=1.5,
        )

        # Phase 3: Scaling bars appear showing independent scaling (1.5s)
        self.play(Create(x_bars), Create(y_bars), Create(z_bars), run_time=1.5)

        self.wait(0.5)

        # Phase 4: Rotate to emphasize orthogonality and decoupling (4.0s total)
        axes_group = VGroup(x_axis, y_axis, z_axis)
        labels_group = VGroup(lambda_1_label, lambda_2_label, lambda_3_label)
        bars_group = VGroup(x_bars, y_bars, z_bars)

        self.play(
            axes_group.animate.rotate(PI / 8),
            labels_group.animate.rotate(PI / 8),
            bars_group.animate.rotate(PI / 8),
            run_time=1.5,
        )

        self.play(
            axes_group.animate.rotate(-PI / 4),
            labels_group.animate.rotate(-PI / 4),
            bars_group.animate.rotate(-PI / 4),
            run_time=1.5,
        )

        self.play(
            axes_group.animate.rotate(PI / 8),
            labels_group.animate.rotate(PI / 8),
            bars_group.animate.rotate(PI / 8),
            run_time=1.0,
        )

        # Phase 5: Decoupled text appears (1.0s)
        self.play(FadeIn(decouple_text), run_time=1.0)

        # Final hold (1.0s)
        self.wait(1.0)
