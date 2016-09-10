import json
from time import sleep

from piazza_api import Piazza

import config

username = config.username
password = config.password
class_id = 'is0q8vy2dsm6yx'
p = Piazza()
p.user_login(email=username, password=password)
cis121 = p.network(class_id)

# get the total number of posts
stats = cis121.get_statistics()
# get it using the daily posts in the statistics page
total_num_posts = sum(d['questions'] for d in stats['daily'])

# now load the "class database"
try: 
    with open(config.LOCAL_DATA_FILE_NAME, 'r') as data_file:
        try:
            current_data = json.load(data_file)
        except ValueError: # empty file
            current_data = {}
except IOError: #file didn't exist
    current_data = {}

counter = 0
limit = 10
for post_number in range(1, total_num_posts):
    encoded_post_number = str(post_number).encode('utf-8')
    if counter > limit:
        sleep(10) # avoid rate limits
        counter = 0
    if encoded_post_number not in current_data:
        print post_number
        current_data[encoded_post_number] = cis121.get_post(post_number)
        counter +=1 


with open(config.LOCAL_DATA_FILE_NAME, 'w') as data_file:
    json.dump(current_data, data_file)
