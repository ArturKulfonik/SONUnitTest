import pytest
from unittest.mock import patch
from main import ( Student,
                  editPresence, )

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