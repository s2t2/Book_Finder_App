import operator
import csv
import requests
import json

list_names = "https://api.nytimes.com/svc/books/v3/lists/names.json?api-key=za7DPypRNtsNzAW8VGweJEJW6EHJJZSG"
api_url = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key=za7DPypRNtsNzAW8VGweJEJW6EHJJZSG"
def get_products(api_url):
    request_url = api_url
    response = requests.get(request_url)
    return json.loads(response.text)

def parse_json(api_url):
    response = requests.get(api_url)
    response_data = json.loads(response.text)
    return response_data

def read_date(date):
    date = str(date)
    day = date[-2:]
    if '0' in day:
        day = date[-1:]
    year = date[0: 4]
    month = date[5: 7]
    month_table = {'01':'Janurary', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June', '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}
    month_name = month_table[month]
    return f"{month_name} {day}, {year}"

get_products(list_names)
nyt_list = parse_json(list_names)

nyt_list_names = []
nyt_list_info = {}
nyt_list_dict = {}
for item in nyt_list['results']:
    list_name = item['list_name']
    list_name_nyt = item['list_name_encoded']
    last_date = item['newest_published_date']
    last_updated = item['updated']
    string = f"List Name: {list_name}\nUpdated on: {last_date} Updated {last_updated}"
    nyt_list_names.append(list_name)
    nyt_list_dict[list_name] = list_name_nyt
    readable_date = read_date(last_date)
    nyt_list_info[item['list_name']] = f"The best seller list for {list_name} was last updated on {readable_date} and is typically updated {last_updated.lower()}."


#Print welcoming message to user with a description of the app
print("               ")
print("Welcome to the Book Finder!\nIn this app you'll be able to search for a book by genre, browse best seller lists, and book purchasing options.\nAll in one place." )
#For this app you can indicate book genre, and we'll pull best selling from the NYT
print("               ")
prompt = "When you're ready to being, press enter.."
begin = input(prompt)
print("               ")
print("Let's browse New York Times Best Seller Lists to find a book!")
print("               ")


#Allow the user to see what genres are available
#Prompt the user for book genre
#Print thank you, and print the genre selected
genre = ''
def list_browse():
    global genre
    global nyt_list_data_adj
    while True:
        print("               ")
        prompt1 = "Enter in the genre of best seller list you want to browse (ex. 'Hardcover Fiction').\nIf you want to see a complete list of genres, enter 'show me'.\nEnter here: "
        genre = input(prompt1)
        if genre == 'show me' or genre == 'Show me' or genre == 'SHOW ME':
            for lis in nyt_list_names:
                print(lis)
        elif genre in nyt_list_names:
            print("               ")
            print("We found a matching genre!")
            print(nyt_list_info[genre])
            print("        ")
            print(f"The New York Times Top 5 Best Selling {genre} Books: ")
            print("        ")
            url_list = nyt_list_dict[genre]
            list_data_url = f"https://api.nytimes.com/svc/books/v3/lists/current/{url_list}.json?api-key=za7DPypRNtsNzAW8VGweJEJW6EHJJZSG"
            nyt_list_data = parse_json(list_data_url)
            nyt_list_data_adj = nyt_list_data['results']['books']
            break
        else:
            print("               ")
            print("We couldn't find a matching genre! Please try again")

list_browse()

#From NYT API, return a top 5 list of the best selling books within that genre for that timeframe

book_list = {}
read_list = {}

def add_books_to_list(author):
    prompt5 = "Would you like to add a book to your Read List?\nIf no, enter 'no. If yes, enter 'yes'.\nEnter here: "
    read_book = input(prompt5)
    if read_book == 'no' or read_book == 'No' or read_book == 'NO':
        pass
    elif read_book == 'yes' or read_book == 'Yes' or read_book == 'YES':
        prompt6 = "Enter in the book title here: "
        book_add = input(prompt6)
        read_list[book_add] = author
        print("     ")
        print(f"{book_add} has been added!")
        print("     ")

def book_ranking():
    for book in nyt_list_data_adj:
        global book_list
        if book['rank'] <= 5:
            rank = book['rank']
            book_name = book['title']
            author = book['author']
            book_list[book_name] = author
            print(f"{rank}. {book_name}\nWritten by {author} ")
            print("      ")
        else:
            pass
    while True:
        add_books_to_list(author)
        print("     ")

        break


book_ranking()

