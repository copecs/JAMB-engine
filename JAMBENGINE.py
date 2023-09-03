import time
import re
X = int(time.time())
next_nadole=0
next_nagore=9

class Coo:
    def __init__(self, r, c, v):
        self.r = r
        self.c = c
        self.v = v


def bit_parity(br):
    num = 0
    while br > 0:
        num += 1 if br % 2 == 1 else 0
        br >>= 1
    return num % 2


def bintoint(broj: str):
    p = 1
    s = 0
    for i in range(2, -1, -1):
        if broj[i] == "1":
            s += p
        p *= 2
    return s


def randomkockica():
    def rnd():
        m = 6345147*5748019
        #m = 8467*8501 #neke druge vrednosti
        #m = 482718298365513*473049867772689 #neke druge vrednosti
        broj = ""
        global X
        for i in range(3):
            X = (X * X) % m
            broj += str(bit_parity(X))
        return bintoint(broj)
    a = rnd()
    while a == 0 or a == 7:
        a = rnd()
    return a


def rolaj(dices, indexi):
    indexi = [ord(i) - ord('0') for i in indexi]
    for i in indexi:
        dices[i - 1] = randomkockica()


def print_table(matrica,table_coo,sume):
    a,b,c=0,0,0
    n=len(table_coo) if table_coo!=0 else 0
    display = "123456KFPJ"
    print("     ↓↓     ↑↑   rucna")
    for i in range(10):
        if(table_coo!=0):
            j = 0
            while j < n:
                if table_coo[j].r == i and table_coo[j].c == 0:
                    a = table_coo[j].v

                if table_coo[j].r == i and table_coo[j].c == 1:
                    b = table_coo[j].v

                if table_coo[j].r == i and table_coo[j].c == 2:
                    c = table_coo[j].v
                j += 1
        else:
            a,b,c=matrica[i][0],matrica[i][1],matrica[i][2]
        print("{:>}   |{:>2}|   |{:>2}|  |{:>2}|".format(display[i], a if a>=0 else "X", b if b>=0 else "X", c if c>=0 else "X"))
        a, b, c = 0, 0, 0
    print("SUME:{:>2}     {:>2}    {:>2} ".format(sume[0],sume[1],sume[2]))
    print("Ukupan broj bodova je: {}".format(sume[0]+sume[1]+sume[2]))


def check_input_polje(polje):
    pattern=r"^([JFKP]|[1-6])[123]$"
    return re.match(pattern,polje)

def prvo_polje(char):
    switch_case = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "K": 7, "F": 8, "P": 9, "J": 10}
    return switch_case[char.upper()]


def intable_coo(i, j, table_coo, n):
    for l in range(n):
        if i == table_coo[l].r and j == table_coo[l].c:
            return True
    return False


def validno_polje(polje, table_coo, brbacanja,matrica):
    global next_nadole
    global next_nagore
    n=len(table_coo) if table_coo!=0 else 0
    if(len(polje)!=2):
        return False
    i,j=prvo_polje(polje[0]) - 1 , int(polje[1]) - 1
    if j == 0 and next_nadole==i and i<=9:
        return True
    if j == 1 and next_nagore==i and i>=0:
        return True
    if j == 2 and brbacanja==0:
        if table_coo!=0 and not intable_coo(i,j,table_coo,n):
            return True
        elif matrica!=0 and not matrica[i][j]!=0:
            return True
    return False


def kenta(dices, brbacanja):
    suma = [0, 0, 0, 0, 0, 0]
    for dice in dices:
        suma[dice - 1] += 1
    if suma.count(1) == 5 and (sum(dices) == 15 or sum(dices) == 20):
        return 66 - 10 * brbacanja
    else:
        return 0


def ful(dices):
    suma = [0, 0, 0, 0, 0, 0]
    twos, threes = 0, 0
    for dice in dices:
        suma[dice - 1] += 1
    for i in range(6):
        if suma[i] == 3:
            threes = i + 1
        elif suma[i] == 2:
            twos = i + 1
    if threes and twos:
        return 30 + threes * 3 + twos * 2
    return 0


