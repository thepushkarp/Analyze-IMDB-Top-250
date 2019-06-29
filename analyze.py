import sys
import time
from random import randint
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

movieNames = [] # Movie Names
years = [] # Release Years
genres = [] # Movie Genres
imdbRatings = [] # IMDB Ratings
metascores = [] # Metascores

#For monitoring request frequency
startTime = time.time()
reqNum = 0

print("Fetching Webpages...")

for i in range(1, 201 + 1, 50):
	url = ('https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=' + str(i) + '&ref_=adv_nxt')

	# Make a get request
	try:
		response = requests.get(url, headers = {"Accept-Language": "en-US, en;q=0.5"})
		response.raise_for_status()
	# Throw warning in case of errors
	except requests.exceptions.RequestException as excep:
		print(f'\nThere was a problem:\n{excep}')
		sys.exit()

	# Pause the loop
	time.sleep(randint(1,4))

	# Monitor the request frequency
	reqNum += 1
	elapsedTime = time.time() - startTime
	print(f"Request: {reqNum}; Frequency: {reqNum/elapsedTime:.6f} requests/s")

	# Parse the HTML Contents
	imdbSoup = bs(response.text, 'lxml')
	movieContainers = imdbSoup.find_all('div', class_ = 'lister-item mode-advanced')

	for container in movieContainers:

		# Movie Name
		name = container.h3.a.text
		movieNames.append(name)

		# Release Year
		year = container.h3.find('span', class_ = 'lister-item-year').text
		years.append(int(year[-5:-1]))

		# Movie Genre
		genre = container.p.find('span', class_ = 'genre').text.strip('\n').strip()
		genres.append(genre.split(', '))

		# IMDB Rating
		rating = container.strong.text
		imdbRatings.append(float(rating))

		# Metascore
		metascore = container.find('span', class_ = 'metascore favorable')
		if metascore is not None:
			metascores.append(int(metascore.text))
		else:
			metascores.append(None)

print()

# Create DataFrame of Movie Data
movieRatings = pd.DataFrame({
'Movie': movieNames,
'Year': years,
'Genre': genres,
'IMDB Rating': imdbRatings,
'Metascore': metascores,
'Normalised IMDB Rating': (pd.Series(imdbRatings)*10).tolist()
})

# Export data to .csv
movieRatings.to_csv('movieRatings.csv', encoding='utf-8')
print("Data Exported to movieRatings.csv")
