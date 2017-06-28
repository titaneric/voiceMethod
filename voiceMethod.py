import tkinter as tk
import argparse
from speech2Text import Speech
import sys
import os

language_info = '''Assign the corresponding code of prefer language.
The default language is Chinese, Mandarin (Traditional, Taiwan).
The language supports:
國語（臺灣):  cmn-Hant-TW
한국어 (대한민국): ko-KR
日本語（日本): ja-JP
Español (España): es-ES
Français (France): fr-FR
Deutsch (Deutschland): de-DE
English (Great Britain): en-GB
English (United States): en-US
'''

punctuation_list = [" ", ",", ".", "?", ":",
                    ";", "~", "\\n", "\\'", '\\"',
                    "(", ")", "-", "+", "..."]

documents = []

string_buffer = ""

fileName = "./output.txt"

lang = 'cmn-Hant-TW'

newLine = False

mode = "v"

revised_line = ""

root = None

option = None

textDict = None


def produceSelection(index):
    global option
    if 1 <= index <= 10:
        code = '''
option{0} = tk.Entry(option, width='3')
option{0}.grid(row={2}, column={1})
option{0}.config(font=(None, 15))
option{0}.insert(0, "{0}")
        '''.format(index if 1 <= index <= 9 else 0,
                   2 * ((index - 1) % 5), (index - 1) // 5)
    elif 11 <= index <= 15:
        code = '''
option{0} = tk.Entry(option, width='3')
option{0}.grid(row={2}, column={1})
option{0}.config(font=(None, 15))
option{0}.insert(0, "{3}")
        '''.format(index, 2 * ((index - 1) % 5),
                   (index - 1) // 5, 'F{}'.format(index - 10))
    exec(code)


def insertText(index, text):
    global option
    code = '''
option{0} = tk.Entry(option, width='15')
option{0}.grid(row={3}, column={1})
option{0}.config(font=(None, 15))
option{0}.insert(0, "{2}")
    '''.format(index, 2 * ((index - 1) % 5) + 1, text, (index - 1) // 5)
    exec(code)


def shutdown(event):
    sys.stdout.write("\n")
    sys.stdout.flush()
    global fileName
    global documents
    global newLine
    global string_buffer
    documents.append(string_buffer)
    if newLine:
        documents.append("\n")
    with open(fileName, "w") as f:
        f.writelines(documents)

    sys.exit()


def changeMode(event, m):
    close(event)
    global mode
    mode = m


def input_method():
    global root
    global option
    global textDict
    global mode
    speech = Speech(language=lang)
    transcripts = speech.transcripts_list
    root = tk.Tk()
    option = tk.Frame(root)

    if transcripts:
        textDict = {(i + 1): transcript
                    for i, transcript in enumerate(transcripts)}
    else:
        textDict = {(i + 1): punctuation
                    for i, punctuation in enumerate(punctuation_list)}

    for index, text in textDict.items():
        produceSelection(index)
        insertText(index, text)

    option.bind("<Key>", key)
    option.bind("<q>", close)
    if mode == "v":
        option.bind("<z>", shutdown)
        option.bind("<e>", lambda event: changeMode(event, "e"))
    elif mode == "e":
        option.bind("<v>", lambda event: changeMode(event, "v"))
    option.focus_set()
    option.pack()
    root.mainloop()


def edit():
    global documents
    global string_buffer
    global revised_line
    global mode
    while True:
        sys.stdout.write('''
In edit mode.
Please input the lino what you want to edit: ''')
        sys.stdout.flush()
        lino = input()
        try:
            number = int(lino)
            number -= 1
            try:
                if 0 <= number < len(documents):
                    sys.stdout.write("Change #{0} to:\n[{0}] ".format(lino))
                    sys.stdout.flush()
                    while mode == "e":
                        input_method()
                    revised_line += "\n"
                    documents[number] = revised_line
                    revised_line = ""
                    os.system("clear")
                    printDocument()
                    break
            except IndexError:
                pass
        except ValueError:
            pass


def close(event):
    global root
    root.destroy()


def printDocument():
    global documents
    global string_buffer
    for i, document in enumerate(documents):
        sys.stdout.write("[{0}] {1}".format(i + 1, document))
    sys.stdout.write("[{0}] {1}".format(len(documents) + 1, string_buffer))
    sys.stdout.flush()


def key(event):
    global mode
    global documents
    global string_buffer
    global textDict
    global revised_line
    global root
    try:
        key_event = event.keysym
        select = int(key_event)
        try:
            entry = None
            if "\\" not in textDict[select if 1 <= select <= 9 else 10] \
                    and 0 <= select <= 9:
                entry = textDict[select if 1 <= select <= 9 else 10]
            elif textDict[select if 1 <= select <= 9 else 10] != "\\n":
                entry = textDict[select if 1 <= select <= 9 else 10][1:]
            else:
                entry = "\n"

            if mode == "v":
                string_buffer += entry

            if entry != "\n" and mode == "e":
                revised_line += entry

            sys.stdout.write("{}".format(entry))
            if entry == "\n" and mode == "v":
                documents.append(string_buffer)
                string_buffer = ""
                sys.stdout.write("[{}] ".format(len(documents) + 1))
            sys.stdout.flush()
            root.destroy()
        except KeyError:
            pass

    except ValueError:
        if key_event.startswith("F"):
            key_event = key_event.strip("F")
            select = 10 + int(key_event)
            try:
                entry = textDict[select]
                if mode == "v":
                    string_buffer += entry
                elif mode == "e":
                    revised_line += entry

                sys.stdout.write("{}".format(entry))
                sys.stdout.flush()
                root.destroy()
            except KeyError:
                pass
        else:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Voice input method',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--file", "-f", help="assign the output file name")
    parser.add_argument("--language", "-l", help=language_info)
    parser.add_argument("--newline", "-n", action="store_true",
                        help="append the newline to ducuments when terminating")
    args = parser.parse_args()

    if args.file:
        fileName = args.file
    if args.language:
        lang = args.language
    if args.newline:
        newLine = True

    sys.stdout.write("[1] ")
    sys.stdout.flush()

    while True:
        if mode == "v":
            input_method()
        elif mode == "e":
            edit()
