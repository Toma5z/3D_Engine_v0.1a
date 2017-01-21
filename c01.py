#
#    xp = x1 / z1
#    yp = y1 / z1
#
#
#	 xr = x * cos( B ) - z * sin( B )
#    zr = x * sin( B ) + z * cos( B )
#
#
#
#

from tkinter import *
from random import randint
import math

global screenH, screenW, sH2, sW2, fps, camera_x, camera_y, x_temp, y_temp, z_temp, k_temp




screenW = 640
screenH = 480
sH2 = screenH//2
sW2 = screenW//2
camera_x = 0
camera_y = 0
x_temp = 0.0
y_temp = 0.0
z_temp = 0.0

k_temp = 0

fps = 0


class p:
	"klasa opisujaca obiekt: punkt/wierzcholek"
	def __init__(self, x = 0.0, y = 0.0, z = 0.0):
		self.x = x
		self.y = y
		self.z = z
	def pokaz(self):
		return "x = "+str(self.x)+" , y = "+str(self.y)+" , z = "+str(self.z)
		
class w:
	"klasa opisujaca obiekt: wektor/krawedz"
	def __init__(self, p1=p(), p0=p()):
		self.p1 = p1
		self.p0 = p0


class s:
	"klasa opisująca obiekt: trojkat/sciana"
	def __init__(self, w=w(), p=p()):
		self.w = w
		self.p = p
		
		
class Szescian:
	"klasa opisujaca obiek: szescian"
	def __init__(self, p0=p(), size = 100.0, nazwa = "sz", color = "blue"):
		self.p0 = p0
		self.s = size
		self.n = nazwa
		self.c = color
		
		#   tworzenie wierzchołków W = 8
		ws = []
		ws.append(p( -size + p0.x,  size + p0.y,  size + p0.z)) #  0
		ws.append(p(  size + p0.x,  size + p0.y,  size + p0.z)) #  1
		ws.append(p(  size + p0.x, -size + p0.y,  size + p0.z)) #  2
		ws.append(p( -size + p0.x, -size + p0.y,  size + p0.z)) #  3
		
		ws.append(p( -size + p0.x,  size + p0.y, -size + p0.z)) #  4
		ws.append(p(  size + p0.x,  size + p0.y, -size + p0.z)) #  5
		ws.append(p(  size + p0.x, -size + p0.y, -size + p0.z)) #  6
		ws.append(p( -size + p0.x, -size + p0.y, -size + p0.z)) #  7

		self.ws = ws
		
		#    tworzenie krawedzi K = 12      
		ks = []
		ks.append(w( ws[1], ws[0]))	#  0
		ks.append(w( ws[1], ws[2]))	#  1
		ks.append(w( ws[2], ws[3]))	#  2
		ks.append(w( ws[0], ws[3]))	#  3
		
		ks.append(w( ws[4], ws[5]))	#  4
		ks.append(w( ws[6], ws[5]))	#  5
		ks.append(w( ws[6], ws[7]))	#  6
		ks.append(w( ws[4], ws[7]))	#  7
		
		ks.append(w( ws[4], ws[0]))	#  8
		ks.append(w( ws[1], ws[5]))	#  9
		ks.append(w( ws[6], ws[2]))	# 10
		ks.append(w( ws[7], ws[3]))	# 11
		
		self.ks = ks
		
		#   tworzenie scian z trojkatow S = 6*2 (bo jedna sciana (kwadrat) sklada sie z dwoch trojkatow (najprostrze figury))  
		#	UWAGA: Dobrze jak kazdy ktrojkat zawiera inna krawedz - latwo wtedy okreslic jedna z jego widzialnych stron (przez zamiane wierzcholkow krawedzi)
		ss = []
		ss.append(s( ks[ 0], ws[ 2])) ; ss.append(s( ks[ 3], ws[ 2]))
		ss.append(s( ks[ 4], ws[ 6])) ; ss.append(s( ks[ 6], ws[ 4])) 	
		ss.append(s( ks[ 9], ws[ 4])) ; ss.append(s( ks[ 8], ws[ 1])) 	
		
		ss.append(s( ks[ 5], ws[ 2])) ; ss.append(s( ks[ 1], ws[ 5])) 	
		ss.append(s( ks[10], ws[ 7])) ; ss.append(s( ks[ 2], ws[ 7])) 	
		ss.append(s( ks[ 7], ws[ 0])) ; ss.append(s( ks[11], ws[ 0]))
		self.ss = ss

		

				

def wyswietl(ss, nazwa, color):
	ss2 = list(ss)														# ss2 = list(ss) kopiuje tablice, natomiast ss2 = ss daje nową nazwę, ale zmiany dotycza tej samej tablicy
	pi = math.pi
	m = p(x_temp, y_temp, z_temp + 400.0)	
	for x in range(len(ss2)):
		ss2[x] = rot_s(ss2[x], math.radians(45))
		ss2[x] = prz_s(ss2[x], m)
		temp = per_s(ss2[x])
		if temp!=None: Ekran.create_polygon(temp, outline="black", fill=color, width = '0', tags=nazwa)


