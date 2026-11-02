"""Gera llms-full.txt a partir do index.html do portfólio (texto em português)."""
import re, sys
from bs4 import BeautifulSoup

site = sys.argv[1]
html = open(f"{site}/index.html", encoding="utf-8").read()
soup = BeautifulSoup(html, "html.parser")
URL = "https://dyegoseabra.com.br/"

def pt(el):
    """Texto do elemento sem as partes em inglês."""
    if el is None:
        return ""
    el = BeautifulSoup(str(el), "html.parser")
    for e in el.select(".en"):
        e.decompose()
    return re.sub(r"\s+", " ", el.get_text(" ")).replace(" .", ".").replace(" ,", ",").strip()

out = []
summary = open(f"{site}/llms.txt", encoding="utf-8").read().split("\n## ")[0]
summary = summary.replace("Este arquivo resume o portfólio para assistentes de IA. A versão completa, com o detalhe de cada projeto, está em [llms-full.txt](https://dyegoseabra.com.br/llms-full.txt).", "Versão completa do portfólio para assistentes de IA, gerada a partir do texto do site. O resumo está em [llms.txt](https://dyegoseabra.com.br/llms.txt).")
out.append(summary.strip())

hero = soup.select_one("#inicio")
out.append("## Apresentação\n\n" + pt(hero.select_one("p.lead.pt")))

sobre = soup.select_one("#sobre")
out.append("## Sobre\n\n" + "\n\n".join(pt(p) for p in sobre.select(".about p.pt")))
items = []
for li in sobre.select(".timeline li"):
    when = pt(li.select_one(".when")); cargo = pt(li.select_one("b")); d = pt(li.select_one(".d.pt"))
    items.append(f"- **{when}: {cargo}.** {d}")
out.append("### Trajetória\n\n" + "\n".join(items))
sk = []
for div in sobre.select(".skills > div"):
    sk.append(f"- **{pt(div.select_one('h4'))}:** " + ", ".join(pt(li) for li in div.select("li")))
out.append("### Competências\n\n" + "\n".join(sk))

out.append("## Projetos\n\nCada projeto tem um painel de detalhes no site, aberto pelo endereço indicado. As telas usam dados fictícios.")
for tpl in soup.select("template[id^=p-]"):
    pid = tpl["id"][2:]
    t = BeautifulSoup(tpl.decode_contents(), "html.parser")
    title = pt(t.select_one(".m-title")).rstrip(".")
    block = [f"### {title}", f"Endereço: {URL}#{pid}", f"*{pt(t.select_one('.m-kicker'))} · {pt(t.select_one('.m-sub'))}*"]
    body = t.select_one(".m-body")
    for el in body.find_all(["h4", "p", "ul", "a"], recursive=False):
        if el.name == "h4":
            if pt(el).lower() == "stack":
                continue
            block.append(f"**{pt(el)}**")
        elif el.name == "p":
            block.append(pt(el))
        elif el.name == "ul":
            block.append("\n".join("- " + pt(li) for li in el.select("li")))
        elif el.name == "a":
            block.append(f"Código: {el['href']}")
    tags = [pt(x) for x in body.select(".tag")]
    if tags:
        block.append("Stack: " + ", ".join(tags))
    caps = [b.get("data-pt") for b in t.select(".m-thumb")] or [pt(t.select_one("figcaption"))]
    block.append("Telas:\n" + "\n".join("- " + c for c in caps if c))
    note = t.select_one(".m-note")
    if note:
        block.append(pt(note))
    out.append("\n\n".join(block))

out.append("## Contato\n\n" + open(f"{site}/llms.txt", encoding="utf-8").read().split("## Currículo e contato\n")[1].split("\n## ")[0].strip())
open(f"{site}/llms-full.txt", "w", encoding="utf-8").write("\n\n".join(out) + "\n")
print(len("\n\n".join(out)))
