from tkinter import *
from tkinter import ttk
from descent import *
from thrust import *

materials = ["Kevlar", "Steel", "Custom"]    
    
def density(var, slider):
	if var.get() == "Custom":
		slider.pack()
	else:
		slider.pack_forget()

class Tab1:
	def optCallback(self):
		a = self.g.get() * 9.81
		C = self.C.get()
		t_wheel = self.t_wheel.get()
		t_rocket = self.t_rocket.get()
		
		if self.d_wheel_variable.get() == "Kevlar":
			d_wheel = 1380
		elif self.d_wheel_variable.get() == "Steel":
			d_wheel = 7750
		else:
			d_wheel = self.d_wheel_custom.get()
		
		if self.d_rocket_variable.get() == "Kevlar":
			d_rocket = 1380
		elif self.d_rocket_variable.get() == "Steel":
			d_rocket = 7750
		else:
			d_rocket = self.d_rocket_custom.get()
		
		h_rocket = self.h_rocket.get()
		r_rocket = self.r_rocket.get()
		
		alpha = 1
		beta = 10**self.comf.get()
		
		alpha_learn = 10**self.learn.get()
		
		obj, r_1, omega, r_2, h = grad_descent(a, C, t_wheel, t_rocket, d_wheel, d_rocket, h_rocket, r_rocket, alpha, beta, alpha_learn)
		_, _, _, _, _, KE, V = calculate_obj(a, C, t_wheel, t_rocket, d_wheel, d_rocket, h_rocket, r_rocket, alpha, beta, omega, r_2, h)

		m = get_mass(r_1, r_2, h, t_rocket, d_rocket)

		rot = rotations(KE, self.i_beam.get(), self.v_beam.get())
		time = rot_time(rot, omega)
		vel = ion_velocity(self.v_beam.get())
		mass = prop_mass(m, omega, r_1, vel)
		
		popup = Toplevel()
		popup.title("Optimization Results")
		obj_label = Label(popup, text=f"Objective Value: {obj: .2f}").pack()
		r_1_label = Label(popup, text=f"Outer radius: {r_1: .2f} m").pack()
		r_2_label = Label(popup, text=f"Inner radius: {r_2: .2f} m").pack()
		omega_label = Label(popup, text=f"Rotational speed: {(omega * 30/math.pi): .2f} RPM").pack()
		h_label = Label(popup, text=f"Wheel height: {h: .2f} m").pack()
		ke_label = Label(popup, text = f"Total kinetic energy: {KE: .2f}J").pack()
		v_label = Label(popup, text = f"Volume/crew: {(V/C): .2f}m^3").pack()

		sep = ttk.Separator(popup, orient="horizontal")
		sep.pack(fill="x")

		rotation_label = Label(popup, text = f"Number of rotations needed: {rot/(2*math.pi): .2f}").pack()
		time_label = Label(popup, text = f"Time to rotate up to speed: {time: .2f}s").pack()
		prop_mass_label = Label(popup, text = f"Propellant mass: {(mass): .2f}kg").pack()

	def __init__(self, scroll_frame):
		self.label = Label(scroll_frame, text="Select the following parameters").pack()

		self.g = Scale(scroll_frame, from_ = 0.1, to=1.5, digits = 2, resolution = 0.1, orient="horizontal", label="g's", length=300)
		self.g.pack()
		self.C = Scale(scroll_frame, from_ = 1, to=10, digits = 2, orient="horizontal", label="Crew size", length=300)
		self.C.pack()
		self.t_wheel = Scale(scroll_frame, from_ = 0.1, to=1, digits = 2, resolution = 0.1, orient="horizontal", label="Wheel material thickness (m)", length=300)
		self.t_wheel.pack()
		self.t_rocket = Scale(scroll_frame, from_ = 0.1, to=1, digits = 2, resolution = 0.1, orient="horizontal", label="Rocket material thickness (m)", length=300)
		self.t_rocket.pack()

		self.d_wheel_view = Frame(scroll_frame)
		self.d_wheel_view.pack()
		self.d_wheel_variable = StringVar(self.d_wheel_view)
		self.d_wheel_variable.set("Kevlar")
		self.d_wheel_label = Label(self.d_wheel_view, text="Wheel material").pack()
		self.d_wheel = OptionMenu(self.d_wheel_view, self.d_wheel_variable, *materials, command=lambda e: density(self.d_wheel_variable, self.d_wheel_custom))
		self.d_wheel.pack()

		self.d_wheel_custom = Scale(self.d_wheel_view, from_ = 500, to=2000, digits = 2, orient="horizontal", label="Wheel Density", length=300)

		self.d_rocket_view = Frame(scroll_frame)
		self.d_rocket_view.pack()
		self.d_rocket_variable = StringVar(self.d_rocket_view)
		self.d_rocket_variable.set("Kevlar")
		self.d_rocket_label = Label(self.d_rocket_view, text="Rocket material").pack()
		self.d_rocket = OptionMenu(self.d_rocket_view, self.d_rocket_variable, *materials, command=lambda e: density(self.d_rocket_variable,self.d_rocket_custom))
		self.d_rocket.pack()
			
		self.d_rocket_custom = Scale(self.d_rocket_view, from_ = 500, to=2000, digits = 2, orient="horizontal", label="Rocket Density", length=300)

		self.h_rocket = Scale(scroll_frame, from_ = 1, to=20, orient="horizontal", label="Rocket height (m)", length=300)
		self.h_rocket.pack()
		self.r_rocket = Scale(scroll_frame, from_ = 1, to=20, orient="horizontal", label="Rocket radius (m)", length=300)
		self.r_rocket.pack()

		self.opt_label = Label(scroll_frame, text="Optimization parameters").pack()

		self.comf_label_1 = Label(scroll_frame, text="Comfortability weight").pack()
		self.comf_label = Label(scroll_frame, text="1e0")
		self.comf_label.pack()
		self.comf = Scale(scroll_frame, from_=-5, to=5, tickinterval=0.1, orient="horizontal", showvalue=0, length=300)
		self.comf.config(command=lambda e: self.comf_label.config(text=f"1e{self.comf.get()}"))
		self.comf.pack()

		self.learn_label_1 = Label(scroll_frame, text="Learning rate").pack()
		self.learn_label = Label(scroll_frame, text="1e0")
		self.learn_label.pack()
		self.learn = Scale(scroll_frame, from_=-10, to=0, tickinterval=0.1, orient="horizontal", showvalue=0, length=300)
		self.learn.config(command=lambda e: self.learn_label.config(text=f"1e{self.learn.get()}"))
		self.learn.pack()

		self.thrust_param_label = Label(scroll_frame, text="Choose thrust parameters").pack()
		self.i_beam = Scale(scroll_frame, from_ = 10, to=40, orient="horizontal", label="Ion beam current (A)", length=300)
		self.i_beam.pack()
		self.v_beam = Scale(scroll_frame, from_ = 50, to=200, orient="horizontal", label="Ion beam voltage (V)", length=300)
		self.v_beam.pack()


		self.opt = Button(scroll_frame, text="Optimize", command=self.optCallback).pack()


