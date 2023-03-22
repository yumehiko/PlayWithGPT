

import tkinter as tk

class gui(tk.Frame):
    def __init__(self, master=None, on_input=None):
        super().__init__(master)
        self.master = master
        self.master.title("PlayWithGPT")
        self.on_input = on_input
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # テキスト入力エリア
        self.input_label = tk.Label(self, text="入力")
        self.input_label.pack(side="top")
        self.input_text = tk.Text(self, width=50, height=10)
        self.input_text.pack(side="top")

        # テキスト表示エリア
        self.output_label = tk.Label(self, text="出力")
        self.output_label.pack(side="top")
        self.output_text = tk.Text(self, width=50, height=10)
        self.output_text.pack(side="top")

        # 入力確定ボタン
        self.submit_button = tk.Button(self, text="入力確定", command=self.submit_input)
        self.submit_button.pack(side="top")

    def submit_input(self):
        input_text = self.input_text.get("1.0", tk.END)
        output_text = self.on_input(input_text)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, output_text)