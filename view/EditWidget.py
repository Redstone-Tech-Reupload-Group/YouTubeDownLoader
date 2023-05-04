from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QWidget, QSizePolicy, QHBoxLayout
from qfluentwidgets import LineEdit, PushButton, ToolButton, SwitchButton, TextEdit
from qfluentwidgets import FluentIcon as FIF


class EditWidget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.main_layout = QGridLayout(self)
        self.title_label = QLabel(self.tr('edit_title'), self)

        self.origin_link_label = QLabel(self.tr('origin_link'), self)
        self.origin_link_input = LineEdit(self)

        self.auto_quality_label = QLabel(self.tr('auto_quality'), self)
        self.auto_quality_btn = SwitchButton()
        self.quality_label = QLabel(self.tr('quality'), self)
        self.quality_input = LineEdit(self)
        self.get_quality_btn = ToolButton(FIF.SEARCH, self)

        self.get_info_btn = PushButton(self.tr('get_info'), self, FIF.MESSAGE)
        self.download_btn = PushButton(self.tr('download_video'), self, FIF.DOWNLOAD)

        self.video_title_label = QLabel(self.tr('video_title'), self)
        self.video_title_input = LineEdit(self)
        self.copy_title_btn = ToolButton(FIF.COPY, self)

        self.reprint_info_label = QLabel(self.tr('reprint_info'), self)
        self.reprint_info_input = LineEdit(self)
        self.copy_reprint_btn = ToolButton(FIF.COPY, self)

        self.video_description_input = TextEdit(self)

        self.play_btn = ToolButton(FIF.VIDEO, self)
        self.copy_btn = ToolButton(FIF.COPY, self)
        self.link_btn = ToolButton(FIF.GLOBE, self)
        self.folder_btn = ToolButton(FIF.FOLDER, self)

        self.log_output = TextEdit(self)

        self.init_ui()
        self.setObjectName(text)

    def init_ui(self):
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(20, 5, 20, 5)
        for i in range(9):
            self.main_layout.setColumnStretch(i, 1)
            self.main_layout.setRowStretch(i, 0)
        self.main_layout.setRowStretch(6, 1)
        self.main_layout.setRowStretch(7, 1)
        self.main_layout.setRowStretch(8, 1)

        self.title_label.setMargin(10)
        self.main_layout.addWidget(self.title_label, 0, 0, 1, 9, Qt.AlignCenter)

        widget_1 = QWidget()
        layout_1 = QHBoxLayout()
        layout_1.setContentsMargins(0, 5, 0, 5)
        self.origin_link_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout_1.addWidget(self.origin_link_label, stretch=1)
        layout_1.addWidget(self.origin_link_input, stretch=6)
        widget_1.setLayout(layout_1)
        self.main_layout.addWidget(widget_1, 1, 0, 1, 9)

        widget_2 = QWidget()
        layout_2 = QGridLayout()
        # layout_2.setSpacing(0)
        layout_2.setContentsMargins(0, 0, 0, 5)
        self.quality_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout_2.addWidget(self.auto_quality_label, 0, 0, Qt.AlignLeft)
        layout_2.addWidget(self.auto_quality_btn, 0, 1, Qt.AlignLeft)
        layout_2.addWidget(self.quality_label, 0, 3, Qt.AlignCenter)
        layout_2.addWidget(self.quality_input, 0, 4, 1, 2)
        layout_2.addWidget(self.get_quality_btn, 0, 6)
        widget_2.setLayout(layout_2)
        self.main_layout.addWidget(widget_2, 2, 0, 1, 9)

        self.main_layout.addWidget(self.get_info_btn, 3, 2, 1, 2, Qt.AlignHCenter)
        self.main_layout.addWidget(self.download_btn, 3, 5, 1, 2, Qt.AlignHCenter)

        widget_3 = QWidget()
        layout_3 = QHBoxLayout()
        layout_3.setContentsMargins(0, 15, 0, 5)
        layout_3.addWidget(self.video_title_label, stretch=1)
        layout_3.addWidget(self.video_title_input, stretch=6)
        layout_3.addWidget(self.copy_title_btn, stretch=1)
        widget_3.setLayout(layout_3)
        self.main_layout.addWidget(widget_3, 4, 0, 1, 9)
        self.video_title_input.setText('【MC】【】')

        widget_4 = QWidget()
        layout_4 = QHBoxLayout()
        layout_4.setContentsMargins(0, 0, 0, 5)
        layout_4.addWidget(self.reprint_info_label, stretch=1)
        layout_4.addWidget(self.reprint_info_input, stretch=6)
        layout_4.addWidget(self.copy_reprint_btn, stretch=1)
        widget_4.setLayout(layout_4)
        self.main_layout.addWidget(widget_4, 5, 0, 1, 9)
        self.reprint_info_input.setText('转自 有能力请支持原作者')

        self.video_description_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.video_description_input, 6, 0, 3, 9)
        self.video_description_input.setStyleSheet('font-size: 12px;font-family: \'Segoe UI\', \'Microsoft YaHei\';')
        self.video_description_input.setText(
            '作者：\r\n发布时间：\r\n搬运：\r\n视频摘要：\r\n原简介翻译：\r\n存档：\r\n其他外链：')

        widget_5 = QWidget()
        layout_5 = QHBoxLayout()
        layout_5.setContentsMargins(0, 5, 0, 15)
        layout_5.addWidget(self.play_btn, stretch=1)
        layout_5.addWidget(self.copy_btn, stretch=1)
        layout_5.addWidget(self.link_btn, stretch=1)
        layout_5.addWidget(self.folder_btn, stretch=1)
        widget_5.setLayout(layout_5)
        self.main_layout.addWidget(widget_5, 9, 0, 1, 9)

        self.log_output.setFixedHeight(100)
        self.log_output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_layout.addWidget(self.log_output, 10, 0, 2, 9)
        self.log_output.setStyleSheet('font-size: 12px;font-family: \'Segoe UI\', \'Microsoft YaHei\';')
        self.log_output.setReadOnly(True)

        self.setLayout(self.main_layout)

        self.set_qss()

    def set_qss(self):
        self.title_label.setObjectName('Title')
        self.origin_link_label.setObjectName('Text')
        self.auto_quality_label.setObjectName('Text')
        self.quality_label.setObjectName('Text')
        self.video_title_label.setObjectName('Text')
        self.reprint_info_label.setObjectName('Text')

        with open(f'res/qss/light/edit_widget.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())