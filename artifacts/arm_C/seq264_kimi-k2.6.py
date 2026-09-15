from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 6: Common pitfalls in backpropagation ---
        # Use the specified dark background
        self.camera.background_color = "#181825"

        # ====== 1. Faint cyan-pink grid ======
        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": "#89b4fa",
                "stroke_opacity": 0.15,
                "stroke_width": 1,
            },
            axis_config={
                "stroke_color": "#89b4fa",
                "stroke_opacity": 0.3,
            },
        )
        grid.fade(0.7)

        # ====== 2. Four pulsing neural nodes ======
        positions = {
            "nw": UP * 2.3 + LEFT * 3.5,
            "ne": UP * 2.3 + RIGHT * 3.5,
            "sw": DOWN * 2.3 + LEFT * 3.5,
            "se": DOWN * 2.3 + RIGHT * 3.5,
        }
        palette = ["#f38ba8", "#94e2d5", "#fab387", "#a6e3a1"]
        nodes = VGroup()
        cores = []
        halos = []
        for i, (key, pos) in enumerate(positions.items()):
            core = Circle(
                radius=0.12, fill_color=palette[i], fill_opacity=1, stroke_width=0
            )
            halo = Circle(
                radius=0.2,
                stroke_color=palette[i],
                stroke_opacity=0.6,
                stroke_width=2,
                fill_opacity=0,
            )
            core.set_z_index(2)
            halo.set_z_index(0)
            group = VGroup(core, halo).move_to(pos)
            nodes.add(group)
            cores.append(core)
            halos.append(halo)

        # ====== 3. The Big Title ======
        title = Text(
            "Backpropagation",
            font="Sans",
            color="#BB9AF7",
        ).scale(1.5)
        title.set_z_index(3)

        # =========== ANIMATIONS ===========
        # Show grid faintly behind everything (1.5s)
        self.play(FadeIn(grid, shift=UP * 0.2), run_time=1.5)

        # Title fades in with a slight scale-up (1.5s)
        self.play(
            FadeIn(title, scale=1.2),
            run_time=1.5,
            rate_func=smooth,
        )

        # Nodes gently pulse into existence (2.0s)
        self.play(
            LaggedStart(*[GrowFromCenter(core) for core in cores], lag_ratio=0.3),
            run_time=2.0,
        )

        # Gentle pulsing halos (0.8s)
        self.play(
            *[h.animate.scale(1.3).set_stroke(opacity=0.3) for h in halos],
            run_time=0.8,
            rate_func=there_and_back,
        )

        # Pad remaining time (6.0 - 1.5 - 1.5 - 2.0 - 0.8 = 0.2s)
        self.wait(0.2)
        # --- Scene 5: Practical application of backpropagation ---
        self.clear()

        # ── 1. CONFIGURATION ───────────────────────────────────────────
        self.camera.background_color = "#181825"

        # Palette
        C_BLUE = "#89b4fa"
        C_PEACH = "#fab387"
        C_PINK = "#f38ba8"
        C_GREEN = "#a6e3a1"
        C_TEAL = "#94e2d5"
        C_WHITE = "#cdd6f4"

        # ── 2. PIPE BACKGROUND ───────────────────────────────────────
        pipe = Rectangle(
            height=2.5, width=12, color=C_BLUE, fill_opacity=0.1, stroke_width=2
        ).to_edge(LEFT, buff=0.5)

        # Stage labels
        lbl_input = Text("INPUT", font_size=20, color=C_TEAL)
        lbl_weights = Text("WEIGHTS", font_size=20, color=C_PEACH)
        lbl_output = Text("OUTPUT", font_size=20, color=C_GREEN)

        # ── 3. SHAPE GROUPS (flowing through pipeline) ─────────────────
        # Input     → Squares
        # Weights   → Diamonds (rotated squares)
        # Output    → Circles
        input_shapes = VGroup(
            *[
                Square(side_length=0.4)
                .set_fill(C_TEAL, opacity=0.85)
                .set_stroke(C_TEAL, width=2)
                for _ in range(3)
            ]
        )
        weight_shapes = VGroup(
            *[
                Square(side_length=0.4)
                .rotate(PI / 4)
                .set_fill(C_PEACH, opacity=0.85)
                .set_stroke(C_PEACH, width=2)
                for _ in range(3)
            ]
        )
        output_shapes = VGroup(
            *[
                Circle(radius=0.22)
                .set_fill(C_GREEN, opacity=0.85)
                .set_stroke(C_GREEN, width=2)
                for _ in range(3)
            ]
        )

        # Arrange vertically
        input_shapes.arrange(DOWN, buff=0.35)
        weight_shapes.arrange(DOWN, buff=0.35)
        output_shapes.arrange(DOWN, buff=0.35)

        # Position inside pipe
        input_shapes.move_to(pipe.get_left() + RIGHT * 1.6)
        weight_shapes.move_to(pipe.get_center())
        output_shapes.move_to(pipe.get_right() + LEFT * 1.6)

        # Labels above their columns
        lbl_input.next_to(input_shapes, UP, buff=0.6)
        lbl_weights.next_to(weight_shapes, UP, buff=0.6)
        lbl_output.next_to(output_shapes, UP, buff=0.6)

        # ── 4. DATA-FLOW ARROWS ──────────────────────────────────────
        arrow_in_w = Arrow(
            input_shapes.get_right(), weight_shapes.get_left(), color=C_BLUE, buff=0.25
        )
        arrow_w_out = Arrow(
            weight_shapes.get_right(), output_shapes.get_left(), color=C_BLUE, buff=0.25
        )
        arrow_out = Arrow(
            output_shapes.get_right(),
            output_shapes.get_right() + RIGHT * 1.8,
            color=C_BLUE,
            buff=0.1,
        )

        # ── 5. ERROR BAR CHART (far right) ───────────────────────────
        chart_title = Text("ERROR", font_size=20, color=C_PINK)

        # Shrinking error values
        error_vals = [2.5, 2.0, 1.4, 0.9, 0.35]
        bar_colors = [C_PINK, C_PINK, C_PINK, C_PEACH, C_GREEN]

        bars = VGroup()
        for val, col in zip(error_vals, bar_colors):
            bar = Rectangle(
                width=0.38,
                height=val * 0.65,
                fill_color=col,
                fill_opacity=0.9,
                stroke_width=1,
                stroke_color=C_WHITE,
            )
            bars.add(bar)

        bars.arrange(RIGHT, buff=0.25)
        bars.next_to(arrow_out, RIGHT, buff=0.6)
        chart_title.next_to(bars, UP, buff=0.35)

        # ── 6. ANIMATIONS ────────────────────────────────────────────
        # Duration budget: 8.0 s
        #   0.0 - 0.8  : Pipe draws in
        #   0.8 - 1.6  : Labels fade in
        #   1.6 - 3.4  : Shapes cascade in (3 × 0.6)
        #   3.4 - 4.2  : Arrows draw
        #   4.2 - 4.8  : Flow arrow + charts fade in
        #   4.8 - 7.0  : Bars grow one-by-one (5 × 0.44)
        #   7.0 - 7.8  : Indication on best bar
        #   7.8 - 8.0  : Hold

        self.play(Create(pipe), run_time=0.8)

        self.play(
            FadeIn(lbl_input), FadeIn(lbl_weights), FadeIn(lbl_output), run_time=0.8
        )

        # Cascade the shape groups one after another (top,mid,bottom)
        for i in range(3):
            self.play(
                FadeIn(input_shapes[i], scale=0.5),
                FadeIn(weight_shapes[i], scale=0.5),
                FadeIn(output_shapes[i], scale=0.5),
                run_time=0.6,
            )

        self.play(Create(arrow_in_w), Create(arrow_w_out), run_time=0.8)

        self.play(FadeIn(arrow_out, scale=0.5), run_time=0.6)

        # Error bars shrink pass-by-pass
        for bar in bars:
            self.play(GrowFromCenter(bar), run_time=0.44)

        self.play(FadeIn(chart_title), run_time=0.4)

        # Emphasize the final (green) bar = backprop succeeded
        self.play(Indicate(bars[-1], color=C_GREEN, scale_factor=1.4), run_time=0.8)

        # Hold
        self.wait(0.2)
