from random import random
from qtpy.QtGui import (QColor, QMouseEvent)
from qtpy.QtCore import (Qt, Signal)
from qtpy.QtWidgets import (QWidget, QSpacerItem, QCheckBox, QHBoxLayout,
                            QSizePolicy, QPushButton, QColorDialog)
from config import color_palette


class ColorButton(QPushButton):
    """Custom button to allow the user to select a color. The default
    color is a random bright color.

    Left-clicking opens a color dialog box to choose a color.
    Right-clicking resets the color to the default."""

    color_changed = Signal(QColor)

    def __init__(self, *args, color=None, index=-1, **kwargs):
        super().__init__(*args, **kwargs)
        if not color:
            if index >= 0:
                color = self.index_color(index)
            else:
                color = self.random_color()
        elif not isinstance(color, QColor):
            color = QColor(color)

        self._color = None
        self._default = color
        self.dialog_box = QColorDialog(self)
        self.dialog_box.setCurrentColor(color)

        self.pressed.connect(self.dialog_box.show)
        self.dialog_box.colorSelected.connect(lambda c: setattr(self, 'color', c))

        self.color = self._default

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color: QColor):
        """Set the background color of the button to the selected color."""
        if color == self._color:
            return

        self._color = color
        style_str = "ColorButton {background-color: " + self._color.name() + "};"
        self.setStyleSheet(style_str)

        self.color_changed.emit(color)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.RightButton:
            self.color = self._default
            return

        return super().mousePressEvent(e)

    @staticmethod
    def random_color():
        """Pick a random color for the default color of each PV. This
        function ensures that the color is bright, since it will be on a
        black background."""
        h = int(360 * random())
        s = int(256 * (0.5 + random()/2.0))
        l = int(256 * (0.4 + random()/5.0))
        color = QColor()
        color.setHsl(h, s, l)
        return color

    @staticmethod
    def index_color(index):
        modded_index = index % len(color_palette)
        color = color_palette[modded_index]

        dark_factor = (index // len(color_palette)) * 35
        return color.darker(100 + dark_factor)



class CenterCheckbox(QWidget):
    toggled = Signal(bool)
    def __init__(self, parent, init_data=True):
        super().__init__(parent)

        self.check_box = QCheckBox(parent)
        self.check_box.setChecked(init_data)
        self.check_box.toggled.connect(self.toggled)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))
        layout.addWidget(self.check_box)
        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.setLayout(layout)

    @property
    def checkState(self):
        return self.check_box.isChecked()

    @checkState.setter
    def checkState(self, state):
        self.check_box.setChecked(state)
