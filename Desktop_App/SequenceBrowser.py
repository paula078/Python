import tkinter
from tkinter import filedialog
from tkinter import *
import xlsxwriter

# Program uruchamia aplikacje okienkowa ulatwiajacy przeszukiwanie duzych plikow wyjsciowych z pomiaru spektroskopu LC-MS/MS
# Program tworzy plik .xls z wszyskimi rekordami sekwencji, ktore zostaly znalezione dla bialka o podanym ID
# Program ma za zadanie glownie ulatwic prace z duzymi plikami - takimi, ktorych nie da sie otworzyc np. w excelu'

root = tkinter.Tk()
height = 400
width = 600
root.geometry(f'{width}x{height}')
root.configure(background='lightgrey')
root.title("Sequence browser")


label = tkinter.Label(root, text="Enter protein's ID", font=("Times New Roman", 20), bg="lightgrey")
label.place(relx=0.37, rely=0.3, anchor="n")

frame_file = tkinter.Frame(root, bg="lightgrey")
frame_file.place(relx=0.80, rely=0.1, relwidth=0.35, relheight=0.09, anchor="n")

# czesc okienka w ktorym wyswietla sie pole do wpisywania tekstu oraz "OK"
frame = tkinter.Frame(root, bg="lightgrey")
frame.place(relx=0.5, rely=0.4, relwidth=0.75, relheight=0.2, anchor="n")

entry = tkinter.Entry(frame, bd=2.5, font=("Times New Roman", 20))
entry.place(relwidth=0.65, relheight=0.5)

check_mod = tkinter.IntVar()
check_button = tkinter.Checkbutton(root, text="Only modifications", variable=check_mod, bg="lightgrey", font=("Times New Roman", 10))
check_button.place(relx=0.12, rely=0.6)

check_uniq = tkinter.IntVar()
unique_button = tkinter.Checkbutton(root, text="Unique sequences", variable=check_uniq, bg="lightgrey", font=("Times New Roman", 10))
unique_button.place(relx=0.4, rely=0.6)


file_label = tkinter.Label(root, text='Loaded file:', font=("Times New Roman", 8), bg="lightgrey")
file_label.place(relx=0.77, rely=0.21, anchor="n")

file_path = ""

col_names = {}

# wybor pliku wejsciowego
def select_file():
    global file_path
    file_path = filedialog.askopenfilename(initialdir="/",
                                           title="Select File",
                                           filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
    file_name = file_path.split("/")
    file_label.config(text=f'Loaded file: {file_name[-1]}')
    button.config(state=NORMAL)

def click():
    global file_path, unique_sequence
    seq_list = []
    id = entry.get()
    option = 0

    if check_mod.get():
        option += 1
    if check_uniq.get():
        option += 2
        unique_sequence = []

    with open(file_path, "r") as file:
        for line in file:
            temp_list = line.split("\t")
            if "Sequence" in line:
                header = temp_list
                for i in range(len(temp_list)):
                    col_names[temp_list[i]] = i

            if id in temp_list[col_names["Proteins"]]:
                match option:
                    case 0:
                        seq_list.append(temp_list)
                    case 1:
                        if "Unmodified" not in temp_list[col_names["Modifications"]]:
                            seq_list.append(temp_list)
                    case 2:
                        if temp_list[col_names["Sequence"]] not in unique_sequence:
                            unique_sequence.append(temp_list[col_names["Sequence"]])
                            seq_list.append(temp_list)

            elif id in temp_list[col_names["Proteins"]]:
                seq_list.append(temp_list)


    with xlsxwriter.Workbook('Result.xlsx') as workbook:
        worksheet = workbook.add_worksheet()

        worksheet.write_row(0, 0, header)
        for row_num, data in enumerate(seq_list):
            worksheet.write_row(row_num+1, 0, data)


button_path = tkinter.Button(frame_file, text="Select file", command=select_file, font=("Times New Roman", 12),
                             bg='white', bd=2.5)
button_path.place(relx=0.12, rely=0.01, relwidth=0.55, relheight=0.85)

button = tkinter.Button(frame, text="OK", state=DISABLED, command=click, bg='white', font=("Times New Roman", 20), bd=2.5)
button.place(relx=0.75, relwidth=0.2, relheight=0.45)

root.mainloop()