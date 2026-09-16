from manim import *

class NeuralNetworkExplanation(Scene):
    def construct(self):
        # Scene 1: Introduction
        title = Text("What is a Neural Network?", font_size=48)
        subtitle = Text("A visual explanation", font_size=32).next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Scene 2: Biological neuron
        neuron_title = Text("Biological Neuron", font_size=36).to_edge(UP)
        
        # Create neuron diagram
        cell_body = Circle(radius=0.8, color=BLUE, fill_opacity=0.3)
        nucleus = Circle(radius=0.3, color=PURPLE, fill_opacity=0.5).move_to(cell_body)
        dendrites = VGroup(*[
            Line(cell_body.get_left() + UP*i*0.3, 
                 cell_body.get_left() + LEFT*2 + UP*i*0.3, 
                 color=GREEN)
            for i in range(-2, 3)
        ])
        axon = Line(cell_body.get_right(), cell_body.get_right() + RIGHT*3, 
                   color=YELLOW, stroke_width=4)
        axon_terminal = Circle(radius=0.15, color=RED).move_to(axon.get_end())
        
        neuron_diagram = VGroup(cell_body, nucleus, dendrites, axon, axon_terminal)
        
        self.play(Write(neuron_title))
        self.play(Create(neuron_diagram))
        self.wait(2)
        
        # Scene 3: Artificial neuron
        self.play(FadeOut(neuron_title), FadeOut(neuron_diagram))
        
        artificial_title = Text("Artificial Neuron", font_size=36).to_edge(UP)
        
        # Create artificial neuron
        inputs = VGroup(*[
            Text(f"x{i+1}", font_size=24).move_to(LEFT*3 + UP*(1-i))
            for i in range(3)
        ])
        weights = VGroup(*[
            Text(f"w{i+1}", font_size=20, color=YELLOW).move_to(LEFT*1.5 + UP*(1-i))
            for i in range(3)
        ])
        summation = Circle(radius=0.6, color=BLUE, fill_opacity=0.3).move_to(ORIGIN)
        sigma = Text("Σ", font_size=36).move_to(summation)
        activation = Text("σ", font_size=36, color=RED).move_to(RIGHT*1.5)
        output = Text("y", font_size=24).move_to(RIGHT*3)
        
        connections = VGroup(*[
            Arrow(inputs[i].get_right(), summation.get_left() + UP*(1-i)*0.2, 
                  buff=0.1, color=GRAY)
            for i in range(3)
        ])
        connection_to_activation = Arrow(summation.get_right(), activation.get_left(), 
                                        buff=0.1, color=GRAY)
        connection_to_output = Arrow(activation.get_right(), output.get_left(), 
                                    buff=0.1, color=GRAY)
        
        artificial_neuron = VGroup(
            inputs, weights, summation, sigma, activation, output,
            connections, connection_to_activation, connection_to_output
        )
        
        self.play(Write(artificial_title))
        self.play(Create(artificial_neuron))
        self.wait(3)
        
        # Scene 4: Network layers
        self.play(FadeOut(artificial_title), FadeOut(artificial_neuron))
        
        layers_title = Text("Layers of a Neural Network", font_size=36).to_edge(UP)
        
        # Create network layers
        layer_names = ["Input", "Hidden", "Output"]
        layer_colors = [GREEN, BLUE, RED]
        
        layers = VGroup()
        for i, (name, color) in enumerate(zip(layer_names, layer_colors)):
            layer = VGroup()
            for j in range(3 - i):
                circle = Circle(radius=0.3, color=color, fill_opacity=0.3)
                circle.move_to(RIGHT*(i*3 - 3) + UP*(j - 1))
                label = Text(name[0], font_size=20).move_to(circle)
                layer.add(VGroup(circle, label))
            layers.add(layer)
        
        # Add connections between layers
        connections = VGroup()
        for i in range(2):
            for j in range(len(layers[i])):
                for k in range(len(layers[i+1])):
                    arrow = Arrow(
                        layers[i][j].get_right(),
                        layers[i+1][k].get_left(),
                        buff=0.1,
                        color=GRAY,
                        stroke_width=1.5
                    )
                    connections.add(arrow)
        
        self.play(Write(layers_title))
        self.play(Create(layers))
        self.play(Create(connections))
        self.wait(3)
        
        # Scene 5: Simple network example
        self.play(FadeOut(layers_title), FadeOut(layers), FadeOut(connections))
        
        example_title = Text("Simple Network Example", font_size=36).to_edge(UP)
        
        # Simple 3-neuron network
        positions = [LEFT*4, ORIGIN, RIGHT*4]
        neurons_simple = VGroup()
        
        for i, pos in enumerate(positions):
            circle = Circle(radius=0.4, color=[BLUE, PURPLE, GREEN][i])
            circle.move_to(pos)
            label = Text(f"a{i+1}", font_size=24).move_to(circle)
            neurons_simple.add(VGroup(circle, label))
        
        connections_simple = VGroup(
            Arrow(neurons_simple[0].get_center(), neurons_simple[1].get_center(), buff=0.4),
            Arrow(neurons_simple[1].get_center(), neurons_simple[2].get_center(), buff=0.4)
        )
        
        self.play(Write(example_title))
        self.play(Create(neurons_simple))
        self.play(Create(connections_simple))
        self.wait(3)
        
        # Scene 6: Learning process
        self.play(FadeOut(example_title), FadeOut(neurons_simple), FadeOut(connections_simple))
        
        learning_title = Text("How Neural Networks Learn", font_size=36).to_edge(UP)
        
        # Create learning diagram
        input_layer = VGroup(*[
            Circle(radius=0.3, color=GREEN, fill_opacity=0.3).move_to(LEFT*3 + UP*(1-i))
            for i in range(3)
        ])
        output_layer = VGroup(*[
            Circle(radius=0.3, color=RED, fill_opacity=0.3).move_to(RIGHT*3 + UP*(1-i))
            for i in range(3)
        ])
        
        # Forward pass
        forward_arrows = VGroup(*[
            Arrow(input_layer[i].get_right(), output_layer[j].get_left(),
                  buff=0.3, color=BLUE, stroke_width=2)
            for i in range(3) for j in range(3)
        ])
        
        # Loss calculation
        loss_text = Text("Loss = (predicted - actual)²", font_size=24, color=YELLOW)
        loss_text.move_to(DOWN*2)
        
        # Backward pass
        backward_arrows = VGroup(*[
            Arrow(output_layer[j].get_left(), input_layer[i].get_right(),
                  buff=0.3, color=RED, stroke_width=2)
            for i in range(3) for j in range(3)
        ])
        
        self.play(Write(learning_title))
        self.play(Create(input_layer), Create(output_layer))
        self.play(Create(forward_arrows))
        self.play(Write(loss_text))
        self.wait(2)
        self.play(Create(backward_arrows))
        self.wait(3)
        
        # Scene 7: Conclusion
        self.play(
            FadeOut(learning_title), FadeOut(input_layer), FadeOut(output_layer),
            FadeOut(forward_arrows), FadeOut(loss_text), FadeOut(backward_arrows)
        )
        
        conclusion_title = Text("Conclusion", font_size=48)
        conclusion_points = VGroup(
            Text("• Neural networks mimic brain structure", font_size=28),
            Text("• They learn by adjusting weights", font_size=28),
            Text("• Used for pattern recognition", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(conclusion_title, DOWN, buff=0.5)
        
        self.play(Write(conclusion_title))
        self.play(Write(conclusion_points))
        self.wait(3)
        
        # Final fade out
        self.play(FadeOut(conclusion_title), FadeOut(conclusion_points))
        self.wait(1)
