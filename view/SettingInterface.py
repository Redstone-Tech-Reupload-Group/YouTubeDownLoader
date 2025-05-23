from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel, QFileDialog
from qfluentwidgets import (
    ScrollArea,
    ExpandLayout,
    SettingCardGroup,
    PushSettingCard,
    SwitchSettingCard,
    ComboBoxSettingCard,
    InfoBar,
    CustomColorSettingCard,
    setThemeColor,
    OptionsSettingCard,
    setTheme,
    Theme,
)
from qfluentwidgets import FluentIcon as FIF

from common.Config import cfg
from common.MyWidget import RangeSettingCard, TextDialog, DistListSettingCard
from common.SignalBus import signal_bus
from common.Style import StyleSheet, MyIcon


class SettingInterface(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.scroll_area = ScrollArea(self)
        self.scroll_widget = QWidget(self)
        self.expand_layout = ExpandLayout(self.scroll_widget)

        self.title_label = QLabel(self.tr('Settings'), self)

        self.edit_setting_group = SettingCardGroup(self.tr('Download Setting'), self.scroll_widget)
        self.reprint_id_card = PushSettingCard(
            self.tr('Edit'), FIF.DOWNLOAD, self.tr('Reprinter ID'), cfg.get(cfg.reprint_id), self.edit_setting_group
        )
        self.proxy_enable = SwitchSettingCard(
            FIF.GLOBE,
            self.tr('Enable Proxy'),
            self.tr('Whether to enable web proxy'),
            configItem=cfg.proxy_enable,
            parent=self.edit_setting_group,
        )
        self.proxy_card = PushSettingCard(
            self.tr('Edit'), FIF.GLOBE, self.tr('Proxy Setting'), cfg.get(cfg.proxy), self.edit_setting_group
        )
        self.thread_card = RangeSettingCard(
            cfg.thread, MyIcon.NUMBER, self.tr('Number of threads'), parent=self.edit_setting_group
        )
        self.download_folder_card = PushSettingCard(
            self.tr('Choose folder'),
            FIF.FOLDER_ADD,
            self.tr('Download directory'),
            cfg.get(cfg.download_folder),
            self.edit_setting_group,
        )

        self.advanced_setting_group = SettingCardGroup(self.tr('Advanced setting'), self.scroll_widget)
        self.google_api_card = PushSettingCard(
            self.tr('Edit'),
            MyIcon.KEY,
            self.tr('Google Api Token'),
            str_encryption(cfg.get(cfg.api_token)),
            self.advanced_setting_group,
        )
        self.subscribe_channel_card = DistListSettingCard(
            cfg.subscribe_channels, self.tr('Subscribe Channels'), parent=self.advanced_setting_group
        )
        self.api_server_card = PushSettingCard(
            self.tr('Edit'), MyIcon.SERVER, self.tr('Api Server'), cfg.get(cfg.api_server), self.advanced_setting_group
        )

        self.system_setting_group = SettingCardGroup(self.tr('System Setting'), self.scroll_widget)
        self.theme_card = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('Application theme'),
            self.tr('Change the appearance of your application'),
            texts=[self.tr('Light'), self.tr('Dark'), self.tr('Use system setting')],
            parent=self.system_setting_group,
        )
        self.theme_color_card = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('Theme color'),
            self.tr('Change the theme color of you application'),
            self.system_setting_group,
        )
        self.mica_card = SwitchSettingCard(
            FIF.TRANSPARENT,
            self.tr('Mica effect'),
            self.tr('Apply semi transparent to windows and surfaces'),
            cfg.mica_enabled,
            self.system_setting_group,
        )
        self.language_card = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr('Language'),
            self.tr('Set your preferred language for UI'),
            texts=['简体中文', 'English', self.tr('Use system setting')],
            parent=self.system_setting_group,
        )

        self.setObjectName(text)
        self.init_layout()
        self.init_widget()
        self.connect_signal()

    def init_layout(self):
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_setting_group.addSettingCard(self.reprint_id_card)
        self.edit_setting_group.addSettingCard(self.proxy_enable)
        self.edit_setting_group.addSettingCard(self.proxy_card)
        self.edit_setting_group.addSettingCard(self.thread_card)
        self.edit_setting_group.addSettingCard(self.download_folder_card)

        self.advanced_setting_group.addSettingCard(self.google_api_card)
        self.advanced_setting_group.addSettingCard(self.subscribe_channel_card)
        self.advanced_setting_group.addSettingCard(self.api_server_card)

        self.system_setting_group.addSettingCard(self.theme_card)
        self.system_setting_group.addSettingCard(self.theme_color_card)
        self.system_setting_group.addSettingCard(self.mica_card)
        self.system_setting_group.addSettingCard(self.language_card)

        self.expand_layout.setSpacing(28)
        self.expand_layout.setContentsMargins(20, 10, 20, 0)
        self.expand_layout.addWidget(self.edit_setting_group)
        self.expand_layout.addWidget(self.advanced_setting_group)
        self.expand_layout.addWidget(self.system_setting_group)

    def init_widget(self):
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setViewportMargins(0, 10, 0, 20)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.scroll_area)

        self.set_qss()

    def set_qss(self):
        self.title_label.setObjectName('Title')
        self.scroll_widget.setObjectName('ScrollWidget')

        StyleSheet.SCROLL.apply(self)

    def connect_signal(self):
        cfg.appRestartSig.connect(self.show_restart_tooltip)
        cfg.themeChanged.connect(self.on_theme_changed)

        self.reprint_id_card.clicked.connect(self.on_reprint_id_card_clicked)
        self.download_folder_card.clicked.connect(self.on_download_folder_card_clicked)
        self.proxy_card.clicked.connect(self.on_proxy_card_clicked)

        self.google_api_card.clicked.connect(self.on_google_api_card_clicked)
        self.api_server_card.clicked.connect(self.on_api_server_card_clicked)

        self.theme_color_card.colorChanged.connect(setThemeColor)
        self.mica_card.checkedChanged.connect(signal_bus.mica_enable_changed)

    def show_restart_tooltip(self):
        """show restart tooltip"""
        InfoBar.warning('', self.tr('Configuration takes effect after restart'), parent=self.window())

    def on_theme_changed(self, theme: Theme):
        """theme changed slot"""
        setTheme(theme)

        self.set_qss()

    def on_reprint_id_card_clicked(self):
        w = TextDialog(self.tr('Nick Name'), self.tr('please input your nick name:'), cfg.get(cfg.reprint_id), self)
        w.setTitleBarVisible(False)
        if w.exec():
            cfg.set(cfg.reprint_id, w.input_edit.text())
            self.reprint_id_card.setContent(w.input_edit.text())
        else:
            print('Cancel button is pressed')

    def on_proxy_card_clicked(self):
        w = TextDialog(self.tr('Proxy Setting'), self.tr('manual proxy configuration:'), cfg.get(cfg.proxy), self)
        w.setTitleBarVisible(False)
        if w.exec():
            cfg.set(cfg.proxy, w.input_edit.text())
            self.proxy_card.setContent(w.input_edit.text())
        else:
            print('Cancel button is pressed')

    def on_google_api_card_clicked(self):
        w = TextDialog(
            self.tr('API Token Setting'), self.tr('set your google develop token:'), cfg.get(cfg.api_token), self
        )
        w.setTitleBarVisible(False)
        if w.exec():
            cfg.set(cfg.api_token, w.input_edit.text())
            self.google_api_card.setContent(str_encryption(w.input_edit.text()))
        else:
            print('Cancel button is pressed')

    def on_api_server_card_clicked(self):
        w = TextDialog(self.tr('API Server'), self.tr('manual your server address:'), cfg.get(cfg.api_server), self)
        w.setTitleBarVisible(False)
        if w.exec():
            cfg.set(cfg.api_server, w.input_edit.text())
            self.api_server_card.setContent(w.input_edit.text())
        else:
            print('Cancel button is pressed')

    def on_download_folder_card_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, self.tr('Choose folder'), './')
        if not folder or cfg.get(cfg.download_folder) == folder:
            return

        print(folder)
        cfg.set(cfg.download_folder, folder)
        self.download_folder_card.setContent(folder)


def str_encryption(text: str):
    if len(text) == 0:
        return ''
    else:
        return text[:3] + '***' + text[-3:]
