import pytest
from unittest.mock import patch
from main import ( Student,
                  addNewStudent )

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