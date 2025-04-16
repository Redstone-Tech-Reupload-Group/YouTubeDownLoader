from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QFileDialog
from qfluentwidgets import ToolButton, LineEdit, PrimaryPushButton, TextEdit, InfoBar

from qfluentwidgets import FluentIcon as FIF

from common.Config import cfg, SUCCESS, WARNING
from common.MyWidget import FileLineEdit
from common.Style import StyleSheet


class VideoTransInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.convert_process = None
        self.main_layout = QVBoxLayout(self)

        self.input_label = QLabel(self.tr('Input Path'), self)
        self.input_path = FileLineEdit(self)
        self.input_btn = ToolButton(FIF.FOLDER, self)

        self.output_label = QLabel(self.tr('Output Path'), self)
        self.output_path = LineEdit(self)

        self.start_btn = PrimaryPushButton(self.tr('Start'), self)

        self.log_output = TextEdit(self)

        self.init_ui()
        self.connect_signal()
        self.set_qss()

    def init_ui(self):
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(15, 5, 15, 10)

        widget_1 = QWidget()
        layout_1 = QHBoxLayout()
        layout_1.setContentsMargins(0, 15, 0, 5)
        self.input_path.setDragEnabled(True)
        self.input_path.setAcceptDrops(True)
        layout_1.addWidget(self.input_label, stretch=1)

        widget_1_1 = QWidget()
        layout_1_1 = QHBoxLayout()
        layout_1_1.setContentsMargins(0, 15, 0, 5)
        layout_1_1.addWidget(self.input_path, stretch=5)
        layout_1_1.addWidget(self.input_btn, stretch=1)
        widget_1_1.setLayout(layout_1_1)

        layout_1.addWidget(widget_1_1, stretch=5)
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

        self.log_output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.log_output)
        self.log_output.setReadOnly(True)

        self.setLayout(self.main_layout)

    def set_qss(self):
        self.input_label.setObjectName('Text')
        self.output_label.setObjectName('Text')

        StyleSheet.CARD_INF.apply(self)

    def connect_signal(self):
        self.input_btn.clicked.connect(self.on_input_btn_clicked)
        self.start_btn.clicked.connect(self.convert_video)

    def on_input_btn_clicked(self):
        options = QFileDialog.Options()
        options.filter = 'VIDEO files (*.mp4)'
        file, _ = QFileDialog.getOpenFileName(None, 'Choose Video File', cfg.get(cfg.download_folder),
                                              'Video files (*.mp4)', options=options)
        self.input_path.setText(file)
        self.output_path.setText(file[:-4] + '_yuv420p.mp4')

    def convert_video(self):
        if self.input_path.text() == '' or self.output_path.text() == '':
            self.show_finish_tooltip(self.tr('input or output can not be empty'), WARNING)
            return

        if self.convert_process is None:
            self.convert_process = QProcess()
            self.convert_process.readyReadStandardOutput.connect(self.handle_stdout)
            self.convert_process.readyReadStandardError.connect(self.handle_stderr)
            self.convert_process.finished.connect(self.convert_finished)
            self.convert_process.start("ffmpeg", ['-y', '-i',
                                                  self.input_path.text(),
                                                  '-vf', 'format=yuv420p',
                                                  self.output_path.text()])
        else:
            self.show_finish_tooltip(self.tr('process is running, please wait until it done.'), WARNING)

    def handle_stderr(self):
        data = self.convert_process.readAllStandardError()
        stderr = bytes(data).decode('utf8')
        self.log_update(stderr)

    def handle_stdout(self):
        data = self.convert_process.readAllStandardOutput()
        stdout = bytes(data).decode('utf8')
        self.log_update(stdout)

    def log_update(self, text):
        self.log_output.append(text)

    def convert_finished(self):
        self.log_update('done')
        self.show_finish_tooltip(self.tr('convert done'), SUCCESS)
        self.convert_process = None

    def show_finish_tooltip(self, text, tool_type: int):
        if tool_type == SUCCESS:
            InfoBar.success('', text, parent=self.window(), duration=6000)
        elif tool_type == WARNING:
            InfoBar.warning('', text, parent=self.window(), duration=6000)