class Tab2:
	def density(self, var, slider):
		if var.get() == "Custom":
			slider.pack()
		else:
			slider.pack_forget()
		self.calculate(var)
	
	def r_1_calc(self, val):
		omega_rad = math.sqrt(self.g.get() * 9.8 / self.r_1.get())
		omega_rpm = omega_rad * 30/math.pi
		self.omega.set(omega_rpm)
		self.calculate(val)
	
	def omega_calc(self, val):
		omega_rad = self.omega.get() * math.pi/30
		r_1_val = self.g.get() * 9.8 / (omega_rad**2)
		self.r_1.set(r_1_val)
		self.calculate(val)
	
	def g_calc(self, val):
		omega_rad = self.omega.get() * math.pi/30
		r_1_val = self.g.get() * 9.8 / (omega_rad**2)
		self.r_1.set(r_1_val)
		self.calculate(val)

	def calculate(self, val):
		a = self.g.get() * 9.81
		C = self.C.get()
		t_wheel = self.t_wheel.get()
		t_rocket = self.t_rocket.get()
		
		if self.d_wheel_variable.get() == "Kevlar":
			d_wheel = 1380
		elif self.d_wheel_variable.get() == "Steel":
			d_wheel = 7750
		else:
			d_wheel = self.d_wheel_custom.get()
		
		if self.d_rocket_variable.get() == "Kevlar":
			d_rocket = 1380
		elif self.d_rocket_variable.get() == "Steel":
			d_rocket = 7750
		else:
			d_rocket = self.d_rocket_custom.get()
		
		h_rocket = self.h_rocket.get()
		r_rocket = self.r_rocket.get()

		omega = self.omega.get() * math.pi/30
		r_2 = self.r_2.get()
		h = self.h.get()
		r_1 = self.r_1.get()
		
		alpha = 1
		beta = 10**self.comf.get()
		
		obj, _, _, _, _, KE, V = calculate_obj(a, C, t_wheel, t_rocket, d_wheel, d_rocket, h_rocket, r_rocket, alpha, beta, omega, r_2, h)

		m = get_mass(r_1, r_2, h, t_rocket, d_rocket)

		self.obj_label.config(text = f"Objective value: {obj: .2f}")
		self.ke_label.config(text = f"Total kinetic energy: {KE: .2f}J")
		self.v_label.config(text = f"Volume/crew: {(V/C): .2f}m^3")

		rot = rotations(KE, self.i_beam.get(), self.v_beam.get())
		time = rot_time(rot, omega)
		vel = ion_velocity(self.v_beam.get())
		mass = prop_mass(m, omega, r_1, vel)

		self.rotation_label.config(text = f"Number of rotations needed: {rot/(2*math.pi): .2f}")
		self.time_label.config(text = f"Time to rotate up to speed: {time: .2f}s")
		self.prop_mass_label.config(text = f"Propellant mass: {(mass): .2f}kg")

	def set_comf_label(self, val):
		self.comf_label.config(text=f"1e{val}")
		self.calculate(val)
	
	def __init__(self, scroll_frame):
		self.label = Label(scroll_frame, text="Select the following parameters").pack()

		self.g = Scale(scroll_frame, from_ = 0.1, to=1.5, digits = 2, resolution = 0.1, orient="horizontal", label="g's", length=300, command=self.g_calc)
		self.g.pack()
		self.C = Scale(scroll_frame, from_ = 1, to=10, digits = 2, orient="horizontal", label="Crew size", length=300, command=self.calculate)
		self.C.pack()
		self.t_wheel = Scale(scroll_frame, from_ = 0.1, to=1, digits = 2, resolution = 0.1, orient="horizontal", label="Wheel material thickness (m)", length=300, command=self.calculate)
		self.t_wheel.pack()
		self.t_rocket = Scale(scroll_frame, from_ = 0.1, to=1, digits = 2, resolution = 0.1, orient="horizontal", label="Rocket material thickness (m)", length=300, command=self.calculate)
		self.t_rocket.pack()
                
		self.d_wheel_view = Frame(scroll_frame)
		self.d_wheel_view.pack()
		self.d_wheel_variable = StringVar(self.d_wheel_view)
		self.d_wheel_variable.set("Kevlar")
		self.d_wheel_label = Label(self.d_wheel_view, text="Wheel material").pack()
		self.d_wheel = OptionMenu(self.d_wheel_view, self.d_wheel_variable, *materials, command=lambda e: self.density(self.d_wheel_variable, self.d_wheel_custom))
		self.d_wheel.pack()

		self.d_wheel_custom = Scale(self.d_wheel_view, from_ = 500, to=2000, digits = 2, orient="horizontal", label="Wheel Density", length=300, command=self.calculate)

		self.d_rocket_view = Frame(scroll_frame)
		self.d_rocket_view.pack()
		self.d_rocket_variable = StringVar(self.d_rocket_view)
		self.d_rocket_variable.set("Kevlar")
		self.d_rocket_label = Label(self.d_rocket_view, text="Rocket material").pack()
		self.d_rocket = OptionMenu(self.d_rocket_view, self.d_rocket_variable, *materials, command=lambda e: self.density(self.d_rocket_variable, self.d_rocket_custom))
		self.d_rocket.pack()
			
		self.d_rocket_custom = Scale(self.d_rocket_view, from_ = 500, to=2000, digits = 2, orient="horizontal", label="Rocket Density", length=300, command=self.calculate)

		self.h_rocket = Scale(scroll_frame, from_ = 1, to=20, orient="horizontal", label="Rocket height (m)", length=300, command=self.calculate)
		self.h_rocket.pack()
		self.r_rocket = Scale(scroll_frame, from_ = 1, to=20, orient="horizontal", label="Rocket radius (m)", length=300, command=self.calculate)
		self.r_rocket.pack()

		self.opt_label = Label(scroll_frame, text="Optimization parameters").pack()

		self.comf_label_1 = Label(scroll_frame, text="Comfortability weight").pack()
		self.comf_label = Label(scroll_frame, text="1e0")
		self.comf_label.pack()
		self.comf = Scale(scroll_frame, from_=-5, to=5, tickinterval=0.1, orient="horizontal", showvalue=0, length=300)
		self.comf.config(command=self.set_comf_label)
		self.comf.pack()

		self.val_label = Label(scroll_frame, text="Choose wheel parameters").pack()
		self.r_1 = Scale(scroll_frame, from_ = 10, to=40, orient="horizontal", label="Outer radius (m)", length=300, command=self.r_1_calc)
		self.r_1.pack()
		self.r_2 = Scale(scroll_frame, from_ = 8, to=38, orient="horizontal", label="Inner radius (m)", length=300, command=self.calculate)
		self.r_2.pack()
		self.omega = Scale(scroll_frame, from_ = 1, to=12, orient="horizontal", label="Rotational speed (RPM)", length=300, command=self.omega_calc)
		self.omega.pack()
		self.h = Scale(scroll_frame, from_ = 1, to=20, orient="horizontal", label="Wheel height (m)", length=300, command=self.calculate)
		self.h.pack()

		self.thrust_param_label = Label(scroll_frame, text="Choose thrust parameters").pack()
		self.i_beam = Scale(scroll_frame, from_ = 10, to=40, orient="horizontal", label="Ion beam current (A)", length=300, command=self.calculate)
		self.i_beam.pack()
		self.v_beam = Scale(scroll_frame, from_ = 50, to=200, orient="horizontal", label="Ion beam voltage (V)", length=300, command=self.calculate)
		self.v_beam.pack()

		self.sep = ttk.Separator(scroll_frame, orient="horizontal")
		self.sep.pack(fill="x")

		self.out_label = Label(scroll_frame, text="Outputs").pack()
		self.obj_label = Label(scroll_frame, text="Objective value: ")
		self.obj_label.pack()
		self.ke_label = Label(scroll_frame, text="Total kinetic energy: ")
		self.ke_label.pack()
		self.v_label = Label(scroll_frame, text="Volume/crew: ")
		self.v_label.pack()

		self.sep2 = ttk.Separator(scroll_frame, orient="horizontal")
		self.sep2.pack(fill="x")

		self.thrust_label = Label(scroll_frame, text="Thrust Info").pack()	
		self.rotation_label = Label(scroll_frame, text="Number of rotations needed: ")
		self.rotation_label.pack()
		self.time_label = Label(scroll_frame, text="Time to rotate up to speed: ")
		self.time_label.pack()
		self.prop_mass_label = Label(scroll_frame, text="Propellant mass: ")
		self.prop_mass_label.pack()	


