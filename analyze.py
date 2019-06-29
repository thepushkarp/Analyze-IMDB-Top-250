import sys
import requests
from bs4 import BeautifulSoup as bs

movieNames = [] # Movie Names
dates = [] # Release Dates
genres = [] # Movie Genres
imdbRatings = [] # IMDB Ratings
metascores = [] # Metascores

url = 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=1&ref_=adv_nxt'
for i in range(1, 201 + 1, 50):
	splitUrl = url.split('=')
	splitUrl[3] = f'{i}&ref_'
	url = '='.join(splitUrl)

	try:
		response = requests.get(url)
		response.raise_for_status()
	except requests.exceptions.RequestException as excep:
		print(f'\nThere was a problem:\n{excep}')
		sys.exit()

	imdbSoup = bs(response.text, 'lxml')
	movieContainers = imdbSoup.find_all('div', class_ = 'lister-item mode-advanced')

	for container in movieContainers:
		# name
		name = container.h3.a.text
		movieNames.append(name)

		# release date
		date = container.h3.find('span', class_ = 'lister-item-year').text
		dates.append(date.strip('()'))

		# genre
		genre = container.p.find('span', class_ = 'genre').text.strip('\n')
		genres.append(genre)

		# rating
		rating = container.strong.text
		imdbRatings.append(float(rating))

		# metascore
		metascore = container.find('span', class_ = 'metascore favorable')
		if metascore is not None:
			metascores.append(int(metascore.text))
		else:
			metascores.append('No Metascore')
