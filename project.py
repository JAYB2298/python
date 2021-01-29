from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import cv2
import face_recognition
import os
import shutil
from tkinter import messagebox

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')

m = 5
n = 0
basepath = ""
faceEncoding = []
faceImg = {}
count = 0
similarFace = []
facePic = []
flag3 = False


def selectDirectory(root, canvas, scroll_x, scroll_y, frame):
    global basepath, faceEncoding, faceImg, count, facePic, similarFace, flag3, m, n
    faceEncoding = []
    faceImg = {}
    count = 0
    similarFace = []
    facePic = []

    basepath = filedialog.askdirectory(parent=root,
                                       initialdir=os.getcwd(),
                                       title="Please select a folder:")
    print(basepath)
    if (flag3):
        canvas.delete("all")
        frame = Frame(canvas)
        m = 5
        n = 0

    flag3 = True

    showDirectoryImages(root, canvas, scroll_x, scroll_y, frame)


def get_encodings(imagePath):
    img = cv2.imread(imagePath)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faces = face_cascade.detectMultiScale(grey, scaleFactor=1.3, minNeighbors=8)
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5)

    print(len(faces))
    if (len(faces) == 1):
        print("1 face")
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in faces]

        encoding = face_recognition.face_encodings(rgb, boxes)[0]
        # print(type(encoding[0]))
        # print(encoding)
        return encoding, faces, rgb
    else:
        # print(len(faces)+" Faces")
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in faces]

        encoding = face_recognition.face_encodings(rgb, boxes)
        # print(type(encoding))
        return encoding, faces, rgb


def classify(basepath):
    global count

    for entry in os.listdir(basepath):
        if os.path.isdir(os.path.join(basepath, entry)):
            print(entry)
        elif os.path.isfile(os.path.join(basepath, entry)):
            print(entry)
            if (entry.endswith("jpg") or entry.endswith("JPG")):

                temp1, faces, imgx = get_encodings(basepath + "/" + entry)

                if (len(faceEncoding) == 0):

                    if (type(temp1) == list):
                        flag = 0
                        for i in temp1:
                            faceEncoding.append(i)
                            x, y, w, h = faces[flag]
                            flag = flag + 1
                            img1 = imgx[y:y + h, x:x + w]
                            # cv2.imwrite(f"{count}.jpg", img1)
                            facePic.append(img1)
                            faceImg[count] = [entry]
                            count = count + 1


                    else:
                        faceEncoding.append(temp1)
                        x, y, w, h = faces[0]
                        img1 = imgx[y:y + h, x:x + w]
                        # cv2.imwrite(f"{count}.jpg", img1)
                        facePic.append(img1)
                        faceImg[count] = [entry]
                        count = count + 1

                else:
                    if (type(temp1) == list):
                        count1 = 0
                        for face_encoding in temp1:
                            matches = face_recognition.compare_faces(faceEncoding, face_encoding, tolerance=0.5)

                            if any(matches):
                                index = matches.index(True)
                                print("Match1")
                                temp2 = faceImg[index]
                                temp2.append(str(entry))
                                faceImg[index] = temp2
                                print(len(faceEncoding))
                                print(faceImg)
                                count1 = count1 + 1

                            else:
                                print("Not Matched")
                                faceEncoding.append(face_encoding)
                                faceImg[count] = [entry]
                                x, y, w, h = faces[count1]
                                img1 = imgx[y:y + h, x:x + w]
                                # cv2.imwrite(f"{count}.jpg", img1)
                                facePic.append(img1)
                                count = count + 1
                                count1 = count1 + 1
                                print(len(faceEncoding))
                                print(faceImg)

                    else:
                        matches = face_recognition.compare_faces(faceEncoding, temp1, tolerance=0.5)
                        if any(matches):
                            index = matches.index(True)
                            print("Match1")
                            temp2 = faceImg[index]
                            temp2.append(str(entry))
                            faceImg[index] = temp2
                            print(len(faceEncoding))
                            print(faceImg)

                        else:
                            print("Not Matched")
                            faceEncoding.append(temp1)
                            faceImg[count] = [entry]
                            x, y, w, h = faces[0]
                            img1 = imgx[y:y + h, x:x + w]
                            # cv2.imwrite(f"{count}.jpg", img1)
                            facePic.append(img1)
                            count = count + 1

                            print(len(faceEncoding))
                            print(faceImg)


