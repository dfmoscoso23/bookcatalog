
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
	def buscador(self):
		raw_isbn=str(self.ean)
		print(libro.eanCheck(raw_isbn))
		if len(raw_isbn) ==12:
			raw_isbn=str(raw_isbn)+str(libro.eanCheck(raw_isbn))
		isbn_guinado=raw_isbn[0:3]+"-"+raw_isbn[3:6]+"-"+raw_isbn[6:8]+"-"+raw_isbn[8:12]+"-"+raw_isbn[-1]
		print(isbn_guinado)
		url='http://www.editoriallosada.com/search/content/'+isbn_guinado
		r = requests.get(url)
		time.sleep(1)
		soup = BeautifulSoup(r.text, 'lxml')
		try:
			busca=soup.find('div', class_="ds-2col-fluid node node-libro node-teaser view-mode-teaser clearfix")
			href=busca.h2.a['href']
		except:
			busca=soup.find('div', class_="group-right")
			href=busca.h2.a['href']
		urlo='http://www.editoriallosada.com'+href
		print(urlo)
		ro = requests.get(urlo)
		time.sleep(1)
		soupo = BeautifulSoup(ro.text, 'lxml')
		self.soupo=soupo
	def buscador_isbn_corto(self):
		raw_isbn=str(self.ean)
		if len(raw_isbn) ==12:
			raw_isbn=raw_isbn[3:]
			raw_isbn=str(raw_isbn)+str(libro.tendigitISBN(raw_isbn))
		isbn_guinado=raw_isbn[0:3]+"-"+raw_isbn[3:5]+"-"+raw_isbn[5:9]+"-"+raw_isbn[-1]
		print(isbn_guinado)
		url='http://www.editoriallosada.com/search/content/'+isbn_guinado
		r = requests.get(url)
		time.sleep(1)
		soup = BeautifulSoup(r.text, 'lxml')
		busca=soup.find('div', class_="ds-2col-fluid node node-libro node-teaser view-mode-teaser clearfix")
		href=busca.h2.a['href']
		urlo='http://www.editoriallosada.com'+href
		print(urlo)
		ro = requests.get(urlo)
		time.sleep(1)
		soupo = BeautifulSoup(ro.text, 'lxml')
		self.soupo=soupo
	def extraccion_datos(self):
		soupo=self.soupo
		self.titulo = soupo.find('h1',class_="page-header").text
		try:
			self.sinopsis =soupo.find('div', class_="lead").text
		except:
			try:
				self.sinopsis = soupo.find('div', class_="group-footer").p.text
			except:
				pass
		try:
			div_formato=soupo.find('div', class_="field field-name-field-formato field-type-text field-label-hidden")
			formato=div_formato.find('div', class_="field-item even").text
		except:
			pass
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
		try:
			self.coleccion = soupo.find('div',class_="full-coleccion").a.text
		except:
			pass
		try:
			self.autor = soupo.find('div',class_="field field-name-field-autores-relacionados").text
		except:
			pass
		try:
			otros_involucrados=soupo.find('div',class_="otros-involucrados").text
			print(otros_involucrados)
		except:
			otros_involucrados=""
		if bool(re.search(r'tradu|Tradu',otros_involucrados)):
			try:
				pre_traductor=re.search(r'(.* de |.*: |.*ción |.* por )(.*)',str(otros_involucrados))
				self.traductor= pre_traductor.group(2)
			except:
				pass  
		else:
			self.traductor=""
		if bool(re.search(r'ilust|Ilust',otros_involucrados)):
			try:
				pre_ilustrador= re.search(r'(.* de |.*ción |.*: |.* del |.* por )(\w*)',otros_involucrados)
				self.ilustrador= pre_ilustrador.group(2)
			except:
				pass
		else:
			self.ilustrador = ""
		div_paginas=soupo.find('div', class_="field field-name-field-paginas field-type-text field-label-inline clearfix")
		try:
			self.paginas=div_paginas.find('div', class_="field-item even").text
		except:
			pass
		try:
			preimg=soupo.find('div', class_="hover-icon")
			self.imagen_url=preimg.a['href']
			with open('imagenes/'+str(self.ean)+'.jpg','wb') as fi:
				fi.write(requests.get(self.imagen_url).content)
		except:
			pass
	def eanCheck(ean):
		checksum = 0
		for i, digit in enumerate(reversed(ean)):
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

