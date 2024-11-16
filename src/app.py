import tkinter as tk
from tkinter import messagebox, scrolledtext
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading


class ChatApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Chat")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.create_ui()

        # Variáveis do tray icon
        self.icon = None
        self.create_tray_icon()

    def create_ui(self):
        # Área de chat
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Arial", 12))
        self.chat_area.config(state=tk.DISABLED)  # Apenas leitura
        self.chat_area.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        # Área de entrada
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.input_area = tk.Text(bottom_frame, wrap=tk.WORD, height=3, font=("Arial", 12))
        self.input_area.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Botões de ação
        button_frame = tk.Frame(bottom_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)

        send_button = tk.Button(button_frame, text="Send", command=self.send_message)
        send_button.grid(row=0, column=0, padx=5)

        mic_button = tk.Button(button_frame, text="Mic", command=lambda: print("Mic clicked"))
        mic_button.grid(row=0, column=1, padx=5)

        trash_button = tk.Button(button_frame, text="Trash", command=lambda: print("Trash clicked"))
        trash_button.grid(row=0, column=2, padx=5)

        settings_button = tk.Button(button_frame, text="Settings", command=lambda: print("Settings clicked"))
        settings_button.grid(row=0, column=3, padx=5)

    def send_message(self):
        # Obtém o texto do usuário
        user_message = self.input_area.get("1.0", tk.END).strip()
        if user_message:
            self.update_chat(f"User: {user_message}")
            # Simula resposta da AI
            self.update_chat(f"Model: Hello, I received: {user_message}")
        self.input_area.delete("1.0", tk.END)

    def update_chat(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.see(tk.END)  # Rola para o final
        self.chat_area.config(state=tk.DISABLED)

    def create_tray_icon(self):
        # Criação do ícone para o tray
        icon_image = self.generate_icon_image()
        menu = Menu(MenuItem("Open", self.show_window), MenuItem("Quit", self.quit_app))
        self.icon = Icon("AI Chat", icon_image, menu=menu)

        # Inicia o tray icon em uma thread separada
        threading.Thread(target=self.icon.run, daemon=True).start()

    def generate_icon_image(self):
        # Gera um ícone simples com PIL
        size = (64, 64)
        image = Image.new("RGB", size, color="blue")
        draw = ImageDraw.Draw(image)
        draw.ellipse((16, 16, 48, 48), fill="white", outline="black")
        return image

    def show_window(self, _=None):
        self.root.deiconify()

    def hide_window(self):
        self.root.withdraw()

    def quit_app(self, _=None):
        self.icon.stop()
        self.root.quit()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ChatApp()
    app.run()
