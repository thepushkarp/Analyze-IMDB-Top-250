import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd

# Read data from csv file
movieRatings = pd.read_csv('movieRatings.csv', header = 0)

# Add decade column to Movie Ratings DataFrame
movieRatings['Decade'] = ((movieRatings['Year']//10).astype(int)*10)

# Number of movies releasd and average IMDB Ratings segregated by decade
moviesByDecade = pd.DataFrame({
	'Decade' : movieRatings['Decade'].value_counts().index,
	'Movies' : movieRatings['Decade'].value_counts(),
	'Average IMDB Rating' : None
}).sort_values('Decade').reset_index(drop = True)

# Calculate Average IMDB Ratings
for i in range(len(moviesByDecade)):
	decadeFilter = movieRatings['Decade'] == moviesByDecade.iloc[i, 0]
	filteredMovies = movieRatings[decadeFilter]
	moviesByDecade.iloc[i, 2] = filteredMovies['IMDB Rating'].mean()

# Set of unique genres
genreList = set()

# List of genre for each movie
genres = []

# Add genres to genreList
for i in range(len(movieRatings)):
	genre = movieRatings.iloc[i, 2].strip('[]').split(', ')
	genre = [genreName.strip('\'') for genreName in genre]
	genres.append(genre)
	genreList.update(set(genre))

# Change Genre Column to list from string
movieRatings['Genre'] = pd.Series(genres)

# Number of movies segregated by Genre
moviesByGenre = pd.DataFrame({
	'Genres' : list(genreList),
	'Movies' : 0
})

# Add number of movies for each genre
for i in range(len(moviesByGenre)):
	for j in range(len(movieRatings)):
		if moviesByGenre.iloc[i, 0] in movieRatings.iloc[j, 2]:
			moviesByGenre.iloc[i, 1]+=1

# Plot movies by genre
moviesByGenre.plot(x = 'Genres', y = 'Movies', kind = 'bar', figsize=(17, 17), fontsize = 15)
plt.title('Number of movies in IMDB Top 250 by genre', fontsize=30)
plt.legend(['Number of movies'], fontsize = 15)
plt.xlabel('Genres', fontsize=20)
plt.ylabel('Number of movies', fontsize=20)
plt.savefig('genre.png')

# Plot movies by decade
moviesByDecade.plot(x = 'Decade', y = 'Movies', kind = 'bar', figsize=(17, 17), fontsize = 15)
plt.title('Number of movies in IMDB Top 250 by decade', fontsize=30)
plt.legend(['Number of movies'], fontsize = 15)
plt.xlabel('Decade', fontsize=20)
plt.ylabel('Number of movies', fontsize=20)
plt.savefig('decade.png')

# Plot average IMDB rating
moviesByDecade.plot(x = 'Decade', y = 'Average IMDB Rating', kind = 'line', figsize=(17, 17), fontsize = 15)
plt.title('Average IMDB ratings of IMDB Top 250 movies by decade', fontsize=30)
plt.legend(['Average IMDB rating'], fontsize = 15)
plt.xlabel('Decade', fontsize=20)
plt.ylabel('IMDB rating', fontsize=20)
plt.savefig('average.png')
