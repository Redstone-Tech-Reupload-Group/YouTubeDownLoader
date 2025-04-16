import ctypes
import logging
import os
import sys

from PySide6.QtCore import QSize, QTranslator, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import (
    NavigationItemPosition,
    FluentTranslator,
    Dialog,
    SplashScreen,
    FluentWindow
)
from qfluentwidgets import FluentIcon as FIF

from Path import BASE_DIR
from common.Config import cfg, VERSION, LOG_PATH, LOG_NAME
from common.SignalBus import signal_bus
from common.Style import MyIcon
from view.DownloadInterface import DownloadInterface
from view.InfoInterface import InfoInterface
from view.LocalVideoInterface import LocalVideoInterface
from view.SettingInterface import SettingInterface
from view.SubscribeInterface import SubscribeInterface
from view.TodoListInterface import TodoListInterface
from view.ToolInterface import ToolInterface
from view.UploadInterface import UploadInterface


class Window(FluentWindow):
    def __init__(self):
        super().__init__()
        self.init_window()

        self.download_interface = DownloadInterface('edit_interface', self)
        self.upload_interface = UploadInterface('upload_interface', self)
        self.local_video_interface = LocalVideoInterface('local_video_interface', self)
        self.subscribe_interface = SubscribeInterface('subscribe_interface', self)
        self.todo_list_interface = TodoListInterface('todo_list_interface', self)
        self.tool_interface = ToolInterface('tool_interface', self)

        self.info_interface = InfoInterface('info_interface', self)
        self.setting_interface = SettingInterface('setting_interface', self)

        self.navigationInterface.setAcrylicEnabled(True)

        self.init_navigation()

        self.connect_signal()
        self.splash_screen.finish()

    def init_navigation(self):

        self.addSubInterface(self.download_interface, FIF.EDIT, self.tr('Download'))
        self.addSubInterface(self.upload_interface, FIF.SEND, self.tr('Upload'))
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.local_video_interface, FIF.HISTORY, self.tr('Local Video'), pos)
        self.addSubInterface(self.subscribe_interface, FIF.RINGER, self.tr('Subscription Information'), pos)
        self.addSubInterface(self.todo_list_interface, FIF.FEEDBACK, self.tr('Todo List'), pos)
        self.addSubInterface(self.tool_interface, MyIcon.TOOL, self.tr('Tool'), pos)

        self.addSubInterface(self.info_interface, FIF.INFO, self.tr('About'), position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.setting_interface, FIF.SETTING, self.tr('Setting'),
                             position=NavigationItemPosition.BOTTOM)

        self.navigationInterface.setExpandWidth(200)

    def init_window(self):
        self.resize(650, 750)
        self.setWindowIcon(QIcon(f'{BASE_DIR}/res/icons/logo.ico'))
        self.setWindowTitle('YoutubeDownloader V' + VERSION)

        self.setMicaEffectEnabled(cfg.get(cfg.mica_enabled))

        self.splash_screen = SplashScreen(self.windowIcon(), self)
        self.splash_screen.setIconSize(QSize(106, 106))
        self.splash_screen.raise_()

        desktop = QApplication.primaryScreen().availableGeometry()
        _w, _h = desktop.width(), desktop.height()
        self.move(_w // 2 - self.width() // 2, _h // 2 - self.height() // 2)

        self.show()
        QApplication.processEvents()

    def connect_signal(self):
        signal_bus.mica_enable_changed.connect(self.setMicaEffectEnabled)
        signal_bus.path2_download_signal.connect(self.local2_download)
        signal_bus.url2_download_signal.connect(self.url2_download)
        signal_bus.path2_upload_signal.connect(self.path2_upload)

    def local2_download(self, path):
        self.download_interface.update_ui(path)
        self.switch_to(self.download_interface)

    def url2_download(self, url):
        self.download_interface.set_url(url)
        self.switch_to(self.download_interface)

    def path2_upload(self, path):
        self.upload_interface.init_text(path)
        self.switch_to(self.upload_interface)

    def switch_to(self, widget):
        self.stackedWidget.setCurrentWidget(widget)
        self.navigationInterface.setCurrentItem(widget.objectName())

    def switch_to_subscribe(self):
        if cfg.get(cfg.api_token) == '':
            dialog = Dialog(
                self.tr('No API Token!'),
                self.tr('You haven\'t set your token yet, please go to the settings screen to set it first'),
                self.window())
            dialog.setTitleBarVisible(False)
            if dialog.exec():
                self.switch_to(self.setting_interface)
            else:
                self.switch_to(self.download_interface)
        else:
            self.switch_to(self.subscribe_interface)

    def switch_to_todo(self):
        if cfg.get(cfg.api_server) == '':
            dialog = Dialog(
                self.tr('No API Server!'),
                self.tr('You haven\'t set api server yet, please go to the settings screen to set it first'),
                self.window())
            dialog.setTitleBarVisible(False)
            if dialog.exec():
                self.switch_to(self.setting_interface)
            else:
                self.switch_to(self.download_interface)
        else:
            self.switch_to(self.todo_list_interface)

    def on_current_interface_changed(self, index):
        widget = self.stack_widget.widget(index)
        self.navigation_interface.setCurrentItem(widget.objectName())


class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a', encoding='utf-8')

    def write(self, message):
        try:
            self.terminal.write(message)
            self.terminal.flush()
            self.log.write(message)
            self.log.flush()
        except Exception as e:
            print(str(e))

    def debug(self, message):
        self.terminal.write('[debug]' + message + '\n')
        self.terminal.flush()
        self.log.write('[debug]' + message + '\n')
        self.log.flush()

    def warning(self, message):
        self.terminal.write('[warning]' + message + '\n')
        self.terminal.flush()
        self.log.write('[warning]' + message + '\n')
        self.log.flush()

    def error(self, message):
        self.terminal.write('[error]' + message + '\n')
        self.terminal.flush()
        self.log.write('[error]' + message + '\n')
        self.log.flush()

    def isatty(self):
        return False

    def flush(self):
        pass


def hideConsole():
    """
    Hides the console window in GUI mode. Necessary for frozen application, because
    this application support both, command line processing AND GUI mode and theirfor
    cannot be run via pythonw.exe.
    """

    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        # if you wanted to close the handles...
        # ctypes.windll.kernel32.CloseHandle(whnd)


if __name__ == '__main__':
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)

    sys.stdout = Logger(LOG_PATH + '/' + LOG_NAME + '.log', sys.stdout)
    sys.stderr = Logger(LOG_PATH + '/' + LOG_NAME + '.log', sys.stderr)

    logging.basicConfig(filename=LOG_PATH + '/' + LOG_NAME + '.log', level=logging.INFO)

    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)

    # internationalization
    locale = cfg.get(cfg.language).value
    fluentTranslator = FluentTranslator(locale)
    settingTranslator = QTranslator()
    settingTranslator.load(locale, '', '', f'{BASE_DIR}/res/lang')

    app.installTranslator(fluentTranslator)
    app.installTranslator(settingTranslator)

    w = Window()
    w.show()

    hideConsole()

    app.exec()
