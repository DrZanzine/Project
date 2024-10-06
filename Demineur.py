from random import shuffle
import time as tm
import pygame
from pygame.locals import *
from math import*
global case_restante, liste_beige, bombe, fini, panneau_case_restante, nb_bombe

pygame.init()
pygame.key.set_repeat(400, 30)

# =============================================================================
# 
# =============================================================================

class Cellule():
    def __init__(self, coords:tuple , contenu:int = 0 , cacher:int = 1):
        self.coords = coords#(i,j)
        self.contenu = contenu
        self.cacher = cacher
        
    def __repr__(self):
        i , j = self.coords
        return str(self.contenu)
    
    def est_mine(self):
        return self.contenu() == True

    def cellule_voisine(self, dim:int):
        i , j = self.coords
        cellule_voisine = []
        for k , l in [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j-1),(i+1,j),(i+1,j+1)]:
            if 0 <= k < dim and 0 <= l < dim:
                cellule_voisine.append((k,l))
        return cellule_voisine
        
 
class Tableau():
    def __init__(self, dim:int, N_D_Bombe:int):
        self.dim = dim
        self.nombre_de_bombes = N_D_Bombe
        matrice = [[Cellule((i,j)) for j in range(dim)] for i in range(dim)]
        tab = [(i,j) for i in range(dim) for j in range(dim)]
        shuffle(tab)
        tab = tab[: N_D_Bombe]
        for i , j in tab:
            matrice[i][j].contenu = -1
        for i in range(dim):
            for j in range(dim):
                if matrice[i][j].contenu != -1:
                    tab_vois = matrice[i][j].cellule_voisine(dim)
                    mine_voisine = 0
                    for k , l in tab_vois:
                        if matrice[k][l].contenu == -1:
                            mine_voisine += 1
                    matrice[i][j].contenu = mine_voisine
        self.matrice = matrice
        
# =============================================================================
# 
# =============================================================================

def ecriture(texte:str, coords:tuple, scale=20, color = 'black'):
    x, y = coords
    font = pygame.font.SysFont("arialblack",scale , color)
    temp_img = font.render(str(texte),1,(1, 23, 51),'white')
    temp_rect = temp_img.get_rect()
    fenetre.blit(temp_img,(x - temp_rect.right/2, y - temp_rect.bottom/2))
    
def ecriture_and_slice(texte):
    liste = texte.splitlines()
    n = 1
    for ligne in liste:
        ecriture(ligne,(800/2,300/2 + 29*n),20 ,'white')
        n += 1

def devoile(coords):
    global echelle, bombe, case_restante, fini, panneau_case_restante, nb_bombe
    i , j = coords
    cellule = plateau.matrice[i][j]
    n = cellule.contenu
    
    if cellule.cacher == 1:
        cellule.cacher = 0
        case_restante -= 1
        #Cas ou cellule n'est pas une mauvaise case
        if n >= 0:
            fenetre.blit(liste_beige[(i+j)%2], (j*echelle, i*echelle))
            
            if n == 0:
                for duo in cellule.cellule_voisine(dim):
                    devoile(duo)
            
            elif n > 0 :
                aff_chif(coords , n)
                
        #cas ou cellule est une mauvaise case
        else:
            case_restante += 1
            fenetre.blit(bombe,(j*echelle , i*echelle))
            liste_mine = []
            for k in range (dim):
                for l in range (dim):
                    if plateau.matrice[k][l].contenu == -1 and plateau.matrice[k][l].cacher == 1:
                        fenetre.blit(bombe,(l*echelle , k*echelle))
                        plateau.matrice[k][l].cacher = 0
            fini = True
            ecriture('BOOM !', (300,300), 'red', 100)
    
    fenetre.blit(panneau_case_restante,(599,60))
    ecriture(case_restante-nb_bombe, (699,95))
    
    if case_restante - nb_bombe == 0:
        ecriture('GAGNER !', (300,300), 'red', 100)
        fini = True
        
