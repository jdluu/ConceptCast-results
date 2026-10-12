from manim import *
import numpy as np

# Global wave parameters
WAVE_SPEED = 2.2
WAVE_PERIOD = 0.9
WAVE_MAX_R = 6.5


def make_growing_wave(center, color=BLUE, speed=WAVE_SPEED, max_r=WAVE_MAX_R):
    """A circular wavefront that expands from `center` and fades away."""
    wave = Circle(radius=0.02, color=color, stroke_width=3)
    wave.move_to(center)
    state = {"r": 0.02}

    def upd(m, dt):
        state["r"] += speed * dt
        r = min(state["r"], max_r)
        op = max(0.0, 1.0 - state["r"] / max_r)
        m.become(Circle(radius=r, color=color, stroke_width=3, stroke_opacity=op))
        m.move_to(center)
        if state["r"] >= max_r:
            m.clear_updaters()
            m.set_stroke(opacity=0)

    wave.add_updater(upd)
    return wave


def make_emitter(holder, get_center, color=BLUE, period=WAVE_PERIOD,
                 speed=WAVE_SPEED, max_r=WAVE_MAX_R):
    """Attaches an updater to `holder` that spawns wavefronts periodically
    at the (possibly moving) position returned by `get_center`."""
    state = {"t": period}

    def upd(m, dt):
        state["t"] += dt
        while state["t"] >= period:
            state["t"] -= period
            holder.add(make_growing_wave(np.array(get_center()), color, speed, max_r))

    holder.add_updater(upd)
    return holder


