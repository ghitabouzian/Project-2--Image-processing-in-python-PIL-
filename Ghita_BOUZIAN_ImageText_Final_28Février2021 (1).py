# Créé par pc, le 20/02/2021 en Python 3.7
# PROJET : CACHER UN TEXTE OU UNE IMAGE DANS UNE AUTRE IMAGE ET LES RETROUVER
# GHITA BOUZIAN

#Cette fonction convertit un nombre décimal en un nombre binaire sous forme d'une liste de 8 bits
def D2B (decimal):
  liste_B=[]
  if decimal==0:
    liste_B=[0]
  else:
    #Cette boucle construit le nombre binaire sous forme d'une liste constituée des restes des divisions successives par 2
    while decimal>=1:
      liste_B.append(decimal%2)
      decimal=decimal//2
    liste_B.reverse()
  #Calculer le nombre de 0 manquants
  x=8-len(liste_B)
  #Construire une liste de 0 manquants liste_zéro
  liste_zéro=[]
  for loop in range (x):
    liste_zéro.append(0)
  #Concaténer la liste des 0 avec la liste binaire pour avoir une liste 8 bits
  return(liste_zéro+liste_B)

#Cette fonction convertit un nombre binaire sous forme d'une liste de 8 bits en un nombre décimal
def B2D (liste_B):
  decimal=0
  liste_B.reverse()
  #Cette boucle calcule le nombre décimal en multipliant les éléments de la liste binaire inversée par des puisances de 2
  for i in range(8):
    decimal = decimal+liste_B[i]*2**i

  return(decimal)

#Cette fonction extrait X bits de poids fort d'une liste de 8 bits
def B2XHB (liste_8B, XHB):
  list_XHB=[]
  #Cette boucle construit la liste constituée des X bits de poids fort de la liste binaire
  for i in range(0,XHB):
    list_XHB.append(liste_8B[i])

  return(list_XHB)

#Cette fonction extrait X bits de poids faible d'une liste de 8 bits
def B2XLB (liste_8B, XLB):
  list_XLB=[]
  #Cette boucle construit la liste constituée des X bits de poids faible de la liste binaire
  for i in range(8-XLB,8):
    list_XLB.append(liste_8B[i])

  return(list_XLB)

#Cette fonction cache un texte dans une image en remplaçant le 1er bit de poids faible de la couleur Rouge de ses pixels par les bits du code ASCII du texte
def cacherTexte(img,texte):
    #Charger les pixels de l'image et calculer sa taille
    pixels=img.load()
    largeur,hauteur=img.size

    #Convertir la longueur du texte en binaire 8 bits
    longueurTexte_b=D2B(len(texte))
    #Convertir les codes ASCII des caractères du texte en liste de listes binaires (liste_Caractères_b)
    liste_Caractères_b=[D2B(ord(c)) for c in texte]
    #Construire une liste binaire, constituée de chaque bit de la longueur du texte et ses caractères
    #Conserver la longueur du texte permettra par la suite de trouver tout le texte caché
    liste_Longueur_Texte_b=longueurTexte_b
    for l in liste_Caractères_b:
        liste_Longueur_Texte_b= liste_Longueur_Texte_b+l

    #Calculer le nombre total de bits à cacher
    totalBits=len(liste_Longueur_Texte_b)
    #Cacher dans la suite chaque bit de la liste comprenant longueur et texte
    x=0
    y=0
    for i in range (totalBits):
        #Extraire les valeurs RVB ou RVBA d'un pixel (x,y) de l'image.
        if img.mode=='RGB':
            rouge,vert,bleu = pixels[x,y][0],pixels[x,y][1],pixels[x,y][2]
        else:
            rouge,vert,bleu,alpha = pixels[x,y][0],pixels[x,y][1],pixels[x,y][2],pixels[x,y][3]
        #Convertir la valeur Rouge en binaire 8 bits
        rouge_b=D2B(rouge)
        #Calculer la nouvelle valeur Rouge binaire 8 bits en remplaçant le 1er bit de poids faible par 1 bit de la liste lol_Longueur_Texte_b
        rouge_b=B2XHB(rouge_b,7)
        rouge_b.append(liste_Longueur_Texte_b[i])
        #Convertir la couleur Rouge binaire en décimal
        rouge=B2D(rouge_b)
        #Modifier le pixel de l'image Transformée selon son mode
        if img.mode=='RGB':
            pixels[x,y]=(rouge,vert,bleu)
        else:
            pixels[x,y]=(rouge,vert,bleu,alpha)
        #Modifier x et y sans déborder sur la largeur et la hauteur
        #i+1 le rang du prochain bit à récupérer
        x=(i+1)//400
        y=(i+1)%400



