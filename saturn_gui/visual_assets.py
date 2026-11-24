"""Reference artwork for the existing Tk desktop shell; no solver dependency."""
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from functools import wraps
from PIL import Image, ImageTk, ImageOps

ATLAS = Path(__file__).with_name('assets') / 'saturn-atlas.webp'
LABELS = {'project':0,'projeto':0,'rotor':1,'bearings':2,'mancais':2,'loads':3,'cargas':3,'optimization':4,'otimização':4,'results':5,'resultados':5,'run':6,'execução':6}

def _image_icon(atlas, index):
    img = atlas.crop((18*index,414,18*(index+1),432)).convert('RGBA')
    img.putdata([(213,232,248,max(0,min(255,round((max(r,g,b)-85)*1.65)))) for r,g,b,a in img.getdata()])
    return img.resize((24,24),Image.Resampling.LANCZOS)

def apply_reference_assets(app):
    atlas=Image.open(ATLAS).convert('RGB')
    side=next((w for w in app.winfo_children() if isinstance(w,ttk.Frame) and str(w.cget('style'))=='Sidebar.TFrame'),None)
    if side is None: return
    children=side.winfo_children(); canvases=[w for w in children if isinstance(w,tk.Canvas)]
    if not canvases:
        logo=tk.Canvas(side,height=126,highlightthickness=0,bg='#19364b'); logo.pack(fill='x',before=children[0])
        art=tk.Canvas(side,height=170,highlightthickness=0,bg='#19364b'); art.pack(side='bottom',fill='both',expand=True)
    else:
        logo=canvases[0]; art=canvases[-1] if len(canvases)>1 else tk.Canvas(side,height=170,highlightthickness=0,bg='#19364b')
        if len(canvases)==1: art.pack(side='bottom',fill='both',expand=True)
    def fit(canvas, image, bottom=False):
        def render(_event=None):
            w,h=canvas.winfo_width(),canvas.winfo_height()
            if w<2 or h<2:return
            out=ImageOps.fit(image,(w,h),method=Image.Resampling.LANCZOS,centering=(.5,1. if bottom else .5))
            canvas._saturn_photo=ImageTk.PhotoImage(out,master=canvas)
            canvas.delete('all'); canvas.create_image(0,0,anchor='nw',image=canvas._saturn_photo)
        canvas.bind('<Configure>',render,add='+');canvas.after_idle(render)
    fit(logo,atlas.crop((0,327,128,413)))
    fit(art,atlas.crop((0,0,128,327)),True)
    for key,button in getattr(app,'_nav_buttons',{}).items():
        idx=LABELS.get(str(key).casefold())
        if idx is None:continue
        button._saturn_icon=ImageTk.PhotoImage(_image_icon(atlas,idx),master=button)
        original=str(button.cget('text')); first=original.split(maxsplit=1)
        text=first[1] if len(first)==2 and not first[0][0].isalnum() else original
        button.configure(image=button._saturn_icon,compound='left',text=text)

def install(app_class):
    original=app_class._build_shell
    @wraps(original)
    def shell(self,*args,**kwargs):
        result=original(self,*args,**kwargs)
        apply_reference_assets(self)
        return result
    app_class._build_shell=shell
