import numpy as np
import cv2 as cv
import glob
import numpy as np

chessboardSize = (6, 8)
frameSize = (480, 640)


criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)


objp = np.zeros((chessboardSize[0]*chessboardSize[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboardSize[0],
                       0:chessboardSize[1]].T.reshape(-1, 2)

objPoints = []
imgPoints = []


# images = glob.glob('*.png')
# images = "D:\DMS\calibration"
images = glob.glob("D:/DMS/calibration/*.png")
# D:\DMS\calibration\Image__2018-10-05__10-29-04.png
for image in images:
    print(image)
    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

    if ret == True:
        objPoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgPoints.append(corners)

        cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(1000)

cv.destroyAllWindows()


##################CALIBRATION##################

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objPoints, imgPoints, frameSize, None, None)

print("Camera Calibrated: ", ret)
print("\nCamera Matrix: \n", cameraMatrix)
print("\nDistortion Parameter: \n", dist)
print("\nRotation Vectors: \n", rvecs)
print("\nTranslation Vectors: \n", tvecs)



# UNDISTORTED IMAGE

img = cv.imread('Boxes/b18p4.png')
h, w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(
    cameraMatrix, dist, (w, h), 1, (w, h))


dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('calibrationResult1.png', dst)

mapx, mapy = cv.initUndistortRectifyMap(
    cameraMatrix, dist, None, newCameraMatrix,(w,h),5)
dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

x, y, w, h = roi
dst = dst[y:y+h, x:x+h]
cv.imwrite('calibrationResult2.png', dst)


mean_error = 0

for i in range(len(objPoints)):
    imgPoints2,_ = cv.projectPoints(objPoints[i],rvecs[i],tvecs[i],cameraMatrix,dist)
    error = cv.norm(imgPoints[i],imgPoints2,cv.NORM_L2)/len(imgPoints2)
    mean_error +=error

print("\nTotal error: {}".format(mean_error/len(objPoints)))


# Image__2018-10-05__10-29-04.png

# import glob

# files = glob.glob("D:/DMS/calibration/*.png")
# print(files)