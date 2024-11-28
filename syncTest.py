import pytest
from unittest.mock import patch
from main import ( Student,
                  syncPresence )

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
