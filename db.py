import shelve

database_file = 'feedbacks.db'
feedback_key = 'feedback'

def save_feedback(feedback):    # feedback is a dictionary of one feedback entry - name, email, description, image_file
    with shelve.open(database_file) as db:
        if feedback_key in db:
            feedbacks = db[feedback_key] # A list of feedback
        else: 
            feedbacks = []
            
        feedbacks.append(feedback)
        db[feedback_key] = feedbacks # save the new list to the db
        
def get_all_feedbacks():
    with shelve.open(database_file) as db:
        feedbacks = db.get(feedback_key, [])
    return feedbacks

if __name__ == "__main__": #Code that will run if db.py is run directly, not imported
    print(get_all_feedbacks())