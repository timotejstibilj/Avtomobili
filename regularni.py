import re


# pattern = re.compile(
#    r"<span>(?P<ime_avtomobila>\w{3}.*?)</span>\n\s*</div>.*?"
#    r"<td class=\"pl-3\">(?P<prevozeni_kilometri>\d+\skm)</td>.*?"
#    r"<td class=\"w-75 pl-3\">(?P<leto_prve_registracije>.*)</td>.*?"
#    r"<td class=\"pl-3\">(?P<vrsta_motorja>\D*)</td>.*?"
#    r"<td class=\"pl-3 text-truncate\">(?P<vrsta_menjalnika>.*menjalnik)</td>.*?"
#    r'<td class=\"pl-3 text-truncate\">\n\s*(?P<karakteristike_motorja>\d*.*\D)\n\s*</td>.*?'
#    r'<div class="GO-Results-Price-TXT-Regular">(?P<cena>\d+.*)</div>',
#    flags=re.DOTALL,
# )

pattern = r'<div class="GO-Results-Price-TXT-Regular">(?P<cena>\d+.*)</div>'


with open("rabljeni-avtomobili-oblika-11-stran-1.html", encoding="utf-8") as file:
    content = file.read()

count = 0
for zadetek in re.finditer(pattern, content):
    print(zadetek.groupdict())
    count += 1


print(count)
