from manim import *

class SceneGen(Scene):
    def construct(self):
        # ------------------------------------------------------------
        # Scene 1: Introduction to waves – a simple sine wave
        # ------------------------------------------------------------
        title = Text("Step 1: What is a periodic wave?", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        axes = Axes(x_range=[0, 6], y_range=[-1.5, 1.5], x_length=10, y_length=3)
        axes_labels = axes.get_axis_labels(x_label="t", y_label="Amplitude")
        self.play(Create(axes), Write(axes_labels))
        self.wait(0.3)

        # Create a moving sine wave (source points and line)
        wave = always_redraw(lambda: ParametricFunction(
            lambda t: axes.coords_to_point(t, np.sin(2 * PI * 1.0 * t)),
            t_range=[0, 4], color=BLUE, stroke_width=3
        ))
        self.play(Create(wave))
        self.wait(0.5)

        # Show the wave train
        arrow = Arrow(start=axes.coords_to_point(0, 1.2), end=axes.coords_to_point(0.8, 1.2), color=YELLOW)
        peak_label = Text("peak", font_size=24, color=YELLOW).next_to(arrow, UP, buff=0.05)
        self.play(Write(arrow), Write(peak_label))
        self.wait(1)

        self.clear()

        # ------------------------------------------------------------
        # Scene 2: Introduce source and observer, stationary
        # ------------------------------------------------------------
        title2 = Text("Step 2: Stationary source, stationary observer", font_size=32).to_edge(UP)
        self.play(Write(title2))
        self.wait(0.3)

        source = Circle(radius=0.4, color=RED, fill_opacity=0.8).shift(LEFT * 4)
        source_label = Text("Source", font_size=24, color=RED).next_to(source, DOWN)
        self.play(FadeIn(source), Write(source_label))
        self.wait(0.5)

        observer = Circle(radius=0.3, color=GREEN, fill_opacity=0.8).shift(RIGHT * 4 + UP * 0.5)
        observer_label = Text("Observer", font_size=24, color=GREEN).next_to(observer, DOWN)
        self.play(FadeIn(observer), Write(observer_label))
        self.wait(0.5)

        # Draw some wavefronts between them
        wavefronts = VGroup()
        for i in range(5):
            radius = 0.6 + i * 0.6
            circle = Circle(radius=radius, color=BLUE, stroke_width=2).move_to(source.get_center())
            wavefronts.add(circle)
        self.play(LaggedStartMap(Create, wavefronts, lag_ratio=0.3), run_time=2)
        self.wait(1)

        wf_text = Text("Constant wavelength λ₀", font_size=28).to_edge(DOWN)
        self.play(Write(wf_text))
        self.wait(1.5)

        self.clear()

        # ------------------------------------------------------------
        # Scene 3: Source moves – visualise compression in front
        # ------------------------------------------------------------
        title3 = Text("Step 3: Moving source → wavefront crowding", font_size=32).to_edge(UP)
        self.play(Write(title3))
        self.wait(0.3)

        moving_source = Circle(radius=0.4, color=RED, fill_opacity=0.8).move_to(LEFT * 4)
        source_label2 = Text("Source (moving right)", font_size=24, color=RED).next_to(moving_source, DOWN)
        self.play(FadeIn(moving_source), Write(source_label2))
        self.wait(0.3)

        # Generate a ring every 0.5 sec while moving
        rings = VGroup()
        for step in range(6):
            r = Circle(radius=0.5, color=BLUE, stroke_width=2)
            r.move_to(LEFT * 4 + RIGHT * step * 0.3)  # source shifted
            rings.add(r)
        # Show them with a small offset to simulate crowding
        self.play(LaggedStartMap(Create, rings, lag_ratio=0.25, run_time=2))
        self.wait(0.5)

        # Animate the source moving right a bit more
        self.play(
            moving_source.animate.shift(RIGHT * 1.5),
            rings[-1].animate.shift(RIGHT * 1.5),
            run_time=1.5
        )
        self.wait(0.5)

        # Add a compression indicator on the right side
        compress_arrow = DoubleArrow(start=rings[3].get_right() + DOWN * 1.5,
                                     end=rings[4].get_right() + DOWN * 1.5,
                                     color=YELLOW)
        compress_label = Text("Compressed", font_size=24, color=YELLOW).next_to(compress_arrow, DOWN)
        self.play(Create(compress_arrow), Write(compress_label))
        self.wait(1.5)

        self.clear()

        # ------------------------------------------------------------
        # Scene 4: Observer moving toward source – perceived frequency
        # ------------------------------------------------------------
        title4 = Text("Step 4: Observer moves toward source", font_size=32).to_edge(UP)
        self.play(Write(title4))
        self.wait(0.3)

        fixed_source = Circle(radius=0.4, color=RED, fill_opacity=0.8).shift(LEFT * 4)
        src_lbl = Text("Source (stationary)", font_size=24, color=RED).next_to(fixed_source, DOWN)
        self.play(FadeIn(fixed_source), Write(src_lbl))
        self.wait(0.5)

        moving_ob = Circle(radius=0.3, color=GREEN, fill_opacity=0.8).shift(RIGHT * 3)
        ob_lbl = Text("Observer (moving left)", font_size=24, color=GREEN).next_to(moving_ob, DOWN)
        self.play(FadeIn(moving_ob), Write(ob_lbl))
        self.wait(0.3)

        # Create static wavefronts
        fwaves = VGroup()
        for i in range(4):
            circ = Circle(radius=0.7 + i * 0.7, color=BLUE, stroke_width=2).move_to(fixed_source.get_center())
            fwaves.add(circ)
        self.play(*[Create(c) for c in fwaves], run_time=1.5)
        self.wait(0.3)

        # Animate the observer moving left across the wavefronts
        self.play(
            moving_ob.animate.shift(LEFT * 3.5),
            ob_lbl.animate.shift(LEFT * 3.5),
            run_time=2
        )
        self.wait(0.5)

        freq_text = Text("Observer meets wavefronts more often → higher perceived frequency", font_size=26, color=YELLOW).to_edge(DOWN)
        self.play(Write(freq_text))
        self.wait(2)

        self.clear()

        # ------------------------------------------------------------
        # Scene 5: Summary with formulas and visual
        # ------------------------------------------------------------
        title5 = Text("Doppler Effect: Summary", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title5))
        self.wait(0.3)

        # Show the idea of frequency shift
        eqn = MathTex(r"f_{\text{obs}} = f_{\text{src}} \frac{v \pm v_{\text{obs}}}{v \mp v_{\text{src}}}", font_size=40).shift(UP * 0.5)
        self.play(Write(eqn))
        self.wait(1)

        bullet1 = Text("Source moves toward observer → compression → higher pitch", font_size=26).next_to(eqn, DOWN, buff=0.8)
        bullet2 = Text("Observer moves toward source → more wavefronts per sec → higher pitch", font_size=26).next_to(bullet1, DOWN, buff=0.3)
        bullet3 = Text("Motion away → lower pitch", font_size=26).next_to(bullet2, DOWN, buff=0.3)
        self.play(Write(bullet1), Write(bullet2), Write(bullet3))
        self.wait(1.5)

        # Final visual: a moving source with rings
        final_source = Circle(radius=0.4, color=RED, fill_opacity=0.8).shift(LEFT * 3)
        rad = 0.5
        for i in range(4):
            r = Circle(radius=rad + i*0.4, color=BLUE, stroke_width=2).move_to(final_source.get_center()+RIGHT*i*0.3)
            self.play(Create(r), run_time=0.3)
        self.play(final_source.animate.shift(RIGHT*0.5), run_time=1)
        self.wait(1)

        final_text = Text("Doppler effect: shifts in frequency due to relative motion", font_size=28, color=GREEN).to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)

        self.clear()

        # ------------------------------------------------------------
        # Scene 6: Real-world examples (no new objects needed)
        # ------------------------------------------------------------
        title6 = Text("Everyday examples", font_size=34).to_edge(UP)
        self.play(Write(title6))
        self.wait(0.3)

        ex1 = Text("• Ambulance siren: higher pitch when approaching, lower when moving away", font_size=26).shift(UP*1)
        ex2 = Text("• Radar speed guns: reflected wave frequency shift gives speed", font_size=26).next_to(ex1, DOWN, buff=0.5)
        ex3 = Text("• Redshift / Blueshift in astronomy (light Doppler)", font_size=26).next_to(ex2, DOWN, buff=0.5)
        self.play(FadeIn(ex1, shift=DOWN), FadeIn(ex2, shift=DOWN), FadeIn(ex3, shift=DOWN), run_time=2)
        self.wait(2)

        final_arrow = Arrow(start=LEFT*3, end=RIGHT*3, color=YELLOW)
        final_label = Text("Relative motion → Frequency shift", font_size=30, color=YELLOW).next_to(final_arrow, UP)
        self.play(Create(final_arrow), Write(final_label))
        self.wait(2)

        self.clear()

        # ------------------------------------------------------------
        # Scene 7: Quick animation showing the full effect
        # ------------------------------------------------------------
        title7 = Text("Picturing the shift", font_size=34).to_edge(UP)
        self.play(Write(title7))
        self.wait(0.3)

        # A simple moving source emitting rings
        src = Circle(radius=0.3, color=RED).shift(LEFT*3)
        self.play(FadeIn(src))
        rings_final = VGroup()
        for i in range(6):
            c = Circle(radius=0.4 + i*0.5, color=BLUE, stroke_width=2).move_to(src.get_center()+RIGHT*i*0.2)
            rings_final.add(c)
        self.play(LaggedStartMap(Create, rings_final, lag_ratio=0.2), run_time=2)
        self.play(src.animate.shift(RIGHT*1.5), run_time=1.5)
        self.wait(0.5)

        # Show compressed front
        front_circle = Circle(radius=0.5, color=YELLOW, stroke_width=4).move_to(src.get_center()+RIGHT*1.5)
        self.play(Create(front_circle))
        self.wait(1)

        conclude = Text("Same physicist, same effect", font_size=28, color=GREEN).to_edge(DOWN)
        self.play(Write(conclude))
        self.wait(2)

        self.clear()

        # ------------------------------------------------------------
        # Scene 8: final quiz question to reinforce
        # ------------------------------------------------------------
        title8 = Text("Quick check:", font_size=34).to_edge(UP)
        self.play(Write(title8))
        self.wait(0.3)

        q = Text("Q: A source emits 440 Hz. An observer moves toward it at 10 m/s.\nSound speed 340 m/s. What frequency does the observer hear?", font_size=26).shift(UP*0.5)
        self.play(Write(q))
        self.wait(1)

        # Simulate answer
        answer = MathTex(r"f_{\text{obs}} = 440 \cdot \frac{340+10}{340} = 452.9\ \text{Hz}", font_size=34, color=YELLOW).shift(DOWN*1.5)
        self.play(Write(answer))
        self.wait(2)

        final_words = Text("Higher pitch when approaching!", font_size=30, color=GREEN).to_edge(DOWN)
        self.play(Write(final_words))
        self.wait(3)

        self.clear()

        # ------------------------------------------------------------
        # Scene 9: wrap-up
        # ------------------------------------------------------------
        wrap = Text("Doppler effect: frequency shift due to relative motion", font_size=32, color=BLUE).shift(UP)
        self.play(Write(wrap))
        self.wait(0.5)

        waves_final = VGroup(*[
            Circle(radius=i*0.5, color=BLUE, stroke_width=2).move_to(ORIGIN + LEFT*0.5)
            for i in range(1, 5)
        ])
        self.play(LaggedStartMap(Create, waves_final, lag_ratio=0.3), run_time=1.5)
        self.wait(1)

        thanks = Text("Thanks for learning! Try the formula with different numbers.", font_size=24).to_edge(DOWN)
        self.play(Write(thanks))
        self.wait(3)

        self.clear()

        # ------------------------------------------------------------
        # Scene 10: Final tweetable takeaway
        # ------------------------------------------------------------
        final_title = Text("Doppler Effect in one shot", font_size=36, color=MAROON).to_edge(UP)
        self.play(Write(final_title))
        self.wait(0.3)

        note = Text(
            "Source and observer: their relative motion changes the\n"
            "number of wavefronts encountered per second.\n"
            "That's the Doppler Effect.",
            font_size=28, color=GREY
        ).shift(UP*0.5)
        self.play(FadeIn(note, scale=0.9))
        self.wait(1.5)

        icon = Circle(radius=0.8, color=BLUE).shift(DOWN*1.5)
        icon_label = Text("f obs ≠ f src", font_size=30).move_to(icon.get_center())
        self.play(Create(icon), Write(icon_label))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.5)