from ast import Str
from tkinter.font import BOLD, Font
from pytube import YouTube
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from shutil import copyfile
import os

FolderName = Str()
filters = []
audio = None
def onComplete(stream, file):
    if(stream.type == "audio"):
        part = file.split(".mp4")[0]
        copyfile(file,part + ".mp3")
        os.remove(file)

def GetQualities():
    global filters
    global audio
    yt = None

    try:
        yt = YouTube(entryVar.get(), on_complete_callback=onComplete)
    except:
        return errorUrlLabel.config(text="Invalid Url", font=Font(weight=BOLD, size=12))
         
        

    filters = yt.streams.filter(type="video", progressive=True)
    audio = yt.streams.filter(only_audio=True).get_audio_only()


    choices = []
    for filter in filters:
        print(filter)
        choices.append(filter.resolution)


    choices.append("Audio Only")
    qualityCombo.config(values=choices)
    return errorUrlLabel.config(text="Valid Url", fg="green" ,font=Font(weight=BOLD, size=12))

def openLocation():
    global FolderName
    FolderName = filedialog.askdirectory()

    if(len(FolderName) > 0):
        fileLabel.config(text=FolderName, fg='green')
        errorFileLabel.config(text='')
    else:
        errorFileLabel.config(text='Please Choose a valid path', fg='red')
        fileLabel.config(text='')

def DownloadVideo():
    choice = qualityCombo.get()

    if(len(choice) < 1):
        return errorUrlLabel.config(text="Invalid Quality Choice", font=Font(weight=BOLD, size=12))
    else:
        if(choice == 'Audio Only'):
            select = audio
        else:
            for filter in filters:
                if(filter.resolution == choice):
                    select = filter
                    break

    #download function
    select.download(FolderName)
    if(choice == 'Audio Only'):
        pass#copyfile(FolderName + select.title + ".mp4", FolderName + select.title + ".mp3")

    errorUrlLabel.config(text="Download Completed!!", fg='green')


root = Tk()

root.iconbitmap(r'C:\\Users\\jk\Desktop\\py\\arrow.ico')
root.title("Youtube Downloader")
root.geometry('400x300+200+200')
root.resizable(False, False)
root.columnconfigure(0, weight=100)

urlLabel = Label(root, text="Enter the URL")
urlLabel.grid()


entryVar = StringVar()
urlEntry = Entry(root, width=50, textvariable= entryVar)
urlEntry.grid()

checkUrl = Button(root, text="Check URL", bg='dark red', fg="white", command=GetQualities)
checkUrl.grid()

errorUrlLabel = Label(root, text="", fg='red')
errorUrlLabel.grid()


fileLabel = Label(root, text="Choose where to save the file", font=Font(size=15, weight='bold'), )
fileLabel.grid()


fileButton = Button(root, text="Choose path", bg='dark red', fg="white", command=openLocation)
fileButton.grid()

errorFileLabel = Label(root, text="Choose path", fg='red')
errorFileLabel.grid()

qualityLabel = Label(root, text="Choose The Quality", font=Font(weight=BOLD), pady=12)
qualityLabel.grid()


qualityCombo = ttk.Combobox(root)
qualityCombo.grid()

Label('', pady=6).grid()

downloadButton = Button(root, text="Download", bg='dark red', fg='white', command=DownloadVideo)
downloadButton.grid()


root.mainloop()
