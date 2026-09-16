from manim import *

class EigenvalueScene(Scene):
    def construct(self):
        # Title
        title = Text("Eigenvalues and Eigenvectors", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Introduction
        intro = Text("For a square matrix A, a scalar λ is an eigenvalue if there exists a non-zero vector v such that Av = λv.", font_size=24).next_to(title, DOWN, buff=0.5)
        self.play(Write(intro))
        self.wait(2)

        # Matrix A
        matrix_A = MathTex(r"A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}").next_to(intro, DOWN, buff=0.5)
        self.play(Write(matrix_A))
        self.wait(1)

        # Eigenvalue equation
        eq = MathTex(r"A \vec{v} = \lambda \vec{v}").next_to(matrix_A, DOWN, buff=0.5)
        self.play(Write(eq))
        self.wait(1)

        # Rewrite as (A - λI)v = 0
        rewrite = MathTex(r"(A - \lambda I) \vec{v} = \vec{0}").next_to(eq, DOWN, buff=0.5)
        self.play(Write(rewrite))
        self.wait(1)

        # Characteristic equation
        char_eq = MathTex(r"\det(A - \lambda I) = 0").next_to(rewrite, DOWN, buff=0.5)
        self.play(Write(char_eq))
        self.wait(1)

        # Compute A - λI
        A_minus_lambda_I = MathTex(r"A - \lambda I = \begin{pmatrix} 2-\lambda & 1 \\ 1 & 2-\lambda \end{pmatrix}").next_to(char_eq, DOWN, buff=0.5)
        self.play(Write(A_minus_lambda_I))
        self.wait(1)

        # Determinant
        det_eq = MathTex(r"\det\begin{pmatrix} 2-\lambda & 1 \\ 1 & 2-\lambda \end{pmatrix} = (2-\lambda)^2 - 1 = 0").next_to(A_minus_lambda_I, DOWN, buff=0.5)
        self.play(Write(det_eq))
        self.wait(1)

        # Solve for λ
        solve_eq = MathTex(r"\lambda^2 - 4\lambda + 3 = 0").next_to(det_eq, DOWN, buff=0.5)
        self.play(Write(solve_eq))
        self.wait(1)

        roots = MathTex(r"\lambda_1 = 3, \quad \lambda_2 = 1").next_to(solve_eq, DOWN, buff=0.5)
        self.play(Write(roots))
        self.wait(2)

        # Clear for eigenvectors
        self.play(FadeOut(VGroup(intro, matrix_A, eq, rewrite, char_eq, A_minus_lambda_I, det_eq, solve_eq, roots)))

        # Eigenvector for λ=3
        header = Text("Eigenvector for λ = 3", font_size=36).next_to(title, DOWN, buff=0.5)
        self.play(Write(header))

        system = MathTex(r"\begin{pmatrix} -1 & 1 \\ 1 & -1 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}").next_to(header, DOWN, buff=0.5)
        self.play(Write(system))
        self.wait(1)

        solution = MathTex(r"x = y").next_to(system, DOWN, buff=0.5)
        self.play(Write(solution))
        self.wait(1)

        v_e = MathTex(r"\vec{v} = \begin{pmatrix} 1 \\ 1 \end{pmatrix}").next_to(solution, DOWN, buff=0.5)
        self.play(Write(v_e))
        self.wait(2)

        # Clear for next eigenvector
        self.play(FadeOut(VGroup(header, system, solution, v_e)))

        # Eigenvector for λ=1
        header2 = Text("Eigenvector for λ = 1", font_size=36).next_to(title, DOWN, buff=0.5)
        self.play(Write(header2))

        system2 = MathTex(r"\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}").next_to(header2, DOWN, buff=0.5)
        self.play(Write(system2))
        self.wait(1)

        solution2 = MathTex(r"x = -y").next_to(system2, DOWN, buff=0.5)
        self.play(Write(solution2))
        self.wait(1)

        v_e2 = MathTex(r"\vec{v} = \begin{pmatrix} 1 \\ -1 \end{pmatrix}").next_to(solution2, DOWN, buff=0.5)
        self.play(Write(v_e2))
        self.wait(2)

        # Clear
        self.play(FadeOut(VGroup(header2, system2, solution2, v_e2)))

        # Conclusion
        conclusion = Text("The eigenvalues are 3 and 1, with corresponding eigenvectors (1,1) and (1,-1).", font_size=28).next_to(title, DOWN, buff=0.5)
        self.play(Write(conclusion))
        self.wait(2)

        # End
        self.play(FadeOut(VGroup(title, conclusion)))
        self.wait(1)
