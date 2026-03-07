import pandas as pd
import csv
import json
import os
import re
import unicodedata

def normalize_text(text):
    if not text: return ""
    text = str(text).strip().lower()
    text = "".join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return " ".join(text.split())

def map_belt(grado):
    if not grado: return 'WHITE'
    grado = grado.lower()
    if 'gris' in grado or 'gray' in grado: return 'GRAY'
    if 'negro' in grado or 'preta' in grado: return 'BLACK'
    if 'marrón' in grado or 'marron' in grado or 'marrom' in grado: return 'BROWN'
    if 'morado' in grado or 'roxo' in grado: return 'PURPLE'
    if 'azul' in grado: return 'BLUE'
    if 'blanco' in grado or 'branca' in grado or 'banco' in grado: return 'WHITE'
    return 'WHITE'

# 1. Read Excel sheets
excel_path = r'd:\DOJO DEMO\INGRESOS 2025.xlsx'
sheets = ['INGRESOS', 'HISTORICO']
excel_records = []

for sheet in sheets:
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet)
        for _, row in df.iterrows():
            raw_name = str(row.iloc[1]).strip()
            if not raw_name or raw_name.lower() in ['nan', 'alumno', 'adultos', 'niños', 'total', 'mes', 'ingresos', 'gastos', 'unnamed', 'fecha de pago']:
                continue
            
            try:
                raw_date = str(row.iloc[2]).strip()
                payment_date = raw_date[:10] if raw_date and raw_date != 'nan' else ""
                
                raw_val = str(row.iloc[3]).replace('.', '').replace('$', '').strip()
                fee = int(float(raw_val)) if raw_val and raw_val != 'nan' else 0
                
                plan = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else ""
                
                excel_records.append({
                    "norm_name_tokens": set(normalize_text(raw_name).split()),
                    "fee": fee,
                    "plan": plan,
                    "last_pay": payment_date,
                    "orig_name": raw_name
                })
            except: pass
    except: pass

# 2. Leer CSV Principal y Mezclar
students = []
with open('d:/DOJO DEMO/dojo_unificado_completo.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        orig_name = row["Alumno"].strip()
        norm_name_tokens = set(normalize_text(orig_name).split())
        
        fee_csv = 0
        if row.get("Valor"):
            try: fee_csv = int(row["Valor"].replace(".", "").replace("$", "").strip())
            except: pass
            
        student = {
            "id": str(i + 1), "name": orig_name, "email": row["Correo"].strip(), "phone": row["Telefono"].strip(),
            "birthDate": row["FechaNacimiento"].strip() if row.get("FechaNacimiento") else None,
            "belt": map_belt(row["Grado"]), "classesAttended": 0, "classesToNextBelt": 40,
            "lastPaymentMonth": row["FechaPago"][:7] if row.get("FechaPago") else "",
            "isPaid": bool(row.get("FechaPago") and row["FechaPago"].strip()), "history": [],
            "plan": row.get("Plan", "Pendiente").strip(), "joinDate": row.get("FechaIngreso", "").strip(),
            "lastPaymentDate": row.get("FechaPago", "").strip(), "monthlyFee": fee_csv
        }
        if row.get("Tutor"): student["tutorName"] = row["Tutor"].strip()

        # --- BUSQUEDA CON SUBSET DE TOKENS ---
        best_match = None
        for ex in excel_records:
            # Si TODOS los tokens del nombre del Excel están en los tokens del CSV
            if ex["norm_name_tokens"].issubset(norm_name_tokens) or norm_name_tokens.issubset(ex["norm_name_tokens"]):
                best_match = ex
                break
        
        # Rescate si no hay match (match de al menos 2 tokens en común si el nombre es corto)
        if not best_match:
            for ex in excel_records:
                common = ex["norm_name_tokens"].intersection(norm_name_tokens)
                if len(common) >= 2:
                    best_match = ex
                    break

        if best_match:
            student["monthlyFee"] = best_match["fee"] if best_match["fee"] > 0 else student["monthlyFee"]
            student["plan"] = best_match["plan"] if best_match["plan"] else student["plan"]
            student["lastPaymentDate"] = best_match["last_pay"] if best_match["last_pay"] else student["lastPaymentDate"]
            if "2026" in student["lastPaymentDate"] or "2025-12" in student["lastPaymentDate"]:
                student["isPaid"] = True
                student["lastPaymentMonth"] = student["lastPaymentDate"][:7]

        if student["monthlyFee"] > 0 and student["lastPaymentDate"]:
            student["history"].append({"date": student["lastPaymentDate"], "status": "Completado", "amount": student["monthlyFee"]})
            
        students.append(student)

# 3. Guardar Resultado
data_content = "import { type Student } from '../types';\n\nexport const INITIAL_STUDENTS_DATA: Student[] = " + json.dumps(students, indent=2, ensure_ascii=False) + ";"
with open('d:/DOJO DEMO/src/data/students.ts', 'w', encoding='utf-8') as f:
    f.write(data_content)
print(f"Data merge completa. registros procesados.")
