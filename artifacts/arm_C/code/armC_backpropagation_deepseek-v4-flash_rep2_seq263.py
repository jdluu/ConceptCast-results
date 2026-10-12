import numpy as np
from manim import *


class SceneGen(Scene):
    def construct(self):
        # --- Scene 1: Forward Pass: Computing the Network's Output ---
        self.clear()
        self.camera.background_color = "#181825"

        # Define colors matching the palette
        blue = "#89B4FA"
        green = "#A6E3A1"
        orange = "#FAB387"
        text_color = "#CDD6F4"
        secondary_text = "#A6ADC8"

        # === PHASE 1: Title and Input (0 - 1.4s) ===

        # Title
        title = Text("Forward Pass", font_size=42, color=text_color, font="Sans")
        title.to_edge(UP, buff=0.8)
        self.play(Write(title), run_time=0.5)

        # Input label (x)
        input_label = MathTex("x", color=secondary_text, font_size=36)
        input_label.move_to(LEFT * 5.8)
        self.play(FadeIn(input_label, scale=0.5), run_time=0.3)

        # Input arrow
        input_arrow = Arrow(
            start=LEFT * 5.5,
            end=LEFT * 3.1,
            color=blue,
            stroke_width=3,
            tip_length=0.25,
        )
        self.play(GrowFromCenter(input_arrow), run_time=0.6)

        # === PHASE 2: Neuron 1 with gear effect (1.4 - 3.0s) ===

        # Weight label w1
        w1_label = MathTex("w_1", color=blue, font_size=28)
        w1_label.move_to(LEFT * 3.2)
        self.play(FadeIn(w1_label, scale=0.5), run_time=0.25)

        # Neuron 1 (gear)
        n1 = Circle(radius=0.6, color=blue, fill_opacity=0.3, stroke_width=3)
        n1.move_to(LEFT * 2.5)
        self.play(Create(n1), run_time=0.35)

        # Inner gear details (small dashes around the circle)
        gear_teeth_1 = VGroup()
        for i in range(12):
            angle = i * TAU / 12
            start_point = LEFT * 2.5 + np.array(
                [0.5 * np.cos(angle), 0.5 * np.sin(angle), 0]
            )
            end_point = LEFT * 2.5 + np.array(
                [0.7 * np.cos(angle), 0.7 * np.sin(angle), 0]
            )
            tooth = Line(start_point, end_point, color=blue, stroke_width=2.5)
            gear_teeth_1.add(tooth)

        self.play(
            LaggedStart(*[Create(t) for t in gear_teeth_1], lag_ratio=0.05),
            run_time=0.45,
        )

        # Start spinning neuron 1
        self.play(
            Rotate(n1, angle=TAU, rate_func=linear, run_time=0.55),
            Rotate(gear_teeth_1, angle=TAU, rate_func=linear, run_time=0.55),
        )

        # === PHASE 3: Connection to Neuron 2 and spin transfer (3.0 - 4.5s) ===

        # Connecting rod from n1 to n2
        conn_1 = Line(LEFT * 1.9, LEFT * 0.6, color=blue, stroke_width=2.5)
        self.play(Create(conn_1), run_time=0.2)

        # Weight label w2
        w2_label = MathTex("w_2", color=green, font_size=28)
        w2_label.move_to(LEFT * 0.7)
        self.play(FadeIn(w2_label, scale=0.5), run_time=0.2)

        # Neuron 2 (gear)
        n2 = Circle(radius=0.6, color=green, fill_opacity=0.3, stroke_width=3)
        n2.move_to(ORIGIN)
        self.play(Create(n2), run_time=0.3)

        # Gear teeth for n2
        gear_teeth_2 = VGroup()
        for i in range(12):
            angle = i * TAU / 12
            start_point = ORIGIN + np.array(
                [0.5 * np.cos(angle), 0.5 * np.sin(angle), 0]
            )
            end_point = ORIGIN + np.array([0.7 * np.cos(angle), 0.7 * np.sin(angle), 0])
            tooth = Line(start_point, end_point, color=green, stroke_width=2.5)
            gear_teeth_2.add(tooth)

        self.play(
            LaggedStart(*[Create(t) for t in gear_teeth_2], lag_ratio=0.05),
            run_time=0.3,
        )

        # Spin both neuron 1 and 2
        self.play(
            Rotate(n1, angle=TAU * 2, rate_func=linear, run_time=0.5),
            Rotate(gear_teeth_1, angle=TAU * 2, rate_func=linear, run_time=0.5),
            Rotate(n2, angle=TAU, rate_func=linear, run_time=0.5),
            Rotate(gear_teeth_2, angle=TAU, rate_func=linear, run_time=0.5),
        )

        # === PHASE 4: Connection to Neuron 3 and output (4.5 - 6.1s) ===

        # Connecting rod from n2 to n3
        conn_2 = Line(RIGHT * 0.6, RIGHT * 1.9, color=green, stroke_width=2.5)
        self.play(Create(conn_2), run_time=0.2)

        # Weight label w3
        w3_label = MathTex("w_3", color=orange, font_size=28)
        w3_label.move_to(RIGHT * 1.8)
        self.play(FadeIn(w3_label, scale=0.5), run_time=0.15)

        # Neuron 3 (gear)
        n3 = Circle(radius=0.6, color=orange, fill_opacity=0.3, stroke_width=3)
        n3.move_to(RIGHT * 2.5)
        self.play(Create(n3), run_time=0.3)

        # Gear teeth for n3
        gear_teeth_3 = VGroup()
        for i in range(12):
            angle = i * TAU / 12
            start_point = RIGHT * 2.5 + np.array(
                [0.5 * np.cos(angle), 0.5 * np.sin(angle), 0]
            )
            end_point = RIGHT * 2.5 + np.array(
                [0.7 * np.cos(angle), 0.7 * np.sin(angle), 0]
            )
            tooth = Line(start_point, end_point, color=orange, stroke_width=2.5)
            gear_teeth_3.add(tooth)

        self.play(
            LaggedStart(*[Create(t) for t in gear_teeth_3], lag_ratio=0.05),
            run_time=0.3,
        )

        # Output arrow
        output_arrow = Arrow(
            start=RIGHT * 3.1,
            end=RIGHT * 4.0,
            color=orange,
            stroke_width=3,
            tip_length=0.25,
        )
        self.play(GrowFromCenter(output_arrow), run_time=0.3)

        # Output label y_pred
        output_label = MathTex(r"\hat{y}", color=orange, font_size=38)
        output_label.next_to(output_arrow, RIGHT, buff=0.15)
        self.play(Write(output_label), run_time=0.25)

        # === PHASE 5: Glow effect on final neuron and brief hold (6.1 - 7.0s) ===

        # Final spin with all three gears spinning
        self.play(
            Rotate(n1, angle=TAU * 2, rate_func=linear, run_time=0.4),
            Rotate(gear_teeth_1, angle=TAU * 2, rate_func=linear, run_time=0.4),
            Rotate(n2, angle=TAU * 2, rate_func=linear, run_time=0.4),
            Rotate(gear_teeth_2, angle=TAU * 2, rate_func=linear, run_time=0.4),
            Rotate(n3, angle=TAU, rate_func=linear, run_time=0.4),
            Rotate(gear_teeth_3, angle=TAU, rate_func=linear, run_time=0.4),
        )

        # Glow effect on neuron 3 - indicate it
        self.play(Indicate(n3, color=orange, scale_factor=1.2), run_time=0.5)

        # Final hold to complete 7.0s
        self.wait(0.1)
        # --- Scene 2: Loss Function: Measuring Prediction Error ---
        self.clear()
        self.camera.background_color = "#181825"

        # Colors from catppuccin_mocha palette
        text_color = "#CDD6F4"
        accent_red = "#F38BA8"
        accent_gold = "#FAB387"
        accent_green = "#A6E3A1"
        accent_blue = "#89B4FA"

        # --- Objects ---
        # Title
        title = Text("Loss Function", font="Sans", font_size=48, color=text_color)
        title.move_to(UP * 3.2)

        # Target center (bullseye)
        ring_center = LEFT * 0.5
        target_center = Dot(
            point=ring_center,
            radius=0.15,
            color=accent_gold,
            fill_opacity=1.0,
            stroke_width=0,
        )

        # Concentric rings (centered at ring_center)
        ring4 = Circle(
            radius=2.4, color=accent_blue, stroke_width=1.5, fill_opacity=0.1
        )
        ring4.move_to(ring_center)

        ring3 = Circle(radius=1.8, color=accent_green, stroke_width=2, fill_opacity=0.0)
        ring3.move_to(ring_center)

        ring2 = Circle(radius=1.2, color=accent_gold, stroke_width=2, fill_opacity=0.0)
        ring2.move_to(ring_center)

        ring1 = Circle(radius=0.6, color=accent_red, stroke_width=3, fill_opacity=0.0)
        ring1.move_to(ring_center)

        # Arrow from bullseye to prediction landing point
        pred_point = RIGHT * 2.0 + UP * 0.3
        prediction_arrow = Arrow(
            start=ring_center,
            end=pred_point,
            color=accent_red,
            tip_length=0.25,
            stroke_width=4,
            buff=0,
        )

        # Labels
        true_label = Text("True Label", font="Sans", font_size=28, color=text_color)
        true_label.move_to(DOWN * 3.2 + LEFT * 0.5)

        pred_label = Text("Prediction", font="Sans", font_size=28, color=accent_red)
        pred_label.next_to(pred_point, RIGHT, buff=0.25)

        # Glowing measuring brace between bullseye and prediction
        measure_brace = BraceBetweenPoints(
            point_1=ring_center, point_2=pred_point, direction=UP, color=accent_gold
        )
        measure_brace.stroke_width = 2.5

        # Brace annotation
        loss_label = MathTex(
            r"	ext{Loss} = L(y, \hat{y})", font_size=34, color=accent_green
        )
        loss_label.next_to(measure_brace, UP, buff=0.15)

        # --- Animation Sequence (total: 6.5s) ---

        # 1. Title slides in (0.5s)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.5)

        # 2. Concentric rings unfurl outward-to-inward (1.2s)
        self.play(
            LaggedStart(
                Create(ring4),
                Create(ring3),
                Create(ring2),
                Create(ring1),
                lag_ratio=0.2,
            ),
            run_time=1.2,
        )

        # 3. Bullseye pulses into existence (0.3s)
        self.play(GrowFromCenter(target_center), run_time=0.3)

        # 4. Arrow draws from center to prediction point (0.5s)
        self.play(Create(prediction_arrow), run_time=0.5)

        # 5. Both labels fade in simultaneously (0.6s)
        self.play(Write(true_label), Write(pred_label), run_time=0.6)

        # 6. Measuring brace grows across the gap (0.5s)
        self.play(GrowFromCenter(measure_brace), run_time=0.5)

        # 7. Loss formula appears (0.4s)
        self.play(Write(loss_label), run_time=0.4)

        # 8. Glow highlight on brace + label (0.7s)
        self.play(
            Indicate(measure_brace, color=accent_gold, scale_factor=1.05), run_time=0.7
        )

        # 9. Pause to let the concept sink in (1.8s)
        self.wait(1.8)
        # --- Scene 3: Goal of Backpropagation: Minimizing the Loss ---
        # ---- Palette (Catppuccin Mocha) ----
        BG = "#1E1E2E"
        TEXT = "#CDD6F4"
        SUBTLE = "#A6ADC8"
        CURVE = "#FAB387"
        HIKER = "#F38BA8"
        ARROW = "#A6E3A1"
        AXIS = "#89B4FA"
        ACCENT = "#CBA6F7"

        self.camera.background_color = BG

        total_time = 6.0
        t_remaining = total_time

        # ---------- 1. Title ----------
        title = Text("Minimizing the Loss", font_size=40, color=TEXT)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.5)
        t_remaining -= 0.5

        # ---------- 2. Axes ----------
        axes = Axes(
            x_range=[-4, 4, 0.5],
            y_range=[-1, 5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={"color": AXIS, "stroke_width": 1.5},
        )
        axes.shift(DOWN * 0.4)

        x_label = MathTex("x", color=AXIS, font_size=28).next_to(
            axes.x_axis.get_end(), DOWN
        )
        y_label = MathTex("\	ext{Loss}", color=AXIS, font_size=28).next_to(
            axes.y_axis.get_end(), LEFT
        )

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=0.6)
        t_remaining -= 0.6

        # ---------- 3. Parabola ----------
        def loss_func(x):
            return (x - 1) ** 2 / 2 + 0.2

        parabola = axes.plot(
            loss_func, x_range=[-3.5, 3.5], color=CURVE, stroke_width=4
        )
        self.play(Create(parabola), run_time=0.6)
        t_remaining -= 0.6

        # ---------- 4. Valley (Global Minimum) ----------
        valley_x = 1.0
        valley_y = loss_func(valley_x)
        valley_point = axes.coords_to_point(valley_x, valley_y)

        valley_dot = Dot(valley_point, radius=0.15, color=ACCENT)
        valley_dot.set_fill(ACCENT, opacity=1.0)

        glow = Circle(
            radius=0.3,
            color=ACCENT,
            stroke_width=2,
            fill_opacity=0.15,
            fill_color=ACCENT,
        )
        glow.move_to(valley_point)

        min_label = Text("Global Minimum", font_size=24, color=ACCENT)
        min_label.next_to(valley_dot, DOWN + RIGHT, buff=0.15)

        self.play(
            FadeIn(valley_dot, scale=0.5),
            FadeIn(glow, scale=0.5),
            Write(min_label),
            run_time=0.5,
        )
        t_remaining -= 0.5

        # ---------- 5. Hiker ----------
        hiker_x = -2.0
        hiker_y = loss_func(hiker_x)
        hiker_point = axes.coords_to_point(hiker_x, hiker_y)

        hiker_dot = Dot(hiker_point, radius=0.22, color=HIKER)
        hiker_dot.set_fill(HIKER, opacity=1.0)

        hiker_label = Text("Hiker (Loss)", font_size=22, color=TEXT)
        hiker_label.next_to(hiker_dot, UP, buff=0.25)

        self.play(FadeIn(hiker_dot, scale=0.5), Write(hiker_label), run_time=0.5)
        t_remaining -= 0.5

        # ---------- 6. Downhill Arrows ----------
        arrow_end_1 = axes.coords_to_point(hiker_x + 0.6, hiker_y - 0.8)
        arrow_end_2 = axes.coords_to_point(hiker_x - 0.4, hiker_y - 0.3)
        arrow_end_3 = axes.coords_to_point(hiker_x + 0.2, hiker_y - 1.0)

        arrow1 = Arrow(
            start=hiker_point,
            end=arrow_end_1,
            color=ARROW,
            stroke_width=3,
            tip_length=0.18,
            buff=0.1,
        )
        arrow2 = Arrow(
            start=hiker_point,
            end=arrow_end_2,
            color=ARROW,
            stroke_width=2.5,
            tip_length=0.15,
            buff=0.1,
        )
        arrow3 = Arrow(
            start=hiker_point,
            end=arrow_end_3,
            color=ARROW,
            stroke_width=2.5,
            tip_length=0.15,
            buff=0.1,
        )

        self.play(
            LaggedStart(
                Create(arrow1),
                Create(arrow2),
                Create(arrow3),
                lag_ratio=0.15,
            ),
            run_time=0.7,
        )
        t_remaining -= 0.7

        # ---------- 7. Dashed steepest-descent path ----------
        path_points = []
        steps = 40
        for i in range(steps + 1):
            t = i / steps
            x = hiker_x + (valley_x - hiker_x) * t
            y = loss_func(x)
            path_points.append(axes.coords_to_point(x, y))

        # Build dashed path from alternating segments
        dash_segments = VGroup()
        for i in range(0, len(path_points) - 1, 2):
            p1 = path_points[i]
            p2 = path_points[i + 1]
            seg = Line(p1, p2, color=SUBTLE, stroke_width=2.5)
            dash_segments.add(seg)

        self.play(Create(dash_segments), run_time=0.7)
        t_remaining -= 0.7

        # ---------- 8. Green flash highlight along path ----------
        flash_rect = SurroundingRectangle(
            VGroup(dash_segments, hiker_dot, valley_dot, min_label),
            color=ACCENT,
            buff=0.15,
            stroke_width=2.5,
        )
        flash_rect.set_fill(ACCENT, opacity=0.08)

        self.play(FadeIn(flash_rect, scale=0.95), run_time=0.3)
        self.play(FadeOut(flash_rect), run_time=0.3)
        t_remaining -= 0.6

        # ---------- 9. Hold remaining time ----------
        if t_remaining > 0:
            self.wait(t_remaining)
        else:
            self.wait(0.3)
        # --- Scene 4: Chain Rule: The Mathematical Engine ---
        self.clear()
        # --- Scene 4: Chain Rule: The Mathematical Engine ---
        # Set background color
        self.camera.background_color = "#1E1E2E"

        # ─── Title ───
        title = Text("Chain Rule", font="Sans", font_size=52, color="#CDD6F4")
        title.to_edge(UP, buff=0.6)
        self.play(Write(title, run_time=0.8))
        self.wait(0.2)

        # ─── Create the three nested "Russian dolls" (RoundedRectangles) ───
        # Outer doll — blue
        outer_doll = RoundedRectangle(
            width=6.0,
            height=4.0,
            corner_radius=0.5,
            stroke_color="#89B4FA",
            stroke_width=3,
            fill_color="#89B4FA",
            fill_opacity=0.08,
        )
        outer_doll.shift(UP * 0.1)

        # Middle doll — green
        middle_doll = RoundedRectangle(
            width=4.5,
            height=2.8,
            corner_radius=0.4,
            stroke_color="#A6E3A1",
            stroke_width=3,
            fill_color="#A6E3A1",
            fill_opacity=0.12,
        )
        middle_doll.shift(UP * 0.05)

        # Inner doll — peach/orange
        inner_doll = RoundedRectangle(
            width=3.0,
            height=1.6,
            corner_radius=0.3,
            stroke_color="#FAB387",
            stroke_width=3,
            fill_color="#FAB387",
            fill_opacity=0.18,
        )
        inner_doll.shift(DOWN * 0.05)

        # Center the dolls
        doll_group = VGroup(outer_doll, middle_doll, inner_doll)
        doll_group.move_to(ORIGIN)

        # Animate dolls appearing (outer → middle → inner)
        self.play(Create(outer_doll, run_time=1.0))
        self.play(Create(middle_doll, run_time=0.8))
        self.play(Create(inner_doll, run_time=0.6))
        self.wait(0.3)

        # ─── Labels (partial derivative terms inside each doll) ───
        outer_label = MathTex(r"\frac{dL}{dy}", color="#F38BA8", font_size=42)
        outer_label.next_to(outer_doll, UP, buff=0.25)
        outer_label.shift(LEFT * 0.3)

        middle_label = MathTex(r"\frac{dy}{dz}", color="#A6E3A1", font_size=36)
        middle_label.move_to(middle_doll.get_center() + UP * 0.1)

        inner_label = MathTex(r"\frac{dz}{dw}", color="#89B4FA", font_size=30)
        inner_label.move_to(inner_doll.get_center())

        self.play(
            FadeIn(outer_label, shift=DOWN * 0.2, run_time=0.6),
            FadeIn(middle_label, scale=0.5, run_time=0.6),
            FadeIn(inner_label, scale=0.5, run_time=0.6),
        )
        self.wait(0.3)

        # ─── Glowing golden connection arrows ───
        arrow_1_start = outer_doll.get_right() + LEFT * 0.3 + DOWN * 0.2
        arrow_1_end = middle_doll.get_right() + LEFT * 0.3 + UP * 0.2
        arrow_1 = Arrow(
            start=arrow_1_start,
            end=arrow_1_end,
            color="#FAB387",
            stroke_width=4,
            tip_length=0.2,
            buff=0,
        )

        arrow_2_start = middle_doll.get_left() + RIGHT * 0.3 + DOWN * 0.1
        arrow_2_end = inner_doll.get_left() + RIGHT * 0.3 + UP * 0.1
        arrow_2 = Arrow(
            start=arrow_2_start,
            end=arrow_2_end,
            color="#FAB387",
            stroke_width=4,
            tip_length=0.2,
            buff=0,
        )

        self.play(Create(arrow_1, run_time=0.5), Create(arrow_2, run_time=0.5))

        tip_dot_1 = Dot(point=arrow_1.get_end(), radius=0.08, color="#FAB387")
        tip_dot_2 = Dot(point=arrow_2.get_end(), radius=0.08, color="#FAB387")
        self.add(tip_dot_1, tip_dot_2)
        self.wait(0.2)

        # ─── Chain equation at the bottom ───
        chain_eq = MathTex(
            r"\frac{dL}{dw} = \frac{dL}{dy} \cdot \frac{dy}{dz} \cdot \frac{dz}{dw}",
            color="#FAB387",
            font_size=38,
        )
        chain_eq.next_to(outer_doll, DOWN, buff=0.8)
        self.play(Write(chain_eq, run_time=1.2))
        self.wait(0.3)

        # ─── Highlight individual terms ───
        chain_eq_highlighted = MathTex(
            r"\frac{dL}{dw}",
            r" = ",
            r"\frac{dL}{dy}",
            r" \cdot ",
            r"\frac{dy}{dz}",
            r" \cdot ",
            r"\frac{dz}{dw}",
            color="#FAB387",
            font_size=38,
        )
        chain_eq_highlighted.next_to(outer_doll, DOWN, buff=0.8)

        self.play(Transform(chain_eq, chain_eq_highlighted, run_time=0.5))

        # Highlight dL/dy (pink → matches outer_label)
        self.play(
            chain_eq_highlighted[2].animate.set_color("#F38BA8"),
            Indicate(outer_label, color="#F38BA8", scale_factor=1.1, run_time=0.6),
        )
        self.wait(0.2)

        # Highlight dy/dz (green → matches middle_label)
        self.play(
            chain_eq_highlighted[4].animate.set_color("#A6E3A1"),
            Indicate(middle_label, color="#A6E3A1", scale_factor=1.1, run_time=0.6),
        )
        self.wait(0.2)

        # Highlight dz/dw (blue → matches inner_label)
        self.play(
            chain_eq_highlighted[6].animate.set_color("#89B4FA"),
            Indicate(inner_label, color="#89B4FA", scale_factor=1.1, run_time=0.6),
        )
        self.wait(0.2)

        # ─── Final polish: golden circumscribe on the full chain ───
        # Note: Circumscribe only accepts shape=Rectangle or shape=Circle
        self.play(
            Circumscribe(
                chain_eq_highlighted,
                shape=Rectangle,
                color="#FAB387",
                buff=0.15,
                stroke_width=2,
                run_time=1.2,
            )
        )
        self.wait(0.5)

        # ─── Hold final scene ───
        self.wait(1.0)
        # --- Scene 5: Computing Gradients Layer by Layer (Backward Pass) ---
        # Set background
        self.camera.background_color = "#181825"

        # --- Title ---
        title = Text("Backward Pass", font_size=40, color="#CDD6F4")
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.5)

        # --- Three neurons in a row ---
        neuron_3 = Circle(radius=0.6, color="#FAB387", fill_opacity=0.3, stroke_width=3)
        neuron_3.move_to(RIGHT * 2.5)

        neuron_2 = Circle(radius=0.6, color="#A6E3A1", fill_opacity=0.3, stroke_width=3)
        neuron_2.move_to(ORIGIN)

        neuron_1 = Circle(radius=0.6, color="#89B4FA", fill_opacity=0.3, stroke_width=3)
        neuron_1.move_to(LEFT * 2.5)

        neurons = VGroup(neuron_1, neuron_2, neuron_3)
        self.play(Create(neurons), run_time=0.7)

        # --- Labels ---
        label_3 = Text("Layer 3", font_size=22, color="#A6ADC8")
        label_3.next_to(neuron_3, DOWN, buff=0.3)
        label_2 = Text("Layer 2", font_size=22, color="#A6ADC8")
        label_2.next_to(neuron_2, DOWN, buff=0.3)
        label_1 = Text("Layer 1", font_size=22, color="#A6ADC8")
        label_1.next_to(neuron_1, DOWN, buff=0.3)
        labels = VGroup(label_1, label_2, label_3)

        # --- Connections (arrows pointing right) ---
        arrow_12 = Arrow(
            start=neuron_1.get_right(),
            end=neuron_2.get_left(),
            color="#585B70",
            stroke_width=3,
            tip_length=0.2,
        )
        arrow_23 = Arrow(
            start=neuron_2.get_right(),
            end=neuron_3.get_left(),
            color="#585B70",
            stroke_width=3,
            tip_length=0.2,
        )
        connections = VGroup(arrow_12, arrow_23)

        self.play(Write(labels), Create(connections), run_time=0.8)
        self.wait(0.3)

        # --- Delta w formulas (appear from right to left) ---
        delta_w3 = MathTex(
            r"\Delta w_3 = -\alpha \cdot \frac{\partial L}{\partial w_3}",
            color="#F38BA8",
            font_size=28,
        )
        delta_w3.next_to(neuron_3, UP, buff=0.4)

        delta_w2 = MathTex(
            r"\Delta w_2 = -\alpha \cdot \frac{\partial L}{\partial w_2}",
            color="#F38BA8",
            font_size=28,
        )
        delta_w2.next_to(neuron_2, UP, buff=0.4)

        delta_w1 = MathTex(
            r"\Delta w_1 = -\alpha \cdot \frac{\partial L}{\partial w_1}",
            color="#F38BA8",
            font_size=28,
        )
        delta_w1.next_to(neuron_1, UP, buff=0.4)

        # --- Error arrows (pointing left) ---
        error_arrow_32 = Arrow(
            start=neuron_3.get_left(),
            end=neuron_2.get_right(),
            color="#F38BA8",
            stroke_width=4,
            tip_length=0.25,
        )
        error_arrow_21 = Arrow(
            start=neuron_2.get_left(),
            end=neuron_1.get_right(),
            color="#F38BA8",
            stroke_width=4,
            tip_length=0.25,
        )

        # --- Animate backward pass: Layer 3 glow + delta ---
        # Step 1: Highlight neuron_3
        glow_3 = neuron_3.copy()
        glow_3.set_stroke(color="#F38BA8", width=8)
        glow_3.set_opacity(0.0)
        self.play(glow_3.animate.set_opacity(0.6).set_stroke_width(8), run_time=0.5)

        # Step 2: Show error arrow from 3 to 2
        self.play(
            glow_3.animate.set_stroke(color="#F38BA8", width=8),
            Create(error_arrow_32),
            run_time=0.5,
        )

        # Step 3: Show delta_w3
        self.play(Write(delta_w3), run_time=0.5)

        # Step 4: Fade neuron_3 glow, highlight neuron_2
        glow_2 = neuron_2.copy()
        glow_2.set_stroke(color="#F38BA8", width=8)
        glow_2.set_opacity(0.0)
        self.play(
            glow_3.animate.set_opacity(0.0),
            glow_2.animate.set_opacity(0.6).set_stroke_width(8),
            run_time=0.5,
        )

        # Step 5: Show error arrow from 2 to 1
        self.play(
            glow_2.animate.set_stroke(color="#F38BA8", width=8),
            Create(error_arrow_21),
            run_time=0.5,
        )

        # Step 6: Show delta_w2
        self.play(Write(delta_w2), run_time=0.5)

        # Step 7: Fade neuron_2 glow, highlight neuron_1
        glow_1 = neuron_1.copy()
        glow_1.set_stroke(color="#F38BA8", width=8)
        glow_1.set_opacity(0.0)
        self.play(
            glow_2.animate.set_opacity(0.0),
            glow_1.animate.set_opacity(0.6).set_stroke_width(8),
            run_time=0.5,
        )

        # Step 8: Show delta_w1
        self.play(glow_1.animate.set_stroke(color="#F38BA8", width=8), run_time=0.5)

        # Step 9: Show delta_w1
        self.play(Write(delta_w1), run_time=0.5)

        # Step 10: Show final annotation
        error_label = Text("∂L/∂w", font_size=26, color="#A6ADC8")
        error_label.next_to(neuron_3, DOWN, buff=1.0)
        error_label.shift(LEFT * 0.5)

        caption = Text(
            "Gradient flows backward through the network", font_size=20, color="#585B70"
        )
        caption.to_edge(DOWN, buff=0.4)

        self.play(
            Write(error_label),
            Write(caption),
            glow_1.animate.set_opacity(0.0),
            run_time=0.5,
        )

        self.wait(0.7)
        # --- Scene 6: Gradient Descent Step: Updating the Weights ---
        self.clear()

        # Set background color
        self.camera.background_color = "#181825"

        # --- Colors from palette ---
        color_blue = "#89b4fa"
        color_peach = "#fab387"
        color_pink = "#f38ba8"
        color_green = "#a6e3a1"
        color_text = "#CDD6F4"
        color_trail = "#A6ADC8"

        # 1. Title
        title = Text(
            "Gradient Descent Step", font="Sans", font_size=36, color=color_text
        )
        title.to_edge(UP, buff=0.5)

        # 2. Axes (contour background)
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
            axis_config={
                "color": color_blue,
                "include_tip": False,
                "include_numbers": False,
                "stroke_width": 1.0,
            },
        )
        axes.move_to(ORIGIN)
        axes.x_axis.set_stroke(opacity=0.3)
        axes.y_axis.set_stroke(opacity=0.3)

        # 3. Concentric elliptical contours
        contour_1 = Ellipse(
            width=8, height=4.8, color=color_green, stroke_width=1.5, fill_opacity=0.0
        )
        contour_2 = Ellipse(
            width=5.5,
            height=3.3,
            color=color_green,
            stroke_width=1.5,
            fill_opacity=0.05,
        )
        contour_3 = Ellipse(
            width=3.0, height=1.8, color=color_green, stroke_width=1.5, fill_opacity=0.1
        )
        contour_4 = Ellipse(
            width=1.2,
            height=0.7,
            color=color_green,
            stroke_width=1.5,
            fill_opacity=0.15,
        )

        # 4. Marble (golden dot)
        marble_pos = UP * 1.5 + LEFT * 1.0
        marble = Dot(point=marble_pos, radius=0.18, color=color_peach, fill_opacity=1.0)
        marble_glow = Dot(
            point=marble_pos, radius=0.3, color=color_peach, fill_opacity=0.2
        )

        # 5. Trail dots (previous positions)
        trail_positions = [
            UP * 2.1 + LEFT * 1.5,
            UP * 1.9 + LEFT * 1.3,
            UP * 1.7 + LEFT * 1.1,
        ]
        trail_dots = VGroup(
            *[
                Dot(point=pos, radius=0.08, color=color_trail, fill_opacity=0.5)
                for pos in trail_positions
            ]
        )

        # 6. Step arrow
        arrow_start = marble.get_center()
        arrow_end = arrow_start + DOWN * 0.5 + RIGHT * 0.3
        step_arrow = Arrow(
            start=arrow_start,
            end=arrow_end,
            color=color_pink,
            stroke_width=3,
            tip_length=0.2,
        )

        # 7. Learning rate label
        lr_label = Text(
            "Learning Rate (\u03b1)", font="Sans", font_size=24, color=color_blue
        )
        lr_label.next_to(step_arrow, RIGHT, buff=0.5)
        lr_label.shift(UP * 0.3)

        # 8. Brace for step size
        lr_brace = BraceBetweenPoints(
            arrow_start, arrow_end, direction=DOWN, color=color_peach
        )
        lr_brace_text = lr_brace.get_tex(r"\alpha", buff=0.15)
        lr_brace_text.set_color(color_peach)
        lr_brace_text.font_size = 22

        # --- Build scene ---

        # Phase 1: Background (0.7s)
        self.play(
            FadeIn(axes, shift=DOWN * 0.2, scale=0.95), Write(title), run_time=0.7
        )

        # Phase 2: Contours (1.2s)
        self.play(
            Create(contour_1, run_time=0.3),
            Create(contour_2, run_time=0.3),
            Create(contour_3, run_time=0.3),
            Create(contour_4, run_time=0.3),
            run_time=1.2,
        )

        # Phase 3: Trail dots (0.5s)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in trail_dots], lag_ratio=0.15),
            run_time=0.5,
        )

        # Phase 4: Marble with glow (0.5s)
        self.play(GrowFromCenter(marble_glow), GrowFromCenter(marble), run_time=0.5)

        # Phase 5: Arrow (0.6s)
        self.play(Create(step_arrow, run_time=0.6))

        # Phase 6: Learning rate label and brace (0.6s)
        self.play(
            FadeIn(lr_label, shift=RIGHT * 0.3),
            GrowFromCenter(lr_brace),
            Write(lr_brace_text),
            run_time=0.6,
        )

        # Phase 7: Final emphasis (0.9s) -- using Indicate instead of Circumscribe
        self.play(Indicate(marble, color=color_peach, scale_factor=1.15, run_time=0.9))

        # Phase 8: Hold (2.0s)
        self.wait(2.0)
        # --- Scene 7: Iterative Refinement: Epochs of Training ---
        self.clear()

        # --- Colors based on style guidelines ---
        bg = "#181825"
        title_color = "#CDD6F4"
        c1 = "#89B4FA"  # Forward pass - blue
        c2 = "#A6E3A1"  # Compute loss - green
        c3 = "#F38BA8"  # Backward pass - pink
        c4 = "#FAB387"  # Update weights - orange
        text_color = "#A6ADC8"

        self.camera.background_color = bg

        # 1. Title
        title = Text("Iterative Training Loop", font_size=36, color=title_color)
        title.to_edge(UP).shift(DOWN * 0.3)

        # 2. Create the four boxes
        box_h = 1.2
        box_w = 2.5
        corner_r = 0.2

        # Forward Pass - top left
        box1 = RoundedRectangle(
            width=box_w,
            height=box_h,
            corner_radius=corner_r,
            fill_color=c1,
            fill_opacity=0.2,
            stroke_color=c1,
            stroke_width=2.5,
        )
        box1.move_to(LEFT * 2.5 + UP * 0.8)
        label1 = Text("Forward Pass", font_size=20, color=c1)
        label1.move_to(box1.get_center())

        # Compute Loss - bottom left
        box2 = RoundedRectangle(
            width=box_w,
            height=box_h,
            corner_radius=corner_r,
            fill_color=c2,
            fill_opacity=0.2,
            stroke_color=c2,
            stroke_width=2.5,
        )
        box2.move_to(LEFT * 2.5 + DOWN * 1.0)
        label2 = Text("Compute Loss", font_size=20, color=c2)
        label2.move_to(box2.get_center())

        # Backward Pass - bottom right
        box3 = RoundedRectangle(
            width=box_w,
            height=box_h,
            corner_radius=corner_r,
            fill_color=c3,
            fill_opacity=0.2,
            stroke_color=c3,
            stroke_width=2.5,
        )
        box3.move_to(RIGHT * 2.5 + DOWN * 1.0)
        label3 = Text("Backward Pass", font_size=20, color=c3)
        label3.move_to(box3.get_center())

        # Update Weights - top right
        box4 = RoundedRectangle(
            width=box_w,
            height=box_h,
            corner_radius=corner_r,
            fill_color=c4,
            fill_opacity=0.2,
            stroke_color=c4,
            stroke_width=2.5,
        )
        box4.move_to(RIGHT * 2.5 + UP * 0.8)
        label4 = Text("Update Weights", font_size=20, color=c4)
        label4.move_to(box4.get_center())

        # 3. Connecting arrows between boxes
        # Arrow 1: box1 -> box2 (top left to bottom left)
        a1_start = box1.get_bottom() + DOWN * 0.05
        a1_end = box2.get_top() + UP * 0.05
        arrow1 = Arrow(a1_start, a1_end, color=c4, stroke_width=3, tip_length=0.15)

        # Arrow 2: box2 -> box3 (bottom left to bottom right)
        a2_start = box2.get_right() + RIGHT * 0.05
        a2_end = box3.get_left() + LEFT * 0.05
        arrow2 = Arrow(a2_start, a2_end, color=c4, stroke_width=3, tip_length=0.15)

        # Arrow 3: box3 -> box4 (bottom right to top right)
        a3_start = box3.get_top() + UP * 0.05
        a3_end = box4.get_bottom() + DOWN * 0.05
        arrow3 = Arrow(a3_start, a3_end, color=c4, stroke_width=3, tip_length=0.15)

        # Arrow 4: box4 -> box1 (top right to top left)
        a4_start = box4.get_left() + LEFT * 0.05
        a4_end = box1.get_right() + RIGHT * 0.05
        arrow4 = Arrow(a4_start, a4_end, color=c4, stroke_width=3, tip_length=0.15)

        # 4. Epoch counter
        epoch_counter = Text("Epoch: 0 / 1000", font_size=28, color=text_color)
        epoch_counter.next_to(box2, DOWN * 2.2)

        # 5. Loss decay curve on the right
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 4, 1],
            x_length=3.5,
            y_length=2.0,
            axis_config={"color": "#6C7086", "stroke_width": 1.5},
        )
        axes.move_to(RIGHT * 4.0 + DOWN * 0.2)

        # Labels for axes
        x_label = Text("Epochs", font_size=14, color="#6C7086")
        x_label.next_to(axes.x_axis, DOWN, buff=0.15)
        y_label = Text("Loss", font_size=14, color="#6C7086")
        y_label.next_to(axes.y_axis, LEFT, buff=0.15)

        # Decaying loss curve (exponential-like)
        loss_curve = axes.plot(
            lambda x: 3.5 * np.exp(-0.6 * x) + 0.3,
            x_range=[0, 5],
            color=c2,
            stroke_width=2,
        )

        # Hiker dot - starts at high loss (epoch 0)
        hiker = Dot(color=c4, radius=0.15)
        initial_y = 3.5 * np.exp(0) + 0.3
        initial_point = axes.coords_to_point(0, initial_y)
        hiker.move_to(initial_point)

        # Loss value text near hiker
        loss_value = MathTex(f"L = {initial_y:.2f}", font_size=18, color=c4)
        loss_value.next_to(hiker, RIGHT * 0.5)

        # --- Animate entrance ---
        # Phase 1: Title
        self.play(Write(title, run_time=0.4))

        # Phase 2: Boxes and labels
        self.play(
            *[Create(box, run_time=0.3) for box in [box1, box2, box3, box4]],
            *[Write(lbl, run_time=0.2) for lbl in [label1, label2, label3, label4]],
            run_time=0.8,
        )

        # Phase 3: Connecting arrows
        self.play(
            Create(arrow1, run_time=0.25),
            Create(arrow2, run_time=0.25),
            Create(arrow3, run_time=0.25),
            Create(arrow4, run_time=0.25),
            run_time=0.6,
        )

        # Phase 4: Epoch counter
        self.play(Write(epoch_counter, run_time=0.3))

        # Phase 5: Axes
        self.play(
            Create(axes, run_time=0.4),
            Write(x_label, run_time=0.15),
            Write(y_label, run_time=0.15),
            run_time=0.5,
        )

        # Phase 6: Loss curve + hiker
        self.play(
            Create(loss_curve, run_time=0.6),
            FadeIn(hiker, run_time=0.2),
            Write(loss_value, run_time=0.2),
            run_time=0.6,
        )
        # Total so far: 0.4 + 0.8 + 0.6 + 0.3 + 0.5 + 0.6 = 3.2s

        # --- Main animation: Hiker moves down curve over epochs ---
        num_steps = 5
        for i in range(num_steps):
            t = i + 1
            x_pos = t
            y_pos = 3.5 * np.exp(-0.6 * t) + 0.3

            new_point = axes.coords_to_point(x_pos, y_pos)

            # Update loss value
            new_loss = MathTex(f"L = {y_pos:.2f}", font_size=18, color=c4)
            new_loss.next_to(new_point, RIGHT * 0.5)

            # Update epoch counter
            new_epoch = Text(f"Epoch: {t} / 1000", font_size=28, color=text_color)
            new_epoch.move_to(epoch_counter.get_center())

            # Move hiker and update labels
            self.play(
                hiker.animate.move_to(new_point),
                ReplacementTransform(loss_value, new_loss),
                ReplacementTransform(epoch_counter, new_epoch),
                run_time=0.35,
            )

            epoch_counter = new_epoch
            loss_value = new_loss

            # Flash arrows to show cycle (skip flash on last step)
            if i < num_steps - 1:
                self.play(
                    arrow1.animate.set_stroke(opacity=0.6),
                    arrow2.animate.set_stroke(opacity=0.6),
                    arrow3.animate.set_stroke(opacity=0.6),
                    arrow4.animate.set_stroke(opacity=0.6),
                    run_time=0.1,
                )
                self.play(
                    arrow1.animate.set_stroke(opacity=1.0),
                    arrow2.animate.set_stroke(opacity=1.0),
                    arrow3.animate.set_stroke(opacity=1.0),
                    arrow4.animate.set_stroke(opacity=1.0),
                    run_time=0.1,
                )
        # Loop time: 5 × 0.35 + 4 × 0.2 = 1.75 + 0.8 = 2.55s
        # Total so far: 3.2 + 2.55 = 5.75s

        # Final wait to reach exactly 6.5 seconds
        self.wait(0.75)
        # --- Scene 8: Vanishing & Exploding Gradients ---
        self.clear()
        self.camera.background_color = "#181825"

        # Colors from palette
        blue = "#89B4FA"
        peach = "#FAB387"
        red = "#F38BA8"
        text_color = "#CDD6F4"

        y_n = -0.5  # y-coordinate for neurons

        # ===== TITLE =====
        title = Text("Vanishing & Exploding Gradients", font_size=30, color=text_color)
        title.to_edge(UP, buff=0.4)

        # ===== VANISHING SIDE (Left) =====
        v_title = Text("Vanishing", font_size=26, color=red)
        v_title.move_to(LEFT * 3.5 + UP * 2.2)

        # Vanishing neurons (x = -3, -1.5, 0)
        v_n1 = Circle(radius=0.4, color=blue, fill_opacity=0.2, stroke_width=2)
        v_n1.move_to(LEFT * 3.0 + UP * y_n)
        v_n2 = Circle(radius=0.4, color=blue, fill_opacity=0.2, stroke_width=2)
        v_n2.move_to(LEFT * 1.5 + UP * y_n)
        v_n3 = Circle(radius=0.4, color=blue, fill_opacity=0.2, stroke_width=2)
        v_n3.move_to(ORIGIN + UP * y_n)

        # Neuron labels
        v_l1 = Text("L1", font_size=12, color=blue).next_to(v_n1, DOWN, buff=0.15)
        v_l2 = Text("L2", font_size=12, color=blue).next_to(v_n2, DOWN, buff=0.15)
        v_l3 = Text("L3", font_size=12, color=blue).next_to(v_n3, DOWN, buff=0.15)

        # Dashed connections
        v_c1 = DashedLine(
            v_n1.get_center(),
            v_n2.get_center(),
            color=blue,
            stroke_width=1,
            dash_length=0.08,
        )
        v_c2 = DashedLine(
            v_n2.get_center(),
            v_n3.get_center(),
            color=blue,
            stroke_width=1,
            dash_length=0.08,
        )

        # Vanishing arrows (error flows rightward: x=-3.75 -> x=-3 -> x=-1.5 -> x=0)
        # Arrow 3 - Strongest (rightmost, enters first), stroke=5
        vs3 = LEFT * 3.75 + UP * y_n
        ve3 = v_n1.get_center() + RIGHT * 0.15
        v_a3 = Arrow(start=vs3, end=ve3, color=red, stroke_width=5, tip_length=0.15)
        v_a3g = Arrow(
            start=vs3,
            end=ve3,
            color=red,
            stroke_width=14,
            tip_length=0.15,
            fill_opacity=0.15,
        )

        # Arrow 2 - Medium, stroke=2
        vs2 = LEFT * 2.25 + UP * y_n
        ve2 = v_n2.get_center() + RIGHT * 0.15
        v_a2 = Arrow(start=vs2, end=ve2, color=red, stroke_width=2, tip_length=0.12)
        v_a2g = Arrow(
            start=vs2,
            end=ve2,
            color=red,
            stroke_width=6,
            tip_length=0.12,
            fill_opacity=0.15,
        )

        # Arrow 1 - Weakest (leftmost), stroke=0.8
        vs1 = LEFT * 0.75 + UP * y_n
        ve1 = v_n3.get_center() + RIGHT * 0.15
        v_a1 = Arrow(start=vs1, end=ve1, color=red, stroke_width=0.8, tip_length=0.08)
        v_a1g = Arrow(
            start=vs1,
            end=ve1,
            color=red,
            stroke_width=3,
            tip_length=0.08,
            fill_opacity=0.15,
        )

        # Vanishing warning
        v_warn = Text("Vanishing!", font_size=20, color=peach)
        v_warn.move_to(LEFT * 3.5 + DOWN * 1.5)

        # ===== EXPLODING SIDE (Right) =====
        e_title = Text("Exploding", font_size=26, color=peach)
        e_title.move_to(RIGHT * 3.5 + UP * 2.2)

        # Exploding neurons (x = 1.5, 3.0, 4.5)
        e_n1 = Circle(radius=0.4, color=red, fill_opacity=0.2, stroke_width=2)
        e_n1.move_to(RIGHT * 1.5 + UP * y_n)
        e_n2 = Circle(radius=0.4, color=red, fill_opacity=0.2, stroke_width=2)
        e_n2.move_to(RIGHT * 3.0 + UP * y_n)
        e_n3 = Circle(radius=0.4, color=red, fill_opacity=0.2, stroke_width=2)
        e_n3.move_to(RIGHT * 4.5 + UP * y_n)

        # Neuron labels
        e_l1 = Text("L1", font_size=12, color=red).next_to(e_n1, DOWN, buff=0.15)
        e_l2 = Text("L2", font_size=12, color=red).next_to(e_n2, DOWN, buff=0.15)
        e_l3 = Text("L3", font_size=12, color=red).next_to(e_n3, DOWN, buff=0.15)

        # Dashed connections
        e_c1 = DashedLine(
            e_n1.get_center(),
            e_n2.get_center(),
            color=red,
            stroke_width=1,
            dash_length=0.08,
        )
        e_c2 = DashedLine(
            e_n2.get_center(),
            e_n3.get_center(),
            color=red,
            stroke_width=1,
            dash_length=0.08,
        )

        # Error arrows (flow leftward: x=5.25 -> x=4.5 -> x=3.0 -> x=1.5)
        # Arrow 3 - First encountered (rightmost), normal stroke=3
        es3 = RIGHT * 5.25 + UP * y_n
        ee3 = e_n3.get_center() + LEFT * 0.15
        e_a3 = Arrow(start=es3, end=ee3, color=red, stroke_width=3, tip_length=0.15)
        e_a3g = Arrow(
            start=es3,
            end=ee3,
            color=red,
            stroke_width=8,
            tip_length=0.15,
            fill_opacity=0.15,
        )

        # Arrow 2 - Growing, stroke=6
        es2 = RIGHT * 3.75 + UP * y_n
        ee2 = e_n2.get_center() + LEFT * 0.15
        e_a2 = Arrow(start=es2, end=ee2, color=red, stroke_width=6, tip_length=0.18)
        e_a2g = Arrow(
            start=es2,
            end=ee2,
            color=red,
            stroke_width=14,
            tip_length=0.18,
            fill_opacity=0.2,
        )

        # Arrow 1 - Hugest (leftmost), stroke=10
        es1 = RIGHT * 2.25 + UP * y_n
        ee1 = e_n1.get_center() + LEFT * 0.15
        e_a1 = Arrow(start=es1, end=ee1, color=red, stroke_width=10, tip_length=0.22)
        e_a1g = Arrow(
            start=es1,
            end=ee1,
            color=red,
            stroke_width=22,
            tip_length=0.22,
            fill_opacity=0.2,
        )

        # Exploding warning
        e_warn = Text("Exploding!", font_size=20, color=red)
        e_warn.move_to(RIGHT * 3.5 + DOWN * 1.5)

        # ===== CENTRAL ELEMENTS =====
        # Warning triangle
        warn_icon = Text("\u26a0", font_size=44, color=peach)
        warn_icon.move_to(UP * 1.5)

        # Divider line
        divider = DashedLine(
            UP * 2.5, DOWN * 2.5, color="#565F89", stroke_width=1, dash_length=0.06
        )

        # Flow direction labels
        v_flow_label = Text("Error \u2192", font_size=14, color="#565F89")
        v_flow_label.next_to(v_n1, UP, buff=0.3)
        e_flow_label = Text("Error \u2192", font_size=14, color="#565F89")
        e_flow_label.next_to(e_n3, UP, buff=0.3)

        # ===== ANIMATION (Total: 8.0s) =====
        elapsed = 0

        # Phase 1: Title (0.8s)
        self.play(Write(title), run_time=0.6)
        self.wait(0.2)
        elapsed += 0.8

        # Phase 2: Vanishing structure (1.0s)
        self.play(
            Write(v_title),
            Create(v_n1),
            Create(v_n2),
            Create(v_n3),
            Write(v_l1),
            Write(v_l2),
            Write(v_l3),
            Create(v_c1),
            Create(v_c2),
            Write(v_flow_label),
            run_time=0.8,
        )
        self.wait(0.2)
        elapsed += 1.0

        # Phase 3: Exploding structure (1.0s)
        self.play(
            Write(e_title),
            Create(e_n1),
            Create(e_n2),
            Create(e_n3),
            Write(e_l1),
            Write(e_l2),
            Write(e_l3),
            Create(e_c1),
            Create(e_c2),
            Write(e_flow_label),
            Create(divider),
            run_time=0.8,
        )
        self.wait(0.2)
        elapsed += 1.0

        # Phase 4: Vanishing arrows (1.0s)
        self.play(
            Create(v_a3g),
            Create(v_a3),
            Create(v_a2g),
            Create(v_a2),
            Create(v_a1g),
            Create(v_a1),
            run_time=0.8,
        )
        self.wait(0.2)
        elapsed += 1.0

        # Phase 5: Exploding arrows (1.0s)
        self.play(
            Create(e_a3g),
            Create(e_a3),
            Create(e_a2g),
            Create(e_a2),
            Create(e_a1g),
            Create(e_a1),
            run_time=0.8,
        )
        self.wait(0.2)
        elapsed += 1.0

        # Phase 6: Warning labels (1.0s)
        self.play(Write(v_warn), Write(e_warn), Write(warn_icon), run_time=0.8)
        self.wait(0.2)
        elapsed += 1.0

        # Phase 7: Emphasis - color change + thickness (1.0s)
        self.play(
            v_a3.animate.set_stroke_width(7).set_color(peach),
            v_a1.animate.set_stroke_width(2).set_color(peach),
            e_a3.animate.set_stroke_width(5).set_color(peach),
            e_a1.animate.set_stroke_width(14).set_color(peach),
            run_time=0.8,
        )
        self.wait(0.2)
        elapsed += 1.0

        # Phase 8: Warning pulse + hold (0.8s)
        self.play(warn_icon.animate.scale(1.4), run_time=0.3)
        self.play(warn_icon.animate.scale(1 / 1.4), run_time=0.3)
        self.wait(0.2)
        elapsed += 0.8

        # Final hold to match 8.0s exactly
        remaining = 8.0 - elapsed
        if remaining > 0:
            self.wait(remaining)
