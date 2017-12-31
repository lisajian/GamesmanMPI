conda install --yes --file requirements.txt

while read requirement; do conda install --yes $requirement; done < requirements.txt || pip install $requirement; done < requirements.txt

# credits to Till Hoffmann, stack overflow
