from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QFileDialog
from qfluentwidgets import ToolButton, LineEdit, PrimaryPushButton, TextEdit, InfoBar, SwitchButton

from qfluentwidgets import FluentIcon as FIF

from common.Config import cfg, SUCCESS, WARNING
from common.MyWidget import FileLineEdit
from common.Style import StyleSheet


class SubtitleWrapInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.wrap_process = None
        self.main_layout = QVBoxLayout(self)

        self.video_input_label = QLabel(self.tr('Video Path'), self)
        self.video_input_path = FileLineEdit(self)
        self.video_input_btn = ToolButton(FIF.FOLDER, self)

        self.sub_input_label = QLabel(self.tr('Subtitle Path'), self)
        self.sub_input_path = FileLineEdit(self)
        self.sub_input_btn = ToolButton(FIF.FOLDER, self)

        self.output_label = QLabel(self.tr('Output Path'), self)
        self.output_path = LineEdit(self)

        self.quality_btn = SwitchButton(self)
        self.quality_label = QLabel(self.tr('Compress at Sametime'))
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
        self.video_input_path.setDragEnabled(True)
        self.video_input_path.setAcceptDrops(True)
        layout_1.addWidget(self.video_input_label, stretch=1)

        widget_1_1 = QWidget()
        layout_1_1 = QHBoxLayout()
        layout_1_1.setContentsMargins(0, 0, 0, 0)
        layout_1_1.addWidget(self.video_input_path, stretch=5)
        layout_1_1.addWidget(self.video_input_btn, stretch=1)
        widget_1_1.setLayout(layout_1_1)

        layout_1.addWidget(widget_1_1, stretch=5)
        widget_1.setLayout(layout_1)
        self.main_layout.addWidget(widget_1)

        widget_2 = QWidget()
        layout_2 = QHBoxLayout()
        layout_2.setContentsMargins(0, 5, 0, 5)
        layout_2.addWidget(self.sub_input_label, stretch=1)

        widget_2_1 = QWidget()
        layout_2_1 = QHBoxLayout()
        layout_2_1.setContentsMargins(0, 0, 0, 0)
        self.sub_input_path.setDragEnabled(True)
        self.sub_input_path.setAcceptDrops(True)
        layout_2_1.addWidget(self.sub_input_path, stretch=5)
        layout_2_1.addWidget(self.sub_input_btn, stretch=1)
        widget_2_1.setLayout(layout_2_1)

        layout_2.addWidget(widget_2_1, stretch=5)
        widget_2.setLayout(layout_2)
        self.main_layout.addWidget(widget_2)

        widget_3 = QWidget()
        layout_3 = QHBoxLayout()
        layout_3.setContentsMargins(0, 5, 0, 5)
        layout_3.addWidget(self.output_label, stretch=1)
        layout_3.addWidget(self.output_path, stretch=5)
        widget_3.setLayout(layout_3)
        self.main_layout.addWidget(widget_3)

        widget_4 = QWidget()
        layout_4 = QHBoxLayout()
        layout_4.setContentsMargins(0, 5, 0, 5)
        layout_4.addWidget(self.quality_label, stretch=1)
        self.quality_btn.setChecked(cfg.get(cfg.compress_video))
        layout_4.addWidget(self.quality_btn)
        layout_4.addWidget(QLabel(' '), stretch=1)
        layout_4.addWidget(self.start_btn, stretch=1)
        widget_4.setLayout(layout_4)
        self.main_layout.addWidget(widget_4)

        self.main_layout.addSpacerItem(QSpacerItem(40, 40))

        self.log_output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.log_output)
        self.log_output.setReadOnly(True)

        self.setLayout(self.main_layout)

    def set_qss(self):
        self.video_input_label.setObjectName('Text')
        self.sub_input_label.setObjectName('Text')
        self.output_label.setObjectName('Text')
        self.quality_label.setObjectName('Text')

        StyleSheet.CARD_INF.apply(self)

    def connect_signal(self):
        self.video_input_btn.clicked.connect(self.choose_video)
        self.sub_input_btn.clicked.connect(self.choose_subtitle)
        self.quality_btn.checkedChanged.connect(self.quality_btn_changed)
        self.start_btn.clicked.connect(self.wrap_subtitle)

    def choose_video(self):
        options = QFileDialog.Options()
        options.filter = 'Video files (*.mp4)'
        file, _ = QFileDialog.getOpenFileName(None, 'Choose Video File', cfg.get(cfg.download_folder),
                                              'Video files (*.mp4)', options=options)
        self.video_input_path.setText(file)
        self.output_path.setText(file[:-4] + '_x264.mp4')

    def choose_subtitle(self):
        options = QFileDialog.Options()
        options.filter = 'Subtitle files (*.ass *.srt)'
        file, _ = QFileDialog.getOpenFileName(None, 'Choose Subtitle File', cfg.get(cfg.download_folder),
                                              'Subtitle files (*.ass *.srt)', options=options)
        self.sub_input_path.setText(file)

    def quality_btn_changed(self, is_checked: bool):
        cfg.set(cfg.compress_video, is_checked)

    # ffmpeg -i input.mp4 -vf subtitles=sub.ass -c:v libx264 -crf 22.5 -preset ultrafast -movflags +faststart -c:a copy output.mp4
    def wrap_subtitle(self):
        if self.wrap_process is None:
            self.wrap_process = QProcess()
            self.wrap_process.readyReadStandardOutput.connect(self.handle_stdout)
            self.wrap_process.readyReadStandardError.connect(self.handle_stderr)
            self.wrap_process.finished.connect(self.convert_finished)

            sub_path = self.sub_input_path.text().replace('\\', '\\\\').replace(':', '\\:')
            if cfg.get(cfg.compress_video):
                args = ['-y', '-i', self.video_input_path.text(),
                        '-vf', f'subtitles=\'{sub_path}\'', '-c:v', 'libx264',
                        '-crf', '22.5', '-preset', 'ultrafast', '-movflags', '+faststart',
                        '-c:a', 'copy', self.output_path.text()]
            else:
                args = ['-y', '-i', self.video_input_path.text(),
                        '-vf', f'subtitles=\'{sub_path}\'',
                        self.output_path.text()]

            self.wrap_process.start("ffmpeg", args)
        else:
            self.show_finish_tooltip(self.tr('process is running, please wait until it done.'), WARNING)

    def handle_stderr(self):
        data = self.wrap_process.readAllStandardError()
        stderr = bytes(data).decode('utf8')
        self.log_update(stderr)

    def handle_stdout(self):
        data = self.wrap_process.readAllStandardOutput()
        stdout = bytes(data).decode('utf8')
        self.log_update(stdout)

    def log_update(self, text):
        self.log_output.append(text)

    def convert_finished(self):
        self.log_update('done')
        self.show_finish_tooltip(self.tr('convert done'), SUCCESS)
        self.wrap_process = None

    def show_finish_tooltip(self, text, tool_type: int):
        if tool_type == SUCCESS:
            InfoBar.success('', text, parent=self.window(), duration=6000)
        elif tool_type == WARNING:
            InfoBar.warning('', text, parent=self.window(), duration=6000)
