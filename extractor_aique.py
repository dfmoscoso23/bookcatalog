
import requests
from bs4 import BeautifulSoup
import re
import time


class libro:
	def __init__(self,isbn):
		self.ean = isbn
		self.titulo = ""
		self.editorial = "Losada"
		self.titulo_descipcion = "sinopsis"
		self.sinopsis =""
		self.alto=""
		self.ancho=""
		self.dimension = "cm"
		self.coleccion = ""
		self.num_coleccion = ""
		self.formato_1=""
		self.formato_2=""
		self.tipo_edicion =""
		self.idioma = "Español"
		self.idioma_original ="" 
		self.autor = ""
		self.traductor=""
		self.ilustrador = ""
		self.paginas=0
		self.extranjero =""
		self.bolsillo =""
		self.edad =""
		self.ibic = ""
		self.soupo=""
		self.imagen_url=""
		self.precio=""
		self.precio_sin_iva=""
	def buscador(self, titulo):
		print(titulo)
		url='http://www.aique.com.ar/search/contenido/'+titulo
		r = requests.get(url)
		time.sleep(1)
		soup = BeautifulSoup(r.text, 'lxml')
		try:
			busca=soup.find('div', class_="ds-1col node node-libro view-mode-search_index clearfix")
			href=busca.h2.a['href']
		except:
			try:
				largo=titulo.split(" ")
				print(largo)
				if len(largo)>2:
					titulo=str(largo[0])+" "+str(largo[1])+" "+str(largo[2])
				print(titulo)
				url='http://www.aique.com.ar/search/contenido/'+titulo
				r = requests.get(url)
				time.sleep(1)
				soup = BeautifulSoup(r.text, 'lxml')
				try:
					busca=soup.find('div', class_="ds-1col node node-libro node-promoted node-sticky view-mode-search_index clearfix")
					href=busca.h2.a['href']
				except:
					try:
						busca=soup.find('div', class_="ds-1col node node-libro node-promoted view-mode-search_index clearfix")
						href=busca.h2.a['href']
					except:
						pass
			except:
				pass
		urlo='http://www.aique.com.ar'+href
		print(urlo)
		ro = requests.get(urlo)
		time.sleep(1)
		soupo = BeautifulSoup(ro.text, 'lxml')
		self.soupo=soupo
		return soupo
	def extraccion_datos(self):
		soupo=self.soupo
		self.titulo = soupo.find('h1',class_="title").text
		
		try:
			self.sinopsis=soupo.find('div',class_="group-footer").p.text
		except:
			pass
		try:
			formato=soupo.find('div',class_="field field-name-field-formato field-type-text field-label-inline clearfix").find('div', class_="field-item even").text
			if "," in formato:
				formato=re.sub(r",",".",formato)
			if "cm" in formato:
				forma=formato.split("cm")
				formato3=forma[0]
				formato2=formato3.split("x")
				if float(formato2[0].strip()) > float(formato2[1].strip()):
					self.alto=formato2[0]
					self.ancho=formato2[1]
				else:
					self.alto=formato2[1]
					self.ancho=formato2[0]
			else:
				formato2=formato.split("x")
				if float(formato2[0].strip()) > float(formato2[1].strip()):
					self.alto=formato2[0]
					self.ancho=formato2[1]
				else:
					self.alto=formato2[1]
					self.ancho=formato2[0]
		except:
			pass
		try:
			self.coleccion = ""
		except:
			pass
		try:
			self.autor=soupo.find('a',class_="glossify-link").text
		except:
			pass
		try:
			if bool(soupo.find(text=re.compile(r'Ilust'))):
				self.ilustrador=soupo.find_all('a',class_="glossify-link")[-1]
		except:
			pass
		try:
			self.paginas=soupo.find('div',class_="field field-name-field-paginas field-type-text field-label-inline clearfix").find('div', class_="field-item even").text
		except:
			pass
		try:
			
			self.imagen_url=soupo.find('div',class_="libro-img").a['href']
			with open('imagenes/'+str(self.ean)+'.jpg','wb') as fi:
				fi.write(requests.get(self.imagen_url).content)
		except:
			pass
	def eanCheck(ean):
		checksum = 0
		for i, digit in enumerate(reversed(str(ean))):
			checksum += int(digit) * 3 if (i % 2 == 0) else int(digit)
		return (10 - (checksum % 10)) % 10
	def tendigitISBN(isbn):     
		_sum = 0
		for i in range(9):
			_sum += int(isbn[i]) * (10 - i)
		restante=_sum%11
		digito=11-restante
		if digito==10:
			digito='X'
		elif digito == 11:
			digito=0
		return str(digito)