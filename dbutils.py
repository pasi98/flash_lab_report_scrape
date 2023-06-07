import psycopg2
import psycopg2.extensions
from tika import parser
from PyPDF2 import PdfReader
import requests
import time
import pytesseract
from pdf2image import convert_from_path
import os
import json

#highlight found keywords
def highlight_words_starting_with(input_string, text):
    words = text.split()
    highlighted_words = [word for word in words if word.startswith(input_string)]
    
    for word in words:
        if word in highlighted_words:
            print('\033[1;32m' + word + '\033[0m', end=' ')  # Highlighted word in green
        else:
            print(word, end=' ')
    
    print('\n')


conn = psycopg2.connect(
    host="localhost",
    database="flash_one",
    user="postgres",
    password="tp980212"    
    )

cursor = conn.cursor()


query = "SELECT report_url FROM lab_order_reports ORDER BY id ASC;"

cursor.execute(query)    
    
result = cursor.fetchall()

data_list = list(result)

# print('report url :',data_list)


urls = [url[0] for url in data_list]
print('convert :',urls)
    

arr=[]
for url in urls:
    response = requests.get(url)
    with open('temp.pdf', 'wb') as file:
        file.write(response.content)

    images = convert_from_path('temp.pdf')
    text = ""

    for image in images:
        text += pytesseract.image_to_string(image)

    arr.append(text)  # Append the complete text for each PDF
        # print(text) 
    print('-----------------------------------------------------------------------------')


    os.remove('temp.pdf')  
    time.sleep(5)
        # print(arr)

for index, item in enumerate(arr, start=1):
    report_content = f'report_{item}'  # Dynamic content based on index
    query_after = "UPDATE public.lab_order_reports SET report_content=%s WHERE id=%s;"
    cursor.execute(query_after, (report_content, index))
    conn.commit()
 



while True:
    # Execute the query to retrieve the current row count
    cursor.execute("SELECT COUNT(*) FROM lab_order_reports;")
    current_row_count = cursor.fetchone()[0]

    # Sleep for a certain duration (e.g., 1 second)
    time.sleep(1)

    # Execute the query again to check for changes
    cursor.execute("SELECT COUNT(*) FROM lab_order_reports;")
    new_row_count = cursor.fetchone()[0]

    # Compare the row counts to detect an increase
    if new_row_count > current_row_count:
        # New row detected
        # Perform your desired select query for the new row
        query2 = "SELECT report_url FROM lab_order_reports ORDER BY id DESC LIMIT 1;"
        cursor.execute(query2)

        result = cursor.fetchall()

        data_list = list(result)

# print('report url :',data_list)


        urls = [url[0] for url in data_list]
        print('convert :',urls)
    

        arr_new=[]
        for url in urls:
            response = requests.get(url)
            with open('temp.pdf', 'wb') as file:
                file.write(response.content)

            images = convert_from_path('temp.pdf')
            text = ""

            for image in images:
                text += pytesseract.image_to_string(image)

            arr_new.append(text)  # Append the complete text for each PDF
        # print(text) 
            print('-----------------------------------------------------------------------------')


            os.remove('temp.pdf')  
            time.sleep(5)
        
        print(arr_new)

        for i in arr_new:
                cursor.execute("SELECT * FROM lab_order_reports ORDER BY id DESC LIMIT 1")
                last_row = cursor.fetchone()
                last_row_id = last_row[0]

                new_value = i 
                cursor.execute("UPDATE lab_order_reports SET report_content = %s WHERE id = %s", (new_value, last_row_id))
  
                conn.commit()
        print('done')
        
    query_wanted = "SELECT order_id,report_content FROM lab_order_reports"     
    cursor.execute(query_wanted)
    wanted =cursor.fetchall()

    wanted_dict = {'wanted': wanted}
    # print(wanted_dict)
    with open('wanted.json', 'w') as file:
        json.dump(wanted_dict, file)
    # print(wanted)
    # break


