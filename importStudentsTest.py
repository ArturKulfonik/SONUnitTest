import pytest
import os
from tempfile import NamedTemporaryFile
from unittest.mock import patch
from main import ( Student,
                  importStudents, )

#test import students

@pytest.fixture
def sample_students():
    return [
        Student("Jan", "Kowalski"),
        Student("Anna", "Nowak", True),
        Student("Marek", "Zieliński", False),
    ]

def testImportStudentsCorrectFile():
    with NamedTemporaryFile(delete=False, mode='w') as temp_file:
        temp_file.write("Jan Kowalski\nAnna Nowak\n")
        temp_file_path = temp_file.name
    
    students = importStudents(temp_file_path)
    
    assert len(students) == 2
    assert students[0].imie == "Jan"
    assert students[0].nazwisko == "Kowalski"
    assert students[1].imie == "Anna"
    assert students[1].nazwisko == "Nowak"
    
    os.remove(temp_file_path)

def testImportStudentsFileNotFound():
    students = importStudents("non_existing_file.txt")
    assert students == []