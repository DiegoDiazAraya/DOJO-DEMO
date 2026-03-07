import json
import re

def convert_ts_to_json(ts_file, json_file):
    with open(ts_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar la parte JSON después del '='
    match = re.search(r'=\s*(\[.*\]);', content, re.DOTALL)
    if match:
        json_str = match.group(1)
        # Limpiar posibles trailing commas si las hay (aunque JSON.loads es estricto)
        # En este caso parece JSON válido generado por el script previo.
        data = json.loads(json_str)
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Convertido {ts_file} a {json_file}")
    else:
        print(f"No se encontró data en {ts_file}")

convert_ts_to_json('d:/DOJO DEMO/client/src/data/students.ts', 'd:/DOJO DEMO/server/data/students.json')
convert_ts_to_json('d:/DOJO DEMO/client/src/data/videos.ts', 'd:/DOJO DEMO/server/data/videos.json')
