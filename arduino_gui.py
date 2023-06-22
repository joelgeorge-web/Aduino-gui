from tkinter import *
import serial.tools.list_ports
import functools

ports = serial.tools.list_ports.comports()
serialObj = serial.Serial()

root = Tk()
root.config(bg='grey')

def initComPort(index):
    currentPort = str(ports[index])
    comPortVar = str(currentPort.split(' ')[0])
    print(comPortVar)
    serialObj.port = comPortVar
    serialObj.baudrate = 115200
    serialObj.open()

for onePort in ports:
    comButton = Button(root, text=onePort, font=('Calibri', '13'), height=1, width=45,
                       command=functools.partial(initComPort, index=ports.index(onePort)))
    comButton.grid(row=ports.index(onePort), column=0)

dataCanvas = Canvas(root, width=1000, height=1000, bg='white')
dataCanvas.grid(row=0, column=1, rowspan=100)

vsb = Scrollbar(root, orient='vertical', command=dataCanvas.yview)
vsb.grid(row=0, column=2, rowspan=100, sticky='ns')

dataCanvas.config(yscrollcommand=vsb.set)

dataFrame = Frame(dataCanvas, bg="white")
dataCanvas.create_window((10, 0), window=dataFrame, anchor='nw')

def checkSerialPort():
    if serialObj.isOpen() and serialObj.in_waiting:
        recentPacket = serialObj.readline()
        recentPacketString = recentPacket.decode('utf').rstrip('\n')
        label = Label(dataFrame, text=recentPacketString)
        label.pack()  # or label.grid(...)
        # You can also store the labels in a list and manage them accordingly

        dataCanvas.yview_moveto(1.0)  # Scroll to the bottom of the canvas

    root.after(100, checkSerialPort)  # Schedule the next call to checkSerialPort after 100 milliseconds

# Start the initial call to checkSerialPort
root.after(100, checkSerialPort)

root.mainloop()
