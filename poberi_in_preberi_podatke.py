import re
import requests
import orodja

STEVILO_STRANI = 21
INDEKS_OBLIKE = 11


pattern = re.compile(
    r"<span>(?P<ime_avtomobila>\w{3}.*?)</span>\n\s*</div>(.*\n\s*)*?<td class=\"w-75 pl-3\">(?P<leto_prve_registracije>.*?)</td>(.*\n\s*)*?<td class=\"pl-3\">(?P<prevozeni_kilometri>\d+\skm)</td>(.*\n\s*)*?<td class=\"pl-3\">(?P<vrsta_motorja>\D*)</td>(.*\n\s*)*?<td class=\"pl-3 text-truncate\">(?P<vrsta_menjalnika>.*menjalnik)</td>(.*\n\s*)*?<td class=\"pl-3 text-truncate\">\n\s*(?P<karakteristike_motorja>\d*.*\D)\n\s*</td>(.*\n\s*)*?<div class=\"GO-Results(-Top)?-Price-TXT-Regular\">\d.*?</div>"
)


for stevilo in range(INDEKS_OBLIKE, INDEKS_OBLIKE + 6):
    for stran in range(1, STEVILO_STRANI + 1):
        url = f"https://www.avto.net/Ads/results.asp?znamka=&model=&modelID=&tip=&znamka2=&model2=&tip2=&znamka3=&model3=&tip3=&cenaMin=0&cenaMax=999999&letnikMin=0&letnikMax=2090&bencin=0&starost2=999&oblika={stevilo}&ccmMin=0&ccmMax=99999&mocMin=&mocMax=&kmMin=0&kmMax=9999999&kwMin=0&kwMax=999&motortakt=0&motorvalji=0&lokacija=0&sirina=0&dolzina=&dolzinaMIN=0&dolzinaMAX=100&nosilnostMIN=0&nosilnostMAX=999999&lezisc=&presek=0&premer=0&col=0&vijakov=0&EToznaka=0&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000000000&EQ7=1000100020&EQ8=1010000001&EQ9=1000000000&KAT=1010000000&PIA=&PIAzero=&PSLO=&akcija=0&paketgarancije=&broker=0&prikazkategorije=0&kategorija=0&zaloga=10&arhiv=0&presort=3&tipsort=DESC&stran={stran}"
        datoteka = f"rabljeni-avtomobili-oblika-{stevilo}-stran-{stran}.html"
        orodja.shrani_spletno_stran(url, datoteka)

vsebina = orodja.vsebina_datoteke("rabljeni-avtomobili-oblika-16-stran-10.html")

count = 0
for zadetek in re.finditer(pattern, vsebina):
    print(zadetek.groupdict())
    count += 1


print(count)
