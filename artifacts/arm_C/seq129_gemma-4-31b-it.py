import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: The Sine Wave ---
        # --- Colors & Styling ---
        # Following the professional palette provided in the workflow context
        BG_COLOR = "#181825"
        PRIMARY_COLOR = "#89b4fa"  # Soft Blue
        GRID_COLOR = "#A6ADC8"
        TEXT_COLOR = "#CDD6F4"

        self.camera.background_color = BG_COLOR

        # 1. Objects
        # Coordinate Grid (NumberPlane)
        # Creating a subtle, minimalist grid for a high-contrast look
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": GRID_COLOR,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "stroke_color": GRID_COLOR,
                "stroke_width": 2,
            },
        )

        # Pure Sine Wave
        # We use the .plot method of the NumberPlane to generate the sine curve
        sine_wave = grid.plot(lambda x: np.sin(x), x_range=[-6, 6], color=PRIMARY_COLOR)
        sine_wave.set_stroke(width=4)

        # Name Label
        name_label = Text(
            "The Sine Wave", font="Sans", color=TEXT_COLOR, font_size=42
        ).to_corner(UL, buff=0.5)

        # --- Animation Sequence ---
        # Target Total Duration: 8.0 seconds

        # 0.0s - 1.5s: Fade in the grid and title
        self.play(FadeIn(grid, scale=0.9), Write(name_label), run_time=1.5)
        self.wait(0.5)  # Cumulative: 2.0s

        # 2.0s - 5.0s: Draw the sine wave dynamically (Create)
        # Simulates the wave 'growing' from left to right
        self.play(Create(sine_wave), run_time=3.0, rate_func=linear)

        # 5.0s - 6.5s: Emphasize the wave (Indicate)
        # A subtle pulse to draw attention to the periodicity
        self.play(
            Indicate(sine_wave, color=PRIMARY_COLOR, scale_factor=1.05), run_time=1.5
        )

        # 6.5s - 8.0s: Final pause for visual absorption
        # Total: 2.0 + 3.0 + 1.5 + 1.5 = 8.0 seconds
        self.wait(1.5)
        # --- Scene 2: Superposition ---
        self.clear()

        # Colors from style guidelines and storyboard
        COLOR_AXIS = "#A6ADC8"
        COLOR_WAVE1 = "#CBA6F7"  # Low Freq
        COLOR_WAVE2 = "#F38BA8"  # Mid Freq
        COLOR_WAVE3 = "#A6E3A1"  # High Freq
        COLOR_RESULT = "#FAB387"  # Sum
        BG_COLOR = "#181825"

        self.camera.background_color = BG_COLOR

        # 1. Setup Axes
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": COLOR_AXIS, "stroke_width": 2},
            tips=False,
        ).center()

        label_axes = Text(
            "Amplitude vs Time", font="Sans", font_size=24, color=COLOR_AXIS
        )
        label_axes.to_edge(UP)

        # Wave functions
        # Low frequency: sin(x)
        # Mid frequency: 0.5 * sin(3x)
        # High frequency: 0.2 * sin(10x)
        f1 = lambda x: np.sin(x)
        f2 = lambda x: 0.5 * np.sin(3 * x)
        f3 = lambda x: 0.2 * np.sin(10 * x)
        f_sum = lambda x: f1(x) + f2(x) + f3(x)

        # Create Graphs
        wave_1 = axes.plot(f1, color=COLOR_WAVE1)
        wave_2 = axes.plot(f2, color=COLOR_WAVE2)
        wave_3 = axes.plot(f3, color=COLOR_WAVE3)
        resultant_wave = axes.plot(f_sum, color=COLOR_RESULT)

        # Position waves vertically for the "stacking" start
        # We shift them so they appear as distinct components initially
        wave_1.shift(UP * 1.5)
        wave_2.shift(UP * 0.5)
        wave_3.shift(DOWN * 0.5)

        # Labels for components
        lbl1 = Text(
            "Low Frequency", font="Sans", font_size=20, color=COLOR_WAVE1
        ).next_to(wave_1, LEFT)
        lbl2 = Text(
            "Mid Frequency", font="Sans", font_size=20, color=COLOR_WAVE2
        ).next_to(wave_2, LEFT)
        lbl3 = Text(
            "High Frequency", font="Sans", font_size=20, color=COLOR_WAVE3
        ).next_to(wave_3, LEFT)
        lbl_sum = Text(
            "Summed Complex Wave", font="Sans", font_size=24, color=COLOR_RESULT
        ).to_edge(DOWN)

        # --- Animation Sequence ---
        # Total Duration: 7.0s

        # 0.0s - 1.0s: Setup scene
        self.play(Write(axes), Write(label_axes), run_time=1.0)

        # 1.0s - 3.0s: Introduce the three simple waves
        self.play(
            LaggedStart(
                Create(wave_1),
                Write(lbl1),
                Create(wave_2),
                Write(lbl2),
                Create(wave_3),
                Write(lbl3),
                lag_ratio=0.3,
            ),
            run_time=2.0,
        )

        # 3.0s - 5.0s: Merge waves into the center
        # Move waves to y=0 and fade them out as the resultant wave appears
        self.play(
            wave_1.animate.shift(DOWN * 1.5).set_stroke(opacity=0.3),
            wave_2.animate.shift(DOWN * 0.5).set_stroke(opacity=0.3),
            wave_3.animate.shift(UP * 0.5).set_stroke(opacity=0.3),
            FadeOut(lbl1, shift=DOWN * 0.2),
            FadeOut(lbl2, shift=DOWN * 0.2),
            FadeOut(lbl3, shift=DOWN * 0.2),
            run_time=2.0,
        )

        # 5.0s - 6.5s: Resultant wave emerges and highlights
        self.play(Create(resultant_wave), Write(lbl_sum), run_time=1.5)

        # 6.5s - 7.0s: Final hold
        self.wait(0.5)

        # Verify total run_time: 1.0 + 2.0 + 2.0 + 1.5 + 0.5 = 7.0s
        # --- Scene 3: Circular Representation ---
        # --- Configuration ---
        COLOR_PRIMARY = "#89b4fa"
        COLOR_ACCENT = "#a6e3a1"
        COLOR_CIRCLE = "#A6ADC8"
        COLOR_LINE = "#CDD6F4"
        self.camera.background_color = "#181825"

        circle_center = LEFT * 3
        radius = 2.0

        # --- Objects ---
        orbit_circle = Circle(radius=radius, color=COLOR_CIRCLE).move_to(circle_center)
        circle_label = Text(
            "Phase Circle", font="Sans", font_size=24, color=COLOR_CIRCLE
        )
        circle_label.next_to(orbit_circle, UP, buff=0.5)

        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=6,
            y_length=5,
            axis_config={"include_numbers": False, "color": COLOR_LINE},
        ).shift(RIGHT * 2 + DOWN * 0.5)

        theta = ValueTracker(0)

        # Pre-calculate a simple sine curve
        # We use a lower resolution for the plot to speed up rendering
        full_sine_wave = axes.plot(
            lambda x: radius * np.sin(x * (2 * PI / 6)),
            x_range=[0, 12],
            color=COLOR_PRIMARY,
            stroke_width=4,
        )

        # Dots and lines (initially hidden/offscreen to prevent artifacts)
        orbit_point = Dot(color=COLOR_PRIMARY).shift(RIGHT * 10)
        radius_line = Line(color=COLOR_PRIMARY).shift(RIGHT * 10)
        projection_line = Line(color=COLOR_LINE, stroke_width=2).shift(RIGHT * 10)

        # --- Performance-Optimized Updaters ---
        # To avoid the timeout, we minimize the number of operations inside updaters.
        # We calculate the position once and reuse it.

        def update_orbit():
            angle = theta.get_value()
            # Calculate current point on the circle
            pos = circle_center + np.array(
                [radius * np.cos(angle), radius * np.sin(angle), 0]
            )
            orbit_point.move_to(pos)
            radius_line.set_points([circle_center, pos])

            # Project point to Y-axis of axes
            y_val = pos[1] - circle_center[1]
            proj_end = axes.coords_to_point(0, y_val)
            projection_line.set_points([pos, proj_end])

        # We use a single updater on a dummy object or the ValueTracker itself
        # to ensure a strict execution order and reduce overhead.
        theta.add_updater(lambda v: update_orbit())

        # --- Animation Sequence ---
        # 1. Intro (2s)
        self.play(FadeIn(orbit_circle), Write(circle_label), Create(axes), run_time=2.0)

        # Set initial positions before starting the main animation
        update_orbit()
        self.add(radius_line, orbit_point, projection_line)

        # 2. Motion and Drawing (8s)
        # Using 'Create' on a pre-calculated path is the most efficient "drawing" method.
        # We use a linear rate function for a constant angular velocity.
        self.play(
            theta.animate.set_value(4 * PI),
            Create(full_sine_wave),
            run_time=8.0,
            rate_func=linear,
        )

        # 3. Outro (2s)
        self.play(Indicate(full_sine_wave, color=COLOR_ACCENT), run_time=2.0)
        # --- Scene 4: The Wrapping Mechanism ---
        # Set background color as per style guidelines
        self.camera.background_color = "#181825"

        # Color Palette
        C_SIGNAL = "#fab387"  # Orange-ish
        C_SPIRAL = "#cba6f7"  # Lavender
        C_COM = "#f38ba8"  # Red-pink
        C_VECTOR = "#a6e3a1"  # Green

        # 1. Setup Objects
        # ------------------

        # Time Domain Signal (Top)
        # f(t) = sin(2*t)
        axes = Axes(
            x_range=[0, 2 * PI, 1],
            y_range=[-1.2, 1.2, 1],
            x_length=6,
            y_length=2,
            axis_config={"include_tip": False},
        ).to_edge(UP, buff=0.5)

        signal_label = Text("Time Domain Signal", font="Sans", font_size=24).next_to(
            axes, UP
        )

        # The signal function
        k_val = 2  # Base frequency

        def signal_func(t):
            return np.sin(k_val * t)

        original_signal = axes.plot(signal_func, color=C_SIGNAL, x_range=[0, 2 * PI])

        # Wrapping Spiral (Center)
        # We use a ValueTracker for the wrapping frequency 'w'
        w_tracker = ValueTracker(1.0)

        def get_spiral():
            w = w_tracker.get_value()
            return (
                ParametricFunction(
                    lambda t: np.array(
                        [
                            signal_func(t) * np.cos(w * t),
                            signal_func(t) * np.sin(w * t),
                            0,
                        ]
                    ),
                    t_range=[0, 2 * PI],
                    color=C_SPIRAL,
                )
                .scale(2)
                .move_to(ORIGIN)
            )

        # always_redraw allows the spiral to morph as w_tracker changes
        wrapping_spiral = always_redraw(get_spiral)

        # Center of Mass (COM)
        # We simulate the shift towards resonance when w approx k_val
        def get_com_point():
            w = w_tracker.get_value()
            # Amplitude peak using a Gaussian function to simulate the FT magnitude response
            offset = 1.5 * np.exp(-((w - k_val) ** 2) / 0.2)
            return np.array([offset * np.cos(PI / 4), offset * np.sin(PI / 4), 0])

        com_dot = always_redraw(
            lambda: Dot(point=get_com_point(), color=C_COM, radius=0.08)
        )

        # Mass Vector connecting origin to COM
        mass_vector = always_redraw(
            lambda: Arrow(
                start=ORIGIN,
                end=get_com_point(),
                color=C_VECTOR,
                buff=0,
                stroke_width=3,
            )
        )

        # Dynamic label for the amplitude vector
        vector_label = Text(
            "Amplitude Vector", font="Sans", font_size=20, color=C_VECTOR
        )
        vector_label.add_updater(lambda m: m.next_to(com_dot, UR, buff=0.1))

        # 2. Animations
        # -------------

        # Step 1: Introduction of the signal
        self.play(
            Write(signal_label), Create(axes), Create(original_signal), run_time=2.0
        )

        # Step 2: Introduce wrapping components
        self.play(
            FadeIn(wrapping_spiral), FadeIn(com_dot), FadeIn(mass_vector), run_time=1.0
        )

        self.play(Write(vector_label), run_time=1.0)
        self.wait(1.0)

        # Step 3: The Resonance Phase
        # Transition w from 1.0 to k_val (2.0)
        # As w matches k, the spiral becomes "unbalanced" and the COM shifts away from origin
        self.play(w_tracker.animate.set_value(k_val), run_time=4.0, rate_func=linear)

        # Emphasize the resonance peak
        self.play(Indicate(com_dot, color=C_COM, scale_factor=2), run_time=1.0)

        # Step 4: Moving away from resonance
        # Transition w to a higher value; the spiral balances again and COM returns to center
        self.play(w_tracker.animate.set_value(4.0), run_time=2.0)

        # Final pause to reach 13s total
        self.wait(1.0)
        # --- Scene 5: Domain Transformation ---
        self.clear()

        # --- Configuration & Colors ---
        # Using the requested palette from workflow_context
        COLOR_TIME = "#89b4fa"  # Light Blue
        COLOR_FREQ = "#a6e3a1"  # Light Green
        COLOR_ARROW = "#CDD6F4"  # Soft White/Grey
        BG_COLOR = "#181825"  # Dark Navy/Purple

        self.camera.background_color = BG_COLOR

        # 1. Objects Definition

        # Time Domain Graph (Left)
        time_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=4,
            y_length=3,
            axis_config={"include_tip": False, "stroke_color": GRAY},
        ).shift(LEFT * 3.5)

        # Define a composite signal (Sum of two sines) for visual clarity
        def signal_func(x):
            return np.sin(2 * np.pi * x) + 0.5 * np.sin(4 * np.pi * x)

        time_graph = time_axes.plot(signal_func, color=COLOR_TIME, stroke_width=4)
        time_label = Text(
            "Waveform (Time)", font="Sans", color=COLOR_TIME, font_size=24
        ).next_to(time_axes, UP)
        time_group = VGroup(time_axes, time_graph, time_label)

        # Transform Arrow (Center)
        transform_arrow = Arrow(
            start=LEFT * 1.2, end=RIGHT * 1.2, color=COLOR_ARROW, buff=0, stroke_width=3
        ).shift(ORIGIN)

        ft_text = MathTex(r"\mathcal{F}", color=COLOR_ARROW, font_size=48).next_to(
            transform_arrow, UP, buff=0.2
        )
        ft_label = Text(
            "FT Operator", font="Sans", color=COLOR_ARROW, font_size=18
        ).next_to(transform_arrow, DOWN, buff=0.2)
        arrow_group = VGroup(transform_arrow, ft_text, ft_label)

        # Frequency Domain Graph (Right)
        # A simplified bar chart representing the components of the signal
        # Since it's a composite of sin(2pi*x) and 0.5*sin(4pi*x), we have peaks at 1Hz and 2Hz
        bar_values = [0, 1.0, 0.5, 0, 0]
        bar_names = ["0", "1", "2", "3", "4"]

        freq_chart = BarChart(
            values=bar_values,
            bar_names=bar_names,
            y_range=[0, 1.2, 0.3],
            x_length=4,
            y_length=3,
            bar_colors=[COLOR_FREQ],
            axis_config={"include_tip": False, "stroke_color": GRAY},
            y_axis_config={"include_numbers": True},
        ).shift(RIGHT * 3.5)

        freq_label = Text(
            "Spectrum (Frequency)", font="Sans", color=COLOR_FREQ, font_size=24
        ).next_to(freq_chart, UP)
        freq_group = VGroup(freq_chart, freq_label)

        # --- Animations ---

        # Duration Total: 6.0s
        # 1. Intro the worlds (0.0 - 2.0s)
        self.play(
            FadeIn(time_group, shift=RIGHT),
            FadeIn(freq_group, shift=LEFT),
            run_time=1.5,
        )
        self.wait(0.5)

        # 2. Introduce the operator (2.0 - 3.5s)
        self.play(
            GrowFromCenter(transform_arrow),
            Write(ft_text),
            FadeIn(ft_label, shift=UP),
            run_time=1.5,
        )

        # 3. Visual Bridge / Morph Metaphor (3.5 - 5.0s)
        # We simulate the "transformation" by pulsing the signal and then the bars
        # Highlighting that the energy in time becomes energy in frequency
        self.play(
            Indicate(time_graph, color=COLOR_TIME, scale_factor=1.1), run_time=0.75
        )
        self.play(
            Indicate(freq_chart, color=COLOR_FREQ, scale_factor=1.05), run_time=0.75
        )

        # 4. Final dwell (5.0 - 6.0s)
        self.wait(1.0)

        # Final check on run_times: 1.5 + 0.5 + 1.5 + 0.75 + 0.75 + 1.0 = 6.0s
        # --- Scene 6: The Frequency Spectrum ---
        # --- Configuration & Colors ---
        BG_COLOR = "#181825"
        AXIS_COLOR = "#A6ADC8"
        SPIKE_COLOR = "#CBA6F7"
        LABEL_COLOR = "#CDD6F4"
        self.camera.background_color = BG_COLOR

        # --- 1. Objects ---
        # Spectrum Axes: Frequency (x) vs Magnitude (y)
        spectrum_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 5, 1],
            x_length=9,
            y_length=5,
            axis_config={"color": AXIS_COLOR, "stroke_width": 2.0},
            tips=True,
        )

        x_label = Text("Frequency (Hz)", font="Sans", color=LABEL_COLOR, font_size=24)
        y_label = Text("Magnitude", font="Sans", color=LABEL_COLOR, font_size=24)
        x_label.next_to(spectrum_axes.x_axis, DOWN, buff=0.4)
        y_label.next_to(spectrum_axes.y_axis, LEFT, buff=0.4).rotate(90 * DEGREES)

        # Define frequency components: (frequency, magnitude)
        components = [(2, 3), (5, 4.5), (8, 2)]

        spikes = VGroup()
        labels = VGroup()

        for freq, mag in components:
            # Create a vertical line from x-axis up to magnitude
            start_pt = spectrum_axes.c2p(freq, 0)
            end_pt = spectrum_axes.c2p(freq, mag)

            line = Line(start_pt, end_pt, color=SPIKE_COLOR, stroke_width=4)

            # Dot at the top for visual emphasis
            dot = Dot(end_pt, color=SPIKE_COLOR, radius=0.08)

            # Frequency label below the axis
            label = Text(f"{freq}Hz", font="Sans", color=LABEL_COLOR, font_size=20)
            label.next_to(start_pt, DOWN, buff=0.2)

            spikes.add(VGroup(line, dot))
            labels.add(label)

        # --- 2. Animations ---
        # Total duration target: 7.0s

        # Intro: Axes and Labels (2.0s)
        self.play(Create(spectrum_axes), Write(x_label), Write(y_label), run_time=1.5)
        self.wait(0.5)

        # Animation of the spikes appearing (2.0s)
        # We use LaggedStart to make them "pop" in sequentially
        self.play(
            LaggedStart(
                *[GrowFromCenter(spike) for spike in spikes],
                lag_ratio=0.4,
                run_time=2.0,
            ),
            LaggedStart(
                *[FadeIn(label, shift=UP * 0.3) for label in labels],
                lag_ratio=0.4,
                run_time=2.0,
            ),
        )

        # Final emphasis: Indicate the highest peak (1.0s)
        highest_spike = spikes[1]  # The 5Hz component
        self.play(
            Indicate(highest_spike, color=SPIKE_COLOR, scale_factor=1.2), run_time=1.0
        )

        # Final pause to reach 7.0s total (1.5 + 0.5 + 2.0 + 1.0 + 2.0 = 7.0)
        self.wait(2.0)
