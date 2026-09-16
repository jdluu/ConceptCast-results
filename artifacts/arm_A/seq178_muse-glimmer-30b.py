from manim import *

class SceneGen(Scene):
    def construct(self):
        # Scene 1: What is a signal
        title = Text("Fourier Transform", font_size=64).to_edge(UP)
        sub = Text("Decomposing a signal into frequencies", font_size=36).next_to(title, DOWN)
        self.play(Write(title), Write(sub))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(sub))

        # Scene 2: Time domain signal
        self.clear()
        axes = Axes(x_range=[-4,4,1], y_range=[-1.5,1.5,0.5], axis_config={"color": WHITE})
        x_label = axes.get_x_axis_label("t")
        y_label = axes.get_y_axis_label("x(t)")
        signal = axes.plot(lambda x: np.sin(x) + 0.5*np.sin(3*x), color=BLUE)
        label = Text("x(t) in time domain", font_size=32).to_edge(UP)
        self.play(Create(axes), Write(x_label), Write(y_label), Write(label))
        self.play(Create(signal), run_time=2)
        self.wait(1)
        self.play(FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(signal), FadeOut(label))

        # Scene 3: Building blocks - sine waves
        self.clear()
        axes2 = Axes(x_range=[-2*np.pi,2*np.pi,1], y_range=[-2,2,1], axis_config={"color": WHITE})
        sin1 = axes2.plot(lambda x: np.sin(x), color=RED)
        sin2 = axes2.plot(lambda x: 0.5*np.sin(3*x), color=GREEN)
        sum_wave = axes2.plot(lambda x: np.sin(x)+0.5*np.sin(3*x), color=YELLOW)
        txt = Text("Any signal = sum of sines", font_size=32).to_edge(UP)
        self.play(Create(axes2), Write(txt))
        self.play(Create(sin1), run_time=1.5)
        self.play(Create(sin2), run_time=1.5)
        self.play(Create(sum_wave), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(axes2), FadeOut(txt), FadeOut(sin1), FadeOut(sin2), FadeOut(sum_wave))

        # Scene 4: Frequency concept
        self.clear()
        freq_title = Text("Frequency = how fast it oscillates", font_size=40).to_edge(UP)
        axes3 = Axes(x_range=[0,10,1], y_range=[-1.5,1.5,0.5])
        low = axes3.plot(lambda x: np.sin(1*x), color=BLUE)
        high = axes3.plot(lambda x: np.sin(4*x), color=ORANGE)
        label_low = Text("low f", font_size=24, color=BLUE).next_to(axes3, DOWN, buff=0.3).shift(LEFT*2)
        label_high = Text("high f", font_size=24, color=ORANGE).next_to(axes3, DOWN, buff=0.3).shift(RIGHT*2)
        self.play(Write(freq_title), Create(axes3))
        self.play(Create(low), Write(label_low))
        self.wait(0.8)
        self.play(Create(high), Write(label_high))
        self.wait(1)
        self.play(FadeOut(freq_title), FadeOut(axes3), FadeOut(low), FadeOut(high), FadeOut(label_low), FadeOut(label_high))

        # Scene 5: Superposition to frequency spectrum
        self.clear()
        spectrum_axes = Axes(x_range=[0,6,1], y_range=[0,1.2,0.2], x_length=8, y_length=3)
        spectrum_axes.add_coordinates()
        spectrum_axes.x_axis.set_label("frequency f")
        spectrum_axes.y_axis.set_label("Amplitude")
        bar1 = Rectangle(height=0.6, width=0.4, color=RED, fill_opacity=0.8).move_to(spectrum_axes.c2p(1,0.3))
        bar2 = Rectangle(height=0.3, width=0.4, color=GREEN, fill_opacity=0.8).move_to(spectrum_axes.c2p(3,0.15))
        title5 = Text("Frequency domain: which frequencies are present?", font_size=32).to_edge(UP)
        self.play(Write(title5), Create(spectrum_axes))
        self.play(GrowFromCenter(bar1), GrowFromCenter(bar2))
        self.wait(1.5)
        self.play(FadeOut(title5), FadeOut(spectrum_axes), FadeOut(bar1), FadeOut(bar2))

        # Scene 6: Fourier Transform formula
        self.clear()
        formula = MathTex(
            r"X(f)=\int_{-\infty}^{\infty} x(t)\,e^{-2\pi i f t}\,dt",
            font_size=72
        )
        desc = Text("Integral projects signal onto each frequency", font_size=28).next_to(formula, DOWN)
        self.play(Write(formula))
        self.play(Write(desc))
        self.wait(2)
        self.play(FadeOut(formula), FadeOut(desc))

        # Scene 7: Summary
        self.clear()
        summary = Text("Fourier Transform: time -> frequency", font_size=48)
        bullet1 = Text("Signal = sum of sinusoids", font_size=32).next_to(summary, DOWN, buff=0.5)
        bullet2 = Text("Transform finds amplitudes per frequency", font_size=32).next_to(bullet1, DOWN)
        bullet3 = Text("Inverse rebuilds original signal", font_size=32).next_to(bullet2, DOWN)
        self.play(Write(summary))
        self.play(Write(bullet1))
        self.play(Write(bullet2))
        self.play(Write(bullet3))
        self.wait(2)
