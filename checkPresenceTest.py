import pytest
from unittest.mock import patch
from main import ( Student,
                  checkPresence, )

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
        #ma byc uniwersalne, jak jest z konsoli albo z aplikacji itd
        checkPresence(sample_students)
    
    assert sample_students[0].presence is True
    assert sample_students[1].presence is False
    assert sample_students[2].presence is True