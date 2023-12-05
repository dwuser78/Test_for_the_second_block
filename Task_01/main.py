from datetime import datetime
import getopt
import csv
import os
import sys
import string
import random


_NOTES_DIR = "notes"
_NOTES_EXT = ".csv"
_FILE_NAME_SIZE = 9
_SHORT_OPTS = "lsaedhf:i:t:m:"
_LONG_OPTS = ["list", "show", "add", "edit", "del", "help", "filter=", "id=",
              "title=", "msg="]

def print_help():
    print("A command-line utility for working with your notes.")
    print("Usage: <command> [options]")
    print("Commands:")
    print("\t-l, --list\tPrint a list of notes.")
    print("\t-s, --show\tShow the selected note.")
    print("\t-a, --add\tAdd a new note.")
    print("\t-e, --edit\tEdit a specific note")
    print("\t-d, --del\tDelete a specific note.")
    print("\t-h, --help\tPrint this help page.")
    print("Options:")
    print("\t-f <dd.mm.yyyy | dd.mm.yyyy-dd.mm.yyyy>,\n"
          "\t    --filter <dd.mm.yyyy | dd.mm.yyyy-dd.mm.yyyy>\n"
          "\t\t\tUse notes for the specified date.")
    print("\t-i, --id\tUse a note with a specific ID.")
    print("\t-t, --title\tNote title.")
    print("\t-m, --msg\tNote Body.")
    print("Usage example:")
    print("\tpython main.py --add --title=\"Note title\" --msg=\"Note body\"")
    print("\tpython main.py --edit --id=1bsk3klp2 --title=\"New note title\" "
          "--msg=\"New note body\"")
    print("\tpython main.py --edit --id=1bsk3klp2 --title=\"New note title\"")
    print("\tpython main.py --edit --id=1bsk3klp2 --msg=\"New note body\"")
    print("\tpython main.py --del --id=1bsk3klp2")
    print("\tpython main.py --del --id=1bsk3klp2 7kvljvdi8")
    print("\tpython main.py --del --filter=03.12.2023-05.12.2023")
    print("\t")

def get_filtered_notes(notes_dir, date_str=""):
    note_file_names = os.listdir(notes_dir)
    filtered_file_names = []

    if date_str == "":
        return note_file_names
    else:
        date_str = date_str.split("-", 1)

        try:
            dates = [datetime.strptime(date, "%d.%m.%Y") for date in date_str]
        except ValueError:
            print('Invalid date value')
            raise SystemExit(1)

        for note_file_name in note_file_names:
            try:
                with open(os.sep.join([notes_dir, note_file_name]), "r") as csv_file:
                    csv_data = csv.reader(csv_file, delimiter=";")
                    csv_row = next(csv_data)

                    date_time = datetime.strptime(csv_row[3], "%d.%m.%Y %H:%M:%S")
                    date_time = date_time.replace(hour=0, minute=0, second=0, microsecond=0)

                    if len(dates) == 1:
                        if date_time == dates[0]:
                            filtered_file_names.append(note_file_name)
                    else:
                        if dates[0] <= date_time <= dates[1]:
                            filtered_file_names.append(note_file_name)
            except Exception:
                print("Error reading the note file")
                raise SystemExit(1)

        return filtered_file_names

def print_notes_list(notes_dir, date_str=""):
    note_file_names = get_filtered_notes(notes_dir, date_str)

    print("ID\t\tTitle")

    for note_file_name in note_file_names:
        id = note_file_name.rsplit(_NOTES_EXT, 1)[0]

        try:
            with open(os.sep.join([notes_dir, note_file_name]), "r") as csv_file:
                csv_data = csv.reader(csv_file, delimiter=";")
                csv_row = next(csv_data)
        except Exception:
            print("Error reading the note file")
            raise SystemExit(1)

        print(f"{id}\t{csv_row[1]}")

def show_note(notes_dir, id):
    if id == "":
        print("The note ID cannot be empty")
        raise SystemExit(1)

    note_file_name = f"{id}{_NOTES_EXT}"

    if not os.path.exists(os.sep.join([notes_dir, note_file_name])):
        print("The note file was not found")
        raise SystemExit(1)

    try:
        with open(os.sep.join([notes_dir, note_file_name]), "r") as csv_file:
            csv_data = csv.reader(csv_file, delimiter=";")
            csv_row = next(csv_data)
    except Exception:
        print("Error reading the note file")
        raise SystemExit(1)

    print(csv_row[1])
    print(csv_row[2])

def create_note(notes_dir, title_note, msg_note):
    if title_note == "":
        print("The title of the note cannot be empty")
        raise SystemExit(1)

    if msg_note == "":
        print("The body of the note cannot be empty")
        raise SystemExit(1)

    date_note = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    while True:
        id = "".join(random.choices(string.ascii_lowercase + string.digits,
                                    k=_FILE_NAME_SIZE))
        note_file_name = f"{id}{_NOTES_EXT}"

        if not os.path.exists(os.sep.join([notes_dir, note_file_name])):
            break
    try:
        with open(os.sep.join([notes_dir, note_file_name]), "w") as csv_file:
            csv_data = csv.writer(csv_file, delimiter=";")
            csv_data.writerow([id, title_note, msg_note, date_note])
    except Exception:
        print("Error writing the note file")
        raise SystemExit(1)

    print("A new note has been successfully created")


