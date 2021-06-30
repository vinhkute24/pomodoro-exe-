from tkinter import *
import time
from PIL import ImageTk , Image
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
import pickle 
import random
import pygame 
import sys 




class main_pomodoro(tk.Tk) : 
    def __init__(self ,*args, **kwargs) : 
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Quang Vinh_Podomoro") 
        self.container = tk.Frame(self)
        self.geometry("680x400")
        
        
        self.container.pack(side="top", fill="both", expand=True)
        self.frames ={}
        for F in (pomodoro,shortBreak,longBreak, toDoList) : 
            working_page = F.__name__ 
            frame = F(parent=self.container, controller=self)
            self.frames[working_page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("pomodoro")   
         
    def show_frame(self, working_page) : 
        if working_page not in self.frames:
            self.frames[working_page] = working_page(self.container, self)
        frame = self.frames[working_page]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

class toDoList(tk.Frame) :
    
    def update_listbox (self):
        #Clear listbox
        self.clear_listbox()
    #Populate listbox
        for task in self.tasks:
            self.lb_tasks.insert("end", task)
    #clear the list box from line 0 until the end of the list   
    
    def clear_listbox(self):
        self.lb_tasks.delete(0, "end")
    #Add a task in our list box
    
    def add_task(self):
        self.task = self.txt_input.get()
        if self.task !="":
            self.tasks.append(self.task)
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "Please type a task in the box before click this button")
        self.txt_input.delete(0,"end")

    def del_one(self):
        self.task = self.lb_tasks.get("active")
        if self.task in self.tasks:
            self.tasks.remove(self.task)
        self.update_listbox()
        
    def asc_order(self):
        self.tasks.sort()
        self.update_listbox()
        
    def desc_order(self):
        self.tasks.sort()
        self.tasks.reverse()
        self.update_listbox()
        
    def loadTask(self) :
        self.task = pickle.load(open("task.txt" ,"rb"))
    
        for self.task in self.task :
            self.lb_tasks.insert(tk.END, self.task)
             
    def saveTask(self) :
        self.task = self.lb_tasks.get(0, self.lb_tasks.size())
        pickle.dump(self.task, open("task.txt" , "wb"))
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #meme 
        
        self.img = ImageTk.PhotoImage(Image.open("D:\python\python\pomodoro\working.png" ))
        panel = Label(self, image = self.img)
        panel.place(x = 280 , y = 0 )
        
        #list
        self.tasks = []
        #List used for testing  
        self.tasks = []
        #Buttons
        
        lbl_title = Label(self, text="To-Do-List", bg="white")
        lbl_title.grid(row=0, column=0)

        self.lbl_display = Label(self, text="", bg="white")
        self.lbl_display.grid(row=1, column=1)

        self.txt_input= Entry(self, width="20" )
        self.txt_input.grid(row=1, column=1)

        btn_add_task = Button(self, text="Add Task", fg="green", bg="white", command=self.add_task)
        btn_add_task.place(x = "200", y = "50")

        btn_del_one = Button(self, text="Delete one", fg="green", bg="white", command=self.del_one)
        btn_del_one.place(x = "200", y = "80")

        btn_asc_order = Button(self, text="Sort (Asc)", fg="green", bg="white", command=self.asc_order)
        btn_asc_order.place(x = "200", y = "110")

        btn_desc_order = Button(self, text="Sort (Desc)", fg="green", bg="white", command=self.desc_order)
        btn_desc_order.place(x = "200", y = "140")
        
        self.lb_tasks = Listbox(self)
        self.lb_tasks.grid(row=2, column=1, rowspan=9)
        
        #back_button = tk.Button(self, text = "Back To\nPomodoro" , font= ("Arival", 10, 'bold') , command=lambda: controller.show_frame("pomodoro"))
        #back_button.place(x = "200", y = "0")
        
        button_save_task = tk.Button(self, text = "Save Task", fg="green", bg="white", command = self.saveTask)
        button_save_task.place(x = "200", y = "20")
        
        button_load_task = tk.Button(self, text = "Load Task", fg="green", bg="white", command = self.loadTask)
        button_load_task.place(x = "200", y = "170")
        
        #Stop button 
        self.back_icon = PhotoImage(file = r"D:\python\python\pomodoro\back1.png")
        self.photoimage2 = self.back_icon.subsample(3, 3)
        Button(self, image = self.photoimage2,
            compound = LEFT, command=lambda: self.controller.show_frame("pomodoro")).place(x = "3", y = "50")
        
       
      
