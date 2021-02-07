import re
import requests
import orodja

STEVILO_STRANI = 21

vzorec_oglasa = re.compile(
    r"<span>(?P<ime_avtomobila>\w{3}.*?)</span>\n\s*</div>(.*\n\s*)*?"
    r"<td class=\"w-75 pl-3\">(?P<leto_prve_registracije>.*?)</td>(.*\n\s*)*?"
    r"<td class=\Dd-none d-md-block pl-3\"\>\S+\<\/td\>\D*?<td class=\"pl-3\">(?P<prevozeni_kilometri>\d+\skm)</td>(.*\n\s*)*?"
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
        sez = karakteristike_motorja.split()[:2]
        return sez[0] + " " + sez[1]
    else:
        return "velikost motorja ni znana"


def izloci_moc_motorja(karakteristike_motorja):
    if "kW" in karakteristike_motorja or "KM" in karakteristike_motorja:
        if "," in karakteristike_motorja:
            moc = karakteristike_motorja[
                karakteristike_motorja.index(",") + 1 :
            ].lstrip()
        else:
            moc = karakteristike_motorja
        return moc
    else:
        return "moc motorja ni znana"


def popravi_zapis_cene(cena):
    stevke = [znak for znak in cena if znak.isdigit()]
    string = "".join(stevke)
    return int(string)


def izloci_podatke_oglasa(blok):
    oglas = blok
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


def oglasi_na_strani(stran):
    url = (
        "https://www.avto.net/Ads/results.asp?znamka=&model=&modelID=&tip=&znamka2="
        "&model2=&tip2=&znamka3=&model3=&tip3=&cenaMin=0&cenaMax=999999&letnikMin=0"
        "&letnikMax=2090&bencin=0&starost2=999&oblika=&ccmMin=0&ccmMax=99999&mocMin"
        "=&mocMax=&kmMin=5000&kmMax=9999999&kwMin=0&kwMax=999&motortakt=&motorvalji"
        "=&lokacija=0&sirina=&dolzina=&dolzinaMIN=&dolzinaMAX=&nosilnostMIN=&nosiln"
        "ostMAX=&lezisc=&presek=&premer=&col=&vijakov=&EToznaka=&vozilo=&airbag=&bar"
        "va=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ"
        "5=1000000000&EQ6=1000000000&EQ7=1000100020&EQ8=1010000001&EQ9=100000000&KAT"
        "=1010000000&PIA=&PIAzero=&PSLO=&akcija=&paketgarancije=0&broker=&prikazkat"
        f"egorije=&kategorija=&ONLvid=&ONLnak=&zaloga=10&arhiv=&presort=&tipsort=&stran={stran}"
    )
    ime_datoteke = f"rabljeni-avtomobili-stran-{stran}.html"
    orodja.shrani_spletno_stran(url, ime_datoteke)


def zapisi_oglase():
    oglasi = []
    for stran in range(1, STEVILO_STRANI + 1):
        # shrani spletne strani
        oglasi_na_strani(stran)

        ime_datoteke = f"rabljeni-avtomobili-stran-{stran}.html"
        vsebina = orodja.vsebina_datoteke(ime_datoteke)
        for oglas in vzorec_oglasa.finditer(vsebina):
            urejeni_podatki = izloci_podatke_oglasa(oglas.groupdict())
            oglasi.append(urejeni_podatki)

        print(f"končana je stran {stran}")

    oglasi.sort(key=lambda oglas: oglas["ime_avtomobila"])
    return oglasi


urejeni_oglasi = zapisi_oglase()
orodja.zapisi_json(urejeni_oglasi, "obdelani-podatki/oglasi.json")
orodja.zapisi_csv(
    urejeni_oglasi,
    [
        "ime_avtomobila",
        "znamka",
        "leto_prve_registracije",
        "prevozeni_kilometri",
        "vrsta_motorja",
        "vrsta_menjalnika",
        "velikost_motorja",
        "moc_motorja",
        "cena",
    ],
    "obdelani-podatki/oglasi.csv",
)
