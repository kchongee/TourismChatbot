import requests
import re
import pandas as pd
import html
import time 

# places_df = pd.read_csv('tourist_places.csv').fillna('')
# places_dict_list = places_df.to_dict('records')
# print(len(places_dict_list))
# places_dict_list = places_dict_list[12:]
# print(len(places_dict_list))
# print(places_dict_list[0])

# faqs_df = pd.read_csv('faqs.csv',index_col=False).fillna('')
# faqs_df = faqs_df.iloc[:,1:]
# faqs_df.to_csv('faqs.csv',index=False)


# index_stopped = 0
# with open('index_stopped.txt', 'r') as f:
#     txt = f.read()
#     print(txt)
#     print(type(txt))
#     index_stopped = int(txt) if txt else index_stopped
#     print(index_stopped)
#     print(type(index_stopped))

# with open('index_stopped.txt', 'w') as f:
#     f.write('0,0')

# with open('index_stopped.txt', 'r') as f:
#     txt = f.read()
#     if txt:
#         list = txt.split(',')
#         query_index_stopped = int(list[0])
#         place_index_stopped = int(list[1])
#         print(list)
#         print(query_index_stopped)
#         print(place_index_stopped)