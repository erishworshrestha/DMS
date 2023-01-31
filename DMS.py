import cv2
from numpy.lib.npyio import _savez_compressed_dispatcher
from scipy.spatial import distance as dist
from skimage.metrics import structural_similarity as compare_ssim
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import serial
from tkinter import *
from PIL import Image, ImageTk
import serial.tools.list_ports
from tkinter import filedialog
import csv
from datetime import datetime
import os
from tkinter import messagebox
import time

filename = None
camera = 0  
count = 0
camera_number = 0
# referenceHeight = 83.7
# referencepixelsPerMetric = 13.49334255641328
# referenceHeight = 82.2
# referencepixelsPerMetric = 14.604202393679552  # best
referenceHeight = 84.4
# referencepixelsPerMetric_length = 13.919578040030524
referencepixelsPerMetric_length = 14
# referencepixelsPerMetric_breadth = 14.013408411678437
# referencepixelsPerMetric_breadth = 14.602791137313442
referencepixelsPerMetric_breadth = 13.9


# result_planes = []
# result_norm_planes = []

ports = list(serial.tools.list_ports.comports())

root = Tk()
width_screen = root.winfo_screenwidth()
height_screen = root.winfo_screenheight()

root.geometry("%dx%d" % (width_screen, height_screen))

root.configure(bg='#2a9d8f')

fieldnames = ["S.N", "Timestamp", "SerialNumber",
              "Length", "Breadth", "Height", "Volume", "Volumetric Weight(5000)", "Volumetric Weight(6000)"]

Label(root, text="Dimension Measurement System", bg='#2a9d8f',
      font=("Georgia", "24", "bold")).pack()

f1 = LabelFrame(root)
f1.place(x=10, y=100, height=400, width=600)
L1 = Label(f1)
L1.pack()


def button(x, y, text, bcolor="#ffcc66", fcolor="#264653", cmd=None, font=(
        'Ebrima', 12)):

    def on_enter(e):
        mybutton['background'] = bcolor
        mybutton['foreground'] = fcolor

    def on_leave(e):
        mybutton['background'] = fcolor
        mybutton['foreground'] = bcolor

    mybutton = Button(root, width=20, height=1, text=text, fg=bcolor, bg=fcolor, font=font,
                      border=4, activeforeground=fcolor, activebackground=bcolor, command=cmd)

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


# def controller(img):
#     brightness = -65
#     contrast = 48
#     shadow = 0
#     max = 255 + brightness
#     al_pha = (max - shadow) / 255
#     ga_mma = shadow
#     cal = cv2.addWeighted(img, al_pha, img, 0, ga_mma) 

#     if contrast != 0:
#         Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
#         Gamma = 127 * (1 - Alpha)
#         cal = cv2.addWeighted(cal, Alpha, cal, 0, Gamma)
#     return cal


def convert(img):
    plane = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0,0,100), (179, 255, 255))
    nzmask = cv2.inRange(hsv, (0, 0, 5), (255, 255, 255))
    nzmask = cv2.erode(nzmask, np.ones((3,3)))
    mask = mask & nzmask
    new_img = img.copy()
    new_img[np.where(mask)] = 255

    gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)

    result  = plane - gray
    
    dilated_img = cv2.dilate(result, np.ones((7, 7), np.uint8))
    # cv2.imshow("test",result)
    # dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(plane, bg_img)
    # norm_img = cv2.normalize(
    #     diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    
    # cv2.imshow("gray",gray)
    # cv2.imshow("norm_img",norm_img)
    return (diff_img,new_img)
    # return (diff_img,gray)


def findHeight():
    if(ser.isOpen() == False):
        ser.open()
    vals = []
    i=0
    while( i<=3 ):
        height = ser.readline().decode('utf-8').rstrip()
        if(height != ''):
            vals.append(height)
            i = i+1

    ser.close()
    height = mostFrequent(vals, len(vals))
    # height = vals
    print(height)
    height = float(height)
    # height = float(height)/10
    return height


def calibration():
    global BaseHeight
    if(ser.isOpen() == False):
        ser.open()
    print("Calibrating.........")
    BaseHeight = findHeight()
    # ret, image = cap.read()
    # if ret:
    #     cv2.imwrite("initial.jpg", image)
    ser.close()
    if BaseHeight != '':
        # BaseHeight = float(BaseHeight)/10
        print("Base Height : " + str(BaseHeight) + " cm")
        return BaseHeight


