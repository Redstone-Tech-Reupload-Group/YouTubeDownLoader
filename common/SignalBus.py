from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    """ Signal bus """

    mica_enable_changed = Signal(bool)
    path2_download_signal = Signal(str)
    url2_download_signal = Signal(str)
    path2_upload_signal = Signal(str)
    log_signal = Signal(str)


signal_bus = SignalBus()
