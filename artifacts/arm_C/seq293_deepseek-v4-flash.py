import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: What is a Vector? ---
        self.clear()
        self.camera.background_color = "#1E1E2E"
        vec_end = np.array([3, 2, 0])
        angle_val = np.arctan2(2, 3)
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            axis_config={
                "color": "#585B70",
                "stroke_width": 1.5,
                "include_numbers": True,
                "numbers_to_exclude": [0],
            },
            background_line_style={
                "stroke_color": "#313244",
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
        )
        for num in grid.get_x_axis().numbers:
            num.set_color("#585B70").scale(0.6)
        for num in grid.get_y_axis().numbers:
            num.set_color("#585B70").scale(0.6)
        vector_arrow = Arrow(
            start=ORIGIN,
            end=vec_end,
            tip_length=0.25,
            color="#89B4FA",
            stroke_width=5,
        )
        vector_label = MathTex(
            r"\vec{v} = (3, 2)",
            color="#89B4FA",
            font_size=38,
        ).next_to(vec_end, RIGHT + UP, buff=0.2)
        magnitude_brace = BraceBetweenPoints(
            ORIGIN,
            vec_end,
            color="#A6E3A1",
        )
        magnitude_text = magnitude_brace.get_text("Magnitude")
        magnitude_text.set_color("#A6E3A1").scale(0.9)
        angle_arc = Arc(
            radius=0.6,
            start_angle=0,
            angle=angle_val,
            color="#FAB387",
            stroke_width=3,
        )
        arc_mid_angle = angle_val / 2
        label_pos = np.array(
            [1.1 * np.cos(arc_mid_angle), 1.1 * np.sin(arc_mid_angle), 0]
        )
        direction_label = MathTex(
            r"	ext{Direction}",
            color="#FAB387",
            font_size=30,
        ).move_to(label_pos)
        origin_dot = Dot(ORIGIN, color="#CDD6F4", radius=0.06)
        self.add(grid, origin_dot)
        self.wait(0.3)
        self.play(Create(vector_arrow), run_time=1.2)
        self.play(Write(vector_label), run_time=0.8)
        self.play(GrowFromCenter(magnitude_brace), Write(magnitude_text), run_time=1.0)
        self.play(Create(angle_arc), Write(direction_label), run_time=1.0)
        self.play(
            Indicate(magnitude_brace, color="#A6E3A1", scale_factor=1.06),
            Indicate(angle_arc, color="#FAB387", scale_factor=1.06),
            run_time=1.2,
        )
        self.wait(1.0)
        # --- Scene 2: What is a Matrix? ---
        # === Scene 2: What is a Matrix? ===
        # Narration: "A matrix is a rectangular array of numbers that, when applied to a vector,
        # transforms it — stretching, rotating, or flipping it in space."

        self.camera.background_color = "#1E1E2E"

        # ---- PHASE 1: Matrix on left ----
        entries = [
            [MathTex("a", color="#89B4FA"), MathTex("b", color="#FAB387")],
            [MathTex("c", color="#A6E3A1"), MathTex("d", color="#F38BA8")],
        ]
        matrix = Matrix(entries)
        matrix.get_brackets()[0].set_color("#CBA6F7")
        matrix.get_brackets()[1].set_color("#CBA6F7")
        matrix.scale(1.2)
        matrix.shift(LEFT * 4)

        a_label = MathTex("A =", font_size=48, color="#A6ADC8")
        a_label.next_to(matrix, LEFT, buff=0.3)

        matrix_group = VGroup(a_label, matrix)

        title = Text("What is a Matrix?", font_size=36, color="#CDD6F4")
        title.to_edge(UP, buff=0.5)

        self.play(Write(title), run_time=0.6)
        self.play(Create(matrix_group), run_time=1.0)
        self.wait(0.2)

        # ---- PHASE 2: Input vector ----
        input_vec = Arrow(
            start=LEFT * 4 + DOWN * 1.5,
            end=LEFT * 4 + UP * 1.0 + RIGHT * 1.2,
            color="#89B4FA",
            stroke_width=8,
            tip_length=0.25,
        )
        input_label = MathTex("v", color="#89B4FA", font_size=36)
        input_label.next_to(input_vec, DOWN, buff=0.15)

        input_group = VGroup(input_vec, input_label)

        self.play(GrowFromCenter(input_vec), Write(input_label), run_time=1.0)
        self.wait(0.2)

        # ---- PHASE 3: Transformation arrow ----
        transform_arrow = Arrow(
            start=LEFT * 1.5,
            end=RIGHT * 1.5,
            color="#FAB387",
            stroke_width=6,
            tip_length=0.3,
        )
        arrow_label = Text("Transforms", font_size=28, color="#FAB387")
        arrow_label.next_to(transform_arrow, DOWN, buff=0.15)

        self.play(GrowFromCenter(transform_arrow), Write(arrow_label), run_time=0.8)
        self.wait(0.15)

        # ---- PHASE 4: Transformed grid on right ----
        ref_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            axis_config={"color": "#585B70", "stroke_width": 1, "stroke_opacity": 0.3},
        )
        ref_axes.shift(RIGHT * 3.5)

        b1 = Vector([2.0, 0.8], color="#89B4FA", stroke_width=8, tip_length=0.25)
        b1.shift(RIGHT * 3.5)

        b2 = Vector([0.6, 2.0], color="#F38BA8", stroke_width=8, tip_length=0.25)
        b2.shift(RIGHT * 3.5)

        transform_label = Text("Transformation", font_size=28, color="#A6E3A1")
        transform_label.next_to(RIGHT * 3.5 + DOWN * 2.8, ORIGIN, buff=0)

        grid_dots = VGroup()
        for x in range(-2, 3):
            for y in range(-2, 3):
                pt = (
                    RIGHT * 3.5
                    + (x * 0.4) * b1.get_vector()
                    + (y * 0.4) * b2.get_vector()
                )
                d = Dot(point=pt, radius=0.04, color="#585B70", fill_opacity=0.5)
                grid_dots.add(d)

        self.play(Create(ref_axes), run_time=0.5)
        self.play(
            GrowFromCenter(b1),
            GrowFromCenter(b2),
            FadeIn(grid_dots, lag_ratio=0.02),
            Write(transform_label),
            run_time=1.0,
        )
        self.wait(0.2)

        # ---- PHASE 5: Output vector ----
        output_vec = Vector(
            [1.2 * 2.0 + 2.5 * 0.6, 1.2 * 0.8 + 2.5 * 2.0],
            color="#F38BA8",
            stroke_width=8,
            tip_length=0.25,
        )
        output_vec.shift(RIGHT * 3.5)

        output_label = MathTex("Av", color="#F38BA8", font_size=36)
        output_label.next_to(output_vec, UP, buff=0.15)

        self.play(GrowFromCenter(output_vec), Write(output_label), run_time=0.8)
        self.wait(1.0)
        # --- Scene 3: Applying a Matrix to a Vector ---
        # Scene 3: Applying a Matrix to a Vector
        # Setup grid
        grid = NumberPlane(
            x_range=[-7, 7], y_range=[-4, 4], axis_config={"color": "#585B70"}
        )
        grid.set_color("#89B4FA")
        grid.set_opacity(0.6)

        # Matrix: [[0, -1], [1, 0]] (90-degree rotation)
        # Input: v = [3, 1]
        # Output: Av = [-1, 3]

        # Create input vector (blue)
        input_vec = Vector([3, 1], tip_length=0.25, stroke_width=6)
        input_vec.set_color("#89B4FA")
        input_label = MathTex("v", color="#89B4FA", font_size=36)
        input_label.next_to(input_vec.get_end(), UR, buff=0.15)

        # Create output vector (red/pink)
        output_vec = Vector([-1, 3], tip_length=0.25, stroke_width=6)
        output_vec.set_color("#F38BA8")
        output_label = MathTex("A \\cdot v", color="#F38BA8", font_size=36)
        output_label.next_to(output_vec.get_end(), UL, buff=0.15)

        # Matrix display as MathTex for cleaner look
        matrix_tex = MathTex(
            "\\begin{pmatrix} 0 & -1 \\\\ 1 & 0 \\end{pmatrix}",
            font_size=36,
            color="#A6E3A1",
        )
        matrix_tex.to_corner(UL)

        # Equation: A * v = Av
        eq_tex = MathTex(
            "\\begin{pmatrix} 0 & -1 \\\\ 1 & 0 \\end{pmatrix}",
            "\\begin{pmatrix} 3 \\\\ 1 \\end{pmatrix}",
            "=",
            "\\begin{pmatrix} -1 \\\\ 3 \\end{pmatrix}",
            font_size=30,
            color="#CDD6F4",
        )
        eq_tex.next_to(matrix_tex, DOWN, buff=0.8)

        # Transition label
        transition_label = Tex(
            "Before $\\rightarrow$ After", color="#FAB387", font_size=28
        )
        transition_label.to_edge(DOWN, buff=0.5)

        # Total timing: exactly 7.0 seconds
        # 0.5 + 0.2 = 0.7
        self.play(Create(grid, lag_ratio=0), run_time=0.5)
        self.wait(0.2)

        # Show input vector with grow animation (0.6 + 0.2 = 0.8, 1.5 total)
        self.play(GrowArrow(input_vec), Write(input_label), run_time=0.6)
        self.wait(0.2)

        # Show matrix (0.5 + 0.2 = 0.7, 2.2 total)
        self.play(Write(matrix_tex), run_time=0.5)
        self.wait(0.2)

        # Show equation (0.7 + 0.3 = 1.0, 3.2 total)
        self.play(Write(eq_tex), run_time=0.7)
        self.wait(0.3)

        # Fade input, grow output (0.9 + 0.3 = 1.2, 4.4 total)
        self.play(
            input_vec.animate.set_opacity(0.3),
            input_label.animate.set_opacity(0.3),
            GrowArrow(output_vec),
            Write(output_label),
            run_time=0.9,
        )
        self.wait(0.3)

        # Highlight output (0.5 + 0.2 = 0.7, 5.1 total)
        self.play(
            output_vec.animate.set_stroke_width(9),
            output_label.animate.scale(1.25),
            run_time=0.5,
        )
        self.wait(0.2)

        # Show transition label (0.5 + 0.2 = 0.7, 5.8 total)
        self.play(Write(transition_label), run_time=0.5)
        self.wait(0.2)

        # Final circumscribe flash (1.0 + 0.2 = 1.2, 7.0 total)
        self.play(Circumscribe(output_vec, color="#F38BA8", buff=0.15), run_time=1.0)
        self.wait(0.2)
        # --- Scene 4: Special Vectors That Don't Change Direction ---
        self.clear()

        # ---- Color Palette ----
        plane_color = "#585B70"
        line_color = "#A6ADC8"
        vec_color = "#89B4FA"
        trans_vec_color = "#F38BA8"
        check_color = "#A6E3A1"
        label_color = "#CBA6F7"

        # 1. Create NumberPlane grid
        grid = NumberPlane(
            x_range=[-7, 7], y_range=[-4, 4], axis_config={"color": plane_color}
        )

        # 2. Create diagonal dashed line through origin (slope = 1)
        eigen_line = DashedLine(
            start=grid.c2p(-3.5, -3.5),
            end=grid.c2p(3.5, 3.5),
            color=line_color,
            stroke_width=2,
            dash_length=0.15,
        )

        # 3. Original eigenvector: a blue arrow along the diagonal
        original_vec = Vector([1.5, 1.5, 0], color=vec_color, tip_length=0.25)

        # Label for original eigenvector
        v_label = MathTex("v", color=vec_color, font_size=36)
        v_label.next_to(original_vec.get_end(), UP + RIGHT, buff=0.15)

        # 4. Transformed eigenvector: a longer red arrow along the same line
        trans_vec = Vector([2.8, 2.8, 0], color=trans_vec_color, tip_length=0.25)

        # Label for transformed eigenvector - A·v = λv
        av_label = MathTex(
            r"A \cdot v = \lambda v", color=trans_vec_color, font_size=28
        )
        av_label.next_to(trans_vec.get_end(), UP + RIGHT, buff=0.15)

        # 5. Checkmark label
        check_label = Tex(
            r"\checkmark 	ext{ Direction unchanged!}",
            color=check_color,
            font_size=28,
        )
        check_label.move_to(RIGHT * 3 + DOWN * 2.5)

        # 6. Title label
        eigen_label = Tex("Eigenvector", color=label_color, font_size=26)
        eigen_label.to_edge(UP, buff=0.5)

        # ---- Animations ----
        # Phase 1 (2.5s): Fade in grid + dashed line
        self.play(FadeIn(grid, run_time=1.0))
        self.play(Create(eigen_line, run_time=1.0))
        self.wait(0.5)

        # Phase 2 (1.5s): Show original eigenvector
        self.play(Create(original_vec, run_time=0.8))
        self.play(Write(v_label, run_time=0.5))
        self.wait(0.2)

        # Phase 3 (1.5s): Show transformed eigenvector
        self.play(Create(trans_vec, run_time=0.8))
        self.play(Write(av_label, run_time=0.5))
        self.wait(0.2)

        # Phase 4 (1.5s): Show checkmark and label
        self.play(Write(check_label, run_time=0.7))
        self.play(Write(eigen_label, run_time=0.6))
        self.wait(0.2)

        # Phase 5 (0.5s): Final hold
        self.wait(0.5)
        # --- Scene 5: The Eigenvalue: Stretch Factor ---
        self.clear()
        # Set background color
        self.camera.background_color = "#1E1E2E"

        # --- Title ---
        title = Tex("Eigenvalue ($\\lambda$)", font_size=28, color="#CDD6F4")
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # --- NumberLine along the eigenvector direction ---
        number_line = NumberLine(
            x_range=[0, 6, 1],
            length=10,
            include_numbers=True,
            include_ticks=True,
            color="#585B70",
            font_size=24,
            numbers_to_include=list(range(0, 7)),
            decimal_number_config={"num_decimal_places": 0},
        ).shift(DOWN * 0.5)
        for num in number_line.numbers:
            num.set_color("#A6ADC8")

        # --- Original segment: from 0 to 2 (blue) ---
        orig_start = number_line.n2p(0)
        orig_end = number_line.n2p(2)
        original_segment = Line(orig_start, orig_end, color="#89B4FA", stroke_width=8)

        # --- Stretched segment: from 0 to 4 (red) ---
        stretch_end = number_line.n2p(4)
        stretched_segment = Line(
            orig_start, stretch_end, color="#F38BA8", stroke_width=8
        )

        # --- Labels for segments ---
        orig_label = Text("Original", font_size=20, color="#89B4FA")
        orig_label.next_to(original_segment, DOWN, buff=0.15)

        stretch_label = Text("Stretched", font_size=20, color="#F38BA8")
        stretch_label.next_to(stretched_segment, DOWN, buff=0.15)

        # --- Brace between 2 and 4 (showing stretch factor) ---
        point_2 = number_line.n2p(2)
        point_4 = number_line.n2p(4)
        stretch_brace = BraceBetweenPoints(point_2, point_4, direction=UP)
        stretch_brace.set_color("#A6E3A1")

        # --- Eigenvalue label above brace ---
        eigenvalue_label = Tex("$\\lambda = 2$", font_size=36, color="#FAB387")
        eigenvalue_label.next_to(stretch_brace, UP, buff=0.1)

        # --- Scale ruler (visual representation) ---
        ruler_ticks = VGroup()
        ruler_positions = [0, 1, 2, 3, 4, 5, 6]
        for pos in ruler_positions:
            p = number_line.n2p(pos)
            tick = Line(p + DOWN * 0.1, p + DOWN * 0.3, color="#585B70", stroke_width=2)
            ruler_ticks.add(tick)

        ruler_label = Tex("Scale", font_size=18, color="#A6ADC8")
        ruler_label.next_to(ruler_ticks, DOWN, buff=0.05)

        # --- Build animation sequence (6.5s total) ---

        # 1. Fade in title and number line (0.8s)
        self.play(
            FadeIn(title, shift=UP * 0.3),
            Create(number_line, run_time=0.6),
            run_time=0.8,
        )

        # 2. Show original segment (0.8s)
        self.play(Create(original_segment), Write(orig_label), run_time=0.8)

        # 3. Brief pause then indicate the original (1.0s)
        self.wait(0.3)
        self.play(
            Indicate(original_segment, color="#89B4FA", scale_factor=1.05), run_time=0.7
        )

        # 4. Show stretched segment growing (1.2s)
        self.play(GrowFromCenter(stretched_segment), Write(stretch_label), run_time=1.0)
        self.wait(0.2)

        # 5. Show brace and eigenvalue label (1.2s)
        self.play(Create(stretch_brace), Write(eigenvalue_label), run_time=1.0)
        self.wait(0.2)

        # 6. Show scale ruler (0.8s)
        self.play(
            *[Create(tick) for tick in ruler_ticks],
            FadeIn(ruler_label, shift=DOWN * 0.2),
            run_time=0.8,
        )

        # 7. Final pause (0.7s to reach exactly 6.5s)
        self.wait(0.7)
        # --- Scene 6: The Defining Equation: A v = λ v ---
        self.clear()

        # Background color
        self.camera.background_color = "#1E1E2E"

        # 1. Faint grid background
        grid = NumberPlane(
            x_range=[-7, 7],
            y_range=[-4, 4],
            axis_config={"color": "#313244"},
            background_line_style={
                "stroke_color": "#A6ADC8",
                "stroke_width": 1,
                "stroke_opacity": 0.12,
            },
        )
        self.add(grid)

        # 2. Title
        title = Tex("The Defining Equation", font_size=32, color="#CDD6F4")
        title.to_edge(UP, buff=0.5)

        # 3. Main equation: A v = lambda v
        equation = MathTex(
            r"A \vec{v} = \lambda \vec{v}",
            font_size=56,
            color="#CDD6F4",
            substrings_to_isolate=["A", r"\vec{v}", r"\lambda"],
        )
        equation.move_to(ORIGIN)

        # Color the individual components
        equation.set_color_by_tex("A", "#CBA6F7")
        equation.set_color_by_tex(r"\lambda", "#FAB387")
        equation.set_color_by_tex(r"\vec{v}", "#89B4FA")

        # 4. Labels underneath each symbol
        a_part = equation.get_part_by_tex("A")
        lambda_part = equation.get_part_by_tex(r"\lambda")
        v_part = equation.get_part_by_tex(r"\vec{v}")

        matrix_label = Tex("Matrix", font_size=28, color="#CBA6F7")
        scalar_label = Tex("Scalar", font_size=28, color="#FAB387")
        eigenvector_label = Tex("Eigenvector", font_size=28, color="#89B4FA")

        matrix_label.next_to(a_part, DOWN, buff=0.35)
        scalar_label.next_to(lambda_part, DOWN, buff=0.35)
        eigenvector_label.next_to(v_part, DOWN, buff=0.35)

        # 5. Subtle glow effect around the equation
        glow_bg = BackgroundRectangle(
            equation,
            color="#CBA6F7",
            fill_opacity=0.06,
            buff=0.3,
        )
        glow_bg.set_stroke(opacity=0.0)

        # Animation sequence (~7.0 seconds total)
        self.play(FadeIn(grid, run_time=0.4))
        self.play(Write(title, run_time=0.5))
        self.play(
            FadeIn(glow_bg, run_time=0.3),
            Write(equation, run_time=0.7),
        )
        self.wait(0.3)
        self.play(GrowFromCenter(matrix_label), run_time=0.4)
        self.wait(0.2)
        self.play(GrowFromCenter(scalar_label), run_time=0.4)
        self.wait(0.2)
        self.play(GrowFromCenter(eigenvector_label), run_time=0.4)
        self.play(
            Indicate(equation, color="#CBA6F7", scale_factor=1.02),
            run_time=0.8,
        )
        self.wait(1.0)

        # Fill remaining time to match 7.0 seconds exactly
        elapsed = 0.4 + 0.5 + 0.7 + 0.3 + 0.4 + 0.2 + 0.4 + 0.2 + 0.4 + 0.8 + 1.0
        remaining = 7.0 - elapsed
        if remaining > 0:
            self.wait(remaining)
        # --- Scene 7: Finding Eigenvectors: Solving (A - λI)v = 0 ---
        self.clear()
        self.camera.background_color = "#181825"

        # === Build Objects ===

        # 1. Left: Matrix A box (square)
        matrix_a_box = Square(side_length=0.8, stroke_width=2, color="#CBA6F7")
        matrix_a_box.move_to(LEFT * 4.5)
        label_a = MathTex("A", font_size=36, color="#CBA6F7")
        label_a.move_to(matrix_a_box.get_center())

        # 2. Middle: A - lambda*I rectangle
        subtracted_box = Rectangle(
            height=0.8, width=1.2, stroke_width=2, color="#FAB387"
        )
        subtracted_box.move_to(ORIGIN)
        label_a_minus = MathTex("A - \\lambda I", font_size=30, color="#FAB387")
        label_a_minus.move_to(subtracted_box.get_center())

        # 3. Right: Magnifying glass (circle + handle line)
        magnify_circle = Circle(radius=0.8, stroke_width=3, color="#A6E3A1")
        magnify_circle.move_to(RIGHT * 3.5)

        magnify_handle = Line(
            start=RIGHT * 3.5 + DOWN * 0.65,
            end=RIGHT * 3.5 + DOWN * 1.3,
            stroke_width=3,
            color="#A6E3A1",
        )

        # 4. Null space dot (inside magnifying glass)
        null_dot = Dot(point=RIGHT * 3.5 + UP * 0.2, radius=0.08, color="#F38BA8")
        null_dot_label = MathTex("v = 0", font_size=22, color="#F38BA8")
        null_dot_label.next_to(null_dot, RIGHT, buff=0.15)

        # 5. Null space text label below magnifying glass
        null_space_text = Text("Null Space", font_size=24, color="#A6ADC8")
        null_space_text.next_to(magnify_circle, DOWN, buff=0.8)

        # 6. Equation label at bottom
        equation = MathTex("(A - \\lambda I)v = 0", font_size=28, color="#89B4FA")
        equation.move_to(DOWN * 2.5)

        # 7. Arrows between boxes
        arrow_1 = Arrow(
            start=matrix_a_box.get_right() + RIGHT * 0.3,
            end=subtracted_box.get_left() + LEFT * 0.3,
            stroke_width=4,
            color="#CDD6F4",
        )
        arrow_2 = Arrow(
            start=subtracted_box.get_right() + RIGHT * 0.3,
            end=magnify_circle.get_left() + LEFT * 0.3,
            stroke_width=4,
            color="#CDD6F4",
        )

        # === Animate with total 8.0s ===

        # Phase 1: Show matrix A box (0.6s)
        self.play(Create(matrix_a_box), Write(label_a), run_time=0.6)
        self.wait(0.2)

        # Phase 2: Show arrow 1 and subtracted matrix (1.5s)
        self.play(Create(arrow_1), run_time=0.5)
        self.play(Create(subtracted_box), Write(label_a_minus), run_time=1.0)
        self.wait(0.2)

        # Phase 3: Show arrow 2 and magnifying glass (1.8s)
        self.play(Create(arrow_2), run_time=0.5)
        self.play(Create(magnify_circle), Create(magnify_handle), run_time=0.8)
        self.wait(0.3)

        # Phase 4: Show null space dot and label (1.5s)
        self.play(
            GrowFromCenter(null_dot),
            Write(null_dot_label),
            FadeIn(null_space_text, shift=UP * 0.3),
            run_time=1.5,
        )
        self.wait(0.3)

        # Phase 5: Show equation at bottom + final hold (2.1s)
        self.play(Write(equation), run_time=1.2)
        self.wait(0.9)

        # Total: 0.6 + 0.2 + 0.5 + 1.0 + 0.2 + 0.5 + 0.8 + 0.3 + 1.5 + 0.3 + 1.2 + 0.9 = 8.0s
        # --- Scene 8: The Characteristic Polynomial and Determinant ---
        self.clear()
        self.camera.background_color = "#181825"

        # 1. Create Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5,
            axis_config={"color": "#585B70"},
        )
        axes.center()

        # 2. Define the polynomial - a cubic with roots at -2, 0.5, 2.5
        def poly_func(x):
            return 0.3 * (x + 2.0) * (x - 0.5) * (x - 2.5)

        graph = axes.plot(
            poly_func,
            x_range=[-3.2, 3.2],
            color="#89B4FA",
            stroke_width=3.0,
        )

        # 3. Title
        title = MathTex(
            "\	ext{Characteristic Polynomial}", font_size=28, color="#FAB387"
        )
        title.to_edge(UP)

        # 4. Determinant formula - use MathTex for math mode
        det_formula = MathTex(r"\det(A - \lambda I) = 0", font_size=32, color="#CBA6F7")
        det_formula.next_to(title, DOWN, buff=0.3)

        # 5. Root markers at x-intercepts
        root_x_values = [-2.0, 0.5, 2.5]
        root_labels_text = [r"\lambda_1", r"\lambda_2", r"\lambda_3"]

        root_labels = VGroup()
        checkmarks = VGroup()
        root_dots = VGroup()

        for i, x_root in enumerate(root_x_values):
            # Dot at the x-intercept
            dot_point = axes.c2p(x_root, 0)
            dot = Dot(dot_point, color="#A6E3A1", radius=0.10)
            root_dots.add(dot)

            # Root label below the x-axis
            label_point = axes.c2p(x_root, -0.6)
            label = MathTex(root_labels_text[i], font_size=24, color="#A6E3A1")
            label.move_to(label_point)
            root_labels.add(label)

            # Checkmark above the root
            check_point = axes.c2p(x_root, 0.4)
            check = MathTex(r"\checkmark", font_size=28, color="#A6E3A1")
            check.move_to(check_point)
            checkmarks.add(check)

        # --- ANIMATION SEQUENCE ---

        # Step 1: Create axes (1.2s)
        self.play(Create(axes), run_time=1.2)

        # Step 2: Write title and formula simultaneously (0.8s)
        self.play(
            Write(title),
            Write(det_formula),
            run_time=0.8,
        )

        # Step 3: Draw the polynomial curve (1.5s)
        self.play(Create(graph), run_time=1.5)

        # Step 4: Show dots at intercepts (0.5s)
        self.play(
            *[GrowFromCenter(dot) for dot in root_dots],
            run_time=0.5,
        )

        # Step 5: Show each root label + checkmark pair sequentially (0.9s each)
        for i in range(3):
            self.play(
                Write(root_labels[i]),
                Write(checkmarks[i]),
                run_time=0.9,
            )

        # Step 6: Final pause (0.8s)
        self.wait(0.8)
        # --- Scene 9: Multiple Eigenvectors for the Same Eigenvalue ---
        self.camera.background_color = "#1E1E2E"

        # 1. NumberPlane with muted grid lines
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            x_length=14,
            y_length=8,
            background_line_style={
                "stroke_color": "#585B70",
                "stroke_width": 1,
                "stroke_opacity": 0.35,
            },
            axis_config={
                "color": "#585B70",
                "stroke_width": 1.5,
            },
        )
        self.add(grid)

        # 2. Diagonal line (eigenspace) through origin
        eigenspace_line = Line(
            start=grid.c2p(-5.5, -3.3),
            end=grid.c2p(5.5, 3.3),
            color="#CBA6F7",
            stroke_width=3,
        )
        eigenspace_line.set_opacity(0.5)

        # 3. Shaded region - polygon strip along the eigenspace line
        p1 = grid.c2p(-4.5, -2.7)
        p2 = grid.c2p(4.5, 2.7)
        # Perpendicular offset
        line_dir = np.array([1, 0.6, 0])
        line_dir = line_dir / np.linalg.norm(line_dir)
        perp = np.array([-line_dir[1], line_dir[0], 0]) * 0.35

        shaded_region = Polygon(
            p1 - perp,
            p2 - perp,
            p2 + perp,
            p1 + perp,
            color="#CBA6F7",
            fill_opacity=0.15,
            stroke_width=0,
        )

        # 4. Three vectors along the line (different lengths, same direction)
        origin_point = grid.c2p(0, 0)

        short_end = grid.c2p(1.5, 0.9)
        short_vec = Arrow(
            start=origin_point,
            end=short_end,
            color="#89B4FA",
            tip_length=0.2,
            stroke_width=5,
            buff=0,
        )

        med_end = grid.c2p(3.0, 1.8)
        medium_vec = Arrow(
            start=origin_point,
            end=med_end,
            color="#A6E3A1",
            tip_length=0.2,
            stroke_width=5,
            buff=0,
        )

        long_end = grid.c2p(4.5, 2.7)
        long_vec = Arrow(
            start=origin_point,
            end=long_end,
            color="#F38BA8",
            tip_length=0.2,
            stroke_width=5,
            buff=0,
        )

        # 5. Labels for vectors
        v1_label = MathTex("v_1", color="#89B4FA", font_size=28)
        v1_label.next_to(short_end, UP + RIGHT, buff=0.15)

        v2_label = MathTex("v_2", color="#A6E3A1", font_size=28)
        v2_label.next_to(med_end, UP + RIGHT, buff=0.15)

        v3_label = MathTex("v_3", color="#F38BA8", font_size=28)
        v3_label.next_to(long_end, UP + RIGHT, buff=0.15)

        # 6. Eigenspace label
        eigenspace_label = Tex("Eigenspace", color="#FAB387", font_size=28)
        eigenspace_label.move_to(grid.c2p(2.5, 3.3))

        # --- Animations (total = 6.5s) ---
        self.wait(0.3)

        self.play(Create(eigenspace_line), run_time=0.6)
        self.play(FadeIn(shaded_region, scale=0.8), run_time=0.5)

        self.play(Create(short_vec), run_time=0.6)
        self.play(Write(v1_label), run_time=0.4)

        self.play(Create(medium_vec), run_time=0.6)
        self.play(Write(v2_label), run_time=0.4)

        self.play(Create(long_vec), run_time=0.6)
        self.play(Write(v3_label), run_time=0.4)

        self.play(Write(eigenspace_label), run_time=0.6)

        self.play(
            Circumscribe(eigenspace_line, color="#CBA6F7", fade_out=True), run_time=0.5
        )

        self.wait(1.0)
        # --- Scene 10: Real-World Examples: Why Eigenvectors Matter ---
        self.clear()
        self.camera.background_color = "#1E1E2E"

        # ============================================
        # PANEL DIVIDERS
        # ============================================
        divider_1 = DashedLine(
            start=UP * 3.5 + LEFT * 2.5,
            end=DOWN * 3.5 + LEFT * 2.5,
            color="#585B70",
            stroke_width=1,
            dash_length=0.08,
        )
        divider_2 = DashedLine(
            start=UP * 3.5 + RIGHT * 2.5,
            end=DOWN * 3.5 + RIGHT * 2.5,
            color="#585B70",
            stroke_width=1,
            dash_length=0.08,
        )

        # ============================================
        # PANEL TITLES
        # ============================================
        physics_title = Text("Physics", font_size=26, color="#CDD6F4", font="Sans")
        physics_title.move_to(LEFT * 4 + UP * 3.2)

        data_title = Text("Data Science", font_size=26, color="#CDD6F4", font="Sans")
        data_title.move_to(ORIGIN + UP * 3.2)

        eng_title = Text("Engineering", font_size=26, color="#CDD6F4", font="Sans")
        eng_title.move_to(RIGHT * 4 + UP * 3.2)

        # ============================================
        # LEFT PANEL: Physics - Rotating Ellipsoid
        # ============================================
        ellipsoid = Ellipse(
            width=1.5,
            height=2.5,
            color="#89B4FA",
            fill_opacity=0.2,
            fill_color="#89B4FA",
            stroke_width=2,
        )
        ellipsoid.move_to(LEFT * 4)

        inner_ellipse = Ellipse(
            width=1.0,
            height=2.0,
            color="#89B4FA",
            fill_opacity=0.1,
            fill_color="#89B4FA",
            stroke_width=1,
            stroke_opacity=0.4,
        )
        inner_ellipse.move_to(LEFT * 4)

        axis_line = Line(
            start=LEFT * 4 + UP * 2.0,
            end=LEFT * 4 + DOWN * 2.0,
            color="#FAB387",
            stroke_width=3,
        )

        glow_dots = VGroup(
            *[
                Dot(
                    point=LEFT * 4 + UP * y,
                    radius=0.03,
                    color="#FAB387",
                    fill_opacity=0.4,
                )
                for y in np.arange(-1.8, 1.9, 0.3)
            ]
        )

        axis_label = Text("Principal\nAxis", font_size=13, color="#FAB387", font="Sans")
        axis_label.next_to(axis_line, RIGHT, buff=0.15)

        # ============================================
        # CENTER PANEL: Data Science - Scatter + PCA
        # ============================================
        scatter_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=3.5,
            y_length=3.5,
            axis_config={
                "color": "#585B70",
                "stroke_width": 1,
                "include_tip": False,
                "include_numbers": False,
            },
        )
        scatter_axes.move_to(ORIGIN + DOWN * 0.3)

        # Generate elongated scatter (correlated data along ~45 deg)
        np.random.seed(42)
        points = VGroup()
        base_angle = np.pi / 4
        for i in range(30):
            angle = base_angle + np.random.normal(0, 0.35)
            r = np.random.exponential(0.4) * 2.5
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            pt = Dot(
                point=scatter_axes.c2p(x, y),
                radius=0.04,
                color="#A6ADC8",
                fill_opacity=0.7,
            )
            points.add(pt)

        # PCA Arrow (PC1 - direction of greatest variance)
        pca_arrow = Arrow(
            start=scatter_axes.c2p(-2.0, -2.0),
            end=scatter_axes.c2p(2.0, 2.0),
            color="#F38BA8",
            stroke_width=3,
            tip_length=0.15,
            buff=0,
        )

        pca_label = Text("PC1", font_size=16, color="#F38BA8", font="Sans")
        pca_label.next_to(pca_arrow, UP, buff=0.1)

        # ============================================
        # RIGHT PANEL: Engineering - Bridge Mode Shape
        # ============================================
        bridge_center = RIGHT * 4

        # First mode shape (fundamental sine)
        def mode_1(t):
            x = t - 3
            y = 1.5 * np.sin(np.pi * (x + 3) / 6)
            return bridge_center + np.array([x, y, 0])

        wave = ParametricFunction(
            mode_1,
            t_range=[0, 6],
            color="#CBA6F7",
            stroke_width=2.5,
        )

        # Second mode shape (inverted for vibration effect)
        def mode_2(t):
            x = t - 3
            y = -1.2 * np.sin(np.pi * (x + 3) / 6)
            return bridge_center + np.array([x, y, 0])

        wave_2 = ParametricFunction(
            mode_2,
            t_range=[0, 6],
            color="#CBA6F7",
            stroke_width=2.5,
        )

        # Support pillars and ground
        left_pillar = Line(
            start=bridge_center + LEFT * 2.8 + DOWN * 1.5,
            end=bridge_center + LEFT * 2.8 + UP * 1.8,
            color="#585B70",
            stroke_width=2,
        )
        right_pillar = Line(
            start=bridge_center + RIGHT * 2.8 + DOWN * 1.5,
            end=bridge_center + RIGHT * 2.8 + UP * 1.8,
            color="#585B70",
            stroke_width=2,
        )
        ground = Line(
            start=bridge_center + LEFT * 3.5 + DOWN * 1.5,
            end=bridge_center + RIGHT * 3.5 + DOWN * 1.5,
            color="#585B70",
            stroke_width=1.5,
        )

        mode_label = Text("Mode Shape", font_size=14, color="#FAB387", font="Sans")
        mode_label.next_to(ground, DOWN, buff=0.15)

        # ============================================
        # ANIMATION SEQUENCE (Total: 8.0s)
        # ============================================

        # Phase 1: Build panels
        self.play(Create(divider_1), Create(divider_2), run_time=0.3)

        self.play(
            FadeIn(physics_title, shift=UP * 0.15),
            FadeIn(data_title, shift=UP * 0.15),
            FadeIn(eng_title, shift=UP * 0.15),
            run_time=0.4,
        )

        # Left panel build
        self.play(
            Create(ellipsoid),
            Create(inner_ellipse),
            Create(axis_line),
            FadeIn(glow_dots, lag_ratio=0.1),
            Write(axis_label),
            run_time=0.7,
        )

        # Center panel build
        self.play(Create(scatter_axes), run_time=0.3)
        self.play(
            LaggedStart(*[FadeIn(pt, scale=0.5) for pt in points], lag_ratio=0.03),
            run_time=0.4,
        )
        self.play(Create(pca_arrow), Write(pca_label), run_time=0.4)

        # Right panel build
        self.play(
            Create(left_pillar), Create(right_pillar), Create(ground), run_time=0.3
        )
        self.play(Create(wave), Write(mode_label), run_time=0.4)

        # Phase 2: Dynamic animations
        # Left: Full rotation of ellipsoid
        self.play(
            Rotate(ellipsoid, angle=PI * 2, about_point=LEFT * 4, rate_func=linear),
            Rotate(inner_ellipse, angle=PI * 2, about_point=LEFT * 4, rate_func=linear),
            run_time=1.6,
        )

        # Center: PCA arrow emphasis
        self.play(Indicate(pca_arrow, color="#F38BA8", scale_factor=1.1), run_time=0.6)

        # Right: Vibration cycles of the bridge
        self.play(Transform(wave, wave_2, run_time=0.35))
        self.play(Transform(wave, wave, run_time=0.35))
        self.play(Transform(wave, wave_2, run_time=0.3))
        self.play(Transform(wave, wave, run_time=0.3))

        # Phase 3: Final hold
        self.wait(1.3)
