import requests
from bs4 import BeautifulSoup
import json
import re

def construct_search_url(song_title, page_number=1):
    base_url = "https://www.ultimate-guitar.com/search.php"
    params = {
        "search_type": "title",
        "value": song_title,
        "page": page_number
    }
    query_string = "&".join([f"{key}={str(value).replace(' ', '%20')}" for key, value in params.items()])
    return f"{base_url}?{query_string}"



def fetch_search_results(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div with the 'data-content' attribute
    data_div = soup.find('div', {'class': 'js-store'})

    # Check if data_div exists and has 'data-content'
    if data_div and 'data-content' in data_div.attrs:
        # Extract and parse the JSON content
        json_data = json.loads(data_div['data-content'])

        # Extract the search results
        results = json_data['store']['page']['data']['results']

        # Filter results to include only those with "chord" in the type
        chord_results = [result for result in results if 'type' in result and "chord" in result['type'].lower()]

        # Sort results by rating (descending), placing unrated results at the end
        sorted_chord_results = sorted(chord_results, key=lambda x: (x['rating'] is None, x['rating']), reverse=True)

        # Return structured results
        return [{
            "title": result['song_name'],
            "artist": result['artist_name'],
            "type": result['type'],
            "rating": result['rating'],
            "tab_url": result['tab_url']
        } for result in sorted_chord_results]
    else:
        return "No results found or unable to parse results."


def search_by_keyword(song_title, page_number=1):
    search_url = construct_search_url(song_title, page_number=page_number)
    search_results = fetch_search_results(search_url)
    return search_results

if __name__=='__main__':
    # Example usage:
    song_title = "bob dylan"
    search_results = search_by_keyword(song_title)

    for result in search_results:
        print(f"Title: {result['title']}")
        print(f"Artist: {result['artist']}")
        print(f"Type: {result['type']}")
        print(f"Rating: {result['rating']}")
        print(f"Tab URL: {result['tab_url']}\n")