def poker(dices):
    suma = [0, 0, 0, 0, 0, 0]
    for dice in dices:
        suma[dice - 1] += 1
    for i in range(6):
        if suma[i] == 4:
            return 40 + (i + 1) * 4
    return 0


def jamb(dices):
    suma = [0, 0, 0, 0, 0, 0]
    for dice in dices:
        suma[dice - 1] += 1
    for i in range(6):
        if suma[i] == 5:
            return 50 + (i + 1) * 5
    return 0


def coo_to_matrix(table_coo, matrica):
    for i in range(10):
        matrica.append([0, 0, 0])
    for i in range(len(table_coo)):
        matrica[table_coo[i].r][table_coo[i].c] = table_coo[i].v
    del(table_coo)


def update_sum(matrica,table_coo,poeni,j,n):
    if table_coo!=0:
        for i in range(n):
            if table_coo[i].r==10 and table_coo[i].c==j:
                table_coo[i].v+=poeni if poeni>0 else 0
    else:
        matrica[10][j]+=poeni if poeni>0 else 0


def odigraj_poen(polje,dices,matrica,brbacanja,table_coo,i,j,sume):
    global next_nadole
    global next_nagore

    if i==-1 and j==-1:
        i = prvo_polje(polje[0]) - 1
        j = int(polje[1]) - 1
    poeni = 0
    if j==0:
        if next_nadole<=9:
            next_nadole+=1
    if j==1:
        if next_nagore>=0:
            next_nagore-=1
    if i >= 0 and i < 6:
        poeni = dices.count(i + 1) * (i + 1)
    elif i == 6:
        poeni = kenta(dices, brbacanja)
    elif i == 7:
        poeni = ful(dices)
    elif i == 8:
        poeni = poker(dices)
    elif i == 9:
        poeni = jamb(dices)
    sume[j]+=poeni
    poeni = poeni if poeni > 0 else -1
    if(table_coo!=0):
        table_coo.append(Coo(i, j, poeni))
    else:
        matrica[i][j] = poeni


#pomocprijatelja
def check_combos(dices,brojbacanja,table_coo,matrica):
    mp=0
    mnd=0
    polje=""
    for i in range(6):
        num_dices=dices.count(i+1)
        p=num_dices*(i+1)
        if(table_coo!=0 and validno_polje(str(i+1)+"3",table_coo,brojbacanja,0)) or (matrica !=0 and validno_polje(str(i+1)+"3",0,brojbacanja,matrica)):
            if num_dices>=mnd and p>mp:
                polje=str(i+1)+"3"
                mnd=num_dices
                mp=p
    p=kenta(dices,brojbacanja)
    if(p and p>mp):
        if (matrica !=0 and validno_polje("k3",0,brojbacanja,matrica)) or (table_coo!=0 and validno_polje("k3",table_coo,brojbacanja,0)):
            mp=p; polje="K3"

    p=ful(dices)
    if(p and p>mp):
        if (matrica !=0 and validno_polje("f3",0,brojbacanja,matrica)) or (table_coo!=0 and validno_polje("f3",table_coo,brojbacanja,0)):
            mp=p; polje="F3"

    p=poker(dices)
    if(p and p>mp):
        if (matrica !=0 and validno_polje("p3",0,brojbacanja,matrica)) or (table_coo!=0 and validno_polje("p3",table_coo,brojbacanja,0)):
            mp=p; polje="P3"
    p=jamb(dices)
    if(p and p>mp):
        if (matrica !=0 and validno_polje("j3",0,brojbacanja,matrica)) or (table_coo!=0 and validno_polje("j3",table_coo,brojbacanja,0)):
            polje="J3"

    return polje


