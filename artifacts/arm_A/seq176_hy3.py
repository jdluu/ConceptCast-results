from manim import *
import numpy as np

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Time domain signal
        title = Text("1. Signals in the Time Domain").to_edge(UP)
        ax = Axes(x_range=[0, 2*np.pi, np.pi/2], y_range=[-1.5, 1.5, 1], x_length=10, y_length=4).shift(DOWN)
        graph = ax.plot(lambda x: np.sin(x), color=BLUE)
        self.play(Write(title))
        self.play(Create(ax))
        self.play(Create(graph))
        self.play(graph.animate.set_color(RED), run_time=1)
        self.wait(0.5)
        self.clear()

        # Scene 2: Superposition of sines
        title2 = Text("2. Complex Signals = Sum of Sines").to_edge(UP)
        ax2 = Axes(x_range=[0, 2*np.pi, np.pi/2], y_range=[-3, 3, 1], x_length=10, y_length=4).shift(DOWN)
        g1 = ax2.plot(lambda x: np.sin(x), color=BLUE)
        g2 = ax2.plot(lambda x: 0.6*np.sin(2*x), color=GREEN)
        g3 = ax2.plot(lambda x: 0.3*np.sin(3*x), color=YELLOW)
        gsum = ax2.plot(lambda x: np.sin(x) + 0.6*np.sin(2*x) + 0.3*np.sin(3*x), color=RED)
        self.play(Write(title2))
        self.play(Create(ax2))
        self.play(Create(g1), Create(g2), Create(g3))
        self.wait(0.5)
        self.play(FadeOut(g1), FadeOut(g2), FadeOut(g3))
        self.play(Create(gsum))
        self.wait(0.5)
        self.clear()

        # Scene 3: Basis functions
        title3 = Text("3. Basis Functions at Different Frequencies").to_edge(UP)
        ax3 = Axes(x_range=[0, 2*np.pi, np.pi/2], y_range=[-1.5, 1.5, 1], x_length=10, y_length=4).shift(DOWN)
        self.play(Write(title3), Create(ax3))
        for i, f in enumerate([1, 2, 3, 4]):
            g = ax3.plot(lambda x, f=f: np.sin(f*x), color=interpolate_color(BLUE, RED, f/4))
            self.play(Create(g), run_time=0.5)
            self.wait(0.2)
        self.wait(0.5)
        self.clear()

        # Scene 4: Correlation / projection
        title4 = Text("4. Extracting a Frequency via Correlation").to_edge(UP)
        ax4 = Axes(x_range=[0, 2*np.pi, np.pi/2], y_range=[-2, 2, 1], x_length=10, y_length=4).shift(DOWN)
        sig = ax4.plot(lambda x: np.sin(x) + 0.5*np.sin(3*x), color=RED)
        basis = ax4.plot(lambda x: np.sin(x), color=BLUE)
        prod = ax4.plot(lambda x: (np.sin(x) + 0.5*np.sin(3*x)) * np.sin(x), color=YELLOW)
        self.play(Write(title4), Create(ax4))
        self.play(Create(sig))
        self.play(Create(basis))
        self.wait(0.5)
        self.play(Transform(basis, prod))
        self.wait(0.5)
        area = ax4.get_area(prod, x_range=[0, 2*np.pi], color=GREEN, opacity=0.5)
        self.play(FadeIn(area))
        self.wait(0.5)
        self.clear()

        # Scene 5: Fourier series of square wave
        title5 = Text("5. Fourier Series Approximates a Square Wave").to_edge(UP)
        ax5 = Axes(x_range=[0, 2*np.pi, np.pi/2], y_range=[-1.5, 1.5, 1], x_length=10, y_length=4).shift(DOWN)
        square = ax5.plot(lambda x: np.sign(np.sin(x)), color=WHITE)
        def fsum(x, n):
            s = np.zeros_like(x)
            for k in range(1, n+1, 2):
                s += (4/(np.pi*k)) * np.sin(k*x)
            return s
        g1 = ax5.plot(lambda x: fsum(x, 1), color=BLUE)
        g3 = ax5.plot(lambda x: fsum(x, 3), color=GREEN)
        g5 = ax5.plot(lambda x: fsum(x, 5), color=YELLOW)
        self.play(Write(title5), Create(ax5))
        self.play(Create(square))
        self.play(Create(g1))
        self.wait(0.3)
        self.play(Transform(g1, g3))
        self.wait(0.3)
        self.play(Transform(g1, g5))
        self.wait(0.5)
        self.clear()

        # Scene 6: Frequency spectrum
        title6 = Text("6. The Frequency Spectrum").to_edge(UP)
        ax6 = Axes(x_range=[0, 6, 1], y_range=[0, 1.5, 0.5], x_length=10, y_length=4).shift(DOWN)
        self.play(Write(title6), Create(ax6))
        bars = VGroup()
        for f in [1, 3, 5]:
            h = 4/(np.pi*f)
            bar = Rectangle(width=0.4, height=h, color=RED).move_to(ax6.c2p(f, h/2))
            bars.add(bar)
            self.play(FadeIn(bar), run_time=0.5)
        self.wait(0.5)
        self.clear()

        # Scene 7: Continuous Fourier Transform
        title7 = Text("7. Continuous Fourier Transform").to_edge(UP)
        formula = MathTex(r"\hat{f}(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt").shift(UP*1.5)
        ax7 = Axes(x_range=[-3, 3, 1], y_range=[-0.5, 2, 0.5], x_length=8, y_length=3).shift(DOWN)
        pulse = ax7.plot(lambda x: np.where(np.abs(x) < 1, 1, 0), color=BLUE)
        sinc = ax7.plot(lambda x: np.sinc(x/np.pi), color=RED)
        self.play(Write(title7))
        self.play(Write(formula))
        self.play(Create(ax7), Create(pulse))
        self.wait(0.5)
        self.play(Transform(pulse, sinc))
        self.wait(0.5)
        self.clear()

        # Scene 8: Complex exponential phasor
        title8 = Text("8. Complex Exponentials: Rotating Phasors").to_edge(UP)
        plane = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1]).shift(DOWN)
        dot = Dot(plane.n2p(1), color=YELLOW)
        circle = Circle(radius=1, color=BLUE).move_to(plane.n2p(0))
        self.play(Write(title8), Create(plane), Create(circle), Create(dot))
        self.play(Rotate(dot, angle=2*np.pi, about_point=plane.n2p(0)), run_time=2)
        self.wait(0.5)
        self.clear()

        # Scene 9: Summary
        title9 = Text("9. Fourier Transform: Time ↔ Frequency").to_edge(UP)
        ax_t = Axes(x_range=[0, 2*np.pi, np.pi/2], y_range=[-1.5, 1.5, 1], x_length=5, y_length=3).shift(LEFT*3)
        ax_f = Axes(x_range=[0, 6, 1], y_range=[0, 1.5, 0.5], x_length=5, y_length=3).shift(RIGHT*3)
        sig = ax_t.plot(lambda x: np.sin(x) + 0.5*np.sin(2*x), color=BLUE)
        b1 = Rectangle(width=0.3, height=1, color=RED).move_to(ax_f.c2p(1, 0.5))
        b2 = Rectangle(width=0.3, height=0.5, color=RED).move_to(ax_f.c2p(2, 0.25))
        arrow = Arrow(ax_t.get_right(), ax_f.get_left(), color=WHITE)
        self.play(Write(title9))
        self.play(Create(ax_t), Create(ax_f))
        self.play(Create(sig), FadeIn(b1), FadeIn(b2))
        self.play(Create(arrow))
        self.wait(1)