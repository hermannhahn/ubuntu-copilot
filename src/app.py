import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk, AppIndicator3, GObject


class TrayApp:
    def __init__(self):
        # Cria o indicador na barra de tarefas
        self.indicator = AppIndicator3.Indicator.new(
            "tray-app",
            "dialog-information",  # Ícone padrão
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())

        # Janela flutuante
        self.window = Gtk.Window(type=Gtk.WindowType.POPUP)
        self.window.set_size_request(300, 150)
        self.window.set_resizable(False)
        self.window.set_border_width(10)
        self.window.set_valign(Gtk.Align.END)
        self.window.set_halign(Gtk.Align.END)

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

    def create_menu(self):
        # Menu de contexto para o indicador
        menu = Gtk.Menu()

        show_item = Gtk.MenuItem(label="Abrir")
        show_item.connect("activate", self.show_window)
        menu.append(show_item)

        quit_item = Gtk.MenuItem(label="Sair")
        quit_item.connect("activate", Gtk.main_quit)
        menu.append(quit_item)

        menu.show_all()
        return menu

    def show_window(self, *_):
        # Mostra a janela flutuante
        if not self.window.get_visible():
            self.window.show_all()
        else:
            self.window.hide()

    def on_mic_click(self, button):
        print("Mic button clicked")

    def on_trash_click(self, button):
        buffer = self.text_view.get_buffer()
        buffer.set_text("")  # Limpa o texto

    def on_settings_click(self, button):
        print("Settings button clicked")


if __name__ == "__main__":
    GObject.threads_init()  # Inicializa threads do GTK
    app = TrayApp()
    Gtk.main()
