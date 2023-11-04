import glob
from PIL import Image
import cv2
import natsort

files = glob.glob('./../images/test_kei/*')
for i in natsort.natsorted(files):
    print(i)
    img = cv2.imread(i)
    cv2.imshow(i, img)
    cv2.waitKey()
    cv2.destroyAllWindows()