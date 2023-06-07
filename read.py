import psycopg2

# def highlight_words_starting_with(input_string, text):
#     words = text.split()
#     highlighted_words = [word for word in words if word == input_string]
    
    # if len(highlighted_words) > 0:  # Check if there are any highlighted words
    #     for word in words:
    #         if word in highlighted_words:
    #             print('\033[1;32m' + word + '\033[0m', end=' ')  # Highlighted word in green
    #         else:
    #             print(word, end=' ')
    # else:
    #     print("No matching words found.")
    
    # print('\n')

def highlight_words_starting_with(input_string, text):
    words = text.split()
    input_string_lower = input_string.lower()  # Convert input_string to lowercase
    highlighted_words = [word for word in words if word.lower().startswith(input_string_lower)]  # Convert word to lowercase for comparison
    if len(highlighted_words) > 0:
        for word in words:
            if word in highlighted_words:
                print('\033[1;32m' + word + '\033[0m', end=' ')  # Highlighted word in green
            else:
                print(word, end=' ')
        print('\n')
    else:
        print("No matching words found.\n")




    
conn = psycopg2.connect(
        host="localhost",
        database="flash_one",
        user="postgres",
        password="tp980212"    
    )

cursor = conn.cursor()

query2 = "SELECT id,report_content FROM lab_order_reports;"
cursor.execute(query2)

result2 = cursor.fetchall()

# data_list2 = list(result2)

# print(result2)
input_words = input("Enter the first few words: ")

    
for i in result2:
    text = i[1]
    highlight_words_starting_with(input_words, text)