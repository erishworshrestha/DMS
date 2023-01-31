import os
import csv
import cv2
import math
import serial
import imutils
import numpy as np
from tkinter import *
from pathlib import Path
from imutils import contours
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog
import serial.tools.list_ports
from PIL import Image, ImageTk
from imutils import perspective
from scipy.spatial import distance as dist
import pickle

print("**************************************************************")
print("Made By Nepal Innovative Project Solution (NIPS)")
print("Instagram/Facebook/TikTok : nipsolution.np")
print("Contact Number/Whatsapp : 9818836736")
print("E-Mail : nipsolution.np@gmail.com")
print("**************************************************************")


agency = ""
dimA = 0
dimB = 0
height = 0
count = 0
camera = 0
shipment = ""
location = ""
filename_ = ""
filename = None
fullLocation = ""
camera_number = 0
LengthAdditional = 0
BreadthAdditional = 0

referenceHeight_length = 95.6
referencepixelsPerMetric_length = 15.835
referenceHeight_breadth = 82.267
referencepixelsPerMetric_breadth = 18.156336813906044  # fixed

ports = list(serial.tools.list_ports.comports())

root = Tk()
width_screen = root.winfo_screenwidth()
height_screen = root.winfo_screenheight()

root.geometry("%dx%d" % (width_screen, height_screen))
root.configure(bg='#2a9d8f')

fieldnames = ["Timestamp", "BoxNumber",
              "Length (cm)", "Breadth (cm)", "Height (cm)", "Weight (kg)", "Volume", "Volumetric Weight(5000)", "Volumetric Weight(6000)"]

Label(root, text="NIPS Dimension Measurement System", bg='#2a9d8f',
      font=("Georgia", "24", "bold")).pack()

f1 = LabelFrame(root)
f1.place(x=10, y=100, height=400, width=600)
L1 = Label(f1)
L1.pack()


def button(x, y, text, width_=20, height_=1, border_=4, bcolor="#ffcc66", fcolor="#264653", cmd=None, font=(
        'Ebrima', 12)):

    def on_enter(e):
        mybutton['background'] = bcolor
        mybutton['foreground'] = fcolor

    def on_leave(e):
        mybutton['background'] = fcolor
        mybutton['foreground'] = bcolor

    mybutton = Button(root, width=width_, height=height_, text=text, fg=bcolor, bg=fcolor, font=font,
                      border=border_, activeforeground=fcolor, activebackground=bcolor, command=cmd)

    mybutton.bind('<Enter>', on_enter)
    mybutton.bind('<Leave>', on_leave)
    mybutton.place(x=x, y=y)


def label(x, y, text, bcolor="#2a9d8f", fcolor="#fff", font=('Georgia', 12)):
    Label(root, text=text, bg=bcolor, fg=fcolor,
          font=font).place(x=x, y=y)


def mostFrequent(arr, n):
    arr.sort()
    max_count = 1
    res = arr[0]
    curr_count = 1
    for i in range(1, n):
        if (arr[i] == arr[i - 1]):
            curr_count += 1
        else:
            if (curr_count > max_count):
                max_count = curr_count
                res = arr[i - 1]
            curr_count = 1
    if (curr_count > max_count):
        max_count = curr_count
        res = arr[n - 1]
    return res


