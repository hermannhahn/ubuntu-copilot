import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk, AppIndicator3, GObject, Gdk


# Classe principal
class TrayApp:
    def __init__(self):
        # Cria o indicador na barra de tarefas
        self.indicator = AppIndicator3.Indicator.new(
            "uubuntu-copilot",
            "dialog-information",  # Ícone padrão
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_empty_menu())  # Necessário, mesmo que vazio

        # Janela flutuante
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_default_size(800, 600)  # Tamanho inicial
        self.window.set_border_width(10)
        self.window.set_title("Chat App")
        self.window.set_position(Gtk.WindowPosition.CENTER)

        self.window.connect("focus-out-event", lambda *args: self.window.hide())

        # Layout principal da janela
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.window.add(main_box)

        # Área de chat (acima)
        self.chat_area = Gtk.TextView()
        self.chat_area.set_wrap_mode(Gtk.WrapMode.WORD)
        self.chat_area.set_editable(False)
        self.chat_area.set_cursor_visible(False)
        self.chat_area.set_vexpand(True)  # Expande para preencher o espaço disponível
        chat_scroll = Gtk.ScrolledWindow()
        chat_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)  # Apenas scroll vertical
        # chat_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        chat_scroll.add(self.chat_area)
        main_box.pack_start(chat_scroll, expand=True, fill=True, padding=0)

        # Área inferior (caixa de texto e ícones)
        bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        main_box.pack_start(bottom_box, expand=False, fill=True, padding=0)

        # Caixa de texto para entrada de perguntas (multilinhas com limite de 3 linhas visíveis)
        input_scroll = Gtk.ScrolledWindow()
        input_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)  # Apenas scroll vertical
        # input_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        input_scroll.set_min_content_height(60)  # Aproximadamente 3 linhas de altura
        input_scroll.set_max_content_height(60)  # Fixar altura máxima em 3 linhas
        self.input_text = Gtk.TextView()
        self.input_text.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        input_scroll.add(self.input_text)
        bottom_box.pack_start(input_scroll, expand=True, fill=True, padding=0)

        # Enter
        self.input_text.connect("key-press-event", self.on_enter)
        
        # Botões com ícones (send, mic, trash, settings)
        send_button = Gtk.Button()
        send_icon = Gtk.Image.new_from_icon_name("mail-send-receive", Gtk.IconSize.BUTTON)
        send_button.add(send_icon)
        send_button.connect("clicked", self.on_send_click)
        bottom_box.pack_start(send_button, expand=False, fill=False, padding=0)

        mic_button = Gtk.Button()
        mic_icon = Gtk.Image.new_from_icon_name("audio-input-microphone", Gtk.IconSize.BUTTON)
        mic_button.add(mic_icon)
        mic_button.connect("clicked", self.on_mic_click)
        bottom_box.pack_start(mic_button, expand=False, fill=False, padding=0)

        trash_button = Gtk.Button()
        trash_icon = Gtk.Image.new_from_icon_name("user-trash", Gtk.IconSize.BUTTON)
        trash_button.add(trash_icon)
        trash_button.connect("clicked", self.on_trash_click)
        bottom_box.pack_start(trash_button, expand=False, fill=False, padding=0)

        settings_button = Gtk.Button()
        settings_icon = Gtk.Image.new_from_icon_name("emblem-system", Gtk.IconSize.BUTTON)
        settings_button.add(settings_icon)
        settings_button.connect("clicked", self.on_settings_click)
        bottom_box.pack_start(settings_button, expand=False, fill=False, padding=0)

        # Monitora cliques no tray via timeout
        self.monitor_tray()

    def create_empty_menu(self):
        # Cria um menu vazio (necessário para evitar erros no AppIndicator)
        menu = Gtk.Menu()
        menu.show_all()
        return menu

    def monitor_tray(self):
        # Adiciona um temporizador para verificar cliques no ícone do tray
        GObject.timeout_add(500, self.show_window)

    def show_window(self, *_):
        # Mostra a janela flutuante maximizada
        if not self.window.get_visible():
            self.window.show_all()
            # self.window.maximize()
        else:
            self.window.hide()
        return False  # Retorna False para não repetir o timeout
    
    def on_enter(self, widget, event):
        if event.keyval == Gdk.KEY_Return:
            self.on_send_click(None)

    def on_send_click(self, button):
        buffer = self.input_text.get_buffer()
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
        if text.strip():  # Verifica se há texto além de espaços em branco
            self.add_message_to_chat(text, True)  # Adiciona a mensagem do usuário
            self.add_message_to_chat("Resposta do modelo de linguagem", False)  # Adiciona a resposta do modelo
            buffer.set_text("")  # Limpa a caixa de texto de entrada

    def add_message_to_chat(self, message, user):
        buffer = self.chat_area.get_buffer()
        end_iter = buffer.get_end_iter()
        if user:
            buffer.insert(end_iter, f"User: {message}\n")
        else:
            buffer.insert(end_iter, f"Model: {message}\n")
        self.chat_area.scroll_to_iter(end_iter, 0, True, 0, 0)

    def on_send_click(self, button):
        print("Send button clicked")

    def on_mic_click(self, button):
        print("Mic button clicked")

    def on_trash_click(self, button):
        # Limpa tanto a entrada quanto a área de chat
        buffer = self.input_text.get_buffer()
        buffer.set_text("")
        chat_buffer = self.chat_area.get_buffer()
        chat_buffer.set_text("")

    def on_settings_click(self, button):
        print("Settings button clicked")


if __name__ == "__main__":
    GObject.threads_init()  # Inicializa threads do GTK
    app = TrayApp()
    Gtk.main()
