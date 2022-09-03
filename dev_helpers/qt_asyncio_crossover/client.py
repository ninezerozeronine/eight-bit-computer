#!/usr/bin/env python

"""
https://programtalk.com/vs2/?source=python/13971/PyQt4/examples/network/fortuneclient.py 
"""
 
#############################################################################
##
## Copyright (C) 2010 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the docameentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSsatUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################
 
import json

from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
 
class Client(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
 
        self.blockSize = 0
        self.currentFortune = ''
 
        hostLabel = QtWidgets.QLabel("Server name:")
        portLabel = QtWidgets.QLabel("Server port:")
 
        self.hostLineEdit = QtWidgets.QLineEdit('Localhost')
        self.portLineEdit = QtWidgets.QLineEdit()
        self.portLineEdit.setValidator(QtGui.QIntValidator(1, 65535, self))
 
        hostLabel.setBuddy(self.hostLineEdit)
        portLabel.setBuddy(self.portLineEdit)
 
        self.statusLabel = QtWidgets.QLabel("This examples requires that you run "
                "the Fortune Server example as well.")
 
        self.getFortuneButton = QtWidgets.QPushButton("Get Fortune")
        self.getFortuneButton.setDefault(True)
        self.getFortuneButton.setEnabled(False)
 
        quitButton = QtWidgets.QPushButton("Quit")
 
        buttonBox = QtWidgets.QDialogButtonBox()
        buttonBox.addButton(self.getFortuneButton,
                QtWidgets.QDialogButtonBox.ActionRole)
        buttonBox.addButton(quitButton, QtWidgets.QDialogButtonBox.RejectRole)
 
        self.tcpSocket = QtNetwork.QTcpSocket(self)
 
        self.hostLineEdit.textChanged.connect(self.enableGetFortuneButton)
        self.portLineEdit.textChanged.connect(self.enableGetFortuneButton)
        self.getFortuneButton.clicked.connect(self.requestNewFortune)
        quitButton.clicked.connect(self.close)
        self.tcpSocket.readyRead.connect(self.readFortune)
        self.tcpSocket.error.connect(self.displayError)
 
        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(hostLabel, 0, 0)
        mainLayout.addWidget(self.hostLineEdit, 0, 1)
        mainLayout.addWidget(portLabel, 1, 0)
        mainLayout.addWidget(self.portLineEdit, 1, 1)
        mainLayout.addWidget(self.statusLabel, 2, 0, 1, 2)
        mainLayout.addWidget(buttonBox, 3, 0, 1, 2)
        self.setLayout(mainLayout)
 
        self.setWindowTitle("Fortune Client")
        self.portLineEdit.setFocus()
 
    def requestNewFortune(self):
        self.getFortuneButton.setEnabled(False)
        self.blockSize = 0
        self.tcpSocket.abort()
        self.tcpSocket.connectToHost(self.hostLineEdit.text(),
                int(self.portLineEdit.text()))
        data = {
            "foo": 1,
            "bar": [5, 10]
        }

        to_send = json.dumps(data).encode("ascii")
        num_bytes_sent = self.tcpSocket.write(to_send)
        print(f"Sent {num_bytes_sent} bytes.")
 
    def readFortune(self):
        qba = self.tcpSocket.readAll()
        print(str(qba))
        print(json.loads(qba.data().decode("ascii")))

        nextFortune = "always the same"

        # instr = QtCore.QDataStream(self.tcpSocket)
        # instr.setVersion(QtCore.QDataStream.Qt_4_0)
 
        # if self.blockSize == 0:
        #     if self.tcpSocket.bytesAvailable() < 2:
        #         return
 
        # self.blockSize = instr.readUInt16()
 
        # if self.tcpSocket.bytesAvailable() < self.blockSize:
        #     return
 
        # nextFortune = instr.readString()
 
        # try:
        #     # Python v3.
        #     nextFortune = str(nextFortune, encoding='ascii')
        # except TypeError:
        #     # Python v2.
        #     pass
 
        # if nextFortune == self.currentFortune:
        #     QtCore.QTimer.singleShot(0, self.requestNewFortune)
        #     return
 
        self.currentFortune = nextFortune
        self.statusLabel.setText(self.currentFortune)
        self.getFortuneButton.setEnabled(True)
 
    def displayError(self, socketError):
        if socketError == QtNetwork.QAbstractSocket.RemoteHostClosedError:
            pass
        elif socketError == QtNetwork.QAbstractSocket.HostNotFoundError:
            QtWidgets.QMessageBox.information(self, "Fortune Client",
                    "The host was not found. Please check the host name and "
                    "port settings.")
        elif socketError == QtNetwork.QAbstractSocket.ConnectionRefusedError:
            QtWidgets.QMessageBox.information(self, "Fortune Client",
                    "The connection was refused by the peer. Make sure the "
                    "fortune server is running, and check that the host name "
                    "and port settings are correct.")
        else:
            QtWidgets.QMessageBox.information(self, "Fortune Client",
                    "The following error occurred: %s." % self.tcpSocket.errorString())
 
        self.getFortuneButton.setEnabled(True)
 
    def enableGetFortuneButton(self):
        self.getFortuneButton.setEnabled(bool(self.hostLineEdit.text() and
                self.portLineEdit.text()))
 
 
if __name__ == '__main__':
 
    import sys
 
    app = QtWidgets.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(client.exec_())