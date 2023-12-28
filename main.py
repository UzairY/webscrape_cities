import requests
from bs4 import BeautifulSoup
import json

# This function returns json object of all the towns in a city
def scrape_town(city_name,country_name):
    city_url = f"https://www.worldcitydb.com/{city_name}_in_{country_name}_state"
    response = requests.get(city_url,verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Replace this selector with the actual one for city elements
        towns = soup.find_all('a', class_='link')   # Selector for city elements
        temp = []
        for town in towns:
            town_name = town.get_text().strip()
            temp.append(town_name)
    return temp

# This function updates the main dictionary object with a city (key) and calls the scrape_town (value) fucntion 
def scrape_cities(country_url,country_name):
    response = requests.get(country_url,verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Replace this selector with the actual one for city elements
        cities = soup.find_all('a', class_='link')   # Selector for city elements
        
        temp = {}
        # Extract city information
        for city in cities:
            city_name = city.get_text()  # Get city name
            # Additional scraping logic for city details if needed
            towns = scrape_town(city_name,country_name)
            # Process or store city information as required
            # print(city_name)  # For demonstration, printing city names
            temp.update({city_name: towns})
    main_dict.update({country_name: temp})


# Main scraping process to get country names
def scrape_countries(main_url):
    response = requests.get(main_url,verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Replace this selector with the actual one for country links
        countries = soup.find_all('a', class_='link')  # Selector for country links
        
        # Extracting and processing country names and their respective URLs
        for country in countries:
            country_name = country.get_text()
            country_link = country['href']
            country_url = f"https://www.worldcitydb.com/{country_link}"  # Full country URL
            scrape_cities(country_url,country_name)
    # print(main_dict)
if __name__ == "__main__":
    main_url = 'https://www.worldcitydb.com/search-by-country?lang=en_US'  # Replace with the main page URL
    main_dict = {}
    scrape_countries(main_url)
    with open('places.txt', 'w') as file:
        file.write(json.dumps(main_dict))