def bot_roll(dices, combb):
    if combb>=0 and combb<=5:
        for j in range(2):
            rol = ""
            for i in range(5):
                if dices[i] != (combb+1): rol += str(i + 1)
            rolaj(dices, rol)
            print("Bot je izrolao: {}".format(dices))
    suma=[0,0,0,0,0,0]
    sumiraj(dices,suma)
    if combb==9:
        for j in range(2):
            rol=""
            sum=max(suma)
            if sum!=5:
                kockica=suma.index(sum)+1
                for i in range(5):
                    if dices[i] != kockica:
                        rol+= str(i+1)
                rolaj(dices,rol)
                print("Bot je izrolao: {}".format(dices))
                sumiraj(dices, suma)
            else:
                break
    if combb==8:
        for j in range(2):
            rol=""
            sum=max(suma)
            if sum!=4:
                kockica=suma.index(sum)+1
                for i in range(5):
                    if dices[i] != kockica:
                        rol+= str(i+1)
                rolaj(dices,rol)
                print("Bot je izrolao: {}".format(dices))
                sumiraj(dices, suma)
            else:
                break
    if combb==7:
        for i in range(2):
            sumiraj(dices, suma)
            sum1 = max(suma)
            kockica1 = suma.index(sum1) + 1
            suma.remove(sum1)
            sum2 = max(suma)
            kockica2 = suma.index(sum2) + 2
            rol=""
            if sum1<=3 and sum2<=2 or sum2<=3 and sum1<=2:
                for i in range(5):
                    if dices[i] != kockica1 and dices[i] != kockica2:
                        rol+= str(i+1)
            if sum1>3:
                n=5-sum1
                for i in range(5):
                    if dices[i] == kockica1 and n>0:
                        rol+=str(i+1)
                        n-=1
            if sum2>3:
                n=5-sum1
                for i in range(5):
                    if dices[i] == kockica2 and n>0:
                        rol+=str(i+1)
                        n-=1
            rolaj(dices,rol)
            print("Bot je izrolao: {}".format(dices))
    if combb==6:
        for l in range(2):
            sumiraj(dices,suma)
            notoneelements=[]
            rol=""
            if 1 in dices and 6 in dices:
                dices[dices.index(6)]=1
            for i in range(6):
                if suma[i]>1:
                    notoneelements.append(i+1)
            for element in notoneelements:
                for i in range(5):
                    if dices[i]==element:
                        rol+=str(i+1)
                rol=rol[:-1]
            rolaj(dices,rol)
            print("Bot je izrolao: {}".format(dices))
            sumiraj(dices,suma)


def sumiraj(dices,suma):
    suma.clear()
    suma.extend([0,0,0,0,0,0])
    for dice in dices:
        suma[dice-1]+=1


def return_probability(dices,expected):
    valid=0
    for i in range(1000):
        for j in range(len(dices)):
            dices[j]=randomkockica()
        if (moj_subset(dices,expected)):
            valid+=1
    return valid/1000


def check_probability(dices,comb):
    probability=0
    suma=[0,0,0,0,0,0]
    expected=[]
    sumiraj(dices,suma)
    if (comb>0 and comb<6):
        return dices.count(comb+1)
    #kenta
    if(comb==6):
        if suma[0]==0:
            for i in range(1,6):
                if suma[i]==0:
                    expected.append(i+1)
        else:
            for i in range(0,5):
                if suma[i]==0:
                    expected.append(i+1)
        probability=return_probability([0]*len(expected),expected)

    #kraj kente
    #full
    if(comb==7):
        num1=max(suma)
        rols=0
        kockica1=suma.index(num1)+1
        suma.pop(kockica1-1)
        num2=max(suma)
        kockica2=suma.index(num2)+2
        while(num1!=3 and num2!=2):
            if num1>3:
                num1-=1
                rols+=1
            elif num1<3:
                num1+=1
                rols+=1
                expected.append(kockica1)
            if num2>2:
                num2-=1
                rols+=1
            elif num2<2:
                num2+=1
                rols+=1
                expected.append(kockica2)
        probability=return_probability([0]*len(expected),expected)
    #kraj fula

    #poker
    if(comb==8):
        num=max(suma)
        kockica=suma.index(num)+1
        while(num!=4):
            if num>4:
                return 1
            else:
                num+=1
                expected.append(kockica)
        probability=return_probability([0]*(len(expected)+1),expected)
    #kraj pokera

    #jamb
    if(comb==9):
        num=max(suma)
        kockica=suma.index(num)+1
        if num==5:
            return 1
        while(num!=5):
            num+=1
            expected.append(kockica)
        probability=return_probability([0]*(len(expected)),expected)
    #krajjamba
    return probability