def per_p(pp):
	"przeliczenie perspektywy 3D na 2D"
	out = p()
	p_ = pp.z
	d = 400
	out.x = pp.x / ( 1 + p_ / d )   +320
	out.y = pp.y / ( 1 + p_ / d )   +240
	return out
	

def per_s(ss):
	out = s()
	out.p = per_p(ss.p)
	out.w.p1 = per_p(ss.w.p1)
	out.w.p0 = per_p(ss.w.p0)

	rk = []
	rk.append(out.w.p0.x)	# P0.x0	 0
	rk.append(out.w.p0.y)	# P0.y0	 1
	rk.append(out.w.p1.x)	# P2.x2	 2
	rk.append(out.w.p1.y)	# P2.y2	 3
	rk.append(out.p.x)		# P1.x1	 4
	rk.append(out.p.y)		# P1.y1	 5
	t=(rk[4]-rk[0])*(rk[3]-rk[1])-(rk[2]-rk[0])*(rk[5]-rk[1])
	if  t > 0: rk = None
	
	return rk
	
def rot_s(ss, kat = math.pi/45):
	global k_temp
	out = s()
	
	kat=math.radians(k_temp)
	
	c_k = math.cos(kat)
	s_k = math.sin(kat)

	out.p.x = ss.p.x * c_k - ss.p.z * s_k
	out.p.z = ss.p.x * s_k + ss.p.z * c_k
	out.p.y = ss.p.y
		
	out.w.p0.x = ss.w.p0.x * c_k - ss.w.p0.z * s_k
	out.w.p0.z = ss.w.p0.x * s_k + ss.w.p0.z * c_k
	out.w.p0.y = ss.w.p0.y
		
	out.w.p1.x = ss.w.p1.x * c_k - ss.w.p1.z * s_k
	out.w.p1.z = ss.w.p1.x * s_k + ss.w.p1.z * c_k
	out.w.p1.y = ss.w.p1.y
	return out

def prz_s(ss, m):
	out = s()
	
	out.p.x = ss.p.x + m.x
	out.p.z = ss.p.z + m.z
	out.p.y = ss.p.y + m.y
		
	out.w.p0.x = ss.w.p0.x + m.x
	out.w.p0.z = ss.w.p0.z + m.z
	out.w.p0.y = ss.w.p0.y + m.y
		
	out.w.p1.x = ss.w.p1.x + m.x
	out.w.p1.z = ss.w.p1.z + m.z
	out.w.p1.y = ss.w.p1.y + m.y
	return out	
	

def put(x,y,color):
	Ekran.create_rectangle(x,y,x+1,y+1, outline=color)

def background():
	global screenH,screenW, sH2, sW2
	
	Ekran.create_rectangle(0,0,screenW, sH2, fill="#62C5FF", width=0, tags="bg")
	Ekran.create_rectangle(0,sH2,screenW, screenH, fill="#4CC634", width=0, tags="bg")
	Ekran.create_text(5,5,anchor=NW, text = "Poruszanie: W,A,S,D + Q,E", tags="text")
	

def Draw():
	global fps, sH2, sW2, k_temp
	fps += 1
	Ekran.delete("sz")
	wyswietl(Sz.ss, Sz.n, Sz.c)	
	#wyswietl(Sz2.ss, Sz2.n, "red")
	#wyswietl(Sz3.ss, Sz3.n, "green")
	k_temp += 2
	
	okno_glowne.after(20, Draw)
	
def FPS():
	global fps, x_temp, y_temp, z_temp, k_temp	
	print(" ****** FPS: "+str(fps))
	print("x: "+str(x_temp))
	print("y: "+str(y_temp))
	print("z: "+str(z_temp))
	
	fps = 0
	okno_glowne.after(1000, FPS)
	
def kdown(e):
	global x_temp, y_temp, z_temp, p
	if e.char == 'd': x_temp += 40
	if e.char == 'a': x_temp -= 40
	if e.char == 'e': y_temp += 40
	if e.char == 'q': y_temp -= 40
	if e.char == 's': z_temp += 40
	if e.char == 'w': z_temp -= 40
	

okno_glowne = Tk()
okno_glowne.geometry('640x480+300+200')

Ekran = Canvas(okno_glowne)
Ekran.bind("<KeyPress>",kdown)
Ekran.focus_set()
Ekran.pack(fill=BOTH, expand=YES)


background()

polozenie = p(200.0,0.0,0.0)
polozenie2 = p(200.0,-200.0,0.0)
Sz = Szescian()
#Sz2 = Szescian(polozenie)
#Sz3 = Szescian(polozenie2)
Draw()
FPS()
okno_glowne.mainloop()


