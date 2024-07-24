
import requests;
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(820, 571)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 20, 47, 13))
        self.label.setObjectName("label")
        self.inputArea = QtWidgets.QLineEdit(Dialog)
        self.inputArea.setGeometry(QtCore.QRect(100, 9, 361, 31))
        self.inputArea.setObjectName("inputArea")
        self.FindBTN = QtWidgets.QPushButton(Dialog)
        self.FindBTN.setGeometry(QtCore.QRect(480, 20, 75, 23))
        self.FindBTN.setObjectName("FindBTN")
        self.FindBTN.clicked.connect(self.getIP) #get Ip funtion name
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(40, 110, 751, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 170, 47, 21))
        self.label_2.setObjectName("label_2")
        self.resultarea = QtWidgets.QTextBrowser(Dialog)
        self.resultarea.setGeometry(QtCore.QRect(40, 200, 531, 341))
        self.resultarea.setObjectName("resultarea")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


         #make function
    def getIP(self):
        #take input text from input field
        ipp = str(self.inputArea.text())
        #here is API url
        linkURl = "https://api.techniknews.net/ipgeo/"
        try:
            respond = requests.get(linkURl+ipp).json()
            ip = respond['ip']
            status = respond['status']
            continent = respond['continent']
            country = respond['country']
            countryCode = respond['countryCode']
            regionName = respond['regionName']
            city = respond['city']
            zip = respond['zip']
            lat = respond['lat']
            lon = respond['lon']
            timezone = respond['timezone']
            currency = respond['currency']
            isp = respond['isp']
            org = respond['org']
            mobile = respond['mobile']
            proxy = respond['proxy']

            finalResult = f'IP : {ip}\nStatus : {status}\nContinent : {continent}\nCountry : {country}\nCountryCode : {countryCode}\nRegionName : {regionName}\nCity : {city}\nZip : {zip}\nLat : {lat}\nLon : {lon}\nTimezone : {timezone}\nCurrency : {currency}\nIsp : {isp}\nOrg : {org}\nMobile : {mobile}\nProxy : {proxy}\n\n'

            # now set the result in result area
            self.resultarea.setText(finalResult)
        except:
            finalResult = "Not found . Try another IP"    
            self.resultarea.setText(finalResult)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Enter Ip"))
        self.FindBTN.setText(_translate("Dialog", "Find"))
        self.label_2.setText(_translate("Dialog", "Details"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

