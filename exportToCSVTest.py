import pytest
import os
from tempfile import NamedTemporaryFile
from unittest.mock import patch
from main import ( Student,
                  exportToCSV, )

#test export to csv (test for txt is same)

@pytest.fixture
def sample_students():
    return [
        Student("Jan", "Kowalski"),
        Student("Anna", "Nowak", True),
        Student("Marek", "Zieliński", False),
    ]

def testExportToCSVFile(sample_students):
    with NamedTemporaryFile(delete=False, mode='w', suffix='.csv') as temp_file:
        temp_file_path = temp_file.name

    exportToCSV(sample_students, temp_file_path)
    assert os.path.exists(temp_file_path)

    os.remove(temp_file_path)

def testexportToCSVCorrectFormat(sample_students):
    with NamedTemporaryFile(delete=False, mode='w', suffix='.csv') as temp_file:
        temp_file_path = temp_file.name

    exportToCSV(sample_students, temp_file_path)
    
    with open(temp_file_path, 'r') as file:
        lines = file.readlines()
        assert len(lines) == 4  # Header + 3 students
        assert "Jan,Kowalski,Nieobecny\n" in lines
        assert "Anna,Nowak,Obecny\n" in lines

    os.remove(temp_file_path)