def moj_subset(dices,expected):
    br_dices=len(dices)
    br_expected=len(expected)
    copy=dices[:]
    for i in range(br_expected):
        if expected[i] in copy:
            copy.remove(expected[i])
    return True if len(copy)==br_dices-br_expected else False


def pomoc_prijatelja(table_coo,matrica,dices,sume):
    def play_for_nadole(dices,next_nadole,brojbacanja,table_coo,matrica,sume):
        bot_roll(dices, next_nadole)
        if table_coo != 0:
            odigraj_poen("", dices, 0, brojbacanja, table_coo, next_nadole, 0, sume)
        else:
            odigraj_poen("", dices, matrica, brojbacanja, table_coo, next_nadole, 0, sume)
    def play_for_nagore(dices,next_nagore,brojbacanja,table_coo,matrica,sume):
        bot_roll(dices, next_nagore)
        if table_coo != 0:
            odigraj_poen("", dices, 0, brojbacanja, table_coo, next_nagore, 1, sume)
        else:
            odigraj_poen("", dices, matrica, brojbacanja, table_coo, next_nagore, 1, sume)
    brojbacanja=0
    global next_nadole
    global next_nagore
    print("Kockice su: {}".format(dices))
    polje=check_combos(dices,brojbacanja,table_coo,matrica)
    if polje!="" and table_coo!=0:
        odigraj_poen(polje,dices,0,brojbacanja,table_coo,-1,-1,sume) #popunjavanje rucne
    elif polje!="" and matrica!=0:
        odigraj_poen(polje, dices, matrica, brojbacanja,0,-1,-1,sume)  # popunjavanje rucne
    elif next_nadole<=9 or next_nagore>=0:
        if next_nadole>5 and next_nagore<=5 and next_nagore>=0:
            if(check_probability(dices[:],next_nadole)>0.35):
                play_for_nadole(dices, next_nadole, brojbacanja, table_coo, matrica, sume)
            else:
                play_for_nagore(dices, next_nagore, brojbacanja, table_coo, matrica, sume)
        elif next_nadole<=5 and next_nadole>=0 and next_nagore<=5 and next_nagore>=0:
            if(check_probability(dices[:],next_nadole)>=check_probability(dices[:],next_nagore)):
                play_for_nadole(dices, next_nadole, brojbacanja, table_coo, matrica, sume)
            else:
                play_for_nagore(dices, next_nagore, brojbacanja, table_coo, matrica, sume)
        elif next_nagore>5 and next_nadole>5:
            if(check_probability(dices[:],next_nagore)>=check_probability(dices[:],next_nadole)):
                play_for_nagore(dices, next_nagore, brojbacanja, table_coo, matrica, sume)
            else:
                play_for_nadole(dices, next_nadole, brojbacanja, table_coo, matrica, sume)
        elif next_nagore>5 and next_nagore<=9 and next_nadole<=5 and next_nadole>=0:
            if (check_probability(dices[:], next_nagore) > 0.35):
                play_for_nadole(dices, next_nadole, brojbacanja, table_coo, matrica, sume)
            else:
                play_for_nagore(dices, next_nagore, brojbacanja, table_coo, matrica, sume)
        elif next_nadole<=9 and next_nadole>=0 and next_nagore<0:
            play_for_nadole(dices, next_nadole, brojbacanja, table_coo, matrica, sume)
        elif next_nagore>=0 and next_nadole<0:
            play_for_nagore(dices, next_nagore, brojbacanja, table_coo, matrica, sume)

    else:
        precrtavaj_rucnu(matrica,dices,sume)