#Ask the user if he/she wants to see a book description
def book_description():
    for book in nyt_list_data_adj:
        if browse_or_read == book['title']:
            desc = book['description']
            print("      ")
            print(f"DESCRIPTON: {desc}")
            print("      ")
        else:
            pass

while True:
    global browse_or_read
    print("More Actions Below:")
    print("       ")
    prompt2 = "Would you like to see the description of a book to learn more? If so, enter the title of the book (ex. 'SULLY').\nIf you want to browse other book lists, enter 'browse'!\nIf you want to be just continue, type 'pass'.\nEnter here: "
    browse_or_read = input(prompt2)
    print("      ")
    if browse_or_read =='browse' or browse_or_read == 'Browse' or browse_or_read == 'BROWSE':
        list_browse()
        book_ranking()
    elif browse_or_read == 'pass' or browse_or_read == 'pass' or browse_or_read == 'pass':
        break
    elif browse_or_read in book_list:
        book_description()
        break

def print_desc(get):
    amz = get['search_results']
    for a in amz:
        try:
            if a['position'] < 4:
                title = a['title']
                print("      ")
                print(title)
                link = "       Navigate to Link: "+ a['link']
                rating = "Average Rating: "+ str(a['rating'])
                print(rating)
                kindle = ''
                kindle_price = ''
                paperback = ''
                paperback_price = ''
                price_name = [price['name'] for price in a['prices']]
                prices = []
                for price in a['prices']:
                    if price['name'] == 'Kindle':
                        kindle = "    Available for Kindle"
                        kindle_price = "        Kindle Price: "+ price['raw']
                        print(kindle)
                        print(kindle_price)
                    if price['name'] == 'Paperback':
                        paperback = "    Available in Paperback"
                        paperback_price = "       Paperback Price: "+ price['raw']
                        print(paperback)
                        print(paperback_price)
                    if "Kindle" and "Paperback" not in price_name:
                        prices.append(price)
                    else:
                        pass
                try:
                    print("    Price: " + prices[0]['raw'])
                except IndexError:
                    pass
                if a['is_prime'] == True:
                    is_prime = '    Amazon Prime Eligible'
                    print(is_prime)
                else:
                    pass
                print(link)
                print("     ")
        except KeyError:
            print("    Prices not available.")
            print(link)

def search_books():
    while browse_or_read != 'done':
        prompt3 = "Would you like to search any book title on Amazon.com?\nIf so, enter 'search'.\nIf you would like to be done enter 'done'.\nIF you would like to continue to browse, enter 'browse'.\nEnter here: "
        print("       ")
        search_book = input(prompt3)
        print("       ")
        if search_book == 'browse' or search_book == 'Browse' or search_book == "BROWSE":
            list_browse()
            book_ranking()
            break
        elif search_book == 'done' or search_book == 'Done' or search_book == 'DONE':
            print("               ")
            if read_list:
                print("Read List:")
                for read in read_list:
                    print(f"{read}, written by {read_list[read]}.")
                print("               ")
                print("We're done finding books! Keep on reading!")
                break
            else:
                print("               ")
                print("We're done finding books! Keep on reading!")
                break
        elif search_book == 'search' or search_book == 'Search' or search_book == 'SEARCH':
            prompt5 = "Enter Book Title here: "
            search_book_title = input(prompt5)
            prompt4 = "Enter Book Author here: "
            search_book_author = input(prompt4)
            search_book_title = search_book_title.replace(" ", "+")
            search_book_author = search_book_author.replace(" ", "+")
            search_term = f"{search_book_title}+{search_book_author}"
            amazon_url = f"https://api.rainforestapi.com/request?api_key=AB2B43542B3C49B2A94D5D80E0B6096C&type=search&amazon_domain=amazon.com&search_term={search_term}"
            get= get_products(amazon_url)
            print_desc(get)
            break

search_books()

def final_prompt():
    print("     ")
    prompt_final = ("Would you like to search another book?\nIf so type 'yes', if no type 'done.\nEnter here: ")
    final = input(prompt_final)
    if final == 'yes' or final == 'Yes' or final == 'YES':
        search_books()
    else:
        print("      ")
        print("Thank you for using the book finder app! Have a great day!")


final_prompt()

#Ask the user if he/she wants to see the book on amazon


#Ask the user if he/she wants to see the book on amazon

#From Amazon API, pull in price and kindle format data
#If not on Amazon, print statement saying that not available on Amazon

#If possible, print the URL for purchase for all items on the list
