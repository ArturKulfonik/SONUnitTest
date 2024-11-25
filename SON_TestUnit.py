import pytest
import os
from tempfile import NamedTemporaryFile
from io import StringIO
from unittest.mock import patch
from datetime import datetime
from SON import ( Student,
                  addNewStudent,
                  editPresence,
                  exportToCSV,
                  importStudents,
                  checkPresence,
                  syncPresence )


#add new student test
@pytest.fixture
def sample_students():
    return [
        Student("Jan", "Kowalski"),
        Student("Anna", "Nowak", True),
        Student("Marek", "Zieliński", False),
    ]

def testAddNewStudentCorrectInput(sample_students):
    with patch("builtins.input", side_effect=["Katarzyna", "Wiśniewska", "tak"]):
        addNewStudent(sample_students)
    
    assert len(sample_students) == 4
    assert sample_students[-1].name == "Katarzyna"
    assert sample_students[-1].surname == "Wiśniewska"
    assert sample_students[-1].presence is True

def testAddNewStudentIncorrectInput(sample_students):
    with patch("builtins.input", side_effect=["Katarzyna", "Wiśniewska", "nie"]):
        addNewStudent(sample_students)
    
    assert len(sample_students) == 4
    assert sample_students[-1].presence is False


#test edit presence
@pytest.fixture
def sample_students():
    return [
        Student("Jan", "Kowalski"),
        Student("Anna", "Nowak", True),
        Student("Marek", "Zieliński", False),
    ]

def testEditPresenceInput(sample_students):
    presence = {student: student.presence for student in sample_students}
    with patch("builtins.input", side_effect=["tak", "nie", "tak"]):
        editPresence(presence)
    
    assert presence[sample_students[0]] is True
    assert presence[sample_students[1]] is False
    assert presence[sample_students[2]] is True

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

#check presence

@pytest.fixture
def sample_students():
    return [
        Student("Jan", "Kowalski"),
        Student("Anna", "Nowak", True),
        Student("Marek", "Zieliński", False),
    ]

def testCheckPresenceCorrectInput(sample_students):
    with patch("builtins.input", side_effect=["tak", "nie", "tak"]):
        checkPresence(sample_students)
    
    assert sample_students[0].obecnosc is True
    assert sample_students[1].obecnosc is False
    assert sample_students[2].obecnosc is True

#test sync

@pytest.fixture
def sample_students():
    return [
        Student("Jan", "Kowalski"),
        Student("Anna", "Nowak", True),
        Student("Marek", "Zieliński", False),
    ]

def testSyncPresenceCorrectUpdate(sample_students):
    obecnosci = {
        sample_students[0]: True,
        sample_students[1]: False,
        sample_students[2]: True,
    }
    syncPresence(sample_students, obecnosci)
    
    assert sample_students[0].obecnosc is True
    assert sample_students[1].obecnosc is False
    assert sample_students[2].obecnosc is True
