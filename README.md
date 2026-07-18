# ItaliaFragile — Atlante del dissesto idrogeologico

Sito statico di data journalism sul rischio frane e alluvioni in Italia, comune per comune.

## Dati
- **ISPRA IdroGEO (PIR)** — Indicatori di rischio della Mosaicatura nazionale ISPRA: aree a pericolosità da frana (PAI) e idraulica, popolazione/famiglie/edifici/imprese/beni culturali esposti. API: `https://idrogeo.isprambiente.it/api/pir/`
- **CNR-IRPI Polaris** — Rapporti periodici sulle vittime di frane e inondazioni in Italia.
- **Confini amministrativi** — ISTAT via openpolis/geojson-italy.
- **Sezione "Il conto"** — dati economici da ANCE-CRESME (*Lo stato di rischio del territorio italiano*, 2023), ISPRA ReNDiS (rapporto 2025), JRC/Commissione europea (Dottori et al., *Nature Climate Change*, 2023), Regione Emilia-Romagna e Greenpeace Italia su dati DPC.

## Struttura
- `index.html` — single page (mappa Leaflet, sidebar, classifiche, fonti)
- `en/index.html` — versione inglese (stessa struttura e stessi dati, raggiungibile su `/en/`; switch IT/EN nella barra di navigazione)
- `data.js` — indicatori nazionali/regionali/provinciali/comunali + confini regioni e province
- `geo_comuni.json` — confini dei 7.899 comuni (semplificati), caricati on demand dal livello "Comuni"
- `scripts/` — pipeline dati: `prepare_geo.sh` (confini via mapshaper) e `build_data.py` (indicatori IdroGEO)
- `robots.txt`, `sitemap.xml`, `llms.txt` — file per motori di ricerca e crawler AI

## SEO
Le pagine includono canonical, hreflang, Open Graph/Twitter card e dati strutturati JSON-LD
(WebSite, Person, Dataset, FAQPage). Gli URL assoluti usano il dominio `https://italiafragile.it`:
se il sito viene pubblicato su un dominio diverso, sostituirlo in `index.html`, `en/index.html`,
`robots.txt`, `sitemap.xml` e `llms.txt` (es. `grep -rl 'italiafragile.it' . | xargs sed -i '' 's|italiafragile.it|NUOVODOMINIO|g'`).

## Build dei dati
```bash
./scripts/prepare_geo.sh /tmp/italiafragile-geo
python3 scripts/build_data.py /tmp/italiafragile-geo
```

## Livello sub-comunale
La mappa può sovrapporre le aree reali delle mosaicature nazionali di pericolosità
(frane P3+P4, alluvioni P2) tramite il servizio WMS pubblico di IdroGEO:
`https://idrogeo.isprambiente.it/geoserver/idrogeo/wms`

## Licenza dati
ISPRA IdroGEO: CC-BY 4.0. Confini: ISTAT (CC-BY).
