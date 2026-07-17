#!/usr/bin/env python3
"""Costruisce data.js per ItaliaFragile a partire dai dati IdroGEO (ISPRA) e
dai confini openpolis/geojson-italy gia' scaricati nella cartella scratchpad.

Uso: python3 scripts/build_data.py <scratchpad_dir>
"""
import json
import sys
from pathlib import Path

SP = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT = Path(__file__).resolve().parent.parent / "data.js"

r1 = lambda v: round(v or 0, 1)
i0 = lambda v: int(round(v or 0))


def indicators(rec):
    """Estrae il set compatto di indicatori da un record PIR."""
    return {
        "pop": i0(rec.get("pop_res021")),
        "ar": r1(rec.get("ar_kmq")),
        # Frane: pericolosita' elevata P3 + molto elevata P4 (PAI)
        "fp": r1(rec.get("ar_frp3p4p") or rec.get("arfrp3p4_p")),
        "fa": r1(rec.get("ar_fr_p3p4")),
        "fpop": i0(rec.get("popfr_p3p4")),
        "fpop_p": r1(rec.get("popfrp3p4p")),
        "fed": i0(rec.get("ed_fr_p3p4")),
        # Alluvioni: scenario medio P2 (tempo di ritorno 100-200 anni)
        "ip": r1(rec.get("aridp2_p")),
        "ia": r1(rec.get("ar_id_p2")),
        "ipop": i0(rec.get("pop_idr_p2")),
        "ipop_p": r1(rec.get("popidp2_p")),
        "ied": i0(rec.get("ed_idr_p2")),
        # Alluvioni scenario elevato P3 (frequente), solo popolazione
        "i3pop": i0(rec.get("pop_idr_p3")),
    }


def main():
    italia = json.load(open(SP / "italia.json"))
    reg_exp = json.load(open(SP / "regioni_export.json"))
    prov_exp = json.load(open(SP / "province_export.json"))
    com_exp = json.load(open(SP / "comuni_export.json"))
    com_reg = json.load(open(SP / "comuni.json"))  # anagrafica con extent + sigla prov
    geo_reg = json.load(open(SP / "regions_s.geojson"))
    geo_prov = json.load(open(SP / "provinces_s.geojson"))

    # --- nazionale ---------------------------------------------------------
    ita = indicators(italia)

    # --- regioni / province ------------------------------------------------
    ind_reg = {}
    for r in reg_exp:
        d = indicators(r)
        d["nome"] = r["regione"]
        ind_reg[str(r["cod_reg"])] = d

    ind_prov = {}
    for p in prov_exp:
        d = indicators(p)
        d["nome"] = p["provincia"]
        d["reg"] = p["cod_reg"]
        ind_prov[str(p["cod_prov"])] = d

    # --- comuni: array compatto per ricerca e classifiche -------------------
    # [pro_com, nome, siglaProv, cod_prov, extent[w,s,e,n], pop, fp, fpop, fpop_p, ip, ipop, ipop_p, fa, ia, fed, ied, i3pop, ar]
    reg_by_procom = {}
    for c in com_reg:
        sig = next((b["name"] for b in c.get("breadcrumb", []) if b.get("t") == "p"), "")
        e = c.get("extent") or [[0, 0], [0, 0]]
        reg_by_procom[c["pro_com"]] = (sig, [round(e[0][0], 3), round(e[0][1], 3), round(e[1][0], 3), round(e[1][1], 3)])

    comuni = []
    n_fr = n_id = n_any = 0
    for c in com_exp:
        d = indicators(c)
        sig, ext = reg_by_procom.get(c["pro_com"], ("", [0, 0, 0, 0]))
        if d["fp"] > 0:
            n_fr += 1
        if d["ip"] > 0:
            n_id += 1
        if d["fp"] > 0 or d["ip"] > 0:
            n_any += 1
        comuni.append([
            c["pro_com"], c["comune"], sig, c["cod_prov"], ext,
            d["pop"], d["fp"], d["fpop"], d["fpop_p"],
            d["ip"], d["ipop"], d["ipop_p"],
            d["fa"], d["ia"], d["fed"], d["ied"], d["i3pop"], d["ar"],
        ])

    stats = {
        "n_comuni": len(com_exp),
        "n_comuni_frane": n_fr,
        "n_comuni_alluvioni": n_id,
        "n_comuni_rischio": n_any,
    }

    # --- geojson: tieni solo le property necessarie -------------------------
    for f in geo_reg["features"]:
        p = f["properties"]
        f["properties"] = {"cod": p["reg_istat_code_num"], "nome": p["reg_name"]}
    for f in geo_prov["features"]:
        p = f["properties"]
        f["properties"] = {"cod": p["prov_istat_code_num"], "nome": p["prov_name"],
                           "sigla": p["prov_acr"], "reg": p["reg_istat_code_num"]}

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("// Dati: ISPRA IdroGEO (Mosaicature nazionali di pericolosita' 2020-2021,\n")
        fh.write("// indicatori di rischio su censimento ISTAT 2021), licenza CC-BY 4.0.\n")
        fh.write("// Confini: ISTAT via openpolis/geojson-italy. Build automatica, non modificare a mano.\n")
        j = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
        fh.write("const ITALIA=" + j(ita) + ";\n")
        fh.write("const STATS=" + j(stats) + ";\n")
        fh.write("const IND_REG=" + j(ind_reg) + ";\n")
        fh.write("const IND_PROV=" + j(ind_prov) + ";\n")
        fh.write("const COMUNI=" + j(comuni) + ";\n")
        fh.write("const GEO_REG=" + j(geo_reg) + ";\n")
        fh.write("const GEO_PROV=" + j(geo_prov) + ";\n")

    print(f"data.js scritto: {OUT.stat().st_size/1e6:.2f} MB")
    print("stats:", stats)
    print("italia:", ita)


if __name__ == "__main__":
    main()
