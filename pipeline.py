import csv
import sys
from datetime import datetime

def clean_data(input_file, output_file):
    print(f"[*] Procesando archivo: {input_file}...")
    processed_rows = 0
    errors = 0
    total_value = 0.0

    try:
        with open(input_file, mode='r', encoding='utf-8-sig') as infile:
            reader = csv.reader(infile)
            header = next(reader, None)

            if not header:
                print("[X] El archivo está vacío.")
                return

            # Limpiar
            cleaned_headers = [h.strip().lower() for h in header]
            
            cleaned_data = []

            for row in reader:
                if not row or len(row) < len(cleaned_headers):
                    errors += 1
                    continue

                row_dict = {cleaned_headers[i]: row[i].strip() for i in range(len(cleaned_headers))}

                try:
                    item_id = row_dict.get('id', '')
                    name = row_dict.get('nombre', '').title()
                    category = row_dict.get('categoria', 'GENERAL').upper()
                    if not category:
                        category = 'GENERAL'
                    
                    price_str = row_dict.get('precio', '0')
                    price = float(price_str)

                    if not item_id or price <= 0:
                        errors += 1
                        continue

                    total_value += price
                    processed_rows += 1

                    cleaned_data.append({
                        'id': item_id,
                        'nombre': name,
                        'categoria': category,
                        'precio_unitario': f"{price:.2f}",
                        'fecha_procesado': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                except ValueError:
                    errors += 1

        if cleaned_data:
            fieldnames = ['id', 'nombre', 'categoria', 'precio_unitario', 'fecha_procesado']
            with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(cleaned_data)

            print(f"[✔] Éxito: {processed_rows} registros procesados correctamente.")
            print(f"[!] Registros omitidos/errores: {errors}")
            print(f"[$] Valor total procesado: ${total_value:.2f}")
            print(f"[📁] Reporte generado en: {output_file}")
        else:
            print("[X] No se encontraron registros válidos.")

    except FileNotFoundError:
        print(f"[X] Error: No se encontró el archivo '{input_file}'.")

if __name__ == "__main__":
    input_filename = sys.argv[1] if len(sys.argv) > 1 else 'datos_entrada.csv'
    clean_data(input_filename, 'reporte_procesado.csv')