#Cette fonction retourne le texte caché dans une image transformée
def trouverTexteCaché(img_Trans):
    #Charger les pixels de l'image
    pixels=img_Trans.load()

    largeur,hauteur=img_Trans.size
    liste_8bits=[]

    #Récupérer la longueur du texte à partir du 1er octet caché
    for y in range(8):
        #Extraire la valeur Rouge du pixel (0,y) de l'image.
        rouge = pixels[0,y][0]
        #Convertir la valeur Rouge en binaire 8 bits
        rouge_b=D2B(rouge)
        #Extraire le 1er bit de poids faible du Rouge (le bit caché) sous forme d'une liste
        liste1B=B2XLB(rouge_b, 1)
        #Retrouver l'octet représentant la longueur du texte en rajoutant chaque bit caché à une liste 8 bits
        liste_8bits.append(liste1B[0])
    #Convertir la longueur du texte en décimal
    longueurTexte=B2D(liste_8bits)

    #Récupérer dans la suite les codes ASCII à partir des octets cachés autre que le 1er octet, et stocker les caractères correspondants dans une liste
    #Trouver pour cela, chaque bit caché et le traiter
    liste_8bits=[]
    listeCaractères=[]
    x=0
    y=8
    for i in range (longueurTexte*8):
        #Extraire la valeur Rouge du pixel (x,y) de l'image.
        rouge = pixels[x,y][0]
        #Convertir la valeur Rouge en binaire 8 bits
        rouge_b=D2B(rouge)
        #Extraire le 1er bit de poids faible du Rouge (le bit caché) sous forme d'une liste
        liste1B=B2XLB(rouge_b, 1)
        #Retrouver l'octet représentant le code ASCII en rajoutant chaque bit caché à une liste 8 bits
        liste_8bits.append(liste1B[0])

        #Convertir 1 octet récupéré en décimal puir char et l'ajouer à une liste de caractères
        if len(liste_8bits)==8:
            caractèreAscii=B2D(liste_8bits)
            listeCaractères.append(chr(caractèreAscii))
            liste_8bits=[]
        #Modifier x et y sans déborder sur la largeur et la hauteur
        #i+8+1 le rang du prochain bit à récupérer (8 bits de longueur inclus)
        x=(i+8+1)//400
        y=(i+8+1)%400


    #convertir la liste des caractères retrouvés en chaine de caractères et Afficher le texte caché
    texteCaché="".join(listeCaractères)
    return(texteCaché)


