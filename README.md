# ItaliaFragile — Atlante del dissesto idrogeologico

Sito statico di data journalism sul rischio frane e alluvioni in Italia, comune per comune.

## Dati
- **ISPRA IdroGEO (PIR)** — Indicatori di rischio della Mosaicatura nazionale ISPRA: aree a pericolosità da frana (PAI) e idraulica, popolazione/famiglie/edifici/imprese/beni culturali esposti. API: `https://idrogeo.isprambiente.it/api/pir/`
- **CNR-IRPI Polaris** — Rapporti periodici sulle vittime di frane e inondazioni in Italia.
- **Confini amministrativi** — ISTAT via openpolis/geojson-italy.

## Struttura
- `index.html` — single page (mappa Leaflet, sidebar, classifiche, fonti)
- `data.js` — indicatori nazionali/regionali/provinciali/comunali + confini regioni e province
- `geo_comuni.json` — confini dei 7.899 comuni (semplificati), caricati on demand dal livello "Comuni"
- `scripts/` — pipeline dati: `prepare_geo.sh` (confini via mapshaper) e `build_data.py` (indicatori IdroGEO)

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
