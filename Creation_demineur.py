from PIL.Image import*
import turtle as tl

#liste_vert  = ['#3CB371','#2E8B57']
#liste_beige = ['#F0E68C','#FFCD75']

def tableau():
    taille = [15, 30, 60]
    for k in range(3):
        tableau = new("RGB", (599,599),'black')
        
        liste_vert = ['#3CB371','#2E8B57']
        dimension = (taille[k],taille[k])
        liste_case = [new("RGB", dimension,liste_vert[0]), new("RGB", dimension,liste_vert[1])]
        
        for i in range(600//taille[k]):
            for j in range(600//taille[k]):
                tableau.paste(liste_case[(i+j)%2],(i*taille[k],j*taille[k]))

        tableau.save(f"tableau_demineur_{k+1}.png","PNG")

def case():
    taille = [60, 30, 15]
    for i in range(3):
        dimension = (taille[i],taille[i])
        new("RGB", dimension,'#F0E68C').save(f"case_beige_0_{100*2**(2*i)}.png","PNG")
        new("RGB", dimension,'#FFCD75').save(f"case_beige_1_{100*2**(2*i)}.png","PNG")
        new("RGB", dimension,'#3CB371').save(f"case_vert_0_{100*2**(2*i)}.png","PNG")
        new("RGB", dimension,'#2E8B57').save(f"case_vert_1_{100*2**(2*i)}.png","PNG")
        new("RGB", dimension,'red').save(f"case_rouge_{100*2**(2*i)}.png","PNG")

def png():
    img = open("fleur.jpg").convert("RGBA")
    L,H = img.size
    for i in range(L):
        for j in range(H):
            x = img.getpixel((i,j))
            y = (x[0]+x[1]+x[2])//3
            if y >=175:
                img.putpixel((i,j),((255,255,255,0)))
            else:
                img.putpixel((i,j),x)
    img.save("Flag2.png","PNG")

#La fleur
    
def petal():
    tl.begin_fill()
    tl.circle(50, 90)
    tl.lt(90)
    tl.circle(50, 90)
    tl.end_fill()
    tl.lt(18)
    
def flower():
    petal()
    petal()
    petal()
    petal()
    petal()    

def little_flower(x = 0, i = 1):
    tl.speed(0)
    tl.setup(200,300)
    tl.hideturtle()
    tl.bgcolor('#87CEEB')
    
    tl.color('green')
    tl.width(12)
    tl.pu()
    tl.goto(0,-150)
    tl.pd()
    tl.lt(90)
    tl.fd(70)
    petal()
    tl.lt(72)
    tl.fd(100)
    if x == 0:
        tl.color('#9518BA','#A530C8')
    else:
        ListeMine = ['#E74C3C','#9B59B6','#3498DB','#1ABC9C','#28B463','#D4AC0D','#F39C12']
        shuffle(ListeMine)
        tl.color(ListeMine[0] , ListeMine[1])
    flower()
    tl.rt(90)
    tl.width(1)
    tl.mainloop()
    tl.getcanvas().postscript(f'petite_fleur_{i}.png')

#png()
#tableau()
#case()
png()
#for i in range (10):
#    little_flower(0,i)