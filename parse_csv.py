import csv
import json
import os

def map_belt(grado):
    if not grado: return 'WHITE'
    grado = grado.lower()
    if 'gris' in grado or 'gray' in grado:
        return 'GRAY'
    if 'negro' in grado or 'preta' in grado:
        return 'BLACK'
    if 'marrón' in grado or 'marron' in grado or 'marrom' in grado:
        return 'BROWN'
    if 'morado' in grado or 'roxo' in grado:
        return 'PURPLE'
    if 'azul' in grado:
        return 'BLUE'
    if 'blanco' in grado or 'branca' in grado:
        return 'WHITE'
    return 'WHITE'

students = []
with open('d:/DOJO DEMO/dojo_unificado_completo.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        student = {
            "id": str(i + 1),
            "name": row["Alumno"].strip(),
            "email": row["Correo"].strip(),
            "phone": row["Telefono"].strip(),
            "birthDate": row["FechaNacimiento"].strip() if row.get("FechaNacimiento") else None,
            "belt": map_belt(row["Grado"]),
            "classesAttended": 0,
            "classesToNextBelt": 40,
            "lastPaymentMonth": row["FechaPago"][:7] if row.get("FechaPago") else "",
            "isPaid": bool(row.get("FechaPago") and row["FechaPago"].strip()),
            "history": [],
            "plan": row.get("Plan", "").strip(),
            "joinDate": row.get("FechaIngreso", "").strip(),
            "lastPaymentDate": row.get("FechaPago", "").strip(),
        }
        
        tutor_name = row.get("Tutor", "").strip()
        if tutor_name:
            student["tutorName"] = tutor_name
            
        if row.get("Valor"):
             try:
                 amount_raw = row["Valor"].replace(".", "").replace("$", "").strip()
                 if amount_raw:
                     amount = int(amount_raw)
                     student["monthlyFee"] = amount
                     if row.get("FechaPago") and row["FechaPago"].strip():
                        student["history"].append({
                            "date": row["FechaPago"][:10],
                            "status": "Completado",
                            "amount": amount
                        })
             except:
                 pass
        students.append(student)

data_content = "import { type Student } from '../types';\n\nexport const INITIAL_STUDENTS_DATA: Student[] = " + json.dumps(students, indent=2, ensure_ascii=False) + ";"

output_path = 'd:/DOJO DEMO/src/data/students.ts'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(data_content)

print(f"File created at {output_path}")
