import re

with open("48_oglasov.html", encoding="utf-8") as file:
    content = file.read()

pattern = re.compile(
    r"<span>(?P<ime_avtomobila>.*)</span>\n\s{4}</div>.*?"
    r"<td class=\"pl-3\">(?P<prevozeni_kilometri>\d+\skm)</td>.*?"
    r"<td class=\"w-75 pl-3\">(?P<leto_prve_registracije>.*)</td>.*?"
    r"<td class=\"pl-3\">(?P<vrsta_motorja>(bencinski|diesel)\smotor)</td>.*?"
    r"<td class=\"pl-3 text-truncate\">(?P<vrsta_menjalnika>.*menjalnik)</td>.*?"
    r'<td class="pl-3 text-truncate">\n\s*(?P<karakteristike_motorja>\d*.*)\n\s*</td>.*?'
    r'<div class="GO-Results-Price-TXT-Regular">(?P<cena>\d+.*)</div>',
    flags=re.DOTALL,
)


count = 0
for zadetek in re.finditer(pattern, content):
    print(zadetek.groupdict())
    count += 1

print(count)