def showFace(window, key):
    m = 5
    n = 0
    window1 = Toplevel(window)

    canvas = Canvas(window1)
    scroll_y = Scrollbar(window1, orient="vertical", command=canvas.yview)
    scroll_y.pack(fill='y', side='right')
    scroll_x = Scrollbar(window1, orient="horizontal", command=canvas.xview)
    scroll_x.pack(fill='x', side='bottom')

    frame = Frame(canvas)

    # key=int(key)
    list3 = faceImg[key]

    btn3 = Button(window1, text="Save into Folder", command=lambda: saveSimilarFace(window1, list3))
    # btn3.grid(row=0, column=2)
    btn3.pack()

    for i in list3:
        im = Image.open(basepath + "/" + i)
        im = im.resize((150, 150), Image.ANTIALIAS)

        tkimage = ImageTk.PhotoImage(im)

        panel = Label(frame, image=tkimage)

        # set the image as img
        panel.image = tkimage
        panel.grid(row=m, column=n)
        n = n + 1
        if (n % 10 == 0):
            m = m + 1
            n = 0

    canvas.create_window(5, 0, anchor='nw', window=frame)
    canvas.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox('all'),
                     yscrollcommand=scroll_y.set,
                     xscrollcommand=scroll_x.set)

    canvas.pack(fill='both', expand=True, side='left')


def showError():
    messagebox.showerror("error", "Please Select Directory First")


def showClassify(root):
    if (basepath == ''):
        showError()
        return

    k = 1
    l = 0
    classify(basepath)
    window = Toplevel(root)
    canvas = Canvas(window)
    scroll_y = Scrollbar(window, orient="vertical", command=canvas.yview)
    scroll_y.pack(fill='y', side='right')
    scroll_x = Scrollbar(window, orient="horizontal", command=canvas.xview)
    scroll_x.pack(fill='x', side='bottom')
    frame = Frame(canvas)

    for i in faceImg.keys():
        im = Image.fromarray(facePic[i])
        im = im.resize((150, 150), Image.ANTIALIAS)

        tkimage = ImageTk.PhotoImage(im)
        imageButton = Button(frame, image=tkimage, command=lambda i=i: showFace(window, i))  # here
        imageButton.image = tkimage
        imageButton.grid(row=k, column=l)

        l = l + 1
        if (l % 10 == 0):
            l = 0
            k = k + 1

    canvas.create_window(5, 0, anchor='nw', window=frame)
    canvas.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox('all'),
                     yscrollcommand=scroll_y.set,
                     xscrollcommand=scroll_x.set)

    canvas.pack(fill='both', expand=True, side='left')


def search(root):
    if (basepath == ''):
        showError()
        return

    window = Toplevel(root)

    text = Label(window, text="Please select that person's image that you want to search:")
    # text.grid(row=1, column=2)
    text.pack()
    btn3 = Button(window, text="Browse", command=lambda: selectOneImage(window))
    # btn3.grid(row=1, column=5)
    btn3.pack()


def saveSimilarFace(window1, list1):
    global basepath
    destinationFolder = filedialog.askdirectory(parent=window1,
                                                initialdir=os.getcwd(),
                                                title="Please select a destination folder:")
    for img in list1:
        shutil.copy(basepath + "/" + img, destinationFolder)


def selectOneImage(window):
    my_filetypes = [('image', '.jpg'), ('image', '.JPG')]

    answer = filedialog.askopenfilename(parent=window,
                                        initialdir=os.getcwd(),
                                        title="Please select a image:",
                                        filetypes=my_filetypes)
    matchedFaces(answer)

    m = 4
    n = 0
    window1 = Toplevel(window)
    btn5 = Button(window1, text="Save into Folder", command=lambda: saveSimilarFace(window1, similarFace))
    # btn5.grid(row=0, column=2)
    btn5.pack()

    canvas = Canvas(window1)
    scroll_y = Scrollbar(window1, orient="vertical", command=canvas.yview)
    scroll_y.pack(fill='y', side='right')
    scroll_x = Scrollbar(window1, orient="horizontal", command=canvas.xview)
    scroll_x.pack(fill='x', side='bottom')

    frame = Frame(canvas)

    for i in similarFace:
        im = Image.open(basepath + "/" + i)
        im = im.resize((150, 150), Image.ANTIALIAS)

        tkimage = ImageTk.PhotoImage(im)

        panel = Label(frame, image=tkimage)

        # set the image as img
        panel.image = tkimage
        panel.grid(row=m, column=n)
        n = n + 1
        if (n % 10 == 0):
            m = m + 1
            n = 0

    canvas.create_window(5, 0, anchor='nw', window=frame)
    canvas.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox('all'),
                     yscrollcommand=scroll_y.set,
                     xscrollcommand=scroll_x.set)

    canvas.pack(fill='both', expand=True, side='left')


