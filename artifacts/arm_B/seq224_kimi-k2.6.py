from manim import *

class SceneGen(Scene):
    def construct(self):
        # Setup
        self.camera.frame_width = 14
        self.camera.frame_height = 8
        
        self.first_scene()
        self.clear()
        
        self.second_scene()
        self.clear()
        
        self.third_scene()
        self.clear()
        
        self.fourth_scene()
        self.clear()
        
        self.fifth_scene()
        self.clear()
        
        self.sixth_scene()
        self.clear()
        
        self.seventh_scene()
        self.clear()
        
        self.eighth_scene()
        
    def first_scene(self):
        title = Text("Fourier Transform", font_size=48, color=BLUE)
        subtitle = Text("Decomposing Signals into Frequencies", font_size=28, color=GRAY)
        
        self.play(Write(title), run_time=1.5)
        self.wait(0.3)
        self.play(title.animate.shift(UP * 2), run_time=0.8)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(0.5)
        
        ax = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=8,
            y_length=3,
            axis_config={"include_tip": False},
        ).shift(DOWN * 1)
        
        wave = ax.plot(lambda x: np.sin(x), color=YELLOW, x_range=[0, 4 * PI])
        
        freq_label = MathTex(r"\sin(1 \cdot t)", color=YELLOW).scale(0.9).next_to(ax, DOWN)
        
        self.play(FadeIn(ax), run_time=1)
        self.play(Create(wave), run_time=2)
        self.play(FadeIn(freq_label), run_time=0.8)
        self.wait(0.5)
        
        question = Text("What if a signal contains MULTIPLE frequencies?", font_size=24, color=RED)
        question.next_to(subtitle, DOWN, buff=0.8)
        
        self.play(FadeIn(question), run_time=1)
        self.wait(1.5)
        
        self.play(
            FadeOut(title), FadeOut(subtitle), FadeOut(freq_label),
            FadeOut(question), FadeOut(ax), FadeOut(wave),
            run_time=0.8
        )

    def second_scene(self):
        title = Text("Scene 1: Adding Simple Waves", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        ax1 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=2,
            axis_config={"include_tip": False},
        ).shift(UP * 1.5 + LEFT * 3.5)
        
        label1 = MathTex(r"\sin(t)", color=GREEN).scale(0.7).next_to(ax1, DOWN)
        wave1 = ax1.plot(lambda x: np.sin(x), color=GREEN, x_range=[0, 4 * PI])
        
        self.play(FadeIn(ax1), run_time=0.8)
        self.play(Create(wave1), run_time=1.5)
        self.play(FadeIn(label1), run_time=0.5)
        self.wait(0.3)
        
        ax2 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=2,
            axis_config={"include_tip": False},
        ).shift(UP * 1.5 + RIGHT * 3.5)
        
        label2 = MathTex(r"\sin(3t)", color=RED).scale(0.7).next_to(ax2, DOWN)
        wave2 = ax2.plot(lambda x: np.sin(3 * x), color=RED, x_range=[0, 4 * PI])
        
        self.play(FadeIn(ax2), run_time=0.8)
        self.play(Create(wave2), run_time=1.5)
        self.play(FadeIn(label2), run_time=0.5)
        self.wait(0.3)
        
        plus = MathTex(r"+", font_size=48).shift(DOWN * 0.5)
        equals = MathTex(r"=", font_size=48).shift(DOWN * 2)
        
        self.play(FadeIn(plus), run_time=0.5)
        
        ax3 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-2.5, 2.5, 0.5],
            x_length=10,
            y_length=2.5,
            axis_config={"include_tip": False},
        ).shift(DOWN * 2.5)
        
        label3 = MathTex(r"\sin(t) + \sin(3t)", color=YELLOW).scale(0.8).next_to(ax3, DOWN)
        wave3 = ax3.plot(lambda x: np.sin(x) + np.sin(3 * x), color=YELLOW, x_range=[0, 4 * PI])
        
        self.play(FadeIn(equals), FadeIn(ax3), run_time=0.8)
        self.play(Create(wave3), run_time=2)
        self.play(FadeIn(label3), run_time=0.5)
        self.wait(1)
        
        key_idea = Text("A complex wave can be BUILT from simple frequencies", font_size=22, color=TEAL)
        key_idea.to_edge(DOWN, buff=0.3)
        
        self.play(FadeIn(key_idea), run_time=0.8)
        self.wait(1.5)
        
        self.play(
            FadeOut(title), FadeOut(ax1), FadeOut(wave1), FadeOut(label1),
            FadeOut(ax2), FadeOut(wave2), FadeOut(label2),
            FadeOut(plus), FadeOut(equals), FadeOut(ax3), FadeOut(wave3), FadeOut(label3),
            FadeOut(key_idea),
            run_time=0.8
        )

    def third_scene(self):
        title = Text("Scene 2: The Core Question", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        question = Text("Given a complex signal, can we find its ingredients?", font_size=28, color=YELLOW)
        self.play(FadeIn(question), run_time=1)
        self.wait(0.5)
        self.play(question.animate.shift(UP * 2), run_time=0.8)
        
        ax = Axes(
            x_range=[0, 6 * PI, PI],
            y_range=[-3, 3, 1],
            x_length=12,
            y_length=4,
            axis_config={"include_tip": False},
        )
        
        complex_wave = ax.plot(
            lambda x: np.sin(x) + 0.5 * np.sin(3 * x) + 0.3 * np.sin(5 * x),
            color=WHITE,
            x_range=[0, 6 * PI]
        )
        
        self.play(FadeIn(ax), run_time=1)
        self.play(Create(complex_wave), run_time=2.5)
        
        mystery_label = Text("\"Mystery Signal\"", font_size=24, color=WHITE)
        mystery_label.next_to(ax, DOWN)
        self.play(FadeIn(mystery_label), run_time=0.5)
        self.wait(0.5)
        
        arrow = Arrow(UP * 0.5, DOWN * 1.5, color=RED).shift(RIGHT * 4 + DOWN * 0.5)
        self.play(GrowArrow(arrow), run_time=0.8)
        
        ingredients = VGroup(
            MathTex(r"\omega_1 = 1", color=GREEN),
            MathTex(r"\omega_2 = 3", color=GREEN),
            MathTex(r"\omega_3 = 5", color=GREEN),
        ).arrange(DOWN, buff=0.3).shift(RIGHT * 4 + DOWN * 2.5)
        
        self.play(FadeIn(ingredients), run_time=1)
        self.wait(1)
        
        challenge = Text("This is the INVERSE problem Fourier solved!", font_size=22, color=TEAL)
        challenge.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(challenge), run_time=0.8)
        self.wait(1.5)
        
        self.play(
            FadeOut(title), FadeOut(question), FadeOut(ax), FadeOut(complex_wave),
            FadeOut(mystery_label), FadeOut(arrow), FadeOut(ingredients), FadeOut(challenge),
            run_time=0.8
        )

    def fourth_scene(self):
        title = Text("Scene 3: Testing for a Frequency", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        concept = Text("Probe the signal with a test frequency, measure how well they 'match'", font_size=22, color=GRAY)
        concept.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(concept), run_time=0.8)
        
        ax1 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=2,
            axis_config={"include_tip": False},
        ).shift(LEFT * 3.5 + UP * 1)
        
        signal = ax1.plot(lambda x: np.sin(x), color=YELLOW, x_range=[0, 4 * PI])
        signal_label = MathTex(r"f(t) = \sin(t)", color=YELLOW).scale(0.7).next_to(ax1, DOWN)
        
        self.play(FadeIn(ax1), run_time=0.8)
        self.play(Create(signal), run_time=1.5)
        self.play(FadeIn(signal_label), run_time=0.5)
        
        ax2 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=2,
            axis_config={"include_tip": False},
        ).shift(RIGHT * 3.5 + UP * 1)
        
        probe = ax2.plot(lambda x: np.sin(x), color=GREEN, x_range=[0, 4 * PI])
        probe_label = MathTex(r"g(t) = \sin(t)", color=GREEN).scale(0.7).next_to(ax2, DOWN)
        
        self.play(FadeIn(ax2), run_time=0.8)
        self.play(Create(probe), run_time=1.5)
        self.play(FadeIn(probe_label), run_time=0.5)
        
        match_text = Text("MATCH! Same frequency → Strong response", font_size=20, color=TEAL)
        match_text.shift(DOWN * 0.5)
        self.play(FadeIn(match_text), run_time=0.8)
        self.wait(0.5)
        
        self.play(FadeOut(match_text), run_time=0.5)
        
        ax3 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1, 2, 0.5],
            x_length=10,
            y_length=2,
            axis_config={"include_tip": False},
        ).shift(DOWN * 2.5)
        
        product = ax3.plot(lambda x: np.sin(x) * np.sin(x), color=BLUE, x_range=[0, 4 * PI])
        product_label = MathTex(r"f(t) \cdot g(t) = \sin^2(t) > 0 \text{ (mostly)}", color=BLUE).scale(0.75).next_to(ax3, DOWN)
        
        area = ax3.get_area(product, x_range=[0, 4 * PI], color=BLUE, opacity=0.3)
        
        self.play(FadeIn(ax3), run_time=0.8)
        self.play(Create(product), run_time=1.5)
        self.play(FadeIn(area), run_time=0.8)
        self.play(FadeIn(product_label), run_time=0.5)
        
        integral = MathTex(r"\int f(t) \cdot g(t)\, dt \text{ is LARGE}", color=RED).scale(0.8).shift(DOWN * 0.3)
        self.play(FadeIn(integral), run_time=0.8)
        self.wait(1.5)
        
        self.play(
            FadeOut(title), FadeOut(concept), FadeOut(ax1), FadeOut(signal), FadeOut(signal_label),
            FadeOut(ax2), FadeOut(probe), FadeOut(probe_label),
            FadeOut(ax3), FadeOut(product), FadeOut(area), FadeOut(product_label), FadeOut(integral),
            run_time=0.8
        )

    def fifth_scene(self):
        title = Text("Scene 4: Mismatch Case", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        ax1 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=2,
            axis_config={"include_tip": False},
        ).shift(LEFT * 3.5 + UP * 1)
        
        signal = ax1.plot(lambda x: np.sin(x), color=YELLOW, x_range=[0, 4 * PI])
        signal_label = MathTex(r"f(t) = \sin(t)", color=YELLOW).scale(0.7).next_to(ax1, DOWN)
        
        self.play(FadeIn(ax1), run_time=0.8)
        self.play(Create(signal), run_time=1.5)
        self.play(FadeIn(signal_label), run_time=0.5)
        
        ax2 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=2,
            axis_config={"include_tip": False},
        ).shift(RIGHT * 3.5 + UP * 1)
        
        probe = ax2.plot(lambda x: np.sin(3 * x), color=RED, x_range=[0, 4 * PI])
        probe_label = MathTex(r"g(t) = \sin(3t)", color=RED).scale(0.7).next_to(ax2, DOWN)
        
        self.play(FadeIn(ax2), run_time=0.8)
        self.play(Create(probe), run_time=1.5)
        self.play(FadeIn(probe_label), run_time=0.5)
        
        mismatch_text = Text("MISMATCH! Different frequencies → Weak response", font_size=20, color=RED)
        mismatch_text.shift(DOWN * 0.5)
        self.play(FadeIn(mismatch_text), run_time=0.8)
        self.wait(0.5)
        
        self.play(FadeOut(mismatch_text), run_time=0.5)
        
        ax3 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=2,
            axis_config={"include_tip": False},
        ).shift(DOWN * 2.5)
        
        product = ax3.plot(lambda x: np.sin(x) * np.sin(3 * x), color=PURPLE, x_range=[0, 4 * PI])
        product_label = MathTex(r"f(t) \cdot g(t) = \sin(t)\sin(3t) \text{ oscillates around 0}", color=PURPLE).scale(0.7).next_to(ax3, DOWN)
        
        area_up = ax3.get_area(product, x_range=[0, PI], color=GREEN, opacity=0.2)
        area_down = ax3.get_area(product, x_range=[PI, 2*PI], color=RED, opacity=0.2)
        area_up2 = ax3.get_area(product, x_range=[2*PI, 3*PI], color=GREEN, opacity=0.2)
        area_down2 = ax3.get_area(product, x_range=[3*PI, 4*PI], color=RED, opacity=0.2)
        
        self.play(FadeIn(ax3), run_time=0.8)
        self.play(Create(product), run_time=1.5)
        self.play(FadeIn(area_up, area_down, area_up2, area_down2), run_time=0.8)
        self.play(FadeIn(product_label), run_time=0.5)
        
        integral = MathTex(r"\int f(t) \cdot g(t)\, dt \approx 0", color=RED).scale(0.8).shift(DOWN * 0.3)
        self.play(FadeIn(integral), run_time=0.8)
        
        cancel = Text("Positive and negative areas CANCEL", font_size=20, color=GRAY)
        cancel.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(cancel), run_time=0.8)
        self.wait(1.5)
        
        self.play(
            FadeOut(title), FadeOut(ax1), FadeOut(signal), FadeOut(signal_label),
            FadeOut(ax2), FadeOut(probe), FadeOut(probe_label),
            FadeOut(ax3), FadeOut(product), FadeOut(area_up), FadeOut(area_down),
            FadeOut(area_up2), FadeOut(area_down2), FadeOut(product_label), FadeOut(integral), FadeOut(cancel),
            run_time=0.8
        )

    def sixth_scene(self):
        title = Text("Scene 5: The Fourier Transform Formula", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        # Build up the formula piece by piece
        part1 = MathTex(r"\hat{f}(\omega)", color=YELLOW).scale(1.5)
        part1.shift(UP * 1.5)
        
        self.play(Write(part1), run_time=0.8)
        
        part2 = MathTex(r"=", color=WHITE).scale(1.5)
        part2.next_to(part1, RIGHT)
        
        self.play(FadeIn(part2), run_time=0.5)
        
        part3 = MathTex(r"\int", color=WHITE).scale(1.5)
        part3.next_to(part2, RIGHT)
        
        self.play(FadeIn(part3), run_time=0.5)
        
        part4 = MathTex(r"f(t)", color=YELLOW).scale(1.2)
        part4.shift(DOWN * 0.5 + LEFT * 2)
        
        part5 = MathTex(r"e^{-i\omega t}", color=GREEN).scale(1.2)
        part5.next_to(part4, RIGHT)
        
        self.play(FadeIn(part4), run_time=0.5)
        self.play(FadeIn(part5), run_time=0.5)
        
        together = VGroup(part4, part5).copy()
        together_target = MathTex(r"f(t)\, e^{-i\omega t}", color=WHITE).scale(1.2)
        together_target.shift(UP * 0.5 + RIGHT * 0.5)
        
        dt = MathTex(r"dt", color=WHITE).scale(1.2)
        dt.next_to(together_target, RIGHT)
        
        integral_part = VGroup(together_target, dt)
        
        self.play(
            Transform(VGroup(part4, part5), together_target),
            FadeIn(dt),
            FadeOut(part1), FadeOut(part2), FadeOut(part3),
            run_time=1
        )
        
        full_formula = MathTex(r"\hat{f}(\omega) = \int_{-\infty}^{\infty} f(t)\, e^{-i\omega t}\, dt", color=WHITE).scale(1.3).shift(UP * 1)
        
        self.play(
            FadeOut(integral_part),
            Write(full_formula),
            run_time=1.5
        )
        
        self.wait(0.5)
        
        # Annotations
        annotation1 = MathTex(r"\text{Test frequency } \omega", color=GREEN).scale(0.8)
        annotation1.next_to(full_formula, DOWN, buff=0.8).shift(LEFT * 3)
        
        arrow1 = Arrow(annotation1.get_top(), full_formula[0][14:16].get_bottom(), color=GREEN, buff=0.2)
        
        self.play(FadeIn(annotation1), GrowArrow(arrow1), run_time=0.8)
        
        annotation2 = MathTex(r"\text{Signal being analyzed}", color=YELLOW).scale(0.8)
        annotation2.next_to(full_formula, DOWN, buff=0.8).shift(RIGHT * 2)
        
        arrow2 = Arrow(annotation2.get_top(), full_formula[0][7:10].get_bottom(), color=YELLOW, buff=0.2)
        
        self.play(FadeIn(annotation2), GrowArrow(arrow2), run_time=0.8)
        
        annotation3 = MathTex(r"\text{Complex oscillation (cos + i*sin)}", color=PURPLE).scale(0.8)
        annotation3.next_to(full_formula, DOWN, buff=1.8)
        
        self.play(FadeIn(annotation3), run_time=0.8)
        
        self.wait(0.5)
        
        euler = MathTex(r"e^{-i\omega t} = \cos(\omega t) - i\sin(\omega t)", color=PURPLE).scale(0.9)
        euler.next_to(annotation3, DOWN, buff=0.3)
        
        self.play(FadeIn(euler), run_time=0.8)
        self.wait(1.5)
        
        summary = Text("For each ω, measure how much f(t) 'contains' that frequency", font_size=22, color=TEAL)
        summary.to_edge(DOWN, buff=0.3)
        
        self.play(FadeIn(summary), run_time=0.8)
        self.wait(1.5)
        
        self.play(
            FadeOut(title), FadeOut(full_formula), FadeOut(annotation1), FadeOut(arrow1),
            FadeOut(annotation2), FadeOut(arrow2), FadeOut(annotation3), FadeOut(euler), FadeOut(summary),
            run_time=0.8
        )

    def seventh_scene(self):
        title = Text("Scene 6: Frequency Domain View", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        time_text = Text("TIME DOMAIN", font_size=22, color=YELLOW).shift(UP * 2.5 + LEFT * 4)
        freq_text = Text("FREQUENCY DOMAIN", font_size=22, color=GREEN).shift(UP * 2.5 + RIGHT * 4)
        
        self.play(FadeIn(time_text), run_time=0.5)
        self.play(FadeIn(freq_text), run_time=0.5)
        
        # Time domain: sum of three sines
        ax_time = Axes(
            x_range=[0, 6 * PI, PI],
            y_range=[-2.5, 2.5, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"include_tip": False, "numbers_to_exclude": []},
        ).shift(LEFT * 3.5)
        
        time_wave = ax_time.plot(
            lambda x: np.sin(x) + 0.5 * np.sin(3 * x) + 0.7 * np.sin(5 * x),
            color=YELLOW,
            x_range=[0, 6 * PI]
        )
        
        self.play(FadeIn(ax_time), run_time=0.8)
        self.play(Create(time_wave), run_time=2)
        
        # Arrow showing transform
        transform_arrow = Arrow(LEFT * 1, RIGHT * 1, color=RED, buff=0.3).shift(DOWN * 0.5)
        transform_label = MathTex(r"\mathcal{F}", color=RED).scale(1.2).next_to(transform_arrow, UP, buff=0.1)
        
        self.play(GrowArrow(transform_arrow), FadeIn(transform_label), run_time=0.8)
        
        # Frequency domain: spikes
        ax_freq = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 1.2, 0.2],
            x_length=6,
            y_length=3,
            axis_config={"include_tip": False},
        ).shift(RIGHT * 3.5)
        
        ax_freq_labels = VGroup(
            MathTex(r"1", color=WHITE).scale(0.6).next_to(ax_freq.c2p(1, 0), DOWN),
            MathTex(r"3", color=WHITE).scale(0.6).next_to(ax_freq.c2p(3, 0), DOWN),
            MathTex(r"5", color=WHITE).scale(0.6).next_to(ax_freq.c2p(5, 0), DOWN),
        )
        
        self.play(FadeIn(ax_freq), run_time=0.8)
        
        # Build up the frequency spikes
        spike1 = Line(ax_freq.c2p(1, 0), ax_freq.c2p(1, 1), color=GREEN, stroke_width=8)
        spike2 = Line(ax_freq.c2p(3, 0), ax_freq.c2p(3, 0.5), color=GREEN, stroke_width=8)
        spike3 = Line(ax_freq.c2p(5, 0), ax_freq.c2p(5, 0.7), color=GREEN, stroke_width=8)
        
        freq_label = MathTex(r"|\hat{f}(\omega)|", color=GREEN).scale(0.8).next_to(ax_freq, DOWN)
        
        self.play(Create(spike1), run_time=0.8)
        self.play(Create(spike2), run_time=0.8)
        self.play(Create(spike3), run_time=0.8)
        self.play(FadeIn(ax_freq_labels), FadeIn(freq_label), run_time=0.5)
        
        # Highlight the correspondence
        highlight1 = SurroundingRectangle(VGroup(spike1, ax_freq_labels[0]), color=YELLOW, buff=0.1)
        highlight2 = SurroundingRectangle(VGroup(spike2, ax_freq_labels[1]), color=YELLOW, buff=0.1)
        highlight3 = SurroundingRectangle(VGroup(spike3, ax_freq_labels[2]), color=YELLOW, buff=0.1)
        
        amp_label1 = MathTex(r"\text{Amplitude } 1", color=YELLOW).scale(0.6).next_to(spike1, RIGHT, buff=0.2)
        amp_label2 = MathTex(r"0.5", color=YELLOW).scale(0.6).next_to(spike2, RIGHT, buff=0.2)
        amp_label3 = MathTex(r"0.7", color=YELLOW).scale(0.6).next_to(spike3, RIGHT, buff=0.2)
        
        self.play(Create(highlight1), FadeIn(amp_label1), run_time=0.6)
        self.play(FadeOut(highlight1), run_time=0.3)
        self.play(Create(highlight2), FadeIn(amp_label2), run_time=0.6)
        self.play(FadeOut(highlight2), run_time=0.3)
        self.play(Create(highlight3), FadeIn(amp_label3), run_time=0.6)
        self.play(FadeOut(highlight3), run_time=0.3)
        
        self.wait(0.5)
        
        key_insight = Text("The Fourier Transform reveals the 'recipe' of frequencies", font_size=22, color=TEAL)
        key_insight.to_edge(DOWN, buff=0.3)
        
        self.play(FadeIn(key_insight), run_time=0.8)
        self.wait(1.5)
        
        self.play(
            FadeOut(title), FadeOut(time_text), FadeOut(freq_text),
            FadeOut(ax_time), FadeOut(time_wave), FadeOut(transform_arrow), FadeOut(transform_label),
            FadeOut(ax_freq), FadeOut(spike1), FadeOut(spike2), FadeOut(spike3),
            FadeOut(ax_freq_labels), FadeOut(freq_label), FadeOut(amp_label1), FadeOut(amp_label2), FadeOut(amp_label3),
            FadeOut(key_insight),
            run_time=0.8
        )

    def eighth_scene(self):
        title = Text("Scene 7: Summary and Power", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1)
        
        # Recap points
        points = VGroup(
            Text("1. Any signal can be built from sine waves", font_size=22, color=YELLOW),
            Text("2. The Fourier Transform finds which frequencies are present", font_size=22, color=GREEN),
            Text("3. It uses correlation: multiply and integrate", font_size=22, color=TEAL),
            Text("4. Result: frequency spectrum showing 'ingredients'", font_size=22, color=ORANGE),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).shift(UP * 0.5)
        
        for point in points:
            self.play(FadeIn(point), run_time=0.7)
            self.wait(0.3)
        
        self.wait(0.5)
        
        # Visual summary
        signal_x = 7
        bar_width = 0.8
        bar_max_height = 3
        
        # Create abstract frequency bars
        bars = VGroup()
        freqs = [0.5, 0.3, 0.8, 0.2, 0.6, 0.4, 0.9]
        colors_bar = [RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE]
        
        for i, (h, c) in enumerate(zip(freqs, colors_bar)):
            bar = Rectangle(
                width=bar_width,
                height=h * bar_max_height,
                fill_color=c,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=1
            )
            bar.move_to(DOWN * 2 + LEFT * (signal_x/2 - 0.5) + RIGHT * i * (bar_width + 0.1) + UP * (h * bar_max_height / 2))
            bars.add(bar)
        
        freq_axis = Arrow(
            DOWN * 2 + LEFT * (signal_x/2),
            DOWN * 2 + RIGHT * (signal_x/2),
            color=WHITE, buff=0
        )
        
        amp_axis = Arrow(
            DOWN * 2 + LEFT * (signal_x/2),
            DOWN * 2 + UP * 3,
            color=WHITE, buff=0
        )
        
        self.play(FadeIn(freq_axis), FadeIn(amp_axis), run_time=0.5)
        
        for bar in bars:
            self.play(GrowFromEdge(bar, DOWN), run_time=0.4)
        
        self.wait(0.5)
        
        # Applications
        apps_title = Text("Applications:", font_size=26, color=WHITE).next_to(bars, DOWN, buff=0.5).shift(LEFT * 2)
        apps = VGroup(
            Text("Audio processing", font_size=18, color=GRAY),
            Text("Image compression (JPEG)", font_size=18, color=GRAY),
            Text("Medical imaging (MRI)", font_size=18, color=GRAY),
            Text("Quantum mechanics", font_size=18, color=GRAY),
        ).arrange(RIGHT, buff=0.4).next_to(apps_title, RIGHT)
        
        self.play(FadeIn(apps_title), run_time=0.5)
        for app in apps:
            self.play(FadeIn(app), run_time=0.4)
        
        self.wait(0.5)
        
        # Final formula
        final = MathTex(r"\hat{f}(\omega) = \int_{-\infty}^{\infty} f(t)\, e^{-i\omega t}\, dt", color=WHITE).scale(1.2)
        final.to_edge(DOWN, buff=0.8)
        
        surround = SurroundingRectangle(final, color=YELLOW, buff=0.2)
        
        self.play(Write(final), run_time=1.5)
        self.play(Create(surround), run_time=0.8)
        
        # Pulse animation on the formula
        self.play(surround.animate.set_color(RED), run_time=0.5)
        self.play(surround.animate.set_color(YELLOW), run_time=0.5)
        
        self.wait(2)
        
        # Fade everything
        self.play(
            FadeOut(title), FadeOut(points), FadeOut(bars),
            FadeOut(freq_axis), FadeOut(amp_axis),
            FadeOut(apps_title), FadeOut(apps),
            FadeOut(final), FadeOut(surround),
            run_time=1
        )
        
        # Final message
        thanks = Text("Fourier Transform: Seeing the Hidden Frequencies", font_size=32, color=BLUE)
        self.play(FadeIn(thanks), run_time=1)
        self.wait(1)
        
        end = Text("End of Tutorial", font_size=28, color=GRAY).next_to(thanks, DOWN, buff=0.5)
        self.play(FadeIn(end), run_time=0.8)
        self.wait(2)
        
        self.play(FadeOut(thanks), FadeOut(end), run_time=0.8)
