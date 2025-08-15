import tkinter as tk
from tkinter import ttk

class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern Calculator")
        self.geometry("400x500")
        self.configure(bg="#2E2E2E")

        # To store the expression
        self.expression_var = tk.StringVar()
        self.is_result = False

        self.s = ttk.Style(self)
        self._create_display()
        self._create_buttons()

    def _create_button_styles(self):
        self.s.configure('TButton', font=('Arial', 18), padding=10, borderwidth=0)
        self.s.map('TButton', background=[('active', '#6A6A6A')])

        self.s.configure('Num.TButton', background='#505050', foreground='#FFFFFF')
        self.s.configure('Op.TButton', background='#FF9500', foreground='#FFFFFF')
        self.s.map('Op.TButton', background=[('active', '#BFA100')])
        self.s.configure('Misc.TButton', background='#D3D3D3', foreground='#000000')
        self.s.map('Misc.TButton', background=[('active', '#C0C0C0')])

    def _create_buttons(self):
        self._create_button_styles()
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1)

        buttons = {
            'C': (0, 0, 'Misc.TButton'), '/': (0, 3, 'Op.TButton'),
            '7': (1, 0, 'Num.TButton'), '8': (1, 1, 'Num.TButton'), '9': (1, 2, 'Num.TButton'), '*': (1, 3, 'Op.TButton'),
            '4': (2, 0, 'Num.TButton'), '5': (2, 1, 'Num.TButton'), '6': (2, 2, 'Num.TButton'), '-': (2, 3, 'Op.TButton'),
            '1': (3, 0, 'Num.TButton'), '2': (3, 1, 'Num.TButton'), '3': (3, 2, 'Num.TButton'), '+': (3, 3, 'Op.TButton'),
            '0': (4, 0, 'Num.TButton'), '.': (4, 2, 'Num.TButton'), '=': (4, 3, 'Op.TButton'),
        }

        for text, (row, col, style) in buttons.items():
            command = lambda t=text: self._on_button_press(t)
            if text == 'C':
                command = self._clear
            elif text == '=':
                command = self._calculate

            button = ttk.Button(buttons_frame, text=text, style=style, command=command)

            columnspan = 1
            if text == 'C':
                columnspan = 3
            elif text == '0':
                columnspan = 2

            button.grid(row=row, column=col, columnspan=columnspan, sticky="nsew", padx=2, pady=2)


    def _on_button_press(self, char):
        current_text = self.expression_var.get()

        if self.is_result:
            if char in '0123456789.':
                current_text = ''
            self.is_result = False

        if current_text == "Error":
             current_text = ""

        self.expression_var.set(current_text + str(char))

    def _clear(self):
        self.expression_var.set("")
        self.is_result = False

    def _calculate(self):
        current_expression = self.expression_var.get()
        try:
            if not current_expression:
                return

            # Basic security: only allow expected characters.
            allowed_chars = "0123456789./*-+"
            if not all(char in allowed_chars for char in current_expression):
                raise ValueError("Invalid character")

            result = eval(current_expression)

            if result == int(result):
                result = int(result)

            self.expression_var.set(str(result))
            self.is_result = True
        except ZeroDivisionError:
            self.expression_var.set("Error")
            self.is_result = True
        except Exception:
            self.expression_var.set("Error")
            self.is_result = True

    def _create_display(self):
        # Style for the display
        self.s.configure("Display.TEntry",
                    foreground="#FFFFFF",
                    fieldbackground="#3B3B3B",
                    borderwidth=0,
                    font=('Arial', 30, 'bold'))

        # The display screen
        display_frame = ttk.Frame(self)
        display_frame.pack(fill="x", padx=10, pady=(20, 10))

        display = ttk.Entry(display_frame,
                            textvariable=self.expression_var,
                            justify='right',
                            style="Display.TEntry",
                            state='readonly')
        display.pack(fill="both", expand=True, ipady=20)


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
