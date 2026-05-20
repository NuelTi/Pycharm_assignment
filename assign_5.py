# ---ADMIN DATA---
students = []
teachers = []
homeroom_teachers = []


# ---Defining FUNCTIONS---
def find_student(first, last):
    for s in students:
        if s["first"] == first and s["last"] == last:
            return s
    return None


def find_teacher(first, last):
    for t in teachers:
        if t["first"] == first and t["last"] == last:
            return t
    return None


def find_homeroom_teacher(first, last):
    for h in homeroom_teachers:
        if h["first"] == first and h["last"] == last:
            return h
    return None


# ---CREATE USERS---
def create_user():
    while True:
        print("\nCreate: student | teacher | homeroom teacher | end")
        choice = input("Choose: ").lower()

        if choice == "student":
            first = input("First name:")
            last = input("Last name:")
            class_name = input("Class (e.g. 3C):")

            students.append({
                "first": first,
                "last": last,
                "class": class_name})


        elif choice == "teacher":
            first = input("First name:")
            last = input("Last name:")
            subject = input("Subject:")

            print("Enter classes (empty line to stop):")
            classes = []
            while True:
                c = input()
                if c == "":
                    break
                classes.append(c)

            teachers.append({
                "first": first,
                "last": last,
                "subject": subject,
                "classes": classes})


        elif choice == "homeroom teacher":
            first = input("First name:")
            last = input("Last name:")
            class_name = input("Class they lead:")

            homeroom_teachers.append({
                "first": first,
                "last": last,
                "class": class_name})


        elif choice == "end":
            break

        else:
            print("Invalid option.")


# --- MANAGE USERS ---
def manage_user():
    while True:
        print("\nManage: class | student | teacher | homeroom teacher | end")
        choice = input("Choose: ").lower()

        if choice == "class":
            class_name = input("Enter class: ")

            print("\nStudents:")
            found = False
            for s in students:
                if s["class"] == class_name:
                    print(s["first"], s["last"])
                    found = True

            if not found:
                print("No students found.")

            print("\nHomeroom teacher:")
            for h in homeroom_teachers:
                if h["class"] == class_name:
                    print(h["first"], h["last"])

        elif choice == "student":
            first = input("First name: ")
            last = input("Last name: ")

            student = find_student(first, last)
            if student is None:
                print("Student not found.")
                continue

            print("Class:", student["class"])
            print("Teachers:")

            for t in teachers:
                if student["class"] in t["classes"]:
                    print(t["first"], t["last"], "-", t["subject"])

        elif choice == "teacher":
            first = input("First name: ")
            last = input("Last name: ")

            teacher = find_teacher(first, last)
            if teacher is None:
                print("Teacher not found.")
                continue

            print("Classes:")
            for c in teacher["classes"]:
                print(c)

        elif choice == "homeroom teacher":
            first = input("First name: ")
            last = input("Last name: ")

            h = find_homeroom_teacher(first, last)
            if h is None:
                print("Homeroom teacher not found.")
                continue

            print("Students in class", h["class"])
            for s in students:
                if s["class"] == h["class"]:
                    print(s["first"], s["last"])

        elif choice == "end":
            break

        else:
            print("Invalid option.")


# --- MAIN ---
def main():
    print("Commands: create | manage | end")

    while True:
        command = input("\nEnter command: ").lower()

        if command == "create":
            create_user()

        elif command == "manage":
            manage_user()

        elif command == "end":
            print("Program ended.")
            break

        else:
            print("Invalid command.")


# RUN PROGRAM
main()