import numpy as np
from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Pure sine wave
        axes1 = Axes(x_range=[0, 2*PI, PI], y_range=[-1.5, 1.5, 1], x_length=10, y_length=4)
        sine1 = axes1.plot(lambda x: np.sin(x), color=BLUE)
        label1 = Text("A pure tone: sin(t)").to_edge(UP)
        dot1 = Dot(color=RED).move_to(axes1.c2p(0, 0))
        self.play(Create(axes1), Write(label1))
        self.play(Create(sine1))
        self.play(MoveAlongPath(dot1, sine1), run_time=4, rate_func=linear)
        self.play(FadeOut(dot1))
        self.wait(0.5)
        self.clear()

        # Scene 2: Sum of two sines
        axes2 = Axes(x_range=[0, 2*PI, PI], y_range=[-2, 2, 1], x_length=10, y_length=4)
        s_a = axes2.plot(lambda x: np.sin(x), color=BLUE)
        s_b = axes2.plot(lambda x: 0.5*np.sin(3*x), color=GREEN)
        s_c = axes2.plot(lambda x: np.sin(x) + 0.5*np.sin(3*x), color=YELLOW)
        label2 = Text("Complex signal = sum of simple sines").to_edge(UP)
        self.play(Create(axes2), Write(label2))
        self.play(Create(s_a))
        self.play(Create(s_b))
        self.play(Create(s_c))
        self.wait(1)
        self.clear()

        # Scene 3: Rotating phasor
        label3 = Text("A sine wave is a rotating vector's projection").to_edge(UP)
        circ = Circle(radius=1.5).shift(LEFT*3)
        phasor = Arrow(circ.get_center(), circ.get_top(), color=YELLOW, buff=0)
        dot3 = Dot(circ.get_top(), color=RED)
        phasor_group = VGroup(phasor, dot3)
        self.play(Write(label3), Create(circ), Create(phasor_group))
        self.play(Rotate(phasor_group, angle=2*PI, about_point=circ.get_center(), run_time=4, rate_func=linear))
        self.wait(0.5)
        self.clear()

        # Scene 4: Two phasors tip-to-tail
        label4 = Text("Add rotating vectors tip-to-tail").to_edge(UP)
        origin = LEFT*4
        v1 = Arrow(origin, origin + RIGHT*1.5, color=RED, buff=0)
        v2 = Arrow(origin + RIGHT*1.5, origin + RIGHT*1.5 + UP*0.8, color=GREEN, buff=0)
        t_track = ValueTracker(0)
        def update_vecs(mob):
            ang = t_track.get_value()
            v1.put_start_and_end_on(origin, origin + 1.5*np.array([np.cos(ang), np.sin(ang), 0]))
            tip = v1.get_end()
            v2.put_start_and_end_on(tip, tip + 0.8*np.array([np.cos(3*ang), np.sin(3*ang), 0]))
        grp = VGroup(v1, v2)
        grp.add_updater(update_vecs)
        self.play(Write(label4), Create(grp))
        self.play(t_track.animate.set_value(2*PI), run_time=4, rate_func=linear)
        grp.clear_updaters()
        self.wait(0.5)
        self.clear()

        # Scene 5: Square wave approximation
        label5 = Text("Fourier series: build a square wave").to_edge(UP)
        axes5 = Axes(x_range=[-PI, PI, PI/2], y_range=[-1.5, 1.5, 1], x_length=8, y_length=4)
        square = axes5.plot(lambda x: np.sign(np.sin(x)), color=WHITE)
        approx = axes5.plot(lambda x: sum(np.sin((2*k-1)*x)/(2*k-1) for k in range(1, 6)), color=YELLOW)
        self.play(Write(label5), Create(axes5), Create(square))
        self.play(Create(approx), run_time=2)
        self.wait(1)
        self.clear()

        # Scene 6: Correlation
        label6 = Text("Correlate signal with cos(ωt) to find frequency").to_edge(UP)
        axes6 = Axes(x_range=[0, 2*PI, PI], y_range=[-2, 2, 1], x_length=10, y_length=4)
        sig = axes6.plot(lambda x: np.sin(x) + 0.5*np.sin(3*x), color=YELLOW)
        basis = axes6.plot(lambda x: np.cos(x), color=BLUE)
        prod = axes6.plot(lambda x: (np.sin(x) + 0.5*np.sin(3*x))*np.cos(x), color=RED)
        area = axes6.get_area(prod, x_range=[0, 2*PI], color=RED, opacity=0.4)
        self.play(Write(label6), Create(axes6), Create(sig), Create(basis))
        self.play(Create(prod))
        self.play(Create(area))
        self.wait(1)
        self.clear()

        # Scene 7: Spectrum
        label7 = Text("Fourier Transform: the frequency spectrum").to_edge(UP)
        axes7 = Axes(x_range=[0, 5, 1], y_range=[0, 1.5, 0.5], x_length=10, y_length=5)
        axes7_labels = VGroup(Text("Frequency").next_to(axes7.x_axis, DOWN), Text("Amplitude").next_to(axes7.y_axis, LEFT))
        bar1 = Rectangle(width=0.4, height=1.0, color=BLUE).move_to(axes7.c2p(1, 0.5))
        bar3 = Rectangle(width=0.4, height=0.5, color=GREEN).move_to(axes7.c2p(3, 0.25))
        self.play(Write(label7), Create(axes7), Create(axes7_labels))
        self.play(Create(bar1), Create(bar3))
        self.wait(1)