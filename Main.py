'''
Created on 18 Nov 2017

@author: przem
'''
import fractions
import math
import sys
import numpy
zaszyfrowany_tekst = []
stale_czestosci = []
obliczone_czestosci = []
haslo = []
odszyfrowany_tekst = []


# metoda Kasinskiego
def MetodaKasinskiego():
    powtorzenia = []
    tab = []
    
    # bede sprawdzal tekst i nadawal im flagi dla powtorzen
    for i in range(len(zaszyfrowany_tekst) / 2, 2, -1):
        for j in range(len(zaszyfrowany_tekst) / 2):
            slowo = zaszyfrowany_tekst[j:j + i]
            if j + i > len(zaszyfrowany_tekst):
                break
            for k in range(len(zaszyfrowany_tekst), j, -1):
                if zaszyfrowany_tekst[k:k + i] == slowo:
                    flaga = True
                    for x in [sa[1] for sa in powtorzenia]:
                        if x == j:
                            flaga = False

                    if flaga :
                        powtorzenia.append((k - j, j))
                        
    # licze powtorzenia i zapisuje do tablicy                
    for element1 in [el[0] for el in powtorzenia]:
        for element2 in [el[0] for el in powtorzenia]:
            x = fractions.gcd(element1, element2)
            tab.append(x)
        
    mediana = numpy.median(tab)
    return int(mediana)


# metoda Friedmana
def MetodaFriedmana(szyfrogram):
    ilosc_koincydencji = [len(szyfrogram)]
    
    # ilosc koindycencji
    for i in range(1, len(szyfrogram)):
        ilosc_koincydencji.append(0)
        for j in range(len(szyfrogram)):
            if szyfrogram[j] == szyfrogram[(i + j) % len(szyfrogram)]:
                ilosc_koincydencji[i] = ilosc_koincydencji[i] + 1
                
    srednia = 0
    odchylenie = 0
    
    # liczenie sredniej koincycencji
    for j in range(len(szyfrogram)):
        srednia += ilosc_koincydencji[j]
    srednia /= len(szyfrogram)
    
    # liczenie odchylenia koincydencji
    for j in range(len(szyfrogram)):
        odchylenie += int (math.fabs(ilosc_koincydencji[j] - srednia))
    odchylenie /= len(szyfrogram)
    
    # j bedzie wynikiem koincydencji chyba, ze srednia z odchyleniem beda wieksze to wtedy nie bedzie wyniku
    for j in range(1, len(szyfrogram)):
        if ilosc_koincydencji[j] > srednia + odchylenie:
            return j
        
    return 'nie ma rozwiazania'


def ObliczanieCzestosci(iteration):
    czestosci = []
    
    for c in range(26):
        czestosci.append(0)
    t = iteration
    
    while t < len(zaszyfrowany_tekst):
        czestosci[ ord(zaszyfrowany_tekst[t]) - ord('a') ] += 1
        t += 5

    for c in range(26):
        czestosci[c] = round (czestosci[c] * 1.0 / (len(zaszyfrowany_tekst) / 5.0), 3)
    return czestosci


def ObliczanieLitery(czestosci):
    przesuniecia = []
    
    for x in (range(26)):
        roznica = 0.0
        przesuniecia.append(0.0)
        for l in range(len(czestosci)):
            roznica += abs(czestosci[ (l + x) % 26 ] - stale_czestosci[l])
        przesuniecia[x] = roznica
        
    return przesuniecia.index(min(przesuniecia))


def OdszyfrowanieTekstu():
    for i in range(len(zaszyfrowany_tekst)):
        odszyfrowany_tekst.append(chr((ord(zaszyfrowany_tekst[i]) - ord('a') - (ord(haslo[i % 5]) - ord('a'))) % 26 + ord('a')))

with open('czestosci_liter.txt', 'r') as plik_czestosci:
    for line in plik_czestosci:
        stale_czestosci.append(float(line) / 1000.0)
        
with open('szyfr.txt', 'r') as plik_szyfrogram:
    zaszyfrowany_tekst = plik_szyfrogram.read().replace('\n', '').replace(' ', '')

#drukowanie wynikow
print "Dlugosci klucza obiema metodami:\n"
kasinski = MetodaKasinskiego()
print "metoda Kasinskiego - ", kasinski
friedman = MetodaFriedmana(zaszyfrowany_tekst)
print "metoda Friedmana - ", friedman, "\n"

if kasinski == friedman:
    for it in range(kasinski):
        ob = ObliczanieCzestosci(it)
        k = chr(ord('a') + ObliczanieLitery(ob))
        haslo.append(k)
        obliczone_czestosci.append(ob)
        
    with open('obliczone_czestosci.txt', 'w') as plik_szyfrogram:
        for i in range(len(obliczone_czestosci)):
            plik_szyfrogram.write('Obliczone czestotliwosci dla i = ' + str(i))
            plik_szyfrogram.write(''.join(str(obliczone_czestosci[i])))
            plik_szyfrogram.write('\n')
            
    OdszyfrowanieTekstu()
    odszyfrowany_tekst = ''.join(odszyfrowany_tekst)
    
    with open('odszyfrowany_szyfr.txt', 'w') as plik_szyfrogram:
        plik_szyfrogram.write(odszyfrowany_tekst)
    print "Odszyfrowany zaszyfrowany_tekst:"
    print odszyfrowany_tekst, "\n"
    print "Klucz: ", ''.join(haslo)
