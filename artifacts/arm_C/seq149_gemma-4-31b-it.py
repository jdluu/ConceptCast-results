import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Linear Transformations ---
        # Set background color as per style guidelines
        self.camera.background_color = "#181825"

        # Define colors from the provided palette
        # Palette: #89b4fa, #fab387, #f38ba8, #a6e3a1, #94e2d5
        COLOR_PLANE_BG = "#565F89"
        COLOR_GRID = "#89b4fa"
        COLOR_ORIGIN = "#f38ba8"

        # 1. Objects
        # Coordinate Plane - The static background reference
        # Fixed: 'include_tip' is the correct keyword for axis_config in NumberPlane
        coord_plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-7, 7, 1],
            background_line_style={"stroke_color": COLOR_PLANE_BG, "stroke_width": 1},
            axis_config={"include_tip": True},
        )

        # Transformation Grid - The "rubber sheet" that will be sheared
        # Fixed: Removed the incorrect 'include_tips' argument from axis_config.
        # Using 'include_tip': False to ensure the grid lines don't have arrows.
        trans_grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-7, 7, 1],
            background_line_style={"stroke_color": COLOR_GRID, "stroke_width": 2},
            axis_config={"include_tip": False},
        )

        # Origin Point - Pinned at the center
        origin_point = Dot(point=ORIGIN, color=COLOR_ORIGIN, radius=0.1)

        # Label for context
        title = Text("Linear Transformation: Shear", font="Sans", font_size=40)
        title.to_edge(UP)

        # 2. Animations
        # Initial setup: Fade in the plane and grid
        self.play(
            FadeIn(coord_plane),
            Create(trans_grid),
            FadeIn(origin_point),
            Write(title),
            run_time=3.0,
        )

        self.wait(2.0)

        # The Linear Transformation
        # A shear transformation matrix [1, 1; 0, 1]
        # x' = x + y
        # y' = y
        shear_matrix = [[1, 1], [0, 1]]

        # We animate the transformation over 5 seconds
        self.play(
            trans_grid.animate.apply_matrix(shear_matrix),
            run_time=5.0,
            rate_func=smooth,
        )

        # Highlight the origin to show it remains fixed
        self.play(
            Indicate(origin_point, color=COLOR_ORIGIN, scale_factor=1.5), run_time=1.5
        )

        # Final state hold to match total duration (15.0s)
        # 3.0 + 2.0 + 5.0 + 1.5 = 11.5s. Need 3.5s more.
        self.wait(3.5)
        # --- Scene 2: Vector Displacement ---
        self.clear()

        # --- Configuration & Colors ---
        BG_COLOR = "#181825"
        COLOR_BASE_VECTOR = "#BB9AF7"
        COLOR_TRANS_VECTOR = "#9ECE6A"
        COLOR_SPAN_LINE = "#565F89"
        COLOR_GRID = "#313244"

        self.camera.background_color = BG_COLOR

        # --- Objects ---
        # Grid setup
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-7, 7, 1],
            background_line_style={
                "stroke_color": COLOR_GRID,
                "stroke_width": 1.0,
            },
        )

        # Base Vector (v1 = [1, 1, 0])
        start_point = ORIGIN
        end_point = np.array([1, 1, 0])
        base_vector = Arrow(start_point, end_point, color=COLOR_BASE_VECTOR, buff=0)

        # Original Span Line (dashed line extending the vector's direction)
        span_start = -1.5 * end_point
        span_end = 3.5 * end_point
        # Fixed: Use DashedLine instead of Line with set_stroke(dash_length=...)
        span_line = DashedLine(
            span_start,
            span_end,
            color=COLOR_SPAN_LINE,
            dash_length=0.1,
            stroke_opacity=0.5,
        )

        # Target Vector (v2 = [2, 1, 0])
        target_end = np.array([2, 1, 0])
        transformed_vector = Arrow(
            start_point, target_end, color=COLOR_TRANS_VECTOR, buff=0
        )
        transformed_vector.set_opacity(0)  # Start hidden

        # --- Animation Sequence ---
        # Total Duration: 12.0s

        # 1. Setup: Show grid and original vector (2.0s)
        self.add(grid)
        self.play(Create(span_line), GrowFromCenter(base_vector), run_time=1.5)
        self.wait(0.5)  # Total: 2.0s

        # 2. Transformation buildup (1.0s)
        self.play(Indicate(base_vector, scale_factor=1.1), run_time=1.0)  # Total: 3.0s

        # 3. The Transformation (4.0s)
        # Using ReplacementTransform for the vector and animate the grid stretching
        self.play(
            ReplacementTransform(base_vector, transformed_vector),
            grid.animate.stretch_to_fit_width(grid.width * 1.5),
            run_time=3.0,
            rate_func=smooth,
        )
        self.wait(1.0)  # Total: 7.0s

        # 4. Highlighting the Displacement (3.0s)
        # Projection of (2,1) onto the line spanned by (1,1) is (1.5, 1.5)
        projection_point = np.array([1.5, 1.5, 0])
        displacement_line = DashedLine(
            target_end, projection_point, color=COLOR_BASE_VECTOR, stroke_width=2
        )

        self.play(Create(displacement_line), run_time=1.5)
        self.play(Indicate(displacement_line), run_time=1.5)  # Total: 10.0s

        # 5. Final Hold (2.0s)
        self.wait(2.0)  # Total: 12.0s
        # --- Scene 3: The Eigenvector Definition ---
        self.clear()

        # --- Style Setup ---
        # Primary Palette
        COLOR_BG = "#181825"
        COLOR_CLOUD = "#565F89"
        COLOR_EIGEN = "#fab387"  # Using a warm gold-ish from the palette
        COLOR_SPAN = "#565F89"

        self.camera.background_color = COLOR_BG

        # --- Objects ---
        # 1. The Coordinate System (subtle)
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-7, 7, 1],
            background_line_style={"stroke_color": "#2d2d3d", "stroke_width": 1},
            axis_config={"include_ticks": False},
        )

        # 2. The Eigen-Span (the line the eigenvector stays on)
        # Use DashedLine instead of Line.set_stroke(dash_length=...) to avoid previous errors
        eigen_span = DashedLine(
            start=np.array([-4, 0, 0]),
            end=np.array([6, 0, 0]),
            color=COLOR_SPAN,
            stroke_opacity=0.4,
        )

        # 3. The Eigenvector
        # Starting at [2, 0, 0]
        eigenvector = Arrow(
            start=ORIGIN, end=[2, 0, 0], color=COLOR_EIGEN, buff=0, stroke_width=4
        )

        # 4. The Vector Cloud (Random vectors that will change direction)
        # We'll create a few vectors scattered around
        cloud_points = [
            [1, 2, 0],
            [-2, 1, 0],
            [2, -1, 0],
            [-1, -2, 0],
            [1.5, 1.5, 0],
            [-1.5, -1.5, 0],
            [0, 2, 0],
            [0, -2, 0],
        ]
        vector_cloud = VGroup(
            *[
                Arrow(start=ORIGIN, end=p, color=COLOR_CLOUD, buff=0, stroke_width=2)
                for p in cloud_points
            ]
        )

        # --- Animations ---

        # Total Duration: 15.0s

        # Phase 1: Setup and Introduction (4.0s)
        self.add(grid)
        self.play(
            Create(eigen_span),
            FadeIn(vector_cloud, lag_ratio=0.1),
            Write(eigenvector),
            run_time=3.0,
        )
        self.wait(1.0)

        # Phase 2: The Transformation (5.0s)
        # We define a transformation matrix. Let's use a shear/scale.
        # Matrix [[2, 0], [0, 0.5]] -> Eigenvector [1,0] stays on axis and scales by 2.
        # Others will rotate/shift.

        # Transformation targets
        # Eigenvector: scales from 2 to 4
        eigenvector_target = Arrow(
            start=ORIGIN, end=[4, 0, 0], color=COLOR_EIGEN, buff=0, stroke_width=4
        )

        # Cloud vectors: transformed by [[2, 0], [0, 0.5]]
        # Note: Since these are just Arrows, we transform the end point.
        cloud_targets = VGroup(
            *[
                Arrow(
                    start=ORIGIN,
                    end=[p[0] * 2, p[1] * 0.5, 0],
                    color=COLOR_CLOUD,
                    buff=0,
                    stroke_width=2,
                )
                for p in cloud_points
            ]
        )

        # Animation of transformation
        self.play(
            ReplacementTransform(eigenvector, eigenvector_target),
            ReplacementTransform(vector_cloud, cloud_targets),
            run_time=4.0,
            rate_func=smooth,
        )

        # Highlight the fact that the eigenvector stayed on the line
        self.play(
            Indicate(eigenvector_target, color=COLOR_EIGEN, scale_factor=1.1),
            run_time=1.0,
        )

        # Phase 3: Final Observation (6.0s)
        # Adding a textual explanation to reinforce the pedagogical goal
        label = Text(
            "Stays on its span", font="Sans", font_size=32, color=COLOR_EIGEN
        ).next_to(eigenvector_target, UP, buff=0.5)

        self.play(Write(label), run_time=2.0)
        self.wait(4.0)

        # Sum of run_times: 3.0 + 1.0 + 4.0 + 1.0 + 2.0 + 4.0 = 15.0 seconds
        # --- Scene 4: The Eigenvalue ---
        self.clear()

        # Colors based on style guidelines
        BG_COLOR = "#181825"
        COLOR_LAMBDA = "#C0CAF5"
        COLOR_VECTOR = "#E0AF68"
        COLOR_SCALAR = "#2AC3DE"

        self.camera.background_color = BG_COLOR

        # 1. Objects Setup
        # We define an eigenvector for this scene.
        # Let's assume the eigenvector is in the direction [2, 1, 0]
        vec_dir = np.array([2, 1, 0])
        vec_unit = vec_dir / np.linalg.norm(vec_dir)
        initial_length = 2.0

        # The main ScalingVector
        # We use a function for the arrow to make it easier to update via ValueTracker
        # or just create targets.
        eigenvector = Arrow(
            start=ORIGIN, end=vec_unit * initial_length, color=COLOR_VECTOR, buff=0
        )

        # Lambda label
        lambda_label = MathTex(r"\lambda", color=COLOR_LAMBDA, font_size=60).next_to(
            eigenvector.get_end(), UP + RIGHT, buff=0.2
        )

        # Scalar value display (Top Right)
        scalar_value = MathTex(
            r"\lambda = 1", color=COLOR_SCALAR, font_size=48
        ).to_corner(UR, buff=1.0)

        # Reference line to show the axis (eigen-axis)
        axis_line = Line(
            start=-vec_unit * 4, end=vec_unit * 4, color=GRAY, stroke_opacity=0.3
        )

        # 2. Animations

        # Initial state
        self.add(axis_line)
        self.play(
            Create(eigenvector), Write(lambda_label), Write(scalar_value), run_time=2.0
        )
        self.wait(1.0)  # Total: 3.0

        # Transition 1: Scaling to 2x (Stretching)
        # We'll use a replacement transform or just animate the end point
        target_2x = Arrow(
            start=ORIGIN,
            end=vec_unit * (initial_length * 2),
            color=COLOR_VECTOR,
            buff=0,
        )
        scalar_2x = MathTex(r"\lambda = 2", color=COLOR_SCALAR, font_size=48).to_corner(
            UR, buff=1.0
        )

        self.play(
            Transform(eigenvector, target_2x),
            ReplacementTransform(scalar_value, scalar_2x),
            lambda_label.animate.next_to(target_2x.get_end(), UP + RIGHT, buff=0.2),
            run_time=2.0,
        )
        self.wait(1.0)  # Total: 6.0

        # Update local references for next steps
        scalar_value = scalar_2x

        # Transition 2: Scaling to 0.5x (Shrinking)
        target_05x = Arrow(
            start=ORIGIN,
            end=vec_unit * (initial_length * 0.5),
            color=COLOR_VECTOR,
            buff=0,
        )
        scalar_05x = MathTex(
            r"\lambda = 0.5", color=COLOR_SCALAR, font_size=48
        ).to_corner(UR, buff=1.0)

        self.play(
            Transform(eigenvector, target_05x),
            ReplacementTransform(scalar_value, scalar_05x),
            lambda_label.animate.next_to(target_05x.get_end(), UP + RIGHT, buff=0.2),
            run_time=2.0,
        )
        self.wait(1.0)  # Total: 9.0

        scalar_value = scalar_05x

        # Transition 3: Scaling to -1x (Flipping)
        # Eigenvalue is negative, flips to opposite side
        target_neg = Arrow(
            start=ORIGIN, end=-vec_unit * initial_length, color=COLOR_VECTOR, buff=0
        )
        scalar_neg = MathTex(
            r"\lambda = -1", color=COLOR_SCALAR, font_size=48
        ).to_corner(UR, buff=1.0)

        self.play(
            Transform(eigenvector, target_neg),
            ReplacementTransform(scalar_value, scalar_neg),
            lambda_label.animate.next_to(target_neg.get_end(), DOWN + LEFT, buff=0.2),
            run_time=3.0,  # Slower flip for clarity
        )

        # Final hold to match total duration of 14s
        # Current total: 9.0 + 3.0 = 12.0. Need 2.0 more.
        self.wait(2.0)  # Total: 14.0
        # --- Scene 5: The Characteristic Equation ---
        # --- Configuration & Colors ---
        BG_COLOR = "#181825"
        PRIMARY_COLOR = "#89b4fa"  # Blueish
        ACCENT_COLOR = "#f38ba8"  # Pinkish/Red
        GRID_COLOR = "#565F89"  # Muted Blue/Grey
        TEXT_COLOR = "#C0CAF5"  # Light Lavender

        self.camera.background_color = BG_COLOR

        # --- 1. Objects ---

        # The initial grid (representing geometric space)
        collapsing_plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-7, 7, 1],
            background_line_style={"stroke_color": GRID_COLOR, "stroke_width": 1},
            axis_config={"include_numbers": False},
        )

        # Equations using raw strings (r"") to avoid LaTeX escape sequence warnings
        # Eq1: Av = lambda v
        eq1 = MathTex(
            r"A\mathbf{v} = \lambda\mathbf{v}", color=TEXT_COLOR, font_size=72
        )

        # Eq2: (A - lambda I)v = 0
        eq2 = MathTex(
            r"(A - \lambda I)", r"\mathbf{v} = 0", color=TEXT_COLOR, font_size=72
        )

        # The determinant symbol
        det_symbol = MathTex(
            r"\det(A - \lambda I) = 0", color=ACCENT_COLOR, font_size=48
        ).shift(UP * 2.0)

        brace = Brace(eq2[0], direction=UP, color=ACCENT_COLOR)
        brace_text = Text("Singular Matrix", font_size=24, color=ACCENT_COLOR).next_to(
            brace, UP, buff=0.1
        )

        # --- 2. Animations ---

        # T=0: Setup plane and Eq1
        self.add(collapsing_plane)
        self.play(Write(eq1), run_time=2.0)
        self.wait(1.0)  # Cumulative: 3.0

        # T=3: Morph Eq1 to Eq2
        self.play(ReplacementTransform(eq1, eq2), run_time=2.0)
        self.wait(1.0)  # Cumulative: 6.0

        # T=6: Highlight the (A - lambda I) part
        self.play(Create(brace), Write(brace_text), run_time=2.0)
        self.wait(1.0)  # Cumulative: 9.0

        # T=9: Introduce determinant and collapse space
        # Using a non-uniform scale [x, y, z] to flatten the plane into a line on the X axis
        self.play(
            FadeIn(det_symbol, shift=DOWN * 0.5),
            collapsing_plane.animate.scale([1, 0.01, 1]),
            run_time=3.0,
        )
        self.wait(1.0)  # Cumulative: 13.0

        # Final polish: Indicate the determinant result
        self.play(
            Indicate(det_symbol, color=ACCENT_COLOR, scale_factor=1.2), run_time=2.0
        )

        self.wait(1.0)  # Cumulative: 16.0
        # --- Scene 6: Eigenspace ---
        # Fix: Use self.camera.background_color as per style guidelines
        self.camera.background_color = "#181825"

        # Define the colors from the palette
        C_EIGENLINE = "#7AA2F7"  # Bright highlighted blue
        C_VECTORS = "#BB9AF7"  # Purple for the vectors
        C_AXES = "#444466"  # Subtle color for axes

        # 1. Objects
        # Create coordinate plane (Axes)
        axes = Axes(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            x_length=12,
            y_length=6,
            axis_config={"color": C_AXES, "include_tip": False},
        ).set_stroke(width=1.0)

        # Eigenspace Line: Defined by a direction vector [2, 1, 0]
        dir_vec = np.array([2, 1, 0])
        line_start = -3 * dir_vec
        line_end = 3 * dir_vec

        eigen_line = Line(
            start=line_start, end=line_end, color=C_EIGENLINE, stroke_width=4
        )

        # MultiVectorSet: Several vectors along the line
        scalars = [-2, -1, 0.5, 1.2, 2.5]
        vectors = VGroup()
        for s in scalars:
            # Fix: Removed 'max_tip_length' as it's not a valid keyword argument for Arrow
            vec = Arrow(
                start=ORIGIN, end=s * dir_vec, color=C_VECTORS, buff=0, stroke_width=3
            )
            vectors.add(vec)

        # Title/Text
        text = Tex("Eigenspace", font_size=48, color=WHITE).to_edge(UP)

        # 2. Animations
        # Total desired duration: 12.0s

        # (0.0 - 2.0s) Fade in axes and title
        self.play(Create(axes), Write(text), run_time=2.0)
        self.wait(0.5)  # (2.0 - 2.5s)

        # (2.5 - 4.5s) Create the eigenspace line
        self.play(Create(eigen_line), run_time=2.0)
        self.wait(0.5)  # (4.5 - 5.0s)

        # (5.0 - 7.0s) Plot the vectors one by one
        self.play(
            LaggedStart(*[GrowFromCenter(v) for v in vectors], lag_ratio=0.2),
            run_time=2.0,
        )
        self.wait(1.0)  # (7.0 - 8.0s)

        # (8.0 - 12.0s) Pulsing animation
        # Split into two 2-second segments to reach exactly 12.0s
        self.play(
            *[vec.animate.scale(1.1).set_color(WHITE) for vec in vectors], run_time=2.0
        )
        self.play(
            *[vec.animate.scale(1 / 1.1).set_color(C_VECTORS) for vec in vectors],
            run_time=2.0,
        )
        # --- Scene 7: Diagonalization ---
        self.clear()

        # Set background color as per style guidelines
        # Note: self.set_background_color is not a method of Scene.
        # Use self.camera.background_color or simply add a background rectangle.
        bg = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color="#181825",
            fill_opacity=1,
            stroke_width=0,
        )
        self.add(bg)

        # Define professional color palette
        COLOR_PRIMARY = "#89b4fa"  # Blue
        COLOR_SECONDARY = "#fab387"  # Orange
        COLOR_ACCENT = "#a6e3a1"  # Green
        COLOR_TEXT = "#C0CAF5"  # Light Blue/Gray
        COLOR_PLANE_LEFT = "#565F89"
        COLOR_PLANE_RIGHT = "#9ECE6A"

        # --- 1. Objects Setup ---

        # Left Plane: Original Basis (Standard Euclidean)
        # We'll represent the "skewed" effect by showing a transformation on it
        left_plane = NumberPlane(
            x_range=[-4, 4],
            y_range=[-4, 4],
            x_length=5,
            y_length=5,
            axis_config={"color": COLOR_PLANE_LEFT},
            background_line_style={
                "stroke_color": COLOR_PLANE_LEFT,
                "stroke_opacity": 0.3,
            },
        ).shift(LEFT * 3.5)

        # Right Plane: Eigen Basis
        right_plane = NumberPlane(
            x_range=[-4, 4],
            y_range=[-4, 4],
            x_length=5,
            y_length=5,
            axis_config={"color": COLOR_PLANE_RIGHT},
            background_line_style={
                "stroke_color": COLOR_PLANE_RIGHT,
                "stroke_opacity": 0.3,
            },
        ).shift(RIGHT * 3.5)

        # Matrix A and Decomposition
        matrix_a_tex = MathTex(r"A", color=COLOR_PRIMARY).shift(UP * 3 + LEFT * 3.5)
        matrix_diag_tex = MathTex(r"D", color=COLOR_ACCENT).shift(UP * 3 + RIGHT * 3.5)

        decomposition_eq = MathTex(r"A = PDP^{-1}", color=COLOR_TEXT).to_edge(
            DOWN, buff=1.0
        )

        # --- 2. Visual Metaphors (Transformation) ---

        # Define a simple diagonalizable matrix A
        # A = [[2, 1], [1, 2]] -> Eigenvalues 3, 1. Eigenvectors [1, 1] and [1, -1]
        # To visualize "skewing" vs "scaling"

        # Object on the left: A simple square that will be skewed
        square_left = Square(side_length=1, color=COLOR_SECONDARY).move_to(
            left_plane.coords_to_point(0, 0)
        )

        # The "Skewed" version of the square (A * v)
        # For A=[[2,1],[1,2]], (1,0)->(2,1), (0,1)->(1,2), (1,1)->(3,3)
        skewed_square = Polygon(
            left_plane.coords_to_point(0, 0),
            left_plane.coords_to_point(2, 1),
            left_plane.coords_to_point(3, 3),
            left_plane.coords_to_point(1, 2),
            color=COLOR_SECONDARY,
            fill_opacity=0.5,
        )

        # Object on the right: The same transformation, but represented as simple scaling along axes
        # Since we are in the Eigen-basis, the transformation is just stretching
        # Let's say axis X is scaled by 3 and axis Y by 1
        rect_right = Rectangle(
            width=3, height=1, color=COLOR_SECONDARY, fill_opacity=0.5
        ).move_to(right_plane.coords_to_point(0, 0))

        # Start with a small square on the right to show the "scaling" process
        square_right = Square(
            side_length=1, color=COLOR_SECONDARY, fill_opacity=0.5
        ).move_to(right_plane.coords_to_point(0, 0))

        # --- 3. Animation Sequence ---

        # Total duration target: 13.0s

        # Initial Appearance (2s)
        self.play(
            Create(left_plane),
            Create(right_plane),
            Write(matrix_a_tex),
            Write(matrix_diag_tex),
            run_time=2.0,
        )
        self.wait(0.5)

        # Step 1: Show skewed transformation on the left (3s)
        self.play(FadeIn(square_left), run_time=0.5)
        self.play(ReplacementTransform(square_left, skewed_square), run_time=2.0)
        self.wait(0.5)

        # Step 2: Show scaling transformation on the right (3s)
        self.play(FadeIn(square_right), run_time=0.5)
        self.play(ReplacementTransform(square_right, rect_right), run_time=2.0)
        self.wait(0.5)

        # Step 3: Introduce the Equation (3s)
        self.play(Write(decomposition_eq), run_time=1.5)
        # Highlight components of the equation
        self.play(
            Indicate(decomposition_eq[0][0]),  # A
            run_time=0.5,
        )
        self.play(
            Indicate(decomposition_eq[0][2]),  # D
            run_time=0.5,
        )
        self.play(
            Indicate(decomposition_eq[0][3]),  # P and P^-1
            run_time=0.5,
        )

        # Final Pause (1s)
        self.wait(1.0)

        # Calculation: 2.0 + 0.5 + 0.5 + 2.0 + 0.5 + 0.5 + 2.0 + 0.5 + 1.5 + 0.5 + 0.5 + 0.5 + 1.0 = 12.5s
        # Adding a tiny bit more wait to hit exactly 13.0s
        self.wait(0.5)
