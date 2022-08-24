# -*- coding: utf-8 -*-
## @package proxen.gui
# @brief The GUI app main window implementation -- see MainWindow class.
import utils
from PySide6 import QtCore, QtWidgets, QtWebEngineCore, QtNetwork, QtWebEngineWidgets
from PySide6.QtCore import Signal, Slot
# from PySide6.QtGui import QAction

# ******************************************************************************** #
# GLOBALS

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"

# ******************************************************************************** #
# *****          WebInterceptoraddMainLayout
# ******************************************************************************** #

class WebInterceptor(QtWebEngineCore.QWebEngineUrlRequestInterceptor):

    def __init__(self, parent: QtCore.QObject = None):
        super().__init__(parent)
        utils.log('+ WebInterceptor CREATED')

    def interceptRequest(self, info: QtWebEngineCore.QWebEngineUrlRequestInfo):
        if info.resourceType() == QtWebEngineCore.QWebEngineUrlRequestInfo.ResourceTypeScript:
            utils.log(f'INTERCEPTED [SCRIPT] :: {info.requestUrl().url()}')

# ******************************************************************************** #
# *****          WebPage
# ******************************************************************************** #     

class WebPage(QtWebEngineCore.QWebEnginePage):

    def __init__(self, profile: QtWebEngineCore.QWebEngineProfile, parent: QtCore.QObject = None):
        super().__init__(profile, parent)
        self.setAudioMuted(True)
        self.initialize()
        utils.log('+ WebPage CREATED')

    def initialize(self):
        self.interceptor = WebInterceptor(self)
        # self.profile().setHttpUserAgent(USER_AGENT)
        self.profile().setUrlRequestInterceptor(self.interceptor)

        self.settings().setAttribute(QtWebEngineCore.QWebEngineSettings.PluginsEnabled, True)
        self.settings().setAttribute(QtWebEngineCore.QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QtWebEngineCore.QWebEngineSettings.JavascriptCanOpenWindows, True)
        self.settings().setAttribute(QtWebEngineCore.QWebEngineSettings.JavascriptCanAccessClipboard, True)
        self.settings().setAttribute(QtWebEngineCore.QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        self.settings().setAttribute(QtWebEngineCore.QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QtWebEngineCore.QWebEngineSettings.LocalStorageEnabled, True)
        # self.settings().setAttribute(QtWebEngineCore.QWebEngineSettings.AllowRunningInsecureContent, True)
        # self.settings().setAttribute(QtWebEngineCore.QWebEngineSettings.AutoLoadImages, false)

        self.initCookies()

        # self.initPageWatcher()
        # self.profile().clearHttpCache()
        # self.profile().setHttpCacheType(QtWebEngineCore.QWebEngineProfile.HttpCacheType.NoCache)

        self.proxyAuthenticationRequired.connect(self.on_proxyAuthenticationRequired)

    def initCookies(self):
        store = self.profile().cookieStore()
        store.cookieAdded.connect(self.on_cookieAdded)
        store.loadAllCookies()

    @Slot(QtCore.QUrl, QtNetwork.QAuthenticator, str)
    def on_proxyAuthenticationRequired(self, requestUrl: QtCore.QUrl, authenticator: QtNetwork.QAuthenticator, proxyHost: str):
        utils.log('Request proxy authentication', 'debug')
        proxy = QtNetwork.QNetworkProxy.applicationProxy()
        authenticator.setUser(proxy.user())
        authenticator.setPassword(proxy.password())

    @Slot(QtNetwork.QNetworkCookie)
    def on_cookieAdded(self, cookie: QtNetwork.QNetworkCookie):
        utils.log(f'COOKIE ADDED :: {cookie.name()} {cookie.value()} {cookie.domain()} ; requested_url: {self.requestedUrl()}', 'debug')

# ******************************************************************************** #
# *****          MainWindow
# ******************************************************************************** #

## The application's main GUI interface to control the system proxy settings.
class MainWindow(QtWidgets.QMainWindow):

    ## Gets the application instance.
    # @returns `QtWidgets.QApplication` the application instance
    @staticmethod
    def get_app(args):
        try:
            app = QtWidgets.QApplication.instance()
            if app is None:
                app = QtWidgets.QApplication(args)
            return app
        except:
            return QtWidgets.QApplication(args)

    def __init__(self, url: QtCore.QUrl):
        super().__init__()
        self.progress = 0
        self.url = url
        # QtWebEngineCore.QWebEngineProfile.defaultProfile().setHttpUserAgent(USER_AGENT)
        self.profile = QtWebEngineCore.QWebEngineProfile('qtsample')
        self.web_page = WebPage(self.profile, self)
        self.view = QtWebEngineWidgets.QWebEngineView(self)

        # URL input
        self.locationEdit = QtWidgets.QLineEdit(self)
        self.locationEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, self.locationEdit.sizePolicy().verticalPolicy())
        self.locationEdit.returnPressed.connect(self.changeLocation)

        # connect signals
        self.view.loadProgress.connect(self.on_view_loadProgress)
        self.view.loadFinished.connect(self.on_view_loadFinished)
        self.view.titleChanged.connect(self.on_view_titleChanged)

        # set page
        self.view.setPage(self.web_page)
        # load URL
        self.view.load(self.url)
        
        # toolbar
        self.toolbar = self.addToolBar('Navigation')
        self.toolbar.addAction(self.view.pageAction(QtWebEngineCore.QWebEnginePage.Back))
        self.toolbar.addAction(self.view.pageAction(QtWebEngineCore.QWebEnginePage.Forward))
        self.toolbar.addAction(self.view.pageAction(QtWebEngineCore.QWebEnginePage.Reload))
        self.toolbar.addAction(self.view.pageAction(QtWebEngineCore.QWebEnginePage.Stop))
        self.toolbar.addWidget(self.locationEdit)

        self.setCentralWidget(self.view)

    @Slot()
    def changeLocation(self):
        self.url = QtCore.QUrl.fromUserInput(self.locationEdit.text())
        self.view.load(self.url)
        self.view.setFocus()

    @Slot(bool)
    def on_view_loadFinished(self, finished: bool):
        self.progress = 100
        self.on_view_titleChanged(self.view.title())
        self.locationEdit.setText(self.view.url().toString())

    @Slot(str)
    def on_view_titleChanged(self, title: str):
        if self.progress > 0 and self.progress < 100:
            title = f'{title} ({self.progress}%)'
        self.setWindowTitle(title)

    @Slot(int)
    def on_view_loadProgress(self, progress: int):
        self.progress = progress
        self.on_view_titleChanged(self.view.title())