class pomodoro(tk.Frame) : 
    def quit(self):
        sys.exit()
    def start_timer(self) :
            pygame.init()
            pygame.mixer.init()
            
            #Stop button 
            stop_icon = PhotoImage(file = r"D:\python\python\pomodoro\stop.png")
            photoimage = stop_icon.subsample(3, 3)
            Button(self, image = photoimage,
                    compound = LEFT, command=self.stop_time).place(x = "270", y = "251") 
            #next button
            photo = PhotoImage(file = r"D:\python\python\pomodoro\next.png")
            photoimage1 = photo.subsample(3, 3)
            tk.Button(self, image = photoimage1, command=lambda: self.controller.show_frame("shortBreak")).place(x = "455", y = "251") 
            
            min_update = tk.Label(self, text= "25", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
            min_update.place(x = 290, y = 150)
            dauHaiCham2= tk.Label(self, text= ":", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
            dauHaiCham2.place(x= 370, y = 150)
            sec_update = tk.Label(self, text= "00", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
            sec_update.place(x = 395 , y = 150)
            
            self.temp = int(self.min_podomoro.get()) * 60 + int(self.sec_podomoro.get())
            while self.temp > -1 : 
                self.min_calculate, self.sec_calculate = divmod(self.temp,60)
                if self.min_calculate > 60 :
                    self.min_calculate = divmod(self.min_calculate, 60)
                min_update.config(text=self.min_calculate)
                sec_update.config(text=self.sec_calculate)
                self.update()
                time.sleep(1) 
                if self.temp == 0 :
                    messagebox.showinfo("Vinh Thong bao" , " TIME UP !! ")
                    #pygame.mixer.music.load("meo.mp3")
                    #pygame.mixer.music.play()
                    self.controller.show_frame("shortBreak")
                self.temp = self.temp -1 
                
    def stop_time(self):
        self.temp = 0       
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
         
        #meme 
        
        #self.img = ImageTk.PhotoImage(Image.open("D:\python\python\pomodoro\working.png" ))
        #panel = Label(self, image = self.img)
        #panel.place(x = 50 , y = 0 )
        
        background_working_colour = "#db524d"	
        background = Frame(self, bg = background_working_colour,height = "400",width = "800")
        background.pack()
        
        self.min_podomoro=StringVar()
        self.min_podomoro.set('25')
        self.sec_podomoro = StringVar()
        self.sec_podomoro.set('00')
        
        self.podomor_time_color_fg = "White"
        self.time_color = "#df645f"
        #poromodo Button  
        poromodo_button = tk.Button(self, text = "Porodomo" , font= ("Arival", 10, 'bold') , bg = self.podomor_time_color_fg, command=lambda: controller.show_frame("pomodoro"))
        poromodo_button.place(x = "260", y = "100")

        #Short break Button  
        poromodo_button = tk.Button(self, text = "Short Break" , font= ("Arival", 10, 'bold') , bg = self.podomor_time_color_fg, command=lambda: controller.show_frame("shortBreak"))
        poromodo_button.place(x = "350", y = "100")

        #long break Button  
        poromodo_button = tk.Button(self, text = "Long Break" , font= ("Arival", 10, 'bold') , bg = self.podomor_time_color_fg, command=lambda: controller.show_frame("longBreak"))
        poromodo_button.place(x = "450", y = "100")

        #Start button
        start_button =  tk.Button(self, text = "START" , font= ("Arival", 20, 'bold') , bg = self.podomor_time_color_fg, command=self.start_timer)
        start_button.place(x = "330", y = "250")
        min_init = tk.Label(self, text= "25", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
        min_init .place(x = 290, y = 150)
        dauHaiCham2_init= tk.Label(self, text= ":", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
        dauHaiCham2_init.place(x= 370, y = 150)
        sec_init = tk.Label(self, text= "00", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
        sec_init.place(x = 395 , y = 150)
        
        #to list button 
        todolist_button = tk.Button(self, text = "To Do List" , font= ("Arival", 10, 'bold') , bg = self.podomor_time_color_fg, command=lambda: controller.show_frame("toDoList"))
        todolist_button.place(x = "550", y = "100")
        
        #exit button
        self.off_icon = PhotoImage(file = r"D:\python\python\pomodoro\off.png")
        self.photoimage3 = self.off_icon.subsample(3, 3)
        Button(self, image = self.photoimage3,
            compound = LEFT, command=self.quit).place(x = 0, y = 0)
        
        
        
        
class shortBreak(tk.Frame) : 
   
    def start_timer(self) : 
            pygame.init()
            pygame.mixer.init()
            
            #Stop button 
            stop_icon = PhotoImage(file = r"D:\python\python\pomodoro\stop.png")
            photoimage = stop_icon.subsample(3, 3)
            Button(self, image = photoimage,
                    compound = LEFT, command=self.stop_time).place(x = "270", y = "251") 
            #next button
            photo = PhotoImage(file = r"D:\python\python\pomodoro\next.png")
            photoimage1 = photo.subsample(3, 3)
            tk.Button(self, image = photoimage1, command=lambda: self.controller.show_frame("longBreak")).place(x = "455", y = "251") 
            min_update = tk.Label(self, text= "05", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
            min_update.place(x = 330, y = 150)
            dauHaiCham2= tk.Label(self, text= ":", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
            dauHaiCham2.place(x= 370, y = 150)
            sec_update = tk.Label(self, text= "00", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
            sec_update.place(x = 395 , y = 150)
            
            self.temp = int(self.min_podomoro.get()) * 60 + int(self.sec_podomoro.get())
            while self.temp > -1 : 
                self.min_calculate, self.sec_calculate = divmod(self.temp,60)
                if self.min_calculate > 60 :
                    self.min_calculate = divmod(self.min_calculate, 60)
                min_update.config(text=self.min_calculate)
                sec_update.config(text=self.sec_calculate)

                self.update()
                time.sleep(1) 
                
                if self.temp == 0 :
                    messagebox.showinfo("Vinh Thong bao" , " TIME UP !! ")
                    #pygame.mixer.music.load("meo.mp3")
                    #pygame.mixer.music.play()
                    self.controller.show_frame("longBreak")
                self.temp = self.temp -1 
                
    def stop_time(self):
        self.temp = 0  
        
    def quit(self):
        sys.exit()
                
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        background_shortBreak_colour = "#437ea8"	
        background = Frame(self, bg = background_shortBreak_colour,height = "400",width = "800")
        background.pack()
    
        self.min_podomoro=StringVar()
        self.min_podomoro.set('05')
        self.sec_podomoro = StringVar()
        self.sec_podomoro.set('00')

        self.podomor_time_color_fg = "White"
        self.time_color = "#437ea8"
        
        #poromodo Button  
        poromodo_button = tk.Button(self, text = "Porodomo" , font= ("Arival", 10, 'bold') , bg = self.podomor_time_color_fg, command=lambda: controller.show_frame("pomodoro"))
        poromodo_button.place(x = "260", y = "100")

        #Short break Button  
        poromodo_button = tk.Button(self, text = "Short Break" , font= ("Arival", 10, 'bold') , bg = self.podomor_time_color_fg, command=lambda: controller.show_frame("shortBreak"))
        poromodo_button.place(x = "350", y = "100")

        #long break Button  
        poromodo_button = tk.Button(self, text = "Long Break" , font= ("Arival", 10, 'bold') , bg = self.podomor_time_color_fg, command=lambda: controller.show_frame("longBreak"))
        poromodo_button.place(x = "450", y = "100")

        #Start button
        start_button =  tk.Button(self, text = "START" , font= ("Arival", 20, 'bold') , bg = self.podomor_time_color_fg,command=self.start_timer)
        start_button.place(x = "330", y = "250")
        min_init = tk.Label(self, text= "05", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
        min_init .place(x = 290, y = 150)
        dauHaiCham2_init= tk.Label(self, text= ":", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
        dauHaiCham2_init.place(x= 370, y = 150)
        sec_init = tk.Label(self, text= "00", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
        sec_init.place(x = 395 , y = 150)
        
        #to list button 
        
        todolist_button = tk.Button(self, text = "To Do List" , font= ("Arival", 10, 'bold') , bg = self.podomor_time_color_fg, command=lambda: controller.show_frame("toDoList"))
        todolist_button.place(x = "550", y = "100")
        
        #exit button
        self.off_icon = PhotoImage(file = r"D:\python\python\pomodoro\off.png")
        self.photoimage3 = self.off_icon.subsample(3, 3)
        Button(self, image = self.photoimage3,
            compound = LEFT, command=self.quit).place(x = 0, y = 0)
        

class longBreak(tk.Frame) : 
    def start_timer(self) :
            pygame.init()
            pygame.mixer.init()
             
            #Stop button 
            stop_icon = PhotoImage(file = r"D:\python\python\pomodoro\stop.png")
            photoimage = stop_icon.subsample(3, 3)
            Button(self, image = photoimage,
                    compound = LEFT, command=self.stop_time).place(x = "270", y = "251") 
            #next button
            photo = PhotoImage(file = r"D:\python\python\pomodoro\next.png")
            photoimage1 = photo.subsample(3, 3)
            tk.Button(self, image = photoimage1, command=lambda: self.controller.show_frame("pomodoro")).place(x = "455", y = "251") 
            min_update = tk.Label(self, text= "25", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
            min_update.place(x = 290, y = 150)
            dauHaiCham2= tk.Label(self, text= ":", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
            dauHaiCham2.place(x= 370, y = 150)
            sec_update = tk.Label(self, text= "00", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
            sec_update.place(x = 395 , y = 150)
            
            self.temp = int(self.min_podomoro.get()) * 60 + int(self.sec_podomoro.get())
            while self.temp > -1 : 
                self.min_calculate, self.sec_calculate = divmod(self.temp,60)
                if self.min_calculate > 60 :
                    self.min_calculate = divmod(self.min_calculate, 60)
                min_update.config(text=self.min_calculate)
                sec_update.config(text=self.sec_calculate)
                self.update()
                time.sleep(1) 
                if self.temp == 0 :
                    messagebox.showinfo("Vinh Thong bao" , " TIME UP !! ")
                    #pygame.mixer.music.load("meo.mp3")
                    #pygame.mixer.music.play()
                    self.controller.show_frame("pomodoro")
                self.temp = self.temp -1 
                
    def stop_time(self):
        self.temp = 0  
        
    def quit(self):
        sys.exit()
                
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        background_working_colour = "#468e91"	
        background = Frame(self, bg = background_working_colour,height = "400",width = "800")
        background.pack()
        
        self.min_podomoro=StringVar()
        self.min_podomoro.set('15')
        self.sec_podomoro = StringVar()
        self.sec_podomoro.set('00')
        
        self.podomor_time_color_fg = "White"
        self.time_color = "#468e91"
        
        #poromodo Button  
        poromodo_button = tk.Button(self, text = "Porodomo" , font= ("Arival", 10, 'bold') , bg = self.podomor_time_color_fg, command=lambda: controller.show_frame("pomodoro"))
        poromodo_button.place(x = "260", y = "100")

        #Short break Button  
        poromodo_button = tk.Button(self, text = "Short Break" , font= ("Arival", 10, 'bold') , bg = self.podomor_time_color_fg, command=lambda: controller.show_frame("shortBreak"))
        poromodo_button.place(x = "350", y = "100")

        #long break Button  
        poromodo_button = tk.Button(self, text = "Long Break" , font= ("Arival", 10, 'bold') , bg = self.podomor_time_color_fg, command=lambda: controller.show_frame("longBreak"))
        poromodo_button.place(x = "450", y = "100")

        #Start button

        start_button =  tk.Button(self, text = "START" , font= ("Arival", 20, 'bold') , bg = self.podomor_time_color_fg,command=self.start_timer)
        start_button.place(x = "330", y = "250")
        min_init = tk.Label(self, text= "15", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
        min_init .place(x = 290, y = 150)
        dauHaiCham2_init= tk.Label(self, text= ":", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
        dauHaiCham2_init.place(x= 370, y = 150)
        sec_init = tk.Label(self, text= "00", font=("Helvetica",50, 'bold') , bg = self.time_color, fg = self.podomor_time_color_fg)
        sec_init.place(x = 395 , y = 150)
        
        #to list button 
        
        todolist_button = tk.Button(self, text = "To Do List" , font= ("Arival", 10, 'bold') , bg = self.podomor_time_color_fg, command=lambda: controller.show_frame("toDoList"))
        todolist_button.place(x = "550", y = "100")
        
        #exit button
        self.off_icon = PhotoImage(file = r"D:\python\python\pomodoro\off.png")
        self.photoimage3 = self.off_icon.subsample(3, 3)
        Button(self, image = self.photoimage3,
            compound = LEFT, command=self.quit).place(x = 0, y = 0)
        
        
if __name__ == "__main__":
    app = main_pomodoro()
    app.mainloop()