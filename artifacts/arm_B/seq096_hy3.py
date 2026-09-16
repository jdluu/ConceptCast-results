from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Introduction to vectors
        axes = Axes(x_range=[-3, 3], y_range=[-3, 3], x_length=6, y_length=6, axis_config={"color": WHITE})
        vec = Arrow(ORIGIN, [2, 1, 0], color=YELLOW, buff=0)
        vec_lab = MathTex(r"\vec{v}").next_to(vec.get_end(), UR, buff=0.1)
        text = Text("A vector has direction and magnitude").to_edge(UP)
        self.play(Create(axes))
        self.play(GrowArrow(vec), Write(vec_lab))
        self.play(Write(text))
        self.wait(1)
        self.clear()

        # Scene 2: Linear transformation of space
        plane = NumberPlane(x_range=[-4, 4], y_range=[-4, 4], x_length=8, y_length=8)
        mat_tex = MathTex(r"A = \begin{bmatrix} 2 & 0 \\ 0 & 0.5 \end{bmatrix}").to_edge(UP)
        self.play(Create(plane))
        self.play(Write(mat_tex))
        self.wait(0.5)
        self.play(plane.animate.apply_matrix([[2, 0], [0, 0.5]]), run_time=2)
        self.wait(1)
        self.clear()

        # Scene 3: General vector changes direction
        axes = Axes(x_range=[-3, 3], y_range=[-3, 3], x_length=6, y_length=6, axis_config={"color": WHITE})
        v = Arrow(ORIGIN, [1, 2, 0], color=RED, buff=0)
        text = Text("Most vectors change direction under A").to_edge(UP)
        self.play(Create(axes), GrowArrow(v))
        self.play(Write(text))
        self.wait(0.5)
        v_new = Arrow(ORIGIN, [2, 1, 0], color=BLUE, buff=0)
        self.play(Transform(v, v_new), run_time=2)
        self.wait(1)
        self.clear()

        # Scene 4: Special vector stays on its line
        axes = Axes(x_range=[-4, 4], y_range=[-4, 4], x_length=6, y_length=6, axis_config={"color": WHITE})
        v = Arrow(ORIGIN, [2, 0, 0], color=GREEN, buff=0)
        text = Text("But vectors on the x-axis stay on their line").to_edge(UP)
        self.play(Create(axes), GrowArrow(v), Write(text))
        v_new = Arrow(ORIGIN, [4, 0, 0], color=GREEN, buff=0)
        self.play(Transform(v, v_new), run_time=2)
        self.wait(1)
        self.clear()

        # Scene 5: Eigenvalue as scalar factor
        axes = Axes(x_range=[-4, 4], y_range=[-4, 4], x_length=6, y_length=6, axis_config={"color": WHITE})
        v = Arrow(ORIGIN, [2, 0, 0], color=GREEN, buff=0)
        lam = MathTex(r"\lambda = 2").to_edge(UP)
        eq = MathTex(r"A\vec{v} = 2\vec{v}").to_edge(DOWN)
        self.play(Create(axes), GrowArrow(v), Write(lam), Write(eq))
        v_new = Arrow(ORIGIN, [4, 0, 0], color=GREEN, buff=0)
        self.play(Transform(v, v_new), run_time=2)
        self.wait(1)
        self.clear()

        # Scene 6: Two eigenvectors of a symmetric matrix
        axes = Axes(x_range=[-4, 4], y_range=[-4, 4], x_length=6, y_length=6, axis_config={"color": WHITE})
        mat_tex = MathTex(r"A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}").to_edge(UP)
        v1 = Arrow(ORIGIN, [1, 1, 0], color=YELLOW, buff=0)
        v2 = Arrow(ORIGIN, [1, -1, 0], color=PURPLE, buff=0)
        self.play(Create(axes), Write(mat_tex), GrowArrow(v1), GrowArrow(v2))
        v1b = Arrow(ORIGIN, [3, 3, 0], color=YELLOW, buff=0)
        v2b = Arrow(ORIGIN, [-1, 1, 0], color=PURPLE, buff=0)
        self.play(Transform(v1, v1b, run_time=2), Transform(v2, v2b, run_time=2))
        labels = MathTex(r"\lambda_1 = 3,\ \lambda_2 = -1").to_edge(DOWN)
        self.play(Write(labels))
        self.wait(1)
        self.clear()

        # Scene 7: Summary equation
        title = Text("Eigenvectors").to_edge(UP)
        eq = MathTex(r"A\vec{v} = \lambda\vec{v}").scale(1.5)
        note = Text("Non-zero vectors that only scale by a scalar (eigenvalue)").next_to(eq, DOWN)
        self.play(Write(title))
        self.play(Write(eq))
        self.play(Write(note))
        self.wait(2)
        self.clear()