import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import Config

# Set the default size of the window for testing on PC (Phone-like shape)
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

class CalculatorApp(App):
    def build(self):
        # Main layout: Vertical Box (Screen on top, Buttons below)
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None

        main_layout = BoxLayout(orientation="vertical")

        # The Display Screen (TextInput)
        self.solution = TextInput(
            multiline=False,
            readonly=True,
            halign="right",
            font_size=55,
            background_color=(0, 0, 0, 1), # Black background
            foreground_color=(1, 1, 1, 1)  # White text
        )
        main_layout.add_widget(self.solution)

        # The Buttons (GridLayout)
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]

        grid_layout = GridLayout(cols=4, spacing=2, padding=2)

        for row in buttons:
            for label in row:
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    font_size=30,
                    background_color=(0.2, 0.2, 0.2, 1) # Dark grey buttons
                )
                button.bind(on_press=self.on_button_press)
                grid_layout.add_widget(button)

        # Add an "Equals" button at the bottom
        equals_button = Button(
            text="=",
            font_size=30,
            size_hint=(1, 0.2), # Take up 20% of the height
            background_color=(0.18, 0.5, 0.9, 1) # Blue color
        )
        equals_button.bind(on_press=self.on_solution)
        
        main_layout.add_widget(grid_layout)
        main_layout.add_widget(equals_button)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            # Clear the screen
            self.solution.text = ""
        else:
            if current and (self.last_was_operator and button_text in self.operators):
                # Don't allow two operators in a row
                return
            elif current == "" and button_text in self.operators:
                # First character cannot be an operator
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text

        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            try:
                # 'eval' does the math magic automatically
                solution = str(eval(self.solution.text)) 
                self.solution.text = solution
            except Exception:
                self.solution.text = "Error"

if __name__ == "__main__":
    CalculatorApp().run()