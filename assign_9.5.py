import sys
import os
import csv
import json
import pickle


# ---------- BASE CLASS ----------
class FileHandler:

    def __init__(self, filename):

        self.filename = filename
        self.data = []

    def read_file(self):
        pass

    def save_file(self, dst):
        pass


# ---------- CSV CLASS ----------
class CSVFile(FileHandler):

    def read_file(self):

        with open(self.filename, "r") as file:

            reader = csv.reader(file)

            for row in reader:
                self.data.append(row)

    def save_file(self, dst):

        with open(dst, "w", newline="") as file:

            writer = csv.writer(file)

            for row in self.data:
                writer.writerow(row)


# ---------- JSON CLASS ----------
class JSONFile(FileHandler):

    def read_file(self):

        with open(self.filename, "r") as file:

            self.data = json.load(file)

    def save_file(self, dst):

        with open(dst, "w") as file:

            json.dump(self.data, file)


# ---------- PICKLE CLASS ----------
class PickleFile(FileHandler):

    def read_file(self):

        with open(self.filename, "rb") as file:

            self.data = pickle.load(file)

    def save_file(self, dst):

        with open(dst, "wb") as file:

            pickle.dump(self.data, file)


# ---------- CHECK ARGUMENTS ----------
if len(sys.argv) < 4:

    print("Usage:")
    print("python reader.py src dst changes")
    exit()


src = sys.argv[1]
dst = sys.argv[2]
changes = sys.argv[3:]


# ---------- CHECK FILE ----------
if not os.path.isfile(src):

    print("File does not exist.")

    folder = os.path.dirname(src)

    if folder == "":
        folder = "."

    print("\nFiles in directory:")

    for file in os.listdir(folder):
        print(file)

    exit()


# ---------- CHOOSE FILE TYPE ----------
if src.endswith(".csv"):

    handler = CSVFile(src)

elif src.endswith(".json"):

    handler = JSONFile(src)

elif src.endswith(".pickle"):

    handler = PickleFile(src)

else:

    print("Unsupported file type.")
    exit()


# ---------- READ FILE ----------
handler.read_file()


# ---------- APPLY CHANGES ----------
for change in changes:

    parts = change.split(",")

    if len(parts) != 3:

        print("Wrong change:", change)
        continue

    x = int(parts[0])
    y = int(parts[1])
    value = parts[2]

    # check indexes
    if y >= len(handler.data):

        print("Wrong row:", y)
        continue

    if x >= len(handler.data[y]):

        print("Wrong column:", x)
        continue

    # change value
    handler.data[y][x] = value


# ---------- DISPLAY DATA ----------
print("\nModified data:\n")

for row in handler.data:
    print(row)


# ---------- SAVE FILE ----------
if dst.endswith(".csv"):

    save_handler = CSVFile(dst)

elif dst.endswith(".json"):

    save_handler = JSONFile(dst)

elif dst.endswith(".pickle"):

    save_handler = PickleFile(dst)

else:

    print("Unsupported destination type.")
    exit()


save_handler.data = handler.data

save_handler.save_file(dst)

print("\nFile saved to:", dst)