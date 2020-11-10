# Rabljeni avtomobili

Analiziral bom 3000 oglasov avtomobilov na spletni strani [avto.net](https://www.avto.net/Ads/results.asp?znamka=&model=&modelID=&tip=&znamka2=&model2=&tip2=&znamka3=&model3=&tip3=&cenaMin=0&cenaMax=999999&letnikMin=0&letnikMax=2090&bencin=0&starost2=999&oblika=0&ccmMin=0&ccmMax=99999&mocMin=&mocMax=&kmMin=0&kmMax=9999999&kwMin=0&kwMax=999&motortakt=0&motorvalji=0&lokacija=0&sirina=0&dolzina=&dolzinaMIN=0&dolzinaMAX=100&nosilnostMIN=0&nosilnostMAX=999999&lezisc=&presek=0&premer=0&col=0&vijakov=0&EToznaka=0&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000000000&EQ7=1110100120&EQ8=1010000001&EQ9=1000000000&KAT=1010000000&PIA=&PIAzero=&PSLO=&akcija=0&paketgarancije=&broker=0&prikazkategorije=0&kategorija=0&zaloga=10&arhiv=0&presort=3&tipsort=DESC&stran=1&subSTAR=303)


Za vsak avtomobil bom zajel:
- polno ime
- ceno
- leto (prve) registracije
- število prevoženih kilometrov
- vrsto goriva
- tip menjalnika
- velikost in moč motorja

Zajeti podatki so shranjeni csv in json zapisu v mapi "obdelani_podatki".


Hipoteze:
- Ali ima avto z dizlovim motorjem večjo moč kakor avto z bencinskim motorjem, upoštevajoč isto obdobje izdelave in isti cenovni rang?
- Ali ima študent s privarčevanimi 300€ na izbiro vsaj 100 zmerno obrabljenih avtomobilov (< 150 000 prevoženih km in mlajših kot 10 let)?
- Katera znamka avtomobilov starih največ 5 let ima najboljše razmerje med ceno in prevoženimi kilometri?
- Ali lahko na podlagi preostalih podatkov v oglasu napovemo ceno avtomobila?