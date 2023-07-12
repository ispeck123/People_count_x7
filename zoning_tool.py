import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from tkinter import filedialog


class Draw(tkinter.Frame):
    def __init__(self, master, img):
        tkinter.Frame.__init__(self, master=None)
        self.x = self.y = 0
        self.rect = None
        master.title('Draw Rectangle')

        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None

        self.im = img
        self.width, self.height = self.im.size

        self.tk_im = PIL.ImageTk.PhotoImage(self.im)
        self.canvas = tkinter.Canvas(master, width=self.width, height=self.height, cursor="cross")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)

        self.sbarv = tkinter.Scrollbar(self, orient=tkinter.VERTICAL)
        self.sbarh = tkinter.Scrollbar(self, orient=tkinter.HORIZONTAL)
        self.sbarv.config(command=self.canvas.yview)
        self.sbarh.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.sbarv.set)
        self.canvas.config(xscrollcommand=self.sbarh.set)

        self.canvas.grid(row=0, column=0, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        self.sbarv.grid(row=0, column=1, stick=tkinter.N + tkinter.S)
        self.sbarh.grid(row=1, column=0, sticky=tkinter.E + tkinter.W)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.canvas.config(scrollregion=(0, 0, self.width + 20, self.height + 20))
        self.master.mainloop()

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, fill="")

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def on_button_release(self, event):
        print("Strating point : (" + str(self.start_x) + "," + str(self.start_y) + ")")
        print("Ending point : (" + str(self.curX) + "," + str(self.curY) + ")")


class App:
    def __init__(self, window, window_title, video_source):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source)
        self.count = 0

        self.text = tkinter.StringVar()
        self.text.set("pause")
        self.btn_pause = tkinter.Button(window, textvariable=self.text, width=50, command=self.increment)
        self.btn_pause.pack(anchor=tkinter.CENTER, expand=True)

        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # self.btn_pause=tkinter.Button(window, textvariable = self.text, width=50, command=self.increment)
        # self.btn_pause.pack(anchor=tkinter.CENTER, expand=True)
        self.delay = 1
        self.play()
        self.window.mainloop()

    def increment(self):
        self.count = 1

    def play(self):
        if self.count == 0:
            self.update()
            self.text.set("pause")
            self.window.after(self.delay, self.play)
        else:
            self.pause()
            self.text.set("resume")

    def pause(self):
        ret, frame = self.vid.get_frame()
        if ret:
            img = PIL.Image.fromarray(frame)
            self.window.destroy()
            Draw(tkinter.Tk(), img)

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)


class MyVideoCapture:
    def __init__(self, video_source):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


class Main_page:
    def __init__(self):
        self.vid = None
        self.root = tkinter.Tk()
        self.root.title("Zone Co-ordinates finding tool")

        self.canvas1 = tkinter.Canvas(self.root, width=500, height=500, bg='azure3', relief='raised')
        self.canvas1.pack()

        self.label1 = tkinter.Label(self.root, text='Zone Co-ordinates finding tool', bg='azure3')
        self.label1.config(font=('helvetica', 25))
        self.canvas1.create_window(250, 50, window=self.label1)

        self.label2 = tkinter.Label(self.root, text='Select the video file ', bg='azure3')
        self.label2.config(font=('helvetica', 15))
        self.canvas1.create_window(250, 150, window=self.label2)

        self.vid_button = tkinter.Button(text="      Import mp4 file     ", command=self.get_video, bg='royalblue',
                                         fg='white', font=('helvetica', 12, 'bold'))
        self.canvas1.create_window(250, 200, window=self.vid_button)

        self.label3 = tkinter.Label(self.root, text='Enter rtsp stream ', bg='azure3')
        self.label3.config(font=('helvetica', 15))
        self.canvas1.create_window(250, 350, window=self.label3)

        self.rtsp_name = tkinter.StringVar()
        self.url_text_box = tkinter.Entry(self.root, width=50, textvariable=self.rtsp_name)
        self.canvas1.create_window(250, 400, window=self.url_text_box)

        self.rtsp_button = tkinter.Button(text="      Stream     ", command=self.stream, bg='royalblue', fg='white',
                                          font=('helvetica', 12, 'bold'))
        self.canvas1.create_window(250, 450, window=self.rtsp_button)

        self.root.mainloop()

    def get_video(self):
        self.vid = filedialog.askopenfilename()
        self.root.destroy()
        App(tkinter.Tk(), "Video player", self.vid)

    def stream(self):
        self.vid = self.url_text_box.get()
        self.root.destroy()
        App(tkinter.Tk(), "Video player", self.vid)


Main_page()
