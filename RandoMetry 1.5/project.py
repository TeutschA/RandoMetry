# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import random as rand
import numpy as np
import time
import colors as cs
import os
import datetime
from PIL import Image
import ctypes
import msvcrt
import subprocess
from ctypes import wintypes


###MAXIMIZE CONSOLE
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)

SW_MAXIMIZE = 3

kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)

def maximize_console(lines=None):
    fd = os.open('CONOUT$', os.O_RDWR)
    try:
        hCon = msvcrt.get_osfhandle(fd)
        max_size = kernel32.GetLargestConsoleWindowSize(hCon)
        if max_size.X == 0 and max_size.Y == 0:
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        os.close(fd)
    cols = max_size.X
    hWnd = kernel32.GetConsoleWindow()
    if cols and hWnd:
        if lines is None:
            lines = max_size.Y
        else:
            lines = max(min(lines, 9999), max_size.Y)
        subprocess.check_call('mode.com con cols={} lines={}'.format(
                                cols, lines))
        user32.ShowWindow(hWnd, SW_MAXIMIZE)
        
        
        
maximize_console()
os.system('cls')
rand.seed()
t0 = time.time()
gWidth = 24.5
gHeight = 16.4
gRatio = gWidth/gHeight
gColor = '#FFFFFF'

GOLDEN = (1.+np.sqrt(5.))/2.
SILVER = 1. + np.sqrt(2.)

maxLength = 5.
minLength = 0.25
pType = 'rectangles'
iterations = 3
n=20
pAlpha = 0.
INCHES_to_CM = 1.*2.54
res = 300
EPSILON = 1e-6
datas = []
m = 3
user = os.path.expanduser('~')
if not os.path.isdir(user+'/RandoMetry'):
    os.mkdir(user+'/RandoMetry')
def randomRectangleC(minL,maxL,pCols,alph,rats,cter):
    boolInside = False
    while(not boolInside):
        length = (minL + rand.random()*(maxL - minL))/2.
        sigx = gWidth /5.
        sigy = gHeight /5.
        mux = cter[0]
        muy = cter[1]
        x = -1.
        y=-1.
        while x<0 or x > gWidth:
            x = np.random.randn()*sigx + mux
        while y<0 or y> gHeight : 
            y = np.random.randn()*sigy + muy
        center = (x,y)
        ratio = rats[rand.randint(0,len(rRatios)-1)]
        if ratio != 0:
            width = length/ratio
        angle = rand.random()*2.*np.pi
        alea = rand.randint(0,1)
        if alea ==0 : 
            lengthT = length
            length = width
            width = lengthT
        vs = vertices(center,length,width,angle)
        color = randomColor(pCols)
        boolInside = are_inside(vs) 
    return [vs,width,length,angle,color,alph] 

def randomRectangle(minL,maxL,pCols,alph,rats):
    boolInside = False
    while(not boolInside):
        length = (minL + rand.random()*(maxL - minL))/2.
        center = [rand.random()*gWidth,rand.random()*gHeight]
        ratio = rats[rand.randint(0,len(rRatios)-1)]
        if ratio !=0:
            width = length/ratio
        angle = rand.random()*2.*np.pi
        alea = rand.randint(0,1)
        if alea ==0 : 
            lengthT = length
            length = width
            width = lengthT
        vs = vertices(center,length,width,angle)
        color = randomColor(pCols)
        boolInside = are_inside(vs) 
    return [vs,width,length,angle,color,alph] 

def randomRegulierC(minL,maxL,pCols,alph,m,cter):
    boolInside = False
    while(not boolInside):
        length = (minL + rand.random()*(maxL - minL))/2.
        sigx = gWidth /10.
        sigy = gHeight /10.
        mux = cter[0]
        muy = cter[1]
        x = -1.
        y=-1.
        while x<0 or x > gWidth:
            x = np.random.randn()*sigx + mux
        while y<0 or y> gHeight : 
            y = np.random.randn()*sigy + muy
        center = (x,y)
        angle = rand.random()*2.*np.pi
        vs = verticesReguliers(center,length,angle,m)
        color = randomColor(pCols)
        boolInside = are_inside(vs)
    return [vs,m,length,angle,color,alph] 

def randomRegulier(minL,maxL,pCols,alph,m):
    boolInside = False
    while(not boolInside):
        length = (minL + rand.random()*(maxL - minL))/2.
        center = [length + rand.random()*(gWidth-2.*length),length+rand.random()*(gHeight-2.*length)]
        angle = rand.random()*2.*np.pi
        vs = verticesReguliers(center,length,angle,m)
        color = randomColor(pCols)
        boolInside = are_inside(vs)
    return [vs,m,length,angle,color,alph]  

def rotation(vs,angle,center):
    cx = center[0]
    cy = center[1]
    vsRot =[]
    for v in vs :
        x = v[0]
        y = v[1]
        vsRot.append((np.cos(angle)*(x-cx)+cx-y*np.sin(angle),np.cos(angle)*(y-cy)+cy+np.sin(angle)*(x+cx)))
    return vsRot
    
def verticesReguliers(center,length,angle,m):
    rot = 2.*np.pi/float(m)
    vs = []
    for i in range(0,m):
        vs.append((center[0]+np.cos(rot*i)*length,center[1]+np.sin(rot*i)*length ))
    return rotation(vs,angle,center)
def vertices(center,length,width,angle) : 
    v1 = np.array([(center[0]-width/2.)*np.cos(angle)-(center[1]+length/2.)*np.sin(angle),(center[1]+length/2.)*np.cos(angle)+(center[0]-width/2.)*np.sin(angle)])
    v2 = np.array([(center[0]-width/2.)*np.cos(angle)-(center[1]-length/2.)*np.sin(angle),(center[1]-length/2.)*np.cos(angle)+(center[0]-width/2.)*np.sin(angle)])
    v3 = np.array([(center[0]+width/2.)*np.cos(angle)-(center[1]-length/2.)*np.sin(angle),(center[1]-length/2.)*np.cos(angle)+(center[0]+width/2.)*np.sin(angle)])
    v4 = np.array([(center[0]+width/2.)*np.cos(angle)-(center[1]+length/2.)*np.sin(angle),(center[1]+length/2.)*np.cos(angle)+(center[0]+width/2.)*np.sin(angle)])
    return [v1,v2,v3,v4]
    
