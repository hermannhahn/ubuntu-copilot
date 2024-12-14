import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

from settings import SettingsWindow, load_api_key, load_project_id, load_region
from ai import GenerativeChat

class ChatWindow:
    def __init__(self):
        
        # Load AI
        self.ai = GenerativeChat()
        self.api_key = load_api_key()
        self.project_id = load_project_id()
        self.region = load_region()
        
        # Layout principal
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.layout.set_margin_top(0)
        self.layout.set_margin_bottom(0)
        self.layout.set_margin_start(0)
        self.layout.set_margin_end(0)

        # Área de exibição do chat
        self.chat_display = Gtk.TextView()
        self.chat_display.set_wrap_mode(Gtk.WrapMode.WORD)
        self.chat_display.set_editable(False)
        self.chat_display.set_cursor_visible(False)
        self.chat_display.set_margin_top(5)
        self.chat_display.set_margin_bottom(5)
        self.chat_display.set_margin_start(5)
        self.chat_display.set_margin_end(5)

        # Scroll para a área de chat
        self.chat_scroll = Gtk.ScrolledWindow()
        self.chat_scroll.set_vexpand(True)

        # Bottom
        self.bottom = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.bottom.set_margin_top(0)
        self.bottom.set_margin_bottom(5)
        self.bottom.set_margin_start(5)
        self.bottom.set_margin_end(5)

        # Campo de texto multilinhas (TextView)
        self.entry = Gtk.TextView()
        self.entry.set_wrap_mode(Gtk.WrapMode.WORD)  # Quebra de linha automática
        self.entry.set_vexpand(True)  # Expande verticalmente
        self.entry.connect("key-press-event", self.on_key_press)

        # Botão de enviar
        self.send_button = Gtk.Button(label="Enviar")
        self.send_button.connect("clicked", self.on_message_sent)

        # Botão para abrir configurações
        self.settings_button = Gtk.Button(label="⚙")
        self.settings_button.connect("clicked", self.open_settings)
            
        self.chat_scroll.set_child(self.chat_display)
        self.layout.append(self.chat_scroll)
        self.layout.append(self.bottom)
        self.bottom.append(self.entry)
        self.bottom.append(self.send_button)
        self.bottom.append(self.settings_button)

    def on_key_press(self, widget, event):
        if event.keyval == 65293:  # Enter key
            self.on_message_sent(widget)
            return True
        return False

    def on_message_sent(self, widget):
        # verifica api
        self.check_api_key()
        # Captura o texto da entrada
        message = self.entry.get_text()
        # Limpa o campo de entrada
        self.entry.set_text("")
        # Exibe a mensagem no chat
        buffer = self.chat_display.get_buffer()
        buffer.insert(buffer.get_end_iter(), f"Você: {message}\n")

        # Verifica se a mensagem não está vazia
        if message.strip():
            # Envia a mensagem para o modelo de linguagem e exibe a resposta
            self.ai.get_response(message, self.callback)

    def callback(self, response):
        buffer = self.chat_display.get_buffer()
        buffer.insert(buffer.get_end_iter(), f"Bot: {response}\n")

    def open_settings(self, widget=None):
        # Abre a janela de configurações
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def close_alert(self, d):
        d.close()

    def check_api_key(self):
        # Verifica se as credenciais estão configuradas
        if not self.api_key or not self.project_id or not self.region:
            # api key alert message
            self.api_alert = Gtk.MessageDialog(
                transient_for=None,
                title="Settings",
                modal=True,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Por favor, configure as credenciais antes de continuar.",
            )
            self.api_alert.connect("response", lambda d, r: self.close_alert(d))
            self.api_alert.show()
            return
    