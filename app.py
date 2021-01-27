import tkinter as tk
import tkinter.messagebox as tkmsg
import serial.tools.list_ports
import thermostat

class Application(tk.Frame):
    dev = None
    running = False
    after_id = None

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.dev = thermostat.Thermostat()

    def get_ports(self, event):
        self.lst_ports.delete(0,tk.END)
        ports = serial.tools.list_ports.comports()
        for p in ports:
            self.lst_ports.insert(tk.END, p.device)
        self.lst_ports.activate(0)
        self.ent_port['state'] = tk.NORMAL
        self.btn_open_port['state'] = tk.NORMAL
    
    def select_port(self, event):
        sel = self.lst_ports.curselection()
        port = self.lst_ports.get(sel[0])
        print("OK", sel, port)
        self.ent_port.delete(0, tk.END)
        self.ent_port.insert(0, port)
    
    def open_port(self, event):
        port = self.ent_port.get()
        ret = self.dev.init_serial(port)
        if ret == 0:
            self.ent_set_temp['state'] = tk.NORMAL
            self.btn_set_temp['state'] = tk.NORMAL
            self.btn_start['state'] = tk.NORMAL
        else:
            tkmsg.showerror("Error", "Failed to open PORT \"{:}\"".format(port))

    def set_temp(self, event):
        temp = float(self.ent_set_temp.get())
        print("Set Temp:", temp)
        self.dev.set_temp(temp)

    def loop(self):
        temp = []
        self.dev.loop(temp)
        self.after_id = self.after(100, self.loop)
        self.ent_get_temp.delete(0, tk.END)
        self.ent_get_temp.insert(0, "{:.2f}°C".format(temp[0]))
        if self.dev.heater:
            self.ent_get_temp['fg'] = 'red'
        elif self.dev.fan:
            self.ent_get_temp['fg'] = 'green'
        else:
            self.ent_get_temp['fg'] = 'black'

    def toggle(self, event):
        if self.running:
            self.running = False
            self.after_cancel(self.after_id)
            self.ent_get_temp['state'] = tk.DISABLED
        else:
            self.running = True
            self.ent_get_temp['state'] = tk.NORMAL
            self.loop()
        print("Running:", self.running)
    
    def createWidgets(self):
        self.lbl_greet = tk.Label(self, text="Collect active ports:")
        self.lbl_greet.grid(row=0, column=1, columnspan=2, sticky="e")
        self.btn_get_ports = tk.Button(self, text="Get Ports")
        self.btn_get_ports.bind('<Button-1>', self.get_ports)
        self.btn_get_ports.grid(row=0, column=3, sticky="w")
        self.lst_ports = tk.Listbox(self, height=5, width=50)
        self.lst_ports.bind('<<ListboxSelect>>', self.select_port)
        self.lst_ports.grid(row=1, column=1, columnspan=3)
        self.lbl_port = tk.Label(self, text="Port of choice:")
        self.lbl_port.grid(row=2, column=1, sticky="e")
        self.ent_port = tk.Entry(self, state=tk.DISABLED)
        self.ent_port.grid(row=2, column=2)
        self.btn_open_port = tk.Button(self, text="Open Port", state=tk.DISABLED)
        self.btn_open_port.bind('<Button-1>', self.open_port)
        self.btn_open_port.grid(row=2, column=3, sticky="w")
        self.lbl_set_temp = tk.Label(self, text="Set Temperature:")
        self.lbl_set_temp.grid(row=3, column=1, sticky="e")
        self.ent_set_temp = tk.Entry(self, state=tk.DISABLED)
        self.ent_set_temp.grid(row=3, column=2)
        self.btn_set_temp = tk.Button(self, text="Set Temp", state=tk.DISABLED)
        self.btn_set_temp.bind('<Button-1>', self.set_temp)
        self.btn_set_temp.grid(row=3, column=3, sticky="w")
        self.lbl_set_temp = tk.Label(self, text="Current Temperature:")
        self.lbl_set_temp.grid(row=4, column=1, sticky="e")
        self.ent_get_temp = tk.Entry(self, state=tk.DISABLED)
        self.ent_get_temp.grid(row=4, column=2)
        self.btn_start = tk.Button(self, text="Start/Stop", state=tk.DISABLED)
        self.btn_start.bind('<Button-1>', self.toggle)
        self.btn_start.grid(row=4, column=3, sticky="w")

if __name__ == "__main__":
    app = Application()
    app.master.title('Thermostat')
    app.mainloop()