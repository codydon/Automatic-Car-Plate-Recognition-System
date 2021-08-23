from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,  QFileDialog, QDialog
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidget
import sys
import os
from db import *
import autoplate as main
import searchplate as search

import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import pytesseract
from PIL import Image
class AutoPlate(main.Ui_MainWindow, QtWidgets.QMainWindow):
        def __init__(self):
                super(AutoPlate,self).__init__()
                #setting up the first window
                self.setupUi(self)
                self.setFixedSize(831, 551)
                #connecting buttons
                self.pushButton.clicked.connect(self.choosePic)
                self.pushButton_2.clicked.connect(self.takePicture)
                #button search page
                self.pushButton_4.clicked.connect(self.searchNdelete)
        
        def choosePic(self):
                #reading image from user, grayscale & blur
                fname = QFileDialog.getOpenFileName(self, 'open file', 'C\\', 'Image files (*.jpg *.png)')
                global imagePath
                imagePath = fname[0]
                self.processPic()

        def takePicture(self):
                try:
                        #capture image using laptop's webcam 0
                        videoCaptureObject = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                        result = True
                        while(result):
                                now = QDateTime.currentDateTime()
                                datetime = QDateTime.currentDateTime()
                                tdate = now.toString(Qt.ISODate)
                                time = datetime.toString()
                                ret,frame = videoCaptureObject.read()
                                global store
                                store = 'Pic.jpg'
                                path ='C:/Users/Kiongoss/Desktop/Ml project/AutoPlate'
                                print(store)
                                #cv2.imwrite(store, frame)
                                cv2.imwrite(os.path.join(path, "pic.jpg"), frame)
                                result = False
                        videoCaptureObject.release()
                        cv2.destroyAllWindows()
                        global imagePath
                        imagePath = path+'/pic.jpg'
                        print(imagePath)
                        self.processPic()
                except Exception:
                        print("No number  Plate found")
                        self.label_9.setText("Camera Found No Plate!")

        
        def processPic(self):
                self.label_9.clear()                
                img = cv2.imread(imagePath)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
                plt.show()
                #apply filter and find edges for localization
                bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
                edged = cv2.Canny(bfilter, 30, 200) #Edge detection
                plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
                #plt.show()

                #find contours(outline) and apply mask
                keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours = imutils.grab_contours(keypoints)
                contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

                location = None
                for contour in contours:
                        approx = cv2.approxPolyDP(contour, 10, True)
                        if len(approx) == 4:
                                location = approx
                                break

                location
                try:
                        mask = np.zeros(gray.shape, np.uint8)
                        new_image = cv2.drawContours(mask, [location], 0,255, -1)
                        new_image = cv2.bitwise_and(img, img, mask=mask)                        
                        plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
                        #plt.show()
                except:
                        self.label_9.setText("Number Plate Not Found")


                (x,y) = np.where(mask==255)
                (x1, y1) = (np.min(x), np.min(y))
                (x2, y2) = (np.max(x), np.max(y))
                cropped_image = gray[x1:x2+1, y1:y2+1]
                #print(cropped_image)
                plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
                #plt.show()

                #convert numpy.ndarray array to a png
                cdata= Image.fromarray(cropped_image)
                cdata.save('kenyanPlate.png')

                # Create an image object of PIL library
                c_image = cv2.imread('kenyanPlate.png')

                #set pytesseract path
                pytesseract.pytesseract.tesseract_cmd = r'C:\Users\codyDon\AppData\Local\Tesseract-OCR\tesseract.exe'
                #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

                # pytesseract is trained in many languages
                image_to_text = pytesseract.image_to_string(c_image, lang='eng')
                date = QDate.currentDate().toString("yyyy-MM-dd")

                # Print the text to the screen
                if image_to_text != "":
                        self.label_9.setText(image_to_text)
                        cursor = conn.cursor()
                        query = ("INSERT INTO my_table (number,date) VALUE(%s,%s)")
                        values = (image_to_text, date)
                        cursor.execute( query,values)
                        conn.commit()
                        cursor.close()
                        print(image_to_text)
                else:
                        self.label_9.setText("Number Plate Not Found")



                #APP LAUNCH

        def searchNdelete(self):
                self.ui = SearchDelete()
                self.ui.show()
                self.hide()

class SearchDelete(search.Ui_MainWindow, QtWidgets.QMainWindow):
                def __init__(self):
                        super(SearchDelete, self).__init__()
                        self.setupUi(self)

                        self.pushButton.clicked.connect(self.back_button)
                        self.pushButton_2.clicked.connect(self.search)
                #redirectback to maindashboard
                def back_button(self):
                        self.ui = AutoPlate()
                        self.ui.show()
                        self.hide()

                def search(self):
                        platenumber = self.lineEdit.text()
                        cursor = conn.cursor()
                        query = """SELECT *FROM my_table WHERE number=(%s)"""
                        values = (platenumber,)
                        cursor.execute( query,values)
                        result = cursor.fetchall()
                        
                        self.tableWidget.setRowCount(0)

                        for row_number, row_data in enumerate(result):
                                self.tableWidget.insertRow(row_number)

                        for column_number, data in enumerate(row_data):
                                self.tableWidget.setItem(row_number, column_number, QTableWidget(str(data)))
                        print(result)
                        conn.commit()
                        cursor.close()

if __name__ == "__main__":
        #create an application
        app = QtWidgets.QApplication(sys.argv)
        w = AutoPlate()
        #show the window and start the app
        w.show()
        app.exec_()