#Cette fonction cache une Image invisible dans une autre visible en en conservant 4 de poids fort
def cacherImg (visible, invisible):
    #Convertir les 2 images en mode RGBA pour permettre de cacher aussi la valeur d'opacité
    if visible.mode=='RGB':
        visible=visible.convert('RGBA')
    if invisible.mode=='RGB':
        invisible=invisible.convert('RGBA')
    #Charger les pixels des images visible et celle à cacher (invisible) et calculer leurs tailles
    pixels_V=visible.load()
    pixels_Inv=invisible.load()

    largeurV, hauteurV= visible.size
    largeurInv, hauteurInv= invisible.size

    for x in range(largeurInv):
       for y in range(hauteurInv):
          #Extraire les valeurs RVBA de chaque pixel (x,y) de l'image Visible et son correspondant dans l'image Invisible.
          rougeV,vertV,bleuV,alphaV = pixels_V[x,y][0], pixels_V[x,y][1], pixels_V[x,y][2], pixels_V[x,y][3]
          rougeInv,vertInv,bleuInv,alphaInv = pixels_Inv[x,y][0], pixels_Inv[x,y][1], pixels_Inv[x,y][2], pixels_Inv[x,y][3]
          #Convertir les valeurs RVBA en binaire 8 bits
          rougeV_b=D2B(rougeV)
          vertV_b=D2B(vertV)
          bleuV_b=D2B(bleuV)
          alphaV_b=D2B(alphaV)
          rougeInv_b=D2B(rougeInv)
          vertInv_b=D2B(vertInv)
          bleuInv_b=D2B(bleuInv)
          alphaInv_b=D2B(alphaInv)

          #Remplacer dans la suite les 4 de poids faible des valeurs liées à l'image Visible par ceux forts de l'image invisible

          #Extraire les 4 de poids fort des valeurs de l'image Invisible et uniquement 2 bits pour l'opacité
          rougeInv_XHB=B2XHB(rougeInv_b,4)
          vertInv_XHB=B2XHB(vertInv_b,4)
          bleuInv_XHB=B2XHB(bleuInv_b,4)
          alphaInv_XHB=B2XHB(alphaInv_b,2)
          #Extraire Ybits de poids fort des valeurs de l'image Visible (Ybits est complément de Xbits pour avoir 8 bits) et 6 bits pour l'opacité
          rougeV_YHB=B2XHB(rougeV_b,4)
          vertV_YHB=B2XHB(vertV_b,4)
          bleuV_YHB=B2XHB(bleuV_b,4)
          alphaV_YHB=B2XHB(alphaV_b,6)
          #Construire les nouvelles valeurs en concaténant les Ybits de poids fort des valeurs de l'image Visible avec les Xbits de poids fort des celles de l'image invisible
          rougeV_b=rougeV_YHB+rougeInv_XHB
          vertV_b=vertV_YHB+vertInv_XHB
          bleuV_b=bleuV_YHB+bleuInv_XHB
          alphaV_b=alphaV_YHB+alphaInv_XHB

          #Convertir les valeurs binaires en décimal
          rougeV=B2D(rougeV_b)
          vertV=B2D(vertV_b)
          bleuV=B2D(bleuV_b)
          alphaV=B2D(alphaV_b)

          #Modifier le pixel de l'image à transformer
          pixels_V[x,y]=(rougeV,vertV,bleuV,alphaV)



#Cette fonction trouve et retourne le nom de l'image cachée dans une autre déjà transformée en en récupérant 4 bits de poids faible
def trouverImgCachée (img_Trans):
    #Charger les pixels de l'image Transformée
    pixels_Trans=img_Trans.load()

    #Créer une image Invisible initiale de taille 20x20 pixels
    largeurInv=20
    hauteurInv=20
    invisible = Image.new('RGBA', (largeurInv,hauteurInv))
    pixels_Inv=invisible.load()

    for x in range(largeurInv):
        for y in range(hauteurInv):
            #Extraire les valeurs RVBA de chaque pixel (x,y) dans l'image Visible.
            rougeT,vertT,bleuT,alphaT = pixels_Trans[x,y][0], pixels_Trans[x,y][1], pixels_Trans[x,y][2], pixels_Trans[x,y][3]
            #Convertir les valeurs RVBA en binaire 8 bits
            rougeT_b=D2B(rougeT)
            vertT_b=D2B(vertT)
            bleuT_b=D2B(bleuT)
            alphaT_b=D2B(alphaT)

            #Extraire les 4 bits de poids faible des valeurs liées à l'image Transformée et uniquement 2 bits pour l'opacité
            rougeT_XLB=B2XLB(rougeT_b,4)
            vertT_XLB=B2XLB(vertT_b, 4)
            bleuT_XLB=B2XLB(bleuT_b, 4)
            alphaT_XLB=B2XLB(alphaT_b, 2)
            #Construire les octets de couleur/opacité de l'image cachée par concaténation des 4bits/2bits obtenus (comme bits de poids fort cette fois-ci) et une liste de zéros manquants
            rougeInv_b=rougeT_XLB+[0,0,0,0]
            vertInv_b=vertT_XLB+[0,0,0,0]
            bleuInv_b=bleuT_XLB+[0,0,0,0]
            alphaInv_b=alphaT_XLB+[0,0,0,0,0,0]
            #Convertir les valeurs binaires en décimal
            rougeInv=B2D(rougeInv_b)
            vertInv=B2D(vertInv_b)
            bleuInv=B2D(bleuInv_b)
            alphaInv=B2D(alphaInv_b)

            #Modifier le pixel de l'image Transformée
            pixels_Inv[x,y]=(rougeInv,vertInv,bleuInv,alphaInv)


    #Sauvegarder et Afficher l'image cachée
    invisible.save("invisibleCachée.png", "PNG")
    return("invisibleCachée.png")

