import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Step 1: Signals in the Time Domain ---
        # --- Color Palette Setup ---
        BG_COLOR = "#181825"
        COLOR_BLUE = "#89b4fa"
        COLOR_PEACH = "#fab387"
        COLOR_PINK = "#f38ba8"
        COLOR_GREEN = "#a6e3a1"
        COLOR_TEAL = "#94e2d5"

        # --- Background ---
        self.camera.background_color = BG_COLOR

        # --- Title ---
        title = Text("Signals in the Time Domain", font_size=36, color=WHITE).to_edge(
            UP
        )

        # --- Axes for the signal ---
        axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=5,
            axis_config={
                "color": WHITE,
                "include_tip": True,
                "tip_length": 0.15,
            },
        ).move_to(ORIGIN)

        # --- Axis Labels ---
        x_label = Text("Time", font_size=24, color=WHITE).next_to(
            axes.x_axis, DOWN, buff=0.3
        )
        y_label = (
            Text("Amplitude", font_size=24, color=WHITE)
            .next_to(axes.y_axis, LEFT, buff=0.3)
            .shift(UP * 0.5)
        )

        # --- Signal Graph (sine wave) ---
        graph = axes.plot(lambda x: np.sin(x), color=COLOR_BLUE, stroke_width=3)

        # --- Floating Dot (starts at origin of axes) ---
        dot = Dot(color=COLOR_PEACH, radius=0.1).move_to(axes.c2p(0, 0))

        # --- Animations ---
        # 1. Write the title with a flourish
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # 2. Fade in axes and labels
        self.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.0)
        self.wait(0.3)

        # 3. Grow the dot from center
        self.play(GrowFromCenter(dot), run_time=0.5)

        # 4. Draw the sine wave with the dot following along
        tracker = ValueTracker(0)

        # Update dot position to follow the sine curve
        dot.add_updater(
            lambda d: d.move_to(
                axes.c2p(tracker.get_value(), np.sin(tracker.get_value()))
            )
        )

        # Animate: draw the graph while the dot moves along it
        self.play(
            Create(graph),
            tracker.animate.set_value(4 * PI),
            run_time=3.0,
            rate_func=linear,
        )

        # Clear the updater after animation
        dot.clear_updaters()

        # 5. Final pause
        self.wait(1.0)
        # --- Scene 2: Step 2: Pure Frequencies: The Building Blocks ---
        self.camera.background_color = "#181825"

        ACCENT_1 = "#CBA6F7"
        ACCENT_2 = "#F38BA8"
        ACCENT_3 = "#FAB387"
        ACCENT_4 = "#A6E3A1"
        ACCENT_5 = "#89B4FA"

        title = Text(
            "Pure Frequencies: The Building Blocks", font_size=36, color=WHITE
        ).shift(UP * 3.2)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=5,
            axis_config={"color": ACCENT_3, "include_tip": True, "stroke_width": 2},
            x_axis_config={"numbers_to_include": [-3, -2, -1, 0, 1, 2, 3]},
            y_axis_config={"numbers_to_include": [-2, -1, 0, 1, 2]},
        ).shift(DOWN * 0.3)

        x_label = axes.get_x_axis_label(MathTex(r"t"), direction=RIGHT * 0.5)
        y_label = axes.get_y_axis_label(MathTex(r"A"), direction=UP * 0.5)

        sine_low = axes.plot(
            lambda x: 1.5 * np.sin(x), x_range=[-3, 3], color=ACCENT_5, stroke_width=3
        )
        sine_mid = axes.plot(
            lambda x: 1.2 * np.sin(2 * x),
            x_range=[-3, 3],
            color=ACCENT_1,
            stroke_width=3,
        )
        sine_high = axes.plot(
            lambda x: 0.8 * np.sin(4 * x),
            x_range=[-3, 3],
            color=ACCENT_4,
            stroke_width=3,
        )

        label_low = (
            MathTex(
                r"f_1(t) = A_1 \sin(2\pi \cdot 1 \cdot t)", font_size=28, color=ACCENT_5
            )
            .next_to(axes, DOWN, buff=0.4)
            .shift(LEFT * 2)
        )
        label_mid = MathTex(
            r"f_2(t) = A_2 \sin(2\pi \cdot 2 \cdot t)", font_size=28, color=ACCENT_1
        ).next_to(label_low, DOWN, buff=0.3)
        label_high = MathTex(
            r"f_3(t) = A_3 \sin(2\pi \cdot 4 \cdot t)", font_size=28, color=ACCENT_4
        ).next_to(label_mid, DOWN, buff=0.3)

        # FIXED: Create labels separately, then position manually
        brace_amp = BraceBetweenPoints(
            axes.c2p(0.25, 0),
            axes.c2p(0.25, 1.5),
            direction=LEFT,
            color=ACCENT_2,
            buff=0.1,
        )
        amp_label = Tex("Amplitude", font_size=22, color=ACCENT_2).next_to(
            brace_amp, LEFT, buff=0.15
        )

        brace_freq = BraceBetweenPoints(
            axes.c2p(0, -1.8),
            axes.c2p(2 * PI, -1.8),
            direction=DOWN,
            color=ACCENT_3,
            buff=0.1,
        )
        freq_label = Tex("Period", font_size=22, color=ACCENT_3).next_to(
            brace_freq, DOWN, buff=0.15
        )

        # Animation sequence...
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(Create(axes), run_time=2)
        self.play(FadeIn(x_label), FadeIn(y_label), run_time=1)
        self.wait(0.5)
        self.play(Create(sine_low), run_time=2)
        self.play(FadeIn(label_low), run_time=0.8)
        self.wait(0.5)
        self.play(GrowFromCenter(brace_amp), FadeIn(amp_label), run_time=1.5)
        self.wait(0.5)
        self.play(GrowFromCenter(brace_freq), FadeIn(freq_label), run_time=1.5)
        self.wait(0.5)
        self.play(Create(sine_mid), run_time=2)
        self.play(FadeIn(label_mid), run_time=0.8)
        self.wait(0.3)
        self.play(Create(sine_high), run_time=2)
        self.play(FadeIn(label_high), run_time=0.8)
        self.wait(1)
        self.play(Indicate(label_low, color=ACCENT_5, scale_factor=1.1), run_time=1)
        self.wait(1)
        # --- Scene 3: Step 3: Superposition: Mixing Waves Together ---
        self.clear()

        # Colors (Catppuccin Mocha)
        BG_COLOR = "#1E1E2E"
        ACCENT_2 = "#F38BA8"  # Pink/Red
        ACCENT_4 = "#A6E3A1"  # Green
        ACCENT_5 = "#89B4FA"  # Blue

        self.camera.background_color = BG_COLOR

        # 1. Title
        title = Text("Superposition: Mixing Waves Together", font_size=36, color=WHITE)
        title.to_edge(UP)

        # 2. Axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=4,
            axis_config={"color": WHITE},
            tips=False,
        )
        axes.shift(DOWN * 0.5)

        # 3. Define Waves
        sine_wave_1 = axes.plot(
            lambda x: np.sin(x), x_range=[-5, 5], color=ACCENT_5, stroke_width=3
        )

        sine_wave_2 = axes.plot(
            lambda x: 0.5 * np.sin(3 * x),
            x_range=[-5, 5],
            color=ACCENT_4,
            stroke_width=3,
        )

        # Combined Wave (Sum of both)
        combined_wave = axes.plot(
            lambda x: np.sin(x) + 0.5 * np.sin(3 * x),
            x_range=[-5, 5],
            color=ACCENT_2,
            stroke_width=4,
        )

        # 4. Labels for the waves
        label_1 = Text("Pure Tone 1", font_size=20, color=ACCENT_5)
        label_1.next_to(axes, RIGHT, buff=0.2).shift(UP * 0.5)

        label_2 = Text("Pure Tone 2", font_size=20, color=ACCENT_4)
        label_2.next_to(label_1, DOWN, buff=0.2)

        label_combined = Text("Superposition", font_size=24, color=ACCENT_2)
        label_combined.next_to(axes, DOWN, buff=0.5)

        # 5. Animations (Total: 7.5s)
        # 0.0 - 1.0s: Title appears
        self.play(Write(title), run_time=1.0)

        # 1.0 - 2.0s: Axes appear
        self.play(FadeIn(axes), run_time=1.0)

        # 2.0 - 3.5s: First wave builds up
        self.play(Create(sine_wave_1), FadeIn(label_1), run_time=1.5)

        # 3.5 - 5.0s: Second wave builds up
        self.play(Create(sine_wave_2), FadeIn(label_2), run_time=1.5)

        # 5.0 - 6.5s: Waves combine into superposition
        self.play(
            ReplacementTransform(sine_wave_1, combined_wave),
            ReplacementTransform(sine_wave_2, combined_wave.copy()),
            FadeOut(label_1),
            FadeOut(label_2),
            FadeIn(label_combined),
            run_time=1.5,
        )

        # 6.5 - 7.5s: Final pause
        self.wait(1.0)
        # --- Scene 4: Step 4: The Prism Analogy: Decomposing Light ---
        self.clear()

        # --- Scene 4: The Prism Analogy: Decomposing Light ---

        # Title
        title = Text("The Prism Analogy: Decomposing Light", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Create prism (triangle)
        prism = Triangle(color=WHITE, fill_color="#89b4fa", fill_opacity=0.5)
        prism.scale(1.5)
        prism.move_to(ORIGIN)

        # Prism label
        prism_label = Text("Fourier Transform", font_size=24, color="#fab387")
        prism_label.next_to(prism, DOWN, buff=0.3)

        self.play(GrowFromCenter(prism))
        self.play(FadeIn(prism_label))
        self.wait(0.5)

        # White light arrow (input)
        white_arrow = Arrow(
            start=LEFT * 4 + UP * 0.3,
            end=LEFT * 1.5 + UP * 0.3,
            color=WHITE,
            buff=0,
            stroke_width=6,
        )
        white_label = Text("White Light\n(Complex Signal)", font_size=20, color=WHITE)
        white_label.next_to(white_arrow, UP, buff=0.2)

        self.play(GrowArrow(white_arrow))
        self.play(FadeIn(white_label))
        self.wait(0.5)

        # Rainbow rays (output frequencies)
        colors = ["#f38ba8", "#fab387", "#f9e2af", "#a6e3a1", "#89b4fa", "#cba6f7"]
        labels = ["Low Freq", "Med-Low", "Medium", "Med-High", "High Freq", "Very High"]

        rays = VGroup()
        ray_labels = VGroup()

        for i, (color, label) in enumerate(zip(colors, labels)):
            angle = -PI / 4 + i * PI / 8
            end_point = prism.get_right() + 2.5 * np.array(
                [np.cos(angle), np.sin(angle), 0]
            )

            ray = Line(
                start=prism.get_right(), end=end_point, color=color, stroke_width=4
            )
            ray_label = Text(label, font_size=16, color=color)
            ray_label.next_to(ray.get_end(), RIGHT, buff=0.1)

            rays.add(ray)
            ray_labels.add(ray_label)

        # Animate rays one by one
        for i in range(len(rays)):
            self.play(Create(rays[i]), FadeIn(ray_labels[i]), run_time=0.3)

        self.wait(0.3)

        # Fade out white light
        self.play(FadeOut(white_arrow), FadeOut(white_label))

        # Analogy explanation
        analogy = Text(
            "Just as a prism splits light into colors,", font_size=24, color="#a6e3a1"
        )
        analogy2 = Text(
            "the Fourier Transform splits signals into frequencies.",
            font_size=24,
            color="#a6e3a1",
        )
        analogy_group = VGroup(analogy, analogy2).arrange(DOWN, buff=0.2)
        analogy_group.to_edge(DOWN, buff=0.5)

        self.play(Write(analogy))
        self.play(Write(analogy2))
        self.wait(1)
        # --- Scene 5: Step 5: The Frequency Domain View ---
        self.clear()

        # Set background color to match style guidelines
        self.camera.background_color = "#181825"

        # --- 1. Objects ---

        # Title
        title = Text("The Frequency Domain View", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)

        # Data for Table and Bar Chart
        frequencies = ["50", "120", "200", "350"]
        amplitudes_str = ["0.8", "0.5", "0.3", "0.1"]
        amplitudes_val = [0.8, 0.5, 0.3, 0.1]
        colors = ["#89b4fa", "#fab387", "#f38ba8", "#a6e3a1"]

        table_data = list(zip(frequencies, amplitudes_str))

        # Construct Table
        table = Table(
            table_data,
            col_labels=[
                Text("Freq (Hz)", font_size=24),
                Text("Magnitude", font_size=24),
            ],
            include_outer_lines=True,
            v_buff=0.5,
            h_buff=0.8,
            line_config={"stroke_width": 1.5, "stroke_color": "#94e2d5"},
        )

        # Styling Table
        table.scale(0.7)
        table.move_to(LEFT * 2.0)

        # Construct Bar Chart Visualization
        bars = VGroup()
        for i, (val, color) in enumerate(zip(amplitudes_val, colors)):
            bar = Rectangle(
                width=0.5,
                height=val * 3.0,
                fill_color=color,
                fill_opacity=0.9,
                stroke_color=WHITE,
                stroke_width=1,
            )
            bars.add(bar)

        bars.arrange(RIGHT, buff=0.6)
        bars.next_to(table, RIGHT, buff=1.0)
        bars.align_to(table.get_bottom(), DOWN)

        # Bar Labels
        bar_labels = VGroup()
        for bar, freq, color in zip(bars, frequencies, colors):
            label = Text(freq, font_size=18, color=color)
            label.next_to(bar, DOWN, buff=0.1)
            bar_labels.add(label)

        bar_header = Text("Spectrum", font_size=24, color="#fab387")
        bar_header.next_to(bars, UP, buff=0.3)

        # --- 2. Animations (Total: 6.5s) ---

        # Title Intro (1.5s)
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)

        # Table Appearance (1.5s)
        self.play(FadeIn(table), run_time=1.0)
        self.wait(0.5)

        # Bar Chart Growth (2.0s)
        self.play(
            FadeIn(bar_header),
            LaggedStart(*[GrowFromCenter(bar) for bar in bars], lag_ratio=0.2),
            FadeIn(bar_labels),
            run_time=2.0,
        )

        # Highlight Static Nature (1.5s)
        highlight = SurroundingRectangle(
            table, color=WHITE, buff=0.1, corner_radius=0.1
        )
        self.play(Create(highlight), run_time=0.5)
        self.wait(1.0)
        # --- Scene 6: Step 6: The Mathematics: Correlation ---
        self.clear()
        bg = "#181825"
        self.camera.background_color = bg

        # === PALETTE ===
        c1 = "#89b4fa"  # blue
        c2 = "#fab387"  # orange
        c3 = "#f38ba8"  # pink
        c4 = "#a6e3a1"  # green
        c5 = "#94e2d5"  # teal
        cwhite = "#cdd6f4"

        # === TITLE ===
        title = Text("The Mathematics: Correlation", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.4)

        # === AXES for signal ===
        ax = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=2.5,
            axis_config={
                "color": cwhite,
                "stroke_width": 1.5,
                "include_numbers": False,
            },
            tips=False,
        ).shift(UP * 1.0)

        # Signal: composite waveform
        signal_func = lambda x: (
            0.6 * np.sin(x) + 0.4 * np.sin(3 * x) + 0.2 * np.sin(5 * x)
        )
        signal_graph = ax.plot(signal_func, color=c1, stroke_width=3)
        signal_label = (
            Text("Signal", font_size=22, color=c1)
            .next_to(ax, LEFT, buff=0.2)
            .shift(UP * 0.3)
        )

        # === TEST FREQUENCY (below) ===
        ax2 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=1.8,
            axis_config={
                "color": cwhite,
                "stroke_width": 1.5,
                "include_numbers": False,
            },
            tips=False,
        ).shift(DOWN * 1.3)

        # Test frequency: pure sine at frequency 1
        test_func = lambda x: np.sin(x)
        test_graph = ax2.plot(test_func, color=c2, stroke_width=3)
        test_label = (
            Text("Test Frequency", font_size=22, color=c2)
            .next_to(ax2, LEFT, buff=0.2)
            .shift(UP * 0.2)
        )

        # === MULTIPLICATION RESULT (product curve) ===
        ax3 = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=1.8,
            axis_config={
                "color": cwhite,
                "stroke_width": 1.5,
                "include_numbers": False,
            },
            tips=False,
        ).shift(DOWN * 3.2)

        product_func = lambda x: signal_func(x) * test_func(x)
        product_graph = ax3.plot(product_func, color=c3, stroke_width=3)
        product_label = (
            Text("Product", font_size=22, color=c3)
            .next_to(ax3, LEFT, buff=0.2)
            .shift(UP * 0.2)
        )

        # === BRACE showing "Sum of Area" ===
        brace = Brace(product_graph, direction=DOWN, color=c5, buff=0.1)
        brace_text = brace.get_tex(r"\int = 	ext{Correlation Value}")
        brace_text.set_color(c5)
        brace_text.font_size = 24

        # === RESULT BOX ===
        result_box = RoundedRectangle(
            corner_radius=0.15, width=3.5, height=0.7, color=c4, stroke_width=2
        ).to_corner(DR, buff=0.5)
        result_text = Text("Large Area = Match!", font_size=22, color=c4)
        result_text.move_to(result_box)

        # === ARROW (main_6) connecting signal to product ===
        main_arrow = Arrow(
            start=ax.get_right() + RIGHT * 0.2,
            end=ax3.get_right() + RIGHT * 0.2,
            color=cwhite,
            stroke_width=3,
            buff=0.1,
        )
        multiply_label = Text("×", font_size=36, color=YELLOW).next_to(
            main_arrow, LEFT, buff=0.15
        )

        # === ANIMATIONS ===
        # 1. Title
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.0)

        # 2. Signal graph
        self.play(
            FadeIn(ax, shift=UP * 0.2),
            Create(signal_graph),
            FadeIn(signal_label),
            run_time=1.5,
        )

        # 3. Test frequency graph
        self.play(
            FadeIn(ax2, shift=UP * 0.2),
            Create(test_graph),
            FadeIn(test_label),
            run_time=1.2,
        )

        # 4. Arrow and multiply label
        self.play(
            GrowFromCenter(main_arrow),
            FadeIn(multiply_label),
            run_time=0.8,
        )

        # 5. Product graph (result of multiplication)
        self.play(
            FadeIn(ax3, shift=UP * 0.2),
            Create(product_graph),
            FadeIn(product_label),
            run_time=1.2,
        )

        # 6. Brace showing integration (sum of area)
        self.play(
            GrowFromCenter(brace),
            FadeIn(brace_text, shift=UP * 0.2),
            run_time=1.0,
        )

        # 7. Result box
        self.play(
            GrowFromCenter(result_box),
            FadeIn(result_text),
            run_time=0.8,
        )

        # Total: 1.0 + 1.5 + 1.2 + 0.8 + 1.2 + 1.0 + 0.8 = 7.5 ✓
        # --- Scene 7: Step 7: Phase: The Timing Component ---
        self.clear()

        # --- Color palette (Catppuccin Mocha) ---
        BG = "#181825"
        ACCENT_BLUE = "#89b4fa"
        ACCENT_PEACH = "#fab387"
        ACCENT_RED = "#f38ba8"
        ACCENT_GREEN = "#a6e3a1"
        ACCENT_TEAL = "#94e2d5"
        TEXT_WHITE = "#cdd6f4"

        self.camera.background_color = BG

        # --- Title ---
        title = Text(
            "Phase: The Timing Component",
            font_size=36,
            color=TEXT_WHITE,
        ).to_edge(UP, buff=0.5)

        # --- Unit circle (phasor diagram) ---
        circle = Circle(
            radius=2.0,
            color=ACCENT_BLUE,
            stroke_width=2.0,
        ).shift(DOWN * 0.3)

        # Axes through the circle
        h_axis = Line(
            start=circle.get_center() + LEFT * 2.3,
            end=circle.get_center() + RIGHT * 2.3,
            color=TEXT_WHITE,
            stroke_width=1.5,
            stroke_opacity=0.5,
        )
        v_axis = Line(
            start=circle.get_center() + DOWN * 2.3,
            end=circle.get_center() + UP * 2.3,
            color=TEXT_WHITE,
            stroke_width=1.5,
            stroke_opacity=0.5,
        )

        # Axis labels
        re_label = Text("Re", font_size=20, color=TEXT_WHITE).next_to(
            h_axis.get_end(), DOWN + RIGHT, buff=0.1
        )
        im_label = Text("Im", font_size=20, color=TEXT_WHITE).next_to(
            v_axis.get_end(), UP + LEFT, buff=0.1
        )

        # --- Phasor arrow (phase = 60°) ---
        phase_angle = PI / 3  # 60 degrees
        arrow_tip = circle.get_center() + 2.0 * np.array(
            [np.cos(phase_angle), np.sin(phase_angle), 0]
        )
        phasor = Arrow(
            start=circle.get_center(),
            end=arrow_tip,
            buff=0,
            color=ACCENT_PEACH,
            stroke_width=4,
            tip_length=0.2,
        )

        # Phase angle arc
        angle_arc = Arc(
            radius=0.6,
            start_angle=0,
            angle=phase_angle,
            arc_center=circle.get_center(),
            color=ACCENT_RED,
            stroke_width=3,
        )

        # Phase label
        phi_label = (
            MathTex(r"\varphi", font_size=36, color=ACCENT_RED)
            .next_to(angle_arc, RIGHT, buff=0.15)
            .shift(UP * 0.15)
        )

        # Dot at arrow tip
        tip_dot = Dot(point=arrow_tip, radius=0.07, color=ACCENT_PEACH)

        # --- Horizontal projection (cos component) ---
        cos_line = DashedLine(
            start=arrow_tip,
            end=circle.get_center() + RIGHT * 2.0 * np.cos(phase_angle),
            color=ACCENT_GREEN,
            stroke_width=2,
            dash_length=0.1,
        )
        cos_label = MathTex(r"\cos\varphi", font_size=24, color=ACCENT_GREEN).next_to(
            circle.get_center() + RIGHT * 1.0 * np.cos(phase_angle),
            DOWN,
            buff=0.25,
        )

        # --- Vertical projection (sin component) ---
        sin_line = DashedLine(
            start=arrow_tip,
            end=circle.get_center() + UP * 2.0 * np.sin(phase_angle),
            color=ACCENT_TEAL,
            stroke_width=2,
            dash_length=0.1,
        )
        sin_label = MathTex(r"\sin\varphi", font_size=24, color=ACCENT_TEAL).next_to(
            circle.get_center() + UP * 1.0 * np.sin(phase_angle),
            LEFT,
            buff=0.25,
        )

        # --- Explanation text ---
        explanation = Text(
            "Phase = where in the cycle the wave starts",
            font_size=24,
            color=TEXT_WHITE,
        ).to_edge(DOWN, buff=0.4)

        # Magnitude label on the phasor
        mag_label = MathTex(r"A", font_size=28, color=ACCENT_PEACH).next_to(
            phasor.get_center() + UP * 0.2 + RIGHT * 0.2, UR, buff=0.05
        )

        # ============================================================
        # ANIMATIONS (total: 6.5s)
        # ============================================================

        # 1. Title fade in (0.8s)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.8)

        # 2. Draw unit circle (0.8s)
        self.play(Create(circle), run_time=0.8)

        # 3. Draw axes (0.5s)
        self.play(
            Create(h_axis),
            Create(v_axis),
            FadeIn(re_label),
            FadeIn(im_label),
            run_time=0.5,
        )

        # 4. Phasor arrow grows from center (0.8s)
        self.play(GrowArrow(phasor), run_time=0.8)
        self.play(FadeIn(tip_dot), FadeIn(mag_label), run_time=0.3)

        # 5. Draw angle arc and label (0.7s)
        self.play(Create(angle_arc), run_time=0.5)
        self.play(FadeIn(phi_label, shift=RIGHT * 0.1), run_time=0.3)

        # 6. Show projections (0.8s)
        self.play(
            Create(cos_line),
            Create(sin_line),
            FadeIn(cos_label),
            FadeIn(sin_label),
            run_time=0.8,
        )

        # 7. Explanation text (0.6s)
        self.play(FadeIn(explanation, shift=UP * 0.2), run_time=0.6)

        # 8. Animate phasor rotation to show phase change (1.1s)
        self.play(
            Rotate(phasor, angle=PI / 3, about_point=circle.get_center()),
            Rotate(tip_dot, angle=PI / 3, about_point=circle.get_center()),
            run_time=1.1,
        )

        # Total: 0.8+0.8+0.5+0.8+0.3+0.5+0.3+0.8+0.6+1.1 = 6.5s ✓
        # --- Scene 8: Step 8: Synthesis: The Inverse Transform ---
        self.clear()

        # Color palette
        PEACH = "#fab387"
        MAUVE = "#cba6f7"
        GREEN = "#a6e3a1"
        BLUE = "#89b4fa"
        TEAL = "#94e2d5"

        # 1. Title
        title = Text(
            "Synthesis: The Inverse Transform", font_size=36, color=WHITE
        ).to_edge(UP, buff=0.5)

        # 2. Main axes for the reconstructed signal
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=5,
            axis_config={
                "color": PEACH,
                "include_tip": True,
                "stroke_width": 2,
            },
            tips=True,
        ).shift(DOWN * 0.3)

        x_label = axes.get_x_axis_label(MathTex("t", color=PEACH))
        y_label = axes.get_y_axis_label(MathTex("f(t)", color=PEACH))

        # 3. Individual frequency components
        component_1 = axes.plot(
            lambda x: 0.8 * np.sin(2 * x),
            x_range=[-3, 3],
            color=BLUE,
            stroke_width=2.5,
            stroke_opacity=0.7,
        )
        component_2 = axes.plot(
            lambda x: 0.5 * np.sin(4 * x + 1),
            x_range=[-3, 3],
            color=GREEN,
            stroke_width=2.5,
            stroke_opacity=0.7,
        )
        component_3 = axes.plot(
            lambda x: 0.3 * np.sin(7 * x + 2),
            x_range=[-3, 3],
            color=MAUVE,
            stroke_width=2.5,
            stroke_opacity=0.7,
        )

        # Component labels with plus signs
        label_1 = (
            MathTex(r"A_1 \sin(\omega_1 t + \phi_1)", font_size=28, color=BLUE)
            .next_to(axes, UP, buff=0.15)
            .shift(LEFT * 3.5)
        )
        plus_1 = MathTex("+", font_size=36, color=WHITE).next_to(
            label_1, RIGHT, buff=0.15
        )
        label_2 = MathTex(
            r"A_2 \sin(\omega_2 t + \phi_2)", font_size=28, color=GREEN
        ).next_to(plus_1, RIGHT, buff=0.15)
        plus_2 = MathTex("+", font_size=36, color=WHITE).next_to(
            label_2, RIGHT, buff=0.15
        )
        label_3 = MathTex(
            r"A_3 \sin(\omega_3 t + \phi_3)", font_size=28, color=MAUVE
        ).next_to(plus_2, RIGHT, buff=0.15)

        components = VGroup(component_1, component_2, component_3)
        comp_labels = VGroup(label_1, label_2, label_3, plus_1, plus_2)

        # 4. Reconstructed signal (sum of components)
        reconstructed = axes.plot(
            lambda x: (
                0.8 * np.sin(2 * x) + 0.5 * np.sin(4 * x + 1) + 0.3 * np.sin(7 * x + 2)
            ),
            x_range=[-3, 3],
            color=PEACH,
            stroke_width=4,
        )

        # 5. Sigma notation for synthesis
        sigma_formula = MathTex(
            r"f(t) = \sum_{n} A_n \sin(n\omega t + \phi_n)",
            font_size=30,
            color=WHITE,
        ).to_edge(DOWN, buff=0.4)

        formula_box = SurroundingRectangle(
            sigma_formula, color=TEAL, buff=0.12, corner_radius=0.1
        )

        # === ANIMATIONS ===
        self.play(FadeIn(title), run_time=0.6)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.6)
        self.play(Create(component_1), FadeIn(label_1), run_time=0.5)
        self.play(Create(component_2), FadeIn(plus_1), FadeIn(label_2), run_time=0.5)
        self.play(Create(component_3), FadeIn(plus_2), FadeIn(label_3), run_time=0.5)
        self.wait(0.3)
        self.play(
            ReplacementTransform(components.copy(), reconstructed),
            run_time=0.8,
        )
        self.play(
            FadeOut(components),
            FadeOut(comp_labels),
            run_time=0.4,
        )
        self.play(
            GrowFromCenter(sigma_formula),
            Create(formula_box),
            run_time=0.5,
        )
        self.wait(0.8)
        # --- Scene 9: Step 9: Applications: Why it Matters ---
        # Set background color
        self.camera.background_color = "#181825"

        # Create title
        title = Text("Applications: Why it Matters", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)

        # Create number line
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            color="#f38ba8",
            stroke_width=2.0,
            include_numbers=True,
            font_size=24,
        )
        number_line.shift(DOWN * 0.5)

        # Create application labels
        applications = [
            ("MP3\nAudio", -4, "#89b4fa"),
            ("JPEG\nImages", -2, "#fab387"),
            ("WiFi\nData", 0, "#a6e3a1"),
            ("Medical\nSignals", 2, "#94e2d5"),
            ("Radar", 4, "#f38ba8"),
        ]

        labels = []
        dots = []
        for app_name, position, color in applications:
            # Create dot on number line
            dot = Dot(point=number_line.n2p(position), radius=0.08, color=color)
            dots.append(dot)

            # Create label
            label = Text(app_name, font_size=20, color=color)
            label.next_to(dot, DOWN, buff=0.3)
            labels.append(label)

        # Animations
        self.play(Write(title), run_time=1.5)
        self.play(Create(number_line), run_time=2)

        # Animate dots and labels with staggered timing
        for i in range(len(applications)):
            self.play(
                GrowFromCenter(dots[i]), FadeIn(labels[i], shift=UP * 0.2), run_time=0.8
            )
            if i < len(applications) - 1:
                self.wait(0.2)

        self.wait(1)
