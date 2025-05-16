import tkinter as tk
from tkinter import scrolledtext, END
from chatbot import chat_with_gemini

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot de Estudiantes")
        self.root.geometry("500x500")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', font=("Arial", 12))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(root, font=("Arial", 12))
        self.entry.pack(padx=10, pady=(0,10), fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(root, text="Enviar", command=self.send_message)
        self.send_button.pack(padx=10, pady=(0,10))

        self.add_message("Chatbot", "¡Bienvenido! Hazme una pregunta sobre los estudiantes. Escribe 'salir' para terminar.")

    def add_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(END, f"{sender}: {message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(END)

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        self.add_message("Tú", user_input)
        self.entry.delete(0, END)
        if user_input.lower() == 'salir':
            self.root.quit()
            return
        try:
            respuesta = chat_with_gemini(user_input)
        except Exception as e:
            respuesta = f"Error: {str(e)}"
        self.add_message("Chatbot", respuesta)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()
