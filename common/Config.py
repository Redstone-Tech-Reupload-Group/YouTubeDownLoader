import sys
import time
from enum import Enum

from PyQt5.QtCore import QLocale
from qfluentwidgets import qconfig, OptionsConfigItem, OptionsValidator, QConfig, ConfigItem, \
    RangeConfigItem, RangeValidator, BoolValidator, ConfigSerializer, FolderValidator, Theme

from Path import BASE_DIR

VERSION = '6.4.1'
LICENCE_PATH = f'{BASE_DIR}/res/LICENCE.html'

LOG_PATH = 'log'
LOG_NAME = time.strftime("%Y-%m-%d", time.localtime())

INFO = 0
SUCCESS = 1
WARNING = 2


class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


def is_win11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    reprint_id = ConfigItem(
        'DownloadSetting', 'Reprint', ''
    )
    proxy_enable = ConfigItem(
        "DownloadSetting", "EnableProxy", True, BoolValidator())

    proxy = ConfigItem(
        'DownloadSetting', 'Proxy', 'http://127.0.0.1:1080'
    )
    thread = RangeConfigItem(
        "DownloadSetting", "Thread", 4, RangeValidator(1, 16))
    download_folder = ConfigItem(
        "DownloadSetting", "DownloadFolder", "download", FolderValidator())
    auto_quality = ConfigItem(
        "DownloadSetting", "AutoQuality", True, BoolValidator())

    api_token = ConfigItem(
        "AdvancedSetting", "ApiToken", "", restart=True
    )
    subscribe_channels = ConfigItem(
        "AdvancedSetting", "SubscribeChannels", [])
    api_server = ConfigItem(
        "AdvancedSetting", "ApiServer", "", restart=True
    )

    compress_video = ConfigItem(
        "VideoSetting", "CompressVideo", True, BoolValidator()
    )

    mica_enabled = ConfigItem("System", "MicaEnabled", is_win11(), BoolValidator())
    language = OptionsConfigItem(
        "System", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)


cfg = Config()
qconfig.load(f'config/config.json', cfg)
