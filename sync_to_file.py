import json
import os
import sys

def save_students(students_list_json):
    try:
        data = json.loads(students_list_json)
        
        # Formatear el contenido como un archivo TypeScript
        content = "import { type Student } from '../types';\n\nexport const INITIAL_STUDENTS_DATA: Student[] = "
        content += json.dumps(data, indent=2, ensure_ascii=False)
        content += ";"
        
        output_path = 'd:/DOJO DEMO/src/data/students.ts'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Base de datos sincronizada: {len(data)} estudiantes guardados.")
        return True
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        save_students(sys.argv[1])
    else:
        print("Falta el JSON de estudiantes.")
