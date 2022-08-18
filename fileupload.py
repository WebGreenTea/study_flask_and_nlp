import js
import asyncio
import word_frequency
from js import document,FileReader
from pyodide import create_proxy

def readComplete(event):
    text = document.getElementById("textContent")
    text.innerText = event.target.result

def process_file(x):
    fileList = document.getElementById("upload").files

    for file in fileList:
        reader = FileReader.new()
        OnloadEvent = create_proxy(readComplete)
        reader.onload = OnloadEvent
        reader.readAsText(file)


def setup():
    fileEvent = create_proxy(process_file)

    e = document.getElementById("upload")
    e.addEventListener("change",fileEvent,False)

setup()