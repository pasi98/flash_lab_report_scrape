import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def highlight_words_starting_with(input_string, text):
    words = text[1].split()
    value = text[0]
    input_string_lower = input_string.lower()  # Convert input_string to lowercase
    highlighted_words = [word for word in words if word.lower().startswith(input_string_lower)]  # Convert word to lowercase for comparison

    if len(highlighted_words) > 0:
        highlighted_text = ''
        for word in words:
            if word in highlighted_words:
                highlighted_text += '\033[1;32m' + word + '\033[0m '  # Highlighted word in green
            else:
                highlighted_text += word + ' '
        highlighted_text += '\n'
        return str(value) #+ ' - ' + highlighted_text --if want text
    # else:
    #     return "No matching words found.\n"

@app.route('/highlight', methods=['POST'])
def highlight():
    data = request.get_json()
    input_string = data['input_string']
    
    with open('wanted.json', 'r') as file:
        wanted_data = json.load(file)
        wanted = wanted_data['wanted']

    results = []
    for i in wanted:
        highlighted_text = highlight_words_starting_with(input_string, i)
        if highlighted_text is not None:
            results.append(highlighted_text)
    
    return jsonify(results)


if __name__ == '__main__':
    app.run()
