from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """ Signal bus """

    mica_enable_changed = pyqtSignal(bool)
    path2_download_signal = pyqtSignal(str)
    url2_download_signal = pyqtSignal(str)
    path2_upload_signal = pyqtSignal(str)
    log_signal = pyqtSignal(str)


signal_bus = SignalBus()