def matchedFaces(path):
    global similarFace
    similarFace = []
    sample, temp7, temp8 = get_encodings(path)

    if (type(sample) == list):
        for entry in os.listdir(basepath):
            if os.path.isdir(os.path.join(basepath, entry)):
                print(entry)
            elif os.path.isfile(os.path.join(basepath, entry)):
                print(entry)
                if (entry.endswith("jpg") or entry.endswith("JPG")):
                    x, q, o = get_encodings(basepath + "/" + entry)
                    if (type(x) == list):
                        for j in x:
                            matches = face_recognition.compare_faces(sample, j, tolerance=0.5)
                            if any(matches):
                                print("match")
                                print(entry)
                                similarFace.append(entry)
                                break
                    else:

                        matches = face_recognition.compare_faces(sample, x, tolerance=0.5)
                        if any(matches):
                            print("match")
                            similarFace.append(entry)

    else:
        for entry in os.listdir(basepath):
            if os.path.isdir(os.path.join(basepath, entry)):
                print(entry)
            elif os.path.isfile(os.path.join(basepath, entry)):
                print(entry)
                if (entry.endswith("jpg") or entry.endswith("JPG")):
                    x, q, o = get_encodings(basepath + "/" + entry)
                    if (type(x) == list):
                        for j in x:
                            matches = face_recognition.compare_faces([sample], j, tolerance=0.5)
                            if any(matches):
                                print("match")
                                print(entry)
                                similarFace.append(entry)
                                break
                    else:

                        matches = face_recognition.compare_faces([sample], x, tolerance=0.4)
                        if any(matches):
                            print("match")
                            similarFace.append(entry)


def homePage():
    root = Tk()
    canvas = Canvas(root)

    # Set Title as Image Loader
    root.title("Photo Gallery")

    # Set the resolution of window
    root.geometry("550x300")

    # Allow Window to be resizable
    root.resizable(width=True, height=True)

    scroll_y = Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_y.pack(fill='y', side='right')
    scroll_x = Scrollbar(root, orient="horizontal", command=canvas.xview)
    scroll_x.pack(fill='x', side='bottom')
    frame = Frame(canvas)

    btn4 = Button(root, text="Select Directory",
                  command=lambda: selectDirectory(root, canvas, scroll_x, scroll_y, frame))
    # btn4.grid(row=0, column=0)
    btn4.pack()

    btn1 = Button(root, text="Classify", command=lambda: showClassify(root))
    btn1.pack()
    # btn1.grid(row=0, column=1)

    btn2 = Button(root, text="Search Specific Person in the Directory", command=lambda: search(root))
    # btn2.grid(row=0, column=2)
    btn2.pack()

    root.mainloop()


def getFileName(image):
    print(str(image))


def showDirectoryImages(root, canvas, scroll_x, scroll_y, frame):
    global m, n

    for images in os.listdir(basepath):
        if images.endswith("jpg") or images.endswith("JPG"):

            im = Image.open(basepath + "/" + images)
            im = im.resize((150, 150), Image.ANTIALIAS)

            tkimage = ImageTk.PhotoImage(im)

            handler = lambda img=images: getFileName(img)  # here modify
            imageButton = Button(frame, image=tkimage, command=handler)  # here
            imageButton.image = tkimage
            imageButton.grid(row=m, column=n)

            n = n + 1
            if (n % 10 == 0):
                m = m + 1
                n = 0

    canvas.create_window(5, 0, anchor='nw', window=frame)
    canvas.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox('all'),
                     yscrollcommand=scroll_y.set,
                     xscrollcommand=scroll_x.set)

    canvas.pack(fill='both', expand=True, side='left')


homePage()
