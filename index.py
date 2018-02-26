# libs and modules needed in programe
import sys
import os
import urllib
import pafy  # youtube download
import humanize  # to convert units(computer units)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType


# ui file location
FORM_CLASS, _ = loadUiType(os.path.join(os.path.dirname('__file__'), "main.ui"))


# launching ui file defined above
class MainApp(QMainWindow, FORM_CLASS):  # QMainWindow refere to window type used in ui file
    # this is constructor
    threads=[]
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ui()
        self.actions()

    # methods to control ui elements , every self = QMainWindow
    def ui(self):
        self.setFixedSize(848, 663)
        QMessageBox.information(self,'Disclaimer',"This application is Beta version and may include some bugs ,please send me your feedback")

    def actions(self):
        self.pushButton.clicked.connect(self.download)
        self.pushButton_8.clicked.connect(self.download_vi)
        self.pushButton_12.clicked.connect(self.download_py)
        self.pushButton_2.clicked.connect(self.browse)
        self.pushButton_5.clicked.connect(self.browse_vi)
        self.pushButton_9.clicked.connect(self.browse_py)
        self.pushButton_13.clicked.connect(self.vi_information)
        self.pushButton_15.clicked.connect(self.clear_fn)
        self.radioButton_3.toggled.connect(self.radio_buttons)
        self.radioButton_2.toggled.connect(self.radio_buttons)
        self.radioButton.toggled.connect(self.radio_buttons)


    def clear_fn(self):
        self.comboBox_2.clear()
        self.lineEdit_4.setText('')
        self.lineEdit_3.setText('')

    def download(self):
        url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()
        if url=='' or save_location=='' :
            QMessageBox.warning(self,'Error','URL or save location is missing')
            return
        if url.startswith('https://www.youtube.com') :
            QMessageBox.information(self,'Content Error','Please provide youtube links in the next tab')
            self.lineEdit.setText('')
            return
        else :
            try:
                urllib.request.urlretrieve(url, save_location,
                                       self.progress_bar)  # save location is for ex : home/abdo/Desktop/"filename"
                self.pushButton.setEnabled(False)
                self.PushButton_2.setEnabled(False)
            except Exception:
                QMessageBox.warning(self, "Error", "Download failed")
                return
            QMessageBox.information(self, "Download completed", 'Download has been finished succfully')
            self.progressBar.setProperty("value", 0)
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lcdNumber_3.setProperty("value", 0)
            self.pushButton.setEnabled(True)
            self.PushButton_2.setEnabled(True)
    def download_vi(self):
        url = self.lineEdit_4.text()
        save_location = self.lineEdit_3.text()
        if url == "" or save_location == "":
            QMessageBox.warning(self, "Error", 'URL or Save location is missing ')
            return
        else:
            video = pafy.new(url)
            st = video.allstreams
            quality = self.comboBox_2.currentIndex()
            if quality == -1:
                QMessageBox.warning(self, "Error", 'Quality is missing ')
            else:
                self.pushButton_8.setEnabled(False)
                self.pushButton_13.setEnabled(False)
                self.pushButton_15.setEnabled(False)
                self.pushButton_5.setEnabled(False)
                self.comboBox_2.setEnabled(False)
                starting_download = st[quality].download(filepath=save_location, callback=self.vi_progress)
                QMessageBox.information(self, "Download completed", 'Download has been finished succfully')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
            self.comboBox_2.clear()
            self.progressBar_2.setProperty("value", 0)
            self.lcdNumber_7.setProperty("value", 0)
            self.pushButton_8.setEnabled(True)
            self.pushButton_13.setEnabled(True)
            self.pushButton_15.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.comboBox_2.setEnabled(True)

    def radio_buttons(self):
        if self.radioButton_3.isChecked():
            self.comboBox.clear()
            data=['m4a','webm']
            for x in data :
                self.comboBox.addItem(x)
        elif self.radioButton_2.isChecked():
            self.comboBox.clear()
            data=['mp4','webm']
            for y in data :
                self.comboBox.addItem(y)
        else :
            self.comboBox.clear()
            data=['mp4','3gp','webm']
            for z in data :
                self.comboBox.addItem(z)

    def download_py(self):
        url = self.lineEdit_6.text()
        save_location = self.lineEdit_5.text()
        if save_location==''or url=='':
            QMessageBox.warning(self,'Error','Save location or URL is missing')
            return
        else :
            os.chdir(save_location)
        if not url.startswith('https://www.youtube.com/watch?v=') :
            QMessageBox.warning(self,"Error",'Please provide only youtube links')
            self.lineEdit_6.setText('')
            return
        else :
            py = pafy.get_playlist(url)
            videos = py['items']
            try :
                os.mkdir(str(py['title']))
            except FileExistsError :
                QMessageBox.warning(self,'Error','There is a file in the same directory have same name of playlist folder,please change save location')
                self.lineEdit_5.setText('')
                save_location=''
                return
            folder = os.chdir(str(py['title']))
            self.pushButton_9.setEnabled(False)
            self.pushButton_12.setEnabled(False)
            self.radioButton.setEnabled(False)
            self.radioButton_2.setEnabled(False)
            self.radioButton_3.setEnabled(False)
            self.comboBox.setEnabled(False)
            if self.radioButton_3.isChecked():
                for au in videos:
                    p = au['pafy']
                    quality_text = self.comboBox.currentText()
                    quality=p.getbestaudio(preftype=quality_text)
                    download = quality.download(filepath=folder, callback=self.py_progress)
                    QApplication.processEvents()
            elif self.radioButton_2.isChecked():
                for au in videos:
                    p = au['pafy']
                    quality_text = self.comboBox.currentText()
                    quality = p.getbestvideo(preftype=quality_text)
                    download = quality.download(filepath=folder, callback=self.py_progress)
                    QApplication.processEvents()
            else :
                for au in videos:
                    p = au['pafy']
                    quality_text = self.comboBox.currentText()
                    quality = p.getbest(preftype=quality_text)
                    download = quality.download(filepath=folder, callback=self.py_progress)
                    QApplication.processEvents()
            QMessageBox.information(self, "Download completed", 'Download has been finished succfully')
            self.pushButton_9.setEnabled(True)
            self.pushButton_12.setEnabled(True)
            self.radioButton.setEnabled(True)
            self.radioButton_2.setEnabled(True)
            self.radioButton_3.setEnabled(True)
            self.comboBox.setEnabled(True)
            self.lineEdit_6.setText('')
            self.lineEdit_5.setText('')
            self.progressBar_3.setProperty('value',0)
            self.lcdNumber_10.setProperty('value',0)


    def vi_information(self):
        url = self.lineEdit_4.text()
        if not url.startswith('https://www.youtube.com/watch?v=') :
            QMessageBox.warning(self,"Error",'Please provide only youtube links')
            self.lineEdit_4.setText('')
            return
        else :
            try:
                video = pafy.new(url)
                st = video.allstreams
                for i in st:
                    size = humanize.naturalsize(i.get_filesize())
                    data = '{} {} {} {}'.format(i.mediatype, i.extension, i.quality,
                                            size)  # to satisfy addItem argument conditions
                    self.comboBox_2.addItem(data)
            except:
                QMessageBox.warning(self, "Error", 'Provide link first')

    def cancel(self):
        pass

    def pause(self):
        pass

    def browse(self):
        ls=[]
        url=self.lineEdit.text()
        ls.append(url.split('.'))
        ls=ls[0]
        vol=len(ls)
        if vol<4 :
            ex='All Files(*.*)'
            QMessageBox.information(self,'File Type','No extension detected')
        else :
            ex=ls[vol-1]
        # directory='.' to set default directory of any system , filter to get file types
        save_place = QFileDialog.getSaveFileName(self, caption='Save as', directory='.', filter=ex)
        # slicing to get path only
        name = str(save_place)  # because it's tuble by defult
        path = (name[2:].split(',')[0].replace("'", ""))
        self.lineEdit_2.setText(path)  # getting path to line edit box

    def browse_vi(self):
        try:
            save_location = QFileDialog.getExistingDirectory(self, "Select Directory", )  # save without name
        except:
            QMessageBox.warning(self, "Error", 'Please provide save location')
        self.lineEdit_3.setText(save_location)

    def browse_py(self):
        save_location = QFileDialog.getExistingDirectory(self, "Select Directory", )
        self.lineEdit_5.setText(save_location)

    def progress_bar(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize
        ls=[]
        if totalsize > 0:
            persent = (read * 100) / totalsize
            self.progressBar.setValue(persent)
            size=humanize.naturalsize(totalsize)
            sl=size.find('MB')
            vol=size[:sl-1]
            self.lcdNumber_3.setProperty("value", vol)
            QApplication.processEvents()  # for not responding problem (temprory solution)
    def vi_progress(self, total, recvd, ratio, rate, eta):
        if total > 0:
            self.progressBar_2.setValue(recvd * 100 / total)
            self.lcdNumber_7.setProperty('value', rate)
            QApplication.processEvents()

    def py_progress(self, total, recvd, ratio, rate, eta):
        if total > 0:
            self.progressBar_3.setValue(recvd * 100 / total)
            self.lcdNumber_10.setProperty('value', rate)
            QApplication.processEvents()


# openning ui window to user
def main():
    app = QApplication(sys.argv)
    window = MainApp()  # calling class of main window (first window)
    window.show()  # to show window
    app.exec_()  # infinit loop to make continous show for window


if __name__ == '__main__':
    main()