def randomColor(colos):
    return colos[rand.randint(0,len(colos)-1)]
    
def are_inside(vs): 
    for v in vs : 
        if ((v[0]<0  or v[0]>gWidth) or (v[1]<0 or v[1]>gHeight)):
            return False
    return True

def verifRatio(r1,r2):
    if (r1-r2)*(r1-r2)<EPSILON : 
        return True
    return False
    
def ratioRange(r1,r2,K):
    step = (float(r2-r1))/float(K)
    rRatioRange = []
    for i in range(0,K):
        rRatioRange.append(r1 + step*i)
    return rRatioRange
        

follow = True
while(follow == True):
    rRatios = []
    pColors = []
    string = ''
    cls = ""
    ratios = ""
    fromSource = False
    stTemp = 'oui'
    source =''
    mode ='uniform'
    center = (-1.,-1.)
    while stTemp != 'oui' and stTemp != 'non' : 
        stTemp = input('Voulez vous partir d\'une image existante (oui/non) ? ')
        os.system('cls')
        if stTemp == 'oui':
            print('Placez l\'image dans le dossier imagesSources et entrez son nom. Par exemple (source.png).')
            source = 'imagesSources/'+input('Entrez ici le nom de l\'image : ')
            fromSource = True
        elif stTemp =='non' : 
            fromSource = False
    print("Bienvenue dans les réglagles cher camarade. Voici les réglages actuels : " )
    while (string != 'ok' or len(pColors)==0 or (len(rRatios)==0 and pType =='rectangles') or (m<=2 and pType == 'reguliers') or res==0 or (mode == 'centered' and center[0]<0)) and string != 'quit' : 
        print("\n Paramètres de la grille : \n ")
        print("- Taille de l'image : ", gWidth, "x", gHeight, ". Tapez w pour modifier la largeur, h pour la hauteur.")
        if(not fromSource):
            print("- Couleur de fond : ", str(int(cs.hex2rgb(gColor)[0])) +' '+ str(int(cs.hex2rgb(gColor)[1])) +' ' + str(int(cs.hex2rgb(gColor)[2])), ". Tapez bg pour la modifier.")
        print("- Nombres d'itérations du programme : ", iterations,". Tapez it pour le modifier.")
        print("- Résolution : ", str(int(res)), ". Tapez res pour la modifier")        
        print("\n Paramètres des premiers polygones : \n")
        print("- Longueur caractéristique des polygones (longueur des rectangles, diamètre des cercles circonscrit aux polygones réguliers...) :", str(round(minLength,3)), " - ", str(round(maxLength,3)), ". \n Tapez minL pour modifier la longueur minimum et maxL pour la longueur maximum\n")
        print("- Nombre de polygones : ", str(n), ". Tapez n pour le modifier.")
        print("- Couleurs utilisées : ", cls, ". Tapez cls pour les modifier.")
        print("- Type de polygones : ", pType, ". Tapez type pour le modifier.")
        print("- Opacité (entre 0 et 1 ) : ", str(round(1.-pAlpha,2)),". Tapez opac pour le modifier.")
        if pType == "rectangles" : 
            print("- Ratios :", ratios, ".Tapez ratio pour les modifier.")
        elif pType == "reguliers":
            print("- Nombre de côtés : ", m, ". Tapez nside pour le modifier.")
        if mode == 'centered' : 
            print('- Le centre actuel est : ', center,'. Tapez mode pour passer en non centré et center pour changer le centre.')
        elif mode=='uniform':
            print('- Il n\'y a pas de centre choisi. Tapez mode pour passer en mode centré.')
        print('\n')
        print('Entrez ok lorsque les paramètres vous conviennent ou quit pour quitter. \n')
        string = input('Entrez w - h - minL - maxL - n - cls - it - type - ratio - nside - mode- center - ok ou quit : ').lower()
        os.system('cls')
        if string=='w' :
            wTemp = -1.
            while wTemp <=0 :
                try :
                    wTemp = float(input("Entrez la largeur d\'image souhaitée : "))
                    if wTemp <= 0. : 
                        wTemp = -1
                except Exception:
                    print('\n La valeur entrée doit être une valeur numérique positive.')
                    print('\n')
            os.system('cls')
            gWidth = wTemp
        elif string=='h':
            hTemp = -1.
            while hTemp <=0 :
                try :
                    hTemp = float(input("Entrez la hauteur d\'image souhaitée : "))
                    if hTemp <= 0. : 
                        hTemp = -1
                except Exception: 
                    print('\n La valeur entrée doit être une valeur numérique positive')
                    print('\n')
            gHeight = hTemp
        elif string=='mode' and mode=='centered':
            mode = 'uniform'
            center = (-1.,-1.)
        elif string=='mode' and mode=='uniform':
            mode = 'centered'
        elif mode=='centered' and string=='center':
            centTemp = (-1.,-1.)
            while centTemp[0] <0  or centTemp[1]<0 or centTemp[0]> gWidth or centTemp[1]>gHeight :
                try :
                    centTemp = input("Entrez les coordonnées du centre voulu. Par exemple pour (0,0), entrez 0 0 : ").split()
                    centTemp = (float(centTemp[0]),float(centTemp[1]))
                except Exception: 
                    print('La valeur entrée doit être composée de deux valeurs numériques positives')
                    centTemp = (-1.,-1.)
                    print('\n')
            center = centTemp          
        elif string=='minl' : 
            minTemp = -1.
            while minTemp <=0 :
                try :
                    minTemp = float(input("Entrez la longueur minimum des polygones souhaitée : "))
                    if minTemp <= 0. : 
                        minTemp = -1
                except :
                    print('La valeur entrée doit être une valeur numérique positive')
            minLength = minTemp       
        elif string=='maxl' : 
            maxTemp = -1.
            while maxTemp <=minLength - EPSILON :
                try :
                    maxTemp = float(input("Entrez la longueur maximum des polygones souhaitée : "))
                    if maxTemp <= 0. : 
                        maxTemp = -1
                    if maxTemp <= minLength - EPSILON : 
                        os.system('cls')
                        print('La valeur rentrée doit être supérieur à la valeur minimale rentrée : ', minLength)
                except Exception : 
                    print('La valeur entrée doit être une valeur numérique positive')
                    pass
            maxLength = maxTemp  
        elif string=='n' :
            nTemp = -1.
            while nTemp <=0 :
                try : 
                    nTemp = int(input("Entrez le nombre de polygones : "))
                except Exception:
                    print("Le nombre de polygone doit être une valeur numérique positive")
            n = nTemp
        elif string=='cls':
            colTemp=""
            while colTemp != 'ok' : 
                print('Couleurs actuelles : ' + cls + '\n \n')
                colTemp = input('Entrez ok si vous avez fini, delete pour supprimer une couleur ou sinon range pour un intervalle de couleurs ou  le nom d\'une couleur prérentrée ou  la couleur en RGB : (ex: pour IndianRed, on peut rentrer IndianRed ou 205 92 92) : ').lower()
                colTempS = colTemp.split()
                if len(colTemp.split()) and colTemp in cs.colorsPredefined : 
                    pColors.append(cs.colorsPredefined[colTemp])
                    cls= cls + " " + colTemp
                    os.system('cls')
                    print('La couleur a bien été ajoutée !')
                    print('')
                elif len(colTempS) ==3:
                    try :
                        colHexTemp = str(cs.rgb2hex(int(colTempS[0]),int(colTempS[1]),int(colTempS[2])))
                        pColors.append(colHexTemp)
                        cls = cls + " " + colHexTemp
                        os.system('cls')
                        print('La couleur a bien été ajoutée !')
                        print('')
                    except Exception : 
                        print("Il y a eu une erreur dans la couleur rentré")
                elif colTemp == 'range' : 
                    try :
                        print('')
                        colorTemp1 = input('Première couleur en RGB : (ex: 255 255 0 ) : ').split()
                        colorTemp2 = input('Seconde couleur en RGB : (ex 255 241 0) : ' ).split()
                        ks = int(input("Nombres de couleurs intermédiaires : "))
                        clors = cs.colorsRange(colorTemp1, colorTemp2, ks+2)
                        for i in clors : 
                            pColors.append(i)
                        os.system('cls')
                        print('Le dégradé a bien été ajouté.')
                        print('')
                    except Exception :
                        print("Il y a eu une erreur dans les couleurs ou le nombre rentré")
                elif colTemp == 'delete' :
                    try :
                        print('')
                        colToDel = input('Entrez le code RGB ou le nom de la couleur à supprimer : ')
                        if colToDel in cs.colorsPredefined : 
                            colToDel = cs.colorsPredefined[colToDel]
                            os.system('cls')
                            print('La couleur a bien été supprimé')
                            print('')
                        elif colToDel == 'ok' :
                            os.system('cls')
                        elif len(colToDel.split())==3 : 
                            colS = colToDel.split()
                            colToDel = str(cs.rgb2hex(int(colS[0]),int(colS[1]),int(colS[2])))
                            os.system('cls')
                            print('La couleur a bien été supprimé')
                            print('')
                        else :
                            os.system('cls')
                            print('Vous vous êtes trompés dans la donnée rentrée. \n \n')
                        pColorsTemp = []
                        for i in range(0,len(pColors)) : 
                            if pColors[i] != colToDel :                           
                                pColorsTemp.append(str(pColors[i]))
                        pColors = pColorsTemp
                    except Exception : 
                        print('Il y a eu un problème dans la couleur rentrée.')
                elif colTemp != 'ok' :
                    print('Il y a eu une erreur dans la donnée rentrée : ', colTemp, '. Il est possible que vous vous soyez trompés de caractère ou oublié un de ceux ci. Appuyez sur Entrée pour continuer.')
                    valTemp = input('')
                    os.system('cls')
                cls = ''
                for i in pColors : 
                    if len(cls)>0:
                        cls= cls + " | "+ str(int(cs.hex2rgb(i)[0])) +' '+ str(int(cs.hex2rgb(i)[1])) +' ' + str(int(cs.hex2rgb(i)[2]))
                    else : 
                        cls = str(int(cs.hex2rgb(i)[0])) +' '+ str(int(cs.hex2rgb(i)[1])) +' ' + str(int(cs.hex2rgb(i)[2]))
                
        elif string=='it' : 
            iTemp = -1.
            while iTemp <=0 :
                try:
                    iTemp = int(input("Entrez le nombre d'itérations du programme : "))
                except ValueError : 
                    print('La valeur rentrée doit être une valeur numérique entière')
                    pass
            iterations = iTemp        
        elif string=='type':
            pTypeTemp = ""
            while pTypeTemp != "rectangles" and pTypeTemp != "reguliers" :
                pTypeTemp = input('Entrez le type désiré (rectangles et reguliers sont les seuls gérés actuellement) : ').lower()
                os.system('cls')
            pType = pTypeTemp 
        elif pType == 'rectangles' and string=='ratio': 
            ratioTemp = -1
            while ratioTemp <0 :
                print('Ratios actuels : ' + ratios + ' \n')
                ratioTemp = input("Entrez le ratio des rectangles souhaitée (golden / silver pour les ratios concernés), delete pour un supprimer un, range pour ajouter un intervalle ou ok pour continuer : ").lower()
                if ratioTemp == 'golden':
                    rRatios.append(GOLDEN)
                    ratioTemp=-1
                    os.system('cls')
                    print("Le ratio d'or a été ajouté. ")
                    print(' ')
                elif ratioTemp == 'silver':
                    rRatios.append(SILVER)
                    ratioTemp=-1
                    os.system('cls')
                    print("Le ratio d'argent a été ajouté. ")
                    print(' ')
                elif ratioTemp =='range':
                    os.system('cls')
                    try : 
                        ratio1  = input('Entrez le premier ratio : ')
                        if ratio1 == 'golden' : 
                            ratio1 = GOLDEN
                        elif ratio1 =='silver':
                            ratio1 = SILVER
                        else : 
                            ratio1 = float(ratio1)
                        ratio2 = input('Entrez le second ratio : ')
                        if ratio2 == 'golden' : 
                            ratio2 = GOLDEN
                        elif ratio2 =='silver':
                            ratio2 = SILVER
                        else : 
                            ratio2 = float(ratio2)
                        rangeN = int(input('Entrez le nombre de ratio intermédiaires : '))
                        ratioRangeTemp = ratioRange(ratio1,ratio2,rangeN+2)
                        for i in ratioRangeTemp : 
                            rRatios.append(i)
                    except Exception : 
                        os.system('cls')
                        print('Il y a eu une erreur dans les ratios rentrés ou le nombre de ratio. \n')
                    ratioTemp = -1
                elif ratioTemp == 'ok':
                    print('Retour au menu')
                    ratioTemp = 1
                elif ratioTemp == 'delete':
                    delTemp = input('Rentrez le nom (golden, silver) ou la valeur du ratio à supprimer ou ok pour sortir : ')
                    if delTemp == 'golden' :
                        rRatiosTemp = []
                        for k in range(0,len(rRatios)):
                            if not verifRatio(GOLDEN,rRatios[k]):
                                rRatiosTemp.append(k)
                        rRatios = rRatiosTemp
                        os.system('cls')
                        print('Le ratio d\'or a bien été supprimé')
                        print('')
                    elif delTemp == 'silver' : 
                        rRatiosTemp = []
                        for k in range(0,len(rRatios)):
                            if not verifRatio(SILVER,rRatios[k]):
                                rRatiosTemp.append(k)
                        rRatios = rRatiosTemp
                        print('Le ratio d\'argent a bien été supprimé')
                        print('')
                    elif delTemp == 'ok' : 
                        print('On annule!')
                    else :
                        try :
                            delTemp = float(delTemp)
                            rRatiosTemp = []
                            for k in range(0,len(rRatios)):
                                if not verifRatio(delTemp,rRatios[k]):
                                    rRatiosTemp.append(k)
                            if len(rRatios) > len(rRatiosTemp):
                                rRatios = rRatiosTemp
                                os.system('cls')
                                print('Le ratio a bien été supprimé')
                                print('')
                            else :
                                print('Le ratio n\'a pu être supprimé')
                        except ValueError : 
                            os.system('cls')
                            print("Le ratio rentré doit être une valeur numérique ou silver ou golden.  \n")
                            pass
                    ratioTemp = -1
                else: 
                    try:
                        if float(ratioTemp) <= 0. :
                            os.system('cls')
                            print('La valeur rentrée doit être positive. \n \n')
                        else:
                            ratioTemp = float(ratioTemp)
                            rRatios.append(ratioTemp)
                            os.system('cls')
                            print(ratioTemp, " a été ajouté." )
                            ratioTemp = -1
                    except Exception :
                        os.system('cls')
                        print('Il y a eu une erreur dans la donnée rentrée : ', ratioTemp, '. \n')
                        ratioTemp = -1
                ratios = ''
                for l in rRatios : 
                    if len(ratios)>0:
                        ratios = ratios + " | " + str(round(l,3))
                    else : 
                        ratios = str(round(l,3))
        elif string=='res':
            resTemp = ''
            while resTemp != 'ok' :
                resTemp = input("Entrez la résolution d\'image souhaitée (en ppi) ou ok : ").lower()
                if resTemp != 'ok': 
                    try :
                        res = float(resTemp)
                        resTemp = 'ok'
                    except ValueError : 
                        print("La résolution doit être un nombre. Appuyez sur Entrée pour continuer")
                        vTempo = input('')
                        pass
                os.system('cls')
        elif string=='bg':
            colTemp = input('Entrez le code RGB de la couleur ou son nom : ').lower()
            if len(colTemp.split())==1 and  colTemp in cs.colorsPredefined : 
                gColor = cs.colorsPredefined[colTemp]
            elif len(colTemp.split()) ==3:
                colTempS = colTemp.split()
                gColor = cs.rgb2hex(int(colTempS[0]),int(colTempS[1]),int(colTempS[2]))
        elif string=="opac":
            print("L'opacité actuelle est : ", 1.-pAlpha)
            print('')
            opacTemp = input('Entrez l\'opacité souhaitée (1 = 100%, 0 = 0%) ou ok: ')
            if opacTemp=='ok':
                print('Retour au menu')
            else : 
                try :
                    if (float(opacTemp)>= 0 and float(opacTemp) <= 1) :
                        pAlpha = 1-float(opacTemp)
                    else :
                        print("La valeur rentrée doit être entre 0 et 1")
                except Exception:
                    print("L'opacité doit être une valeur numérique entre 0 et 1. Appuyez sur Entrée pour continuer.")
                    vTemp = input('')
                    pass
        elif string=='nside' :
            nsideTemp = -1.
            while nsideTemp < 3 :
                try : 
                    os.system('cls')
                    nsideTemp = int(input("Entrez le nombre de côtés du poylgone : "))
                except Exception:
                    print("Le nombre de polygone doit être une valeur numérique positive")
            m = nsideTemp
        elif string=='quit' : 
            follow = False
        os.system('cls')
        if minLength >= maxLength + EPSILON : 
            print('La longueur minimale doit être inférieure à la longueur maximale \n.' )
            minLength = maxLength
            string = ''
    if pType == 'rectangles' :
        datas.append([minLength,maxLength,pColors,rRatios,pAlpha,pType,n,center])
    elif pType == 'reguliers' : 
        datas.append([minLength,maxLength,pColors,m,pAlpha,pType,n,center])
        
        
        
        
    ADD = False
    st = ''
    while st != 'non' and string != 'quit' : 
        st = input('Voulez vous rajouter des polygones ? (oui/non) ' )
        if st =='oui' : 
            ADD = True
            if pType =='rectangles':
                ss=""
                while(ss != 'oui' and ss != 'non'):
                    os.system('cls')
                    ss = input("Voulez vous conserver les ratios ? (oui/non) ")
                    os.system('cls')
                if ss == 'non':
                    rRatios = []    
            pColors = []
            string=''
            cls=''
            ratios=''
            for l in rRatios : 
                if len(ratios)>0:
                    ratios = ratios + " | " + str(round(l,3))
                else : 
                    ratios = str(round(l,3))
            while (string != 'ok' or len(pColors)==0 or (len(rRatios)==0 and pType=='rectangles') or (m<3 and pType == 'reguliers') or res==0 or (mode=='centered' and center[0]<0)) and string != 'quit' : 
                print("- Longueur caractéristique des polygones (longueur des rectangles, diamètre des cercles circonscrits aux polygones réguliers...) :", str(round(minLength,3)), " - ", str(round(maxLength,3)), ". Tapez minL pour modifier la longueur minimum et maxL pour la longueur maximum")
                print("- Nombre de polygones : ", str(n), ". Tapez n pour le modifier.")
                print("- Couleurs utilisées : ", cls, ". Tapez cls pour les modifier.")
                print("- Type de polygones : ", pType, ". Tapez type pour le modifier.")
                print("- Opacité (entre 0 et 1 ) : ", str(round(1.-pAlpha,2)),". Tapez opac pour le modifier.")
                if pType == "rectangles" : 
                    print("- Ratios :", ratios, ".Tapez ratio pour les modifier.")
                if pType == "reguliers":
                    print("- Nombre de côtés : ", m, ". Tapez nside pour le modifier.")
                if mode == 'centered' : 
                    print('- Le centre actuel est : ', center,'. Tapez mode pour passer en non centré et center pour changer le centre.')
                elif mode=='uniform':
                    print('- Il n\'y a pas de centre choisi. Tapez mode pour passer en mode centré.')
                    print('\n')
                    print('Entrez ok lorsque vous avez fini. \n')
                string = input('Entrez minL - maxL - n - cls - type - ratio - nside - mode -center ou ok : ')
                os.system('cls')
                if string=='minL' : 
                    minTemp = -1.
                    while minTemp <=0 :
                        try :
                            minTemp = float(input("Entrez la longueur minimum des polygones souhaitée : "))
                            if minTemp <= 0. : 
                                minTemp = -1
                        except :
                            print('La valeur entrée doit être une valeur numérique positive')
                    minLength = minTemp 
                elif string=='maxL' : 
                    maxTemp = -1.
                    while maxTemp < minLength - EPSILON :
                        try :
                            maxTemp = float(input("Entrez la longueur maximum des polygones souhaitée : "))
                            if maxTemp <= 0. : 
                                maxTemp = -1
                            if maxTemp <= minLength - EPSILON : 
                                os.system('cls')
                                print('La valeur rentrée doit être supérieur à la valeur minimale rentrée : ', minLength)
                        except Exception : 
                            print('La valeur entrée doit être une valeur numérique positive')
                            pass
                    maxLength = maxTemp  
                elif string=='mode' and mode=='centered':
                    mode = 'uniform'
                    center = (-1.,-1.)
                elif string=='mode' and mode=='uniform':
                    mode = 'centered'
                elif mode=='centered' and string=='center':
                    centTemp = (-1.,-1.)
                    while centTemp[0] <0  or centTemp[1]<0 or centTemp[0]> gWidth or centTemp[1]>gHeight :
                        try :
                            centTemp = input("Entrez les coordonnées du centre voulu. Par exemple pour (0,0), entrez 0 0 : ").split()
                            centTemp = (float(centTemp[0]),float(centTemp[1]))
                        except Exception: 
                            print('La valeur entrée doit être composée de deux valeurs numériques positives')
                            centTemp = (-1.,-1.)
                            print('\n')
                    center = centTemp     
                elif string=='n' :
                    nTemp = -1.
                    while nTemp <=0 :
                        try :
                            nTemp = int(input("Entrez le nombre de polygones souhaités : "))
                        except (TypeError,ValueError) :
                            print("Le nombre de polygone doit être une valeur numérique positive")
                    n = nTemp
                elif string=='cls':
                    colTemp=""
                    while colTemp != 'ok' : 
                        print('Couleurs actuelles : ' + cls + '\n \n')
                        colTemp = input('Entrez ok si vous avez fini, delete pour supprimer une couleur ou sinon range pour un intervalle de couleurs ou  le nom d\'une couleur prérentrée ou  la couleur en RGB : (ex: pour IndianRed, on peut rentrer IndianRed ou 205 92 92) : ').lower()
                        colTempS = colTemp.split()
                        if len(colTemp.split()) and colTemp in cs.colorsPredefined : 
                            pColors.append(cs.colorsPredefined[colTemp])
                            cls= cls + " " + colTemp
                            os.system('cls')
                            print('La couleur a bien été ajoutée !')
                            print('')
                        elif len(colTempS) ==3:
                            try :
                                colHexTemp = str(cs.rgb2hex(int(colTempS[0]),int(colTempS[1]),int(colTempS[2])))
                                pColors.append(colHexTemp)
                                cls = cls + " " + colHexTemp
                                os.system('cls')
                                print('La couleur a bien été ajoutée !')
                                print('')
                            except Exception : 
                                print("Il y a eu une erreur dans la couleur rentré")
                        elif colTemp == 'range' : 
                            try :
                                print('')
                                colorTemp1 = input('Première couleur en RGB : (ex: 255 255 0 ) : ').split()
                                colorTemp2 = input('Seconde couleur en RGB : (ex 255 241 0) : ' ).split()
                                ks = int(input("Nombres de couleurs intermédiaires : "))
                                clors = cs.colorsRange(colorTemp1, colorTemp2, ks+2)
                                for i in clors : 
                                    pColors.append(i)
                                os.system('cls')
                                print('Le dégradé a bien été ajouté.')
                                print('')
                            except Exception :
                                print("Il y a eu une erreur dans les couleurs ou le nombre rentré")
                        elif colTemp == 'delete' :
                            try :
                                print('')
                                colToDel = input('Entrez le code RGB ou le nom de la couleur à supprimer : ')
                                if colToDel in cs.colorsPredefined : 
                                    colToDel = cs.colorsPredefined[colToDel]
                                    os.system('cls')
                                    print('La couleur a bien été supprimé')
                                    print('')
                                elif colToDel == 'ok' :
                                    os.system('cls')
                                elif len(colToDel.split())==3 : 
                                    colS = colToDel.split()
                                    colToDel = str(cs.rgb2hex(int(colS[0]),int(colS[1]),int(colS[2])))
                                    os.system('cls')
                                    print('La couleur a bien été supprimé')
                                    print('')
                                pColorsTemp = []
                                for i in range(0,len(pColors)) : 
                                    if pColors[i] != colToDel :
                                        pColorsTemp.append(str(pColors[i]))
                                pColors = pColorsTemp
                            except Exception : 
                                print('Il y a eu un problème dans la couleur rentrée.')
                        elif colTemp != 'ok' :
                            print('Il y a eu une erreur dans la donnée rentrée : ', colTemp, '. Il est possible que vous vous soyez trompés de caractère ou oublié un de ceux ci. Appuyez sur Entrée pour continuer.')
                            valTemp = input('')
                            os.system('cls')
                        cls = ''
                        for i in pColors : 
                            if len(cls)>0:
                                cls= cls + " | "+ str(int(cs.hex2rgb(i)[0])) +' '+ str(int(cs.hex2rgb(i)[1])) +' ' + str(int(cs.hex2rgb(i)[2]))
                            else : 
                                cls = str(int(cs.hex2rgb(i)[0])) +' '+ str(int(cs.hex2rgb(i)[1])) +' ' + str(int(cs.hex2rgb(i)[2]))
                elif string=="opac":
                    print("L'opacité actuelle est : ", 1.-pAlpha)
                    print('')
                    opacTemp = input('Entrez l\'opacité souhaitée (1 = 100%, 0 = 0%) ou ok: ')
                    if opacTemp=='ok':
                        print('Retour au menu')
                    else : 
                        try :
                            if (float(opacTemp)>= 0 and float(opacTemp) <= 1) :
                                pAlpha = 1-float(opacTemp)
                            else :
                                print("La valeur rentrée doit être entre 0 et 1")
                        except Exception:
                            print("L'opacité doit être une valeur numérique entre 0 et 1. Appuyez sur Entrée pour continuer.")
                            vTemp = input('')
                            pass
                elif string=='type':
                    pTypeTemp = ""
                    while pTypeTemp != "rectangles" and pTypeTemp != "reguliers" :
                        pTypeTemp = input('Entrez le type désiré (rectangles et reguliers sont les seuls gérés actuellement) : ').lower()
                        os.system('cls')
                    pType = pTypeTemp 
                elif pType == 'rectangles' and string=='ratio': 
                    ratioTemp = -1
                    while ratioTemp <0 :
                        print('Ratios actuels : ' + ratios + ' \n')
                        ratioTemp = input("Entrez le ratio des rectangles souhaitée (golden / silver pour les ratios concernés), delete pour un supprimer un, range pour ajouter un intervalle ou ok pour continuer : ").lower()
                        if ratioTemp == 'golden':
                            rRatios.append(GOLDEN)
                            ratioTemp=-1
                            os.system('cls')
                            print("Le ratio d'or a été ajouté. ")
                            print(' ')
                        elif ratioTemp == 'silver':
                            rRatios.append(SILVER)
                            ratioTemp=-1
                            os.system('cls')
                            print("Le ratio d'argent a été ajouté. ")
                            print(' ')
                        elif ratioTemp =='range':
                            os.system('cls')
                            try : 
                                ratio1  = input('Entrez le premier ratio : ')
                                if ratio1 == 'golden' : 
                                    ratio1 = GOLDEN
                                elif ratio1 =='silver':
                                    ratio1 = SILVER
                                else : 
                                    ratio1 = float(ratio1)
                                ratio2 = input('Entrez le second ratio : ')
                                if ratio2 == 'golden' : 
                                    ratio2 = GOLDEN
                                elif ratio2 =='silver':
                                    ratio2 = SILVER
                                else : 
                                    ratio2 = float(ratio2)
                                rangeN = int(input('Entrez le nombre de ratio intermédiaires : '))
                                ratioRangeTemp = ratioRange(ratio1,ratio2,rangeN+2)
                                for i in ratioRangeTemp : 
                                    rRatios.append(i)
                            except Exception : 
                                os.system('cls')
                                print('Il y a eu une erreur dans les ratios rentrés ou le nombre de ratio. \n')
                            ratioTemp = -1
                        elif ratioTemp == 'ok':
                            print('Retour au menu')
                            ratioTemp = 1
                        elif ratioTemp == 'delete':
                            delTemp = input('Rentrez le nom (golden, silver) ou la valeur du ratio à supprimer ou ok pour sortir : ')
                            if delTemp == 'golden' :
                                rRatiosTemp = []
                                for k in range(0,len(rRatios)):
                                    if not verifRatio(GOLDEN,rRatios[k]):
                                        rRatiosTemp.append(k)
                                rRatios = rRatiosTemp
                                os.system('cls')
                                print('Le ratio d\'or a bien été supprimé')
                                print('')
                            elif delTemp == 'silver' : 
                                rRatiosTemp = []
                                for k in range(0,len(rRatios)):
                                    if not verifRatio(SILVER,rRatios[k]):
                                        rRatiosTemp.append(k)
                                rRatios = rRatiosTemp
                                print('Le ratio d\'argent a bien été supprimé')
                                print('')
                            elif delTemp == 'ok' : 
                                print('On annule!')
                            else :
                                try :
                                    delTemp = float(delTemp)
                                    rRatiosTemp = []
                                    for k in range(0,len(rRatios)):
                                        if not verifRatio(delTemp,rRatios[k]):
                                            rRatiosTemp.append(k)
                                    if len(rRatios) > len(rRatiosTemp):
                                        rRatios = rRatiosTemp
                                        os.system('cls')
                                        print('Le ratio a bien été supprimé')
                                        print('')
                                    else :
                                        print('Le ratio n\'a pu être supprimé')
                                except ValueError : 
                                    os.system('cls')
                                    print("Le ratio rentré doit être une valeur numérique ou silver ou golden.  \n")
                                    pass
                            ratioTemp = -1
                        else: 
                            try:
                                if float(ratioTemp) <= 0. :
                                    os.system('cls')
                                    print('La valeur rentrée doit être positive. \n \n')
                                else:
                                    ratioTemp = float(ratioTemp)
                                    rRatios.append(ratioTemp)
                                    os.system('cls')
                                    print(ratioTemp, " a été ajouté." )
                                    ratioTemp = -1
                            except Exception :
                                os.system('cls')
                                print('Il y a eu une erreur dans la donnée rentrée : ', ratioTemp, '. \n')
                                ratioTemp = -1
                        ratios = ''
                        for l in rRatios : 
                            if len(ratios)>0:
                                ratios = ratios + " | " + str(round(l,3))
                            else : 
                                ratios = str(round(l,3))
                elif string=='nside' :
                    nsideTemp = -1.
                    while nsideTemp < 3 :
                        try : 
                            os.system('cls')
                            nsideTemp = int(input("Entrez le nombre de côtés du poylgone : "))
                        except Exception:
                            print("Le nombre de polygone doit être une valeur numérique positive")
                    m = nsideTemp
                elif string=='mode' and mode=='centered':
                    mode = 'uniform'
                    center = (-1.,-1.)
                elif string=='mode' and mode=='uniform':
                    mode = 'center'
                elif mode=='centered' and string=='center':
                    centTemp = (-1.,-1.)
                    while centTemp[0] <0  or centTemp[1]<0 or centTemp[0]> gWidth or centTemp[1]>gHeight :
                        try :
                            centTemp = input("Entrez les coordonnées du centre voulu. Par exemple pour (0,0), entrez 0 0 : ").split()
                            centTemp = (float(centTemp[0]),float(centTemp[1]))
                        except Exception: 
                            print('La valeur entrée doit être composée de deux valeurs numériques positives')
                            centTemp = (-1.,-1.)
                            print('\n')
                    center = centTemp  
                os.system('cls')
                if minLength >= maxLength + EPSILON : 
                    print('La longueur minimale doit être inférieure à la longueur maximale \n.' )
                    minLength = maxLength
                    string = ''
            if pType == 'rectangles'  and string !='quit': 
                datas.append([minLength,maxLength,pColors,rRatios,pAlpha,pType,n,center])
            elif string != 'quit' : 
                datas.append([minLength,maxLength,pColors,m,pAlpha,pType,n, center])
        
        
                                
    
    dep = ''
    while ADD==True and (follow == True) and (dep != 'couche') and (dep != 'alea'):
        dep = input('Comment doivent être ajoutés les différents rectangles ? Couche par couche (Entrez couche) ou aléatoire (Entrez alea) ? ')
        os.system('cls')
    randomNumber = rand.randint(0,100000)  
    c =0
    
    LINEWIDTH = 0.01*float(res)*0.75/2.54
    date = datetime.datetime.now()
    while (c<iterations and follow == True):
        SOMME =0
        filename = user+'/RandoMetry/image'+ str(date.month) + '-'+ str(date.day) + '_'+ str(date.hour) + '-'+str(date.minute) + '_'+str(c)
        count = 0
        while os.path.isdir(filename):
            filename = filename + str(count)
        os.mkdir(filename)
        polys = []
        t1 = time.time()
        file_name =  filename + '/datas.txt'
        file = open(file_name, "w")
        file.write(" - Taille de l'image : "+ str(gWidth)+ "x"+str(gHeight)+ ".")
        file.write("\n - Nombres d'itérations du programme : "+str(iterations)+".")
        file.write("\n - Couleur de fond : "+str(gColor)+ ".")
        file.write("\n - Résolution : " +str(res)+ ".")
        if dep=='alea' :
            file.write('\n - Le mode aléatoire a été choisi')
        else :
            file.write('\n - Le mode couche par couche a été choisi')
        j = 1
        for sets in datas :
            N = sets[6]
            miL = sets[0]
            maL = sets[1]
            co = sets[2]
            rs = sets[3]
            alp = sets[4]
            typ = sets[5]
            ctr = sets[7]
            file.write("\n \n Polygones " + str(j) + '\n')
            cls = ''
            for i in co : 
                if len(cls)>0:
                    cls= cls + " | "+ str(int(cs.hex2rgb(i)[0])) +' '+ str(int(cs.hex2rgb(i)[1])) +' ' + str(int(cs.hex2rgb(i)[2]))
                else : 
                    cls = str(int(cs.hex2rgb(i)[0])) +' '+ str(int(cs.hex2rgb(i)[1])) +' ' + str(int(cs.hex2rgb(i)[2]))
            ratios = ''
            if typ =='rectangles':
                for l in rRatios : 
                    if len(ratios)>0:
                        ratios = ratios + " | " + str(round(l,3))
                    else : 
                        ratios = str(l)
            file.write("\n - Longueur caractéristique des polygones (longueur des rectangles, rayons des polygones réguliers...) :"+str(miL)+ " - "+str(maL)+ ".")
            file.write("\n - Nombre de polygones : "+str(N)+ ".")
            file.write("\n - Couleurs utilisées : "+str(cls)+ ".")
            file.write("\n - Type de polygones : "+str(typ)+ ".")
            if typ == 'rectangles' :
                file.write("\n - Ratios : "+str(ratios))
            elif typ =='reguliers':
                file.write("\n - Nombre de côtés : "+str(m))
            if ctr[0] < 0 :
                file.write('\n - Le mode choisi est non centré.')
            else :
                file.write('\n - Le centre choisi est (' +str(ctr[0]) + ',' + str(ctr[1]) +').')
            file.write("\n - Opacité : "+str(1.-alp))
            k=0
            while k<N :
                SOMME = SOMME +1
                if typ== 'rectangles' and ctr[0]<0 :
                    polys.append(randomRectangle(miL,maL,co,alp,rs))
                elif typ=='rectangles' :
                    polys.append(randomRectangleC(miL,maL,co,alp,rs,ctr))
                elif typ=='reguliers' and ctr[0]<0:
                    polys.append(randomRegulier(miL,maL,co,alp,rs))
                elif typ=='reguliers':
                    polys.append(randomRegulierC(miL,maL,co,alp,rs,ctr))
                k = k+1
            j = j+1
        file.close()
        if dep == 'alea' :
            doneN =[]
            done=[]
            ns = list(range(len(polys)))
            while len(doneN) != len(polys) :
                r = np.random.randint(len(ns))
                if r not in doneN:
                    doneN.append(r)
            for j in doneN : 
                done.append(polys[j])
        if(fromSource):
            if len(source)>4 and source[-1]=='g' and source[-2] == 'n' and source[-3] == 'p' :
                imageS = source
            else : 
                im = Image.open(source)
                im.save('sources/ImageSource.png')
                imageS = 'sources/ImageSource.png'
            figure = plt.figure(figsize = (gWidth, gHeight))
            axes = figure.add_subplot(111)
            image = mpimg.imread(imageS)
            plt.xlim(0,gWidth)
            plt.ylim(0,gHeight)
            plt.axis('off')
            plt.imshow(image,zorder = 1)
                
            for r in polys :
                axes.add_patch(patches.Polygon(r[0],closed = True,fill=None,edgecolor='#000000', linewidth = LINEWIDTH, alpha=(1-r[5]), zorder = 2)) 
            plt.savefig(filename+'/image_border'+str(c)+'.tiff',format='tiff',dpi = 2.*res)
            plt.savefig(filename+'/image_border_fix'+str(c)+'.tiff',format='tiff', dpi=res)                
            
            figure = plt.figure(figsize = (gWidth, gHeight))
            axes = figure.add_subplot(111)
            image = mpimg.imread(imageS)
            plt.xlim(0,gWidth)
            plt.ylim(0,gHeight)
            plt.axis('off')
            plt.imshow(image,zorder = 1)
                
            for r in polys :
                axes.add_patch(patches.Polygon(r[0],closed= True,color = r[4],alpha = (1-r[5]),zorder = 2))
            plt.savefig(filename+'/image_filled'+str(c)+'.tiff',format='tiff', dpi = 2.*res)
            plt.savefig(filename+'/image_filled_fix'+str(c)+'.tiff',format='tiff',dpi=res)
            
            figure = plt.figure(figsize = (gWidth, gHeight))
            axes = figure.add_subplot(111)
            image = mpimg.imread(imageS)
            plt.xlim(0,gWidth)
            plt.ylim(0,gHeight)
            plt.axis('off')
            plt.imshow(image)
            for r in polys :
                axes.add_patch(patches.Polygon(r[0],closed= True,color = r[4], alpha = (1-r[5]),zorder=2,linewidth = 0))
                axes.add_patch(patches.Polygon(r[0],closed = True,fill=None,edgecolor='#000000', linewidth=LINEWIDTH,zorder = 3)) 
            plt.savefig(filename+'/image_filled_border'+str(c)+'.tiff',format='tiff', dpi= 2.*res)
            plt.savefig(filename+'/image_filled_border_fix'+str(c)+'.tiff',format='tiff',dpi=res)             
        else : 
            figure = plt.figure(figsize = (gWidth, gHeight))
            axes = figure.add_subplot(111)
            plt.xlim(0,gWidth)
            plt.ylim(0,gHeight)
            plt.axis('off')
            
            for r in polys :
                axes.add_patch(patches.Polygon(r[0],closed = True,fill=None,edgecolor='#000000', linewidth = LINEWIDTH)) 
            plt.savefig(filename+'/image_border'+str(c)+'.tiff',format='tiff',facecolor = gColor,dpi = 2.*res)
            plt.savefig(filename+'/image_border_fix'+str(c)+'.tiff',format='tiff',facecolor=gColor, dpi=res)
            
            figure = plt.figure(figsize = (gWidth, gHeight))
            axes = figure.add_subplot(111)
            plt.xlim(0,gWidth)
            plt.ylim(0,gHeight)
            plt.axis('off')
            for r in polys :
                axes.add_patch(patches.Polygon(r[0],closed= True,color = r[4],alpha = (1-r[5]), linewidth = 0))
            plt.savefig(filename+'/image_filled'+str(c)+'.tiff',format='tiff', facecolor=gColor,dpi = 2.*res)
            plt.savefig(filename+'/image_filled_fix'+str(c)+'.tiff',format='tiff',facecolor=gColor,dpi=res)
            
            figure = plt.figure(figsize = (gWidth, gHeight))
            axes = figure.add_subplot(111)
            plt.xlim(0,gWidth)
            plt.ylim(0,gHeight)
            plt.axis('off')
            for r in polys :
                axes.add_patch(patches.Polygon(r[0],closed= True,color = r[4], alpha = (1-r[5]), linewidth = 0))
                axes.add_patch(patches.Polygon(r[0],closed = True,fill=None,edgecolor='#000000', linewidth=LINEWIDTH)) 
            plt.savefig(filename+'/image_filled_border'+str(c)+'.tiff',format='tiff', facecolor=gColor,dpi =2.*res)
            plt.savefig(filename+'/image_filled_border_fix'+str(c)+'.tiff',format='tiff',facecolor=gColor,dpi=res)
        t2 = time.time()-t1
        print("L'itération s'est executé pour ", SOMME, " polygones en ", t2, " secondes")
        c=c+1
    if follow == True :
        t3=time.time()-t0
        print('Le programme a été executé en ',t3,'s pour ', iterations, ' iterations et ', SOMME, ' polygones.')
        input('')
    os.system('cls')
#Reprendre image / semer autour d'un point
#Corriger range (Couleurs inaffichables???)    
    