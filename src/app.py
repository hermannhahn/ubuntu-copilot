import tkinter as tk
from tkinter import messagebox, scrolledtext
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading
from pynput import keyboard


class CrossPlatformApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chat")
        self.root.geometry("800x600")

        # Adiciona a interface de chat
        self.create_ui()

        # Adiciona o monitor de teclado
        self.start_keyboard_monitor()

        # Ícone do tray
        self.icon = None
        self.create_tray_icon()

    def create_ui(self):
        """Cria a interface gráfica do chat."""
        # Área de chat
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Arial", 12), background="#252525", foreground="#252525", borderwidth=0)
        self.chat_area.config(state=tk.DISABLED)  # Apenas leitura
        self.chat_area.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        # Área de entrada e botões
        bottom_frame = tk.Frame(self.root, bg="#252525")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # Botões de ação
        buttons_frame = tk.Frame(bottom_frame, bg="#252525", borderwidth=0)
        buttons_frame.pack(side=tk.RIGHT, padx=2)
        buttons_frame.pack_propagate(False)  # Evitar redimensionamento automático

        # Criar botões com tamanhos mínimos
        button_width = 5  # Largura mínima dos botões
        send_button = tk.Button(buttons_frame, text="↵", command=self.send_message, width=button_width)
        send_button.grid(row=0, column=0, padx=2)

        mic_button = tk.Button(buttons_frame, text="🎤", command=lambda: print("Mic clicked"), width=button_width)
        mic_button.grid(row=0, column=1, padx=2)

        trash_button = tk.Button(buttons_frame, text="🗑️", command=lambda: print("Trash clicked"), width=button_width)
        trash_button.grid(row=0, column=2, padx=2)

        settings_button = tk.Button(buttons_frame, text="🛠", command=lambda: print("Settings clicked"), width=button_width)
        settings_button.grid(row=0, column=3, padx=2)

        # Área de entrada ajustável
        self.input_area = tk.Text(bottom_frame, wrap=tk.WORD, height=3, font=("Arial", 12))
        self.input_area.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Configuração para ajustar a largura do input
        self.root.bind("<Configure>", self.adjust_input_width)

    def adjust_input_width(self, event=None):
        """Ajusta a largura do input_area conforme o tamanho da janela."""
        button_area_width = 5 * 4 * 10 + 20  # Largura total dos botões (+ margem)
        total_width = self.root.winfo_width()
        input_width = max(total_width - button_area_width, 100)  # Garante largura mínima
        self.input_area.config(width=input_width)

    def send_message(self):
        """Envia a mensagem digitada pelo usuário."""
        user_message = self.input_area.get("1.0", tk.END).strip()
        if user_message:
            self.update_chat(f"User: {user_message}")
            self.update_chat(f"Model: Hello, I received: {user_message}")
        self.input_area.delete("1.0", tk.END)

    def update_chat(self, message):
        """Atualiza a área de chat com uma nova mensagem."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def create_tray_icon(self):
        """Cria o ícone do tray com menu."""
        icon_image = self.generate_icon_image()
        menu = Menu(MenuItem("Open", self.show_window), MenuItem("Quit", self.quit_app))
        self.icon = Icon("AI Chat", icon_image, menu=menu)

        # Inicia o tray icon em uma thread separada
        threading.Thread(target=self.icon.run, daemon=True).start()

    def generate_icon_image(self):
        """Gera um ícone simples usando PIL."""
        size = (64, 64)
        image = Image.new("RGB", size, color="blue")
        draw = ImageDraw.Draw(image)
        draw.ellipse((16, 16, 48, 48), fill="white", outline="black")
        return image

    def show_window(self, _=None):
        """Mostra a janela principal."""
        self.root.deiconify()

    def hide_window(self):
        """Esconde a janela principal."""
        self.root.withdraw()

    def quit_app(self, _=None):
        """Encerra o aplicativo."""
        if self.icon:
            self.icon.stop()
        self.root.quit()

    def start_keyboard_monitor(self):
        """Inicia o monitor de teclado em uma thread separada."""
        threading.Thread(target=self.keyboard_listener, daemon=True).start()

    def keyboard_listener(self):
        """Monitora eventos globais de teclado."""
        def on_press(key):
            try:
                if key == keyboard.Key.f1:
                    # A chamada para mostrar a mensagem precisa ser feita na thread principal do Tkinter
                    self.root.after(0, self.on_f1_pressed)
            except Exception as e:
                print(f"Erro no listener de teclado: {e}")

        # Inicia o listener de teclado
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def on_f1_pressed(self):
        """Ação executada ao pressionar F1."""
        messagebox.showinfo("Tecla F1 Pressionada", "Você pressionou F1!")

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = CrossPlatformApp(root)
    app.run()
