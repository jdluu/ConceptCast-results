from manim import *

class SceneGen(Scene):
    def construct(self):
        # --------------------------------------------------------------
        # Scene 1: Introduce vectors and linear transformations
        # --------------------------------------------------------------
        title1 = Text("Eigenvectors & Eigenvalues", font_size=48)
        subtitle1 = Text("Part 1: Vectors and Linear Transformations", font_size=28, color=BLUE)
        VGroup(title1, subtitle1).arrange(DOWN, buff=0.3)
        self.play(Write(title1), Write(subtitle1))
        self.wait(1)

        axes = Axes(x_range=[-3, 3], y_range=[-3, 3], axis_config={"include_numbers": True})
        axes_center = axes.get_center()
        self.play(Create(axes), title1.animate.to_edge(UP), subtitle1.animate.to_edge(UP, buff=0.6).scale(0.6))

        vec = Arrow(axes.c2p(0,0), axes.c2p(2,1), color=YELLOW)
        vec_label = MathTex("\\vec{v} = (2,1)", color=YELLOW).next_to(vec.get_end(), RIGHT, buff=0.2)
        self.play(GrowArrow(vec), Write(vec_label))
        self.wait(0.5)

        matrix = [[1, -1], [1, 1]]
        transform_text = MathTex("T(\\vec{v}) = \\begin{pmatrix}1 & -1\\\\1 & 1\\end{pmatrix}\\vec{v}", font_size=36)
        transform_text.next_to(axes, RIGHT, buff=0.5)
        self.play(Write(transform_text))
        self.wait(0.5)

        new_vec = Arrow(axes.c2p(0,0), axes.c2p(1,3), color=ORANGE)
        new_label = MathTex("T(\\vec{v}) = (1,3)", color=ORANGE).next_to(new_vec.get_end(), RIGHT, buff=0.2)
        self.play(Transform(vec, new_vec), Transform(vec_label, new_label))
        self.wait(1)
        self.clear()

        # --------------------------------------------------------------
        # Scene 2: Show that some vectors only scale
        # --------------------------------------------------------------
        title2 = Text("Part 2: Vectors that only SCALE", font_size=42, color=BLUE)
        self.play(Write(title2))
        self.wait(0.5)
        self.play(title2.animate.to_edge(UP))

        axes2 = Axes(x_range=[-3, 3], y_range=[-3, 3], axis_config={"include_numbers": True})
        self.play(Create(axes2))

        # Show a special vector (1,0) under same transformation
        v_special = Arrow(axes2.c2p(0,0), axes2.c2p(1,0), color=YELLOW, buff=0)
        label_special = MathTex("\\vec{u} = (1,0)", color=YELLOW).next_to(v_special.get_end(), UR, buff=0.2)
        self.play(GrowArrow(v_special), Write(label_special))

        # Apply transformation: (1,0) -> (1,1) -> not pure scaling
        v_transformed = Arrow(axes2.c2p(0,0), axes2.c2p(1,1), color=ORANGE, buff=0)
        label_trans = MathTex("T(\\vec{u}) = (1,1)", color=ORANGE).next_to(v_transformed.get_end(), UR, buff=0.2)
        self.wait(0.3)
        self.play(Transform(v_special, v_transformed), Transform(label_special, label_trans))
        self.wait(0.5)

        # Now show a vector (1, 0.414) that approximately scales? Better use exact eigenvector: (1, 1) -> (1, -1) no. Use matrix [[2,0],[0,3]] for simplicity
        # Let's change matrix for clarity: use diagonal matrix so eigenvectors are obvious
        self.clear()
        title2b = Text("Part 2 (cont): Diagonal Transformation Example", font_size=36, color=BLUE)
        self.play(Write(title2b))
        self.wait(0.5)
        self.play(title2b.animate.to_edge(UP))

        axes2b = Axes(x_range=[-3, 3], y_range=[-3, 3], axis_config={"include_numbers": True})
        self.play(Create(axes2b))

        # Use matrix [[2,0],[0,3]] -> eigenvectors are (1,0) and (0,1)
        v_eig = Arrow(axes2b.c2p(0,0), axes2b.c2p(1.5,0), color=YELLOW, buff=0)
        label_eig = MathTex("\\vec{e}_1 = (1.5, 0)", color=YELLOW).next_to(v_eig.get_end(), UR, buff=0.2)
        self.play(GrowArrow(v_eig), Write(label_eig))

        # Transform: (1.5,0) -> (3,0) (scaled by 2)
        v_scaled = Arrow(axes2b.c2p(0,0), axes2b.c2p(3,0), color=GREEN, buff=0)
        label_scaled = MathTex("T(\\vec{e}_1) = (3,0) = 2 \\cdot \\vec{e}_1", color=GREEN).next_to(v_scaled.get_end(), UR, buff=0.2)
        self.play(Transform(v_eig, v_scaled), Transform(label_eig, label_scaled))
        self.wait(1)
        self.clear()

        # --------------------------------------------------------------
        # Scene 3: Define eigenvector and eigenvalue formally
        # --------------------------------------------------------------
        title3 = Text("Definition: Eigenvector & Eigenvalue", font_size=42, color=BLUE)
        self.play(Write(title3))
        self.wait(0.5)
        self.play(title3.animate.to_edge(UP))

        defn = MathTex(r"T(\vec{v}) = \lambda \vec{v}", font_size=48)
        defn_sub = MathTex(r"\vec{v} \neq 0, \quad \lambda \in \mathbb{R}", font_size=32)
        group_defn = VGroup(defn, defn_sub).arrange(DOWN, buff=0.3)
        self.play(Write(defn), Write(defn_sub))
        self.wait(1)

        highlight1 = SurroundingRectangle(defn[0][1:4], color=YELLOW, buff=0.1)
        highlight2 = SurroundingRectangle(defn[0][5:], color=GREEN, buff=0.1)
        self.play(Create(highlight1), Create(highlight2))
        self.wait(0.5)
        self.play(FadeOut(highlight1), FadeOut(highlight2))

        explain = Text(
            "Non-zero vector that only scales\nunder the transformation.",
            font_size=28, color=YELLOW
        ).next_to(group_defn, DOWN, buff=0.5)
        self.play(Write(explain))
        self.wait(1)
        self.clear()

        # --------------------------------------------------------------
        # Scene 4: Geometric intuition - eigenvector stays on same line
        # --------------------------------------------------------------
        title4 = Text("Geometric Intuition: Stays on the same line", font_size=36, color=BLUE)
        self.play(Write(title4))
        self.wait(0.5)
        self.play(title4.animate.to_edge(UP))

        axes4 = Axes(x_range=[-4, 4], y_range=[-4, 4], axis_config={"include_numbers": True})
        self.play(Create(axes4))

        # Draw a line through origin
        line = Line(axes4.c2p(-3, -1.5), axes4.c2p(3, 1.5), color=PURPLE, stroke_width=2)
        self.play(Create(line))
        line_label = Text("Eigenspace (line of eigenvectors)", font_size=22, color=PURPLE).next_to(line.get_center(), RIGHT, buff=0.3)
        self.play(Write(line_label))

        # Original vector on this line
        v_orig = Arrow(axes4.c2p(0,0), axes4.c2p(2,1), color=YELLOW, buff=0)
        label_orig = MathTex("\\vec{v}", color=YELLOW).next_to(v_orig.get_end(), UR, buff=0.1)
        self.play(GrowArrow(v_orig), Write(label_orig))

        # Transformed vector also on same line (scaled)
        v_new = Arrow(axes4.c2p(0,0), axes4.c2p(3.6,1.8), color=GREEN, buff=0)
        label_new = MathTex("T(\\vec{v}) = 1.8 \\vec{v}", color=GREEN).next_to(v_new.get_end(), UR, buff=0.1)
        self.play(Transform(v_orig, v_new), Transform(label_orig, label_new))
        self.wait(1)
        self.clear()

        # --------------------------------------------------------------
        # Scene 5: How to find eigenvectors - characteristic polynomial
        # --------------------------------------------------------------
        title5 = Text("Finding Eigenvectors: Characteristic Polynomial", font_size=36, color=BLUE)
        self.play(Write(title5))
        self.wait(0.5)
        self.play(title5.animate.to_edge(UP))

        eq1 = MathTex(r"\det(A - \lambda I) = 0", font_size=42)
        eq2 = MathTex(r"\begin{pmatrix}2 & 0 \\ 0 & 3 \end{pmatrix} - \lambda \begin{pmatrix}1 & 0 \\ 0 & 1 \end{pmatrix}", font_size=36)
        eq3 = MathTex(r"\det\begin{pmatrix}2-\lambda & 0 \\ 0 & 3-\lambda \end{pmatrix} = 0", font_size=36)
        eq4 = MathTex(r"(2-\lambda)(3-\lambda) = 0 \Rightarrow \lambda = 2, 3", font_size=36)

        steps = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(eq1))
        self.wait(0.5)
        self.play(Write(eq2))
        self.wait(0.5)
        self.play(Write(eq3))
        self.wait(0.5)
        self.play(Write(eq4))
        self.wait(1)

        note = Text("Eigenvalues: 2 and 3", font_size=28, color=YELLOW).next_to(steps, DOWN, buff=0.4)
        self.play(Write(note))
        self.wait(1)
        self.clear()

        # --------------------------------------------------------------
        # Scene 6: Compute eigenvectors for each eigenvalue
        # --------------------------------------------------------------
        title6 = Text("Computing Eigenvectors", font_size=42, color=BLUE)
        self.play(Write(title6))
        self.wait(0.5)
        self.play(title6.animate.to_edge(UP))

        # For lambda=2
        step1 = MathTex(r"\lambda = 2: \quad (A - 2I)\vec{v} = 0", font_size=32)
        step2 = MathTex(r"\begin{pmatrix}0 & 0 \\ 0 & 1 \end{pmatrix} \vec{v} = 0 \Rightarrow \vec{v} = \begin{pmatrix}1 \\ 0 \end{pmatrix}", font_size=32)
        step3 = MathTex(r"\lambda = 3: \quad (A - 3I)\vec{v} = 0 \Rightarrow \vec{v} = \begin{pmatrix}0 \\ 1 \end{pmatrix}", font_size=32)

        form = VGroup(step1, step2, step3).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(step1), Write(step2))
        self.wait(1)
        self.play(Write(step3))
        self.wait(1)

        result_text = Text("Eigenvectors: (1,0) with eigenvalue 2\n(0,1) with eigenvalue 3", font_size=28, color=GREEN)
        result_text.next_to(form, DOWN, buff=0.5)
        self.play(Write(result_text))
        self.wait(1)
        self.clear()

        # --------------------------------------------------------------
        # Scene 7: Visualize both eigenvectors under transformation
        # --------------------------------------------------------------
        title7 = Text("Visualizing Both Eigenvectors", font_size=42, color=BLUE)
        self.play(Write(title7))
        self.wait(0.5)
        self.play(title7.animate.to_edge(UP))

        axes7 = Axes(x_range=[-4, 4], y_range=[-4, 4], axis_config={"include_numbers": True})
        self.play(Create(axes7))

        # x-axis eigenvector
        vx = Arrow(axes7.c2p(0,0), axes7.c2p(1.5,0), color=YELLOW, buff=0)
        label_vx = MathTex("(1.5,0)", color=YELLOW).next_to(vx.get_end(), DOWN, buff=0.1)
        self.play(GrowArrow(vx), Write(label_vx))

        # y-axis eigenvector
        vy = Arrow(axes7.c2p(0,0), axes7.c2p(0,2), color=ORANGE, buff=0)
        label_vy = MathTex("(0,2)", color=ORANGE).next_to(vy.get_end(), RIGHT, buff=0.1)
        self.play(GrowArrow(vy), Write(label_vy))

        self.wait(0.5)

        # Transform both: scale x by 2, y by 3
        vx_new = Arrow(axes7.c2p(0,0), axes7.c2p(3,0), color=GREEN, buff=0)
        label_vx_new = MathTex("(3,0) = 2 \\cdot (1.5,0)", color=GREEN).next_to(vx_new.get_end(), DOWN, buff=0.1)
        vy_new = Arrow(axes7.c2p(0,0), axes7.c2p(0,6), color=PINK, buff=0)  # off screen but okay
        # Use smaller scaling to keep on screen
        vx_new_small = Arrow(axes7.c2p(0,0), axes7.c2p(2.5,0), color=GREEN, buff=0)
        vy_new_small = Arrow(axes7.c2p(0,0), axes7.c2p(0,3), color=PINK, buff=0)

        self.play(
            Transform(vx, vx_new_small),
            Transform(vy, vy_new_small),
            Transform(label_vx, label_vx_new),
            Transform(label_vy, MathTex("(0,3) = 3 \\cdot (0,1)", color=PINK).next_to(vy_new_small.get_end(), RIGHT, buff=0.1))
        )
        self.wait(1.5)
        self.clear()

        # --------------------------------------------------------------
        # Scene 8: Real-world example - rotation (no real eigenvectors)
        # --------------------------------------------------------------
        title8 = Text("Counterexample: Rotation has NO real eigenvectors", font_size=36, color=RED)
        self.play(Write(title8))
        self.wait(0.5)
        self.play(title8.animate.to_edge(UP))

        axes8 = Axes(x_range=[-3, 3], y_range=[-3, 3], axis_config={"include_numbers": True})
        self.play(Create(axes8))

        v = Arrow(axes8.c2p(0,0), axes8.c2p(2,1), color=YELLOW, buff=0)
        label_v = MathTex("\\vec{v}", color=YELLOW).next_to(v.get_end(), UR, buff=0.1)
        self.play(GrowArrow(v), Write(label_v))

        # Rotate 90 degrees
        v_rot = Arrow(axes8.c2p(0,0), axes8.c2p(-1,2), color=ORANGE, buff=0)
        label_rot = MathTex("R_{90}(\\vec{v})", color=ORANGE).next_to(v_rot.get_end(), UL, buff=0.1)
        self.play(Transform(v, v_rot), Transform(label_v, label_rot))
        self.wait(0.5)

        explanation = Text(
            "No scaling factor makes this work -\nvector changes direction!",
            font_size=24, color=RED
        ).next_to(axes8, DOWN, buff=0.5)
        self.play(Write(explanation))
        self.wait(1.5)
        self.clear()

        # --------------------------------------------------------------
        # Scene 9: Eigenbasis and diagonalization preview
        # --------------------------------------------------------------
        title9 = Text("Eigenbasis: A new coordinate system", font_size=36, color=BLUE)
        self.play(Write(title9))
        self.wait(0.5)
        self.play(title9.animate.to_edge(UP))

        axes9 = Axes(x_range=[-4, 4], y_range=[-4, 4], axis_config={"include_numbers": False})
        grid = NumberPlane(x_range=[-4,4,1], y_range=[-4,4,1])
        self.play(Create(grid), Create(axes9))

        # Show eigenvector directions as new axes
        eig_line1 = Line(axes9.c2p(-3,0), axes9.c2p(3,0), color=YELLOW, stroke_width=3)
        eig_line2 = Line(axes9.c2p(0,-3), axes9.c2p(0,3), color=ORANGE, stroke_width=3)
        self.play(Create(eig_line1), Create(eig_line2))

        labels = VGroup(
            Text("Eigenvector 1", font_size=20, color=YELLOW).next_to(axes9.c2p(3,0), RIGHT),
            Text("Eigenvector 2", font_size=20, color=ORANGE).next_to(axes9.c2p(0,3), UP)
        )
        self.play(Write(labels))
        self.wait(0.5)

        diag_text = MathTex(r"A = PDP^{-1}", font_size=42).to_edge(DOWN, buff=0.5)
        self.play(Write(diag_text))
        self.wait(1)
        self.clear()

        # --------------------------------------------------------------
        # Scene 10: Summary & conclusion
        # --------------------------------------------------------------
        title10 = Text("Summary: Eigenvectors & Eigenvalues", font_size=42, color=BLUE)
        self.play(Write(title10))
        self.wait(0.5)
        self.play(title10.animate.to_edge(UP))

        bullets = [
            "Non-zero vectors that only scale under T",
            "T(v) = λv : v is eigenvector, λ is eigenvalue",
            "Found by solving det(A - λI) = 0",
            "Eigenvectors define a natural coordinate system",
            "Used in PCA, quantum mechanics, vibration analysis"
        ]
        bullet_objs = []
        for i, b in enumerate(bullets):
            t = Text(b, font_size=28, color=YELLOW if i < 3 else BLUE)
            t.shift(UP * (1.5 - i * 0.7))
            bullet_objs.append(t)
            self.play(Write(t), run_time=0.8)
        self.wait(1)

        final = Text("Thanks for watching!", font_size=36, color=GREEN).to_edge(DOWN, buff=0.5)
        self.play(Write(final))
        self.wait(2)
        self.clear()
