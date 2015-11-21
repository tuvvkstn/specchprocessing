from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy as np
import Utils


def process(filename = "4-mowtows.wav", frame_size_ms = 10, windows_type = "Hamming"):
    sample_rate , s = read(filename)
    T_s = 1000.0 / sample_rate #ms
    L = len(s)
    print "Tan so lay mau: %d mau trong 1 giay " % sample_rate
    print "Chu ki mau %0.2f ms" % T_s
    print "So luong mau %d" % L
    print "T_0 = 0, T_max = %0.2f" % (L * T_s)
    frame_size = sample_rate * frame_size_ms / 1000
    print "frame_size = %d" % frame_size



    if windows_type == "Hammiing":
        windows = Utils.hamming(frame_size)
    elif windows_type == "Hanniing" :
        windows = Utils.hanning(frame_size)
    else:
        windows = Utils.rectangle(frame_size)

    L_max = 2 * L / frame_size # so diem tinh nang luong
    print "Tinh nang luong"
    print "So diem tinh nang luong : %d" % L_max
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
    print "So diem tinh bien do : %d" % L_max
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

    plt.figure(num = 1)
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
    title = "Filename: " + filename + "   Frame size: " + str(frame_size_ms) + "ms     Windows Type: " + windows_type
    fig.canvas.set_window_title(title)
    plt.show()

    return

if __name__ == '__main__':
    process()