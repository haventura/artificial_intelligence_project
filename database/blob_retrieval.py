import mysql.connector


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


def readBLOB(emp_id, photo, data):
    print("Reading BLOB data from file table")

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='DABAI',
                                             user='python',
                                             password='python')

        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT * from files where id = %s"""

        cursor.execute(sql_fetch_blob_query, (emp_id,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], )
            print("Name = ", row[1])
            image = row[2]
            file = row[3]
            print("Storing  image and data on disk \n")
            write_file(image, photo)
            write_file(file, data)

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


readBLOB(1, "/Users/dave/Desktop/python_stuff/query_output/photo1.png",
        "/Users/dave/Desktop/python_stuff/query_output/data1.txt")

readBLOB(2, "/Users/dave/Desktop/python_stuff/query_output/photo2.png",
        "/Users/dave/Desktop/python_stuff/query_output/data2.txt")

#readBLOB(2, "D:\Python\Articles\my_SQL\query_output\scott_photo.png",
 #        "D:\Python\Articles\my_SQL\query_output\scott_bioData.txt")
