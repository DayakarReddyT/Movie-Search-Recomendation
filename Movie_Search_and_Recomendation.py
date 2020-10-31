# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 14:02:10 2020

@author: Daya
"""


import pandas as pd
import numpy as np
import warnings
from mlxtend.preprocessing import TransactionEncoder

from tkinter import *
from tkinter import ttk,messagebox
import threading
import time
import random
from pandastable import Table



warnings.filterwarnings('ignore')


df=pd.read_csv("C:/Users/Daya/Desktop/Datasets/movie_metadata.csv")
drop_list=['color','aspect_ratio','facenumber_in_poster','gross','budget','director_facebook_likes',
           'content_rating','actor_3_facebook_likes','plot_keywords','cast_total_facebook_likes','actor_2_facebook_likes',
           'num_critic_for_reviews','actor_1_facebook_likes','num_user_for_reviews','movie_facebook_likes'
          ]

df.drop(drop_list,axis=1,inplace=True)
df.head()

# droping the movies without movie_title

df['movie_title'].dropna(inplace=True)



# Duration 

df['duration'].fillna(0,inplace=True)

# Data Cleaning

unknown_list=['actor_2_name','director_name','genres','actor_1_name','actor_3_name','language','country','movie_imdb_link']
zeros_list=['duration','num_voted_users','title_year']

for item in unknown_list:
    df[item].fillna('Not Available',inplace=True)

for item in zeros_list:
    
    df[item].fillna(0,inplace=True)
    df[item]=df[item].astype(int)

df['imdb_score'].fillna(0,inplace=True)
df['imdb_score']=df['imdb_score'].astype(float)


def split_genre(val):
        
    return val.split('|')
        

df['genres']=df['genres'].apply(split_genre)


all_genres=np.unique(df['genres'].sum())

# Actors 

actors=pd.concat([df['actor_1_name'],df['actor_2_name'],df['actor_3_name']],axis=0)
actors=actors.astype(str)
actors=actors.unique()
df['actors']=df['actor_1_name']+','+df['actor_2_name']+','+df['actor_3_name']

# Directors 

all_directors=df['director_name'].astype(str)
all_directors=all_directors.unique()

# Movies 

all_movies=df['movie_title'].astype(str)
for i in range(len(all_movies)):
    all_movies[i]=all_movies[i].replace('\xa0','')


    
######## Recomendation ###########

te=TransactionEncoder()

x=te.fit_transform(df['genres'])

x=pd.DataFrame(x,columns=te.columns_)

genres=x.astype(int)

genres.insert(0, "movie_title",df["movie_title"])

genres.set_index('movie_title')



def recomend_genre(gen):
    gen=genres[gen]
    
    similar=genres.corrwith(gen).sort_values(ascending=False)
    
    similar_genres=list(similar.index.values[:5])
    
    def check(x):
        for item in similar_genres:
            if(item in x):
                return True
        return False
    return df[df['genres'].apply(check)].sort_values(by='imdb_score',ascending=False)[:100]



movie=x.copy()
movie.head()
movie=movie.transpose()
movie.columns=df['movie_title']

def recomend_movies(title):
    
    title = movie[title+'\xa0']
    
    similar=movie.corrwith(title).sort_values(ascending=False)
    rec_movies=[]
    for item in similar.index.array:
        rec_movies.append(item.replace('\xa0',''))
    
    similar_movie=rec_movies.copy()
    
    
    def check(x):
        for item in similar_movie:
            if(item in x):
                return True
        return False
    
    return df[df['movie_title'].apply(check)].sort_values(by='imdb_score',ascending=False)[:100]




colors=open("C:/Users/Daya/Desktop/DataSets/colors.txt",'r').read().split(',')

data=[]
data_dir=[]
data_act=[]
data_genr=[]

empty_list=[]


movie_lstbox=''
director_lstbox=''
actor_lstbox=''
genre_lstbox=''


movie_initial=True
dir_initial=True
movie_present=True
dir_present=True

selected_movie=''
selected_director=''
selected_actor=''
slected_genre=''
selected_imdb=''

def movies_listbox():
    global movie_lstbox
    movie_lstbox=Listbox(frame,bd=0,height=8,highlightthickness=0,bg=cal_frames)
    movie_lstbox.grid(row=4,column=0,sticky=N+S+W+E,columnspan=4,rowspan=1,padx=10)
    movie_lstbox.bind('<<ListboxSelect>>', on_select)



def dir_listbox_creation():
    global director_lstbox
    director_lstbox=Listbox(frame,bd=0,height=8,highlightthickness=0,bg=cal_frames)
    director_lstbox.grid(row=4,column=1,sticky=W+E,columnspan=4,padx=10)
    director_lstbox.bind('<<ListboxSelect>>', dir_on_select)

    
def act_listbox_creation():
    global actor_lstbox
    actor_lstbox=Listbox(frame,bd=0,height=8,highlightthickness=0,bg=cal_frames)
    actor_lstbox.grid(row=4,column=2,sticky=W+E,columnspan=4,padx=10)
    actor_lstbox.bind('<<ListboxSelect>>', act_on_select)
 

def genr_listbox_creation():
    global genre_lstbox
    genre_lstbox=Listbox(frame,bd=0,height=8,highlightthickness=0,bg=cal_frames)
    genre_lstbox.grid(row=4,column=3,sticky=W+E,columnspan=4,padx=10)
    genre_lstbox.bind('<<ListboxSelect>>', genr_on_select)

    
    
def movie_list(var):
    
    global data,movie_lstbox 
    global director_lstbox
    global movie_present,dir_present,dir_initial,movie_initial
    
    movie_initial=False
    
    
    dir_listbox_update(empty_list)
    act_listbox_update(empty_list)    
    genr_listbox_update(empty_list)
    
    value=movie_ent.get()
    
    value=value.strip().lower()
    
    data=[]
    
    if(value==''):
        
        pass
    else:      
        for item in all_movies:
            if value in item.lower():
                data.append(item)
            
    listbox_update(data)
    

def dir_list(var):
    
    global data_dir,director_lstbox 
    global movie_lstbox
    global movie_present
    global dir_present,dir_initial
    
    dir_initial=False
        
    act_listbox_update(empty_list)
    listbox_update(empty_list)
    genr_listbox_update(empty_list)
    
    
    value=dir_ent.get()
    
    value=value.strip().lower()
    
    data_dir=[]
    
    if(value==''):
        
        pass
    else:      
        for item in all_directors:
            
            if value in item.lower():
                data_dir.append(item)
            
    dir_listbox_update(data_dir)
    

def act_list(var):
    
    global data_act,actor_lstbox 
    global movie_lstbox,director_lstbox
    global movie_present
    global dir_present,dir_initial
        
    dir_listbox_update(empty_list)    
    listbox_update(empty_list)
    genr_listbox_update(empty_list)
        
    
    
    value=act_ent.get()
    
    value=value.strip().lower()
    
    data_act=[]
    
    if(value==''):
        
        pass
    else:      
        for item in actors:
            
            if value in item.lower():
                data_act.append(item)
            
    act_listbox_update(data_act)
    

def genr_list(var):
    
    global data_genr,genre_lstbox 
    global movie_lstbox,director_lstbox,actor_lstbox
    global movie_present
    global dir_present,dir_initial
        
    dir_listbox_update(empty_list)
    act_listbox_update(empty_list)
    listbox_update(empty_list)
    
    
    
    
    value=genr_ent.get()
    
    value=value.strip().lower()
    
    data_genr=[]
    
    if(value==''):
        
        pass
    else:      
        for item in all_genres:
            if value in item.lower():
                data_genr.append(item)
            
    genr_listbox_update(data_genr)
    

def get_rating(var):
    global rating,movie_lstbox,director_lstbox,actor_lstbox,genre_lstbox
    global imdb_ent
       
    
    
    rating=imdb_ent.get()
    if(rating!=''):
        imdb_ent.delete(0,END)
        imdb_ent.insert(0,rating)
        if(float(rating)<0 or float(rating)>10):
            messagebox.showwarning('Warning','Rating should be between 1 and 10 ')
        print(rating)
    
def listbox_update(val):   
    
    
    movie_lstbox.delete(0,END)
    
    val=sorted(val,key=str.lower)
    
    for item in val:
        movie_lstbox.insert(END,item)
        

def dir_listbox_update(val):
    
    director_lstbox.delete(0,END)
    
    val=sorted(val,key=str.lower)
    
    for item in val:
        director_lstbox.insert(END,item)

        
        
def act_listbox_update(val):
    
    actor_lstbox.delete(0,END)
    
    val=sorted(val,key=str.lower)
    
    for item in val:
        actor_lstbox.insert(END,item)

  

def genr_listbox_update(val):
    
    genre_lstbox.delete(0,END)
    
    val=sorted(val,key=str.lower)
    
    for item in val:
        genre_lstbox.insert(END,item)



def on_select(event):
    
    global data
    global movie_present
    global movie_lstbox
    
    value=movie_lstbox.get(movie_lstbox.curselection())
    movie_ent.delete(0,END)
    movie_ent.insert(0,value.strip())    
    movie_lstbox.delete(0,END) 
     
    


    
def dir_on_select(event):   
    
    global data_dir
    global director_lstbox
    global dir_present    
    value=director_lstbox.get(director_lstbox.curselection())
    dir_ent.delete(0,END)
    dir_ent.insert(0,value.strip())    
    director_lstbox.delete(0,END) 
      
    
 
def act_on_select(event):   
    
    global data_act
    global actor_lstbox
    global dir_present
    
    value=actor_lstbox.get(actor_lstbox.curselection())
    act_ent.delete(0,END)
    act_ent.insert(0,value.strip())    
    actor_lstbox.delete(0,END)  
    
    
    
def genr_on_select(event):   
    
    global data_genr
    global genre_lstbox
    global dir_present
    
    value=genre_lstbox.get(genre_lstbox.curselection())
    genr_ent.delete(0,END)
    genr_ent.insert(0,value.strip())    
    genre_lstbox.delete(0,END)  
    
    
    
def movie_search():
    global rating,movie_lstbox,director_lstbox,actor_lstbox,genre_lstbox
    global imdb_ent
    
    selected_movie=movie_ent.get().strip().lower()
    selected_director=dir_ent.get().strip().lower()
    selected_actor=act_ent.get().strip().lower()
    selected_genre=genr_ent.get().strip()
    selected_imdb=imdb_ent.get().strip()
       
    
    
    
    result_df= df[['title_year','movie_title','director_name','actors','duration','imdb_score','genres','language','actor_1_name','actor_2_name','actor_3_name']].copy()
    result_df=result_df.sort_values(by='imdb_score',ascending=True)
    
        
    if(selected_movie!=''):
        result_df=result_df[result_df["movie_title"].str.lower().str.contains(selected_movie)].sort_values(by=['imdb_score'],ascending=True)
    
    if(selected_director!=''):
        result_df=result_df[result_df["director_name"].str.lower().str.contains(selected_director)].sort_values(by=['imdb_score'],ascending=True)
    
    if(selected_actor!=''):
        result_df=result_df[(result_df['actor_1_name'].str.lower()==selected_actor)
                            | (result_df['actor_2_name'].str.lower()==selected_actor ) 
                            | (result_df['actor_3_name'].str.lower()==selected_actor)].sort_values(by=['imdb_score'],ascending=True)
    
    if(selected_genre!=''):
        
        result_df=result_df[result_df['genres'].apply(lambda x: selected_genre in x)].sort_values(by=['imdb_score'],ascending=True)
        
    
    if(selected_imdb!=''):
        
        result_df=result_df[result_df["imdb_score"] > float(selected_imdb)].sort_values(by=['imdb_score'],ascending=True)
        
        
    result_df.reset_index(drop=True, inplace=True) 
    result_df['title_year'].astype(int,inplace=True)
    
    tp=Toplevel(root)
    
    tp.title('Results')
    
    tp.config(bd=3)
    cols = ['No','Year of Release','Movie Title ',' Director Name ',' Actors ',' Duration(mins) ',' Imdb Rating ',' Language ']
    no_of_results=range(0,len(result_df))
    result_df.insert(loc=0,column='no',value=no_of_results)
    
    result_df.drop(['genres','actor_1_name','actor_2_name','actor_3_name'],axis=1,inplace=True)
    cols_width=[70,110,200,150,300,130,130,150]
    tree = ttk.Treeview(tp,height=500)
    tree.pack(expand=1)
    
    tree.column("#0", width=0)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Cooper Black', 10))
    
    tree["columns"] = cols
    
    for i,wid in zip(cols,cols_width):
        tree.column(i, anchor="w",width=wid)
        tree.heading(i, text=i, anchor='w')
  
    for index, row in result_df.iterrows():
        
        tree.insert("",0,text=index,values=list(row))
        
        
        
    
        

        
    
    
    
root=Tk()
root.title("Movie Search & Recomendation")

root.geometry("1200x600+0+0")


Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
Grid.rowconfigure(root, 1, weight=1)
Grid.columnconfigure(root, 0, weight=1)
Grid.rowconfigure(root, 9, weight=1)
Grid.columnconfigure(root, 0, weight=1)

cal_frames='#41B3A3'


frame_title=Frame(root,bd=5,bg=cal_frames)
frame_title.grid(row=0,column=0,sticky=N+S+E+W,rowspan=1,columnspan=5)
Grid.rowconfigure(frame_title, 0, weight=1)
Grid.columnconfigure(frame_title, 0, weight=1)

# Search Frame

frame=Frame(root,highlightthickness=0,highlightbackground="skyblue",bg=cal_frames)
frame.grid(row=1,column=0,sticky=N+S+E+W,rowspan=8,columnspan=5)

# Recomend Frame 

frame_rec=Frame(root,highlightthickness=0,highlightbackground="red",bg=cal_frames)
frame_rec.grid(row=9,column=0,sticky=N+S+E+W,rowspan=16,columnspan=5)



# Extra Remove  #
#Grid.rowconfigure(frame_title, 0, weight=0)
#Grid.columnconfigure(frame_title, 0, weight=0)


for row_index in range(1,9):
    Grid.rowconfigure(frame, row_index, weight=1)
    for col_index in range(6):
        Grid.columnconfigure(frame, col_index, weight=1)


for row_index in range(9,17):
    Grid.rowconfigure(frame_rec, row_index, weight=1)
    for col_index in range(6):
        Grid.columnconfigure(frame_rec, col_index, weight=1)


# Welcome Label

lab1=Label(frame_title,text="Welcome to Box Office !! ", fg='black',font = ("Times New Roman", 40),height=2,bg=cal_frames)
lab1.grid(row=0,column=0)




# Movie Search 

mov_search_lab=Label(frame,text='Search a Movie',fg='white',font=('Courier New',30),bg=cal_frames)
mov_search_lab.grid(row=1,column=0,padx=10,pady=30,sticky=N+S+W,columnspan=3)




# Movies 

movie_lab=Label(frame,text="Movie Title ",font=('Consolas',12),bg=cal_frames)
movie_lab.grid(row=2,column=0,padx=10,sticky=E+W)

movie_ent=Entry(frame,width=20,bd=1,bg='Azure')
movie_ent.grid(row=3,column=0,padx=10,sticky=E+W)
movie_ent.bind('<KeyRelease>', movie_list)

movies_listbox()


#Directors

dir_lab=Label(frame,text="Director Name ",font=('Consolas',12),bg=cal_frames)
dir_lab.grid(row=2,column=1,padx=10,sticky=E+W)

dir_ent=Entry(frame,width=20,bd=1,bg='Azure')
dir_ent.grid(row=3,column=1,padx=10,sticky=E+W)
dir_ent.bind('<KeyRelease>', dir_list)

dir_listbox_creation()



# Actors 
act_lab=Label(frame,text="Actor Name ",font=('Consolas',12),bg=cal_frames)
act_lab.grid(row=2,column=2,padx=10,sticky=E+W)

act_ent=Entry(frame,width=20,bd=1,bg='Azure')
act_ent.grid(row=3,column=2,padx=10,sticky=E+W)
act_ent.bind('<KeyRelease>', act_list)

act_listbox_creation()



# Genres
genr_lab=Label(frame,text="Genre   ",font=('Consolas',12),bg=cal_frames)
genr_lab.grid(row=2,column=3,padx=10,sticky=E+W)

genr_ent=Entry(frame,width=20,bd=1,bg='Azure')
genr_ent.grid(row=3,column=3,padx=10,sticky=E+W)
genr_ent.bind('<KeyRelease>', genr_list)

genr_listbox_creation()


# Imdb score

imdb_lab=Label(frame,text="Imdb Rating >=",font=('Consolas',12),bg=cal_frames)
imdb_lab.grid(row=2,column=4,padx=10,sticky=E+W)

imdb_ent=Entry(frame,width=20,bd=1,bg='Azure')
imdb_ent.grid(row=3,column=4,padx=10,sticky=E+W)
imdb_ent.bind('<KeyRelease>', get_rating)


# Search Movie Label

search_lab=Button(frame,text="Search  ",font=('Bahnschrift',13),command=movie_search,bg='green',fg='ghostwhite',width=10,height=1)
search_lab.grid(row=3,column=5,padx=40,sticky=E+W,columnspan=4)











##############################################################################
#####################    FRAME 2       #######################################
##############################################################################


data_rec=[]
data_dir_rec=[]
data_act_rec=[]
data_genr_rec=[]


movie_rec_lstbox=''
director_rec_lstbox=''
actor_rec_lstbox=''
genre_rec_lstbox=''


movie_rec_initial=True
dir_rec_initial=True
movie_rec_present=True
dir_rec_present=True

def movies_rec_listbox():
    global movie_rec_lstbox
    movie_rec_lstbox=Listbox(frame_rec,bd=0,height=8,highlightthickness=0,bg=cal_frames)
    movie_rec_lstbox.grid(row=12,column=1,sticky=W+E,columnspan=4,padx=10)
    movie_rec_lstbox.bind('<<ListboxSelect>>', on_rec_select)




def genr_rec_listbox_creation():
    global genre_rec_lstbox
    genre_rec_lstbox=Listbox(frame_rec,bd=0,height=8,highlightthickness=0,bg=cal_frames)
    genre_rec_lstbox.grid(row=12,column=3,sticky=W+E,columnspan=4,padx=10)
    genre_rec_lstbox.bind('<<ListboxSelect>>', genr_rec_on_select)

    
    
def movie_rec_list(var):
    
    global data_rec,movie_rec_lstbox 
    global director_rec_lstbox
       
   
    
   
    genr_rec_listbox_update(empty_list)
    
    
    value=movie_rec_ent.get()
    
    value=value.strip().lower()
    
    data=[]
    
    if(value==''):
        
        pass
    else:      
        for item in all_movies:
            if value in item.lower():
                data.append(item)
            
    listbox_rec_update(data)
    


def genr_rec_list(var):
    
    global data_rec_genr,genre_rec_lstbox 
    global movie_rec_lstbox,director_rec_lstbox,actor_rec_lstbox
    
        
    listbox_rec_update(empty_list)
    
    
    
    
    value=genr_rec_ent.get()
    
    value=value.strip().lower()
    
    data_genr=[]
    
    if(value==''):
        
        pass
    else:      
        for item in all_genres:
            if value in item.lower():
                data_genr.append(item)
            
    genr_rec_listbox_update(data_genr)
    


def listbox_rec_update(val):   
    
    
    movie_rec_lstbox.delete(0,END)
    
    val=sorted(val,key=str.lower)
    
    for item in val:
        movie_rec_lstbox.insert(END,item)
        



def genr_rec_listbox_update(val):
    
    genre_rec_lstbox.delete(0,END)
    
    val=sorted(val,key=str.lower)
    
    for item in val:
        genre_rec_lstbox.insert(END,item)



def on_rec_select(event):
    
    global data_rec
    
    global movie_rec_lstbox
    
    value=movie_rec_lstbox.get(movie_rec_lstbox.curselection())
    movie_rec_ent.delete(0,END)
    movie_rec_ent.insert(0,value.strip())    
    movie_rec_lstbox.delete(0,END)  
    
    


    
    
def genr_rec_on_select(event):   
    
    global data_genr_rec
    global genre_rec_lstbox
   
    
    value=genre_rec_lstbox.get(genre_rec_lstbox.curselection())
    genr_rec_ent.delete(0,END)
    genr_rec_ent.insert(0,value.strip())    
    genre_rec_lstbox.delete(0,END)  
     

        
def recomend_movie():
    
    selected_movie=movie_rec_ent.get().strip()
    
    selected_genre=genr_rec_ent.get().strip()
    
    
    result_df=df.copy()
    
    if(selected_movie!='' and selected_genre !=''):
        messagebox.showwarning('Warning','Please Chose Any ONE , Either Movie or Genre')
        return 0
    elif(selected_movie !=''):
        result_df=recomend_movies(selected_movie)
    elif(selected_genre !=''):
        result_df=recomend_genre(selected_genre)
    else:
        messagebox.showwarning('Warning','Please Enter Input')
        return 0
    
    result_df=result_df[['title_year','movie_title','director_name','actors','duration','imdb_score','language']]
    
    
    tp=Toplevel(root)
    tp.title('Results')
    cols = ['No','Year of Release','Movie Title ',' Director Name ',' Actors ',' Duration(mins) ',' Imdb Rating ',' Language ']
    no_of_results=range(0,len(result_df))
    result_df.insert(loc=0,column='no',value=no_of_results)
    
    
    cols_width=[70,110,200,150,300,130,130,150]
    tree = ttk.Treeview(tp,height=5000)
    tree.pack(expand=1)
    tree.column("#0", width=0)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Cooper Black', 10))
    
    tree["columns"] = cols
    
    for i,wid in zip(cols,cols_width):
        tree.column(i, anchor="w",width=wid)
        tree.heading(i, text=i, anchor='w')
    
    for index, row in result_df.iterrows():
        tree.insert("",0,text=index,values=list(row))
    
    
    
    



# Movie Search 

mov_rec_lab=Label(frame_rec,text='Recomend a Movie ',fg='white',font=('Courier New',30),bg=cal_frames)
mov_rec_lab.grid(row=9,column=0,padx=10,pady=30,sticky=N+S+W,columnspan=4)

note_label=Label(frame_rec,text='*Choose any one',fg='red',bg=cal_frames)
note_label.grid(row=9,column=5,padx=30,pady=30,sticky=N+S+W,columnspan=2)

# Movies 

movie_rec_lab=Label(frame_rec,text="Movie Title ",font=('Consolas',12),bg=cal_frames)
movie_rec_lab.grid(row=10,column=1,padx=10,sticky=E+W)

movie_rec_ent=Entry(frame_rec,width=20,bd=1,bg='Azure')
movie_rec_ent.grid(row=11,column=1,padx=10,sticky=E+W)
movie_rec_ent.bind('<KeyRelease>', movie_rec_list)

movies_rec_listbox()




# Genres
genr_rec_lab=Label(frame_rec,text="Genre   ",font=('Consolas',12),bg=cal_frames)
genr_rec_lab.grid(row=10,column=3,padx=10,sticky=E+W)

genr_rec_ent=Entry(frame_rec,width=20,bd=1,bg='Azure')
genr_rec_ent.grid(row=11,column=3,padx=10,sticky=E+W)
genr_rec_ent.bind('<KeyRelease>', genr_rec_list)

genr_rec_listbox_creation()

search_rec_lab=Button(frame_rec,text="Recomend ",command=recomend_movie,font=('Bahnschrift',15),bg='green',fg='ghostwhite',width=10,height=1)
search_rec_lab.grid(row=11,column=5,padx=30,sticky=E+W)






def ran_col():
    return random.choice(colors)

def col_change():
    while(True):
        try:              
                  
            lab1.config(text='Welcome to Box Office !!',fg=random.choice(colors)) 
            time.sleep(4)
            
        except Exception as e :            
            continue
        

threading.Thread(target=col_change).start()

root.mainloop()