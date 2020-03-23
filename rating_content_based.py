#!/usr/bin/env python3
#cosine similarity in prev project
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# Get the data 
path = 'movie_metadata.csv'
df = pd.read_csv(path) 

column_names= ['movie_title','genres','director_name','content_rating','imdb_score','plot_keywords','actor_2_name','actor_1_name']
movie= df[column_names].copy() #for content based
movie=movie.drop('content_rating',axis=1)
column_names1=['movie_title','imdb_score'] #for rating based 
movie1= df[column_names1].copy()


def strip(row):
    s= row['movie_title']
    s=s.replace(u'\xa0',u' ')  # removing encoding
    while( len(s)>1 and s[-1] ==' '):
        s= s[0:-1]
    return str(s)
movie['movie_title']= movie.apply(strip,axis=1)

#add column index
count_row = movie.shape[0] 
cc= [x for x in range(count_row)]
movie['index']=cc
movie1['index']=cc

#handle missing values
column_names= list(movie)
for c in column_names:
    movie[c]=movie[c].fillna('')
column_names1= list(movie1)
for c in column_names1:
    movie1[c]=movie1[c].fillna('')    

#spliting genres for content based 
def split_genre(row):
    s=''
    a= row['genres'].split('|')
    for k in a:
        s+= str(k)
        s+=' '  
    return s
movie['genres']= movie.apply(split_genre,axis=1)
    
#combing all the fields
comb= 'combined'

def combining_funct(row):
    s=''
    for c in column_names:
       if c != 'content_rating' and c!= 'index' and c!= 'imdb_score':
        s+=str(row[c])
        s+=' '
    return s

movie[comb]= movie.apply(combining_funct, axis=1)

#content based
## vectorisation
cv = CountVectorizer() #creating new CountVectorizer() object
count_matrix = cv.fit_transform(movie[comb])

##cosine similarity
cosine_sim = cosine_similarity(count_matrix)

def get_title_from_index(index):
    return movie[movie.index==index]['movie_title'].values[0]

def get_index_from_title(title):
   return movie[movie.movie_title == title]['index'].values[0]

#taking movie from user 
m= input("Enter a movie ")

movie_index = get_index_from_title(m)
similar_movies = list(enumerate(cosine_sim[movie_index]))
sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:] 


#rating based 
#computing distance between two movies 
def ComputeDistance(a, b):
    knndist = abs(a-b)
    return  knndist    
    
#fetching k neighbours
def getNeighbors(movieID, K):
    distances = []
    for id in range(count_row):
        if id != movieID :
            dist = ComputeDistance(movie1.iloc[movieID][1], movie1.iloc[id][1])
            distances.append((id, dist))
    distances.sort(key=lambda elem: elem[1])
    neighbors = []
    for x in range(K):
        neighbors.append(distances[x][0])
    return neighbors

K = 5
neighbors = getNeighbors(movie_index, K) 

#showing output such that common movies to content & rating are displayed first ,followed by content based 
common=[]
for element in sorted_similar_movies:
    for neighbor in neighbors:
        if(movie1.iloc[neighbor][0]== get_title_from_index(element[0])):
            common.append(movie1.iloc[neighbor][0])
        
length = len(common)        
if length ==0:            
    i=0
    print("\nTop 5 similar movies to",m, "are:\n")
    for element in sorted_similar_movies:
         print(get_title_from_index(element[0]))
         i=i+1
         if i>5:
            break  
else:
    i= length
    for c in common:
        print(c)   
    for element in sorted_similar_movies:
        flag=0
        mov= get_title_from_index(element[0])
        for c in common:
            if c==mov :
                flag=1
                break
        if flag==0:
           print(get_title_from_index(element[0]))
           i=i+1
           if i>5:
             break
  
    
    