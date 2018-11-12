import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix

import implicit



fp_data = 'gdistances.csv'

pair_distances = pd.read_csv(fp_data)
pair_distances = pair_distances[["componentA","componentB","distance"]]

print(pair_distances)
print(pair_distances.iloc[1,0])
print(pair_distances.iloc[22821,1])
print(pair_distances.shape[0])  


#print(pair_distances.duplicated(subset=['componentA', 'componentB']))

#ilias=pair_distances.pivot(index='componentA', columns='componentB', values='distance')
#print(ilias	)

'''
#-----------------------------------------------------------------------
# Return a list of components from the csv
#-----------------------------------------------------------------------
def format_matrix(pair_distances):
		
		components = []

		# List 'components' is appended with each component of column 0 in first line and column 1 in second.		
		[components.append(pair_distances.iloc[i,0]) for i in range(pair_distances.shape[0])]
		[components.append(pair_distances.iloc[i,1]) for i in range(pair_distances.shape[0])]
		
		# Remove duplicates: Sets are unordered collections of distinct objects.
		components = list(set(components))
		return components

components = format_matrix(pair_distances)
'''


# Convert artists names into numerical IDs
pair_distances['componentA_id'] = pair_distances['componentA'].astype("category").cat.codes
pair_distances['componentB_id'] = pair_distances['componentB'].astype("category").cat.codes

print(pair_distances)

def format_matrix(pair_distances):
		
		componentsA = []
		componentsB = []
		distance = []

		# List 'components' is appended with each component of column 0 in first line and column 1 in second.		
		[componentsA.append(pair_distances.iloc[i,3]) for i in range(pair_distances.shape[0])]
		[componentsB.append(pair_distances.iloc[i,4]) for i in range(pair_distances.shape[0])]
		[distance.append(pair_distances.iloc[i,2]) for i in range(pair_distances.shape[0])]

		# Remove duplicates: Sets are unordered collections of distinct objects.
		#components = list(set(components))
		return componentsA, componentsB, distance

componentsA, componentsB, distance = format_matrix(pair_distances)
#print(componentsA)
#print(distance)

row = np.array(componentsA)
col = np.array(componentsB)
data = np.array(distance)
item_user_data=csr_matrix((data, (row, col)), shape=(len(componentsA), len(componentsB)))
print(item_user_data)

#-------------------------------------------

# initialize a model
model = implicit.als.AlternatingLeastSquares(factors=50)

#-------------------------------------------

# Calculate the confidence by multiplying it by our alpha value.
alpha_val = 40
data_conf = (item_user_data * alpha_val).astype('double')

#Fit the model
model.fit(data_conf)

#-------------------------------------------

# train the model on a sparse matrix of item/user/confidence weights
model.fit(data_conf)
'''
# recommend items for a user
userid=1

user_items = item_user_data.T.tocsr()
recommendations = model.recommend(userid, user_items)
print(recommendations)
'''


#---------------------
# FIND SIMILAR ITEMS
#---------------------

# Find the 20 most similar to precise/mysql
item_id = 95 #precise/mysql
n_similar = 20

# Use implicit to get similar items.
similar = model.similar_items(item_id, n_similar)

print(similar)

# Print the names of our most similar charms
for item in similar:
    idx, score = item
    print(pair_distances.componentB.loc[pair_distances.componentB_id == idx].iloc[0])


'''
# find related items
itemid=1
related = model.similar_items(itemid)
print(related)

'''
