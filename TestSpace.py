
import pickle

Email_list = [['Ramsook@arizona.edu', 'Ryan'], ['panchobowz@gmail.com' , 'Ryan'],['alyssamagee@arizona.edu', 'Alyssa'],['nthomp1@arizona.edu' , 'Nathan'], 
['emily.lu1054@gmail.com', 'Emily'], ['summerblunk@arizona.edu', 'Summer'], ['elianaefife@gmail.com','Eliana'],['susanforce1111@outlook.com','Susan'],
['aarvayo0701@gmail.com','Angel'], ['joneichenberg@gmail.com','Johnny']]


with open('Email_list.pickle', 'wb') as f:
    pickle.dump(Email_list, f)

# with open('Email_list.pickle', 'rb') as r:
#    stuff = pickle.load(r)

