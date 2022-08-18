from ShrtCde import *
from tkinter.scrolledtext import ScrolledText
from tkinter.colorchooser import askcolor
from tkinter.dialog import Dialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
from os.path import abspath, dirname, isfile, join, splitext
from os import getcwd, system
from sys import argv

here = abspath(dirname(__file__))
path = ''
def main():
    config = here + r"\.PeYxconfig"
    if not isfile(config) or readf(config, 'r') == '': writef(config, ["Arial~20~#000000~#FFFFFF~#0080ff"], 'w')
    font = readf(config, 'r').split('~')

    global mainFont
    mainFont = [font[0], int(font[1])]
    global foreground
    foreground = font[2]
    global foregroundb
    foregroundb = None
    global background
    background = font[3]
    global backgroundb
    backgroundb = None
    global highlight
    highlight = font[4]
    global highlightb
    highlightb = None
    global toolsFont
    toolsFont = [mainFont[0], 12]
    global root
    root = None
    global mainText
    mainText = None
    global textSize
    textSize = None
    global textFont
    textFont = None
    global oldText
    oldText = ''

    def openFile(temp=None):
        global path
        global oldText

        if temp == None: temp = askopenfilename(title="PeYx: Open File", defaultextension='.txt', initialdir=getcwd(), filetypes=(("All Files", '*.*'), ("Text File (.txt)", '.txt'), ("Python Source File (.py)", '.py'), ("C Source File (.c)", '.c'), ("C++ Source File (.cpp)", '.cpp'), ("C/C++ Header File (.h)", '.h'), ("Java Source File (.java)", '.java')))
        if isfile(temp):
            path = temp
            root.title(f'PeYx: {path}')

            data = readf(path, 'r')
            mainText.delete('0.0', 'end')
            mainText.insert('0.0', data)
            oldText = data + "#TOKEN"

    def save(saveas=False):
        global path
        
        if not isfile(path) or saveas:
            temp = asksaveasfilename(title="PeYx: Save File", defaultextension='.txt', initialdir=getcwd(), filetypes=(("All Files", '*.*'), ("Text File (.txt)", '.txt'), ("Python Source File (.py)", '.py'), ("C Source File (.c)", '.c'), ("C++ Source File (.cpp)", '.cpp'), ("C/C++ Header File (.h)", '.h'), ("Java Source File (.java)", '.java')))

            if temp != '': path = temp
            else: return

        root.title(f'PeYx: {path}')

        writef(path, mainText.get('0.0', 'end').split('\n')[:-1])
        openFile(path)

    def checkSave(destroy=True):
        if (not isfile(path) and mainText.get('0.0', 'end') != '\n') or (isfile(path) and readf(path, 'r').split('\n') != mainText.get('0.0', 'end').split('\n')[:-1]):
            dialog = Dialog(None, {'title': 'PeYx: Are you sure you want to quit?',
                            'text':
                            f'File "{path}" has been modified'
                            ' since the last time it was saved.'
                            ' Do you want to save it before'
                            ' exiting the application?',
                            'bitmap': 'warning',
                            'default': 0,
                            'strings': ('Save File',
                                        'Discard Changes',
                                        'Cancel')})
            
            if dialog.num == 0: save()
            elif dialog.num == 2: return 1
        
        if destroy:
            root.destroy()
            quit(0)
    
    def newFile():
        global path
        if checkSave(False) == 1: return

        path = ''
        root.title('PeYx')
        mainText.delete('0.0', 'end')

    def saveFont(): writef(config, [f"{mainFont[0]}~{mainFont[1]}~{foreground}~{background}~{highlight}"], 'w')

    def changeFontSize(v=None):
        global mainFont

        if v == None: mainFont[1] = int(textSize.get())
        else:
            if mainFont[1] + v < 10 or mainFont[1] + v > 50: return

            mainFont[1] += v
            textSize.set(str(mainFont[1]))

        saveFont()
        mainText.config(font=mainFont)
        mainText.tag_configure('highlight', font=mainFont)
    
    def changeFontFamily(n):
        global mainFont

        mainFont[0] = textFont.get()
        toolsFont[0] = textFont.get()
        saveFont()
        generateUI()

    def changeColor(mode='0'):
        global foreground
        global background
        global highlight

        if mode == '0': color = foreground
        if mode == '1': color = highlight
        else: color = background

        color = askcolor(color)
        if color != (None, None):
            if mode == '0':
                foreground = color[1]
                foregroundb.config(bg=foreground)
                mainText.config(fg=foreground, insertbackground=foreground)
            elif mode == '1':
                highlight = color[1]
                highlightb.config(bg=highlight)
                mainText.tag_configure('highlight', foreground=highlight)
            else:
                background = color[1]
                backgroundb.config(bg=background)
                mainText.config(bg=background)
            saveFont()

    def runPython():
        if not isfile(path) or (isfile(path) and readf(path, 'r').split('\n') != mainText.get('0.0', 'end').split('\n')[:-1]):
            showerror("PeYx", "File must be saved before execution.")
            return
        
        if splitext(path)[1] != '.py':
            showerror("PeYx", "Only Python files (.py) can be run by PeYx.")
            return
        
        system(f'python "{path}"')
    
    def updateText():
        global oldText

        if splitext(path)[1] == '.py' and (oldText != mainText.get('0.0', 'end') or oldText.endswith('#TOKEN')):
            keys = ['False', 'class', 'from', 'or', 'None', 'continue', 'global', 'pass', 'True', 'def', 'if', 'raise', 'and', 'del', 'import', 'return', 'as', 'elif', 'in', 'try', 'assert', 'else', 'is' 'while', 'async', 'except', 'lambda', 'with', 'await', 'finally', 'nonlocal', 'yield', 'break', 'for', 'not']
            for i, v in enumerate(mainText.get('0.0', 'end').split('\n'), 0):
                wordSplit = v.split(' ')
                start = 0
                for v2 in wordSplit:
                    if v2 in keys: mainText.replace(f'{i+1}.{start}', f'{i+1}.{start+len(v2)}', v2, 'highlight')
                    elif v2[:-1] in keys and v2[-1] == ':':
                        mainText.replace(f'{i+1}.{start}', f'{i+1}.{start+len(v2)}', v2[:-1], 'highlight')
                        mainText.insert(f'{i+1}.{start+len(v2)-1}', v2[-1])
                    elif v2.startswith('if('): mainText.replace(f'{i+1}.{start}', f'{i+1}.{start+2}', v2[:2], 'highlight')
                    elif v2.startswith('elif('): mainText.replace(f'{i+1}.{start}', f'{i+1}.{start+4}', v2[:4], 'highlight')
                    else: mainText.replace(f'{i+1}.{start}', f'{i+1}.{start+len(v2)}', v2)
                    
                    start += len(v2) + 1
            
            oldText = mainText.get('0.0', 'end')
    
        root.after(1000, updateText)

    def generateUI():
        global path
        global root
        global mainText
        global textSize
        global textFont
        global foregroundb
        global backgroundb
        global highlightb

        if root != None: root.destroy()

        title = 'PeYx'
        if path != '': title = f'PeYx: {path}'

        root = mkRoot(title, "1105x500", f'{here}\\main.png')
        fonts = ['Arial', 'Arial Black', 'Arial CE', 'Arial CYR', 'Arial TUR', 'Bahnschrift', 'Bodoni Bd BT', 'Calibri', 'Cambria', 'Candara', 'Cascadia Code', 'Cascadia Mono', 'CentSchbkCyrill BT', 'Century725 Cn BT', 'Comic Sans MS', 'Consolas', 'Constantia', 'Corbel', 'Courier', 'Courier New', 'DeVinne Txt BT', 'Ebrima', 'Embassy BT', 'EngraversGothic BT', 'Exotc350 Bd BT', 'Fixedsys', 'Franklin Gothic Medium', 'Freehand521 BT', 'Futura Bk BT', 'Gabriola', 'Gadugi', 'Geometr212 BkCn BT', 'Georgia', 'Humanst521 BT', 'Impact', 'Ink Free', 'Javanese Text', 'Kaufmann BT', 'Leelawadee UI', 'Lucida Console', 'Lucida Sans Unicode', 'MS Gothic', 'MS Sans Serif', 'MS Serif', 'MV Boli', 'Malgun Gothic', 'Marlett', 'Microsoft Himalaya', 'Microsoft JhengHei', 'Microsoft New Tai Lue', 'Microsoft PhagsPa', 'Microsoft Sans Serif', 'Microsoft Tai Le', 'Microsoft YaHei', 'Microsoft Yi Baiti', 'MingLiU-ExtB', 'Modern', 'Mongolian Baiti', 'Myanmar Text', 'News701 BT', 'NewsGoth BT', 'OCR-A BT', 'Palatino Linotype', 'Roman', 'Schadow BT', 'Script', 'Segoe Print', 'Segoe Script', 'Segoe UI', 'SimSun', 'Sitka Text', 'Small Fonts', 'Square721 BT', 'Swis721 Blk BT', 'Sylfaen', 'Symbol', 'System', 'Tahoma', 'Terminal', 'Times New Roman', 'Trebuchet MS', 'TypoUpright BT', 'Verdana', 'Webdings', 'Wingdings', 'Yu Gothic']
        
        tools = Frame(root, height=125, bg='white', highlightbackground='dark grey', highlightthickness=1)
        tools.pack(fill='x', expand=1)

        scrollH = Scrollbar(root, orient=HORIZONTAL)
        scrollH.pack(side=BOTTOM, fill='x', expand=1)

        mainText = ScrolledText(root, width=10000, height=10000, font=mainFont, fg=foreground, bg=background, insertbackground=foreground, undo=True, wrap='none', xscrollcommand=scrollH.set, tabs=mkFont(mainFont[0], mainFont[1]).measure('    ')); mainText.pack()
        mainText.tag_configure('highlight', foreground=highlight, font=mainFont)
        scrollH.config(command=mainText.xview)

        fileTools = Frame(tools, width=100, height=25, bg='white', highlightbackground='black', highlightthickness=1)
        fileTools.grid(row=0, column=0)

        Label(fileTools, font=toolsFont, text="FILE  ", bg='white').grid(row=0, column=0)
        Button(fileTools, font=toolsFont, text='Open', width=9, command=openFile).grid(row=0, column=1)
        Button(fileTools, font=toolsFont, text='New', width=9, command=newFile).grid(row=0, column=2)
        Button(fileTools, font=toolsFont, text='Save', width=9, command=save).grid(row=0, column=3)
        Button(fileTools, font=toolsFont, text='Save as', width=9, command=lambda:save(True)).grid(row=0, column=4)

        textTools = Frame(tools, width=100, bg='#f2f2f2', highlightbackground='black', highlightthickness=1)
        textTools.grid(row=0, column=3, padx=3)

        textSize = StringVar(textTools)
        textFont = StringVar(textTools)

        Label(textTools, font=toolsFont, text="WINDOW  ").grid(row=0, column=0)
        Spinbox(textTools, from_=10, to=50, textvariable=textSize, font=toolsFont, width=5, command=changeFontSize).grid(row=0, column=1)
        m = OptionMenu(textTools, textFont, *fonts, command=changeFontFamily); m.grid(row=0, column=2, padx=5)
        backgroundb = Button(textTools, text='   ', font=toolsFont, bg=background, command=lambda:changeColor('2')); backgroundb.grid(row=0, column=3)
        foregroundb = Button(textTools, text='   ', font=toolsFont, bg=foreground, command=changeColor); foregroundb.grid(row=0, column=4)
        textFont.set(mainFont[0])
        textSize.set(mainFont[1])

        pythonTools = Frame(tools, width=100, bg='#f2f2f2', highlightbackground='black', highlightthickness=1)
        pythonTools.grid(row=0, column=4)

        Label(pythonTools, font=toolsFont, text="PYTHON ").grid(row=0, column=0)
        Button(pythonTools, font=toolsFont, text='Run', width=9, command=runPython).grid(row=0, column=1, padx=5)
        highlightb = Button(pythonTools, text='   ', font=toolsFont, bg=highlight, command=lambda:changeColor('1')); highlightb.grid(row=0, column=2)

        m.config(font=(toolsFont[0], 11), width=20)
        for i in range(m['menu'].index('end')): m['menu'].entryconfig(i, font=(fonts[i], 11))

        if isfile(path): openFile(path)

        updateText()

        root.bind('<Control-n>', lambda n:newFile())
        root.bind('<Control-s>', lambda n:save())
        root.bind('<Control-s>a', lambda n:save(True))
        root.bind('<Control-q>', lambda n:changeFontSize(1))
        root.bind('<Control-e>', lambda n:changeFontSize(-1))
        root.bind('<Control-o>', lambda n: openFile())
        root.bind('<F5>', lambda n:runPython())
        root.protocol('WM_DELETE_WINDOW', checkSave)
        root.mainloop()
    
    generateUI()

if __name__ == '__main__':
    if len(argv) > 1:
        argvPath = argv[1]
        if isfile(argvPath): path = argvPath
        elif isfile(join(getcwd(), argvPath)): path = join(getcwd(), argvPath)
        else: quit(0)
    main()