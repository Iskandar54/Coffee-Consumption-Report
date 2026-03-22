import pytest
import tempfile
import os
import sys
from unittest.mock import patch
from main import main

def create_test_csv(content, filename="test.csv"):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', 
                                     delete=False, encoding='utf-8') as f:
        f.write(content)
        return f.name

def test_main_with_valid_files(capsys):
    csv_content = """student,date,coffee_spent,sleep_hours,study_hours,mood,exam
Алексей Смирнов,2024-06-01,450,4.5,12,норм,Математика
Алексей Смирнов,2024-06-02,500,4.0,14,устал,Математика
Дарья Петрова,2024-06-02,250,6.5,8,норм,Математика
Дарья Петрова,2024-06-01,200,7.0,6,отл,Математика"""
    
    file_path = create_test_csv(csv_content)
    
    try:
        with patch.object(sys, 'argv', ['main.py', '--files', file_path, '--report', 'median-coffee']):
            main()

        captured = capsys.readouterr()
        assert "Алексей Смирнов" in captured.out
        assert "475.00" in captured.out
        assert "Дарья Петрова" in captured.out
        assert "225.00" in captured.out
    finally:
        os.unlink(file_path)

def test_main_with_multiple_files():
    csv1 = """student,coffee_spent\nАлексей,450"""
    
    csv2 = """student,coffee_spent\nДарья,200"""
    
    file1 = create_test_csv(csv1, "file1.csv")
    file2 = create_test_csv(csv2, "file2.csv")
    
    try:
        with patch.object(sys, 'argv', ['main.py', '--files', file1, file2, '--report', 'median-coffee']):
            main()
    finally:
        os.unlink(file1)
        os.unlink(file2)

def test_main_with_unknown_report():
    csv_content = "student,coffee_spent\nАлексей,450"
    file_path = create_test_csv(csv_content)
    
    try:
        with patch.object(sys, 'argv', ['main.py', '--files', file_path, '--report', 'unknown-report']):
            with patch('sys.exit') as mock_exit:
                with patch('builtins.print') as mock_print:
                    main()
                    
                    mock_print.assert_any_call('Неизвестный отчет: unknown-report')
                    mock_exit.assert_called_with(1)
    finally:
        os.unlink(file_path)

def test_main_with_nonexistent_file():
    with patch.object(sys, 'argv', ['main.py', '--files', 'nonexistent.csv', '--report', 'median-coffee']):
        with patch('sys.exit') as mock_exit:
            with patch('builtins.print') as mock_print:
                main()
                
                mock_print.assert_any_call("Ошибка: Файл не найден - Файл nonexistent.csv не найден")
                mock_exit.assert_called_with(1)

def test_main_without_files_arg():
    with patch.object(sys, 'argv', ['main.py', '--report', 'median-coffee']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code != 0