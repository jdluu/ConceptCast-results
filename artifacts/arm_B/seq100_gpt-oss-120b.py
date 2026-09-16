from manim import *
import numpy as np


class SceneGen(Scene):
    def construct(self):
        # Scene 1: Coordinate plane and basis vectors
        ax = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            axis_config={"include_numbers": True},
        )
        i_vec = Arrow(start=ORIGIN, end=RIGHT, buff=0, color=RED)
        j_vec = Arrow(start=ORIGIN, end=UP, buff=0, color=BLUE)
        i_label = MathTex(r"\mathbf{e}_1").next_to(i_vec.get_end(), DOWN)
        j_label = MathTex(r"\mathbf{e}_2").next_to(j_vec.get_end(), LEFT)
        title = Title(r"Eigenvectors and Eigenvalues", font_size=48)

        self.play(Create(ax), Write(title))
        self.play(Create(i_vec), Write(i_label))
        self.play(Create(j_vec), Write(j_label))
        self.wait(1)

        self.clear()

        # Scene 2: Introduce matrix A and its action on vectors
        mat = MathTex(r"A = \begin{pmatrix}2 & 1\\ 1 & 2\end{pmatrix}", font_size=36)
        desc = Text("A linear transformation in the plane", font_size=28).next_to(mat, DOWN)

        self.play(Write(mat), Write(desc))
        self.wait(1)

        ax2 = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            axis_config={"include_numbers": True},
        )
        self.play(Create(ax2))
        vec_a = Arrow(start=ORIGIN, end=2 * RIGHT + UP, buff=0, color=YELLOW)
        vec_b = Arrow(start=ORIGIN, end=RIGHT + 2 * UP, buff=0, color=GREEN)
        self.play(Create(vec_a), Create(vec_b))
        self.wait(0.5)

        # Images under A
        A = np.array([[2, 1], [1, 2]])
        Av_a = A @ np.array([2, 1])
        Av_b = A @ np.array([1, 2])
        vec_a_target = Arrow(
            start=ORIGIN,
            end=Av_a[0] * RIGHT + Av_a[1] * UP,
            buff=0,
            color=YELLOW,
        )
        vec_b_target = Arrow(
            start=ORIGIN,
            end=Av_b[0] * RIGHT + Av_b[1] * UP,
            buff=0,
            color=GREEN,
        )

        self.play(Transform(vec_a, vec_a_target), Transform(vec_b, vec_b_target))
        self.wait(1)

        self.clear()

        # Scene 3: An arbitrary vector changes direction
        ax3 = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"include_numbers": True},
        )
        self.play(Create(ax3))
        arb = Arrow(start=ORIGIN, end=3 * RIGHT + UP, buff=0, color=ORANGE)
        self.play(Create(arb))
        self.wait(0.5)

        trans_text = Text("Apply A", font_size=30).next_to(ax3, UP)
        self.play(Write(trans_text))
        Av_arb = A @ np.array([3, 1])
        arb_target = Arrow(
            start=ORIGIN,
            end=Av_arb[0] * RIGHT + Av_arb[1] * UP,
            buff=0,
            color=ORANGE,
        )
        self.play(Transform(arb, arb_target))
        self.wait(1)

        self.clear()

        # Scene 4: Vectors that keep their direction – eigenvectors
        ax4 = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"include_numbers": True},
        )
        self.play(Create(ax4))
        # (1,1) and (1,-1) are eigenvectors of A
        eig1 = Arrow(start=ORIGIN, end=RIGHT + UP, buff=0, color=PURPLE)
        eig2 = Arrow(start=ORIGIN, end=RIGHT - UP, buff=0, color=PURPLE)
        self.play(Create(eig1), Create(eig2))
        self.wait(0.5)

        # Show scaling by eigenvalues λ₁=3 and λ₂=1
        eig1_target = Arrow(start=ORIGIN, end=3 * RIGHT + 3 * UP, buff=0, color=PURPLE)
        eig2_target = Arrow(start=ORIGIN, end=RIGHT - UP, buff=0, color=PURPLE)  # unchanged length
        self.play(Transform(eig1, eig1_target), Transform(eig2, eig2_target))
        self.wait(1)

        self.clear()

        # Scene 5: Formal definition
        definition = MathTex(
            r"\text{Eigenvector } \mathbf{v}\neq\mathbf{0}\text{ satisfies } A\mathbf{v}= \lambda \mathbf{v}",
            font_size=36,
        ).to_edge(UP)
        explanation = Text(
            "λ is the eigenvalue – the factor by which the vector is stretched.",
            font_size=28,
        ).next_to(definition, DOWN)

        self.play(Write(definition), Write(explanation))
        self.wait(2)

        self.clear()

        # Scene 6: Visual summary with eigenvectors of A
        ax6 = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"include_numbers": True},
        )
        self.play(Create(ax6))
        ev1 = Arrow(start=ORIGIN, end=RIGHT + UP, buff=0, color=GOLD)
        ev2 = Arrow(start=ORIGIN, end=RIGHT - UP, buff=0, color=GOLD)
        ev1_label = MathTex(r"\mathbf{v}_1").next_to(ev1.get_end(), UP + RIGHT)
        ev2_label = MathTex(r"\mathbf{v}_2").next_to(ev2.get_end(), DOWN + RIGHT)
        self.play(Create(ev1), Write(ev1_label))
        self.play(Create(ev2), Write(ev2_label))
        self.wait(0.5)

        ev1_img = Arrow(start=ORIGIN, end=3 * RIGHT + 3 * UP, buff=0, color=GOLD)
        ev2_img = Arrow(start=ORIGIN, end=RIGHT - UP, buff=0, color=GOLD)
        lambda1 = MathTex(r"\lambda_1 = 3").next_to(ev1_img.get_end(), UR)
        lambda2 = MathTex(r"\lambda_2 = 1").next_to(ev2_img.get_end(), DR)

        self.play(Transform(ev1, ev1_img), Transform(ev2, ev2_img))
        self.play(Write(lambda1), Write(lambda2))
        self.wait(2)

        final = Title(
            "Every vector is a combination of eigenvectors", font_size=30
        ).to_edge(DOWN)
        self.play(FadeIn(final))
        self.wait(2)
