from reportlab.graphics.barcode.code128 import Code128
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from svglib.svglib import svg2rlg
from math import fmod
from os import mkdir, path
from subprocess import Popen

pathCami = path.expanduser('~\\Documents\\Patrimonio')

if not path.exists(pathCami):
    mkdir(pathCami)

sizeX = 0
sizeY = 0
msgErro = "Digite somente números!"

while (sizeX < (50 * mm)):
    x = input("Digite a largura da página, maior ou igual à 5 cm: ")
    x = x.replace(",", ".")

    try:
        sizeX = float(x) * mm * 10
    except:
        print(msgErro)

while (sizeY < (20 * mm)):
    y = input("Digite a altura da página, maior ou igual à 2 cm: ")
    y = y.replace(",", ".")

    try:
        sizeY = float(y) * mm * 10
    except:
        print(msgErro)
        
try:
    espSup = input('Digite a margem superior da página. Padrão é 0 cm: ')
    espSup = espSup.replace(",", ".")
    espSup = float(espSup)
except:
    espSup = 0

try:
    espEsq = input('Digite a margem esquerda da página. Padrão é 0 cm: ')
    espEsq = espEsq.replace(",", ".")
    espEsq = float(espEsq)
except:
    espEsq = 0

try:
    espEtiq = input('Digite o espaço entre as etiquetas. Padrão é 0 cm: ')
    espEtiq = espEtiq.replace(",", ".")
    espEtiq = float(espEtiq)
except:
    espEtiq = 0
    
try:
    seqInicial = int(input('Digite a sequência inicial. Padrão é 0: '))
except:
    seqInicial = 0

try:
    seqRep = int(input('Digite a quantidade de etiquetas. Padrão é 1: '))
except:
    seqRep = 1

espSup *= mm * 10
espEsq *= mm * 10
espEtiq *= mm * 10
largEtiq = (50 * mm)
altEtiq = (20 * mm)
drawing = svg2rlg("utls.rdc")
intDivX = int(sizeX / largEtiq)

if ((largEtiq * intDivX) + espEsq + espEtiq > sizeX):
    intDivX -= 1
    
intDivY = int(sizeY / altEtiq)

if ((altEtiq * intDivY) + espSup + espEtiq > sizeY):
    intDivY -= 1
    
multSeq = intDivY
qtdPag = 10
newArq = 0

for i in range(seqRep):
    if ((intDivY == multSeq) and (qtdPag == 10)):
        try:
            canvas.save()
        except:
            f = ''
            
        qtdPag = 1
        newArq += 1
        multSeq = 0
        canvas = Canvas(pathCami + "\\Patrimonio_" + str(newArq).zfill(8) + ".pdf", (sizeX, sizeY))
        canvas.setFont("Helvetica-Bold", 12)
        
    if ((intDivY == multSeq) and (qtdPag < 10)):
        qtdPag += 1
        canvas.showPage()
        canvas.setFont("Helvetica-Bold", 12)
        multSeq = 0

    x = (fmod(i,intDivX) * (largEtiq + espEtiq)) + espEsq
    y = sizeY - (multSeq * (altEtiq + espEtiq)) - altEtiq - espSup

##    canvas.rect(x, y, largEtiq, altEtiq)
    drawing.drawOn(canvas, (2 * mm) + x, (2 * mm) + y)
    code128 = Code128(str(seqInicial).zfill(6), barHeight = (4.5 * mm), barWidth = 1.25)
    code128.drawOn(canvas, (11.3 * mm) + x, (5.8 * mm) + y)
    canvas.drawString((25.3 * mm) + x, (2 * mm) + y, str(seqInicial).zfill(6))

    if (fmod((i + 1),intDivX)==0):
        multSeq += 1

    seqInicial += 1

canvas.save()
Popen('explorer ' + pathCami)
