__author__ = 'vuvantu'
import Tkinter
from Tkinter import *
from tkFileDialog   import askopenfilename
import tkMessageBox
from tkMessageBox import showinfo, showwarning, showerror

import os
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy as np
import Utils

class App(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.geometry("600x400+200+200")
        self.grid()

        self.inputFileLabel = Tkinter.Label(self, text = "Input file name wav", anchor = W ,justify = LEFT)
        self.inputFileLabel.place(x = 50, y = 50, width = 350, height = 25)

        self.chooseFile = Tkinter.Button(self, text = "Choose File", anchor = W, command = self.openChooseFileDialog)
        self.chooseFile.place(x = 450, y = 50, width = 100, height = 25)

        self.inputWsLabel = Tkinter.Label(self, text =  "Window size", anchor = W)
        self.inputWsLabel.place(x = 50, y = 100, width = 100, height = 25)


        self.inputWs = Tkinter.Entry(self)
        self.inputWs.place(x = 150, y = 100, width = 40, height = 25)

        self.inputWsLabelMs = Tkinter.Label(self, text =  "Ms",anchor = W)
        self.inputWsLabelMs.place(x = 200, y = 100, width = 40, height = 25)

        self.WTLabel = Tkinter.Label(self, text = "Choose window type", anchor = W)
        self.WTLabel.place(x = 50, y = 150, width = 150, height = 25)

        self.var = IntVar()
        self.var.set(1)
        R1 = Radiobutton(self, text="Hamming ", variable=self.var, value=1,
                          command=self.sel, anchor = W)
        R1.place(x = 70, y = 180, width = 100, height = 25)

        R2 = Radiobutton(self, text="Hanning ", variable=self.var, value=2,
                          command=self.sel, anchor = W)
        R2.place(x = 70, y = 210, width = 100, height = 25)

        R3 = Radiobutton(self, text="Rectangle", variable=self.var, value=3,
                          command=self.sel, anchor = W)
        R3.place(x = 70, y = 240, width = 100, height = 25)


        self.button = Tkinter.Button(self, text = u"Run", command = self.process)
        self.button.place(x = 50, y = 350, width = 100, height = 25)

        # output message
        self.S = Scrollbar(self)
        self.T = Text(self)
        self.S.place(x = 250, y = 100)
        self.T.place(x = 250, y = 100, width = 300, height = 280)
        self.S.config(command = self.T.yview)
        self.T.config(yscrollcommand = self.S.set)

        self.inputFilename = ""
        self.frame_size_ms = ""
        self.windowTypeInt = 0
        self.windowTypeStr = ""

        self.count  = 0

    def sel(self):
        self.windowTypeInt = self.var.get()
        return

    def openChooseFileDialog(self):
        name = askopenfilename()
        self.inputFilename = name
        self.inputFileLabel.config(text = os.path.basename(self.inputFilename))
        self.inputFileLabel.update_idletasks()
        print os.path.basename(self.inputFilename)
        return

    def checkUserVariable(self):

        if self.inputWs.get() == "":
            showerror("Error", "Please enter frame size in ms")
            return False
        self.frame_size_ms = int(self.inputWs.get())
        if(self.frame_size_ms < 10 or self.frame_size_ms > 25):
            showwarning("Error", "Please enter frame size from 10 to 25 ms")
            return False

        if self.windowTypeInt == 0:
            self.windowTypeStr = "Hamming"
        elif self.windowTypeInt == 1:
            self.windowTypeStr = "Hamming"
        else:
            self.windowTypeStr = "Rectangle"

        return True

    def process(self, filename = "4-mowtows.wav", frame_size_ms = 10, windows_type = "Hamming"):
        if not self.checkUserVariable():
            print "User input invalid"
            return

        self.count += 1
        filename = self.inputFilename
        frame_size_ms = self.frame_size_ms
        windows_type = self.windowTypeStr

        print "Enter run..."
        message = "Running...\n"
        self.T.insert(END, message)

        message = ""
        print "File name: %s " % filename
        message = "File name: " + os.path.basename(filename) + "\n"
        self.T.insert(END, message)
        print "Frame_size_ms: %d" % frame_size_ms
        message = "Frame size: " + str(frame_size_ms) + " milisecond\n"
        self.T.insert(END, message)
        print "Window Type: %s" % windows_type
        message = "Window Type: " + windows_type + "\n"
        self.T.insert(END, message)

        try:
            sample_rate , s = read(filename)
        except:
            showerror("Error", "Find not found, please choose .wav file")
            return

        T_s = 1000.0 / sample_rate #ms
        L = len(s)
        print "Tan so lay mau: %d mau trong 1 giay " % sample_rate
        message = "So mau lay trong 1 giay: " + str(sample_rate) + "\n"
        self.T.insert(END,message)
        print "Chu ki mau %0.2f ms" % T_s

        print "So luong mau %d" % L
        message = "So luong mau: " + str(L) + "\n"
        self.T.insert(END,message)


        print "T_0 = 0, T_max = %0.2f" % (L * T_s)
        frame_size = sample_rate * frame_size_ms / 1000
        print "frame_size = %d" % frame_size
        message = "Frame size : " + str(frame_size) + " mau\n"
        self.T.insert(END, message)


        if windows_type == "Hammiing":
            windows = Utils.hamming(frame_size)
        elif windows_type == "Hanniing" :
            windows = Utils.hanning(frame_size)
        else:
            windows = Utils.rectangle(frame_size)

        L_max = 2 * L / frame_size # so diem tinh nang luong

        message = "So diem tinh: " + str(L_max) +  "\n"
        self.T.insert(END, message)

        print "Tinh nang luong"
        print "So diem tinh nang luong : %d" % L_max
        message = "Tinh nang luong...\n"
        self.T.insert(END, message)
        energy = np.zeros(L_max, dtype=float)
        for i in range(L_max):
            energy[i] = 0

            begin = i * frame_size / 2
            end = begin + frame_size
            j = begin
            n = 0
            while j < end :
                if j > L-1:
                    energy[i] += 0
                else :
                    energy[i] +=(s[j] * windows[frame_size - 1 - n]) **2
                j += 1
                n += 1

        print "Tinh Bien do"
        message = "Tinh bien do trung binh...\n"
        self.T.insert(END, message)


        print "So diem tinh bien do : %d" % L_max
        magnitude = np.zeros(L_max, dtype=float)
        for i in range(L_max):
            magnitude[i] = 0

            begin = i * frame_size / 2
            end = begin + frame_size
            j = begin
            n = 0
            while j < end :
                if j > L-1:
                    magnitude[i] += 0
                else :
                    magnitude[i] += abs(s[j]) * windows[frame_size - 1 - n]
                j += 1
                n += 1

        print "Tinh ti le bien thien qua gia tri 0"
        message = "Tinh ti le bien thien qua gia tri 0...\n"
        self.T.insert(END, message)

        zero_crossing_rate = np.zeros(L_max, dtype=float)
        for i in range(L_max):
            zero_crossing_rate[i] = 0

            begin = i * frame_size / 2
            end = begin + frame_size
            j = begin + 1
            n = 0
            while j < end :
                if j > L-1:
                    zero_crossing_rate[i] += 0
                else :
                    zero_crossing_rate[i] += abs( Utils.sign(s[j]) - Utils.sign(s[j-1]) ) * windows[frame_size - 1 - n]
                j += 1
                n += 1
        x = np.zeros(L_max)
        for i in range(L_max):
            x[i] = (i+1) * frame_size / 2

        message = "\n\n\n"
        self.T.insert(END, message)
        plt.figure(num = self.count)
        plt.subplot(411)
        plt.ylabel("Wave")
        plt.plot(s, 'b')

        plt.subplot(412)
        plt.ylabel("Short-term energy")
        plt.plot(x, energy, 'r')

        #plt.figure(num = 2)
        plt.subplot(413)
        plt.ylabel("Average magnitude")
        plt.plot(x, magnitude, 'g')


        #plt.figure(num = 3)
        plt.subplot(414)
        plt.xlabel("ms")
        plt.ylabel("Zero crossing rate")
        plt.plot(x, zero_crossing_rate, 'y')


        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        fig = plt.gcf()
        title = "File: " + os.path.basename(self.inputFilename)+ "   Frame size: " + str(frame_size_ms) + "ms     Windows Type: " + windows_type
        fig.canvas.set_window_title(title)
        plt.show()

        return

if __name__ == "__main__":
    app = App(None)
    app.title("Signal speech processing")
    app.mainloop()