def convert(img):
    plane = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 0, 100), (179, 255, 255))
    nzmask = cv2.inRange(hsv, (0, 0, 5), (255, 255, 255))
    nzmask = cv2.erode(nzmask, np.ones((3, 3)))
    mask = mask & nzmask
    new_img = img.copy()
    new_img[np.where(mask)] = 255
    gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    result = plane - gray
    dilated_img = cv2.dilate(result, np.ones((7, 7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(plane, bg_img)
    return (diff_img, new_img)


def findHeight():
    global height
    vals = []
    i = 0
    if(ser.isOpen() == False):
        ser.open()

    while True:
        height = ser.readline().decode('utf-8').rstrip()
        if(height != ''):
            break

    # height = ser.readline().decode('utf-8').rstrip()
    # while(i <= 3):
    #     height = ser.readline().decode('utf-8').rstrip()
    #     if(height != ''):
    #         vals.append(height)
    #         i = i+1
    # height = mostFrequent(vals, len(vals))
    ser.close()
    print("Height : " + str(height))
    if(height != ''):
        height = float(height)/10
        height = round(height, 2)
    return height


def calibration():
    global BaseHeight
    # print("A product of Nepal Innovative Project Solution (NIPS)")
    if(ser.isOpen() == False):
        ser.open()
    print("Calibrating.........")
    BaseHeight = findHeight()
    label(130+20, 61, "      ")
    label(130+20, 61, BaseHeight, font=('Times New Roman', 16))
    ser.close()
    if BaseHeight != '':
        print("Base Height : " + str(BaseHeight) + " cm")
        return BaseHeight


def newFile():
    global filename_
    global shipment
    global agency
    global location
    global fullLocation

    shipment = str(shipment_number.get())
    filename_ = str(newFileName.get())
    agency = filename_[:4]
    if filename_ != "" or location != "":
        if shipment != "":
            folderPath = "Dimensions\\"+agency+"\\"+shipment+"\\"
            if not os.path.exists(folderPath):
                os.makedirs(folderPath)

            filename = folderPath + filename_ + ".csv"
            location = filename
            with open(filename, 'w', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writeheader()
            label(730, 60+15, "                               ")
            label(730, 60+15, text=filename_)
            label(800, 190+15-60, "         ")
            label(800, 190+15-60, shipment)
            newFileName.delete(0, 'end')
            shipment_number.delete(0, 'end')
            fullLocation = os.path.abspath(location)
            displayData()
        else:
            messagebox.showerror(title="Shipment",
                                 message="Enter Shipment Details")
    else:
        messagebox.showerror(title="SN Number",
                             message="Enter SN Number")
    # if location == "":
    #     messagebox.showerror(title="SN Number",
        # message="Enter SN Number")
    # else:
    #     fullLocation = os.path.abspath(location)
    #     displayData()


def selectCsv():
    global filename
    global location
    global fullLocation
    global filename_
    global shipment

    location = filedialog.askopenfilename(
        title="Select file", filetypes=(("CSV Files", "*.csv"),))
    fullLocation = location
    p = Path(location)
    shipment = p.parts[-2]
    filename = os.path.basename(location)
    filename_ = filename[:-4]
    label(730, 60+15, "                                  ")
    label(730, 60+15, text=filename[:-4])
    label(800, 190+15-60, "         ")
    label(800, 190+15-60, shipment)
    displayData()


def addData():
    # global count
    global LengthAdditional
    global BreadthAdditional
    global fullLocation
    # global filename_
    # global shipment

    # count += 1
    if fullLocation == "":
        messagebox.showerror(title="No File Location",
                             message="Please select or create a file")
    # elif shipment !="":
    #     messagebox.showerror(title="Shipment",
    #                             message="Enter Shipment Details")
    elif not str(newSerial.get()):
        messagebox.showerror(title="No Box Number Detected",
                             message="Enter a Box Number")
    elif not str(newWeight.get()):
        messagebox.showerror(title="Add Weight",
                             message="Enter Weight Value")
    elif dimA == 0 or dimB == 0 or height == 4:
        messagebox.showerror(title="Zero Values",
                             message="Please Measure First")
    else:
        with open(str(fullLocation), 'a', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            info = {
                # "S.N": count,
                "Timestamp": timestamp,
                "BoxNumber": str(newSerial.get()),
                "Length (cm)": dimB,
                "Breadth (cm)": dimA,
                "Height (cm)": height,
                "Weight (kg)": str(newWeight.get()),
                "Volume": volume,
                "Volumetric Weight(5000)": volumetricWeightFirst,
                "Volumetric Weight(6000)": volumetricWeightSecond
            }
            csv_writer.writerow(info)
        # file_list = drive.ListFile(
        #     {'q': "'root' in parents and trashed=false"}).GetList()
        # for file1 in file_list:
        #     if file1['title'] == filename:
        #         file1.Delete()

        # # textfile = drive.CreateFile()
        # textfile.SetContentFile(filename)
        # textfile.Upload()

        takeSnapshot()
        displayData()
        newSerial.delete(0, 'end')
        newWeight.delete(0, 'end')
        resetAddition()
        resetData()


def resetData():
    global dimA
    global dimB
    global height
    dimA = 0
    dimB = 0
    height = 0
    display(dimB, dimA, height)


def display(breadth, length, height):
    label(730, 360+25+35, "     ", font=('Times New Roman', 12))
    label(740, 390+25+35, "     ", font=('Times New Roman', 12))
    label(730, 420+25+35, "     ", font=('Times New Roman', 12))
    label(730, 360+25+35, length, font=('Times New Roman', 12))
    label(740, 390+25+35, breadth, font=('Times New Roman', 12))
    label(730, 420+25+35, height, font=('Times New Roman', 12))


display(dimB, dimA, height)


def count_cameras():
    max_tested = 5
    for i in range(max_tested):
        temp_camera = cv2.VideoCapture(i)
        if temp_camera.isOpened():
            temp_camera.release()
            continue
        return i


camera_count = count_cameras()


def switch():
    global cap
    global camera
    global camera_number
    cap = cv2.VideoCapture(camera_number, cv2.CAP_DSHOW)
    camera_number = camera_number + 1

    if(camera_number == camera_count):
        camera_number = 0


switch()


def takeSnapshot():
    global agency
    global filename_
    global shipment

    agency = filename_[:4]
    img = Image.fromarray(img1)
    folderPath = "Snapshots\\"+agency+"\\"+shipment+"\\"+filename_+"\\"
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    name = folderPath + str(newSerial.get()) + ".jpg"
    img.save(name)


def load_calibration(calib_file):
    with open(calib_file, 'rb') as file:
        data = pickle.load(file)
        mtx = data['mtx']
        dist = data['dist']
    return mtx, dist


# def undistort_image(imagepath, calib_file):
#     mtx, dist = load_calibration(calib_file)
#     # img = cv2.imread(imagepath)
#     img_undist = cv2.undistort(imagepath, mtx, dist, None, mtx)
#     return img_undist


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


for port in ports:
    # print(port)
    if "USB-SERIAL" in port.description:
        if __name__ == '__main__':
            try:
                ser = serial.Serial(str(port[0]), 9600, timeout=1)
                ser.flush()
            except serial.SerialException as e:
                continue
            except OSError:
                continue

        if (ser == None or len(ser.readline()) == 0):
            continue
        else:
            BaseHeight = calibration()
        if BaseHeight != None:
            break
        ser.close()

widthSet = Scale(root, from_=50, to=230, tickinterval=20, bg="#2a9d8f", fg="#fff",
                 length=cap.get(3)-115, orient=HORIZONTAL)
widthSet.place(x=80, y=510)

heightSet = Scale(root, from_=80, to=170, orient=HORIZONTAL, bg="#2a9d8f", fg="#fff",
                  tickinterval=10, length=cap.get(3)-115)
heightSet.place(x=80, y=580)

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

mylist = Listbox(root, yscrollcommand=scrollbar.set, font=('Georgia', 10),
                 height=39, width=52, bg="#264653", fg="#fff", bd=0)


def displayData():
    global fullLocation
    if fullLocation is not None:
        mylist.delete(0, 'end')
        with open(fullLocation) as File:
            reader = csv.DictReader(File)
            for row in reader:
                mylist.insert(
                    END, "--------------------------------------------------------------------------------------------")
                mylist.insert(END, row["Timestamp"] + "        |       " + row["BoxNumber"] + "       |       " +
                              row["Length (cm)"] + "       |       " + row["Breadth (cm)"] + "       |       " + row["Height (cm)"] + "       |       " + row["Weight (kg)"])


mylist.place(x=880, y=70)
scrollbar.config(command=mylist.yview)

BaseHeight = calibration()


def lengthIncrease():
    global LengthAdditional
    if LengthAdditional != 3:
        LengthAdditional = LengthAdditional+1
        label(650+130+30, 360+25+35, LengthAdditional)
    resetData()


def BreadthIncrease():
    global dimA
    global BreadthAdditional
    if BreadthAdditional != 3:
        BreadthAdditional = BreadthAdditional+1
        label(650+130+30, 390+25+35, BreadthAdditional)
    resetData()


def resetAddition():
    global LengthAdditional
    global BreadthAdditional
    LengthAdditional = 0
    BreadthAdditional = 0
    label(650+130+30, 360+25+35, LengthAdditional)
    label(650+130+30, 390+25+35, BreadthAdditional)


def measure():
    global dimA
    global dimB
    global height
    global volume
    global volumetricWeightFirst
    global volumetricWeightSecond
    global BaseHeight
    global originalImage

    width_ = widthSet.get()
    height_ = heightSet.get()
    maxWidth = int(cap.get(3))
    maxHeight = int(cap.get(4))
    upper_left = (width_, height_)
    bottom_right = (maxWidth - width_, maxHeight - height_)
    ret, image = cap.read()
    originalImage = image

    if ret:
        cv2.rectangle(image.copy(), upper_left, bottom_right, (0, 50, 200), 2)

        image = image[upper_left[1]: bottom_right[1],
                      upper_left[0]: bottom_right[0]]
        # image = undistort_image(image, 'calibration_pickle.p')
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # 82 10 89
        lower_blue = np.array([40, 0, 80])
        # lower_blue = np.array([80, 10, 75])
        upper_blue = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        result = cv2.bitwise_and(image, image, mask=mask)
        final2 = image - result
        final2 = cv2.cvtColor(final2, cv2.COLOR_BGR2GRAY)
        final2 = 255 - final2
        edged = cv2.threshold(final2, 0, 255,
                              cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

        if(cnts != ([], None)):
            cnts = imutils.grab_contours(cnts)
            (cnts, _) = contours.sort_contours(cnts)

            for c in cnts:
                if (cv2.contourArea(c) < 3000):
                    continue
                box = cv2.minAreaRect(c)
                box = cv2.cv.BoxPoints(
                    box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int")

                box = perspective.order_points(box)
                cv2.drawContours(
                    image, [box.astype("int")], -1, (0, 255, 0), 2)

                for (x, y) in box:
                    cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)

                (tl, tr, br, bl) = box
                (tltrX, tltrY) = midpoint(tl, tr)
                (blbrX, blbrY) = midpoint(bl, br)
                (tlblX, tlblY) = midpoint(tl, bl)
                (trbrX, trbrY) = midpoint(tr, br)

                cv2.circle(image, (int(tltrX), int(tltrY)),
                           5, (255, 0, 0), -1)
                cv2.circle(image, (int(blbrX), int(blbrY)),
                           5, (255, 0, 0), -1)
                cv2.circle(image, (int(tlblX), int(tlblY)),
                           5, (255, 0, 0), -1)
                cv2.circle(image, (int(trbrX), int(trbrY)),
                           5, (255, 0, 0), -1)

                cv2.line(image, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                         (255, 0, 255), 2)
                cv2.line(image, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                         (255, 0, 255), 2)

                dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

                if(ser.isOpen() == False):
                    ser.open()
                Height = findHeight()
                ser.close()
                height = float(BaseHeight) - float(Height)

                if height < -0.2:
                    BaseHeight = calibration()
                    continue

                # pixelsPerMetric = referenceHeight/Height*referencepixelsPerMetric
                # pixelsPerMetric_length = referenceHeight_length/Height*referencepixelsPerMetric_length/1.031245115
                pixelsPerMetric_length = referenceHeight_length / \
                    Height*referencepixelsPerMetric_length/1.02

                pixelsPerMetric_breadth = referenceHeight_breadth / \
                    Height*referencepixelsPerMetric_breadth

                dimB = dB / pixelsPerMetric_length*2.54
                dimA = dA / pixelsPerMetric_breadth*2.54

                # pixelsPerMetric_length = dB/45.5*2.54     #40 length
                # pixelsPerMetric_breadth = dA/28.6*2.54    #40 breadth

                # print("Expected PPM of Length : " + str(pixelsPerMetric_length))
                # print("Expected PPM of Breadth : " + str(pixelsPerMetric_breadth))

                # dimA = round(dimA, 2)
                # dimB = round(dimB, 2)
                # height = round(height, 2)
                # volume = round(dimA*dimB*height, 2)
                # volumetricWeightFirst = round(dimA*dimB*height/5000, 2)
                # volumetricWeightSecond = round(dimA*dimB*height/6000, 2)

                dimA = math.ceil(dimA) + BreadthAdditional
                dimB = math.ceil(dimB) + LengthAdditional
                height = math.ceil(height)
                volume = math.ceil(dimA*dimB*height)
                volumetricWeightFirst = math.ceil(dimA*dimB*height/5000)
                volumetricWeightSecond = math.ceil(dimA*dimB*height/6000)

                cv2.putText(image, "Length : {:.1f} cm".format(dimB),
                            (5, 40
                             ), cv2.FONT_HERSHEY_SIMPLEX,
                            0.65, (0, 0, 255), 2)
                cv2.putText(image, "Breadth : {:.1f} cm".format(dimA),
                            (5, 60
                             ), cv2.FONT_HERSHEY_SIMPLEX,
                            0.65, (0, 0, 255), 2)

                cv2.putText(image, "Height : {:.1f} cm".format(height),
                            (5, 80
                             ), cv2.FONT_HERSHEY_SIMPLEX,
                            0.65, (0, 0, 255), 2)

                display(str(dimA), str(dimB), str(height))
                global img1
                img1 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = ImageTk.PhotoImage(Image.fromarray(img1))
                cv2.imshow("Snapshot", cv2.cvtColor(
                    img1, cv2.COLOR_BGR2RGB))
                L1['image'] = image
                root.update()


#################################   L A B E L S  #################################
label(20, 60, "Base-Height : ", font=('Times New Roman bold', 16))
label(130+20+60, 61, "cm", font=('Times New Roman bold', 16))
label(650, 60+15, "Filename : ")
label(15, 527, "Length :")
label(8, 595, "Breadth :")
label(650, 320+25+35, "Dimensions", font=('Times New Roman bold', 18))
label(650, 360+25+35, "Length : ")
label(650+130, 360+25+35, "+")
label(650, 390+25+35, "Breadth : ")
label(650+130, 390+25+35, "+")
label(650, 420+25+35, "Height : ")
label(650+130+30, 360+25+35, LengthAdditional)
label(650+130+30, 390+25+35, BreadthAdditional)
# label(880, 45, "S.N |")
label(880+10, 45, "Time |")
label(935+10, 45, "BoxNumber |")
label(1020+20+10, 45, "Length |")
label(1075+35+10, 45, "Breadth |")
label(1140+50+10, 45, "Height |")
label(1215+45+10, 45, "Weight")
# label(1280, 45, "Volume")
label(650, 190+15-60, "Shipment Number : ")

label(650, 120+15-30, "SN Number : ")
newFileName = Entry(root, width=13, border=0, bg="#2a9d8f", fg="#fff",
                    font=('Times New Roman', 15))
newFileName.place(x=748, y=120+15-30)
Frame(root, width=130, height=2, bg="#fff").place(x=748, y=120+15-30+23)

label(650, 480+35, "Enter a Weight : ")
newWeight = Entry(root, width=5, border=0, bg="#2a9d8f", fg="#fff",
                  font=('Times New Roman', 15))
newWeight.place(x=780, y=480+35)
Frame(root, width=50, height=2, bg="#fff").place(x=775, y=503+35)
label(825, 480+35, "Kg")

label(650, 550, "Enter a Box Number : ")
newSerial = Entry(root, width=17, border=0, bg="#2a9d8f", fg="#fff",
                  font=('Times New Roman', 15))
newSerial.place(x=652, y=575)
Frame(root, width=180, height=2, bg="#fff").place(x=652, y=598)

label(650, 190+15-60+30, "Enter Shipment: ")
shipment_number = Entry(root, width=10, border=0, bg="#2a9d8f", fg="#fff",
                        font=('Times New Roman', 15))
shipment_number.place(x=775, y=190+15-60+30)
Frame(root, width=100, height=2, bg="#fff").place(x=775, y=190+15-60+30+23)

#################################   B U T T O N S  #################################
button(650, 210, "Create an excel file", cmd=newFile)
button(650, 260, "Select an excel file", cmd=selectCsv)
button(650, 610, "Measure", cmd=measure)
button(650, 660, "Proceed", cmd=addData)
button(350, 660, "Reset", cmd=resetAddition)
button(10, 660, "Calibrate", cmd=calibration)
button(840, 360+25+35-10, "+", cmd=lengthIncrease,
       width_=2, height_=1, border_=1)
button(840, 390+25+35, "+", cmd=BreadthIncrease,
       width_=2, height_=1, border_=1)

if(camera_count > 1):
    button(10, 50, "Switch Camera", cmd=switch)

while(True):
    ret, image = cap.read()
    width_ = widthSet.get()
    height_ = heightSet.get()
    maxWidth = int(cap.get(3))
    maxHeight = int(cap.get(4))
    upper = (width_, height_)
    bottom = (maxWidth - width_,
              maxHeight - height_)
    cv2.rectangle(image, upper, bottom, (100, 50, 200), 2)
    img2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = ImageTk.PhotoImage(Image.fromarray(img2))
    L1['image'] = image
    root.update()
