from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: Introduction
        self.clear()
        title = Text("Fourier Transform", font_size=64)
        subtitle = Text("Decomposing a signal into frequencies", font_size=36).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Scene 2: A signal is a function of time
        self.clear()
        axes = Axes(x_range=[-2, 2, 1], y_range=[-1.5, 1.5, 1], axis_config={"color": WHITE})
        x_label = axes.get_x_axis_label("t")
        y_label = axes.get_y_axis_label("x(t)")
        signal = axes.plot(lambda x: np.sin(2*np.pi*x), color=BLUE)
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(signal))
        label = Text("A signal x(t)", font_size=28).next_to(axes, DOWN)
        self.play(Write(label))
        self.wait(1.5)
        self.play(FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(signal), FadeOut(label))

        # Scene 3: Building blocks are sinusoids
        self.clear()
        axes2 = Axes(x_range=[0, 4, 1], y_range=[-2, 2, 1], axis_config={"color": WHITE})
        axes2.to_edge(DOWN)
        base = axes2.plot(lambda x: np.sin(2*np.pi*1*x), color=BLUE)
        high = axes2.plot(lambda x: np.sin(2*np.pi*3*x), color=RED)
        low = axes2.plot(lambda x: 0.5*np.sin(2*np.pi*0.5*x), color=GREEN)
        title2 = Text("Sine waves are the building blocks", font_size=32).to_edge(UP)
        self.play(Write(title2), Create(axes2))
        self.play(Create(base))
        self.wait(0.5)
        self.play(Create(high))
        self.wait(0.5)
        self.play(Create(low))
        self.wait(1)
        self.play(FadeOut(title2), FadeOut(axes2), FadeOut(base), FadeOut(high), FadeOut(low))

        # Scene 4: Superposition
        self.clear()
        axes3 = Axes(x_range=[0, 4, 1], y_range=[-3, 3, 1], axis_config={"color": WHITE})
        axes3.to_edge(DOWN)
        s1 = axes3.plot(lambda x: np.sin(2*np.pi*1*x), color=BLUE)
        s2 = axes3.plot(lambda x: 0.6*np.sin(2*np.pi*3*x), color=RED)
        s3 = axes3.plot(lambda x: 0.3*np.sin(2*np.pi*0.5*x), color=GREEN)
        combined = axes3.plot(lambda x: np.sin(2*np.pi*1*x)+0.6*np.sin(2*np.pi*3*x)+0.3*np.sin(2*np.pi*0.5*x), color=YELLOW)
        title3 = Text("Superposition creates complex signals", font_size=32).to_edge(UP)
        self.play(Write(title3), Create(axes3))
        self.play(Create(s1), Create(s2), Create(s3))
        self.wait(0.8)
        self.play(FadeOut(s1), FadeOut(s2), FadeOut(s3))
        self.play(Create(combined))
        self.wait(1.5)
        self.play(FadeOut(title3), FadeOut(axes3), FadeOut(combined))

        # Scene 5: Frequency domain intuition
        self.clear()
        title4 = Text("Frequency domain: how much of each frequency?", font_size=32).to_edge(UP)
        bars = VGroup(
            Rectangle(width=0.6, height=1.5, color=BLUE),
            Rectangle(width=0.6, height=0.9, color=RED).next_to(Rectangle(width=0.6, height=1.5), RIGHT, buff=0.3),
            Rectangle(width=0.6, height=0.4, color=GREEN).next_to(Rectangle(width=0.6, height=1.5).next_to(Rectangle(width=0.6, height=0.9), RIGHT, buff=0.3), RIGHT, buff=0.3)
        )
        bars.move_to(ORIGIN)
        freq_label = Text("f", font_size=24).next_to(bars, DOWN)
        amp_label = Text("Amplitude", font_size=24).next_to(freq_label, RIGHT)
        self.play(Write(title4))
        self.play(FadeIn(bars), Write(freq_label), Write(amp_label))
        self.play(bars.animate.set_color_by_gradient([BLUE, RED, GREEN]))
        self.wait(1.5)
        self.play(FadeOut(title4), FadeOut(bars), FadeOut(freq_label), FadeOut(amp_label))

        # Scene 6: Fourier transform formula
        self.clear()
        title5 = Text("Fourier Transform X(f) = ∫ x(t) e^{-i2πft} dt", font_size=36).to_edge(UP)
        formula = MathTex(r"X(f)=\int_{-\infty}^{\infty} x(t)\,e^{-i2\pi f t}\,dt", font_size=60)
        formula.next_to(title5, DOWN, buff=0.8)
        arrow = Arrow(start=LEFT*2, end=RIGHT*2, color=YELLOW, buff=0.5)
        time_text = Text("Time domain", font_size=28).next_to(arrow, LEFT).shift(UP*0.5)
        freq_text = Text("Frequency domain", font_size=28).next_to(arrow, RIGHT).shift(UP*0.5)
        self.play(Write(title5))
        self.play(Write(formula))
        self.play(Create(arrow), Write(time_text), Write(freq_text))
        self.wait(2)
        self.play(FadeOut(title5), FadeOut(formula), FadeOut(arrow), FadeOut(time_text), FadeOut(freq_text))

        # Scene 7: Decomposition example
        self.clear()
        axes4 = Axes(x_range=[0, 2, 1], y_range=[-1.5, 1.5, 1], axis_config={"color": WHITE})
        axes4.to_edge(DOWN)
        square = axes4.plot(lambda x: np.sign(np.sin(2*np.pi*1*x)), color=WHITE)
        title6 = Text("Square wave ≈ sum of odd harmonics", font_size=32).to_edge(UP)
        self.play(Write(title6), Create(axes4))
        self.play(Create(square))
        approx = axes4.plot(lambda x: np.sin(2*np.pi*1*x) + 1/3*np.sin(2*np.pi*3*x) + 1/5*np.sin(2*np.pi*5*x), color=YELLOW)
        self.play(Transform(square, approx))
        self.wait(1.5)
        self.play(FadeOut(title6), FadeOut(axes4), FadeOut(square))

        # Scene 8: Summary
        self.clear()
        final = Text("Fourier Transform: Any signal = sum of sinusoids", font_size=42)
        sub = Text("Time ↔ Frequency", font_size=36).next_to(final, DOWN)
        self.play(Write(final), Write(sub))
        self.wait(2)
        self.play(FadeOut(final), FadeOut(sub))
