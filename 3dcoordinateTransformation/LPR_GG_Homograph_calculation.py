#
#  Calculating homography matrix between LPR and general camera to match radar position
#  Note: this requires opencv contrib to be installed
#
import os, sys
import numpy as np
import cv2 as cv
import argparse
argparser = argparse.ArgumentParser(description="parsing required args")
argparser.add_argument("--lpr", "-lprimg", required=True,  help="path to the lpr frame")
argparser.add_argument("--gg", "-ggimg", required=True, help="path to the gg frame")
argparser.add_argument("--loc", "-location", required=True, help="location code or abbreviation e.g. ver for verra  USA",
                       default="ver")
argparser.add_argument("--mmc", "-mmcount", default=15, help="min match count")
argparser.add_argument("--ktr", "-kdtree", default=1, help="lann kdtree index")
argparser.add_argument("--ntr", "-ntree", default=5, help="number of trees in the search algo")
argparser.add_argument("--nck", "-nchecks", default=1, help="number of checks")
argparser.add_argument("--sd", "-sdir", default="")

args = argparser.parse_args()
#



MIN_MATCH_COUNT = args.mmc
FLANN_INDEX_KDTREE = args.ktr
img1 = cv.imread(args.lpr, 0) # queryImage
img2 = cv.imread(args.gg, 0) # trainImage
# Initiate SIFT detector
try:
    sift = cv.SIFT_create()
except:
    print(" opencv does not contain SIFT; install opencv contrib")
    sys.exit()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = args.ntr)
search_params = dict(checks = 50)
flann = cv.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1,des2, k=2)
# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)

if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()
    h,w = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv.perspectiveTransform(pts,M)
    img2 = cv.polylines(img2,[np.int32(dst)], True, 255, 3, cv.LINE_AA)
else:
    print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
    matchesMask = None

fs = cv.FileStorage(os.path.join(args.sd, args.loc + "_homography_matrix.txt"), cv.FILE_STORAGE_WRITE)
fs.write("mat", M)

print("Calulation Finished with success!")


