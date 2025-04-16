from PySide6.QtCore import Qt

from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QLabel, QStackedWidget
from qfluentwidgets import SegmentedWidget

from common.Style import StyleSheet
from view.pivots.SubtitleWrapInterface import SubtitleWrapInterface
from view.pivots.VideoTransInterface import VideoTransInterface


class ToolInterface(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)

        self.title_label = QLabel(self.tr('Tools'), self)

        self.pivot = SegmentedWidget(self)
        self.stacked_widget = QStackedWidget(self)
        self.layout = QVBoxLayout(self)

        self.color_space_interface = VideoTransInterface(self)
        self.subtitle_interface = SubtitleWrapInterface(self)

        self.init_ui()
        self.setObjectName(text)

    def init_ui(self):
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.add_sub_interface(self.color_space_interface, 'ColorSpaceInterface', self.tr('Convert Color Space'))
        self.add_sub_interface(self.subtitle_interface, 'SubtitleInterface', self.tr('Wrap Subtitle'))

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.pivot)
        self.layout.addWidget(self.stacked_widget)
        self.layout.setContentsMargins(20, 10, 20, 10)

        self.stacked_widget.currentChanged.connect(self.on_current_index_changed)
        self.stacked_widget.setCurrentWidget(self.color_space_interface)
        self.pivot.setCurrentItem(self.color_space_interface.objectName())

        self.set_qss()

    def set_qss(self):
        self.title_label.setObjectName('Title')

        StyleSheet.SAMPLE.apply(self)

    def add_sub_interface(self, widget: QWidget, object_name, text):
        widget.setObjectName(object_name)
        self.stacked_widget.addWidget(widget)
        self.pivot.addItem(
            routeKey=object_name, text=text, onClick=lambda: self.stacked_widget.setCurrentWidget(widget)
        )

    def on_current_index_changed(self, index):
        widget = self.stacked_widget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
