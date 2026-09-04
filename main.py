import math

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class SurveyCalculator(App):
    def build(self):
        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8),
        )

        root.add_widget(
            Label(
                text="Survey Calculator",
                font_size=dp(22),
                bold=True,
                size_hint_y=None,
                height=dp(45),
            )
        )

        scroll = ScrollView()
        self.form = GridLayout(
            cols=2,
            spacing=dp(7),
            size_hint_y=None,
        )
        self.form.bind(minimum_height=self.form.setter("height"))
        scroll.add_widget(self.form)
        root.add_widget(scroll)

        self.l_input = self.add_input("Tape length L")
        self.n_input = self.add_input("Number of turns n")
        self.first_input = self.add_input("Distance A to P1")

        self.dynamic_box = GridLayout(
            cols=2,
            spacing=dp(7),
            size_hint_y=None,
        )
        self.dynamic_box.bind(
            minimum_height=self.dynamic_box.setter("height")
        )
        self.form.add_widget(
            Label(
                text="Turn details",
                size_hint_y=None,
                height=dp(40),
            )
        )
        self.form.add_widget(
            Label(
                text="",
                size_hint_y=None,
                height=dp(40),
            )
        )
        self.form.add_widget(self.dynamic_box)
        self.form.add_widget(Label(text=""))

        root.add_widget(
            Button(
                text="Create turn inputs",
                size_hint_y=None,
                height=dp(48),
                on_press=self.create_turn_inputs,
            )
        )

        self.calculate_button = Button(
            text="Calculate",
            size_hint_y=None,
            height=dp(52),
            disabled=True,
        )
        self.calculate_button.bind(on_press=self.calculate)
        root.add_widget(self.calculate_button)

        self.result = Label(
            text="Enter values and press Calculate",
            size_hint_y=None,
            height=dp(90),
        )
        root.add_widget(self.result)

        return root

    def add_input(self, label_text):
        self.form.add_widget(
            Label(
                text=label_text,
                size_hint_y=None,
                height=dp(42),
            )
        )
        field = TextInput(
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(42),
        )
        self.form.add_widget(field)
        return field

    def create_turn_inputs(self, instance):
        self.dynamic_box.clear_widgets()
        self.cross_inputs = []
        self.direction_inputs = []
        self.distance_inputs = []

        try:
            n = int(self.n_input.text)
            if n < 1 or n > 100:
                raise ValueError
        except ValueError:
            self.result.text = "Enter n as a whole number from 1 to 100."
            self.calculate_button.disabled = True
            return

        for i in range(1, n + 1):
            self.dynamic_box.add_widget(
                Label(
                    text=f"Cross distance C{i}",
                    size_hint_y=None,
                    height=dp(42),
                )
            )
            cross = TextInput(
                multiline=False,
                input_filter="float",
                size_hint_y=None,
                height=dp(42),
            )
            self.dynamic_box.add_widget(cross)
            self.cross_inputs.append(cross)

            self.dynamic_box.add_widget(
                Label(
                    text=f"Direction P{i}: R or L",
                    size_hint_y=None,
                    height=dp(42),
                )
            )
            direction = TextInput(
                multiline=False,
                hint_text="R or L",
                size_hint_y=None,
                height=dp(42),
            )
            self.dynamic_box.add_widget(direction)
            self.direction_inputs.append(direction)

            next_point = "B" if i == n else f"P{i + 1}"

            self.dynamic_box.add_widget(
                Label(
                    text=f"Distance P{i} to {next_point}",
                    size_hint_y=None,
                    height=dp(42),
                )
            )
            distance = TextInput(
                multiline=False,
                input_filter="float",
                size_hint_y=None,
                height=dp(42),
            )
            self.dynamic_box.add_widget(distance)
            self.distance_inputs.append(distance)

        self.calculate_button.disabled = False
        self.result.text = "Fill in all turn information."

    def calculate(self, instance):
        try:
            tape_length = float(self.l_input.text)
            turn_count = int(self.n_input.text)
            first_distance = float(self.first_input.text)

            if tape_length <= 0 or first_distance < 0:
                raise ValueError

            total_x = first_distance
            total_y = 0.0
            bearing = 0.0

            for i in range(turn_count):
                cross_distance = float(self.cross_inputs[i].text)
                direction = self.direction_inputs[i].text.strip().upper()
                next_distance = float(self.distance_inputs[i].text)

                if cross_distance <= 0 or cross_distance > 2 * tape_length:
                    self.result.text = (
                        f"C{i + 1} must be greater than 0 and at most 2L."
                    )
                    return

                if direction not in ("R", "L"):
                    self.result.text = f"Direction P{i + 1} must be R or L."
                    return

                if next_distance < 0:
                    raise ValueError

                cosine_value = (
                    (2 * tape_length * tape_length - cross_distance ** 2)
                    / (2 * tape_length * tape_length)
                )
                cosine_value = max(-1.0, min(1.0, cosine_value))

                angle = math.acos(cosine_value)
                turn_angle = math.pi - angle

                if direction == "R":
                    bearing -= turn_angle
                else:
                    bearing += turn_angle

                total_x += next_distance * math.cos(bearing)
                total_y += next_distance * math.sin(bearing)

            final_distance = math.hypot(total_x, total_y)

            self.result.text = (
                f"Calculation complete\n"
                f"X = {total_x:.3f}\n"
                f"Y = {total_y:.3f}\n"
                f"Straight distance AB = {final_distance:.3f}"
            )

        except ValueError:
            self.result.text = "Enter valid numeric values in every field."


if __name__ == "__main__":
    SurveyCalculator().run()