def aff_chif(coords , n):
    i , j = coords
    ListeCouleursChif = ['#1834CF','#16B84E','#EE1010','#6C0277','#048B9A','#801818','#BD33A4','#000000']
    ecriture(n, (j*echelle+echelle//2, i *echelle+echelle//2), ListeCouleursChif[n-1], echelle//2)

# =============================================================================
# 
# =============================================================================

fenetre = pygame.display.set_mode((799, 599))
fond = pygame.image.load("Fond.png").convert()
police = pygame.font.SysFont("arialblack",20 , 'black')
fenetre.blit(fond,(0,0))
pygame.display.update()

liste_texte = ["Bienvenue sur l'incroyable, l'unique et fantastique démineur de Ziane !!!\n('Espace' pour continuer...)",
               "Pour commencer le jeux, nous allons devoir mettre au point\nquelque réglage qui viendront par la suite,",
               "D'abord, nous aurons la dimension du plateau.\n100 case | 400 case | 1600 case (pour les fous),",
               "Ensuite la difficulté du jeux,\nqui se traduit par la fréquence de bombe.",
               "Les difficultées sont les suivantes:\nfacile: 1 bombe toute les 10 cases | normal: 1 pour 6 | difficile: 1 pour 4",
               "Des rappel vous seront donner évidemment ;)",
               "Et enfin, pour vos prochaines parties,\nje vous invite à presser 'retour' pour passer tout ces dialogues\nBon jeux et Bonne chance !!!"]


while True:
    continuer = True
    valeur = ["dimension", "nb_bombe", 0]
    n = 0
    while continuer and len(liste_texte) > n >= 0:
        fenetre.blit(fond,(0,0))
        ecriture_and_slice(liste_texte[n])
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    n += 1
                if event.key == pygame.K_BACKSPACE:
                    n = -1
        
        pygame.display.update()
        
    
    rect_input = pygame.Rect(100,300,10,35)
    txt = ''
    value = 0
    n = 0
    l = ["Quelle dimensions voulez vous ?\n100, 400 ou 1600 cases","Ne rentrez que '100', '400' ou '1600' cases"]
    while continuer and valeur[0] == "dimension":
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    txt = txt[:-1]
                elif event.key == pygame.K_RETURN:
                    value = txt
                else:
                    txt += event.unicode
                
        if value != 0:
            n = 1
            if value in ["100","400","1600"]:
                valeur[0] = int(txt)
            else:
                txt = ''
                value = 0
                fenetre.blit(fond,(0,0))
                ecriture_and_slice(l[n])
                surface_txt = police.render(txt ,1,(1, 23, 51))
                pygame.draw.rect(fenetre,'lightblue',rect_input)
                fenetre.blit(surface_txt,(rect_input.x,rect_input.y))
                rect_input.w = max(10, surface_txt.get_width() + 5)
                pygame.display.update()
        else:
            fenetre.blit(fond,(0,0))
            ecriture_and_slice(l[n])
            surface_txt = police.render(txt ,1,(1, 23, 51))
            pygame.draw.rect(fenetre,'lightblue',rect_input)
            fenetre.blit(surface_txt,(rect_input.x,rect_input.y))
            rect_input.w = max(10, surface_txt.get_width() + 5)
            pygame.display.update()
    
    
    
    rect_input = pygame.Rect(100,300,10,35)
    txt = ''
    value = 0
    n = 0
    l = ["Quelle difficulté voulez vous ?\nfacile(1 pour 10), normale(1 pour 6) ou difficile (1 pour 4)","Ne rentrez que 'facile', 'normale' ou 'difficile'"]
    while continuer and valeur[1] == "nb_bombe":
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    txt = txt[:-1]
                elif event.key == pygame.K_RETURN:
                    value = txt
                else:
                    txt += event.unicode  
                
                
        if value != 0:
            n = 1
            if value in ["facile","normale","difficile"]:
                if value == "facile":
                    valeur[1] = 0.1
                elif value == "normale":
                    valeur[1] = 0.17
                elif value == "difficile":
                    valeur[1] = 0.25
            else:
                txt = ''
                value = 0
                fenetre.blit(fond,(0,0))
                ecriture_and_slice(l[n])
                surface_txt = police.render(txt ,1,(1, 23, 51))
                pygame.draw.rect(fenetre,'lightblue',rect_input)
                fenetre.blit(surface_txt,(rect_input.x,rect_input.y))
                rect_input.w = max(10, surface_txt.get_width() + 5)
                pygame.display.update()
        else:
            fenetre.blit(fond,(0,0))
            ecriture_and_slice(l[n])
            surface_txt = police.render(txt ,1,(1, 23, 51))
            pygame.draw.rect(fenetre,'lightblue',rect_input)
            fenetre.blit(surface_txt,(rect_input.x,rect_input.y))
            rect_input.w = max(10, surface_txt.get_width() + 5)
            pygame.display.update()
    
    if valeur[0] != "dimension":
        case_restante , ratio = valeur[0],valeur[1]
        dim = int(sqrt(case_restante))    
        if case_restante == 1600:
            echelle = 15
        elif case_restante == 400:
            echelle = 30
        elif case_restante == 100:
            echelle = 60
        
        beige_0 = pygame.image.load(f"case_beige_0_{case_restante}.png").convert()
        beige_1 = pygame.image.load(f"case_beige_1_{case_restante}.png").convert()
        liste_beige = (beige_0, beige_1)
        
        vert_0 = pygame.image.load(f"case_vert_0_{case_restante}.png").convert()
        vert_1 = pygame.image.load(f"case_vert_1_{case_restante}.png").convert()
        liste_vert = (vert_0, vert_1)
        
        flag = pygame.image.load(f"Flag_{case_restante}.png").convert_alpha()
        bombe = pygame.image.load(f"Bombe_{case_restante}.png").convert_alpha()
        
        nb_bombe = int(ratio*dim**2)
        plateau = Tableau(dim, nb_bombe)
        tableau = pygame.image.load(f"tableau_demineur_{dim**2}.png").convert()
        fenetre.fill('#87CEEB')
        fenetre.blit(tableau,(0,0))
        
        mine_restante = pygame.image.load(f"Mine_restante.png").convert()
        fenetre.blit(mine_restante,(599,0))
        ecriture(nb_bombe, (699,35))
        
        panneau_case_restante = pygame.image.load(f"Cases_non_révélé.png").convert()
        fenetre.blit(panneau_case_restante,(599,60))
        ecriture(case_restante-nb_bombe, (699,95))
        
        temp = pygame.image.load(f"Temps.png").convert()
        fenetre.blit(temp,(599,420))
        ecriture("00:00", (699,455))
        
        button_recommencer = pygame.image.load(f"Recommencer.png").convert()
        fenetre.blit(button_recommencer,(599,480))
        recommencer_rect = button_recommencer.get_rect()
        recommencer_rect.topleft = (599,480)
        
        button_quitter = pygame.image.load(f"Quitter.png").convert()
        fenetre.blit(button_quitter,(599,540))
        quitter_rect = button_quitter.get_rect()
        quitter_rect.topleft = (599,540)
        
        pygame.display.update()
        fini = False
    
    debut = tm.time()
    while continuer :
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pressed()
                x, y = pygame.mouse.get_pos()
                if not fini:
                    if click[0]:
                        if x < 600:
                            devoile((y//echelle, x//echelle))
                            
                    elif click[2]:
                        if x < 600:
                            i, j = y//echelle, x//echelle
                            if plateau.matrice[i][j].cacher == 2:
                                fenetre.blit(liste_vert[(i+j)%2],(j*echelle, i*echelle))
                                plateau.matrice[i][j].cacher = 1
                                
                            elif plateau.matrice[i][j].cacher == 1:
                                fenetre.blit(flag,(j*echelle, i*echelle))
                                plateau.matrice[i][j].cacher = 2
                if x >= 600:
                    if click[0]:
                        i, j = recommencer_rect.topleft
                        k, l = recommencer_rect.bottomright
                        if i < x < k and j < y < l:
                            continuer = False
                        
                    if click[0]:
                        i, j = quitter_rect.topleft
                        k, l = quitter_rect.bottomright
                        if i < x < k and j < y < l:
                            pygame.quit()
        if not fini:
            fenetre.blit(temp,(599,420))
            temps = int(tm.time() - debut)
            minute = temps // 60
            seconde = temps % 60
            ecriture(str(minute)+":"+str(seconde), (699,455))         
        pygame.display.update()

                
pygame.quit()