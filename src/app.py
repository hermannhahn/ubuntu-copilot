import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, scrolledtext
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading
from pynput import keyboard
from chat import Chat


class CrossPlatformApp:

    def __init__(self, root):
        # Keyboard events
        self.start_keyboard_monitor()

        # Tray icon
        self.icon = None
        self.create_tray_icon()

    def create_tray_icon(self):
        """Cria o ícone do tray com menu."""
        # Gera o ícone
        icon_image = self.generate_icon_image()

        # Cria o menu com ações
        menu = Menu(MenuItem("Chat", self.show_chat),
                    MenuItem("Quit", self.quit_app))

        # Cria o ícone da bandeja
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

    def show_chat(self, _=None):
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
