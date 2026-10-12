import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        self.camera.background_color = "#181825"
        self.scene_1()
        self.scene_2()
        self.scene_3()
        self.scene_4()
        self.scene_5()
        self.scene_6()
        self.scene_7()
        self.scene_8()

    def scene_1(self):
        title = Text("Periodic Wave Decomposition", font_size=36, color="#ECEFF4")
        title.to_edge(UP, buff=0.5)
        time_axis = NumberLine(
            x_range=[-3, 3, 1], length=10, color="#ECEFF4", include_numbers=True
        )
        time_axis.move_to(DOWN * 3)
        time_label = Text("Time", font_size=24, color="#D8DEE9").next_to(
            time_axis, DOWN, buff=0.2
        )
        fundamental = FunctionGraph(
            lambda x: np.sin(x), x_range=[-3, 3], color="#88C0D0", stroke_width=2.5
        )
        fundamental.shift(UP * 0.5)
        harmonic3 = FunctionGraph(
            lambda x: 0.3 * np.sin(3 * x),
            x_range=[-3, 3],
            color="#EBCB8B",
            stroke_width=2,
        )
        harmonic3.shift(DOWN * 0.8)
        harmonic5 = FunctionGraph(
            lambda x: 0.2 * np.sin(5 * x),
            x_range=[-3, 3],
            color="#A3BE8C",
            stroke_width=2,
        )
        harmonic5.shift(DOWN * 1.5)
        square_approx = FunctionGraph(
            lambda x: np.sin(x) + 0.3 * np.sin(3 * x) + 0.2 * np.sin(5 * x),
            x_range=[-3, 3],
            color="#D8DEE9",
            stroke_width=3,
        )
        square_approx.shift(UP * 2)
        sum_arrow = Arrow(
            start=DOWN * 1 + LEFT * 1,
            end=UP * 1.8 + LEFT * 1,
            color="#81A1C1",
            buff=0.1,
        )
        plus1 = Text("+", font_size=36, color="#D8DEE9").move_to(
            (fundamental.get_center() + harmonic3.get_center()) / 2
        )
        plus2 = Text("+", font_size=36, color="#D8DEE9").move_to(
            (harmonic3.get_center() + harmonic5.get_center()) / 2
        )
        fund_label = Text("Fundamental", font_size=24, color="#88C0D0").next_to(
            fundamental, RIGHT, buff=0.5
        )
        h3_label = Text("3rd Harmonic", font_size=24, color="#EBCB8B").next_to(
            harmonic3, RIGHT, buff=0.5
        )
        h5_label = Text("5th Harmonic", font_size=24, color="#A3BE8C").next_to(
            harmonic5, RIGHT, buff=0.5
        )
        sum_label = Text("Sum → Square", font_size=24, color="#D8DEE9").next_to(
            square_approx, RIGHT, buff=0.5
        )
        g1 = VGroup(
            title,
            time_axis,
            time_label,
            fundamental,
            harmonic3,
            harmonic5,
            square_approx,
            sum_arrow,
            plus1,
            plus2,
            fund_label,
            h3_label,
            h5_label,
            sum_label,
        )
        self.play(Write(title), run_time=1.5)
        self.play(Create(time_axis), FadeIn(time_label), run_time=1.5)
        self.play(Create(fundamental), FadeIn(fund_label), run_time=1.5)
        self.play(Create(harmonic3), FadeIn(h3_label), run_time=1.5)
        self.play(Create(harmonic5), FadeIn(h5_label), run_time=1.5)
        self.play(FadeIn(plus1), FadeIn(plus2), run_time=1)
        self.play(GrowFromCenter(sum_arrow), run_time=1.5)
        self.play(Create(square_approx), FadeIn(sum_label), run_time=2)
        self.wait(3)
        self.play(FadeOut(g1), run_time=2)
        self.wait(2)

    def scene_2(self):
        title = Text("From Waveform to Frequency Recipe", font_size=36, color="#ECEFF4")
        title.to_edge(UP, buff=0.5)
        time_axis = NumberLine(
            x_range=[-5, 5, 1], length=6, color="#ECEFF4", include_numbers=True
        )
        time_axis.move_to(LEFT * 4 + DOWN * 2)
        time_label = Text("Time", font_size=24, color="#D8DEE9").next_to(
            time_axis, DOWN, buff=0.2
        )
        time_pulse = FunctionGraph(
            lambda x: np.sinc(x), x_range=[-5, 5], color="#88C0D0", stroke_width=3
        )
        time_pulse.shift(LEFT * 4)
        pulse_label = Text("Time Signal", font_size=24, color="#88C0D0").next_to(
            time_pulse, UP, buff=0.5
        )
        transform_arrow = Arrow(
            start=LEFT * 2.5, end=RIGHT * 1.0, color="#81A1C1", buff=0.2
        )
        transform_label = Text("Transform", font_size=24, color="#81A1C1").next_to(
            transform_arrow, UP, buff=0.2
        )
        bar_values = [1.0, 0.5, 0.3, 0.2, 0.15]
        bar_colors = ["#88C0D0", "#EBCB8B", "#A3BE8C", "#81A1C1", "#B48EAD"]
        bars = VGroup()
        base_x = 3.5
        spacing = 0.8
        for i, (val, color) in enumerate(zip(bar_values, bar_colors)):
            bar = Rectangle(width=0.4, height=val * 2, color=color, fill_opacity=0.8)
            x = base_x + (i - len(bar_values) / 2) * spacing
            y = -1.0 + val
            bar.move_to(np.array([x, y, 0]))
            bars.add(bar)
        spectrum_label = Text("Spectrum", font_size=24, color="#EBCB8B").next_to(
            bars, UP, buff=0.5
        )
        magnifier = Circle(
            radius=0.5, color="#ECEFF4", stroke_width=2, fill_opacity=0.1
        )
        magnifier.move_to(np.array([4.0, 0.7, 0]))
        mag_label = Text("Lens", font_size=20, color="#ECEFF4").next_to(
            magnifier, UP, buff=0.2
        )
        g2 = VGroup(
            title,
            time_axis,
            time_label,
            time_pulse,
            pulse_label,
            transform_arrow,
            transform_label,
            bars,
            spectrum_label,
            magnifier,
            mag_label,
        )
        self.play(Write(title), run_time=1.5)
        self.play(Create(time_axis), FadeIn(time_label), run_time=1)
        self.play(Create(time_pulse), FadeIn(pulse_label), run_time=2)
        self.play(
            GrowFromCenter(transform_arrow), FadeIn(transform_label), run_time=1.5
        )
        self.play(Create(bars), FadeIn(spectrum_label), run_time=2)
        self.play(FadeIn(magnifier), FadeIn(mag_label), run_time=1)
        self.wait(3)
        self.play(FadeOut(g2), run_time=2)
        self.wait(1)

    def scene_3(self):
        title = Text(
            "The Continuous Fourier Transform Integral", font_size=36, color="#ECEFF4"
        )
        title.to_edge(UP, buff=0.5)
        time_pulse = FunctionGraph(
            lambda x: np.exp(-(x**2)), x_range=[-3, 3], color="#88C0D0", stroke_width=3
        )
        time_pulse.shift(LEFT * 4 + UP * 0.5)
        pulse_label = Text("Pulse", font_size=24, color="#88C0D0").next_to(
            time_pulse, UP
        )
        complex_plane = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={"include_tip": True, "stroke_color": "#D8DEE9"},
        )
        re_label = MathTex(r"	ext{Re}", font_size=24, color="#D8DEE9").next_to(
            complex_plane.x_axis, RIGHT
        )
        im_label = MathTex(r"	ext{Im}", font_size=24, color="#D8DEE9").next_to(
            complex_plane.y_axis, UP
        )
        spiral = ParametricFunction(
            lambda t: np.array([np.cos(3 * t), np.sin(3 * t), 0]),
            t_range=[0, 4],
            color="#EBCB8B",
            stroke_width=2,
        )
        spiral_label = MathTex(r"e^{i\omega t}", font_size=24, color="#EBCB8B").next_to(
            spiral, UP
        )
        freq_axis = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 1.2, 0.3],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": True},
        )
        freq_axis.move_to(RIGHT * 4.5 + DOWN * 1)
        freq_label = MathTex(r"\omega", font_size=24, color="#D8DEE9").next_to(
            freq_axis.x_axis, RIGHT
        )
        freq_y_label = MathTex(r"|X(\omega)|", font_size=24, color="#A3BE8C").next_to(
            freq_axis.y_axis, UP
        )
        spectrum = FunctionGraph(
            lambda x: np.exp(-((x / 2) ** 2)),
            x_range=[-5, 5],
            color="#A3BE8C",
            stroke_width=3,
        )
        spectrum.move_to(freq_axis.c2p(0, 0.5))
        g3 = VGroup(
            title,
            time_pulse,
            pulse_label,
            complex_plane,
            re_label,
            im_label,
            spiral,
            spiral_label,
            freq_axis,
            freq_label,
            freq_y_label,
            spectrum,
        )
        self.play(Write(title), run_time=1.5)
        self.play(Create(time_pulse), FadeIn(pulse_label), run_time=2)
        self.play(
            Create(complex_plane), FadeIn(re_label), FadeIn(im_label), run_time=1.5
        )
        self.play(Create(spiral), FadeIn(spiral_label), run_time=2)
        self.play(
            Create(freq_axis), FadeIn(freq_label), FadeIn(freq_y_label), run_time=1.5
        )
        self.play(Create(spectrum), run_time=2)
        self.wait(3)
        self.play(FadeOut(g3), run_time=2)
        self.wait(1)

    def scene_4(self):
        title = Text(
            "Real and Imaginary Parts as Phase Encoding", font_size=36, color="#ECEFF4"
        )
        title.to_edge(UP, buff=0.5)
        axes = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": True},
        )
        real_label = Text("Real", font_size=24, color="#D8DEE9").next_to(
            axes.x_axis, RIGHT
        )
        imag_label = Text("Imaginary", font_size=24, color="#D8DEE9").next_to(
            axes.y_axis, UP
        )
        vec = Arrow(
            start=ORIGIN, end=[0.9, 0.7, 0], color="#88C0D0", buff=0, stroke_width=3
        )
        vec_label = MathTex(
            r"|X|\angle	heta", font_size=24, color="#88C0D0"
        ).next_to(vec.get_end(), UR)
        dot = Dot(point=[0.9, 0.7, 0], color="#EBCB8B")
        arc = Arc(radius=0.5, start_angle=0, angle=0.6, color="#A3BE8C")
        arc_label = MathTex(r"	heta", font_size=20, color="#A3BE8C").next_to(
            arc, RIGHT, buff=0.1
        )
        ghost_spiral = ParametricFunction(
            lambda t: np.array([np.cos(t), np.sin(t), 0]),
            t_range=[0, 3],
            color="#A3BE8C",
            stroke_width=1.5,
        )
        ghost_spiral.shift(UP * 3)
        ghost_spiral.set_opacity(0.4)
        ghost_label = MathTex(r"e^{i	heta}", font_size=24, color="#A3BE8C").next_to(
            ghost_spiral, UP
        )
        mag_label = Text("Magnitude", font_size=20, color="#D8DEE9").next_to(
            ghost_spiral, LEFT, buff=0.5
        )
        phase_label2 = Text("Phase", font_size=20, color="#D8DEE9").next_to(
            ghost_spiral, RIGHT, buff=0.5
        )
        g4 = VGroup(
            title,
            axes,
            real_label,
            imag_label,
            vec,
            vec_label,
            dot,
            arc,
            arc_label,
            ghost_spiral,
            ghost_label,
            mag_label,
            phase_label2,
        )
        self.play(Write(title), run_time=1.5)
        self.play(Create(axes), FadeIn(real_label), FadeIn(imag_label), run_time=2)
        self.play(GrowFromCenter(vec), FadeIn(vec_label), run_time=1.5)
        self.play(FadeIn(dot), run_time=0.5)
        self.play(Create(arc), FadeIn(arc_label), run_time=1)
        self.play(FadeIn(ghost_spiral), FadeIn(ghost_label), run_time=1.5)
        self.play(FadeIn(mag_label), FadeIn(phase_label2), run_time=1)
        self.wait(4)
        self.play(FadeOut(g4), run_time=2)
        self.wait(2)

    def scene_5(self):
        title = Text(
            "Inverse Fourier Transform and Reconstruction",
            font_size=36,
            color="#ECEFF4",
        )
        title.to_edge(UP, buff=0.5)
        spectrum = FunctionGraph(
            lambda x: np.exp(-((x / 2) ** 2)),
            x_range=[-4, 4],
            color="#A3BE8C",
            stroke_width=3,
        )
        spectrum.shift(LEFT * 5 + UP * 0.5)
        spec_label = Text("Spectrum", font_size=24, color="#A3BE8C").next_to(
            spectrum, UP
        )
        spiral1 = ParametricFunction(
            lambda t: np.array([np.cos(2 * t), np.sin(2 * t), 0]),
            t_range=[0, 3],
            color="#88C0D0",
            stroke_width=2,
        )
        spiral1.shift(LEFT * 2 + UP * 1.5)
        spiral2 = ParametricFunction(
            lambda t: np.array([np.cos(4 * t), np.sin(4 * t), 0]),
            t_range=[0, 3],
            color="#EBCB8B",
            stroke_width=2,
        )
        spiral2.shift(LEFT * 2 + UP * 0.5)
        spiral3 = ParametricFunction(
            lambda t: np.array([np.cos(6 * t), np.sin(6 * t), 0]),
            t_range=[0, 3],
            color="#A3BE8C",
            stroke_width=2,
        )
        spiral3.shift(LEFT * 2 + DOWN * 0.5)
        funnel = Polygon(
            [-1.5, 1, 0],
            [-0.5, 0.3, 0],
            [-0.5, -0.3, 0],
            [-1.5, -1, 0],
            color="#81A1C1",
            stroke_width=2,
            fill_opacity=0.1,
        )
        funnel_label = MathTex(r"\Sigma", font_size=30, color="#81A1C1").next_to(
            funnel, RIGHT
        )
        reconstructed = FunctionGraph(
            lambda x: np.exp(-((x / 1.5) ** 2)),
            x_range=[-3, 3],
            color="#D8DEE9",
            stroke_width=3,
        )
        reconstructed.shift(RIGHT * 4 + UP * 0.5)
        recon_label = Text("Reconstructed", font_size=24, color="#D8DEE9").next_to(
            reconstructed, UP
        )
        checkmark = MathTex(r"\checkmark", font_size=48, color="#A3BE8C")
        checkmark.move_to(RIGHT * 6 + UP * 1.5)
        g5 = VGroup(
            title,
            spectrum,
            spec_label,
            spiral1,
            spiral2,
            spiral3,
            funnel,
            funnel_label,
            reconstructed,
            recon_label,
            checkmark,
        )
        self.play(Write(title), run_time=1.5)
        self.play(Create(spectrum), FadeIn(spec_label), run_time=1.5)
        self.play(Create(spiral1), Create(spiral2), Create(spiral3), run_time=2)
        self.play(Create(funnel), FadeIn(funnel_label), run_time=1.5)
        self.play(Create(reconstructed), FadeIn(recon_label), run_time=2)
        self.play(FadeIn(checkmark), run_time=1)
        self.play(Indicate(checkmark, color="#A3BE8C", scale_factor=1.3), run_time=1)
        self.wait(3)
        self.play(FadeOut(g5), run_time=2)
        self.wait(1)

    def scene_6(self):
        title = Text(
            "Discrete Fourier Transform for Sampled Data", font_size=36, color="#ECEFF4"
        )
        title.to_edge(UP, buff=0.5)
        time_axis = NumberLine(
            x_range=[-5, 5, 1], length=10, color="#ECEFF4", include_numbers=True
        )
        time_axis.move_to(DOWN * 2.5)
        time_label = Text("Time Samples", font_size=24, color="#D8DEE9").next_to(
            time_axis, DOWN, buff=0.2
        )
        signal = FunctionGraph(
            lambda x: np.sinc(x / 1.5), x_range=[-5, 5], color="#88C0D0", stroke_width=3
        )
        signal.shift(DOWN * 0.5)
        signal_label = Text("Analog Signal", font_size=24, color="#88C0D0").next_to(
            signal, UP
        )
        sample_x = np.linspace(-4, 4, 9)
        sample_dots = VGroup()
        sample_lines = VGroup()
        for x in sample_x:
            y = np.sinc(x / 1.5) - 0.5
            dot = Dot(point=np.array([x, y, 0]), color="#BF616A", radius=0.08)
            line = DashedLine(
                start=np.array([x, -2.5, 0]),
                end=np.array([x, y, 0]),
                color="#D8DEE9",
                dash_length=0.1,
            )
            sample_dots.add(dot)
            sample_lines.add(line)
        sample_points = [np.array([x, np.sinc(x / 1.5) - 0.5, 0]) for x in sample_x]
        sample_path = VMobject()
        sample_path.set_points_as_corners(sample_points)
        sample_path.set_color("#D8DEE9")
        sample_path.set_stroke(width=2)
        dft_arrow = Arrow(
            start=LEFT * 1 + UP * 0.5, end=RIGHT * 1 + UP * 0.5, color="#81A1C1"
        )
        dft_label = Text("DFT", font_size=24, color="#81A1C1").next_to(
            dft_arrow, UP, buff=0.2
        )
        freq_axis = Axes(
            x_range=[-6, 6, 1], y_range=[0, 1.2, 0.2], x_length=6, y_length=3
        )
        freq_axis.move_to(RIGHT * 4 + DOWN * 1)
        freq_label = Text("Frequency Bins", font_size=24, color="#D8DEE9").next_to(
            freq_axis, UP
        )
        bin_values = [1.0, 0.8, 0.4, 0.2, 0.2, 0.4, 0.8]
        bin_colors = [
            "#88C0D0",
            "#EBCB8B",
            "#A3BE8C",
            "#81A1C1",
            "#B48EAD",
            "#A3BE8C",
            "#EBCB8B",
        ]
        bin_spacing = 0.7
        bars = VGroup()
        for i, (val, color) in enumerate(zip(bin_values, bin_colors)):
            bar = Rectangle(width=0.4, height=val * 1.5, color=color, fill_opacity=0.8)
            x = 4.0 + (i - len(bin_values) / 2) * bin_spacing
            y = -1.0 + val * 0.75
            bar.move_to(np.array([x, y, 0]))
            bars.add(bar)
        g6 = VGroup(
            title,
            time_axis,
            time_label,
            signal,
            signal_label,
            sample_dots,
            sample_lines,
            sample_path,
            dft_arrow,
            dft_label,
            freq_axis,
            freq_label,
            bars,
        )
        self.play(Write(title), run_time=1.5)
        self.play(Create(time_axis), FadeIn(time_label), run_time=1)
        self.play(Create(signal), FadeIn(signal_label), run_time=2)
        self.play(Create(sample_lines), run_time=1.5)
        self.play(FadeIn(sample_dots), run_time=1)
        self.play(Create(sample_path), run_time=1)
        self.play(GrowFromCenter(dft_arrow), FadeIn(dft_label), run_time=1.5)
        self.play(Create(freq_axis), FadeIn(freq_label), run_time=1)
        self.play(Create(bars), run_time=2)
        self.wait(2)
        self.play(FadeOut(g6), run_time=2)
        self.wait(1)

    def scene_7(self):
        title = Text(
            "Fast Fourier Transform Algorithmic Speedup", font_size=36, color="#ECEFF4"
        )
        title.to_edge(UP, buff=0.5)
        grid = VGroup()
        for row in range(8):
            for col in range(8):
                dot = Dot(
                    point=LEFT * 4 + col * 0.4 * RIGHT + row * 0.4 * DOWN,
                    color="#BF616A",
                    radius=0.08,
                )
                grid.add(dot)
        grid_label = Text("O(N²)", font_size=24, color="#BF616A").next_to(
            grid, DOWN, buff=0.3
        )
        speed_arrow = Arrow(start=LEFT * 2.5, end=RIGHT * 1.0, color="#81A1C1")
        speed_label = Text("FFT Speed-up", font_size=24, color="#81A1C1").next_to(
            speed_arrow, UP, buff=0.2
        )
        butterfly = VGroup()
        stages = 4
        node_spacing = 0.6
        x_start = 2.5
        for stage in range(stages):
            num_nodes = 2 ** (stages - stage - 1)
            y_offset = (num_nodes - 1) * node_spacing / 2
            for node in range(num_nodes):
                x = x_start + stage * 1.5
                y = node * node_spacing - y_offset
                butterfly_dot = Dot(point=[x, y, 0], color="#88C0D0", radius=0.08)
                butterfly.add(butterfly_dot)
                if stage > 0:
                    prev_num = 2 ** (stages - stage)
                    for prev in range(prev_num):
                        prev_y = prev * node_spacing - (prev_num - 1) * node_spacing / 2
                        line = Line(
                            start=[x - 1.5, prev_y, 0],
                            end=[x, y, 0],
                            color="#88C0D0",
                            stroke_width=1,
                        )
                        butterfly.add(line)
        butterfly_label = Text(
            "Butterfly Network", font_size=24, color="#88C0D0"
        ).next_to(butterfly, DOWN, buff=0.3)
        speedometer = Arc(
            radius=1.0, start_angle=PI, angle=PI, color="#A3BE8C", stroke_width=4
        )
        speedometer.move_to(np.array([5.5, 2.5, 0]))
        speed_label_slow = Text("Slow", font_size=20, color="#D8DEE9").next_to(
            speedometer, LEFT
        )
        speed_label_fast = Text("Fast", font_size=20, color="#A3BE8C").next_to(
            speedometer, RIGHT
        )
        needle = Line(
            start=np.array([5.5, 2.5, 0]),
            end=np.array([5.0, 1.6, 0]),
            color="#A3BE8C",
            stroke_width=3,
        )
        needle_label = Text("Speed", font_size=20, color="#A3BE8C").next_to(needle, UP)
        g7 = VGroup(
            title,
            grid,
            grid_label,
            speed_arrow,
            speed_label,
            butterfly,
            butterfly_label,
            speedometer,
            speed_label_slow,
            speed_label_fast,
            needle,
            needle_label,
        )
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(grid), FadeIn(grid_label), run_time=2)
        self.play(GrowFromCenter(speed_arrow), FadeIn(speed_label), run_time=1.5)
        self.play(Create(butterfly), FadeIn(butterfly_label), run_time=2)
        self.play(
            Create(speedometer),
            FadeIn(speed_label_slow),
            FadeIn(speed_label_fast),
            run_time=1.5,
        )
        self.play(Create(needle), FadeIn(needle_label), run_time=1)
        self.play(
            Rotate(needle, angle=-PI + 0.3, about_point=np.array([5.5, 2.5, 0])),
            run_time=2,
        )
        self.wait(2)
        self.play(FadeOut(g7), run_time=2)
        self.wait(1)

    def scene_8(self):
        title = Text(
            "Practical Application: Filtering and Spectrograms",
            font_size=36,
            color="#ECEFF4",
        )
        title.to_edge(UP, buff=0.5)
        noisy = FunctionGraph(
            lambda x: np.sin(x) + 0.3 * np.sin(5 * x),
            x_range=[-5, 5],
            color="#BF616A",
            stroke_width=2,
        )
        noisy.shift(LEFT * 5 + UP * 2)
        noisy_label = Text("Noisy Input", font_size=24, color="#BF616A").next_to(
            noisy, UP
        )
        mask = Rectangle(
            width=4, height=2, color="#D8DEE9", stroke_width=2, fill_opacity=0.3
        )
        mask.move_to(np.array([-0.5, 1.5, 0]))
        mask_label = Text("Low-pass Mask", font_size=24, color="#D8DEE9").next_to(
            mask, UP
        )
        spectrum_values = [1.0, 0.9, 0.7, 0.3, 0, 0, 0, 0, 0]
        spectrum_colors = [
            "#88C0D0",
            "#81A1C1",
            "#EBCB8B",
            "#A3BE8C",
            "#D8DEE9",
            "#D8DEE9",
            "#D8DEE9",
            "#D8DEE9",
            "#D8DEE9",
        ]
        bars = VGroup()
        for i, (val, color) in enumerate(zip(spectrum_values, spectrum_colors)):
            bar = Rectangle(width=0.3, height=val * 1.5, color=color, fill_opacity=0.8)
            bar.move_to(np.array([-2.0 + i * 0.5, 1.5 + val * 0.75, 0]))
            bars.add(bar)
        clean = FunctionGraph(
            lambda x: np.sin(x), x_range=[-5, 5], color="#A3BE8C", stroke_width=3
        )
        clean.shift(RIGHT * 5 + UP * 2)
        clean_label = Text("Clean Output", font_size=24, color="#A3BE8C").next_to(
            clean, UP
        )
        spec_grid = Rectangle(width=12, height=4, color="#ECEFF4", stroke_width=2)
        spec_grid.move_to(DOWN * 2.5)
        spec_grid_label = Text(
            "Spectrogram Heatmap", font_size=24, color="#D8DEE9"
        ).next_to(spec_grid, UP)
        spec_bars = VGroup()
        for row in range(5):
            for col in range(20):
                intensity = np.random.rand() * 0.5 + 0.3
                bar = Rectangle(
                    width=0.5, height=0.3, color="#88C0D0", fill_opacity=intensity
                )
                bar.move_to(np.array([-5.5 + col * 0.6, -3.5 + row * 0.5, 0]))
                spec_bars.add(bar)
        legend = VGroup()
        for i in range(5):
            box = Rectangle(
                width=0.3, height=0.3, color="#88C0D0", fill_opacity=0.2 + i * 0.2
            )
            box.move_to(np.array([5.5, -1.5 + i * 0.4, 0]))
            legend.add(box)
        legend_label = Text("Amplitude", font_size=20, color="#D8DEE9").next_to(
            legend, RIGHT
        )
        g8 = VGroup(
            title,
            noisy,
            noisy_label,
            mask,
            mask_label,
            bars,
            clean,
            clean_label,
            spec_grid,
            spec_grid_label,
            spec_bars,
            legend,
            legend_label,
        )
        self.play(Write(title), run_time=1.5)
        self.play(Create(noisy), FadeIn(noisy_label), run_time=2)
        self.play(FadeIn(mask), FadeIn(mask_label), run_time=1)
        self.play(Create(bars), run_time=2)
        self.play(Create(clean), FadeIn(clean_label), run_time=2)
        self.play(Create(spec_grid), FadeIn(spec_grid_label), run_time=1)
        self.play(FadeIn(spec_bars), run_time=2)
        self.play(FadeIn(legend), FadeIn(legend_label), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(g8), run_time=2)
        self.wait(1)
