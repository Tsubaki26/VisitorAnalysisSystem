import glob
import os


files = glob.glob('./../images/test_kei/*')
print(files[0])

for i in range(len(files)):
    os.rename(files[i], "test_"+str(i)+".jpg")