from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QLabel, QGridLayout, QHBoxLayout, QSizePolicy, QStackedWidget, \
    QSpacerItem
from qfluentwidgets import ScrollArea, ExpandLayout, SegmentedWidget, LineEdit, PushButton, TextEdit, PrimaryPushButton

from common.Style import StyleSheet


class ToolInterface(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)

        self.title_label = QLabel(self.tr("Tools"), self)

        self.pivot = SegmentedWidget(self)
        self.stacked_widget = QStackedWidget(self)
        self.layout = QVBoxLayout(self)

        self.song_interface = VideoTransInterface(self)
        self.album_interface = QLabel('Album Interface', self)

        self.init_ui()
        self.setObjectName(text)

    def init_ui(self):
        self.title_label.setAlignment(Qt.AlignHCenter)

        self.add_sub_interface(self.song_interface, 'songInterface', 'Song')
        self.add_sub_interface(self.album_interface, 'albumInterface', 'Album')

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.pivot)
        self.layout.addWidget(self.stacked_widget)
        self.layout.setContentsMargins(20, 10, 20, 10)

        self.stacked_widget.currentChanged.connect(self.on_current_index_changed)
        self.stacked_widget.setCurrentWidget(self.song_interface)
        self.pivot.setCurrentItem(self.song_interface.objectName())

        self.set_qss()

    def set_qss(self):
        self.title_label.setObjectName('Title')

        StyleSheet.SAMPLE.apply(self)

    def add_sub_interface(self, widget: QWidget, object_name, text):
        widget.setObjectName(object_name)
        self.stacked_widget.addWidget(widget)
        self.pivot.addItem(
            routeKey=object_name,
            text=text,
            onClick=lambda: self.stacked_widget.setCurrentWidget(widget),
        )

    def on_current_index_changed(self, index):
        widget = self.stacked_widget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())


class VideoTransInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QVBoxLayout(self)

        self.input_label = QLabel(self.tr('Input Path'), self)
        self.input_path = LineEdit(self)

        self.output_label = QLabel(self.tr('Output Path'), self)
        self.output_path = LineEdit(self)

        self.start_btn = PrimaryPushButton(self.tr('Start'), self)

        self.log_output = TextEdit(self)

        self.init_ui()
        self.set_qss()

    def init_ui(self):
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(15, 5, 15, 10)

        widget_1 = QWidget()
        layout_1 = QHBoxLayout()
        layout_1.setContentsMargins(0, 15, 0, 5)
        layout_1.addWidget(self.input_label, stretch=1)
        layout_1.addWidget(self.input_path, stretch=5)
        widget_1.setLayout(layout_1)
        self.main_layout.addWidget(widget_1)

        widget_2 = QWidget()
        layout_2 = QHBoxLayout()
        layout_2.setContentsMargins(0, 5, 0, 5)
        layout_2.addWidget(self.output_label, stretch=1)
        layout_2.addWidget(self.output_path, stretch=5)
        widget_2.setLayout(layout_2)
        self.main_layout.addWidget(widget_2)

        widget_3 = QWidget()
        layout_3 = QHBoxLayout()
        layout_3.setContentsMargins(0, 5, 0, 5)
        layout_3.addWidget(QLabel(), stretch=3)
        layout_3.addWidget(self.start_btn, stretch=1)
        widget_3.setLayout(layout_3)
        self.main_layout.addWidget(widget_3)

        self.main_layout.addSpacerItem(QSpacerItem(40, 40))

        # self.log_output.setFixedHeight(100)
        self.log_output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.log_output)
        self.log_output.setStyleSheet('font-size: 12px;font-family: \'Segoe UI\', \'Microsoft YaHei\';')
        self.log_output.setReadOnly(True)

        self.setLayout(self.main_layout)

    def set_qss(self):
        self.input_label.setObjectName('Text')
        self.output_label.setObjectName('Text')

        StyleSheet.CARD_INF.apply(self)
