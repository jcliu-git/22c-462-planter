import webbrowser
import os

#Main thread: check for human and display 
webbrowser.open('file://' + os.path.realpath('index.html'))