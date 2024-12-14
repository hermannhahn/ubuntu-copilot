import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib
from gi.repository import Gdk

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
        self.entry.set_vexpand(False)  # Expande verticalmente
        self.entry.set_hexpand(True)  # Expande horizontalmente

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

        # Adicionar controlador de eventos para capturar teclas
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.entry.add_controller(key_controller)

    def on_key_pressed(self, controller, keyval, keycode, state):
        # Detecta Shift+Enter
        if keyval == Gdk.KEY_Return and (state & Gdk.ModifierType.SHIFT_MASK):
            return False  # Permite a quebra de linha normal

        # Detecta Enter sem Shift
        if keyval == Gdk.KEY_Return:
            self.on_message_sent()  # Chama a função de envio
            return True  # Bloqueia a quebra de linha no TextView

        return False  # Permite outros comportamentos padrão
    
    def on_message_sent(self, widget=None):
        # verifica api
        api = self.check_api_key()
        if not api:
            return
        
        # Captura o texto da entrada
        buffer = self.entry.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        text = buffer.get_text(start_iter, end_iter, True).strip()

        if text:
            # Adiciona o texto enviado no display de mensagens
            display_buffer = self.chat_display.get_buffer()
            display_buffer.insert(display_buffer.get_end_iter(), f"Você: {text}\n")
            self.ai.get_response(text, self.callback)

        # Limpa o campo de entrada
        self.entry.set_text("")

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
            return False
        return True

    