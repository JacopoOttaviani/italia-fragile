#!/bin/bash
# Prepara le geometrie per ItaliaFragile a partire da openpolis/geojson-italy.
# Richiede: curl, npx (mapshaper). Uso: ./scripts/prepare_geo.sh <workdir>
set -euo pipefail
W="${1:-/tmp/italiafragile-geo}"
mkdir -p "$W" && cd "$W"
BASE="https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson"

curl -sSL "$BASE/limits_IT_regions.geojson"        -o regions.geojson
curl -sSL "$BASE/limits_IT_provinces.geojson"      -o provinces.geojson
curl -sSL "$BASE/limits_IT_municipalities.geojson" -o municipalities.geojson

# Regioni e province: incluse in data.js dal build_data.py (leggere e semplificate)
npx -y mapshaper regions.geojson   -simplify keep-shapes 8% -o precision=0.0001 regions_s.geojson
npx -y mapshaper provinces.geojson -simplify keep-shapes 8% -o precision=0.0001 provinces_s.geojson

# Comuni: file separato caricato on demand dalla mappa (geo_comuni.json)
npx -y mapshaper municipalities.geojson -simplify keep-shapes 4% \
  -filter-fields com_istat_code_num -rename-fields cod=com_istat_code_num \
  -o precision=0.0001 comuni_s.geojson

echo "Fatto. Copia comuni_s.geojson nel progetto come geo_comuni.json,"
echo "e passa la cartella $W a scripts/build_data.py per regioni/province."
