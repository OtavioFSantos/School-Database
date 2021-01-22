from PyQt5 import uic, QtWidgets
from reportlab.pdfgen import canvas
import mysql.connector

base = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "studants"
)

def form_function():
    name = form.lineEdit.text()
    code = form.lineEdit_2.text()
    studant_class = form.lineEdit_3.text()
    special = ""

    print(f"\nStudant: {name}\nCode: {code}\nClass: {studant_class}")
    if form.radioButton.isChecked():
        print("Studant have a Disability.")
        special = "Studant have a Disability"
    else: 
        special = "Studant doesn't have a Disability"

    cursor = base.cursor()
    command_sql = "INSERT INTO people (studant_name, studant_code, studant_class, studant_special) VALUES (%s, %s, %s, %s)"
    data = (str(name), str(code), str(studant_class), special)
    cursor.execute(command_sql, data)
    base.commit()
    form.lineEdit.setText("")
    form.lineEdit_2.setText("")
    form.lineEdit_3.setText("")
    form.radioButton.setChecked(False)

def show_function():
    form.show()
    form.pushButton.clicked.connect(form_function)
    form.pushButton_2.clicked.connect(list_function)

def list_function():
    lisT.show()
    cursor = base.cursor()
    cursor.execute("SELECT * FROM people")
    data_read = cursor.fetchall()
    lisT.tableWidget.setRowCount(len(data_read))
    lisT.tableWidget.setColumnCount(5)
    for i in range(0, len(data_read)):
        for j in range(0, 5):
            lisT.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(data_read[i][j])))

def gen_pdf():
    cursor = base.cursor()
    cursor.execute("SELECT * FROM people")
    data_read = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("studants.pdf")
    pdf.setFont("Times-Bold", 16)
    pdf.drawString(200, 800, "Registered Students:")
    pdf.setFont("Times-Bold", 12)
    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "Name")
    pdf.drawString(210, 750, "Code")
    pdf.drawString(310, 750, "Class")
    pdf.drawString(410, 750, "Special")
    for i in range(0, len(data_read)):
        y = y + 50
        k = 10
        for j in range(0, 5):
            pdf.drawString(k, 750 - y, str(data_read[i][j]))
            k = k + 100
    pdf.save()

def rem_show():
    rem.show()
    cursor = base.cursor()
    cursor.execute("SELECT * FROM people")
    data_read = cursor.fetchall()
    rem.tableWidget.setRowCount(len(data_read))
    rem.tableWidget.setColumnCount(5)
    for i in range(0, len(data_read)):
        for j in range(0, 5):
            rem.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(data_read[i][j])))

def remove_studant():
    string = rem.tableWidget.currentRow()
    rem.tableWidget.removeRow(string)

    cursor = base.cursor()
    cursor.execute("SELECT id FROM people")
    data_read = cursor.fetchall()
    value_id = data_read[string][0]
    cursor.execute("DELETE FROM people WHERE id=" + str(value_id))
    base.commit()


app = QtWidgets.QApplication([])
form = uic.loadUi("RegisterStudants.ui")
lisT = uic.loadUi("List.ui")
wel = uic.loadUi("Welcome.ui")
rem = uic.loadUi("Remove.ui")
wel.pushButton_2.clicked.connect(show_function)
wel.pushButton.clicked.connect(rem_show)
lisT.pushButton.clicked.connect(gen_pdf)
rem.pushButton.clicked.connect(remove_studant)

wel.show()
app.exec()