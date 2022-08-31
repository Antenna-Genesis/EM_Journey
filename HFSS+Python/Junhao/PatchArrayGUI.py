# -*- coding: utf-8 -*-
from tkinter import Tk, Label, StringVar, Entry, Button, Frame
import pandas as pd
import PatchArrayMain
import CalcPatch
import Project
# import MyProblem

root = Tk()
root.title('矩形贴片天线同轴馈电')
root.geometry('560x280')
root.resizable(width=False, height=False)

frm = Frame(root)
frm.pack()

Label(frm, text='工作频率(GHz):').grid(row=0, column=0)
Label(frm, text='基质厚度(mm):').grid(row=1, column=0)
Label(frm, text='相对介电常数:').grid(row=2, column=0)
Label(frm, text='理论宽度(mm):').grid(row=0, column=2)
Label(frm, text='理论长度(mm):').grid(row=1, column=2)
Label(frm, text='馈电位置(mm):').grid(row=2, column=2)
Label(frm, text='优化相位(deg):').grid(row=3, column=2)


def calc():
    f = float(v1.get())
    h = float(v2.get())
    er = float(v3.get())
    patch = CalcPatch.Patch(f, h, er)
    patch.Calc()
    v4.set(patch.w)
    v5.set(patch.length)
    v6.set(patch.xf)


def hfss():
    f = float(v1.get())
    array = PatchArrayMain.PatchArray(f, [1, 1, 1, 1], [0, 0, 0, 0])
    array.size()
    array.call_hfss()


def GA():
    ObjV = pd.read_csv('C:/Users/tee/PycharmProjects/Result/ObjV.csv')
    Best = pd.read_csv('C:/Users/tee/PycharmProjects/Result/Phen.csv')
    col_name = list(ObjV.columns)
    phase = Best.iloc[ObjV[str(col_name[0])].idxmin(), 0]
    Project.Prj(0, phase, phase * 2.0, phase * 3.0, phase * 4.0, phase * 5.0, phase * 6.0, phase * 7.0)
    v7.set(0)
    v8.set(round(phase, 3))
    v9.set(round(phase * 2, 3))
    v10.set(round(phase * 3, 3))
    v11.set(round(phase * 4, 3))
    v12.set(round(phase * 5, 3))
    v13.set(round(phase * 6, 3))
    v14.set(round(phase * 7, 3))


v1 = StringVar()
Entry(frm, textvariable=v1, width=8).grid(row=0, column=1, padx=10, pady=5)
v2 = StringVar()
Entry(frm, textvariable=v2, width=8).grid(row=1, column=1, padx=10, pady=5)
v3 = StringVar()
Entry(frm, textvariable=v3, width=8).grid(row=2, column=1, padx=10, pady=5)

v4 = StringVar()
Label(frm, textvariable=v4, width=12).grid(row=0, column=3)
v5 = StringVar()
Label(frm, textvariable=v5, width=12).grid(row=1, column=3)
v6 = StringVar()
Label(frm, textvariable=v6, width=12).grid(row=2, column=3)

v7 = StringVar()
Label(frm, textvariable=v7, width=12).grid(row=3, column=3)
v8 = StringVar()
Label(frm, textvariable=v8, width=12).grid(row=3, column=4)
v9 = StringVar()
Label(frm, textvariable=v9, width=12).grid(row=4, column=3)
v10 = StringVar()
Label(frm, textvariable=v10, width=12).grid(row=4, column=4)
v11 = StringVar()
Label(frm, textvariable=v11, width=12).grid(row=5, column=3)
v12 = StringVar()
Label(frm, textvariable=v12, width=12).grid(row=5, column=4)
v13 = StringVar()
Label(frm, textvariable=v13, width=12).grid(row=6, column=3)
v14 = StringVar()
Label(frm, textvariable=v14, width=12).grid(row=6, column=4)

Button(frm, text='calc', command=calc).grid(row=4, column=0)
Button(frm, text='hfss', command=hfss).grid(row=4, column=1)
Button(frm, text='GA', command=GA).grid(row=5, column=0)
root.mainloop()
