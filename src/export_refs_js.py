"""Export the verified references (lv_references.bib) as a JSON object for the model-builder page,
and inject it into model_builder/lv_model_builder.src.html -> lv_model_builder.html."""
import json
import re
from pathlib import Path

FIG = Path(__file__).resolve().parent.parent
BIB = (FIG / "lv_references.bib").read_text(encoding="utf-8")
SRC = FIG.parent / "model_builder" / "lv_model_builder.src.html"
OUT = FIG.parent / "model_builder" / "lv_model_builder.html"

ACC = {r"{\c{c}}": "ç", r"\c{c}": "ç", r"{\'e}": "é", r"\'e": "é", r'{\"o}': "ö", r'\"o': "ö", r"\v{r}": "ř", "--": "–", r"\&": "&", "~": " "}


def field(body, name):
    m = re.search(rf"(?<![a-z]){name}\s*=\s*\{{((?:[^{{}}]|\{{(?:[^{{}}]|\{{[^{{}}]*\}})*\}})*)\}}", body, re.I)
    if not m:
        return ""
    s = m.group(1)
    for a, b in ACC.items():
        s = s.replace(a, b)
    return re.sub(r"[{}]", "", s).strip()


def short_authors(a):
    names = [x.strip() for x in a.split(" and ") if x.strip()]
    fam = [n.split(",")[0].strip() for n in names]
    if not fam:
        return "Anon."
    if len(fam) == 1:
        return fam[0]
    if len(fam) == 2:
        return f"{fam[0]} & {fam[1]}"
    return f"{fam[0]} et al."


def full_authors(a):
    if not a.strip():
        return "Anon."
    names = []
    for n in [x.strip() for x in a.split(" and ") if x.strip()]:
        if "," in n:
            fam, giv = [p.strip() for p in n.split(",", 1)]
            ini = " ".join(w[0] + "." for w in re.split(r"[\s.]+", giv) if w and w[0].isalpha())
            names.append(f"{fam}, {ini}".strip(", "))
        else:
            names.append(n)
    return ", ".join(names[:-1]) + (", & " if len(names) > 2 else " & ") + names[-1] if len(names) > 1 else names[0]


refs = {}
for m in re.finditer(r"(@(\w+)\{([^,]+),.*?)(?=\n@|\Z)", BIB, re.S):
    raw, typ, key = m.group(1).strip(), m.group(2).lower(), m.group(3)
    a = field(raw, "author") or field(raw, "editor")
    if not a:
        print("no author parsed:", key)
    year, title = field(raw, "year"), field(raw, "title")
    venue = field(raw, "journal") or field(raw, "booktitle")
    vol, num, pages = field(raw, "volume"), field(raw, "number"), field(raw, "pages")
    pub = field(raw, "publisher")
    if venue:
        tail = f"{venue}" + (f", {vol}" if vol else "") + (f"({num})" if num and vol else "") + (f", {pages}" if pages else "")
    else:
        tail = pub
    refs[key] = {
        "short": f"{short_authors(a)} ({year})",
        "cite": f"{full_authors(a)} ({year}). {title}. {tail}.",
        "doi": field(raw, "doi"),
        "bib": raw if raw.endswith("}") else raw + "\n}",
    }

src = SRC.read_text(encoding="utf-8")
OUT.write_text(src.replace("/*__REFS_JSON__*/{}", json.dumps(refs, ensure_ascii=False)), encoding="utf-8")
print("refs:", len(refs), "->", OUT.name)