def newFile():
    global filename
    if newFileName.get() != "":
        filename = str(newFileName.get()) + ".csv"
        with open(filename, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
        label(650, 130, text=filename)
        newFileName.delete(0, 'end')
    displayData()


def selectCsv():
    global filename
    location = filedialog.askopenfilename(
        title="Select file", filetypes=(("CSV Files", "*.csv"),))
    filename = os.path.basename(location)

    label(650, 130, text=filename)
    displayData()


def addData():
    global count
    count += 1
    if not str(newSerial.get()):
        messagebox.showerror(title="No Serial Detected",
                             message="Enter a Serial Number")
    else:
        with open(str(filename), 'a', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            timestamp = datetime.now()

            info = {
                "S.N": count,
                "Timestamp": timestamp,
                "SerialNumber": str(newSerial.get()),
                "Length": dimA,
                "Breadth": dimB,
                "Height": height,
                "Volume": volume,
                "Volumetric Weight(5000)": volumetricWeightFirst,
                "Volumetric Weight(6000)": volumetricWeightSecond
            }
            csv_writer.writerow(info)
        takeSnapshot()
        displayData()
        newSerial.delete(0, 'end')


def display(length, breadth, height, volume):
    label(730, 420, length, font=('Times New Roman', 12))
    label(740, 450, breadth, font=('Times New Roman', 12))
    label(730, 480, height, font=('Times New Roman', 12))
    label(730, 510, volume, font=('Times New Roman', 12))


def count_cameras():
    max_tested = 100
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

    if(camera_number==camera_count):
        camera_number = 0

switch()


def takeSnapshot():
    img = Image.fromarray(img1)
    folderPath = "Snapshots\\"+filename[:-4]+"\\"
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    name = folderPath + str(newSerial.get()) + ".jpg"
    img.save(name)


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


for port in ports:
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
    if filename is not None:
        mylist.delete(0, 'end')
        with open(filename) as File:
            reader = csv.DictReader(File)
            for row in reader:
                mylist.insert(
                    END, "--------------------------------------------------------------------------------------------")
                mylist.insert(END, row["S.N"] + " | " + row["Timestamp"] + " | " + row["SerialNumber"] + " | " +
                              row["Length"] + " | " + row["Breadth"] + " | " + row["Height"] + " | " + row["Volume"])


mylist.place(x=880, y=78)
scrollbar.config(command=mylist.yview)

BaseHeight = calibration()

def measure():
    global dimA
    global dimB
    global height
    global volume
    global volumetricWeightFirst
    global volumetricWeightSecond
    global BaseHeight

    width_ = widthSet.get()
    height_ = heightSet.get()
    maxWidth = int(cap.get(3))
    maxHeight = int(cap.get(4))
    upper_left = (width_, height_)
    bottom_right = (maxWidth - width_,
                    maxHeight - height_)
    imageA = cv2.imread("initial.jpg")
    roiA = imageA[upper_left[1]: bottom_right[1],
                  upper_left[0]: bottom_right[0]]
    # gray, gray_norm, mask = convert(roiA)
    ret, image = cap.read()

    if ret:
        cv2.rectangle(image.copy(), upper_left, bottom_right, (0, 50, 200), 2)

        roi = image[upper_left[1]: bottom_right[1],
                    upper_left[0]: bottom_right[0]]

        grayB,gray_shadow = convert(roi)
        gray,mask = convert(roiA+gray_shadow)
        # cv2.imshow("before addition", gray)
        # gray,mask = convert(roiA + gray_shadow)
        # gray = gray + gray_shadow 
        # grayB = grayB + gray_shadow 
        cv2.imshow("after addition", gray) 
        cv2.imshow("gray_shadow", gray_shadow)
        cv2.imshow("compare 2", grayB)
        (score, diff) = compare_ssim(gray, grayB, full=True)
        diff = (diff * 255).astype("uint8")

        # diff = gray - grayB

        edged = cv2.threshold(diff, 0, 255,
                              cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        
        # edged_shadow= cv2.threshold(gray_shadow, 0, 255,
        #                       cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        cv2.imshow("edged",edged)
        # edged = edged - gray_shadow
        # cv2.imshow("edged after",edged)
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        
        if(cnts != ([], None)):
            cnts = imutils.grab_contours(cnts)
            (cnts, _) = contours.sort_contours(cnts)

            for c in cnts:
                # print("Area : " + str(cv2.contourArea(c)))
                # if(biggestContour > cv2.contourArea(c)):
                #     continue
                # else:
                #     biggestContour = cv2.contourArea(c)
                    # print("Biggest : " + str(biggestContour))

                # if (cv2.contourArea(c) < 10000):
                # if (cv2.contourArea(c) < 5000):
                    if (cv2.contourArea(c) < 3000):
                        # print(cv2.contourArea(c))
                        continue
                    box = cv2.minAreaRect(c)
                    box = cv2.cv.BoxPoints(
                        box) if imutils.is_cv2() else cv2.boxPoints(box)
                    box = np.array(box, dtype="int")

                    box = perspective.order_points(box)
                    cv2.drawContours(
                        roi, [box.astype("int")], -1, (0, 255, 0), 2)

                    for (x, y) in box:
                        cv2.circle(roi, (int(x), int(y)), 5, (0, 0, 255), -1)

                    (tl, tr, br, bl) = box
                    (tltrX, tltrY) = midpoint(tl, tr)
                    (blbrX, blbrY) = midpoint(bl, br)

                    (tlblX, tlblY) = midpoint(tl, bl)
                    (trbrX, trbrY) = midpoint(tr, br)

                    cv2.circle(roi, (int(tltrX), int(tltrY)),
                            5, (255, 0, 0), -1)
                    cv2.circle(roi, (int(blbrX), int(blbrY)),
                            5, (255, 0, 0), -1)
                    cv2.circle(roi, (int(tlblX), int(tlblY)),
                            5, (255, 0, 0), -1)
                    cv2.circle(roi, (int(trbrX), int(trbrY)),
                            5, (255, 0, 0), -1)

                    cv2.line(roi, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                            (255, 0, 255), 2)
                    cv2.line(roi, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                            (255, 0, 255), 2)

                    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

                    ser.open()
                    Height = findHeight()
                    ser.close()
                    height = BaseHeight - Height

                    # if(height > 20):
                    #     break

                    # if height < -0.2:
                    #     BaseHeight = calibration()
                    #     continue

                    # pixelsPerMetric = referenceHeight/Height*referencepixelsPerMetric
                    pixelsPerMetric_length = referenceHeight/Height*referencepixelsPerMetric_length
                    pixelsPerMetric_breadth = referenceHeight / \
                        Height*referencepixelsPerMetric_breadth

                    # print(pixelsPerMetric)
                    # dimA = dA / pixelsPerMetric*2.54
                    # dimB = dB / pixelsPerMetric*2.54

                    dimA = dA / pixelsPerMetric_length*2.54
                    dimB = dB / pixelsPerMetric_breadth*2.54

                    # pixelsPerMetric_length = dA/40*2.54
                    # pixelsPerMetric_breadth = dB/40*2.54
                    # print("Length : " + str(pixelsPerMetric_length))
                    # print("Breadth : " + str(pixelsPerMetric_breadth))

                    dimA_vals = []
                    dimB_vals = []
                    height_vals = []

                    for i in range(5):
                        if ser:
                            dimA_vals.append(dimA)
                            dimB_vals.append(dimB)
                            height_vals.append(height)

                    dimA = mostFrequent(dimA_vals, len(dimA_vals))
                    dimB = mostFrequent(dimB_vals, len(dimB_vals))
                    height = mostFrequent(height_vals, len(height_vals))

                    dimA = round(dimA, 2)
                    dimB = round(dimB, 2)
                    height = round(height, 2)
                    volume = round(dimA*dimB*height, 2)
                    volumetricWeightFirst = round(dimA*dimB*height/5000, 2)
                    volumetricWeightSecond = round(dimA*dimB*height/6000, 2)

                    cv2.putText(roi, "Length : {:.1f} cm".format(dimA),
                                (5, 40
                                ), cv2.FONT_HERSHEY_SIMPLEX,
                                0.65, (255, 0, 0), 2)
                    cv2.putText(roi, "Breadth : {:.1f} cm".format(dimB),
                                (5, 60
                                ), cv2.FONT_HERSHEY_SIMPLEX,
                                0.65, (255, 0, 0), 2)
                    cv2.putText(roi, "Height : {:.1f} cm".format(height),
                                (5, 80
                                ), cv2.FONT_HERSHEY_SIMPLEX,
                                0.65, (255, 0, 0), 2)

                    display(str(dimA), str(dimB), str(height), str(volume))
                    global img1
                    img1 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    print(img1.shape)
                    image = ImageTk.PhotoImage(Image.fromarray(img1))
                    cv2.imshow("Snapshot", cv2.cvtColor(
                        img1, cv2.COLOR_BGR2RGB))
                    L1['image'] = image
                    root.update()


#################################   L A B E L S  #################################
label(650, 100, "Filename : ")
label(10, 527, "Length :")
label(10, 595, "Breadth :")
label(650, 380, "Dimensions", font=('Times New Roman bold', 18))
label(650, 420, "Length : ")
label(650, 450, "Breadth : ")
label(650, 480, "Height : ")
label(650, 510, "Volume : ")
label(880, 52, "S.N |")
label(920, 52, "Timestamp |")
label(1020, 52, "Serial |")
label(1075, 52, "Length |")
label(1140, 52, "Breadth |")
label(1215, 52, "Height |")
label(1280, 52, "Volume")

label(650, 160, "Enter a Filename : ")
newFileName = Entry(root, width=17, border=0, bg="#2a9d8f", fg="#fff",
                    font=('Times New Roman', 15))
newFileName.place(x=652, y=190)
Frame(root, width=160, height=2, bg="#fff").place(x=652, y=213)

label(650, 550, "Enter a Serial Number : ")
newSerial = Entry(root, width=17, border=0, bg="#2a9d8f", fg="#fff",
                  font=('Times New Roman', 15))
newSerial.place(x=652, y=575)
Frame(root, width=180, height=2, bg="#fff").place(x=652, y=598)


#################################   B U T T O N S  #################################
button(650, 230, "Create an excel file", cmd=newFile)
button(650, 280, "Select an excel file", cmd=selectCsv)
button(10, 660, "Calibrate", cmd=calibration)
button(650, 610, "Measure", cmd=measure)
button(650, 660, "Proceed", cmd=addData)
button(10, 50, "Switch Camera", cmd=switch)


while(True):
    ret, image = cap.read()
    # image = controller(image)
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
