
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from qt_material import apply_stylesheet
from pathlib import Path
import sys
import os

# Create a variable

app = QApplication(sys.argv)
app.setApplicationName("Webin")
app.setStyleSheet(open("App/qt-webin/br_style_webin.css", "r").read())
apply_stylesheet(app, theme='un')

PROXY = 'Temp'

# main window
class MainWindow(QMainWindow):
    
    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('App/icon.ico'))  
        # creating a tab widget
        self.tabs = QTabWidget()
 
        # making document mode true
        self.tabs.setDocumentMode(True)
 
        # adding action when double clicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
 
        # adding action when tab is changed
        self.tabs.currentChanged.connect(self.current_tab_changed)
 
        # making tabs closeable
        self.tabs.setTabsClosable(True)
 
        # adding action when tab close is requested
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
 
        # making tabs as central widget
        self.setCentralWidget(self.tabs)
 
        # creating a status bar
        self.status = QStatusBar()
 
        # setting status bar to the main window
        self.setStatusBar(self.status)
 
        # creating a tool bar for navigation
        navtb = QToolBar("Навигация")
 
        # adding tool bar tot he main window
        self.addToolBar(navtb)
 
        # creating back action
        back_btn = QAction("Назад", self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)
 
        next_btn = QAction("Вперед", self)
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)
 
        reload_btn = QAction("Перезагрузить", self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
 
        home_btn = QAction("Домой", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)
 
        navtb.addSeparator()
 
        self.urlbar = QLineEdit()
 
        self.urlbar.returnPressed.connect(self.navigate_to_url)
 
        navtb.addWidget(self.urlbar)
 
        stop_btn = QAction("Стоп", self)
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        theme_br_btn = QAction("Тема", self)
        theme_br_btn.triggered.connect(self.cssfile)
        navtb.addAction(theme_br_btn)

        sp_btn = QAction("Программа", self)
        sp_btn.triggered.connect(self.sp_btn_fn)
        navtb.addAction(sp_btn)

        about_btn = QAction("Новая Страница", self)
        about_btn.triggered.connect(lambda:self.add_new_tab(QUrl('http://www.google.com'), 'Новая Страница'))
        navtb.addAction(about_btn)
 
        self.add_new_tab(QUrl('http://www.google.com'), 'Домашняя Страница')
 
        self.show()
 
        self.setWindowTitle("Webin")

    def downloadRequested(self, download):
        old_path = download.url().path()  # download.path()
        suffix = QtCore.QFileInfo(old_path).suffix()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", old_path, "" + suffix
        )
        if path:
            download.setPath(path)
            download.accept()
    def cssfile(self):
        filename, ok = QFileDialog.getOpenFileName(self,"Выбор Файла", "D:\\icons\\avatar\\", "Стили (*.css *.qss *.xml)")
        if filename:
            path = Path(filename)
            try:
                apply_stylesheet(app, theme=filename)
            except:
                app.setStyleSheet(open(filename, "r").read())

                

    def sp_btn_fn(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Версия Webin")
        dlg.setText("Webin \nВерсия Core 23H2 \nДвижок PyQt \nMade By NL \n\nWebinbr.tilda.ws                          ")
        button = dlg.exec()

        if button == QMessageBox.Ok:
            print("Диалог Закрыт")

    def add_new_tab(self, qurl = None, label ="Открытие..."):
 
        if qurl is None:
            qurl = QUrl('http://www.google.com')
 
        browser = QWebEngineView()
 
        browser.setUrl(qurl)
        browser.page().profile().downloadRequested.connect(self.downloadRequested)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
 
        browser.urlChanged.connect(lambda qurl, browser = browser:
                                   self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                     self.tabs.setTabText(i, browser.page().title()))
 
    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()
 
    def current_tab_changed(self, i):
 
        # get the curl
        qurl = self.tabs.currentWidget().url()
 
        # update the url
        self.update_urlbar(qurl, self.tabs.currentWidget())
 
        # update the title
        self.update_title(self.tabs.currentWidget())
 
    # when tab is closed
    def close_current_tab(self, i):
 
        # if there is only one tab
        if self.tabs.count() < 2:
            # do nothing
            return
 
        # else remove the tab
        self.tabs.removeTab(i)
 
    # method for updating the title
    def update_title(self, browser):
 
        # if signal is not from the current tab
        if browser != self.tabs.currentWidget():
            # do nothing
            return
 
        # get the page title
        title = self.tabs.currentWidget().page().title()
 
        # set the window title
        self.setWindowTitle("% s  \ Webin " % title)
 
    # action to go to home
    def navigate_home(self):
 
        # go to google
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))
 
    # method for navigate to url
    def navigate_to_url(self):
 
        # get the line edit text
        # convert it to QUrl object
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            # set scheme
            q.setScheme("http")
 
        # set the url
        self.tabs.currentWidget().setUrl(q)
 
    # method to update the url
    def update_urlbar(self, q, browser = None):
 
        # If this signal is not from the current tab, ignore
        if browser != self.tabs.currentWidget():
 
            return
 
        # set text to the url bar
        self.urlbar.setText(q.toString())
 
        # set cursor position
        self.urlbar.setCursorPosition(0)
window = MainWindow()

app.exec_()

