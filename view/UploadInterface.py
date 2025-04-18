import json
import os
import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget, QSizePolicy, QHBoxLayout, QFileDialog
from qfluentwidgets import TextEdit, ScrollArea, ExpandLayout, LineEdit, ToolButton, PrimaryPushButton, InfoBar
from qfluentwidgets import FluentIcon as FIF

from common.Config import cfg, SUCCESS, WARNING
from common.MyThread import Upload
from common.MyWidget import UploadCard
from common.SignalBus import signal_bus
from common.Style import StyleSheet


class UploadInterface(QFrame):
    _videos = []

    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.upload_thread = None

        self.layout = QVBoxLayout(self)
        self.scroll_area = ScrollArea(self)
        self.scroll_widget = QWidget(self)
        self.expand_layout = ExpandLayout(self.scroll_widget)

        self.title_label = QLabel(self.tr('Upload'), self)

        self.video_title_label = QLabel(self.tr('Video Title'), self.scroll_widget)
        self.video_title_input = LineEdit(self.scroll_widget)

        self.cover_label = QLabel(self.tr('Cover'), self.scroll_widget)
        self.cover_path_input = LineEdit(self.scroll_widget)
        self.cover_path_btn = ToolButton(FIF.FOLDER, self.scroll_widget)

        self.widget_3 = QWidget(self.scroll_widget)
        self.video_label = QLabel(self.tr('Video'), self.scroll_widget)
        self.video_card_view = QWidget(self.scroll_widget)
        self.video_card_layout = QVBoxLayout()
        self.add_video_btn = ToolButton(FIF.FOLDER_ADD, self.scroll_widget)

        self.reprint_info_label = QLabel(self.tr('Source'), self.scroll_widget)
        self.reprint_info_input = LineEdit(self.scroll_widget)

        self.tag_label = QLabel(self.tr('Tag'), self.scroll_widget)
        self.tag_input = LineEdit(self.scroll_widget)

        self.video_description_label = QLabel(self.tr('Description'), self.scroll_widget)
        self.video_description_input = TextEdit(self.scroll_widget)

        self.dynamic_label = QLabel(self.tr('Dynamic'), self.scroll_widget)
        self.dynamic_input = LineEdit(self.scroll_widget)

        self.upload_btn = PrimaryPushButton(self.tr('Upload'), self.scroll_widget, FIF.SEND)

        self.log_output = TextEdit(self)

        self.setObjectName(text)
        self.init_layout()
        self.init_widget()
        self.connect_signal()

    def init_widget(self):
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setViewportMargins(0, 10, 0, 20)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        widget_1 = QWidget(self.scroll_widget)
        layout_1 = QHBoxLayout()
        layout_1.setContentsMargins(5, 0, 0, 0)
        self.video_title_label.setFixedWidth(85)
        layout_1.addWidget(self.video_title_label, stretch=1)
        layout_1.addWidget(self.video_title_input, stretch=6)
        widget_1.setLayout(layout_1)
        widget_1.setFixedHeight(35)
        self.expand_layout.addWidget(widget_1)

        widget_2 = QWidget(self.scroll_widget)
        layout_2 = QHBoxLayout()
        layout_2.setContentsMargins(5, 0, 0, 0)
        self.cover_label.setFixedWidth(85)
        layout_2.addWidget(self.cover_label, stretch=1)
        layout_2.addWidget(self.cover_path_input, stretch=5)
        layout_2.addWidget(self.cover_path_btn, stretch=1)
        widget_2.setLayout(layout_2)
        widget_2.setFixedHeight(35)
        self.expand_layout.addWidget(widget_2)

        layout_3 = QHBoxLayout()
        layout_3.setContentsMargins(5, 0, 0, 0)
        self.video_label.setFixedWidth(85)
        layout_3.addWidget(self.video_label, stretch=1, alignment=Qt.AlignmentFlag.AlignTop)
        layout_3.addWidget(self.video_card_view, stretch=6, alignment=Qt.AlignmentFlag.AlignTop)
        self.video_card_layout.addWidget(self.add_video_btn, alignment=Qt.AlignmentFlag.AlignRight)
        self.widget_3.setLayout(layout_3)
        self.widget_3.setFixedHeight(35)
        self.expand_layout.addWidget(self.widget_3)

        widget_4 = QWidget(self.scroll_widget)
        layout_4 = QHBoxLayout()
        layout_4.setContentsMargins(5, 0, 0, 0)
        self.reprint_info_label.setFixedWidth(85)
        layout_4.addWidget(self.reprint_info_label, stretch=1)
        layout_4.addWidget(self.reprint_info_input, stretch=6)
        widget_4.setLayout(layout_4)
        widget_4.setFixedHeight(35)
        self.expand_layout.addWidget(widget_4)

        widget_5 = QWidget(self.scroll_widget)
        layout_5 = QHBoxLayout()
        layout_5.setContentsMargins(5, 0, 0, 0)
        self.tag_label.setFixedWidth(85)
        layout_5.addWidget(self.tag_label, stretch=1)
        layout_5.addWidget(self.tag_input, stretch=6)
        widget_5.setLayout(layout_5)
        widget_5.setFixedHeight(35)
        self.expand_layout.addWidget(widget_5)

        widget_6 = QWidget(self.scroll_widget)
        layout_6 = QHBoxLayout()
        layout_6.setContentsMargins(5, 0, 0, 0)
        self.video_description_label.setFixedWidth(85)
        layout_6.addWidget(self.video_description_label, stretch=1, alignment=Qt.AlignmentFlag.AlignTop)
        layout_6.addWidget(self.video_description_input, stretch=6, alignment=Qt.AlignmentFlag.AlignTop)
        self.video_description_input.setStyleSheet("font-size: 12px;font-family: 'Segoe UI', 'Microsoft YaHei';")
        self.video_description_input.setFixedHeight(240)
        widget_6.setLayout(layout_6)
        widget_6.setFixedHeight(250)
        self.expand_layout.addWidget(widget_6)

        widget_7 = QWidget(self.scroll_widget)
        layout_7 = QHBoxLayout()
        layout_7.setContentsMargins(5, 0, 0, 0)
        self.dynamic_label.setFixedWidth(85)
        layout_7.addWidget(self.dynamic_label, stretch=1)
        layout_7.addWidget(self.dynamic_input, stretch=6)
        widget_7.setLayout(layout_7)
        widget_7.setFixedHeight(35)
        self.expand_layout.addWidget(widget_7)

        widget_8 = QWidget(self.scroll_widget)
        layout_8 = QHBoxLayout()
        layout_8.setContentsMargins(5, 0, 0, 0)
        layout_8.addWidget(self.upload_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        widget_8.setLayout(layout_8)
        widget_8.setFixedHeight(35)
        self.expand_layout.addWidget(widget_8)

        self.log_output.setFixedHeight(100)
        self.log_output.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.log_output.setStyleSheet("font-size: 12px;font-family: 'Segoe UI', 'Microsoft YaHei';")
        self.log_output.setReadOnly(True)

    def init_layout(self):
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video_card_view.setLayout(self.video_card_layout)
        self.video_card_layout.setSpacing(5)
        self.video_card_layout.setContentsMargins(0, 0, 0, 0)

        self.expand_layout.setSpacing(10)
        self.expand_layout.setContentsMargins(15, 0, 30, 0)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.log_output)

        self.set_qss()

    def init_text(self, path: str):
        data_file = os.path.join(path, 'data.json')
        with open(data_file, 'r') as f:
            data_contents = json.loads(f.read())
            self.video_title_input.setText(data_contents['title'])
            self.reprint_info_input.setText(data_contents['reprint'])
            self.video_description_input.setText(data_contents['description'])

        self.cover_path_input.setText(os.path.join(path, 'cover.jpg'))
        uploader = data_contents['uploader']
        self.tag_input.setText(f'游戏,单机游戏,MC,youtube,minecraft,{uploader}')
        for file in os.listdir(path):
            if file.endswith('.mp4') or file.endswith('.mkv'):
                video_path = os.path.join(path, file)
                self.add_video(video_path)

    def add_video(self, path):
        name = os.path.splitext(os.path.split(path)[1])[0]
        route_key = re.findall(r'\[(.*?)]', name)[-1]
        video = {'name': name, 'route_key': route_key, 'path': path}
        if video not in self._videos:
            self._videos.append(video)

            card = UploadCard(video['name'], video['path'], self.scroll_widget)
            card.setObjectName(video['route_key'])
            card.del_signal.connect(self.del_video)
            self.video_card_layout.addWidget(card)

            self.adjust_size()
        else:
            return

    def del_video(self, route_key):
        card = self.video_card_view.findChild(UploadCard, route_key, options=Qt.FindChildOption.FindDirectChildrenOnly)
        if card is not None:
            card.deleteLater()
            self._videos = [video for video in self._videos if video['route_key'] != route_key]
            self.adjust_size()

    def adjust_size(self):
        count = len(self._videos)
        if count == 0:
            self.video_card_view.setFixedHeight(35)
            self.widget_3.setFixedHeight(35)
        else:
            self.video_card_view.setFixedHeight(count * 85 + 45)
            self.widget_3.setFixedHeight(count * 85 + 45)

        self.video_card_layout.update()
        self.video_card_view.update()
        self.scroll_widget.update()
        self.update()

    def set_qss(self):
        self.title_label.setObjectName('Title')
        self.scroll_widget.setObjectName('ScrollWidget')
        self.video_title_label.setObjectName('Text')
        self.cover_label.setObjectName('Text')
        self.video_label.setObjectName('Text')
        self.reprint_info_label.setObjectName('Text')
        self.tag_label.setObjectName('Text')
        self.video_description_label.setObjectName('Text')
        self.dynamic_label.setObjectName('Text')

        StyleSheet.SAMPLE.apply(self)

    def connect_signal(self):
        self.cover_path_btn.clicked.connect(self.on_cover_path_btn_clicked)
        self.add_video_btn.clicked.connect(self.on_add_video_btn_clicked)
        self.upload_btn.clicked.connect(self.on_upload_btn_clicked)
        signal_bus.log_signal.connect(self.log_update)

    def on_cover_path_btn_clicked(self):
        options = QFileDialog().options()
        options.filter = 'JPEG files (*.jpg)'
        file_name, _ = QFileDialog.getOpenFileName(
            None, 'Choose Image File', cfg.get(cfg.download_folder), 'Image files (*.jpg *.png *.bmp)', options=options
        )
        self.cover_path_input.setText(file_name)

    def on_add_video_btn_clicked(self):
        dialog = QFileDialog()
        dialog.setNameFilter(self.tr('MP4 files (*.mp4)'))
        file_name, _ = dialog.getOpenFileName(
            None, 'Choose Image File', cfg.get(cfg.download_folder), 'Video files (*.mp4)'
        )

        self.add_video(file_name)

    def on_upload_btn_clicked(self):
        cookie_file = os.path.join('config', 'cookies.json')
        if not os.path.exists(cookie_file):
            self.show_finish_tooltip(self.tr('no cookies found'), WARNING)
            return

        with open(cookie_file, 'r') as f:
            cookie_contents = json.loads(f.read())

        sessdata = ''
        bili_jct = ''
        dedeuserid_ckmd5 = ''
        dedeuserid = ''
        access_token = ''

        if 'cookie_info' in cookie_contents:
            cookies = cookie_contents['cookie_info']['cookies']
            for cookie in cookies:
                if cookie['name'] == 'SESSDATA':
                    sessdata = cookie['value']
                elif cookie['name'] == 'bili_jct':
                    bili_jct = cookie['value']
                elif cookie['name'] == 'DedeUserID__ckMd5':
                    dedeuserid_ckmd5 = cookie['value']
                elif cookie['name'] == 'DedeUserID':
                    dedeuserid = cookie['value']
        else:
            self.show_finish_tooltip(self.tr('no cookies found'), WARNING)

        if 'token_info' in cookie_contents:
            access_token = cookie_contents['token_info']['access_token']
        else:
            self.show_finish_tooltip(self.tr('no cookies found'), WARNING)

        login_access = {
            'cookies': {
                'SESSDATA': sessdata,
                'bili_jct': bili_jct,
                'DedeUserID__ckMd5': dedeuserid_ckmd5,
                'DedeUserID': dedeuserid,
            },
            'access_token': access_token,
        }

        if len(self._videos) == 0:
            self.show_finish_tooltip(self.tr('no videos, plead add video first!'), WARNING)
        video_list = []
        for video_info in self._videos:
            card = self.video_card_view.findChild(
                UploadCard, video_info['route_key'], options=Qt.FindChildOption.FindDirectChildrenOnly
            )
            title = 'part'
            if card is not None:
                title = card.title_input.text()
                part_info = {'name': title, 'path': video_info['path']}
                video_list.append(part_info)

            if self.upload_thread and self.upload_thread.isRunning():
                return

            info = {
                'title': self.video_title_input.text(),
                'desc': self.video_description_input.toPlainText(),
                'source': self.reprint_info_input.text(),
                'tag': self.tag_input.text().split(','),
                'dynamic': self.dynamic_input.text(),
                'cover_path': self.cover_path_input.text(),
            }

            self.upload_thread = Upload(login_access, info, video_list)
            self.upload_thread.finish_signal.connect(self.upload_done)
            self.upload_thread.start()

    def log_update(self, text):
        self.log_output.append(text)

    def upload_done(self):
        self.show_finish_tooltip('upload done!', SUCCESS)

    def show_finish_tooltip(self, text, tool_type: int):
        """ show restart tooltip """
        if tool_type == SUCCESS:
            InfoBar.success('', text, parent=self.window(), duration=5000)
        elif tool_type == WARNING:
            InfoBar.warning('', text, parent=self.window(), duration=5000)
