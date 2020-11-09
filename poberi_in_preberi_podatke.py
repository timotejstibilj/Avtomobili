import re
import requests
import orodja

STEVILO_STRANI = 1
INDEKS_OBLIKE = 11

vzorec_bloka = re.compile(
    r"<span>\w{3}.*?</span>\n\s*</div>(.*\n\s*)*?"
    r"<div class=\"GO-Results(-Top)?-Price-TXT-Regular\">\d.*?</div>"
)

vzorec_oglasa = re.compile(
    r"<span>(?P<ime_avtomobila>\w{3}.*?)</span>\n\s*</div>(.*\n\s*)*?"
    r"<td class=\"w-75 pl-3\">(?P<leto_prve_registracije>.*?)</td>(.*\n\s*)*?"
    r"<td class=\"pl-3\">(?P<prevozeni_kilometri>\d+\skm)</td>(.*\n\s*)*?"
    r"<td class=\"pl-3\">(?P<vrsta_motorja>\D*)</td>(.*\n\s*)*?"
    r"<td class=\"pl-3 text-truncate\">(?P<vrsta_menjalnika>.*menjalnik)</td>(.*\n\s*)*?"
    r"<td class=\"pl-3 text-truncate\">\n\s*(?P<karakteristike_motorja>\d*.*\D)\n\s*</td>(.*\n\s*)*?"
    r"<div class=\"GO-Results(-Top)?-Price-TXT-Regular\">(?P<cena>\d.*?)</div>"
)


def doloci_vrsto_menjalnika(menjalnik):
    if menjalnik[0] == "a":
        return "avtomatski menjalnik"
    else:
        return "ročni menjalnik"


def izloci_velikost_motorja(karakteristike_motorja):
    if "ccm" in karakteristike_motorja:
        return karakteristike_motorja[: karakteristike_motorja.index(",")]


def izloci_moc_motorja(karakteristike_motorja):
    if "kW" in karakteristike_motorja or "KM" in karakteristike_motorja:
        moc = karakteristike_motorja[karakteristike_motorja.index(",") + 1 :].lstrip()
        return moc


def popravi_zapis_cene(cena):
    stevke = [znak for znak in cena if znak.isdigit()]
    string = "".join(stevke)
    return int(string)


def izloci_podatke_oglasa(blok):
    oglas = vzorec_oglasa.search(blok).groupdict()
    # ime avtomobila, vrsto motorja pustimo kot je
    oglas["znamka"] = oglas["ime_avtomobila"].split()[0]
    oglas["vrsta_menjalnika"] = doloci_vrsto_menjalnika(oglas["vrsta_menjalnika"])

    # locimo moc in velikost motorja
    moc = izloci_moc_motorja(oglas["karakteristike_motorja"])
    oglas["moc_motorja"] = moc
    velikost = izloci_velikost_motorja(oglas["karakteristike_motorja"])
    oglas["velikost_motorja"] = velikost
    del oglas["karakteristike_motorja"]

    oglas["cena"] = popravi_zapis_cene(oglas["cena"])

    return oglas


def oglasi_na_strani(oblika, stran):
    url = (
        "https://www.avto.net/Ads/results.asp?znamka=&model=&modelID=&tip=&znamka2=&model2=&tip2=&znamka3=&model3=&tip3=&"
        f"cenaMin=0&cenaMax=999999&letnikMin=0&letnikMax=2090&bencin=0&starost2=999&oblika={oblika}&ccmMin=0&ccmMax=99999&"
        "mocMin=&mocMax=&kmMin=0&kmMax=9999999&kwMin=0&kwMax=999&motortakt=0&motorvalji=0&lokacija=0&sirina=0&dolzina=&"
        "dolzinaMIN=0&dolzinaMAX=100&nosilnostMIN=0&nosilnostMAX=999999&lezisc=&presek=0&premer=0&col=0&vijakov=0&EToznaka=0&"
        "vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6="
        "1000000000&EQ7=1000100020&EQ8=1010000001&EQ9=1000000000&KAT=1010000000&PIA=&PIAzero=&PSLO=&akcija=0&paketgarancije=&"
        f"broker=0&prikazkategorije=0&kategorija=0&zaloga=10&arhiv=0&presort=3&tipsort=DESC&stran={stran}"
    )
    ime_datoteke = f"rabljeni-avtomobili-oblika-{oblika}-stran-{stran}.html"
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka.finditer(vsebina):
        yield izloci_podatke_oglasa(blok.group(0))


def zapisi_oglase():
    oglasi = []
    for stran in range(1, STEVILO_STRANI + 1):
        for oblika in range(INDEKS_OBLIKE, INDEKS_OBLIKE + 2):
            for oglas in oglasi_na_strani(oblika, stran):
                oglasi.append(oglas)
    oglasi.sort(key=lambda oglas: oglas["ime_avtomobila"])
    return oglasi


oglasi = zapisi_oglase()
# orodja.zapisi_json(oglasi, "obdelani-podatki/oglasi.json")
# orodja.zapisi_csv(
#    oglasi,
#    [
#        "znamka"
#        "ime_avtomobila"
#        "leto_prve_registracije"
#        "prevozeni_kilometri"
#        "vrsta_motorja"
#        "vrsta_menjalnika"
#        "velikost_motorja"
#        "moc_motorja"
#        "cena"
#    ],
#    "obdelani-podatki/oglasi.csv",
# )
