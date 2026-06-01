# -------------- Program for editing csv files -----------

import sys
import os
import csv


# ---------- CHECK ARGUMENTS ----------
if len(sys.argv) < 4:

    print("Usage:")
    print("python reader.py source.csv destination.csv change1 change2 ...")

    exit()


# ---------- GET ARGUMENTS ----------
src = sys.argv[1]

dst = sys.argv[2]

changes = sys.argv[3:]


# ---------- CHECK SOURCE FILE ----------
if not os.path.isfile(src):

    print("Error: File does not exist.")

    folder = os.path.dirname(src)

    if folder == "":
        folder = "."

    print("\nFiles in the same directory:")

    for file in os.listdir(folder):

        print(file)

    exit()


# ---------- READ CSV ----------
data = []

try:

    with open(src, "r") as file:

        reader = csv.reader(file)

        for row in reader:

            data.append(row)

except:

    print("Error reading file.")

    exit()


# ---------- APPLY CHANGES ----------
for change in changes:

    parts = change.split(",")

    # Optional challenge
    if len(parts) != 3:

        print("Wrong format:", change)

        continue

    try:

        column = int(parts[0])

        row = int(parts[1])

        value = parts[2]

    except:

        print("Wrong change:", change)

        continue

    # Check row
    if row < 0 or row >= len(data):

        print("Row does not exist:", row)

        continue

    # Check column
    if column < 0 or column >= len(data[row]):

        print("Column does not exist:", column)

        continue

    # Change value
    data[row][column] = value


# ---------- DISPLAY MODIFIED DATA ----------
print("\nModified CSV:\n")

for row in data:

    print(",".join(row))


# ---------- SAVE FILE ----------
try:

    with open(dst, "w", newline="") as file:

        writer = csv.writer(file)

        for row in data:

            writer.writerow(row)

except:

    print("Error saving file.")

    exit()


print("\nFile saved to:", dst)