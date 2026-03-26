THEME_MAP = {
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


def build_stylesheet(theme_name: str) -> tuple[float, str]:
    selected = THEME_MAP.get(theme_name, THEME_MAP["Daha Opak"])
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

    return selected["opacity"], stylesheet_template