#Programme Principal
import os.path
from PIL import Image

#Lecture de nom valide de l'image à transformer
existImg=False
largeur = hauteur = 0
while not(existImg) or largeur!=400 or hauteur!=400 :
    nom_Img=input("Nom de l'image à transformer : ")
    existImg=os.path.exists(nom_Img)
    if existImg :
        #Ouvrir l'image
        img = Image.open(nom_Img)
        #Calculer sa résolution
        largeur, hauteur= img.size

#Lecture du texte à cacher (texte) devant être de taille inférieure à 255

#La longueur binaire du texte est stockée dans 1 octet
longueurTexte=0
while longueurTexte<1 or longueurTexte+1>255:
    texte=input("Texte à cacher (entre 1 et 255 caractères max) : ")
    longueurTexte=len(texte)

#Appel de la fonction de transformation cacherTexte
cacherTexte(img,texte)
#Sauvegarder et Afficher l'image transformée
img.save(nom_Img, "PNG")
img.show()


#Question1.b
#Lecture du nom valide de l'image transformée
existImg=False
largeurT = hauteurT = 0
while not(existImg) or largeurT!=400 or hauteurT!=400 :
    NomImg_Trans=input("Nom de l'image transformée : ")
    existImg=os.path.exists(NomImg_Trans)
    if existImg:
        #Ouvrir l'image transformée
        img_Trans = Image.open(NomImg_Trans)
        #Calculer sa résolution
        largeurT, hauteurT= img_Trans.size

#Affichage du texte caché après appel de la fonction de détection trouverTexteCaché
print(trouverTexteCaché(img_Trans))

#Question2.a
#Lecture de noms valides d'images à transformer et celle à cacher (relecture si elles n'existent pas)
existImgV=False
existImgInv=False
largeurV = hauteurV = largeurInv = hauteurInv = 0
while not(existImgV) or not(existImgInv) or largeurV!=400 or hauteurV!=400 or largeurInv!=20 or hauteurInv!=20:
    imgV=input("Nom de l'image à transformer : ")
    imgInv=input("Nom de l'image à cacher : ")
    existImgV=os.path.exists(imgV)
    existImgInv=os.path.exists(imgInv)
    if existImgV and existImgInv:
        #Ouvrir les images visible et celle à cacher (invisible)
        visible = Image.open(imgV)
        invisible = Image.open(imgInv)
        #Calculer leurs résolutions
        largeurV, hauteurV= visible.size
        largeurInv, hauteurInv= invisible.size

#Appel de la fonction de transformation cacherImg
cacherImg(visible,invisible)
#Sauvegarde et Affichage de l'image transformée
visible.save(imgV, "PNG")
visible.show()

#Question2.b
#Lecture du nom valide de l'image transformée
existImg=False
largeurV = hauteurV = 0
while not(existImg) or largeurV!=400 or hauteurV!=400 :
    NomImg_Trans=input("Nom de l'image transformée : ")
    existImg=os.path.exists(NomImg_Trans)
    if existImg:
        #Ouvrir l'image visible transformée
        visible = Image.open(NomImg_Trans)
        #Calculer sa résolution
        largeurV, hauteurV= visible.size

#Appel de la fonction de détection de l'image cachée trouverImgCachée
NomImg_Inv=trouverImgCachée(visible)
#Ouverture et affichage de l'image cachée
invisible = Image.open(NomImg_Inv)
invisible.show()
