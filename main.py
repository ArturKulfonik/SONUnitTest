import os
import csv
from datetime import datetime

class Student:
    def __init__(self, name, surname, presence=False):
        self.name = name
        self.surname = surname
        self.presence = presence

    def __str__(self):
        return f"{self.name} {self.surname} - {'Obecny' if self.presence else 'Nieobecny'}"

    def to_csv(self):
        return f"{self.name},{self.surname},{'Obecny' if self.presence else 'Nieobecny'}"


def importStudents(file_path):
    students = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(' ')
                if len(data) >= 2:
                    students.append(Student(data[0], data[1]))
    else:
        print("Plik nie istnieje.")
    return students


def exportToCSV(students, file_path):
    try:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Imie", "Nazwisko", "Obecny"])
            for student in students:
                writer.writerow([student.name, student.surname, "Obecny" if student.presence else "Nieobecny"])
        print(f"Zapisano plik CSV: {file_path}")
    except Exception as ex:
        print(f"Błąd przy zapisie pliku CSV: {ex}")


def exportToTXT(students, file_path):
    try:
        with open(file_path, 'w') as file:
            for student in students:
                file.write(str(student) + '\n')
        print(f"Zapisano plik TXT: {file_path}")
    except Exception as ex:
        print(f"Błąd przy zapisie pliku TXT: {ex}")


def addNewStudent(students):
    name = input("Podaj imię studenta: ")
    surname = input("Podaj surname studenta: ")
    presence = input("Czy student jest obecny? (tak/nie): ").strip().lower() == 'tak'
    nowy_student = Student(name, surname, presence)
    students.append(nowy_student)
    print(f"Dodano nowego studenta: {nowy_student}")


def editPresence(presence):
    print("Edycja obecności studentów:")
    for student in presence:
        obecny = input(f"Czy {student.name} {student.surname} jest obecny? (tak/nie): ").strip().lower() == 'tak'
        presence[student] = obecny


def syncPresence(students, presence):
    for student in students:
        if student in presence:
            student.presence = presence[student]


def checkPresence(studenci):
    for student in studenci:
        obecny = input(f"Czy {student.name} {student.surname} jest obecny? (tak/nie): ").strip().lower() == 'tak'
        student.presence = obecny


def main():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    input_file_path = os.path.join(desktop_path, "Obecni.txt")

    students = importStudents(input_file_path)

    if not students:
        print("Plik nie zawiera studentów lub nie istnieje.")
        return

    data_input = input("Podaj dzisiejszą datę (dd-mm-YY): ")
    data = datetime.strptime(data_input, "%d-%m-%Y")

    if input("Czy chcesz sprawdzić obecność studentów? (tak/nie): ").strip().lower() == 'tak':
        checkPresence(students)

    print("Lista studentów:")
    for student in students:
        print(student)

    if input("Czy chcesz dodać nowego studenta? (tak/nie): ").strip().lower() == 'tak':
        addNewStudent(students)

    presence = {student: student.presence for student in students}

    if input("Czy chcesz edytować listę obecności? (tak/nie): ").strip().lower() == 'tak':
        editPresence(presence)

    syncPresence(students, presence)

    format_zapisu = input("Podaj format zapisu txt/csv: ").strip().lower()
    output_file_path = os.path.join(desktop_path, "Obecni_Export.csv" if format_zapisu == 'csv' else "Obecni_Export.txt")

    if format_zapisu == 'csv':
        exportToCSV(students, output_file_path)
    elif format_zapisu == 'txt':
        exportToTXT(students, output_file_path)
    else:
        print("Nieznany format.")

    print(f"Zapisano plik na pulpicie: {output_file_path}")


if __name__ == "__main__":
    main()