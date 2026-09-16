import numpy as np
from manim import *

class SceneGen(Scene):
    def construct(self):
        # --- SCENE 1: What is a Linear Transformation? ---
        title1 = Text("Lesson 1: Linear Transformations", font_size=36).to_edge(UP)
        grid1 = NumberPlane(
            x_range=[-5, 5], y_range=[-3, 3],
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1, "stroke_opacity": 0.5}
        )
        vec1 = Arrow(grid1.c2p(0, 0), grid1.c2p(1, 1), buff=0, color=YELLOW)
        label1 = MathTex(r"\vec{v} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}", font_size=32).next_to(vec1.get_end(), UR)

        explanation1 = Text("A transformation moves every vector\nin a specific way.", font_size=24).to_edge(DOWN)

        # Define a transformation matrix
        matrix_A = [[1, 1], [0, 1]]
        transform_tex = MathTex(r"A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}", font_size=32).to_edge(LEFT + UP)

        self.play(Write(title1))
        self.play(Create(grid1))
        self.play(GrowArrow(vec1), Write(label1))
        self.play(Write(explanation1))
        self.wait(1)

        # Show the matrix
        self.play(Write(transform_tex))
        self.wait(0.5)

        # Apply transformation
        explanation2 = Text("Applying matrix A stretches\nand shears the space.", font_size=24).to_edge(DOWN)
        self.play(ReplacementTransform(explanation1, explanation2))

        grid1_target = grid1.copy().apply_matrix(matrix_A)
        vec1_target = vec1.copy().apply_matrix(matrix_A)

        self.play(
            Transform(grid1, grid1_target),
            Transform(vec1, vec1_target),
            label1.animate.next_to(vec1_target.get_end(), UR),
            run_time=3
        )
        self.wait(2)
        self.clear()

        # --- SCENE 2: The Question - Which Vectors Keep Their Direction? ---
        title2 = Text("Lesson 2: The Special Vectors", font_size=36).to_edge(UP)
        grid2 = NumberPlane(
            x_range=[-5, 5], y_range=[-3, 3],
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1, "stroke_opacity": 0.5}
        )
        # Use a simpler matrix for better visual clarity on eigenvectors
        matrix_B = [[2, 1], [0, 3]]

        # Random vectors
        vecs2 = VGroup(*[
            Arrow(grid2.c2p(0, 0), grid2.c2p(*v), buff=0, color=GREY_B)
            for v in [(1, 2), (2, -1), (-1, 0.5)]
        ])

        explanation2_1 = Text("After a transformation, most vectors\nchange their direction.", font_size=24).to_edge(DOWN)

        self.play(Write(title2), Create(grid2))
        self.play(LaggedStart(*[GrowArrow(v) for v in vecs2], lag_ratio=0.5))
        self.play(Write(explanation2_1))
        self.wait(1)

        # Transform them
        vecs2_target = VGroup(*[
            v.copy().apply_matrix(matrix_B) for v in vecs2
        ])
        self.play(Transform(vecs2, vecs2_target), run_time=2)
        self.wait(1)

        # The big question
        question = Text("Are there any special vectors\nthat only scale, without rotating?", font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(ReplacementTransform(explanation2_1, question))
        self.wait(2)
        self.clear()

        # --- SCENE 3: Introducing the Eigenvector ---
        title3 = Text("Lesson 3: The Eigenvector", font_size=36).to_edge(UP)
        grid3 = NumberPlane(
            x_range=[-5, 5], y_range=[-3, 3],
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1, "stroke_opacity": 0.5}
        )
        # Eigenvector for [[2,1],[0,3]] is [1,0] (eigenvalue 2) and [1,2] (eigenvalue 3)
        evec1 = Arrow(grid3.c2p(0, 0), grid3.c2p(1, 0), buff=0, color=GREEN)
        evec1_label = MathTex(r"\vec{v}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}", font_size=30, color=GREEN).next_to(evec1, DOWN)

        explanation3_1 = Text("Yes! This is an eigenvector.", font_size=24).to_edge(DOWN)
        matrix_B_tex = MathTex(r"A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}", font_size=32).to_corner(UR)

        self.play(Write(title3), Create(grid3))
        self.play(GrowArrow(evec1), Write(evec1_label))
        self.play(Write(explanation3_1), Write(matrix_B_tex))
        self.wait(1)

        # Show it only scales
        explanation3_2 = Text("It changes only by a scalar factor.", font_size=24).to_edge(DOWN)
        evec1_scaled = Arrow(grid3.c2p(0, 0), grid3.c2p(2, 0), buff=0, color=GREEN)
        lambda_tex = MathTex(r"\lambda_1 = 2", font_size=30, color=RED).next_to(evec1_scaled, UP)

        self.play(ReplacementTransform(explanation3_1, explanation3_2))
        self.play(Transform(evec1, evec1_scaled), Write(lambda_tex))
        self.wait(1)

        # The equation
        eq = MathTex(r"A \vec{v} = \lambda \vec{v}", font_size=40).next_to(title3, DOWN)
        self.play(Write(eq))
        self.wait(2)
        self.clear()

        # --- SCENE 4: The Equation in Detail ---
        title4 = Text("Lesson 4: The Eigenvalue Equation", font_size=36).to_edge(UP)
        eq4 = MathTex(
            r"A \vec{v} &= \lambda \vec{v} \\",
            r"A \vec{v} - \lambda \vec{v} &= 0 \\",
            r"(A - \lambda I) \vec{v} &= 0",
            font_size=40
        )
        explanation4_1 = Text("For a non-zero v, this means\n(A - λI) must compress space.", font_size=24).to_edge(DOWN)

        self.play(Write(title4))
        self.play(Write(eq4[0]))
        self.wait(1)
        self.play(Write(eq4[1]))
        self.wait(1)
        self.play(Write(eq4[2]))
        self.play(Write(explanation4_1))
        self.wait(2)

        explanation4_2 = Text("This happens only if its\ndeterminant is zero.", font_size=24).to_edge(DOWN)
        det_eq = MathTex(r"\det(A - \lambda I) = 0", font_size=40, color=YELLOW).next_to(eq4, DOWN, buff=0.5)

        self.play(ReplacementTransform(explanation4_1, explanation4_2))
        self.play(Write(det_eq))
        self.wait(2)
        self.clear()

        # --- SCENE 5: Solving for Eigenvalues ---
        title5 = Text("Lesson 5: Finding Eigenvalues", font_size=36).to_edge(UP)
        matrix_C = [[4, 2], [1, 3]]
        matrix_C_tex = MathTex(r"A = \begin{bmatrix} 4 & 2 \\ 1 & 3 \end{bmatrix}", font_size=36).to_corner(UR)

        steps = VGroup(
            MathTex(r"\det\left( \begin{bmatrix} 4 & 2 \\ 1 & 3 \end{bmatrix} - \lambda \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \right) = 0", font_size=36),
            MathTex(r"\det\left( \begin{bmatrix} 4-\lambda & 2 \\ 1 & 3-\lambda \end{bmatrix} \right) = 0", font_size=36),
            MathTex(r"(4-\lambda)(3-\lambda) - (2)(1) = 0", font_size=36),
            MathTex(r"\lambda^2 - 7\lambda + 10 = 0", font_size=36),
            MathTex(r"(\lambda - 2)(\lambda - 5) = 0", font_size=36),
            MathTex(r"\lambda_1 = 2, \quad \lambda_2 = 5", font_size=36, color=YELLOW),
        ).arrange(DOWN, buff=0.4).next_to(title5, DOWN, buff=0.5)

        self.play(Write(title5), Write(matrix_C_tex))
        for step in steps:
            self.play(Write(step))
            self.wait(1)

        explanation5 = Text("We found the eigenvalues!", font_size=24).to_edge(DOWN)
        self.play(Write(explanation5))
        self.wait(2)
        self.clear()

        # --- SCENE 6: Finding Eigenvectors ---
        title6 = Text("Lesson 6: Finding Eigenvectors", font_size=36).to_edge(UP)
        explanation6_1 = Text("Now substitute each λ back\ninto (A - λI)v = 0", font_size=24).to_edge(DOWN)

        # For λ = 2
        lambda_2_steps = VGroup(
            MathTex(r"\lambda = 2:", font_size=32, color=GREEN),
            MathTex(r"\begin{bmatrix} 4-2 & 2 \\ 1 & 3-2 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}", font_size=32),
            MathTex(r"\begin{bmatrix} 2 & 2 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}", font_size=32),
            MathTex(r"x + y = 0 \implies y = -x", font_size=32),
            MathTex(r"\vec{v}_1 = c \begin{bmatrix} 1 \\ -1 \end{bmatrix}", font_size=32, color=GREEN),
        ).arrange(DOWN, buff=0.3).shift(LEFT * 3)

        self.play(Write(title6))
        self.play(Write(explanation6_1))
        self.wait(0.5)
        for step in lambda_2_steps:
            self.play(Write(step))
            self.wait(0.5)

        # For λ = 5
        lambda_5_steps = VGroup(
            MathTex(r"\lambda = 5:", font_size=32, color=RED),
            MathTex(r"\begin{bmatrix} 4-5 & 2 \\ 1 & 3-5 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}", font_size=32),
            MathTex(r"\begin{bmatrix} -1 & 2 \\ 1 & -2 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}", font_size=32),
            MathTex(r"-x + 2y = 0 \implies x = 2y", font_size=32),
            MathTex(r"\vec{v}_2 = c \begin{bmatrix} 2 \\ 1 \end{bmatrix}", font_size=32, color=RED),
        ).arrange(DOWN, buff=0.3).shift(RIGHT * 3)

        for step in lambda_5_steps:
            self.play(Write(step))
            self.wait(0.5)

        self.wait(2)
        self.clear()

        # --- SCENE 7: Visual Confirmation ---
        title7 = Text("Lesson 7: Visual Confirmation", font_size=36).to_edge(UP)
        grid7 = NumberPlane(
            x_range=[-6, 6], y_range=[-4, 4],
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1, "stroke_opacity": 0.5}
        )
        matrix_C = np.array([[4, 2], [1, 3]])

        # Eigenvectors (unnormalized)
        evec2 = Arrow(grid7.c2p(0, 0), grid7.c2p(1, -1), buff=0, color=GREEN)
        evec5 = Arrow(grid7.c2p(0, 0), grid7.c2p(2, 1), buff=0, color=RED)

        evec2_label = MathTex(r"\vec{v}_1", color=GREEN).next_to(evec2.get_end(), DR)
        evec5_label = MathTex(r"\vec{v}_2", color=RED).next_to(evec5.get_end(), UL)

        # Regular vector
        reg_vec = Arrow(grid7.c2p(0, 0), grid7.c2p(1, 1), buff=0, color=YELLOW)
        reg_label = MathTex(r"\vec{u}", color=YELLOW).next_to(reg_vec.get_end(), UL)

        explanation7_1 = Text("Let's transform the space and\nwatch what happens to these vectors.", font_size=24).to_edge(DOWN)

        self.play(Write(title7), Create(grid7))
        self.play(GrowArrow(evec2), Write(evec2_label))
        self.play(GrowArrow(evec5), Write(evec5_label))
        self.play(GrowArrow(reg_vec), Write(reg_label))
        self.play(Write(explanation7_1))
        self.wait(1)

        # Apply transformation
        explanation7_2 = Text("Eigenvectors stay on their span!\nOthers do not.", font_size=24).to_edge(DOWN)

        grid7_target = grid7.copy().apply_matrix(matrix_C)
        evec2_target = evec2.copy().apply_matrix(matrix_C)
        evec5_target = evec5.copy().apply_matrix(matrix_C)
        reg_vec_target = reg_vec.copy().apply_matrix(matrix_C)

        # Highlight that eigenvectors scale
        trace2 = DashedLine(grid7.c2p(0, 0), grid7.c2p(2, -2), color=GREEN, stroke_width=2)
        trace5 = DashedLine(grid7.c2p(0, 0), grid7.c2p(10, 5), color=RED, stroke_width=2)

        self.play(Create(trace2), Create(trace5))
        self.play(
            ReplacementTransform(explanation7_1, explanation7_2),
            Transform(grid7, grid7_target),
            Transform(evec2, evec2_target),
            Transform(evec5, evec5_target),
            Transform(reg_vec, reg_vec_target),
            run_time=3
        )

        # Update labels to follow
        self.play(
            evec2_label.animate.next_to(evec2.get_end(), DR),
            evec5_label.animate.next_to(evec5.get_end(), UL),
            reg_label.animate.next_to(reg_vec.get_end(), UL),
        )
        self.wait(3)
        self.clear()

        # --- SCENE 8: Summary ---
        title8 = Text("Summary: Eigenvectors & Eigenvalues", font_size=36).to_edge(UP)

        summary_points = VGroup(
            Text("1. An eigenvector v of matrix A doesn't change\n   direction when A is applied.", font_size=24),
            Text("2. It only gets scaled by its eigenvalue λ.", font_size=24),
            Text("3. This is described by: A·v = λ·v", font_size=24),
            Text("4. To find λ, solve det(A - λI) = 0.", font_size=24),
            Text("5. To find v, solve (A - λI)v = 0.", font_size=24),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(DOWN * 0.5)

        self.play(Write(title8))
        for point in summary_points:
            self.play(Write(point))
            self.wait(1.5)

        final_message = Text("They reveal the fundamental axes of a transformation.", font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(Write(final_message))
        self.wait(3)
        self.clear()
