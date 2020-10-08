from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QMessageBox
import requests
import xlrd
from requests.auth import HTTPBasicAuth


class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(800, 429)
        self.centralwidget = QtWidgets.QWidget(Main)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(9, 10, 781, 411))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(52, 10, 651, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("Enter your Instance URL")
        self.lineEdit.setToolTip('The URL of your Oracle Cloud service.\nFor example, https://servername.fa.us2.oraclecloud.com')  
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(52, 40, 300, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("Enter your username")
        self.lineEdit_2.setToolTip('Username for the Oracle Cloud service user having REST API and IT Security Manager accesses')  
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(52, 70, 300, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setPlaceholderText("Enter your password")
        self.lineEdit_3.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setToolTip('Password for the Oracle Cloud service user having REST API and IT Security Manager accesses')  
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(504, 50, 199, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.updatePasswords)
        self.progressBar = QtWidgets.QProgressBar(self.frame)
        #self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setGeometry(QtCore.QRect(52, 130, 691, 22))
        self.textBrowser = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser.setGeometry(QtCore.QRect(25, 180, 731, 192))
        self.textBrowser.setObjectName("textBrowser")
        Main.setCentralWidget(self.centralwidget)
        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("The user accounts have been updated")
        msg.setWindowTitle("Password updates successful")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def updatePasswords(self):
        self.progressBar.setProperty("value", 0)
        filename,_ = QFileDialog.getOpenFileName(None, 'Open File', '', ".xls(*.xls *.xlsx)")
        if 1==1:
            if filename is not None or len(filename)>=0:
                self.textBrowser.setText('Reading the file - ' + filename)
                self.progressBar.setProperty("value", 20)
                instanceURL = self.lineEdit.text()
                username = self.lineEdit_2.text()
                password = self.lineEdit_3.text()
                book = xlrd.open_workbook(filename)
                sheet = book.sheet_by_index(0)
                data = [[str(sheet.cell_value(r, c)) for c in range(sheet.ncols)] for r in range(sheet.nrows) if r!=0]
                self.progressBar.setProperty("value", 40)
                url = instanceURL + ':443/hcmRestApi/scim/Users?attributes=id,userName,displayName,active&filter='
                url2 = ''
                self.textBrowser.setText('Fetching user account info to update. This could take a moment. Please wait even if the title bar reads "Not Responding"')
                if len(data) == 1:
                    url2 = 'UserName eq ' + str(data[0][0])
                else:
                    for i in range(len(data)):
                        if i == len(data)-1:
                            url2 = url2 + 'Username eq "' + data[i][0] + '"'
                        else:
                            url2 = url2 + 'Username eq "' + data[i][0] + '" or '
                response = requests.request("GET", url+url2, auth = HTTPBasicAuth(username, password))
                if response.status_code == 200:
                    userResults = response.json()
                    urLen = len(userResults['Resources'])
                    up = dict()
                    self.progressBar.setProperty("value", 50)
                    for i in range(len(data)):
                        up[str(data[i][0]).lower()] = str(data[i][1])
                    dt = ''
                    self.progressBar.setProperty("value", 60)
                    print(up)
                    if urLen > 1:
                        for i in range(urLen):
                            if i == urLen-1:
                                dt = dt + ',{\"method\": \"PATCH\",\"path\": \"/Users/'+ userResults['Resources'][i]['id'] +'\",\"bulkId\": \"clientBulkId1\",\"data\": {\"schemas\": [\"urn:scim:schemas:core:2.0:User\"],\"active\": true,\"password\": \"' + up[userResults['Resources'][i]['userName'].lower()] + '\"}}]}'
                            elif i == 0:
                                dt = dt + '{\"Operations\": [{\"method\": \"PATCH\",\"path\": \"/Users/'+ userResults['Resources'][i]['id'] +'\",\"bulkId\": \"clientBulkId1\",\"data\": {\"schemas\": [\"urn:scim:schemas:core:2.0:User\"],\"active\": true,\"password\": \"' + up[userResults['Resources'][i]['userName'].lower()] + '\"}}'
                            else:
                                dt = dt + ',{\"method\": \"PATCH\",\"path\": \"/Users/'+ userResults['Resources'][i]['id'] +'\",\"bulkId\": \"clientBulkId1\",\"data\": {\"schemas\": [\"urn:scim:schemas:core:2.0:User\"],\"active\": true,\"password\": \"' + up[userResults['Resources'][i]['userName'].lower()] + '\"}}'
                    elif urLen == 1:
                        dt = dt + '{\"Operations\": [{\"method\": \"PATCH\",\"path\": \"/Users/'+ userResults['Resources'][0]['id'] +'\",\"bulkId\": \"clientBulkId1\",\"data\": {\"schemas\": [\"urn:scim:schemas:core:2.0:User\"],\"active\": true,\"password\": \"' + up[userResults['Resources'][i]['userName'].lower()] + '\"}}]}'

                    
                    self.textBrowser.setText('Updating passwords. This could take a moment. Please wait even if the title bar reads "Not Responding"')
                    url3 = instanceURL + "/hcmRestApi/scim/Bulk"
                    self.progressBar.setProperty("value", 70)
                    payload = dt
                    headers = {'content-type': 'application/json' }
                    r = requests.post(url3, auth=HTTPBasicAuth(username, password), headers=headers, data=payload)
                    print(r.status_code)
                    if r.status_code == 200:
                        self.progressBar.setProperty("value", 100)
                        finaltext = ''
                        try:
                            for resc in userResults['Resources']:
                                finaltext = finaltext + 'Password updated for ' + resc['displayName']  + ' (' + resc['userName'] + ')\n'
                        except:
                            finaltext = r.text
                        self.textBrowser.setText(finaltext)
                        self.showdialog()
                    elif r.status_code == 401:
                        self.textBrowser.setText('Authorization failed. Please validate the instance URL, Username and password (Basic Auth)')
                    elif r.status_code == 403:
                        self.textBrowser.setText('Insufficient privileges. Please ensure your user account has REST access (Workers, User accounts) and IT Security Manager privileges')
                    else:
                        self.textBrowser.setText('Unexpected1 error. This could due to your firewall or antivirus restricting network access to the application, the excel sheet, insufficient privileges, instance availability, etc. Please check your network status, excel, instance details and try again.')
                elif response.status_code == 401:
                    self.textBrowser.setText('Authorization failed. Please validate the instance URL, Username and password (Basic Auth)')
                elif response.status_code == 403:
                    self.textBrowser.setText('Insufficient privileges. Please ensure your user account has REST access (Workers, User accounts) and IT Security Manager privileges')
                else:
                    self.textBrowser.setText('Unexpected2 error. This could due to incorrect URL format, your firewall or antivirus restricting network access to the application, the excel sheet, insufficient privileges, instance availability, etc. Please check your network status, excel, instance details and try again.')

            else:
                self.textBrowser.setText('Please select a valid xlsx file containing 2 columns - UserName and Password only')
        else:
            self.textBrowser.setText('Unexpected error. This could due to your firewall or antivirus restricting network access to the application, the excel sheet, insufficient privileges, instance availability, etc. Please check your network status, excel, instance details and try again.')

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Fusion Password Manager", "Fusion Password Manager"))
        self.pushButton.setText(_translate("Fusion Password Manager", "Choose excel file and submit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Main = QtWidgets.QMainWindow()
    ui = Ui_Main()
    ui.setupUi(Main)
    Main.show()
    sys.exit(app.exec_())
