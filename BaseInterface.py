from BaseSearcher import search_by_keyword
from BaseViewer import print_tab_from_url
def pretty_print_result(result):
    rating = "Unrated" if result['rating'] is None else f"Rating: {result['rating']:.2f}"
    return f"{result['title']} - {result['artist']}; {rating}; Type: {result['type']}"

def identify_search_string():
    search_string = input("Enter the title of the song you want to search for: ")
    return search_string

def get_user_choice(num_results):
    print("\nCommands:")
    print("'exit' - Exit the application")
    print("'search' - Perform a new search")
    print("'prev' - Look at previous page's results")
    print("'next' - Look at next page's results")
    print("Enter the number of the tab you want to view.")

    while True:
        user_input = input("\nEnter command or choice: ").lower()

        if user_input == 'exit':
            return 'exit'
        elif user_input == 'search':
            return 'search'
        elif user_input == 'prev':
            return 'prev_page'
        elif user_input == 'next':
            return 'next_page'
        elif user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= num_results:
                return choice
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Invalid input. Please enter a valid command or a number.")

def search_and_display_results():
    page_number = 1
    search_string = identify_search_string()
    search_results = search_by_keyword(search_string, page_number=page_number)

    while True:
        if search_results:
            print("\nSearch Results:\n")
            for i, result in enumerate(search_results, start=1):
                print(f"{i}. {pretty_print_result(result)}")

            choice = get_user_choice(len(search_results))

            if choice == 'exit':
                print("Exiting...")
                selected_tab = None
                break
            elif choice == 'search':
                search_string = identify_search_string()
                search_results = search_by_keyword(search_string, page_number=page_number)
                selected_tab = None
            elif choice == 'next_page':
                page_number += 1
                search_results = search_by_keyword(search_string, page_number=page_number)
                if (search_results == []):
                    page_number -= 1
                    search_results = search_by_keyword(search_string, page_number=page_number)
                print(search_results)
                selected_tab = None
            elif choice == 'prev_page':
                page_number = max(1, page_number - 1)
                search_results = search_by_keyword(search_string, page_number=page_number)
                if(search_results==[]):
                    page_number+=1
                    search_results = search_by_keyword(search_string, page_number=page_number)
                print(search_results)
                selected_tab = None
            else:
                selected_tab = search_results[choice - 1]

            print(selected_tab)
            if(selected_tab!=None):
                print("\nSelected Tab:\n")
                print(pretty_print_result(selected_tab))
                print(f"Tab URL: {selected_tab['tab_url']}\n")

                print_full_tab = input("Would you like to print the full tab? (yes/no): ").lower()
                if print_full_tab == 'yes':
                    # Function to print the full tab goes here
                    print_tab_from_url(selected_tab['tab_url'])
                    # Call the function to fetch and display the full tab here
                    input("Press Enter to return to the search results...")  # Pauses the program
                else:
                    print("Returning to search results...")
        else:
            print("No results found for your search. Exiting...")
            break


if __name__ == '__main__':
    search_and_display_results()

# # Example usage of the CLI function
# search_and_display_results()
#
# #     print(f"Rating: {result['rating']}")
# #     print(f"Tab URL: {result['tab_url']}\n")