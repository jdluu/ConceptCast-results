from manim import *
import numpy as np


class SceneGen(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # Scene 1: What is a signal? A pure tone in the time domain.
        # ------------------------------------------------------------------
        title = Text("The Fourier Transform", gradient=(BLUE, TEAL)).to_edge(UP)
        sub = Text("Decomposing a signal into its frequencies",
                   font_size=28).next_to(title, DOWN, buff=0.3)

        axes = Axes(
            x_range=[0, 4, 1], y_range=[-1.6, 1.6, 1],
            x_length=10, y_length=4,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.8)
        x_lab = axes.get_x_axis_label(Text("time  t", font_size=28)).shift(DOWN * 0.3)
        y_lab = axes.get_y_axis_label(Text("amplitude", font_size=28))

        tone = axes.plot(lambda x: np.sin(TAU * x), x_range=[0, 4], color=BLUE)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP))
        self.play(Create(axes), Write(x_lab), Write(y_lab), run_time=2)
        self.play(Create(tone), run_time=3)

        peak1 = Dot(axes.c2p(0.25, 1), color=YELLOW)
        peak2 = Dot(axes.c2p(1.25, 1), color=YELLOW)
        brace = Brace(VGroup(peak1, peak2), DOWN, color=YELLOW)
        brace_text = Text("one period = one cycle per second",
                          font_size=24).next_to(brace, DOWN, buff=0.2)
        self.play(FadeIn(peak1), FadeIn(peak2))
        self.play(GrowFromCenter(brace), Write(brace_text), run_time=1.5)

        f_lab = Text("frequency  f = 1 Hz", font_size=30, color=BLUE
                     ).next_to(brace_text, DOWN, buff=0.4)
        self.play(Write(f_lab))
        self.wait(1)

        self.play(*[FadeOut(m) for m in [title, sub, axes, x_lab, y_lab,
                                         tone, peak1, peak2, brace,
                                         brace_text, f_lab]])
        self.clear()

        # ------------------------------------------------------------------
        # Scene 2: Superposition — adding simple waves builds a complex one.
        # ------------------------------------------------------------------
        title = Text("Step 1: Superposition", color=TEAL).to_edge(UP)

        axes = Axes(
            x_range=[0, 4, 1], y_range=[-2.2, 2.2, 1],
            x_length=11, y_length=5,
        ).shift(DOWN * 0.7)
        axes.get_x_axis_label(Text("t", font_size=28))

        w1 = axes.plot(lambda x: np.sin(TAU * x), x_range=[0, 4], color=BLUE)
        w2 = axes.plot(lambda x: 0.6 * np.sin(2 * TAU * x), x_range=[0, 4], color=GREEN)
        w3 = axes.plot(lambda x: 0.3 * np.sin(5 * TAU * x), x_range=[0, 4], color=PURPLE)
        wsum = axes.plot(
            lambda x: np.sin(TAU * x) + 0.6 * np.sin(2 * TAU * x) + 0.3 * np.sin(5 * TAU * x),
            x_range=[0, 4], color=WHITE, stroke_width=4)

        l1 = MathTex("1\\,\mathrm{Hz}", color=BLUE, font_size=30).move_to(axes.c2p(0.5, 1.8))
        l2 = MathTex("2\\,\mathrm{Hz}", color=GREEN, font_size=30).move_to(axes.c2p(1.5, 1.8))
        l3 = MathTex("5\\,\mathrm{Hz}", color=PURPLE, font_size=30).move_to(axes.c2p(2.5, 1.8))

        self.play(Write(title))
        self.play(Create(axes), run_time=1.5)
        self.play(Create(w1), Write(l1), run_time=1.5)
        self.play(Create(w2), Write(l2), run_time=1.5)
        self.play(Create(w3), Write(l3), run_time=1.5)
        self.play(w1.animate.set_opacity(0.3),
                  w2.animate.set_opacity(0.3),
                  w3.animate.set_opacity(0.3),
                  FadeOut(l1), FadeOut(l2), FadeOut(l3))
        self.play(Create(wsum), run_time=2)
        self.play(wsum.animate.set_color(YELLOW))
        note = Text("sum of pure tones = a richer signal", font_size=28
                    ).next_to(axes, DOWN, buff=0.3)
        self.play(Write(note))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(axes), FadeOut(w1), FadeOut(w2),
                  FadeOut(w3), FadeOut(wsum), FadeOut(note))
        self.clear()

        # ------------------------------------------------------------------
        # Scene 3: The central question — which frequencies hide inside?
        # ------------------------------------------------------------------
        title = Text("Step 2: The Central Question", color=ORANGE).to_edge(UP)
        q = Text("Given only the complicated signal...", font_size=30
                 ).to_edge(UP, buff=0.9)
        q2 = Text("...which simple tones is it made of?",
                  font_size=30, color=YELLOW).next_to(q, DOWN, buff=0.4)

        axes = Axes(
            x_range=[0, 4, 1], y_range=[-2.2, 2.2, 1],
            x_length=9, y_length=4,
        ).shift(DOWN * 0.9 + RIGHT * 2.5)
        sig = axes.plot(
            lambda x: np.sin(TAU * x) + 0.6 * np.sin(2 * TAU * x) + 0.3 * np.sin(5 * TAU * x),
            x_range=[0, 4], color=WHITE)

        ing1 = axes.plot(lambda x: np.sin(TAU * x), x_range=[0, 4], color=BLUE)
        ing2 = axes.plot(lambda x: 0.6 * np.sin(2 * TAU * x), x_range=[0, 4], color=GREEN)
        ing3 = axes.plot(lambda x: 0.3 * np.sin(5 * TAU * x), x_range=[0, 4], color=PURPLE)

        mystery = MathTex("x(t) = \\,?", font_size=60).shift(LEFT * 4 + DOWN * 1.5)
        box = SurroundingRectangle(mystery, color=RED)

        self.play(Write(title))
        self.play(Write(q))
        self.play(Create(axes), run_time=1.5)
        self.play(Create(sig), run_time=2.5)
        self.play(Write(q2))
        self.play(Write(mystery), Create(box))
        self.wait(0.5)
        self.play(Indicate(sig, color=YELLOW), run_time=1.5)

        guess1 = MathTex("\\sin(2\\pi t)", color=BLUE, font_size=36
                         ).move_to(axes.c2p(1.0, 1.6))
        guess2 = MathTex("0.6\\sin(4\\pi t)", color=GREEN, font_size=36
                         ).move_to(axes.c2p(2.0, 1.6))
        guess3 = MathTex("0.3\\sin(10\\pi t)", color=PURPLE, font_size=36
                         ).move_to(axes.c2p(3.0, 1.6))
        self.play(Create(ing1), Write(guess1), run_time=1.2)
        self.play(Create(ing2), Write(guess2), run_time=1.2)
        self.play(Create(ing3), Write(guess3), run_time=1.2)
        answer = Text("The Fourier transform answers this automatically!",
                      font_size=28, color=TEAL).to_edge(DOWN)
        self.play(Write(answer))
        self.wait(1)
        self.play(*[FadeOut(m) for m in [title, q, q2, axes, sig, ing1, ing2,
                                          ing3, mystery, box, guess1,
                                          guess2, guess3, answer]])
        self.clear()

        # ------------------------------------------------------------------
        # Scene 4: Probing the signal with a test frequency.
        # ------------------------------------------------------------------
        title = Text("Step 3: Probing with a Test Frequency",
                     color=TEAL).to_edge(UP)
        instr = Text("Sweep a pure tone across the signal and measure the response",
                     font_size=26).next_to(title, DOWN, buff=0.3)

        axes = Axes(
            x_range=[0, 4, 1], y_range=[-2.4, 2.4, 1],
            x_length=10, y_length=4.5,
        ).shift(DOWN * 0.9 + LEFT * 1.0)

        signal = axes.plot(
            lambda x: np.sin(TAU * x) + 0.6 * np.sin(2 * TAU * x) + 0.3 * np.sin(5 * TAU * x),
            x_range=[0, 4], color=WHITE)

        freq = ValueTracker(0.3)

        probe = always_redraw(
            lambda: axes.plot(
                lambda x: np.sin(TAU * freq.get_value() * x),
                x_range=[0, 4], color=YELLOW, stroke_width=5))

        def response(f):
            return (1.0 * np.exp(-((f - 1) / 0.15) ** 2)
                    + 0.6 * np.exp(-((f - 2) / 0.15) ** 2)
                    + 0.3 * np.exp(-((f - 5) / 0.15) ** 2))

        bar_base = np.array([6.2, -2.6, 0.0])
        bar = always_redraw(
            lambda: Rectangle(
                width=0.5,
                height=max(response(freq.get_value()), 0.02) * 3.0,
                fill_color=RED, fill_opacity=1, stroke_width=0,
            ).move_to(bar_base, aligned_edge=DOWN))
        bar_frame = Rectangle(width=0.6, height=3.2, color=GREY
                              ).move_to(bar_base + UP * 1.6)
        bar_title = Text("response", font_size=24).next_to(bar_frame, UP, buff=0.2)
        freq_num = always_redraw(
            lambda: DecimalNumber(freq.get_value(), num_decimal_places=2,
                                  color=YELLOW, font_size=36
                                  ).next_to(bar_frame, DOWN, buff=0.4))
        freq_lab = Text("test f (Hz)", font_size=22
                        ).next_to(freq_num, DOWN, buff=0.15)

        self.play(Write(title), Write(instr))
        self.play(Create(axes), run_time=1.5)
        self.play(Create(signal), run_time=2)
        self.play(Create(probe))
        self.play(Create(bar_frame), Write(bar_title), Write(freq_lab),
                  Create(bar), Create(freq_num))
        self.wait(0.5)

        hit1 = Text("resonance at 1 Hz!", font_size=26, color=RED
                    ).to_edge(DOWN).shift(LEFT * 3)
        self.play(freq.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.play(Write(hit1))
        self.play(freq.animate.set_value(2.0), run_time=2, rate_func=smooth)
        hit2 = Text("another at 2 Hz!", font_size=26, color=RED
                    ).next_to(hit1, DOWN, buff=0.2).align_to(hit1, LEFT)
        self.play(Write(hit2))
        self.play(freq.animate.set_value(5.0), run_time=3, rate_func=smooth)
        hit3 = Text("and a weak one at 5 Hz", font_size=26, color=RED
                    ).next_to(hit2, DOWN, buff=0.2).align_to(hit2, LEFT)
        self.play(Write(hit3))
        self.wait(1)
        self.clear()

        # ------------------------------------------------------------------
        # Scene 5: The spinning probe — complex exponentials.
        # ------------------------------------------------------------------
        title = Text("Step 4: A Spinning Probe", color=TEAL).to_edge(UP)
        sub = Text("e^{iωt} wraps the probe around the unit circle",
                   font_size=26).next_to(title, DOWN, buff=0.25)

        plane_axes = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                          x_length=6, y_length=6,
                          axis_config={"stroke_opacity": 0.4}).shift(LEFT * 3.5)
        circle = Circle(radius=2, color=BLUE).move_to(plane_axes.get_origin())
        formula = MathTex("e^{i\\omega t}",
                          "= \\cos(\\omega t) + i\\,\\sin(\\omega t)",
                          font_size=44).shift(RIGHT * 3.2 + UP * 0.5)
        formula[0].set_color(YELLOW)
        formula[1].set_color(WHITE)
        cos_lab = MathTex("\\text{real part: } \\cos", color=GREEN, font_size=30
                          ).next_to(formula, DOWN, buff=0.6).align_to(formula, LEFT)
        sin_lab = MathTex("\\text{imaginary part: } \\sin", color=PURPLE, font_size=30
                          ).next_to(cos_lab, DOWN, buff=0.3).align_to(cos_lab, LEFT)

        t = ValueTracker(0)

        def tip():
            a = TAU * t.get_value()
            return plane_axes.c2p(2 * np.cos(a), 2 * np.sin(a))

        vec = always_redraw(
            lambda: Arrow(plane_axes.get_origin(), tip(), buff=0, color=YELLOW))
        dot = always_redraw(lambda: Dot(tip(), color=YELLOW, radius=0.08))
        h_proj = always_redraw(
            lambda: DashedLine(tip(), plane_axes.c2p(2 * np.cos(TAU * t.get_value()), 0),
                               color=GREEN, stroke_width=3))
        v_proj = always_redraw(
            lambda: DashedLine(tip(), plane_axes.c2p(0, 2 * np.sin(TAU * t.get_value())),
                               color=PURPLE, stroke_width=3))

        self.play(Write(title), Write(sub))
        self.play(Create(plane_axes), Create(circle), run_time=1.5)
        self.play(Write(formula[0]))
        self.play(Create(vec), Create(dot), Create(h_proj), Create(v_proj))
        self.play(t.animate.set_value(1.0), run_time=4, rate_func=linear)
        self.play(Write(formula[1]), Write(cos_lab), Write(sin_lab))
        self.play(t.animate.set_value(3.0), run_time=4, rate_func=linear)
        note = Text("multiplying the signal by e^{-iωt} compares it to this rotation",
                    font_size=24).to_edge(DOWN)
        self.play(Write(note))
        self.wait(1)
        self.clear()

        # ------------------------------------------------------------------
        # Scene 6: The definition of the Fourier transform.
        # ------------------------------------------------------------------
        title = Text("Step 5: The Definition", color=TEAL).to_edge(UP)

        formula = MathTex(
            r"X(f)", r"= \int_{-\infty}^{\infty}",
            r"x(t)\, ", r"e^{-i\,2\pi f t}\,", r"dt",
            font_size=60).shift(UP * 0.6)
        formula[0].set_color(RED)
        formula[2].set_color(WHITE)
        formula[3].set_color(YELLOW)

        b1 = Brace(formula[0], UP, color=RED)
        t1 = Text("how much of frequency f", font_size=24,
                  color=RED).next_to(b1, UP)
        b2 = Brace(formula[2], DOWN, color=WHITE)
        t2 = Text("the signal", font_size=24).next_to(b2, DOWN)
        b3 = Brace(formula[3], DOWN, color=YELLOW)
        t3 = Text("the spinning probe", font_size=24,
                  color=YELLOW).next_to(b3, DOWN)

        self.play(Write(title))
        self.play(Write(formula[1]), Write(formula[4]))
        self.play(Write(formula[2]))
        self.play(Write(formula[3]))
        self.play(Write(formula[0]))
        self.wait(0.5)
        self.play(GrowFromCenter(b1), Write(t1))
        self.play(GrowFromCenter(b2), Write(t2))
        self.play(GrowFromCenter(b3), Write(t3))
        self.wait(0.5)

        explain = VGroup(
            Text("• integrate over all time: one number per frequency", font_size=26),
            Text("• a big |X(f)| means f is a strong ingredient", font_size=26),
            Text("• small |X(f)| means f is (almost) absent", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.5)
        self.play(Write(explain[0]))
        self.play(Write(explain[1]))
        self.play(Write(explain[2]))
        self.wait(1)
        self.clear()

        # ------------------------------------------------------------------
        # Scene 7: The spectrum — the signal seen through frequency glasses.
        # ------------------------------------------------------------------
        title = Text("Step 6: The Spectrum", color=TEAL).to_edge(UP)
        sub = Text("|X(f)| : the fingerprint of the signal",
                    font_size=28).next_to(title, DOWN, buff=0.25)

        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 1.3, 0.5],
            x_length=10, y_length=4.5,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.9)
        x_lab = axes.get_x_axis_label(Text("frequency f (Hz)", font_size=26))
        y_lab = axes.get_y_axis_label(Text("|X(f)|", font_size=26))

        freqs = [1, 2, 5]
        amps = [1.0, 0.6, 0.3]
        cols = [BLUE, GREEN, PURPLE]

        bars = VGroup()
        for f, a, c in zip(freqs, amps, cols):
            bar = Rectangle(width=0.35, height=a * 3.2,
                            fill_color=c, fill_opacity=1, stroke_width=0)
            bar.move_to(axes.c2p(f, 0), aligned_edge=DOWN)
            bars.add(bar)

        labels = VGroup(
            MathTex("1\\,\\mathrm{Hz}", font_size=30, color=BLUE
                    ).next_to(bars[0], UP, buff=0.15),
            MathTex("2\\,\\mathrm{Hz}", font_size=30, color=GREEN
                    ).next_to(bars[1], UP, buff=0.15),
            MathTex("5\\,\\mathrm{Hz}", font_size=30, color=PURPLE
                    ).next_to(bars[2], UP, buff=0.15),
        )

        self.play(Write(title), Write(sub))
        self.play(Create(axes), Write(x_lab), Write(y_lab), run_time=2)
        for bar, lab in zip(bars, labels):
            self.play(GrowFromEdge(bar, DOWN), FadeIn(lab, shift=UP),
                      run_time=1.0)
        self.wait(0.5)

        insight = Text("three clean spikes — the signal was exactly three tones!",
                       font_size=26, color=YELLOW).to_edge(DOWN)
        self.play(Write(insight))
        self.play(Circumscribe(VGroup(bars, labels), color=YELLOW))
        noisy = Text("noisy signals give smeared-out, continuous spectra",
                     font_size=22, color=GREY_B).next_to(insight, DOWN, buff=0.2)
        self.play(Write(noisy))
        self.wait(1)
        self.clear()

        # ------------------------------------------------------------------
        # Scene 8: The inverse transform — rebuilding the signal.
        # ------------------------------------------------------------------
        title = Text("Step 7: Reconstruction", color=TEAL).to_edge(UP)
        sub = Text("Add the ingredients back — nothing was lost!",
                    font_size=28).next_to(title, DOWN, buff=0.25)

        comps = [(1, 1.0), (2, 0.6), (5, 0.3)]

        def partial_sum(n):
            def f(x):
                s = 0.0
                for k in range(n):
                    fk, ak = comps[k]
                    s += ak * np.sin(TAU * fk * x)
                return s
            return f

        axes = Axes(
            x_range=[0, 4, 1], y_range=[-2.2, 2.2, 1],
            x_length=10, y_length=4,
        ).shift(DOWN * 1.0)

        step_lab = MathTex("").to_edge(DOWN)

        self.play(Write(title), Write(sub))
        self.play(Create(axes), run_time=1.5)

        c1 = axes.plot(partial_sum(1), x_range=[0, 4], color=BLUE)
        s1 = MathTex("x(t) \\approx \\sin(2\\pi t)", font_size=36,
                     color=BLUE).to_edge(DOWN)
        self.play(Create(c1), Write(s1), run_time=2)

        c2 = axes.plot(partial_sum(2), x_range=[0, 4], color=GREEN)
        s2 = MathTex("x(t) \\approx \\sin(2\\pi t) + 0.6\\sin(4\\pi t)",
                     font_size=36, color=GREEN).to_edge(DOWN)
        self.play(Transform(c1, c2), Transform(s1, s2), run_time=2)

        c3 = axes.plot(partial_sum(3), x_range=[0, 4], color=PURPLE)
        s3 = MathTex("x(t) = \\sin(2\\pi t) + 0.6\\sin(4\\pi t) + 0.3\\sin(10\\pi t)",
                     font_size=36, color=PURPLE).to_edge(DOWN)
        self.play(Transform(c1, c3), Transform(s1, s3), run_time=2)

        self.play(c1.animate.set_color(YELLOW).set_stroke(width=5))
        done = Text("the original signal is perfectly recovered",
                    font_size=28, color=YELLOW).to_edge(UP, buff=1.0)
        self.play(Write(done))
        self.wait(1)
        self.clear()

        # ------------------------------------------------------------------
        # Scene 9: Recap and where it's used.
        # ------------------------------------------------------------------
        title = Text("Fourier Transform: Summary", gradient=(BLUE, TEAL)).to_edge(UP)

        points = VGroup(
            Text("1. Any signal is a sum of pure frequencies.", font_size=30),
            Text("2. Multiply by a spinning probe  e^{-i2πft}.", font_size=30),
            Text("3. Integrate over time → the spectrum  X(f).", font_size=30),
            Text("4. The spectrum tells you exactly what's inside.", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP * 0.8)

        self.play(Write(title))
        for p in points:
            self.play(Write(p), run_time=1.2)
        self.wait(0.5)

        apps_title = Text("Used everywhere:", font_size=30, color=YELLOW
                          ).to_edge(DOWN, buff=1.6)
        apps = VGroup(
            Text("🎧 audio", font_size=28),
            Text("🖼️ images (JPEG)", font_size=28),
            Text("📡 communications", font_size=28),
            Text("🧲 MRI physics", font_size=28),
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.5)
        self.play(Write(apps_title))
        self.play(FadeIn(apps, shift=UP))
        self.wait(2)
        self.play(*[FadeOut(m) for m in [title, points, apps_title, apps]])
        self.clear()
