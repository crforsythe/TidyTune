import requests
from bs4 import BeautifulSoup
import json
import re
def fetch_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Will raise an error for bad status codes
    return response.text

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    js_store_div = soup.find('div', class_='js-store')
    if js_store_div and 'data-content' in js_store_div.attrs:
        data_content = js_store_div['data-content']
        try:
            data_json = json.loads(data_content)
            # Now extract specific data from data_json
            # For example, lyrics or chords (depends on the structure of the JSON)
            cleanContent = pull_data(data_json)
            return cleanContent
        except json.JSONDecodeError:
            print("Error decoding JSON")
            return None
    else:
        print("Data div not found")
        return None

def pull_data(jsonDict):
    # Navigate through the dictionary to access the content
    tab_content = jsonDict.get("store", {}).get("page", {}).get("data", {}).get("tab_view", {}).get("wiki_tab", {}).get(
        "content", None)

    if tab_content:
        print("Tab Content Found.")
    else:
        print("Tab content not found")

    clean_content = clean_tab_content(tab_content)

    return clean_content

def transpose_chords(chords, semitones):
    # Convert semitones to an integer
    semitones = int(semitones)

    # Define a mapping of chord names and their transpositions
    chord_mapping = {
        'A': 0, 'A#': 1, 'Bb': 1, 'B': 2, 'C': 3, 'C#': 4, 'Db': 4,
        'D': 5, 'D#': 6, 'Eb': 6, 'E': 7, 'F': 8, 'F#': 9, 'Gb': 9,
        'G': 10, 'G#': 11, 'Ab': 11
    }

    transposed_chords = []
    for chord in chords:
        # Check if the chord is enclosed in [ch] tags
        if re.match(r'\[ch\](.*?)\[/ch\]', chord):
            chord_parts = re.split(r'(\[ch\].*?\[/ch\])', chord)
            transposed_parts = []
            for part in chord_parts:
                if part.startswith('[ch]') and part.endswith('[/ch]'):
                    # Transpose the chord part while maintaining modifiers
                    chord_text = re.match(r'\[ch\](.*?)\[/ch\]', part).group(1)
                    transposed_chord = []
                    for chord_token in re.findall(r'[A-Ga-g#b]+|[^\sA-Ga-g#b]+', chord_text):
                        if re.match(r'[A-Ga-g]+', chord_token):
                            chord_name = chord_token
                            modifier = ''
                            while chord_token[len(chord_name):] != '':
                                modifier += chord_token[len(chord_name)]
                                chord_token = chord_token[len(chord_name):]
                            if chord_name in chord_mapping:
                                transposed_index = (chord_mapping[chord_name] + semitones) % 12
                                transposed_chord_name = [k for k, v in chord_mapping.items() if v == transposed_index][0]
                                transposed_chord.append(transposed_chord_name + modifier)
                            else:
                                transposed_chord.append(chord_name + modifier)
                        else:
                            transposed_chord.append(chord_token)
                    transposed_part = ''.join(transposed_chord)
                    part = f'[ch]{transposed_part}[/ch]'
                transposed_parts.append(part)
            transposed_chord = ''.join(transposed_parts)
            transposed_chords.append(transposed_chord)
        else:
            # If the chord is not enclosed in [ch] tags, add it as is
            transposed_chords.append(chord)

    return transposed_chords


def clean_tab_content(tab_content, transpose_semitones=0):
    # Remove [tab] and [/tab] tags
    cleaned_content = re.sub(r'\[/?tab\]', '', tab_content)

    # Optionally, remove [Intro], [Verse], [Outro] and other similar tags if desired
    # cleaned_content = re.sub(r'\[.*?\]', '', cleaned_content)

    # Split the content into lines and transpose the chords in each line
    lines = cleaned_content.split('\n')
    transposed_lines = []
    for line in lines:
        chords = line.split()
        transposed_chords = transpose_chords(chords, transpose_semitones)
        transposed_line = ' '.join(transposed_chords)
        # transposed_line = transposed_line.replace('[ch]', '')
        # transposed_line = transposed_line.replace('[/ch]', '')
        transposed_lines.append(transposed_line)

    return '\n'.join(transposed_lines)


def print_tab_from_url(url, transpose_semitones=0):
    try:
        html = fetch_page(url)
        soup = parse_page(html)
        # Debug: Print a specific part of the soup for easier reading
        # print(soup.title)  # For example, to check the title of the page
        soup_str = str(soup)  # Convert BeautifulSoup object to string
        soup_str = clean_tab_content(soup_str, transpose_semitones)  # Pass the transpose value as a string
        soup_str = soup_str.replace('[ch]', '')
        soup_str = soup_str.replace('[/ch]', '')
        return soup_str
    except requests.RequestException as e:
        print("Error fetching the page:", e)

def main():
    url = 'https://tabs.ultimate-guitar.com/tab/karen-dalton/something-on-your-mind-chords-732739'
    try:
        return print_tab_from_url(url, 2)  # Pass the transpose value as a parameter
    except requests.RequestException as e:
        print("Error fetching the page:", e)



if __name__=='__main__':
    a = main()
    print(a)