def edit_note(notes_dir, id, title_note, msg_note):
    if id == "":
        print("The note ID cannot be empty")
        raise SystemExit(1)

    if title_note == "" and msg_note == "":
        print("The title and body of the note cannot be empty")
        raise SystemExit(1)

    date_note = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    note_file_name = f"{id}{_NOTES_EXT}"

    if not os.path.exists(os.sep.join([notes_dir, note_file_name])):
        print("The note file was not found")
        raise SystemExit(1)

    try:
        with open(os.sep.join([notes_dir, note_file_name]), "r") as csv_file:
            csv_data = csv.reader(csv_file, delimiter=";")
            csv_row = next(csv_data)
    except Exception:
        print("Error reading the note file")
        raise SystemExit(1)

    if title_note == "":
        title_note = csv_row[1]

    if msg_note == "":
        msg_note = csv_row[2]

    try:
        with open(os.sep.join([notes_dir, note_file_name]), "w") as csv_file:
            csv_data = csv.writer(csv_file, delimiter=";")
            csv_data.writerow([id, title_note, msg_note, date_note])
    except Exception:
        print("Error writing the note file")
        raise SystemExit(1)

    print("The note has been successfully edited")

def delete_note(notes_dir, id, other_ids, date_str):
    if id == "" and date_str == "":
        print("The ID or date of the note cannot be empty")
        raise SystemExit(1)

    note_file_names = []

    if id == "":
        note_file_names = get_filtered_notes(notes_dir, date_str)
    elif id == "*":
        note_file_names = get_filtered_notes(notes_dir, "")
    else:
        note_file_names.append(f"{id}{_NOTES_EXT}")

        if len(other_ids) > 0:
            for id in other_ids:
                note_file_names.append(f"{id}{_NOTES_EXT}")

    if len(note_file_names) == 1:
        ans = input("Are you sure you want to delete the file "
                    f"'{note_file_names[0]}' (y/n)? [n]: ")

    elif len(note_file_names) > 1:
        ans = input(f"Are you sure you want to delete {len(note_file_names)} "
                    "files (y/n)? [n]: ")

    else:
        print("The list of files cannot be empty")
        raise SystemExit(1)

    if ans.lower() == "y":
        for note_file_name in note_file_names:
            if os.path.exists(os.sep.join([notes_dir, note_file_name])):
                os.remove(os.sep.join([notes_dir, note_file_name]))
            else:
                curr_id = note_file_name.rsplit(_NOTES_EXT, 1)[0]
                print(f"The note ID '{curr_id}' was not found")

        print("Note(s) have been successfully deleted")


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    notes_dir = os.sep.join([base_dir, _NOTES_DIR])

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, _SHORT_OPTS, _LONG_OPTS)
        if len(opts) > 0:
            if opts[0][0] == "-l" or opts[0][0] == "--list":
                if len(opts) > 1:
                    if opts[1][0] == "-f" or opts[1][0] == "--filter":
                        print_notes_list(notes_dir, opts[1][1])
                    else:
                        print("Invalid command line arguments")
                        raise SystemExit(1)
                else:
                    print_notes_list(notes_dir)

            elif opts[0][0] == "-s" or opts[0][0] == "--show":
                if len(opts) > 1:
                    if opts[1][0] == "-i" or opts[1][0] == "--id":
                        show_note(notes_dir, opts[1][1])
                    else:
                        print("Invalid command line arguments")
                        raise SystemExit(1)
                else:
                    print("Invalid command line arguments")
                    raise SystemExit(1)

            elif opts[0][0] == "-a" or opts[0][0] == "--add":
                if len(opts) > 2:
                    if opts[1][0] == "-t" or opts[1][0] == "--title":
                        title_note = opts[1][1]
                    else:
                        print("Invalid command line arguments")
                        raise SystemExit(1)

                    if opts[2][0] == "-m" or opts[2][0] == "--msg":
                        msg_note = opts[2][1]
                        create_note(notes_dir, title_note, msg_note)
                    else:
                        print("Invalid command line arguments")
                        raise SystemExit(1)
                else:
                    print("Invalid command line arguments")
                    raise SystemExit(1)

            elif opts[0][0] == "-e" or opts[0][0] == "--edit":
                if len(opts) > 1:
                    title_note = ""
                    msg_note = ""

                    if opts[1][0] == "-i" or opts[1][0] == "--id":
                        id = opts[1][1]
                    else:
                        print("Invalid command line arguments")
                        raise SystemExit(1)

                    if opts[2][0] == "-t" or opts[2][0] == "--title":
                        title_note = opts[2][1]
                    elif opts[2][0] == "-m" or opts[2][0] == "--msg":
                        msg_note = opts[2][1]
                    else:
                        print("Invalid command line arguments")
                        raise SystemExit(1)

                    if len(opts) > 3:
                        if opts[3][0] == "-m" or opts[3][0] == "--msg":
                            msg_note = opts[3][1]
                        else:
                            print("Invalid command line arguments")
                            raise SystemExit(1)

                    edit_note(notes_dir, id, title_note, msg_note)
                else:
                    print("Invalid command line arguments")
                    raise SystemExit(1)

            elif opts[0][0] == "-d" or opts[0][0] == "--del":
                if len(opts) > 1:
                    id = ""
                    date_note = ""

                    if opts[1][0] == "-i" or opts[1][0] == "--id":
                        id = opts[1][1]
                    elif opts[1][0] == "-f" or opts[1][0] == "--filter":
                        date_note = opts[1][1]
                    else:
                        print("Invalid command line arguments")
                        raise SystemExit(1)

                delete_note(notes_dir, id, args, date_note)

            elif opts[0][0] == "-h" or opts[0][0] == "--help":
                print_help()

        else:
            print_help()
    except getopt.GetoptError:
        print("Invalid command line arguments")
        raise SystemExit(1)
