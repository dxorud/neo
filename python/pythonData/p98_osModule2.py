import os

myfolder = './'
newpath = os.path.join(myfolder, 'work')

try:
    os.rmdir(path=newpath)
    for idx in range(1, 11):
        newfile = os.path.join(myfolder, 'somefolder' + str(idx).zfill(2))
        os.rmdir(newfile)
except FileExistsError:
    print("Directory already exists")
finally:
    print("Done~!!")