class SceneGen(Scene):
    def construct(self):
        self.step1_stationary_source()
        self.clear()
        self.step2_wavelength_frequency()
        self.clear()
        self.step3_observer_toward()
        self.clear()
        self.step4_observer_away()
        self.clear()
        self.step5_moving_source()
        self.clear()
        self.step6_formula()
        self.clear()
        self.step7_passing_siren()
        self.clear()
        self.step8_light_and_beyond()

    # ------------------------------------------------------------------
    def fade_out_everything(self):
        for m in self.mobjects:
            m.clear_updaters(recursive=True)
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)

    # ------------------------------------------------------------------
    # Step 1: a stationary source emits circular wavefronts
    def step1_stationary_source(self):
        title = Text("The Doppler Effect", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.6)
        subtitle = Text(
            "the apparent shift in frequency for an observer moving relative to a source",
            font_size=22,
        ).next_to(title, DOWN, buff=0.3)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3))

        step = Text("Step 1: a stationary source emits circular wavefronts",
                    font_size=26, color=GREY_A).to_edge(DOWN, buff=0.4)

        source = Dot(LEFT * 3, color=RED, radius=0.16)
        src_label = Text("source at rest", font_size=24, color=RED)
        src_label.next_to(source, DOWN, buff=0.5)

        self.play(GrowFromCenter(source), FadeIn(src_label), FadeIn(step))

        holder = VGroup()
        make_emitter(holder, source.get_center)
        self.add(holder)
        self.wait(4)

        note = Text("wavefronts spread out evenly in all directions",
                    font_size=24, color=BLUE)
        note.next_to(step, UP, buff=0.3)
        self.play(Write(note))
        self.wait(2)
        self.fade_out_everything()

    # ------------------------------------------------------------------
    # Step 2: wavelength, frequency and wave speed
    def step2_wavelength_frequency(self):
        header = Text("Step 2: wavelength λ, frequency f, wave speed v",
                      font_size=30).to_edge(UP, buff=0.4)
        self.play(Write(header))

        source = Dot(LEFT * 3.5, color=RED, radius=0.16)
        src_label = Text("source", font_size=22, color=RED).next_to(source, DOWN, buff=0.35)
        self.play(GrowFromCenter(source), FadeIn(src_label))

        c1 = Circle(radius=1.0, color=BLUE, stroke_width=3).move_to(source.get_center())
        c2 = Circle(radius=2.2, color=BLUE, stroke_width=3).move_to(source.get_center())
        self.play(Create(c1), run_time=1.0)
        self.play(Create(c2), run_time=1.0)

        ang = np.pi / 4
        d = np.array([np.cos(ang), np.sin(ang), 0.0])
        p1 = source.get_center() + 1.0 * d
        p2 = source.get_center() + 2.2 * d
        lam_arrow = DoubleArrow(p1, p2, buff=0, color=BLUE,
                                 stroke_width=3, tip_length=0.18)
        lam_label = MathTex(r"\lambda", font_size=48, color=BLUE)
        lam_label.next_to(lam_arrow, RIGHT, buff=0.12)
        self.play(Create(lam_arrow), Write(lam_label), run_time=1.0)

        fdef = MathTex(r"f = \frac{1}{T}", font_size=40)
        fdef.move_to(np.array([3.2, 2.0, 0.0]))
        period_note = Text("one wavefront emitted every T seconds",
                           font_size=22, color=GREY_A)
        period_note.next_to(fdef, DOWN, buff=0.25)
        self.play(Write(fdef))
        self.play(FadeIn(period_note, shift=UP * 0.2))

        formula = MathTex(r"v = f\,\lambda", font_size=48)
        formula.next_to(period_note, DOWN, buff=0.5)
        box = SurroundingRectangle(formula, color=YELLOW, buff=0.15)
        self.play(Write(formula))
        self.play(Create(box))
        self.wait(1.5)
        self.play(Circumscribe(box, color=YELLOW), run_time=1.5)
        self.wait(1)
        self.fade_out_everything()

    # ------------------------------------------------------------------
    # Step 3: observer moving TOWARD the source -> higher frequency
    def step3_observer_toward(self):
        header = Text("Step 3: observer moves TOWARD the source",
                      font_size=30).to_edge(UP, buff=0.4)
        source = Dot(LEFT * 4, color=RED, radius=0.16)
        src_label = Text("source at rest", font_size=22, color=RED)
        src_label.next_to(source, DOWN, buff=0.35)
        observer = Dot(RIGHT * 2, color=GREEN, radius=0.16)
        obs_label = Text("observer", font_size=22, color=GREEN)
        obs_label.add_updater(lambda m: m.next_to(observer, UP, buff=0.3))

        self.play(Write(header))
        self.play(GrowFromCenter(source), FadeIn(src_label))
        self.play(GrowFromCenter(observer), FadeIn(obs_label))

        holder = VGroup()
        make_emitter(holder, source.get_center)
        self.add(holder)
        self.wait(3)

        at_rest = MathTex(r"f_{\mathrm{obs}} = f", font_size=36)
        at_rest.next_to(observer, DOWN, buff=0.6)
        self.play(Write(at_rest))
        self.wait(1.5)
        self.play(FadeOut(at_rest))

        arrow_start = observer.get_center() + DOWN * 2.2
        move_arrow = Arrow(arrow_start, arrow_start + LEFT * 2.5,
                           buff=0, color=GREEN, stroke_width=5)
        self.play(GrowArrow(move_arrow))
        self.play(
            observer.animate.move_to(LEFT * 1.5),
            run_time=4.5,
            rate_func=linear,
        )
        self.play(FadeOut(move_arrow))

        result = MathTex(r"f_{\mathrm{obs}} > f", font_size=42, color=BLUE)
        result.next_to(observer, DOWN, buff=0.6)
        why = Text("meets wavefronts more often → higher pitch",
                   font_size=24, color=BLUE)
        why.next_to(result, DOWN, buff=0.3)
        self.play(Write(result))
        self.play(FadeIn(why, shift=UP * 0.2))
        self.wait(2)
        self.fade_out_everything()

    # ------------------------------------------------------------------
    # Step 4: observer moving AWAY from the source -> lower frequency
    def step4_observer_away(self):
        header = Text("Step 4: observer moves AWAY from the source",
                      font_size=30).to_edge(UP, buff=0.4)
        source = Dot(LEFT * 4, color=RED, radius=0.16)
        src_label = Text("source at rest", font_size=22, color=RED)
        src_label.next_to(source, DOWN, buff=0.35)
        observer = Dot(LEFT * 0.5, color=GREEN, radius=0.16)
        obs_label = Text("observer", font_size=22, color=GREEN)
        obs_label.add_updater(lambda m: m.next_to(observer, UP, buff=0.3))

        self.play(Write(header))
        self.play(GrowFromCenter(source), FadeIn(src_label))
        self.play(GrowFromCenter(observer), FadeIn(obs_label))

        holder = VGroup()
        make_emitter(holder, source.get_center, max_r=8.5)
        self.add(holder)
        self.wait(2)

        at_rest = MathTex(r"f_{\mathrm{obs}} = f", font_size=36)
        at_rest.next_to(observer, DOWN, buff=0.6)
        self.play(Write(at_rest))
        self.wait(1)
        self.play(FadeOut(at_rest))

        arrow_start = observer.get_center() + DOWN * 2.2
        move_arrow = Arrow(arrow_start, arrow_start + RIGHT * 3.0,
                           buff=0, color=GREEN, stroke_width=5)
        self.play(GrowArrow(move_arrow))
        self.play(
            observer.animate.move_to(RIGHT * 3),
            run_time=4.5,
            rate_func=linear,
        )
        self.play(FadeOut(move_arrow))

        result = MathTex(r"f_{\mathrm{obs}} < f", font_size=42, color=RED)
        result.next_to(observer, DOWN, buff=0.6)
        why = Text("wavefronts overtake the observer less often → lower pitch",
                   font_size=24, color=RED)
        why.next_to(result, DOWN, buff=0.3)
        self.play(Write(result))
        self.play(FadeIn(why, shift=UP * 0.2))
        self.wait(2)
        self.fade_out_everything()

    # ------------------------------------------------------------------
    # Step 5: a moving source bunches wavefronts ahead, spreads them behind
    def step5_moving_source(self):
        header = Text("Step 5: a MOVING source bunches the wavefronts",
                      font_size=30).to_edge(UP, buff=0.4)
        self.play(Write(header))

        source = Dot(LEFT * 4 + DOWN * 0.5, color=RED, radius=0.16)
        src_label = Text("moving source", font_size=22, color=RED)
        src_label.add_updater(lambda m: m.next_to(source, DOWN, buff=0.35))
        self.play(GrowFromCenter(source), FadeIn(src_label))

        holder = VGroup()
        make_emitter(holder, source.get_center)
        self.add(holder)
        self.wait(1.5)

        arrow = Arrow(source.get_center() + UP * 1.6,
                      source.get_center() + UP * 1.6 + RIGHT * 2.5,
                      buff=0, color=ORANGE, stroke_width=5)
        self.play(GrowArrow(arrow))
        self.play(
            source.animate.move_to(RIGHT * 3 + DOWN * 0.5),
            run_time=6,
            rate_func=linear,
        )
        self.play(FadeOut(arrow))

        ahead = Text("ahead: wavefronts closer together → higher f",
                     font_size=24, color=BLUE).to_corner(UR, buff=0.5)
        behind = Text("behind: wavefronts spread apart → lower f",
                      font_size=24, color=RED).to_corner(UL, buff=0.5)
        self.play(Write(ahead))
        self.play(Write(behind))
        self.wait(2.5)
        self.fade_out_everything()

    # ------------------------------------------------------------------
    # Step 6: the Doppler formula
    def step6_formula(self):
        header = Text("Step 6: putting it together — the Doppler formula",
                      font_size=30).to_edge(UP, buff=0.4)
        self.play(Write(header))

        formula = MathTex(
            r"{f_{\mathrm{obs}}}", "=", r"{f}\,",
            r"\frac{v \pm v_{\mathrm{obs}}}{v \mp v_{\mathrm{src}}}",
            font_size=54,
        )
        formula.shift(UP * 1.2)
        self.play(Write(formula), run_time=2)
        self.play(
            formula[0].animate.set_color(GREEN),
            formula[2].animate.set_color(RED),
            formula[3].animate.set_color(TEAL),
            run_time=1,
        )

        box = SurroundingRectangle(formula, color=YELLOW, buff=0.25)
        self.play(Create(box))

        case1 = MathTex(
            r"\text{observer toward source: } "
            r"f_{\mathrm{obs}} = f\,\frac{v + v_{\mathrm{obs}}}{v}",
            font_size=38,
        )
        case2 = MathTex(
            r"\text{source toward observer: } "
            r"f_{\mathrm{obs}} = f\,\frac{v}{v - v_{\mathrm{src}}}",
            font_size=38,
        )
        cases = VGroup(case1, case2).arrange(DOWN, buff=0.5)
        cases.next_to(box, DOWN, buff=0.7)
        self.play(Write(case1), run_time=1.5)
        self.play(Write(case2), run_time=1.5)
        self.play(
            Circumscribe(case1, color=BLUE),
            Circumscribe(case2, color=RED),
            run_time=2,
        )

        note = Text("approaching → higher frequency, receding → lower frequency",
                    font_size=24, color=GREY_A)
        note.next_to(cases, DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(2)
        self.fade_out_everything()

    # ------------------------------------------------------------------
    # Step 7: the classic passing-siren example
    def step7_passing_siren(self):
        header = Text("Step 7: the classic example — a passing siren",
                      font_size=30).to_edge(UP, buff=0.4)
        self.play(Write(header))

        observer = Dot(DOWN * 1.5, color=GREEN, radius=0.16)
        obs_label = Text("listener", font_size=22, color=GREEN)
        obs_label.next_to(observer, DOWN, buff=0.35)
        siren = Dot(LEFT * 5 + UP * 0.8, color=RED, radius=0.16)
        siren_label = Text("siren", font_size=22, color=RED)
        siren_label.add_updater(lambda m: m.next_to(siren, UP, buff=0.3))

        approach = Text("approaching:\nhigher pitch", font_size=24,
                        color=BLUE, line_spacing=0.8)
        approach.to_corner(UL, buff=0.6).shift(DOWN * 0.5)
        recede = Text("receding:\nlower pitch", font_size=24,
                      color=RED, line_spacing=0.8)
        recede.to_corner(UR, buff=0.6).shift(DOWN * 0.5)

        self.play(GrowFromCenter(observer), FadeIn(obs_label))
        self.play(GrowFromCenter(siren), FadeIn(siren_label))
        self.play(FadeIn(approach, shift=RIGHT * 0.5),
                  FadeIn(recede, shift=LEFT * 0.5))

        holder = VGroup()
        make_emitter(holder, siren.get_center, max_r=8.0)
        self.add(holder)
        self.wait(1.5)
        self.play(
            siren.animate.move_to(RIGHT * 5 + UP * 0.8),
            run_time=7,
            rate_func=linear,
        )
        self.wait(2)

        drop = Text("the pitch you hear drops as it passes",
                    font_size=24, color=YELLOW)
        drop.next_to(obs_label, DOWN, buff=0.4)
        self.play(Write(drop))
        self.wait(2)
        self.fade_out_everything()

    # ------------------------------------------------------------------
    # Step 8: light waves — blueshift and redshift
    def step8_light_and_beyond(self):
        header = Text("Step 8: the same idea for light — redshift and blueshift",
                      font_size=30).to_edge(UP, buff=0.4)
        self.play(Write(header))

        star = Dot(LEFT * 3.5, color=YELLOW, radius=0.18)
        star_label = Text("star / galaxy", font_size=22, color=YELLOW)
        star_label.add_updater(lambda m: m.next_to(star, DOWN, buff=0.35))
        self.play(GrowFromCenter(star), FadeIn(star_label))

        holder = VGroup()
        make_emitter(holder, star.get_center, color=PURPLE)
        self.add(holder)
        self.wait(1.5)
        self.play(
            star.animate.move_to(RIGHT * 1.5),
            run_time=5,
            rate_func=linear,
        )
        self.wait(1)

        blue_side = Text("ahead: blueshift (shorter λ, higher f)",
                         font_size=24, color=BLUE).to_corner(UR, buff=0.5)
        red_side = Text("behind: redshift (longer λ, lower f)",
                        font_size=24, color=RED).to_corner(UL, buff=0.5)
        self.play(Write(blue_side))
        self.play(Write(red_side))
        self.wait(2)

        closing1 = Text("Doppler effect:", font_size=30, color=WHITE)
        closing2 = Text("relative motion shifts the observed frequency of any wave",
                        font_size=26, color=WHITE)
        closing = VGroup(closing1, closing2).arrange(DOWN, buff=0.25)
        closing.to_edge(DOWN, buff=0.6)
        self.play(Write(closing1))
        self.play(FadeIn(closing2, shift=UP * 0.2))
        self.wait(2.5)
        self.fade_out_everything()
