from statistics import median
from typing import List, Dict, Tuple, Callable

ReportRow = Tuple[str, float]
ReportData = List[ReportRow]

def generate_median_coffee_report(data: List[Dict]) -> Tuple[ReportData, List[str]]:
    student_spending = {}
    
    for row in data:
        student = row['student']
        coffee_spent = row['coffee_spent']
        
        if student not in student_spending:
            student_spending[student] = []
        student_spending[student].append(coffee_spent)
    
    report = []
    for student, spending in student_spending.items():
        median_spent = median(spending)
        report.append((student, median_spent))
    
    report.sort(key=lambda x: x[1], reverse=True)
    headers = ["student", "median_coffee"]
    
    return report, headers

REPORTS: Dict[str, Callable] = {
    "median-coffee" : generate_median_coffee_report,
}