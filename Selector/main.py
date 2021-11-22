import mysql.connector
import tkinter as tk
from tkinter import filedialog
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(name, year, genre, developer, publisher, logo):
    print("Inserting BLOB into python_employee table")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='games',
                                             user='Lorenc',
                                             password='SAhara137797!')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO games
                          (name, year, genre, developer,publisher,logo) VALUES (%s,%s,%s,%s,%s,%s)"""
        sql_update_blob_query = """ INSERT INTO games
                          (year, genre, developer,publisher,logo) VALUES (%s,%s,%s,%s,%s) Where name=%s"""

        root = tk.Tk()
        root.withdraw()
        logo = filedialog.askopenfilename()
        empPicture = convertToBinaryData(logo)

        # Convert data into tuple format


        insert_blob_tuple = (name, year, genre, developer, publisher, empPicture)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

insertBLOB("Far Cry 3", "2012", "FPS", "Ubisoft", "Ubisoft",r"C:\Users\a.lorenc\Downloads\FarCry3.jpg")
# insertBLOB(2, "Scott", "D:\Python\Articles\my_SQL\images\scott_photo.png",
#            "D:\Python\Articles\my_SQL\images\scott_bioData.txt")
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('fc')
