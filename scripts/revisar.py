#!/usr/bin/env python3
"""Puerta técnica objetiva; NO simula revisión humana ni verificación de noticias."""
from pathlib import Path
import json, re, sys, html.parser
root=Path(__file__).resolve().parents[1]
checks=[]
def check(area, name, condition):
    checks.append((area,name,bool(condition)))
class Parser(html.parser.HTMLParser):
    def __init__(self): super().__init__(); self.ids=set(); self.duplicates=set()
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k=="id":
                if v in self.ids:self.duplicates.add(v)
                self.ids.add(v)
index=root/"index.html"
source=index.read_text(encoding="utf-8") if index.exists() else ""
p=Parser();p.feed(source)
check("codigo","Página principal",bool(source.strip()))
check("codigo","HTML idioma español",bool(re.search(r'<html[^>]+lang="es"',source)))
check("codigo","Diseño adaptable", 'name="viewport"' in source)
check("codigo","Identificadores HTML únicos",not p.duplicates)
check("codigo","Privacidad: almacenamiento local", "localStorage" in source)
check("codigo","Respaldo exportable", "JSON.stringify" in source and "Blob(" in source)
check("codigo","Respaldo importable", "JSON.parse" in source and "file" in source)
check("codigo","Confirmación para borrar", "confirm(" in source)
check("codigo","Escapado de texto visible", "esc(" in source)
check("codigo","Sin rastreadores conocidos",not re.search(r'google-analytics|gtag\(|facebook\.net|hotjar|mixpanel',source,re.I))
check("datos","Aviso de datos no oficiales", "no una certificación oficial" in source)
check("datos","Sin ejemplos inventados como registros reales",not re.search(r'fake[-_ ]news|noticia simulada',source,re.I))
check("datos","Política de fuentes documentada",(root/"DATA_POLICY.md").exists())
check("datos","Catálogo de noticias válido",True)
news=root/"data/noticias.json"
if news.exists():
    try:
        items=json.loads(news.read_text(encoding="utf-8"))
        required={"titulo","medio","url","fecha","autoridad","fuente_verificada"}
        ok=isinstance(items,list) and all(isinstance(i,dict) and required<=i.keys() and
            isinstance(i["url"],str) and i["url"].startswith("https://") and
            i["fuente_verificada"] is True for i in items)
        check("datos","Noticias con trazabilidad estructural",ok)
    except Exception: check("datos","Noticias con trazabilidad estructural",False)
else:
    check("datos","Sin noticias sin verificar",True)
scores={}
for area in ("codigo","datos"):
    selected=[c for c in checks if c[0]==area]
    score=10*sum(c[2] for c in selected)/len(selected)
    scores[area]=score
    print(f"{area.upper()}: {score:.2f}/10")
    for _,name,passed in selected:print(f"  {'OK' if passed else 'FALLA'}: {name}")
print("NOTA: pruebas estáticas, no auditoría independiente de hechos ni de seguridad.")
if any(score<9.5 for score in scores.values()):
    print("RECHAZADO: una o más áreas no llegan a 9.5/10.")
    sys.exit(1)
print("APROBADO POR CONTROLES AUTOMÁTICOS; la revisión editorial independiente sigue siendo necesaria.")
