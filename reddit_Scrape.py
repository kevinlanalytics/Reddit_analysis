#library import(used) in this code
import praw
import pandas as pd

# sign in credidential and channel to the subreddit topics
reddit = praw.Reddit(client_id="RsGMSJef1u3XEA",
                     client_secret="PLIY7TMy87SL453eL-G_mUTT7Fc",
                     user_agent="socialmedia_study")

#channel to subreddit pharmacyschool
subreddit= reddit.subreddit('PHARMACYSCHOOL')
con_SOP = subreddit.controversial("year")

#define the comment dictionary for data mapping
comment_dict = { "title":[],
                "parent_id":[],
                "comment_id":[],
                "comment_body":[]}

#scrape the comments with matching titles
for submission in con_SOP:
    if not submission.stickied:
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            comment_dict["title"].append(submission.title)
            comment_dict["parent_id"].append(comment.parent())
            comment_dict["comment_id"].append(comment.id)
            comment_dict["comment_body"].append(comment.body)

# save them into data frame with the mapping planned out in the dict
comment_data = pd.DataFrame(comment_dict)

# extract out the column of comment_body, and insert into the one string
import string
comment = comment_data[['comment_body']]
comm_str = comment.comment_body.str.cat(sep='') #flatten and make the column into a single string format
translator = str.maketrans('', '', string.punctuation)
#This uses the 3-argument version of str.maketrans
# with arguments (x, y, z) where 'x' and 'y' must be equal-length strings and characters in 'x'
# are replaced by characters in 'y'. 'z' is a string (string.punctuation here)
# where each character in the string is mapped to None
comm_str = comm_str.translate(translator) # apply the mapping and replace out the punctuation
comm_str = comm_str.split() #parse the words out

#caculate the word frequency in comments
import collections
count_list = collections.Counter(comm_str) # count collection of the word frequency
count_list.most_common() #print out the counts
comm_freq = pd.DataFrame(count_list.most_common(), columns=['words','count']) # data frame the words and its count


#all topics in new SOP
#refresh the token for all the title process or else it will not load
topics_dict = { "title":[], "id":[], "comms_num": [], "created": []} #define the title mapping
for submission in con_SOP:
    if not submission.stickied:
        topics_dict["title"].append(submission.title)
        topics_dict["id"].append(submission.id)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)

topics_data = pd.DataFrame(topics_dict)

# extract out the column of topic data, and insert into the one string
topics = topics_data[['title']]
topics_str = topics.title.str.cat(sep='') #flatten and make the column into a single string format
topics_str = topics_str.translate(translator) #apply that translator mapping
topics_str = topics_str.split()#parse the words out

#caculate the word frequency in comments
count_list_topics = collections.Counter(topics_str) # count collection of the word frequency
count_list_topics.most_common() #print out the counts
topic_freq = pd.DataFrame(count_list_topics.most_common(), columns=['words','count'])
# data frame the words and its frequency counts

