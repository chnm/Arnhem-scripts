# make all should run each of the .py scripts to prep the data.
# make clean should remove all the data files.
# make test should run the unit tests.

all : locations people postmarks

people : 
	poetry run python prep_people.py

locations : 
	poetry run python prep_locations.py

postmarks :
	poetry run python prep_postmarks.py

clean :
	rm -f data/locations.csv
	rm -f data/people.csv
	rm -f data/postmarks.csv

.PHONY : all clean
