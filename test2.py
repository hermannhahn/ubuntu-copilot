import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk, AppIndicator3, Gdk


class TrayApp:
    def __init__(self):
        # Cria o indicador na bandeja do sistema
        self.indicator = AppIndicator3.Indicator.new(
            "tray-app",
            "dialog-information",  # Ícone do sistema
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        # Conecta o clique no ícone para abrir a janela
        self.indicator.connect("activate", self.show_window)

        # Janela flutuante
        self.window = Gtk.Window(type=Gtk.WindowType.POPUP)
        self.window.set_size_request(300, 150)
        self.window.set_resizable(False)
        self.window.set_border_width(10)
        self.window.connect("focus-out-event", lambda *args: self.window.hide())

        # Layout principal da janela
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.window.add(main_box)

        # Caixa de texto multilinhas
        self.text_view = Gtk.TextView()
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        main_box.pack_start(self.text_view, expand=True, fill=True, padding=0)

        # Botões com ícones
        button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        main_box.pack_start(button_box, expand=False, fill=False, padding=0)

        # Botão Mic
        mic_button = Gtk.Button()
        mic_icon = Gtk.Image.new_from_icon_name("audio-input-microphone", Gtk.IconSize.BUTTON)
        mic_button.add(mic_icon)
        mic_button.connect("clicked", self.on_mic_click)
        button_box.pack_start(mic_button, expand=False, fill=False, padding=0)

        # Botão Trash
        trash_button = Gtk.Button()
        trash_icon = Gtk.Image.new_from_icon_name("user-trash", Gtk.IconSize.BUTTON)
        trash_button.add(trash_icon)
        trash_button.connect("clicked", self.on_trash_click)
        button_box.pack_start(trash_button, expand=False, fill=False, padding=0)

        # Botão Settings
        settings_button = Gtk.Button()
        settings_icon = Gtk.Image.new_from_icon_name("emblem-system", Gtk.IconSize.BUTTON)
        settings_button.add(settings_icon)
        settings_button.connect("clicked", self.on_settings_click)
        button_box.pack_start(settings_button, expand=False, fill=False, padding=0)

    def show_window(self, *_):
        # Mostra a janela flutuante próxima ao ícone
        if not self.window.get_visible():
            self.position_window()
            self.window.show_all()
        else:
            self.window.hide()

    def position_window(self):
        # Posiciona a janela acima do ícone na bandeja
        screen = Gdk.Screen.get_default()
        pointer = Gdk.Display.get_default().get_default_seat().get_pointer()
        _, icon_x, icon_y = pointer.get_position()

        # Define a posição da janela
        window_width, window_height = self.window.get_size()
        x = max(0, icon_x - (window_width // 2))
        y = max(0, icon_y - window_height - 10)  # Ajuste para abrir acima
        self.window.move(x, y)

    def on_mic_click(self, button):
        print("Mic button clicked")

    def on_trash_click(self, button):
        buffer = self.text_view.get_buffer()
        buffer.set_text("")  # Limpa o texto

    def on_settings_click(self, button):
        print("Settings button clicked")


if __name__ == "__main__":
    app = TrayApp()
    Gtk.main()