def precrtavaj_rucnu(matrica,dices,sume):
    for i in range(10):
        if matrica[i][2]==0:
            odigraj_poen("",dices,matrica,0,0,i,2,sume)
            return
#pomocprijatelja

def jedanpotez(table_coo,matrica,dices,sume):
    global next_nadole
    global next_nagore
    rolaj(dices,"12345")
    print(dices)
    br=0
    if next_nadole<=9 or next_nagore>=0:
        for i in range(2):
            print("Izaberite da li zelite da opet rolate kockice 1-DA, 0-NE"); inp=input()
            if inp=="1":
                print("Izaberite koje indexe opet rolate 1-5 npr 235"); inp=input(); rolaj(dices,inp); print(dices); br+=1
            else:
                break
    print("Unesite polje koje zelite da odigrate npr (F1,11,K2,J3)")
    inp=input()
    a=validno_polje(inp,table_coo,br,0) if table_coo!=0 else validno_polje(inp,0,br,matrica)
    while not check_input_polje(inp) and not a:
        print("Nevalidno polje unesite neko drugo")
        inp=input()
        a = validno_polje(inp, table_coo, br, 0) if table_coo != 0 else validno_polje(inp, 0, br, matrica)

    if matrica!=0:
        odigraj_poen(inp,dices,matrica,br,0,-1,-1,sume)
    else:
        odigraj_poen(inp,dices,0,br,table_coo,-1,-1,sume)


def gameplay():
    popunjeno=0
    table_coo = []
    matrica=[]
    dices=[0,0,0,0,0]
    sume=[0,0,0]
    rolaj(dices, "12345")
    while(popunjeno!=30):
        print_table(matrica, 0,sume) if matrica != [] else print_table(0, table_coo,sume) # automatski da ispisuje posle svakog poteza
        menu()
        inp=input()
        if inp == "1": return 1
        elif inp == "3" and matrica==[]:
            jedanpotez(table_coo,0,dices,sume); popunjeno+=1
        elif inp == "3" and matrica != []:
            jedanpotez(0,matrica,dices,sume); popunjeno+=1
        elif inp == "2": print_table(matrica,0,sume) if matrica!=[] else print_table(0,table_coo,sume)
        elif inp.lower() == "endgame": return 0
        elif inp == "4" and matrica==[]:
            pomoc_prijatelja(table_coo,0,dices,sume); popunjeno+=1
        elif inp == "4" and matrica!=[]:
            pomoc_prijatelja(0,matrica,dices,sume); popunjeno+=1
        else:
            print("Ne validan unos")
        if(popunjeno==10):
            coo_to_matrix(table_coo, matrica)
        rolaj(dices, "12345")
    print_table(matrica, 0,sume)
    print("GOTOVA RUNDA newgame za novu igru endgame za terminaciju")
    inp = input()
    if inp.lower()=="endgame": return 0
    if inp.lower()=="newgame": return 1

def menu():
    print("1 - Stvaranje novog talona za igru")
    print("2 - Ispis talona uz ispis trenutnog broja bodova")
    print("3 - Odigraj potez")
    print("4 - Pomoc prijatelja(kompjuter igra ceo potez umesto vas)")

#print("TEST UNIFORMNE RASPODELE")
#test={1:0,2:0,3:0,4:0,5:0,6:0}
#for i in range(60000):
#    test[randomkockica()]+=1
#print(test)
#print("_______________________")

a=1
while(a!=0):
    next_nadole=0
    next_nagore=9
    a=gameplay()
    print("KRAJ CELE RUNDE")
