from manim import *

class SceneGen(Scene):
    def construct(self):
        # ============================================
        # SCENE 1: Introduction to Vectors
        # ============================================
        
        # Title
        title = Text("Linear Transformations and Eigenvectors", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Create coordinate plane
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"stroke_color": GREY},
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        self.play(Create(plane), run_time=2)
        
        # Show a vector v
        vector_v = Arrow(ORIGIN, [2, 1, 0], buff=0, color=YELLOW)
        vector_v_label = MathTex(r"\vec{v}", color=YELLOW).next_to(vector_v.get_end(), UR, buff=0.1)
        
        self.play(GrowArrow(vector_v), Write(vector_v_label))
        self.wait(0.5)
        
        # Explain what a vector is
        explanation1 = Text("A vector has direction and magnitude", font_size=28)
        explanation1.to_edge(DOWN)
        self.play(Write(explanation1))
        self.wait(1)
        
        # Transform the vector
        vector_w = Arrow(ORIGIN, [-1, 3, 0], buff=0, color=GREEN)
        vector_w_label = MathTex(r"\vec{w}", color=GREEN).next_to(vector_w.get_end(), UL, buff=0.1)
        
        self.play(
            Transform(vector_v, vector_w),
            Transform(vector_v_label, vector_w_label)
        )
        self.wait(0.5)
        
        # Update explanation
        explanation2 = Text("Linear transformations change vectors", font_size=28)
        explanation2.to_edge(DOWN)
        self.play(Transform(explanation1, explanation2))
        self.wait(1.5)
        
        self.clear()

        # ============================================
        # SCENE 2: Show what a linear transformation does
        # ============================================
        
        title2 = Text("Linear Transformations", font_size=36)
        title2.to_edge(UP)
        self.play(Write(title2))
        
        # Create fresh plane
        plane2 = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"stroke_color": GREY},
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        self.play(Create(plane2), run_time=2)
        
        # Show basis vectors
        e1 = Arrow(ORIGIN, [1, 0, 0], buff=0, color=RED)
        e1_label = MathTex(r"\hat{i}", color=RED).next_to(e1.get_end(), DOWN, buff=0.1)
        e2 = Arrow(ORIGIN, [0, 1, 0], buff=0, color=GREEN)
        e2_label = MathTex(r"\hat{j}", color=GREEN).next_to(e2.get_end(), LEFT, buff=0.1)
        
        self.play(GrowArrow(e1), GrowArrow(e2), Write(e1_label), Write(e2_label))
        
        explanation = Text("Standard basis vectors", font_size=28)
        explanation.to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(1)
        
        # Transform the plane with a matrix
        transform_label = MathTex(r"A = \begin{pmatrix} 2 & 1 \\ 0 & 2 \end{pmatrix}", font_size=32)
        transform_label.to_edge(DOWN)
        self.play(Transform(explanation, transform_label))
        
        # Apply matrix transformation
        matrix = [[2, 1], [0, 2]]
        self.play(
            plane2.animate.apply_matrix(matrix),
            e1.animate.apply_matrix(matrix),
            e2.animate.apply_matrix(matrix),
            run_time=3
        )
        self.wait(0.5)
        
        # Update basis labels
        e1_new_label = MathTex(r"A\hat{i}", color=RED).next_to(e1.get_end(), DOWN, buff=0.1)
        e2_new_label = MathTex(r"A\hat{j}", color=GREEN).next_to(e2.get_end(), LEFT, buff=0.1)
        self.play(Transform(e1_label, e1_new_label), Transform(e2_label, e2_new_label))
        self.wait(1.5)
        
        self.clear()

        # ============================================
        # SCENE 3: Show a vector that does NOT change direction
        # ============================================
        
        title3 = Text("Special Case: Direction Preserved", font_size=36)
        title3.to_edge(UP)
        self.play(Write(title3))
        
        plane3 = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"stroke_color": GREY},
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        self.play(Create(plane3), run_time=2)
        
        # Show a horizontal vector
        special_v = Arrow(ORIGIN, [3, 0, 0], buff=0, color=YELLOW)
        special_label = MathTex(r"\vec{v}", color=YELLOW).next_to(special_v.get_end(), UP, buff=0.1)
        
        self.play(GrowArrow(special_v), Write(special_label))
        
        explain = Text("This vector lies on the x-axis", font_size=28)
        explain.to_edge(DOWN)
        self.play(Write(explain))
        self.wait(1)
        
        # Apply same transformation [[2,1],[0,2]]
        matrix2 = [[2, 1], [0, 2]]
        
        # Create transformed vector
        special_v_transformed = Arrow(ORIGIN, [6, 0, 0], buff=0, color=ORANGE)
        transformed_label = MathTex(r"A\vec{v}", color=ORANGE).next_to(special_v_transformed.get_end(), UP, buff=0.1)
        
        self.play(
            explain.animate.become(Text("After transformation...", font_size=28).to_edge(DOWN)),
            plane3.animate.apply_matrix(matrix2),
            Transform(special_v, special_v_transformed),
            run_time=2.5
        )
        
        # Show the result
        result_text = MathTex(r"A\vec{v} = 2\vec{v} = \begin{pmatrix} 6 \\ 0 \end{pmatrix}", font_size=30)
        result_text.to_edge(DOWN)
        self.play(Transform(explain, result_text))
        self.wait(0.5)
        self.play(Transform(special_label, transformed_label))
        self.wait(1)
        
        # Key observation
        key_text = Text("Direction unchanged! Only scaled by 2", font_size=26, color=GREEN)
        key_text.to_edge(DOWN)
        self.play(Transform(explain, key_text))
        self.wait(1.5)
        
        self.clear()

        # ============================================
        # SCENE 4: Contrast with a vector that DOES change direction
        # ============================================
        
        title4 = Text("Contrast: Direction Changed", font_size=36)
        title4.to_edge(UP)
        self.play(Write(title4))
        
        plane4 = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"stroke_color": GREY},
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        self.play(Create(plane4), run_time=2)
        
        # Show a general vector
        general_v = Arrow(ORIGIN, [2, 2, 0], buff=0, color=PURPLE)
        general_label = MathTex(r"\vec{w}", color=PURPLE).next_to(general_v.get_end(), UR, buff=0.1)
        
        self.play(GrowArrow(general_v), Write(general_label))
        
        explain4 = Text("General vector not on x-axis", font_size=28)
        explain4.to_edge(DOWN)
        self.play(Write(explain4))
        self.wait(1)
        
        # Apply transformation
        transformed_w = Arrow(ORIGIN, [6, 4, 0], buff=0, color=PINK)
        transformed_w_label = MathTex(r"A\vec{w}", color=PINK).next_to(transformed_w.get_end(), UR, buff=0.1)
        
        self.play(
            explain4.animate.become(Text("After same transformation...", font_size=28).to_edge(DOWN)),
            plane4.animate.apply_matrix([[2, 1], [0, 2]]),
            Transform(general_v, transformed_w),
            run_time=2.5
        )
        
        # Dashed line to show original direction
        original_direction = DashedLine(ORIGIN, [3, 3, 0], color=GRAY)
        self.play(Create(original_direction))
        
        # Show angle difference
        compare_text = Text("Direction changed! Not a simple scaling", font_size=26, color=RED)
        compare_text.to_edge(DOWN)
        self.play(Transform(explain4, compare_text))
        self.play(Transform(general_label, transformed_w_label))
        self.wait(1.5)
        
        self.clear()

        # ============================================
        # SCENE 5: Define Eigenvector and Eigenvalue
        # ============================================
        
        title5 = Text("Eigenvectors and Eigenvalues", font_size=36)
        title5.to_edge(UP)
        self.play(Write(title5))
        
        plane5 = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"stroke_color": GREY},
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        self.play(Create(plane5), run_time=2)
        
        # The defining equation
        eq1 = MathTex(r"A\vec{v} = \lambda \vec{v}", font_size=40)
        eq1.move_to(RIGHT * 2 + UP * 2)
        self.play(Write(eq1))
        
        # Break it down
        breakdown = VGroup(
            MathTex(r"\text{Where:}", font_size=28),
            MathTex(r"\vec{v} \text{ is the eigenvector (direction)}", font_size=26, color=YELLOW),
            MathTex(r"\lambda \text{ is the eigenvalue (scaling factor)}", font_size=26, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT)
        breakdown.move_to(RIGHT * 2 + DOWN * 1.5)
        
        self.play(Write(breakdown), run_time=2)
        self.wait(1)
        
        # Show visual example
        eigen_v = Arrow(ORIGIN, [2.5, 0, 0], buff=0, color=YELLOW)
        eigen_label = MathTex(r"\vec{v}", color=YELLOW).next_to(eigen_v.get_end(), UP, buff=0.1)
        
        self.play(
            FadeOut(eq1),
            FadeOut(breakdown),
            GrowArrow(eigen_v),
            Write(eigen_label)
        )
        
        # Animate the scaling
        scaled_v = Arrow(ORIGIN, [5, 0, 0], buff=0, color=YELLOW)
        self.play(
            ReplacementTransform(eigen_v.copy(), scaled_v),
            eigen_v.animate.set_opacity(0.3),
            run_time=2
        )
        
        # Show lambda
        lambda_label = MathTex(r"\lambda = 2", font_size=32, color=GREEN)
        lambda_label.move_to(LEFT * 3 + UP * 2)
        self.play(Write(lambda_label))
        
        # Double-headed arrow showing scaling
        brace = DoubleArrow([2.5, -0.5, 0], [5, -0.5, 0], buff=0, color=GREEN)
        brace_label = MathTex(r"\times 2", font_size=24, color=GREEN).next_to(brace, DOWN, buff=0.1)
        
        self.play(Create(brace), Write(brace_label))
        self.wait(1.5)
        
        self.clear()

        # ============================================
        # SCENE 6: Find eigenvalues - the characteristic equation
        # ============================================
        
        title6 = Text("Finding Eigenvalues", font_size=36)
        title6.to_edge(UP)
        self.play(Write(title6))
        
        # Start with Av = λv
        eq_start = MathTex(r"A\vec{v} = \lambda \vec{v}", font_size=36)
        eq_start.move_to(UP * 2)
        self.play(Write(eq_start))
        self.wait(0.5)
        
        # Rearrange
        eq2 = MathTex(r"A\vec{v} - \lambda \vec{v} = \vec{0}", font_size=36)
        eq2.move_to(UP * 2)
        self.play(Transform(eq_start, eq2))
        self.wait(0.5)
        
        # Factor out v
        eq3 = MathTex(r"(A - \lambda I)\vec{v} = \vec{0}", font_size=36)
        eq3.move_to(UP * 2)
        self.play(Transform(eq_start, eq3))
        self.wait(0.5)
        
        # Key insight
        insight = Text("For non-zero v, the matrix must be singular", font_size=26)
        insight.move_to(UP * 0.5)
        self.play(Write(insight))
        self.wait(0.5)
        
        # Determinant condition
        det_eq = MathTex(r"\det(A - \lambda I) = 0", font_size=40, color=YELLOW)
        self.play(Write(det_eq))
        self.wait(0.5)
        
        # Example with A = [[2,1],[0,2]]
        example = VGroup(
            MathTex(r"\text{Example: } A = \begin{pmatrix} 2 & 1 \\ 0 & 2 \end{pmatrix}", font_size=28),
            MathTex(r"\det\begin{pmatrix} 2-\lambda & 1 \\ 0 & 2-\lambda \end{pmatrix} = 0", font_size=28),
            MathTex(r"(2-\lambda)^2 = 0", font_size=28),
            MathTex(r"\lambda = 2 \text{ (repeated)}", font_size=28, color=GREEN)
        ).arrange(DOWN, buff=0.4)
        example.to_edge(DOWN)
        
        self.play(Write(example), run_time=3)
        self.wait(1.5)
        
        self.clear()

        # ============================================
        # SCENE 7: Find eigenvectors for λ = 2
        # ============================================
        
        title7 = Text("Finding Eigenvectors", font_size=36)
        title7.to_edge(UP)
        self.play(Write(title7))
        
        # Substitute eigenvalue
        sub_label = MathTex(r"\lambda = 2: \quad (A - 2I)\vec{v} = \vec{0}", font_size=32)
        sub_label.move_to(UP * 2.5)
        self.play(Write(sub_label))
        
        # Show the matrix
        matrix_eq = MathTex(r"\begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}", font_size=32)
        matrix_eq.move_to(UP * 1)
        self.play(Write(matrix_eq))
        self.wait(0.5)
        
        # Solve
        solution_steps = VGroup(
            MathTex(r"\Rightarrow y = 0", font_size=28),
            MathTex(r"x \text{ is free}", font_size=28),
            MathTex(r"\vec{v} = \begin{pmatrix} x \\ 0 \end{pmatrix} = x\begin{pmatrix} 1 \\ 0 \end{pmatrix}", font_size=28, color=YELLOW)
        ).arrange(DOWN, buff=0.3)
        solution_steps.move_to(DOWN * 0.5)
        
        self.play(Write(solution_steps), run_time=2)
        self.wait(1)
        
        # Show on plane
        plane7 = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"stroke_color": GREY},
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        plane7.scale(0.6)
        plane7.move_to(LEFT * 3.5 + DOWN * 1)
        
        self.play(FadeOut(sub_label), FadeOut(matrix_eq), FadeOut(solution_steps))
        self.play(Create(plane7), run_time=2)
        
        # Draw the eigenspace
        eigenspace = Line([-4, -1, 0], [4, -1, 0], color=YELLOW, stroke_width=4)
        self.play(Create(eigenspace))
        
        # Label it
        eigenspace_label = Text("Eigenspace for λ=2", font_size=22, color=YELLOW)
        eigenspace_label.next_to(eigenspace, DOWN, buff=0.2)
        self.play(Write(eigenspace_label))
        
        # Show eigenvectors along this line
        v1 = Arrow([-2, -1, 0], [-0.5, -1, 0], buff=0, color=YELLOW)
        v2 = Arrow([0.5, -1, 0], [2, -1, 0], buff=0, color=YELLOW)
        v1_label = MathTex(r"\vec{v}_1", font_size=20, color=YELLOW).next_to(v1, UP, buff=0.05)
        v2_label = MathTex(r"\vec{v}_2", font_size=20, color=YELLOW).next_to(v2, UP, buff=0.05)
        
        self.play(GrowArrow(v1), GrowArrow(v2), Write(v1_label), Write(v2_label))
        self.wait(1.5)
        
        self.clear()

        # ============================================
        # SCENE 8: Geometric interpretation - stretching
        # ============================================
        
        title8 = Text("Geometric Meaning: Stretching", font_size=36)
        title8.to_edge(UP)
        self.play(Write(title8))
        
        # Create a more interesting example: diagonal matrix
        plane8 = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"stroke_color": GREY},
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        self.play(Create(plane8), run_time=2)
        
        # Multiple vectors before transformation
        vectors_before = VGroup(
            Arrow(ORIGIN, [2, 0, 0], buff=0, color=RED),
            Arrow(ORIGIN, [0, 1.5, 0], buff=0, color=GREEN),
            Arrow(ORIGIN, [1.5, 1, 0], buff=0, color=GRAY)
        )
        labels_before = VGroup(
            MathTex(r"\vec{v}_1", color=RED).next_to(vectors_before[0].get_end(), DOWN, buff=0.1),
            MathTex(r"\vec{v}_2", color=GREEN).next_to(vectors_before[1].get_end(), LEFT, buff=0.1),
            MathTex(r"\vec{w}", color=GRAY).next_to(vectors_before[2].get_end(), UR, buff=0.1)
        )
        
        self.play(
            *[GrowArrow(v) for v in vectors_before],
            *[Write(l) for l in labels_before],
            run_time=1.5
        )
        
        explain8 = Text("Transformation: stretch x by 3, y by 1", font_size=26)
        explain8.to_edge(DOWN)
        self.play(Write(explain8))
        self.wait(1)
        
        # Apply diagonal transformation [[3,0],[0,1]]
        matrix_diag = [[3, 0], [0, 1]]
        
        self.play(
            plane8.animate.apply_matrix(matrix_diag),
            vectors_before[0].animate.apply_matrix(matrix_diag),
            vectors_before[1].animate.apply_matrix(matrix_diag),
            vectors_before[2].animate.apply_matrix(matrix_diag),
            run_time=3
        )
        
        # Show new labels
        labels_after = VGroup(
            MathTex(r"3\vec{v}_1", color=RED).move_to([5, -0.5, 0]),
            MathTex(r"1\vec{v}_2", color=GREEN).move_to([0, 2, 0]),
            MathTex(r"A\vec{w}", color=GRAY).move_to([5.5, 1.5, 0])
        )
        
        self.play(Transform(labels_before, labels_after))
        
        # Highlight eigenvectors
        highlight1 = SurroundingRectangle(labels_after[0], color=YELLOW)
        highlight2 = SurroundingRectangle(labels_after[1], color=YELLOW)
        
        self.play(Create(highlight1))
        explain_eigen = Text("These preserved their directions - eigenvectors!", font_size=24, color=YELLOW)
        explain_eigen.to_edge(DOWN)
        self.play(Transform(explain8, explain_eigen))
        
        self.play(Transform(highlight1, highlight2))
        self.wait(1.5)
        
        self.clear()

        # ============================================
        # SCENE 9: Rotation example - no real eigenvectors
        # ============================================
        
        title9 = Text("Rotation: No Real Eigenvalues", font_size=36)
        title9.to_edge(UP)
        self.play(Write(title9))
        
        plane9 = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"stroke_color": GREY},
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        )
        self.play(Create(plane9), run_time=2)
        
        # Show vectors
        rotate_v = Arrow(ORIGIN, [2, 0, 0], buff=0, color=YELLOW)
        rotate_label = MathTex(r"\vec{v}", color=YELLOW).next_to(rotate_v.get_end(), UP, buff=0.1)
        
        self.play(GrowArrow(rotate_v), Write(rotate_label))
        
        explain9 = Text("90° rotation matrix", font_size=28)
        explain9.to_edge(DOWN)
        self.play(Write(explain9))
        
        # Apply rotation
        rotation_matrix = [[0, -1], [1, 0]]
        
        self.play(
            plane9.animate.apply_matrix(rotation_matrix),
            rotate_v.animate.apply_matrix(rotation_matrix),
            run_time=3
        )
        
        # Show where it went
        rotated_label = MathTex(r"A\vec{v}", color=ORANGE).next_to(rotate_v.get_end(), LEFT, buff=0.1)
        
        # Dashed original
        dashed_original = DashedLine(ORIGIN, [2, 0, 0], color=GRAY)
        self.play(Create(dashed_original), Transform(rotate_label, rotated_label))
        
        key9 = Text("Every vector changes direction!", font_size=26, color=RED)
        key9.to_edge(DOWN)
        self.play(Transform(explain9, key9))
        
        complex_note = MathTex(r"\text{Eigenvalues are complex: } \lambda = \pm i", font_size=28, color=GREEN)
        complex_note.move_to(DOWN * 2)
        self.play(Write(complex_note))
        self.wait(1.5)
        
        self.clear()

        # ============================================
        # SCENE 10: Summary and key takeaways
        # ============================================
        
        title10 = Text("Summary: Eigenvectors & Eigenvalues", font_size=36)
        title10.to_edge(UP)
        self.play(Write(title10))
        
        # Create summary boxes
        box1 = RoundedRectangle(corner_radius=0.2, width=6, height=1.8, color=BLUE)
        box1.move_to(UP * 1.5)
        box1_content = VGroup(
            MathTex(r"A\vec{v} = \lambda \vec{v}", font_size=32),
            Text("Eigenvector equation", font_size=22)
        ).arrange(DOWN, buff=0.2)
        box1_content.move_to(box1.get_center())
        
        self.play(Create(box1), Write(box1_content))
        
        box2 = RoundedRectangle(corner_radius=0.2, width=6, height=1.8, color=GREEN)
        box2.move_to(DOWN * 0.5)
        box2_content = VGroup(
            Text("Eigenvectors: directions preserved", font_size=22),
            Text("by linear transformation", font_size=22),
            MathTex(r"\text{Eigenvalue } \lambda \text{: scaling factor}", font_size=24)
        ).arrange(DOWN, buff=0.15)
        box2_content.move_to(box2.get_center())
        
        self.play(Create(box2), Write(box2_content))
        
        # Applications
        apps_title = Text("Applications", font_size=28, color=YELLOW)
        apps_title.move_to(DOWN * 2.5)
        self.play(Write(apps_title))
        
        apps = VGroup(
            Text("• Physics: principal axes of rotation", font_size=20),
            Text("• Data Science: PCA for dimensionality reduction", font_size=20),
            Text("• Engineering: stability analysis", font_size=20),
            Text("• Google's PageRank algorithm", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        apps.move_to(DOWN * 3.5)
        
        self.play(Write(apps), run_time=2)
        self.wait(1)
        
        # Final emphasis
        final = MathTex(r"\text{Eigenvectors } = \text{ Natural directions of a matrix}", font_size=32, color=YELLOW)
        final.to_edge(DOWN)
        self.play(Write(final))
        self.wait(2)
        
        self.clear()
