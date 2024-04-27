import tkinter
from tkinter import filedialog

import re

import os.path

import sys

filename = "Untitled"
fileexists = False

def asmtoint(asm):
    asm_split = re.split(" |, |\(|\)", asm)
    args = []
    for i in range (len(asm_split)):
        if (asm_split[i] != ""):
            args.append(asm_split[i])
    opcode = 0
    func = 0
    rd = 0
    rs = 0
    rt = 0
    imm = 0
    z=1
    instructions={"sll":"004","add":"014","sub":"024","nand":"034","nor":"044","bez":"1030","bnez":"1031","bgez":"1032","blez":"1033","bgz":"1034","blz":"1035","lw":"200","sw":"300"}
    for keys in instructions.keys():
        if(args[0]==keys):
            y=instructions[keys]
            k=keys
            z=0;
    if(z):
        raise ValueError("Invalid Instruction")
    opcode=int(y[0])
    func=int(y[1])
    length=int(y[2])

    if(k=="sw" or k=="lw"):
        if(len(args)!=3 and len(args)!=4):
            raise ValueError("Invalid Instruction Format")
    elif(len(args)!=length):
        raise ValueError("Invalid Instruction Format")
    
    if(args[0] == "sll" or args[0] == "add" or args[0] == "sub" or args[0] == "nand" or args[0] == "nor"):
        rd = int(args[1][1:]) if int(args[1][1:])<=7 else 10
        rs = int(args[2][1:]) if int(args[2][1:])<=7 else 10
        rt = int(args[3][1:]) if int(args[3][1:])<=7 else 10
        if(rd==10 or rs==10 or rt==10):
            raise ValueError("Invalid Register")
    elif(args[0] == "bez" or args[0] == "bnez" or args[0] == "bgez" or args[0] == "blez" or args[0] == "bgz" or args[0] == "blz"):
        rt = int(y[3])
        rs = int(args[1][1:]) if int(args[1][1:])<=7 else 10
        imm = int(args[2])
        if(rs==10 or rt==10):
            raise ValueError("Invalid Register")
    elif(args[0] == "lw"):
        if (args[-1] == ''):
            args = args[0:-1]
        rt = int(args[1][1:]) if int(args[1][1:])<=7 else 10
        if (len(args) == 3):
            imm = 0
            rs = int(args[2][1:]) if int(args[2][1:])<=7 else 10
            if(rs==10 or rt==10):
                raise ValueError("Invalid Register")
        else:
            imm = int(args[2])
            rs = int(args[3][1:]) if int(args[3][1:])<=7 else 10
            if(rs==10 or rt==10):
                raise ValueError("Invalid Register")
    elif (args[0] == "sw"):
        if (args[-1] == ''):
            args = args[0:-1]
        rt = int(args[1][1:]) if int(args[1][1:])<=7 else 10
        if (len(args) == 3):
            imm = 0
            rs = int(args[2][1:]) if int(args[2][1:])<=7 else 10
            if(rs==10 or rt==10):
                raise ValueError("Invalid Register")
        else:
            imm = int(args[2])
            rs = int(args[3][1:]) if int(args[3][1:])<=7 else 10
            if(rs==10 or rt==10):
                raise ValueError("Invalid Register")
    else:
        return 0,0,0,0,0,0
    
    return opcode, rs, rt, rd, func, imm

def inttohex(opcode, rs, rt, rd, func, imm):
    if (opcode == 0):
        opstr = format(opcode, '02b')
        rsstr = format(rs, '03b')
        rtstr = format(rt, '03b')
        rdstr = format(rd, '03b')
        fnstr = format(func, '05b')
        #print opstr, rsstr, rtstr, rdstr, fnstr
        instruction = opstr + rsstr + rtstr + rdstr + fnstr
    else :
        opstr = format(opcode, '02b')
        rtstr = format(rt, '03b')
        rsstr = format(rs, '03b')
        if (imm < 0):
            imm2s = ((-imm) ^ 255) + 1
            immstr = format(imm2s, '08b')
        else :
            immstr = format(imm, '08b')
        #print opstr, rtstr, rsstr, immstr
        instruction = opstr + rsstr + rtstr + immstr
    return format(int(instruction, 2), '04x')

def decode(asm):
    opcode, rs, rt, rd, func, imm = asmtoint(asm)
    instruction = inttohex(opcode, rs, rt, rd, func, imm)
    return instruction

def openFile():
    global filename
    openfilename = filedialog.askopenfilename()
    if openfilename is not None:
        filename = openfilename
        asmfile = open(filename, "r")
        asmfile.seek(0)
        asmdata = asmfile.read()
        textArea.delete("1.0", "end - 1c")
        textArea.insert("1.0", asmdata)
        asmfile.close()
        filemenu.entryconfig(filemenu.index("Save"), state = NORMAL)
        frame.title("muCPU Assembler [" + filename + "]")
        frame.focus()
    
def saveFile():
    global filename
    asmdata = textArea.get("1.0", "end - 1c")
    asmfile = open(filename, "w")
    asmfile.seek(0)
    asmfile.truncate()
    asmfile.write(asmdata)
    asmfile.close()

def saveFileAs():
    global filename
    global fileexists
    saveasfilename = filedialog.asksaveasfilename()
    if saveasfilename is not None:
        filename = saveasfilename
        fileexists = True
        asmdata = textArea.get("1.0", "end - 1c")
        asmfile = open(filename, "w")
        asmfile.seek(0)
        asmfile.truncate()
        asmfile.write(asmdata)
        asmfile.close()
        filemenu.entryconfig(filemenu.index("Save"), state = NORMAL)
        frame.title("muCPU Assembler [" + filename + "]")
        frame.focus()
    
        
def exitApp():
    frame.destroy()
    sys.exit()
    
def compileASM():
    global filename
    cpu_out = ""
    asm_in = textArea.get("1.0", "end")
    asmlines = re.split("\n", asm_in)
    for i in range (len(asmlines)):
        if (asmlines[i] != ""):
            #print asmlines[i]
            cpu_out += str(i) + " => x\"" + decode(asmlines[i]) + "\",\n"
    #print cpu_out
    name, ext = os.path.splitext(filename)
    hexfilename = name + ".hex"
    hexfile = open(hexfilename, "w")
    hexfile.seek(0)
    hexfile.truncate()
    hexfile.write(cpu_out)
    hexfile.close()
    
filedialog.Tk().withdraw()
frame = tkinter.Toplevel()

scrollbar = filedialog.Scrollbar(frame)
scrollbar.pack(side = "right", fill = "y")
frame.title("muCPU Assembler [" + filename + "]")
textArea = tkinter.Text(frame, height = 30, width = 100, padx = 3, pady = 3, yscrollcommand = scrollbar.set)
textArea.pack(side="right")
scrollbar.config(command=textArea.yview)

menubar = tkinter.Menu(frame)
filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile, state = "disabled")
filemenu.add_command(label="Save as...", command=saveFileAs)
filemenu.add_command(label="Exit", command=exitApp)
menubar.add_cascade(label="File", menu=filemenu)
runmenu = tkinter.Menu(menubar, tearoff=0)
runmenu.add_command(label="Compile", command=compileASM)
menubar.add_cascade(label="Run", menu=runmenu)
frame.config(menu=menubar)

frame.minsize(750, 450)
frame.maxsize(750, 450)
frame.mainloop()

#Sample counting loop code
"""
lw r4, 176(r0)
lw r3, 177(r0)
sub r2, r4, r1
bez r2, 8
sw r1, 252(r0)
bez r0, -8
add r1, r1, r3
sll r0, r0, r0
bez r0, -2
"""