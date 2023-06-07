import requests
from PyPDF2 import PdfReader
import os
import pytesseract
from pdf2image import convert_from_path
import time

urls = [
    'https://flash-prod.s3.ap-south-1.amazonaws.com/reports/32c2fe474d6e63496bbcac829cfc5bf0.pdf'

]

input_words = input("Enter the first few words: ")
start_time = time.time()


def highlight_words_starting_with(input_string, text):
    words = text.split()
    highlighted_words = [word for word in words if word.startswith(input_string)]
    
    for word in words:
        if word in highlighted_words:
            print('\033[1;32m' + word + '\033[0m', end=' ')  # Highlighted word in green
        else:
            print(word, end=' ')
    
    print('\n')


for url in urls:
    response = requests.get(url)
    with open('temp.pdf', 'wb') as file:
        file.write(response.content)

    with open('temp.pdf', 'rb') as file:
        images = convert_from_path('temp.pdf')
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        highlight_words_starting_with(input_words, text)
        # print(text)   
        print('------------------------------------------------------------') 



    # Delete the temporary PDF file
    os.remove('temp.pdf')

end_time = time.time()

execution_time = end_time - start_time

print("Execution time:", execution_time, "seconds")
