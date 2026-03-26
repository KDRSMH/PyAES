import sys

from PyQt5.QtWidgets import QApplication

from pyaes_app.window import AESCipherApp


def main():
    app = QApplication(sys.argv)
    window = AESCipherApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