def main():
	root = Tk()
        
	root.title("Artificial Gravity Optimizer")
        
	tab = ttk.Notebook(root)

	tab1 = Frame(tab)
	tab2 = Frame(tab)
    
	tab.add(tab1, text="Optimize")
	tab.add(tab2, text="Manual Entry")
    
	tab.pack(expand=1, fill="both")


	# --- OPTIMIZE TAB ---
	canvas1 = Canvas(tab1, height="80000")
	canvas1.pack(side=LEFT)

	scroll_frame = Frame(canvas1)
	scroll_frame.bind(
    "<Configure>",
    lambda e: canvas1.configure(
        scrollregion=canvas1.bbox("all")
		)
	)

	canvas1.create_window((0, 0), window=scroll_frame, anchor="nw")

	scroll = Scrollbar(tab1, command=canvas1.yview)
	scroll.pack(side=RIGHT, fill=Y)

	canvas1.configure(yscrollcommand=scroll.set)

	tab1_obj = Tab1(scroll_frame)
    
	# --- MANUAL TAB ---
	canvas2 = Canvas(tab2, height="80000")
	canvas2.pack(side=LEFT)

	scroll_frame_2 = Frame(canvas2)
	scroll_frame_2.bind(
    "<Configure>",
    lambda e: canvas2.configure(
        scrollregion=canvas2.bbox("all")
		)
	)

	canvas2.create_window((0, 0), window=scroll_frame_2, anchor="nw")

	scroll2 = Scrollbar(tab2, command=canvas2.yview)
	scroll2.pack(side=RIGHT, fill=Y)

	canvas2.configure(yscrollcommand=scroll2.set)
        
	tab2_obj = Tab2(scroll_frame_2)


	root.mainloop()
        
if __name__ == "__main__":
      main()