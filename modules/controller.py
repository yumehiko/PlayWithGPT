

import tkinter as tk

from modules import gptContact
from modules import chatLogger
from modules import aiCommand
from modules import logReader
from modules import findModule
from modules import gui

class Controller:
    def __init__(self):
        self.view = gui.gui(on_input=self.process_input)
        self.view.mainloop()

    def process_input(self, input_text):
        input_text = input_text.strip()
        if input_text == "":
            return ""

        if input_text.lower() in ["clear", "c"]:
            gptContact.clearContext()
            commandText = "=== 文脈をクリアします。AIは記憶を失いますが、会話は続行できます ==="
            chatLogger.log("command", commandText)
            self.view.output_text.delete("1.0", tk.END)
            self.view.output_text.insert(tk.END, commandText)
            return ""

        if input_text.lower() in ["log", "l"]:
            commandText = "=== 最新のログを表示します ==="
            self.view.output_text.delete("1.0", tk.END)
            self.view.output_text.insert(tk.END, commandText)
            log = logReader.ReadLatestJson()
            self.view.output_text.insert(tk.END, log)
            commandText = "=== 以上が最新のログです ==="
            self.view.output_text.insert(tk.END, commandText)
            commandText = "=== 最新のログを表示しました（記録上は省略） ==="
            chatLogger.log("command", commandText)
            return ""

        if input_text.startswith("read: "):
            input_text = input_text[6:]
            file_name = input_text.split(".py")[0] + ".py"
            source_code = findModule.findSourceCode(file_name)
            commandText = file_name + "について話します。内容は、次の通りです：\n" + source_code
            gptContact.sendUserMessage(commandText)
            self.view.output_text.delete("1.0", tk.END)
            self.view.output_text.insert(tk.END, commandText)
            chatLogger.log("command", commandText)
            return ""

        if input_text.lower() in ["end", "e"]:
            commandText = "=== ログを記録しました。セッションを終了します ==="
            chatLogger.log("command", commandText)
            chatLogger.saveJson()
            self.view.output_text.delete("1.0", tk.END)
            self.view.output_text.insert(tk.END, commandText)
            return ""
        
        return input_text