#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt5 + PyCryptodome ile AES-256 (CBC) şifreleme/şifre çözme uygulaması.
"""

import sys
import base64
import hashlib

from PyQt5.QtWidgets import (
    QApplication,
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

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class AESCipherApp(QMainWindow):
    """AES-256 şifreleme ve çözme arayüzünü yöneten ana pencere sınıfı."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyAES | AES-256 Şifreleme")
        self.setMinimumSize(760, 700)
        self.current_theme = "Daha Opak"
        self._apply_styles(self.current_theme)
        self._init_ui()

    def _apply_styles(self, theme_name: str):
        """Seçilen tema tipine göre stil ve pencere şeffaflığı uygular."""
        theme_map = {
            "Daha Opak": {
                "opacity": 0.98,
                "main_bg": "rgba(6, 10, 16, 248)",
                "title": "#e2e8f0",
                "subtitle": "#94a3b8",
                "card_start": "rgba(20, 25, 35, 236)",
                "card_end": "rgba(14, 19, 29, 236)",
                "card_border": "rgba(148, 163, 184, 72)",
                "label": "#cbd5e1",
                "input_bg": "rgba(15, 23, 42, 198)",
                "input_color": "#e2e8f0",
                "input_border": "rgba(148, 163, 184, 92)",
                "focus": "#22d3ee",
                "btn1": "#06b6d4",
                "btn1_hover": "#22d3ee",
                "btn1_press": "#0891b2",
                "btn2": "#2dd4bf",
                "btn2_hover": "#5eead4",
                "btn2_press": "#14b8a6",
                "btn_text": "#0b1120",
            },
            "Daha Transparan": {
                "opacity": 0.93,
                "main_bg": "rgba(7, 11, 18, 208)",
                "title": "#e2e8f0",
                "subtitle": "#93a8bf",
                "card_start": "rgba(20, 26, 37, 170)",
                "card_end": "rgba(14, 20, 30, 170)",
                "card_border": "rgba(148, 163, 184, 58)",
                "label": "#c7d2e0",
                "input_bg": "rgba(15, 23, 42, 126)",
                "input_color": "#e5edf7",
                "input_border": "rgba(148, 163, 184, 72)",
                "focus": "#67e8f9",
                "btn1": "#22d3ee",
                "btn1_hover": "#67e8f9",
                "btn1_press": "#06b6d4",
                "btn2": "#5eead4",
                "btn2_hover": "#99f6e4",
                "btn2_press": "#2dd4bf",
                "btn_text": "#05202a",
            },
            "Premium Siyah": {
                "opacity": 1.0,
                "main_bg": "#030507",
                "title": "#f8fafc",
                "subtitle": "#a9b5c7",
                "card_start": "rgba(9, 12, 17, 245)",
                "card_end": "rgba(4, 7, 11, 245)",
                "card_border": "rgba(56, 189, 248, 74)",
                "label": "#e2e8f0",
                "input_bg": "rgba(2, 6, 12, 222)",
                "input_color": "#f1f5f9",
                "input_border": "rgba(71, 85, 105, 120)",
                "focus": "#38bdf8",
                "btn1": "#38bdf8",
                "btn1_hover": "#7dd3fc",
                "btn1_press": "#0ea5e9",
                "btn2": "#2dd4bf",
                "btn2_hover": "#5eead4",
                "btn2_press": "#14b8a6",
                "btn_text": "#020617",
            },
        }
        selected = theme_map.get(theme_name, theme_map["Daha Opak"])
        self.setWindowOpacity(selected["opacity"])
        stylesheet_template = """
            QMainWindow {
                background-color: __main_bg__;
            }
            QLabel#titleLabel {
                color: __title__;
                font-size: 30px;
                font-weight: 700;
                margin-bottom: 2px;
            }
            QLabel#subtitleLabel {
                color: __subtitle__;
                font-size: 13px;
                margin-bottom: 12px;
            }
            QLabel#themeLabel {
                color: __subtitle__;
                font-size: 12px;
                font-weight: 600;
                margin-right: 4px;
                margin-top: 0px;
            }
            QComboBox#themeCombo {
                background-color: __input_bg__;
                color: __input_color__;
                border: 1px solid __input_border__;
                border-radius: 10px;
                padding: 6px 10px;
                min-width: 140px;
                min-height: 34px;
                font-size: 13px;
            }
            QComboBox#themeCombo::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox#themeCombo QAbstractItemView {
                background-color: rgba(8, 14, 22, 240);
                color: #e2e8f0;
                border: 1px solid rgba(56, 189, 248, 90);
                selection-background-color: rgba(14, 165, 233, 130);
            }
            QFrame#card {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 __card_start__,
                    stop: 1 __card_end__
                );
                border: 1px solid __card_border__;
                border-radius: 16px;
            }
            QLabel {
                color: __label__;
                font-size: 14px;
                font-weight: 600;
                margin-top: 4px;
            }
            QLineEdit, QTextEdit {
                background-color: __input_bg__;
                color: __input_color__;
                border: 1px solid __input_border__;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
                selection-background-color: #0ea5e9;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid __focus__;
            }
            QPushButton {
                background-color: __btn1__;
                color: __btn_text__;
                border: none;
                border-radius: 11px;
                font-size: 14px;
                font-weight: 700;
                padding: 10px 14px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: __btn1_hover__;
            }
            QPushButton:pressed {
                background-color: __btn1_press__;
            }
            QPushButton#decryptButton {
                background-color: __btn2__;
            }
            QPushButton#decryptButton:hover {
                background-color: __btn2_hover__;
            }
            QPushButton#decryptButton:pressed {
                background-color: __btn2_press__;
            }
            """
        replacements = {
            "__main_bg__": selected["main_bg"],
            "__title__": selected["title"],
            "__subtitle__": selected["subtitle"],
            "__card_start__": selected["card_start"],
            "__card_end__": selected["card_end"],
            "__card_border__": selected["card_border"],
            "__label__": selected["label"],
            "__input_bg__": selected["input_bg"],
            "__input_color__": selected["input_color"],
            "__input_border__": selected["input_border"],
            "__focus__": selected["focus"],
            "__btn1__": selected["btn1"],
            "__btn1_hover__": selected["btn1_hover"],
            "__btn1_press__": selected["btn1_press"],
            "__btn2__": selected["btn2"],
            "__btn2_hover__": selected["btn2_hover"],
            "__btn2_press__": selected["btn2_press"],
            "__btn_text__": selected["btn_text"],
        }
        for token, value in replacements.items():
            stylesheet_template = stylesheet_template.replace(token, value)
        self.setStyleSheet(stylesheet_template)

    def handle_theme_change(self, theme_name: str):
        """Tema değişiminde ilgili stil ayarlarını uygular."""
        self.current_theme = theme_name
        self._apply_styles(theme_name)

    def _init_ui(self):
        """Arayüz bileşenlerini oluşturur ve yerleşimi ayarlar."""
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

        # Şifrelenecek metin girişi
        self.input_label = QLabel("Şifrelenecek Metin:")
        self.input_text = QTextEdit()
        self.input_text.setMinimumHeight(120)
        self.input_text.setPlaceholderText("Şifrelenecek metni buraya yazın...")

        # Parola girişi (gizli)
        self.password_label = QLabel("Parola / Anahtar:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Parolanızı girin...")

        # Şifreleme butonu
        self.encrypt_button = QPushButton("Şifrele")
        self.encrypt_button.clicked.connect(self.handle_encrypt)

        # Şifrelenmiş metin çıktısı
        self.encrypted_label = QLabel("Şifrelenmiş Metin (Base64):")
        self.encrypted_output = QTextEdit()
        self.encrypted_output.setMinimumHeight(125)
        self.encrypted_output.setReadOnly(False)
        self.encrypted_output.setPlaceholderText("Şifrelenmiş metin burada görünecek...")

        # Şifre çözme butonu
        self.decrypt_button = QPushButton("Şifreyi Çöz")
        self.decrypt_button.setObjectName("decryptButton")
        self.decrypt_button.clicked.connect(self.handle_decrypt)

        # Çözülmüş metin çıktısı
        self.decrypted_label = QLabel("Çözülmüş Metin:")
        self.decrypted_output = QTextEdit()
        self.decrypted_output.setMinimumHeight(120)
        self.decrypted_output.setReadOnly(True)
        self.decrypted_output.setPlaceholderText("Çözülmüş metin burada görünecek...")

        button_row = QHBoxLayout()
        button_row.setSpacing(10)
        button_row.addWidget(self.encrypt_button)
        button_row.addWidget(self.decrypt_button)

        # Bileşenleri dikey yerleşime ekle
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

    def derive_aes_key(self, password: str) -> bytes:
        """Parolayı SHA-256 ile hash'leyip 32 byte AES anahtarına dönüştürür."""
        return hashlib.sha256(password.encode("utf-8")).digest()

    def handle_encrypt(self):
        """Şifreleme akışını yönetir."""
        plaintext = self.input_text.toPlainText().strip()
        password = self.password_input.text().strip()

        # Boş alan kontrolü
        if not plaintext or not password:
            QMessageBox.warning(self, "Uyarı", "Lütfen metin ve parola alanlarını doldurun!")
            return

        try:
            # SHA-256 ile 256-bit anahtar üret
            key = self.derive_aes_key(password)

            # 16 byte rastgele IV üret ve AES-CBC nesnesini oluştur
            iv = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)

            # PKCS7 padding uygula ve şifrele
            padded_plaintext = pad(plaintext.encode("utf-8"), AES.block_size)
            ciphertext = cipher.encrypt(padded_plaintext)

            # IV + şifreli veriyi birleştirip Base64'e çevir
            encrypted_payload = base64.b64encode(iv + ciphertext).decode("utf-8")
            self.encrypted_output.setPlainText(encrypted_payload)

        except Exception as exc:
            QMessageBox.critical(self, "Hata", f"Şifreleme sırasında hata oluştu: {exc}")

    def handle_decrypt(self):
        """Şifre çözme akışını yönetir."""
        encrypted_b64 = self.encrypted_output.toPlainText().strip()
        password = self.password_input.text().strip()

        # Boş alan kontrolü
        if not encrypted_b64 or not password:
            QMessageBox.warning(self, "Uyarı", "Lütfen şifreli metin ve parola alanlarını doldurun!")
            return

        try:
            # SHA-256 ile 256-bit anahtar üret
            key = self.derive_aes_key(password)

            # Base64 çöz ve IV/ciphertext olarak ayır
            encrypted_data = base64.b64decode(encrypted_b64)
            if len(encrypted_data) <= 16:
                raise ValueError("Geçersiz veri uzunluğu")

            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]

            # AES-CBC ile çöz ve PKCS7 padding kaldır
            cipher = AES.new(key, AES.MODE_CBC, iv)
            padded_plaintext = cipher.decrypt(ciphertext)
            plaintext = unpad(padded_plaintext, AES.block_size).decode("utf-8")

            self.decrypted_output.setPlainText(plaintext)

        except ValueError:
            # Yanlış parola, bozuk veri, padding hatası vb. durumlar
            QMessageBox.warning(self, "Uyarı", "Hatalı Parola veya Bozuk Veri!")
        except Exception as exc:
            QMessageBox.critical(self, "Hata", f"Şifre çözme sırasında beklenmeyen hata: {exc}")


def main():
    """Uygulamayı başlatır."""
    app = QApplication(sys.argv)
    window = AESCipherApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
