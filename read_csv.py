import csv
from typing import List, Dict

def read_csv_files(files: List[str]) -> List[Dict]:
    all_data = []
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row['coffee_spent'] = float(row['coffee_spent'])
                    all_data.append(row)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {file_path} не найден")
        except Exception as e:
            raise Exception(f"Ошибка при чтении файла {file_path}: {e}")
    
    return all_data