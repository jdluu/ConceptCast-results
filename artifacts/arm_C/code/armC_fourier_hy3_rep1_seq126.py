import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: A signal as a function of time ---
        self.clear()
        # --- Scene 1: A signal as a function of time ---
        self.camera.background_color = "#181825"
        self.clear()

        # --- Title ---
        title = Text(
            "A Signal as a Function of Time", font="Sans", font_size=40, color="#CDD6F4"
        )
        title.to_edge(UP, buff=0.4)

        # --- Axes (time horizontal, amplitude vertical) ---
        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-2, 2, 1],
            x_length=9,
            y_length=4,
            axis_config={
                "stroke_width": 2.0,
                "color": "#A6ADC8",
                "include_tip": True,
            },
            tips=True,
        )

        time_label = axes.get_x_axis_label(Tex("Time $\\rightarrow$", color="#94e2d5"))
        # FIX: get_y_axis_label() does not accept 'rotation' in this Manim version.
        # Manually create the label upright (equivalent to rotation=0) and position it.
        amplitude_label = Tex("Amplitude $\\uparrow$", color="#fab387")
        amplitude_label.next_to(axes.get_y_axis(), LEFT, buff=0.2)
        amplitude_label.to_edge(UP, buff=0.3)

        # --- Signal wave: a value changing over time ---
        def sig_func(x):
            return 1.5 * np.sin(x) + 0.6 * np.sin(2.3 * x) + 0.3 * np.sin(4.1 * x)

        signal_wave = axes.plot(sig_func, color="#89b4fa", stroke_width=4)

        # --- Glowing sample point that rides the curve ---
        sample_dot = Dot(radius=0.12, color="#f38ba8")
        halo_outer = Circle(
            radius=0.45, color="#f38ba8", fill_opacity=0.12, stroke_width=0
        )
        halo_mid = Circle(
            radius=0.28, color="#f38ba8", fill_opacity=0.22, stroke_width=0
        )
        sample_label = Text("sample point", font="Sans", font_size=18, color="#f38ba8")
        glow = VGroup(halo_outer, halo_mid, sample_dot, sample_label)

        dot_tracker = ValueTracker(-3.0)

        def update_glow(g):
            x = dot_tracker.get_value()
            p = axes.i2gp(x, signal_wave)
            halo_outer.move_to(p)
            halo_mid.move_to(p)
            sample_dot.move_to(p)
            sample_label.next_to(p, UP, buff=0.35)

        glow.add_updater(update_glow)

        # --- Animations (total = 13.0s) ---
        self.play(Write(title), run_time=1.0)
        self.play(Create(axes), run_time=1.5)
        self.play(FadeIn(time_label), FadeIn(amplitude_label), run_time=1.0)
        self.play(Create(signal_wave), run_time=3.0)
        self.play(FadeIn(glow), run_time=0.5)
        self.play(dot_tracker.animate.set_value(1.0), run_time=5.0)
        self.wait(1.0)
        # --- Scene 2: Complex signals are sums of simple waves ---
        self.camera.background_color = "#181825"
        self.clear()

        # --- Title ---
        title = Text(
            "Complex Signals = Sum of Simple Waves",
            font_size=32,
            color="#CDD6F4",
        ).to_edge(UP, buff=0.4)

        # --- Wave functions (frequency increases: low -> mid -> high) ---
        def f_low(x):
            return 0.40 * np.sin(x)

        def f_mid(x):
            return 0.28 * np.sin(2.0 * x)

        def f_high(x):
            return 0.12 * np.sin(4.5 * x)

        def f_combined(x):
            return f_low(x) + f_mid(x) + f_high(x)

        x_range = [-4.5, 4.5]

        # --- Three stacked pure waves (upper region) ---
        wave_low = FunctionGraph(
            f_low, x_range=x_range, color="#fab387", stroke_width=3
        ).shift(UP * 2.4)
        wave_mid = FunctionGraph(
            f_mid, x_range=x_range, color="#94e2d5", stroke_width=3
        ).shift(UP * 0.8)
        wave_high = FunctionGraph(
            f_high, x_range=x_range, color="#f38ba8", stroke_width=3
        ).shift(DOWN * 0.8)

        label_low = Text("low freq", font_size=22, color="#fab387").next_to(
            wave_low, RIGHT, buff=0.4
        )
        label_mid = Text("mid freq", font_size=22, color="#94e2d5").next_to(
            wave_mid, RIGHT, buff=0.4
        )
        label_high = Text("high freq", font_size=22, color="#f38ba8").next_to(
            wave_high, RIGHT, buff=0.4
        )

        # --- Combination arrow + composite wave (lower region) ---
        combine_arrow = Arrow(
            start=DOWN * 1.5, end=DOWN * 2.3, color="#A6ADC8", stroke_width=4, buff=0.1
        )
        combined_wave = FunctionGraph(
            f_combined, x_range=x_range, color="#89b4fa", stroke_width=5
        ).shift(DOWN * 3.0)
        label_sum = MathTex(r"f(t) = \sum", color="#89b4fa", font_size=26).next_to(
            combined_wave, RIGHT, buff=0.4
        )

        # --- Animation sequence (total = 10.5s) ---
        self.play(Write(title), run_time=1.5)
        self.play(Create(wave_low), FadeIn(label_low, shift=LEFT * 0.2), run_time=1.5)
        self.play(Create(wave_mid), FadeIn(label_mid, shift=LEFT * 0.2), run_time=1.5)
        self.play(Create(wave_high), FadeIn(label_high, shift=LEFT * 0.2), run_time=1.5)
        self.play(GrowArrow(combine_arrow), run_time=0.8)
        self.play(
            Create(combined_wave), FadeIn(label_sum, shift=LEFT * 0.2), run_time=1.5
        )
        self.play(ShowPassingFlash(combined_wave, time_width=0.4, run_time=0.7))
        self.wait(1.5)
        # --- Scene 3: Sine and cosine waves as basis functions ---
        self.camera.background_color = "#181825"
        self.clear()

        palette = {
            "blue": "#89b4fa",
            "peach": "#fab387",
            "teal": "#94e2d5",
            "red": "#f38ba8",
            "green": "#a6e3a1",
            "text": "#CDD6F4",
            "sub": "#a6adc8",
        }

        # ---- Title ----
        title = Text(
            "Sine & Cosine as Basis Functions",
            font_size=40,
            color=palette["text"],
        ).to_edge(UP, buff=0.5)
        if title.width > 13:
            title.scale_to_fit_width(13)

        # ---- Basis function definitions (left to right) ----
        centers = [(-6, 0, 0), (-3, 0, 0), (0, 0, 0), (3, 0, 0), (6, 0, 0)]
        specs = [
            (lambda x: np.sin(x), 1, palette["blue"]),
            (lambda x: np.cos(2 * x), 2, palette["peach"]),
            (lambda x: np.sin(3 * x), 3, palette["teal"]),
            (lambda x: np.cos(4 * x), 4, palette["red"]),
            (lambda x: np.sin(5 * x), 5, palette["green"]),
        ]

        cells = []
        labels = []
        label_colors = []
        for (cx, cy, _), (func, w, color) in zip(centers, specs):
            center = np.array([cx, cy, 0])
            frame = RoundedRectangle(
                width=1.9,
                height=1.7,
                corner_radius=0.15,
                stroke_color=color,
                stroke_width=2.5,
                fill_color="#1e1e2e",
                fill_opacity=0.65,
            ).move_to(center)

            wave = FunctionGraph(
                func, x_range=[-1.6, 1.6], color=color, stroke_width=3.5
            )
            wave.scale(0.5).move_to(center)

            label = MathTex(rf"\omega = {w}", color=color).scale(0.5 + 0.06 * w)
            label.next_to(frame, DOWN, buff=0.2)

            cells.append(VGroup(frame, wave, label))
            labels.append(label)
            label_colors.append(color)

        # ---- Increasing-frequency arrow ----
        arrow = Arrow(
            start=LEFT * 5.4,
            end=RIGHT * 5.4,
            color="#a6adc8",
            stroke_width=2,
            tip_length=0.2,
            buff=0.3,
        ).shift(DOWN * 1.9)
        arrow_label = Text("Increasing frequency", font_size=22, color="#a6adc8")
        arrow_label.next_to(arrow, DOWN, buff=0.15)

        # ---- Caption ----
        caption = Text(
            "Pure sine & cosine waves are basis functions \u2014 each with a fixed frequency, from low to high.",
            font_size=24,
            color=palette["sub"],
        ).to_edge(DOWN, buff=0.4)
        if caption.width > 13:
            caption.scale_to_fit_width(13)

        # ================= ANIMATIONS =================
        # 1. Title
        self.play(Write(title), run_time=1.5)
        self.wait(0.2)

        # 2. Reveal basis cells left-to-right
        for cell in cells:
            self.play(
                FadeIn(cell[0]),
                Create(cell[1]),
                Write(cell[2]),
                run_time=0.8,
            )

        # 3. Frequency direction indicator
        self.play(Write(arrow), Write(arrow_label), run_time=0.8)
        self.wait(0.1)

        # 4. Caption
        self.play(Write(caption), run_time=1.0)
        self.wait(0.1)

        # 5. Emphasize the growing frequencies
        self.play(
            LaggedStart(
                *[
                    Indicate(lbl, color=label_colors[i], scale_factor=1.25)
                    for i, lbl in enumerate(labels)
                ],
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )

        self.wait(1.8)
        # --- Scene 4: Frequency and amplitude of components ---
        self.clear()
        self.camera.background_color = "#181825"

        values = [3.0, 5.0, 2.0, 6.0, 4.0, 1.0]
        bar_colors = ["#89b4fa", "#fab387", "#94e2d5", "#f38ba8", "#a6e3a1", "#A6ADC8"]

        title = Text(
            "Frequency & Amplitude of Components",
            color="#CDD6F4",
            font_size=32,
            font="Sans",
        )
        title.to_edge(UP, buff=0.4)

        barchart = BarChart(
            values,
            bar_names=[f"f{i + 1}" for i in range(len(values))],
            y_range=[0, 7],
            x_length=9,
            y_length=4,
            bar_colors=bar_colors,
            bar_width=0.6,
        )
        barchart.move_to(ORIGIN).shift(DOWN * 0.4)

        freq_label = Tex("Frequency $\\rightarrow$", color="#94e2d5", font_size=30)
        freq_label.next_to(barchart, DOWN, buff=0.4)
        amp_label = Tex("Amplitude $\\uparrow$", color="#fab387", font_size=30)
        amp_label.next_to(barchart, LEFT, buff=0.5)

        value_labels = VGroup()
        for i, val in enumerate(values):
            bar = barchart.bars[i]
            lbl = Text(str(val), font_size=20, color="#CDD6F4", font="Sans")
            lbl.next_to(bar, UP, buff=0.15)
            value_labels.add(lbl)

        dominant = Text("Strong presence", font_size=22, color="#f38ba8", font="Sans")
        dominant.next_to(value_labels[3], UP, buff=0.3)
        weak = Text("Weak presence", font_size=22, color="#A6ADC8", font="Sans")
        weak.next_to(value_labels[5], UP, buff=0.3)

        # Animations
        self.play(FadeIn(title), run_time=0.8)
        self.play(Create(barchart), run_time=1.8)
        self.play(FadeIn(freq_label), FadeIn(amp_label), run_time=1.0)
        self.play(
            LaggedStart(*[Write(l) for l in value_labels], lag_ratio=0.15), run_time=1.4
        )
        self.play(
            Circumscribe(barchart.bars[3], color="#f38ba8", shape=Rectangle),
            FadeIn(dominant, shift=UP * 0.3),
            run_time=1.2,
        )
        self.play(
            Circumscribe(barchart.bars[5], color="#A6ADC8", shape=Rectangle),
            FadeIn(weak, shift=UP * 0.3),
            run_time=1.0,
        )
        self.wait(1.3)
        # --- Scene 5: The Fourier transform maps time to frequency ---
        self.clear()
        self.camera.background_color = "#181825"

        # ----- Palette -----
        c_blue = "#89b4fa"
        c_orange = "#fab387"
        c_teal = "#94e2d5"
        c_red = "#f38ba8"
        c_green = "#a6e3a1"
        c_muted = "#A6ADC8"
        c_text = "#CDD6F4"
        c_glow = "#f9e2af"

        # ----- Title -----
        title = Text(
            "The Fourier Transform: Time to Frequency",
            font_size=32,
            color=c_text,
        ).to_edge(UP, buff=0.4)

        # ===== 1. TIME-DOMAIN PANEL (left) =====
        time_axes = Axes(
            x_range=[-2.5, 2.5, 0.5],
            y_range=[-2, 2, 1],
            x_length=4.5,
            y_length=3,
            axis_config={"color": c_muted, "stroke_width": 2},
        ).shift(LEFT * 4.5)

        time_graph = time_axes.plot(
            lambda x: np.sin(x) + 0.5 * np.sin(3 * x),
            x_range=[-2.2, 2.2],
            color=c_blue,
            stroke_width=4,
        )
        time_label = Text("time domain", font_size=22, color=c_blue).next_to(
            time_axes, DOWN, buff=0.35
        )
        time_x_label = time_axes.get_x_axis_label(
            Text("Time", color=c_muted, font_size=18)
        )
        time_y_label = time_axes.get_y_axis_label(
            Text("Amplitude", color=c_muted, font_size=18)
        )

        # ===== 2. TRANSFORM BOX (center) =====
        box = Rectangle(width=2.2, height=1.6, color=c_orange, stroke_width=3)
        box_label = MathTex(r"\mathcal{F}\{\}", color=c_orange).scale(1.1)
        box_sub = Text("Transform", font_size=18, color=c_orange).next_to(
            box_label, DOWN, buff=0.1
        )
        box_group = VGroup(box, box_label, box_sub)

        # ===== 3. FREQUENCY SPECTRUM (right) =====
        bar_chart = BarChart(
            values=[4.0, 1.0, 6.0, 1.5, 2.0],
            bar_names=["f1", "f2", "f3", "f4", "f5"],
            bar_colors=[c_blue, c_orange, c_teal, c_red, c_green],
            bar_width=0.4,
            x_length=4,
            y_length=4,
            y_range=[0, 7],
        ).shift(RIGHT * 4.5)
        freq_label = Text("frequency spectrum", font_size=22, color=c_teal).next_to(
            bar_chart, UP, buff=0.35
        )
        freq_x_label = bar_chart.get_x_axis_label(
            Text("Frequency", color=c_muted, font_size=18)
        )
        freq_y_label = bar_chart.get_y_axis_label(
            Text("Amplitude", color=c_muted, font_size=18)
        )

        # ===== 4. ARROWS =====
        arrow_in = Arrow(
            start=(-3.0, 0, 0),
            end=(-1.4, 0, 0),
            stroke_width=4,
            color=c_muted,
            buff=0.05,
        )
        arrow_out = Arrow(
            start=(1.4, 0, 0),
            end=(3.0, 0, 0),
            stroke_width=4,
            color=c_muted,
            buff=0.05,
        )

        # Tracer dot that visually "flows" through the transform
        tracer = Dot(point=arrow_in.get_start(), radius=0.12, color=c_glow)

        # Bottom caption
        caption = Text(
            "maps a time-domain signal  ->  a spectrum of amplitudes vs. frequency",
            font_size=22,
            color=c_text,
        ).to_edge(DOWN, buff=0.4)

        # ================= ANIMATIONS (total = 10.0s) =================

        # Step 1 (1.5s): Title, box, arrows
        self.play(
            Write(title),
            Create(box),
            Write(box_label),
            Write(box_sub),
            Create(arrow_in),
            Create(arrow_out),
            run_time=1.5,
        )

        # Step 2 (1.5s): Time panel
        self.play(
            Create(time_axes),
            Create(time_graph),
            Write(time_label),
            FadeIn(time_x_label),
            FadeIn(time_y_label),
            run_time=1.5,
        )

        # Step 3 (0.5s): Tracer appears at input
        self.play(GrowFromCenter(tracer), run_time=0.5)

        # Step 4 (1.0s): Tracer flows into the box
        self.play(tracer.animate.move_to(arrow_in.get_end()), run_time=1.0)

        # Step 5 (0.8s): Box processes + signal flash along wave
        self.play(
            tracer.animate.move_to(ORIGIN),
            Indicate(box, color=c_glow, scale_factor=1.15),
            ShowPassingFlash(time_graph.copy().set_color(c_glow)),
            run_time=0.8,
        )

        # Step 6 (1.0s): Tracer flows out toward spectrum
        self.play(tracer.animate.move_to(arrow_out.get_end()), run_time=1.0)

        # Step 7 (1.5s): Spectrum emerges, tracer consumed
        self.play(
            FadeOut(tracer),
            Create(bar_chart),
            Write(freq_label),
            FadeIn(freq_x_label),
            FadeIn(freq_y_label),
            run_time=1.5,
        )

        # Step 8 (1.2s): Highlight result + reveal caption
        self.play(
            Indicate(bar_chart, color=c_teal, scale_factor=1.05),
            Write(caption),
            run_time=1.2,
        )

        # Step 9: Hold
        self.wait(1.0)
        # --- Scene 6: Correlation with complex exponentials ---
        self.clear()
        # --- Scene 6: Correlation with complex exponentials ---
        self.camera.background_color = "#181825"

        BLUE = "#89b4fa"
        ORANGE = "#fab387"
        GREEN = "#a6e3a1"
        PINK = "#f38ba8"
        TEAL = "#94e2d5"
        GRAY = "#A6ADC8"
        TEXT = "#CDD6F4"

        # ---------- Title ----------
        title = Text(
            "Correlation with Complex Exponentials",
            font="Sans",
            color=TEXT,
            font_size=30,
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.9)
        self.wait(0.1)

        # ---------- Rotating vectors (complex exponentials e^{i*omega*t}) ----------
        centers = [
            np.array([-4.0, 1.6, 0.0]),
            np.array([-4.0, 0.0, 0.0]),
            np.array([-4.0, -1.6, 0.0]),
        ]
        freqs = [1, 3, 5]  # increasing frequencies
        colors = [BLUE, ORANGE, GREEN]
        radius = 1.0

        circles = VGroup()
        freq_labels = VGroup()
        vectors = VGroup()
        dots = VGroup()
        traces = VGroup()
        for c, f, col in zip(centers, freqs, colors):
            circ = Circle(radius=radius, color=GRAY, stroke_width=2).move_to(c)
            circles.add(circ)

            flabel = MathTex(r"\omega = %d" % f, color=col, font_size=22)
            flabel.next_to(circ, LEFT, buff=0.35)
            freq_labels.add(flabel)

            tip = c + np.array([radius, 0.0, 0.0])
            vec = Arrow(c, tip, color=col, stroke_width=4, buff=0.0)
            vectors.add(vec)

            dot = Dot(tip, radius=0.12, color=col)
            dots.add(dot)

            # FIX: removed invalid kwarg `min_distance_to_new_point`
            trace = TracedPath(
                dot.get_center,
                stroke_color=col,
                stroke_width=3,
            )
            traces.add(trace)

        self.play(Create(circles), Write(freq_labels), run_time=0.9)

        # ---------- Signal reference on the right ----------
        axes = Axes(
            x_range=[-2.5, 2.5, 1.0],
            y_range=[-2.0, 2.0, 1.0],
            x_length=4.5,
            y_length=3.6,
            axis_config={"color": GRAY, "stroke_width": 2},
        ).shift(RIGHT * 3.5)

        signal = axes.plot(
            lambda x: np.sin(x) + 0.5 * np.sin(3 * x),
            x_range=[-2.5, 2.5],
            color=TEAL,
            stroke_width=4,
        )
        signal_label = MathTex(r"f(t)", color=TEAL, font_size=24)
        signal_label.next_to(axes, UP, buff=0.1)

        caption = Text(
            "Correlation measures how much the signal aligns with each rotating vector",
            font="Sans",
            color="#BACDDC",
            font_size=18,
        ).to_edge(DOWN, buff=0.3)

        self.play(
            Create(axes),
            Create(signal),
            Write(signal_label),
            Write(caption),
            run_time=0.9,
        )
        self.wait(0.1)

        # ---------- Central projection / correlation result ----------
        corr_dot = Dot(point=ORIGIN, radius=0.12, color=PINK)
        corr_label = Text("projection", font="Sans", color=PINK, font_size=18)
        corr_label.next_to(corr_dot, UP, buff=0.25)
        flow = DashedLine(
            axes.c2p(0, 0), ORIGIN, color=GRAY, stroke_width=1.5, dash_length=0.15
        )

        self.play(
            *[GrowFromCenter(vec) for vec in vectors],
            *[GrowFromCenter(dot) for dot in dots],
            *[Create(tr) for tr in traces],
            GrowFromCenter(corr_dot),
            Write(corr_label),
            Create(flow),
            run_time=0.9,
        )
        self.wait(0.1)

        # ---------- Spin the vectors: correlation with e^{i*omega*t} ----------
        self.play(
            *[
                Rotate(vec, angle=TAU, about_point=c, rate_func=linear)
                for vec, c in zip(vectors, centers)
            ],
            *[
                Rotate(dot, angle=TAU, about_point=c, rate_func=linear)
                for dot, c in zip(dots, centers)
            ],
            run_time=4.0,
        )

        # ---------- Highlight the resulting projection ----------
        self.play(Indicate(corr_dot, color=PINK, scale_factor=1.6), run_time=0.5)
        self.wait(0.6)
        # --- Scene 7: Inverse Fourier transform ---
        self.clear()
        self.camera.background_color = "#181825"

        # Palette (Catppuccin Mocha inspired)
        BLUE = "#89b4fa"
        PEACH = "#fab387"
        RED = "#f38ba8"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"
        TEXT = "#CDD6F4"
        GREY = "#A6ADC8"
        bar_colors = [BLUE, PEACH, TEAL, RED, GREEN]

        # 1. Title
        title_text = Text("Inverse Fourier Transform", color=TEXT, font_size=40)
        title_text.to_edge(UP, buff=0.4)

        # 2. Spectrum (BarChart) on the left
        spectrum = BarChart(
            values=[4.0, 1.0, 6.0, 1.5, 2.0],
            bar_colors=bar_colors,
            y_range=[0, 7, 1],
            x_length=4,
            y_length=4,
            bar_width=0.4,
        )
        spectrum.move_to([-5, 0, 0])
        label_spectrum = Text("Frequency\nSpectrum", color=TEAL, font_size=24)
        label_spectrum.next_to(spectrum, DOWN, buff=0.4)

        # 3. Summation node (Sigma circle) at center
        sum_circle = Circle(radius=1.0, color=PEACH, stroke_width=4, fill_opacity=0.15)
        sigma_label = MathTex(r"\Sigma", color=TEXT, font_size=64)
        sum_node = VGroup(sum_circle, sigma_label)

        # 4. Rebuilt wave (FunctionGraph) on the right
        rebuilt_wave = FunctionGraph(
            lambda x: np.sin(x) + 0.5 * np.sin(3 * x),
            x_range=[-2.2, 2.2],
            color=BLUE,
            stroke_width=4,
        )
        rebuilt_wave.shift(RIGHT * 5)
        label_wave = Text("Time Signal", color=BLUE, font_size=24)
        label_wave.next_to(rebuilt_wave, DOWN, buff=0.5)

        # 5. Arrows
        arrow_feed = Arrow(
            start=[-3.6, 0, 0],
            end=[-1.1, 0, 0],
            color=GREY,
            stroke_width=4,
        )
        arrow_out = Arrow(
            start=[1.1, 0, 0],
            end=[3.6, 0, 0],
            color=GREY,
            stroke_width=4,
        )

        # Flowing dots (frequency components)
        feed_dots = VGroup(
            *[
                Dot(point=arrow_feed.get_start(), radius=0.12, color=c)
                for c in bar_colors
            ]
        )
        out_dots = VGroup(
            *[
                Dot(point=arrow_out.get_start(), radius=0.12, color=c)
                for c in bar_colors
            ]
        )

        # Formula (inverse FT)
        formula = MathTex(
            r"x(t)=\sum_{f} X(f)\,e^{i\,2\pi f t}",
            color=TEXT,
            font_size=28,
        )
        formula.next_to(sum_circle, DOWN, buff=0.7)

        # ----- ANIMATIONS -----
        # A1: Title
        self.play(Write(title_text), run_time=1.0)

        # A2: Spectrum appears
        self.play(
            GrowFromCenter(spectrum),
            Write(label_spectrum),
            run_time=1.5,
        )

        # A3: Sum node appears
        self.play(
            Create(sum_circle),
            Write(sigma_label),
            run_time=1.0,
        )

        # A4: Feed arrow appears
        self.play(Create(arrow_feed), run_time=0.6)

        # A5: Highlight each frequency component
        self.play(
            LaggedStart(
                *[Indicate(bar, color=WHITE) for bar in spectrum.bars],
                lag_ratio=0.15,
            ),
            run_time=1.2,
        )

        # A6: Components flow from spectrum into the sum node
        self.add(feed_dots)
        self.play(
            LaggedStart(
                *[d.animate.move_to(arrow_feed.get_end()) for d in feed_dots],
                lag_ratio=0.1,
            ),
            Indicate(sum_circle, color=PEACH),
            run_time=1.2,
        )

        # A7: Fade out the flow dots
        self.play(FadeOut(feed_dots), run_time=0.3)

        # A8: Output arrow + rebuilt wave + output flow
        self.add(out_dots)
        self.play(
            Create(arrow_out),
            Create(rebuilt_wave),
            Write(label_wave),
            LaggedStart(
                *[d.animate.move_to(arrow_out.get_end()) for d in out_dots],
                lag_ratio=0.1,
            ),
            run_time=1.5,
        )

        # A9: Show the inverse transform formula
        self.play(
            Write(formula),
            Indicate(rebuilt_wave, color=BLUE),
            run_time=0.7,
        )

        # Final pause to reach exactly 9.5s
        self.wait(0.5)
        # --- Scene 8: Practical applications: filtering and compression ---
        self.clear()
        # --- Scene 8: Practical applications: filtering and compression ---
        self.camera.background_color = "#181825"

        # Palette
        BLUE = "#89b4fa"
        PEACH = "#fab387"
        PINK = "#f38ba8"
        GREEN = "#a6e3a1"
        TEAL = "#94e2d5"
        GREY = "#A6ADC8"
        TEXT_LIGHT = "#CDD6F4"

        # 1. Title
        title = Text(
            "Filtering & Compression in Practice", font="Sans", color=TEXT_LIGHT
        )
        title.scale(0.8).to_edge(UP, buff=0.25)
        self.play(Write(title), run_time=1.5)

        # 2. Full spectrum (top)
        full_vals = [4.0, 1.0, 6.0, 1.5, 2.0, 0.5, 3.0]
        full_colors = [BLUE, PEACH, TEAL, PINK, GREEN, GREY, BLUE]
        top_chart = BarChart(
            values=full_vals,
            bar_colors=full_colors,
            bar_width=0.45,
            x_length=9,
            y_length=2.6,
        )
        top_chart.move_to([0, 1.6, 0])
        top_label = Text("Original spectrum", font="Sans", color=TEXT_LIGHT).scale(0.45)
        top_label.next_to(top_chart, UP, buff=0.05)
        self.play(Create(top_chart), FadeIn(top_label), run_time=1.5)

        # 3. Notch band over noisy region
        band = Rectangle(
            width=1.8,
            height=3.2,
            color=PINK,
            fill_opacity=0.25,
            stroke_width=2,
        )
        band.move_to([1.5, 1.6, 0])
        band_label = Text("removed band", font="Sans", color=PINK).scale(0.45)
        band_label.next_to(band, RIGHT, buff=0.15)
        self.play(FadeIn(band), FadeIn(band_label), run_time=1.0)

        # 4. Remove weak frequencies (fade the noisy bars: indices 1, 3, 5)
        noisy = VGroup(top_chart.bars[1], top_chart.bars[3], top_chart.bars[5])
        self.play(FadeOut(noisy), Indicate(band, color=PINK), run_time=1.5)

        # 5. Filtered spectrum (bottom result)
        filt_vals = [4.0, 0.0, 6.0, 0.0, 2.0, 0.0, 3.0]
        filt_colors = [BLUE, PINK, TEAL, PINK, GREEN, PINK, BLUE]
        bottom_chart = BarChart(
            values=filt_vals,
            bar_colors=filt_colors,
            bar_width=0.45,
            x_length=9,
            y_length=1.6,
        )
        bottom_chart.move_to([0, -1.0, 0])
        bottom_label = Text("Filtered spectrum", font="Sans", color=TEXT_LIGHT).scale(
            0.45
        )
        bottom_label.next_to(bottom_chart, UP, buff=0.05)
        self.play(FadeIn(bottom_chart), FadeIn(bottom_label), run_time=1.5)

        # 6. Arrow + cleaner reconstructed wave
        arrow = Arrow(
            start=[0, -1.8, 0],
            end=[0, -2.4, 0],
            color=GREY,
            stroke_width=4,
            buff=0.05,
        )
        wave = FunctionGraph(
            lambda x: np.sin(x) + 0.6 * np.sin(3 * x),
            x_range=[-4.5, 4.5],
            color=BLUE,
            stroke_width=4,
        )
        wave.move_to([0, -3.2, 0]).scale(0.5)
        wave_label = Text("Cleaner signal", font="Sans", color=BLUE).scale(0.45)
        wave_label.next_to(wave, RIGHT, buff=0.2)
        self.play(Create(arrow), Create(wave), FadeIn(wave_label), run_time=2.0)

        # 7. Recap hold
        self.wait(1.5)
