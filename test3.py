import cv2
import math
import pickle
import numpy as np
import imutils
from imutils import contours
from imutils import perspective
from scipy.spatial import distance as dist


referenceHeight_length = 95.6
referencepixelsPerMetric_length = 15.835
referenceHeight_breadth = 82.267
referencepixelsPerMetric_breadth = 18.156336813906044 #fixed


Height = 158

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def load_calibration(calib_file):
    with open(calib_file, 'rb') as file:
        data= pickle.load(file)
        mtx = data['mtx'] 
        dist = data['dist'] 
    return mtx, dist


def undistort_image(imagepath, calib_file):
    mtx, dist = load_calibration(calib_file)
    img = cv2.imread(imagepath)
    img_undist = cv2.undistort(img, mtx, dist, None, mtx)
    return img_undist

# ret, image = cap.read()
image = undistort_image('Boxes/b18p1.png','calibration_pickle.p')
image = cv2.imread('Boxes/b18p7.png')


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


    height = 54.1

    pixelsPerMetric_length = referenceHeight_length / \
        Height*referencepixelsPerMetric_length/1.02

    pixelsPerMetric_breadth = referenceHeight_breadth / \
        Height*referencepixelsPerMetric_breadth

    dimB = dB / pixelsPerMetric_length*2.54
    dimA = dA / pixelsPerMetric_breadth*2.54

    # height = math.ceil(height)
    # volume = math.ceil(dimA*dimB*height)
    # volumetricWeightFirst = math.ceil(dimA*dimB*height/5000)
    # volumetricWeightSecond = math.ceil(dimA*dimB*height/6000)

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

    img1 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imshow("Snapshot", cv2.cvtColor(
        img1, cv2.COLOR_BGR2RGB))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
