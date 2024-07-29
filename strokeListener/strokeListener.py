from PyQt5.QtWidgets import QCheckBox, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QOpenGLWidget, QComboBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent, QTimer
from PyQt5.QtGui import QKeyEvent, QKeySequence, QGuiApplication, QCursor
from krita import DockWidget # type: ignore

PRESETS = [
    'ctrl+shift+1',
    'ctrl+shift+2',
    'ctrl+shift+3',
    'ctrl+shift+4',
    'ctrl+shift+5',
    'ctrl+shift+6',
    'ctrl+shift+7',
    'ctrl+shift+8',
    'ctrl+shift+9',
    'ctrl+shift+0',
    'custom'
]

class MouseListener(QObject):
    mouseReleased = pyqtSignal()

    def __init__(self):
        super().__init__()

    def eventFilter(self, obj, event):
        if (event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton) or \
           (event.type() == QEvent.TabletRelease and event.button() == Qt.LeftButton):
            self.mouseReleased.emit()
        return super().eventFilter(obj, event)

class StrokeListenerDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stroke Listener Docker")
        self.widget = QWidget()
        self.setWidget(self.widget)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 15, 0, 0)
        self.widget.setLayout(self.layout)

        # Preset Dropdown
        self.preset_dropdown = QComboBox()
        self.preset_dropdown.addItems(PRESETS)
        self.layout.addWidget(self.preset_dropdown)

        # Listening Checkbox
        self.listening_checkbox = QCheckBox("Not Listening")
        self.listening_checkbox.setStyleSheet("color: red;")
        self.layout.addWidget(self.listening_checkbox)
        self.listening_checkbox.stateChanged.connect(self.update_checkbox_label)


        # Modifier Checkboxes
        self.ctrl_checkbox = QCheckBox("Ctrl")
        self.layout.addWidget(self.ctrl_checkbox)
        self.shift_checkbox = QCheckBox("Shift")
        self.layout.addWidget(self.shift_checkbox)
        self.alt_checkbox = QCheckBox("Alt")
        self.layout.addWidget(self.alt_checkbox)

        # Shortcut Input
        self.row_layout = QHBoxLayout()
        self.shortcut_label = QLabel("Key")
        self.shortcut_input = QLineEdit()
        self.shortcut_input.setFixedWidth(35)
        self.shortcut_input.setMaxLength(1)  # Only allow 1 character
        self.row_layout.addWidget(self.shortcut_input)
        self.row_layout.addWidget(self.shortcut_label)
        self.layout.addLayout(self.row_layout)
        
        # Initially hide checkboxes and input box
        self.showCustomInput(False)

        # Pushes everything to the top
        self.layout.addSpacerItem(QSpacerItem(150, 300, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.mouse_listener = MouseListener()
        self.listening_checkbox.stateChanged.connect(self.toggleListening)
        self.preset_dropdown.currentTextChanged.connect(self.presetChanged)
        self.ctrl_checkbox.stateChanged.connect(self.updateShortcut)
        self.shift_checkbox.stateChanged.connect(self.updateShortcut)
        self.alt_checkbox.stateChanged.connect(self.updateShortcut)
        self.shortcut_input.textChanged.connect(self.updateShortcut)

        self.shortcut = ""  # Shortcut to execute

    def update_checkbox_label(self):    
        if self.listening_checkbox.isChecked():
            self.listening_checkbox.setText("Listening!")
            self.listening_checkbox.setStyleSheet("color: white;")
        else:
            self.listening_checkbox.setText("Not Listening")
            self.listening_checkbox.setStyleSheet("color: red;")
    
    def showCustomInput(self, show):
        self.ctrl_checkbox.setVisible(show)
        self.shift_checkbox.setVisible(show)
        self.alt_checkbox.setVisible(show)
        self.shortcut_label.setVisible(show)
        self.shortcut_input.setVisible(show)
        
    def presetChanged(self, text):
        if text == 'custom':
            self.showCustomInput(True)
        else:
            self.showCustomInput(False)
        self.updateShortcut()

    def updateShortcut(self):
        preset = self.preset_dropdown.currentText()
        if preset != 'custom':
            self.shortcut = preset
        else:
            shortcut = ""
            if self.ctrl_checkbox.isChecked():
                shortcut += "ctrl+"
            if self.shift_checkbox.isChecked():
                shortcut += "shift+"
            if self.alt_checkbox.isChecked():
                shortcut += "alt+"
            shortcut += self.shortcut_input.text()
            self.shortcut = shortcut

    def toggleListening(self, state):
        if state == Qt.Checked:
            QApplication.instance().installEventFilter(self.mouse_listener)
            self.mouse_listener.mouseReleased.connect(self.simulateKeyPress)
        else:
            QApplication.instance().removeEventFilter(self.mouse_listener)
            self.mouse_listener.mouseReleased.disconnect(self.simulateKeyPress)

    def simulateKeyPress(self):
        # Get the widget under the cursor
        cursor_pos = QCursor.pos()
        widget_under_cursor = QApplication.widgetAt(cursor_pos)

        # Check if the widget under the cursor is a QOpenGLWidget, i.e. drawing surface
        if not isinstance(widget_under_cursor, QOpenGLWidget):
            return
        
        # Check if any modifier keys are pressed
        if QApplication.keyboardModifiers() & (Qt.ControlModifier | Qt.ShiftModifier | Qt.AltModifier):
            return
        
        shortcut = self.shortcut

        if shortcut:
            key_sequence = QKeySequence(shortcut)
            key_events = []

            # Break down the key sequence into individual key press and release events
            for key in range(key_sequence.count()):
                key_code = key_sequence[key] & ~Qt.KeyboardModifierMask
                modifiers = Qt.KeyboardModifiers(key_sequence[key] & Qt.KeyboardModifierMask)

                if modifiers & Qt.ControlModifier:
                    key_events.append(QKeyEvent(QEvent.KeyPress, Qt.Key_Control, Qt.ControlModifier))
                if modifiers & Qt.ShiftModifier:
                    key_events.append(QKeyEvent(QEvent.KeyPress, Qt.Key_Shift, Qt.ShiftModifier))
                if modifiers & Qt.AltModifier:
                    key_events.append(QKeyEvent(QEvent.KeyPress, Qt.Key_Alt, Qt.AltModifier))

                key_events.append(QKeyEvent(QEvent.KeyPress, key_code, modifiers))
                key_events.append(QKeyEvent(QEvent.KeyRelease, key_code, modifiers))

                if modifiers & Qt.ControlModifier:
                    key_events.append(QKeyEvent(QEvent.KeyRelease, Qt.Key_Control, Qt.ControlModifier))
                if modifiers & Qt.ShiftModifier:
                    key_events.append(QKeyEvent(QEvent.KeyRelease, Qt.Key_Shift, Qt.ShiftModifier))
                if modifiers & Qt.AltModifier:
                    key_events.append(QKeyEvent(QEvent.KeyRelease, Qt.Key_Alt, Qt.AltModifier))

            # Post the events
            for event in key_events:
                QGuiApplication.postEvent(QApplication.focusWidget(), event)
                 
            # Timeout to avoid multiple triggers for 1 stroke
            # TODO: find a more elegant solution
            QApplication.instance().removeEventFilter(self.mouse_listener)
            QTimer.singleShot(50, lambda: QApplication.instance().installEventFilter(self.mouse_listener))

    def canvasChanged(self, canvas):
        pass
