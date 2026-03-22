import argparse
import sys
from read_csv import read_csv_files
from reports import REPORTS
from tabulate import tabulate


def print_report(report_data, headers):
    print(tabulate(report_data, headers=headers, tablefmt="grid", floatfmt=".2f"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+', required=True, help='Список CSV файлов для обработки')
    parser.add_argument('--report', required=True, help='Тип отчета')
    
    args = parser.parse_args()
    
    try:
        all_data = read_csv_files(args.files)
        
        if args.report not in REPORTS:
            print(f'Неизвестный отчет: {args.report}')
            print(f'Доступные отчеты: {",".join(REPORTS.keys())}')
            sys.exit(1)

        report_fun = REPORTS[args.report]
        report_data, headers = report_fun(all_data)
        print_report(report_data, headers)
            
    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()