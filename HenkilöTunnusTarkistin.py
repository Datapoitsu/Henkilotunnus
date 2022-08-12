## -------------------- Henkilötunnustarkistaja ------------------------- ##
#Kirjoittanut: Aarni Junkkala

#Suomalaisen henkilötunnuksen rakenne:
# ppkkvvynnnt
# p-> päivä
# k-> kuukausi
# v-> vuosi
# y-> vuosisatakerroin
# n-> identifikaationumero
# t-> tunnisteluku

# Oleellisin osa on tunnisteluku, joka perustuu syntymäpäivä ja identifikaationumero (ppkkvvnnn) jakojäännökseen numerolla 31
# Koodi myös tarkistaa, että onko päivämäärä mahdollinen, karkausvuosi yms. ja tarkistaa identifikaatio luvun mahdollisuuden myös.

def OnkoTunnusOikea(Tunnus):    
    #Tunnus on aina 11 merkkiä pitkä
    if len(Tunnus) != 11:
        return "Tunnus on väärän pituinen"
    
    #Muutetaan tunnus isoihin kirjaimiin, niinkuin sen tulisikin olla
    Tunnus = Tunnus.upper()
    
    # ----- Symboliikan oikein kirjoitus ----- #
    numerot = ["0","1","2","3","4","5","6","7","8","9"]
    vuosiSataTunnukset = ["+","-","A"]
    TarkistusMerkkiSymbolit = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","H","J","K","L","M","N","P","R","S","T","U","V","W","X","Y"]
    for i in range(6):
        if Tunnus[i] not in numerot: 
            return "Päivämäärä on kirjoitettu väärin"
    
    if Tunnus[6] not in vuosiSataTunnukset:
        return "Vuosisatatunnus on kirjoitettu väärin"
    
    for i in range(7,10):
        if Tunnus[i] not in numerot: 
            return "Yksilönumero on kirjoitettu väärin"
    
    if Tunnus[10] not in TarkistusMerkkiSymbolit:
        return "Tarkistusmerkki on kirjoitettu väärin"
    
    # ----- Merkien oikeanlaisuus ----- #
    #päätellaan vuosisata, vuotta varten
    vuosiSataTunnus = Tunnus[6]
    vuosiSata = 0
    if vuosiSataTunnus == "+":
        vuosiSata = 1800
    elif vuosiSataTunnus == "-":
        vuosiSata = 1900
    elif vuosiSataTunnus == "A":
        vuosiSata = 2000
    vuosi = vuosiSata + int(Tunnus[4:6])    #vuosi
    
    if vuosi < 1800 or vuosi >= 2100:
        return "Vuosi on liian iso tai pieni"

    #päätellään karkaus vuosi
    onkoKarkausVuosi = False
    if vuosi % 100 == 0 and vuosi % 400 == 0:
        onkoKarkausVuosi = True
    elif vuosi % 100 != 0 and vuosi % 400 != 0 and vuosi % 4 == 0:
        onkoKarkausVuosi = True
    
    #Kuukauden päättely
    kuukausi = int(Tunnus[2:4])   #kuukausi
    if kuukausi > 12 or kuukausi <= 0:
        return "Kuukausi on liian iso"
    
    #Kuukausien päivien määrien asettelu
    KuukausienPaivienMaarat = [31,28,31,30,31,30,31,31,30,31,30,31]
    if onkoKarkausVuosi == True:
        KuukausienPaivienMaarat[1] += 1
    #Päivänpäättely
    paiva = int(Tunnus[0:2])      #päivä
    if paiva <= 0:
        return "Päivä on liian pieni"
    if paiva > KuukausienPaivienMaarat[kuukausi - 1]:
        return "Päivä on liian iso"
    
    # ----- Tarkistusmerkin tarkistus ----- #
    Tarkistusmerkki = Tunnus[10]
    KorrektiTarkistusMerkki = TarkistusMerkkiSymbolit[int(Tunnus[0:6] + Tunnus[7:10]) % 31]
    if Tarkistusmerkki != KorrektiTarkistusMerkki:
        return "Tarkistus Merkki on väärin"
    
    return True

if __name__ == '__main__':
    print(OnkoTunnusOikea(input("Syötä henkilötunnus, jonka todellisuuden haluat tarkistaa: ")))