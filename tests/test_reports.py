import pytest
from reports import generate_median_coffee_report

def test_median_coffee_basic():
    data = [
        {'student': 'Алексей', 'coffee_spent': 450},
        {'student': 'Алексей', 'coffee_spent': 500},
        {'student': 'Дарья', 'coffee_spent': 200},
        {'student': 'Дарья', 'coffee_spent': 250},
    ]
    
    report, headers = generate_median_coffee_report(data)
    
    assert headers == ["student", "median_coffee"]
    assert len(report) == 2
    assert report[0][0] == 'Алексей'  
    assert report[0][1] == 475.0
    assert report[1][0] == 'Дарья'
    assert report[1][1] == 225.0

def test_median_coffee_odd_count():
    data = [
        {'student': 'Иван', 'coffee_spent': 100},
        {'student': 'Иван', 'coffee_spent': 200},
        {'student': 'Иван', 'coffee_spent': 300},
    ]
    
    report, _ = generate_median_coffee_report(data)
    
    assert report[0][1] == 200.0

def test_median_coffee_single_record():
    data = [
        {'student': 'Мария', 'coffee_spent': 150},
    ]
    report, _ = generate_median_coffee_report(data)
    
    assert report[0][1] == 150.0

def test_median_coffee_multiple_students():
    data = [
        {'student': 'Студент1', 'coffee_spent': 100},
        {'student': 'Студент1', 'coffee_spent': 200},
        {'student': 'Студент2', 'coffee_spent': 500},
        {'student': 'Студент3', 'coffee_spent': 300},
        {'student': 'Студент3', 'coffee_spent': 400},
    ]
    
    report, _ = generate_median_coffee_report(data)
    
    medians = [median for _, median in report]
    assert medians == sorted(medians, reverse=True)
    
    assert report[0][0] == 'Студент2' 
    assert report[1][0] == 'Студент3'  
    assert report[2][0] == 'Студент1'  

def test_median_coffee_empty_data():
    report, headers = generate_median_coffee_report([])
    
    assert report == []
    assert headers == ["student", "median_coffee"]

def test_median_coffee_same_names():
    data = [
        {'student': 'Алексей', 'coffee_spent': 100},
        {'student': 'Алексей', 'coffee_spent': 200},
        {'student': 'Алексей', 'coffee_spent': 300},
    ]
    
    report, _ = generate_median_coffee_report(data)
    
    assert len(report) == 1
    assert report[0][1] == 200.0