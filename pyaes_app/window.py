from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QFrame,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)

from pyaes_app.crypto_service import encrypt_text, decrypt_text
from pyaes_app.themes import build_stylesheet


class AESCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyAES | AES-256 Şifreleme")
        self.setMinimumSize(760, 700)
        self.current_theme = "Daha Opak"
        self.apply_theme(self.current_theme)
        self._init_ui()

    def apply_theme(self, theme_name: str):
        opacity, stylesheet = build_stylesheet(theme_name)
        self.setWindowOpacity(opacity)
        self.setStyleSheet(stylesheet)

    def handle_theme_change(self, theme_name: str):
        self.current_theme = theme_name
        self.apply_theme(theme_name)

    def _init_ui(self):
        central_widget = QWidget(self)
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(26, 20, 26, 20)
        outer_layout.setSpacing(12)

        title_label = QLabel("PyAES")
        title_label.setObjectName("titleLabel")
        subtitle_label = QLabel("AES-256 CBC ile güvenli metin şifreleme ve çözme")
        subtitle_label.setObjectName("subtitleLabel")

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)

        header_left = QVBoxLayout()
        header_left.setContentsMargins(0, 0, 0, 0)
        header_left.setSpacing(0)
        header_left.addWidget(title_label)
        header_left.addWidget(subtitle_label)

        header_right = QHBoxLayout()
        header_right.setContentsMargins(0, 0, 0, 0)
        header_right.setSpacing(6)
        header_right.addStretch(1)
        self.theme_label = QLabel("Tema")
        self.theme_label.setObjectName("themeLabel")
        self.theme_combo = QComboBox()
        self.theme_combo.setObjectName("themeCombo")
        self.theme_combo.addItems(["Daha Opak", "Daha Transparan", "Premium Siyah"])
        self.theme_combo.setCurrentText(self.current_theme)
        self.theme_combo.currentTextChanged.connect(self.handle_theme_change)
        header_right.addWidget(self.theme_label)
        header_right.addWidget(self.theme_combo)

        header_row.addLayout(header_left)
        header_row.addLayout(header_right)

        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        self.input_label = QLabel("Şifrelenecek Metin:")
        self.input_text = QTextEdit()
        self.input_text.setMinimumHeight(120)
        self.input_text.setPlaceholderText("Şifrelenecek metni buraya yazın...")

        self.password_label = QLabel("Parola / Anahtar:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Parolanızı girin...")

        self.encrypt_button = QPushButton("Şifrele")
        self.encrypt_button.clicked.connect(self.handle_encrypt)

        self.encrypted_label = QLabel("Şifrelenmiş Metin (Base64):")
        self.encrypted_output = QTextEdit()
        self.encrypted_output.setMinimumHeight(125)
        self.encrypted_output.setReadOnly(False)
        self.encrypted_output.setPlaceholderText("Şifrelenmiş metin burada görünecek...")

        self.decrypt_button = QPushButton("Şifreyi Çöz")
        self.decrypt_button.setObjectName("decryptButton")
        self.decrypt_button.clicked.connect(self.handle_decrypt)

        self.decrypted_label = QLabel("Çözülmüş Metin:")
        self.decrypted_output = QTextEdit()
        self.decrypted_output.setMinimumHeight(120)
        self.decrypted_output.setReadOnly(True)
        self.decrypted_output.setPlaceholderText("Çözülmüş metin burada görünecek...")

        button_row = QHBoxLayout()
        button_row.setSpacing(10)
        button_row.addWidget(self.encrypt_button)
        button_row.addWidget(self.decrypt_button)

        layout.addWidget(self.input_label)
        layout.addWidget(self.input_text)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addLayout(button_row)
        layout.addWidget(self.encrypted_label)
        layout.addWidget(self.encrypted_output)
        layout.addWidget(self.decrypted_label)
        layout.addWidget(self.decrypted_output)

        card.setLayout(layout)
        outer_layout.addLayout(header_row)
        outer_layout.addWidget(card)

        central_widget.setLayout(outer_layout)
        self.setCentralWidget(central_widget)

    def handle_encrypt(self):
        plaintext = self.input_text.toPlainText().strip()
        password = self.password_input.text().strip()

        if not plaintext or not password:
            QMessageBox.warning(self, "Uyarı", "Lütfen metin ve parola alanlarını doldurun!")
            return

        try:
            encrypted_payload = encrypt_text(plaintext, password)
            self.encrypted_output.setPlainText(encrypted_payload)
        except Exception as exc:
            QMessageBox.critical(self, "Hata", f"Şifreleme sırasında hata oluştu: {exc}")

    def handle_decrypt(self):
        encrypted_b64 = self.encrypted_output.toPlainText().strip()
        password = self.password_input.text().strip()

        if not encrypted_b64 or not password:
            QMessageBox.warning(self, "Uyarı", "Lütfen şifreli metin ve parola alanlarını doldurun!")
            return

        try:
            plaintext = decrypt_text(encrypted_b64, password)
            self.decrypted_output.setPlainText(plaintext)
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Hatalı Parola veya Bozuk Veri!")
        except Exception as exc:
            QMessageBox.critical(self, "Hata", f"Şifre çözme sırasında beklenmeyen hata: {exc}")
