from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: The concept of vectors as arrows and how transformations act on them
        title_1 = Text("Step 1: Vectors & Transformations", font_size=36).to_edge(UP)
        self.play(Write(title_1))
        
        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-4, 4, 1], background_line_style={"stroke_color": BLUE_D, "stroke_width": 1, "stroke_opacity": 0.5})
        self.play(FadeIn(plane))
        
        # A standard vector
        vec_1 = Vector([2, 1], color=YELLOW)
        label_1 = MathTex(r"\vec{v} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}", color=YELLOW).next_to(vec_1, RIGHT)
        self.play(GrowArrow(vec_1), Write(label_1))
        self.wait(1)
        
        # Introduce a transformation matrix
        matrix_A = MathTex(r"A = \begin{bmatrix} 2 & 1 \\ 0 & 2 \end{bmatrix}").to_edge(LEFT).shift(DOWN)
        self.play(Write(matrix_A))
        self.wait(0.5)
        
        # Apply the transformation to the plane and the vector
        matrix = [[2, 1], [0, 2]]
        transform_title = Text("Applying transformation A...", font_size=28, color=RED).next_to(title_1, DOWN)
        self.play(Write(transform_title))
        self.play(
            ApplyMatrix(matrix, plane),
            vec_1.animate.apply_matrix(matrix),
            label_1.animate.next_to(vec_1.get_end(), RIGHT, buff=0.2).apply_matrix(matrix), # Keep label with vector
            run_time=2
        )
        self.wait(1)
        
        explanation_1 = Text("A transformation changes the vector's direction and length.", font_size=24, color=GREEN).to_edge(DOWN)
        self.play(Write(explanation_1))
        self.wait(2)
        
        self.clear()
        
        # Scene 2: Introduce the idea of a special vector - the eigenvector
        title_2 = Text("Step 2: The Special Vector", font_size=36).to_edge(UP)
        self.play(Write(title_2))
        
        plane2 = NumberPlane(x_range=[-4, 4, 1], y_range=[-4, 4, 1], background_line_style={"stroke_color": BLUE_D, "stroke_width": 1, "stroke_opacity": 0.5})
        self.play(FadeIn(plane2))
        
        # This vector lies on an eigenspace
        vec_e = Vector([1, 0], color=YELLOW)
        label_e = MathTex(r"\vec{v}_e = \begin{bmatrix} 1 \\ 0 \end{bmatrix}", color=YELLOW).next_to(vec_e, RIGHT)
        self.play(GrowArrow(vec_e), Write(label_e))
        self.wait(1)
        
        hint_text = Text("What if a vector's direction didn't change?", font_size=28, color=GREEN).to_edge(DOWN)
        self.play(Write(hint_text))
        self.wait(2)
        
        # Apply the same transformation
        self.play(
            ApplyMatrix(matrix, plane2),
            vec_e.animate.apply_matrix(matrix),
            label_e.animate.next_to(vec_e.get_end(), RIGHT, buff=0.2).apply_matrix(matrix),
            run_time=2
        )
        self.wait(1)
        
        highlight_text = Text("It only stretched! It stayed on the same line.", font_size=28, color=ORANGE).to_edge(DOWN)
        self.play(Transform(hint_text, highlight_text))
        self.wait(2)
        
        self.clear()
        
        # Scene 3: Define the eigenvector and eigenvalue formally
        title_3 = Text("Step 3: The Eigenvector Equation", font_size=36).to_edge(UP)
        self.play(Write(title_3))
        
        definition = MathTex(r"A\vec{v} = \lambda\vec{v}", font_size=60).shift(UP*1.5)
        self.play(Write(definition))
        self.wait(1)
        
        # Breakdown the equation
        part_A = definition[0][0:2]
        part_v = definition[0][2]
        part_eq = definition[0][3]
        part_lambda = definition[0][4]
        part_v2 = definition[0][5]
        
        explanation_A = Text("Matrix", font_size=24).next_to(part_A, DOWN, buff=0.5)
        explanation_v = Text("Vector", font_size=24).next_to(part_v, DOWN, buff=0.5)
        explanation_lambda = Text("Scalar", font_size=24).next_to(part_lambda, DOWN, buff=0.5)
        
        self.play(
            FadeIn(explanation_A),
            FadeIn(explanation_v),
            FadeIn(explanation_lambda)
        )
        self.wait(1)
        
        full_text = Text("If this equation holds, then:", font_size=28).shift(DOWN*1.5)
        self.play(Write(full_text))
        self.wait(0.5)
        
        bullet1 = Text("- v is an eigenvector", font_size=24, color=YELLOW).next_to(full_text, DOWN, buff=0.3).align_to(full_text, LEFT)
        bullet2 = Text("- λ (lambda) is the eigenvalue", font_size=24, color=RED).next_to(bullet1, DOWN, buff=0.2).align_to(bullet1, LEFT)
        self.play(Write(bullet1))
        self.play(Write(bullet2))
        self.wait(2)
        
        self.clear()
        
        # Scene 4: Geometric interpretation with multiple eigenvectors
        title_4 = Text("Step 4: Visualizing Eigenvalues", font_size=36).to_edge(UP)
        self.play(Write(title_4))
        
        plane4 = NumberPlane(x_range=[-5, 5, 1], y_range=[-5, 5, 1], background_line_style={"stroke_color": BLUE_D, "stroke_width": 1, "stroke_opacity": 0.5})
        self.play(FadeIn(plane4))
        
        # Create a matrix with distinct eigenvectors
        matrix_B = [[3, 0], [0, 2]]
        
        # First eigenvector (along x-axis, eigenvalue 3)
        vec_e1 = Vector([1, 0], color=YELLOW)
        label_e1 = MathTex(r"\vec{v}_1", color=YELLOW).next_to(vec_e1, UP)
        self.play(GrowArrow(vec_e1), Write(label_e1))
        
        # Second eigenvector (along y-axis, eigenvalue 2)
        vec_e2 = Vector([0, 1], color=GREEN)
        label_e2 = MathTex(r"\vec{v}_2", color=GREEN).next_to(vec_e2, LEFT)
        self.play(GrowArrow(vec_e2), Write(label_e2))
        
        # A non-eigenvector
        vec_other = Vector([1, 1], color=RED)
        label_other = MathTex(r"\vec{u}", color=RED).next_to(vec_other, UR, buff=0.1)
        self.play(GrowArrow(vec_other), Write(label_other))
        self.wait(1)
        
        # Apply transformation
        transform_title_4 = Text("Applying A = [[3,0],[0,2]]", font_size=28, color=ORANGE).to_edge(DOWN)
        self.play(Write(transform_title_4))
        self.play(
            ApplyMatrix(matrix_B, plane4),
            vec_e1.animate.apply_matrix(matrix_B),
            label_e1.animate.next_to(vec_e1.get_end(), UP),
            vec_e2.animate.apply_matrix(matrix_B),
            label_e2.animate.next_to(vec_e2.get_end(), LEFT),
            vec_other.animate.apply_matrix(matrix_B),
            label_other.animate.next_to(vec_other.get_end(), UR, buff=0.1),
            run_time=3
        )
        self.wait(1)
        
        explanation_4 = Text("Eigenvectors stay on their axis lines, others don't.", font_size=24, color=WHITE).to_edge(DOWN)
        self.play(Transform(transform_title_4, explanation_4))
        self.wait(2)
        
        self.clear()
        
        # Scene 5: How to find eigenvalues (det(A - λI) = 0)
        title_5 = Text("Step 5: Finding Eigenvalues", font_size=36).to_edge(UP)
        self.play(Write(title_5))
        
        eq1 = MathTex(r"A\vec{v} = \lambda\vec{v}").shift(UP*2)
        self.play(Write(eq1))
        self.wait(0.5)
        
        eq2 = MathTex(r"A\vec{v} - \lambda\vec{v} = \vec{0}").next_to(eq1, DOWN, buff=0.5)
        self.play(Write(eq2))
        self.wait(0.5)
        
        eq3 = MathTex(r"(A - \lambda I)\vec{v} = \vec{0}").next_to(eq2, DOWN, buff=0.5)
        self.play(Write(eq3))
        self.wait(1)
        
        explanation_5 = Text("Since v is non-zero, (A - λI) must be singular.", font_size=28, color=YELLOW).next_to(eq3, DOWN, buff=1)
        self.play(Write(explanation_5))
        self.wait(1)
        
        eq4 = MathTex(r"\det(A - \lambda I) = 0", font_size=48, color=RED).next_to(explanation_5, DOWN, buff=0.7)
        self.play(Write(eq4))
        self.wait(1)
        
        summary = Text("This is the characteristic equation!", font_size=28, color=GREEN).next_to(eq4, DOWN, buff=0.5)
        self.play(Write(summary))
        self.wait(2)
        
        self.clear()
        
        # Scene 6: Example calculation of finding eigenvalues
        title_6 = Text("Step 6: Example Calculation", font_size=36).to_edge(UP)
        self.play(Write(title_6))
        
        matrix_ex = MathTex(r"A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}").shift(UP*2 + LEFT*3)
        self.play(Write(matrix_ex))
        self.wait(0.5)
        
        # Characteristic equation
        char_eq = MathTex(r"\det\left(\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix} - \lambda \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}\right) = 0").next_to(matrix_ex, DOWN, buff=0.5)
        self.play(Write(char_eq))
        self.wait(1)
        
        char_eq2 = MathTex(r"\det\begin{bmatrix} 2-\lambda & 1 \\ 1 & 2-\lambda \end{bmatrix} = 0").next_to(char_eq, DOWN, buff=0.5)
        self.play(Write(char_eq2))
        self.wait(1)
        
        char_eq3 = MathTex(r"(2-\lambda)^2 - 1 = 0").next_to(char_eq2, DOWN, buff=0.5)
        self.play(Write(char_eq3))
        self.wait(1)
        
        char_eq4 = MathTex(r"\lambda^2 - 4\lambda + 3 = 0").next_to(char_eq3, DOWN, buff=0.5)
        self.play(Write(char_eq4))
        self.wait(1)
        
        char_eq5 = MathTex(r"(\lambda - 1)(\lambda - 3) = 0", color=YELLOW).next_to(char_eq4, DOWN, buff=0.5)
        self.play(Write(char_eq5))
        self.wait(1)
        
        solution = MathTex(r"\lambda_1 = 1, \quad \lambda_2 = 3", color=GREEN).next_to(char_eq5, DOWN, buff=0.5)
        self.play(Write(solution))
        self.wait(2)
        
        self.clear()
        
        # Scene 7: Finding eigenvectors for a given eigenvalue
        title_7 = Text("Step 7: Finding Eigenvectors", font_size=36).to_edge(UP)
        self.play(Write(title_7))
        
        given = Text("Given λ₁ = 1, find v₁ such that Av₁ = 1·v₁", font_size=28).shift(UP*2)
        self.play(Write(given))
        self.wait(0.5)
        
        eq_setup = MathTex(r"\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix} \vec{v}_1 = \vec{v}_1").next_to(given, DOWN, buff=0.5)
        self.play(Write(eq_setup))
        self.wait(0.5)
        
        eq_r = MathTex(r"\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix} \vec{v}_1 - \vec{v}_1 = \vec{0}").next_to(eq_setup, DOWN, buff=0.5)
        self.play(Write(eq_r))
        self.wait(0.5)
        
        eq_r2 = MathTex(r"\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix} \vec{v}_1 = \vec{0}").next_to(eq_r, DOWN, buff=0.5)
        self.play(Write(eq_r2))
        self.wait(1)
        
        eq_r3 = MathTex(r"x_1 + x_2 = 0").next_to(eq_r2, DOWN, buff=0.5)
        self.play(Write(eq_r3))
        self.wait(1)
        
        solution_v = MathTex(r"\vec{v}_1 = t \begin{bmatrix} 1 \\ -1 \end{bmatrix}, \quad t \neq 0", color=YELLOW).next_to(eq_r3, DOWN, buff=0.7)
        self.play(Write(solution_v))
        self.wait(1)
        
        final_vec = MathTex(r"\text{For } t=1: \quad \vec{v}_1 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}", color=GREEN).next_to(solution_v, DOWN, buff=0.5)
        self.play(Write(final_vec))
        self.wait(2)
        
        self.clear()
        
        # Scene 8: Final summary - visualization of eigenvectors and eigenvalues
        title_8 = Text("Step 8: Putting It All Together", font_size=36).to_edge(UP)
        self.play(Write(title_8))
        
        plane8 = NumberPlane(x_range=[-5, 5, 1], y_range=[-5, 5, 1], background_line_style={"stroke_color": BLUE_D, "stroke_width": 1, "stroke_opacity": 0.5})
        self.play(FadeIn(plane8))
        
        # Use the matrix from the example
        matrix_C = [[2, 1], [1, 2]]
        
        # Plot eigenvectors (they are at 45 degree angles for this matrix)
        vec_v1 = Vector([1, -1], color=YELLOW)
        vec_v2 = Vector([1, 1], color=GREEN)
        self.play(GrowArrow(vec_v1), GrowArrow(vec_v2))
        
        label_v1 = MathTex(r"\vec{v}_1", color=YELLOW).next_to(vec_v1, DL, buff=0.1)
        label_v2 = MathTex(r"\vec{v}_2", color=GREEN).next_to(vec_v2, UR, buff=0.1)
        self.play(Write(label_v1), Write(label_v2))
        self.wait(1)
        
        info_text = Text("λ₁ = 1: No stretch along v₁", font_size=24, color=YELLOW).to_corner(DR)
        info_text2 = Text("λ₂ = 3: Stretches by 3 along v₂", font_size=24, color=GREEN).next_to(info_text, UP, buff=0.2)
        self.play(Write(info_text), Write(info_text2))
        self.wait(1)
        
        # Apply transformation to show the effect
        self.play(
            ApplyMatrix(matrix_C, plane8),
            vec_v1.animate.apply_matrix(matrix_C),
            label_v1.animate.next_to(vec_v1.get_end(), DL, buff=0.1),
            vec_v2.animate.apply_matrix(matrix_C),
            label_v2.animate.next_to(vec_v2.get_end(), UR, buff=0.1),
            run_time=3
        )
        self.wait(1)
        
        final_message = Text("Eigenvectors are the 'axes' of a linear transformation.", font_size=28, color=WHITE).to_edge(DOWN)
        self.play(Write(final_message))
        self.wait(3)
        
        self.clear()
