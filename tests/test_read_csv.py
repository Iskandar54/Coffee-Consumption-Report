# test_read_csv.py
import pytest
import tempfile
import os
from read_csv import read_csv_files

def test_read_csv_single_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', 
                                     delete=False, encoding='utf-8') as f:
        f.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
        f.write("Алексей Смирнов,2024-06-01,450,4.5,12,норм,Математика\n")
        f.write("Дарья Петрова,2024-06-01,200,7.0,6,отл,Математика\n")
        temp_file = f.name
    
    try:
        data = read_csv_files([temp_file])
        
        assert len(data) == 2
        assert data[0]['student'] == 'Алексей Смирнов'
        assert data[0]['coffee_spent'] == 450.0
        assert data[1]['student'] == 'Дарья Петрова'
        assert data[1]['coffee_spent'] == 200.0
    finally:
        os.unlink(temp_file)

def test_read_csv_multiple_files():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', 
                                     delete=False, encoding='utf-8') as f1:
        f1.write("student,coffee_spent\nАлексей,450\n")
        file1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', 
                                     delete=False, encoding='utf-8') as f2:
        f2.write("student,coffee_spent\nДарья,200\n")
        file2 = f2.name
    
    try:
        data = read_csv_files([file1, file2])
        
        assert len(data) == 2
        assert data[0]['student'] == 'Алексей'
        assert data[0]['coffee_spent'] == 450.0
        assert data[1]['student'] == 'Дарья'
        assert data[1]['coffee_spent'] == 200.0
    finally:
        os.unlink(file1)
        os.unlink(file2)

def test_read_csv_file_not_found():
    with pytest.raises(FileNotFoundError) as exc_info:
        read_csv_files(['non_existent_file.csv'])
    
    assert "non_existent_file.csv" in str(exc_info.value)

def test_read_csv_invalid_data():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', 
                                     delete=False, encoding='utf-8') as f:
        f.write("student,coffee_spent\n")
        f.write("Алексей,not_a_number\n")
        temp_file = f.name
    
    try:
        with pytest.raises(Exception) as exc_info:
            read_csv_files([temp_file])
        
        assert "ошибка при чтении" in str(exc_info.value).lower()
    finally:
        os.unlink(temp_file)

def test_read_csv_empty_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', 
                                     delete=False, encoding='utf-8') as f:
        f.write("student,coffee_spent\n")
        temp_file = f.name
    
    try:
        data = read_csv_files([temp_file])
        assert len(data) == 0
    finally:
        os.unlink(temp_file)