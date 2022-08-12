## -------------------- Henkilötunnus Generaattori -------------------- ##
#Kirjoittanut: Aarni Junkkala
#Generoi keksittyjä henkilötunnuksia

import random

def Generoi():
    vuosi = random.randint(1800,2099)
    kuukausi = random.randint(1,12)
    
    #päätellään karkaus vuosi
    onkoKarkausVuosi = False
    if vuosi % 100 == 0 and vuosi % 400 == 0:
        onkoKarkausVuosi = True
    elif vuosi % 100 != 0 and vuosi % 400 != 0 and vuosi % 4 == 0:
        onkoKarkausVuosi = True
    
    #Kuukausien päivien määrien asettelu
    KuukausienPaivienMaarat = [31,28,31,30,31,30,31,31,30,31,30,31]
    if onkoKarkausVuosi == True:
        KuukausienPaivienMaarat[1] += 1
    
    #Päätellään vuosisatatunnus
    vuosisataTunnus = ""
    if vuosi >= 1800 and vuosi < 1900:
        vuosisataTunnus = "+"
    elif vuosi >= 1900 and vuosi < 2000:
        vuosisataTunnus = "-"
    elif vuosi >= 2000 and vuosi < 2100:
        vuosisataTunnus = "A"
    else:
        return "FAILED"
    
    #Keksii päivän
    pv = str(random.randint(1,KuukausienPaivienMaarat[kuukausi - 1]))
    #Lisää päivään ja kuukauteen aloitus nollan, jos ne eivät ole kaksilukuisia. Esim: 1 -> 01, 25 -> 25
    if len(pv) <= 1:
        pv = "0" + pv
    kuukausi = str(kuukausi)
    if len(kuukausi) <= 1:
        kuukausi = "0" + kuukausi
    #Karsii vuodesta viimeiset kaksi symbolia
    vuosi = str(vuosi)
    vuosi = vuosi[2:4]
    paivamaaraSymboli = pv + kuukausi + vuosi 
    
    #Yksilötunnus tulee olla väliltä 002 ja 899.
    yksilotunnus = str(random.randint(2,899))
    #Täyttää nollat
    while len(yksilotunnus) < 3:
        yksilotunnus = "0" + yksilotunnus
        
    #Päättelee tarkistusmerkin
    TarkistusMerkkiSymbolit = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","H","J","K","L","M","N","P","R","S","T","U","V","W","X","Y"]
    TarkistusMerkki = TarkistusMerkkiSymbolit[int(paivamaaraSymboli + yksilotunnus) % 31]
    
    return(paivamaaraSymboli + vuosisataTunnus + yksilotunnus + TarkistusMerkki)

print(Generoi())