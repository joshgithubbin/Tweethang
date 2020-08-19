import tweepy
import time
from random_words import RandomWords

###############################################################################

def wordgen():
    rw = RandomWords()
    word = str(rw.random_word())
    blank ='_'
    for i in range(0,len(word)):
        blank += '_'
    return word,blank

###############################################################################

def wordcheck(word,blank,letter,count,fail,ID):
    if len(letter) > 1:
        return 'long'
    newblank =''
    subcount = 0
    for i in range(0,len(word)):
        if word[i].lower() == letter.lower(): 
            newblank += word[i]
            subcount += 1
        else:
            newblank += blank[i]
    if subcount == 0:
        api.send_direct_message(ID,"Strike!")
        fail +=1
    count += subcount
    return newblank,count,fail

###############################################################################

def victorycheck(word,count,fail,ID):
    '''check to see if all letters have been selected.'''
    if count == len(word):
        api.send_direct_message(ID,'The word has been found!')
        api.send_direct_message(ID,'The word was ' + word + '!')
        return 1
    if fail == 6:
        api.send_direct_message(ID,"The word has not been found!")
        api.send_direct_message(ID,"You lose!")
        api.send_direct_message(ID,"The word was " + word + "!")
        return 1
    else:
        api.send_direct_message(ID,str(6 - fail)+' guesses remaining!')
        return 0

###############################################################################
   
def askletter(selected,ID,stamp):
    while True:
        api.send_direct_message(ID, "Type your letter and press enter to make a guess!")
        response = 0
        while response == 0:
            print("made it here")
            time.sleep(60)
            dm = api.list_direct_messages(3) #check this
            message = readmessage(dm)
            newstamp = message.id_
            print(newstamp)
            if str(message.sender_id) == str(ID):
                print('reached this point')
                if newstamp != stamp:
                    print(message.text[0])
                    letter = message.text[0]
                    stamp = newstamp
                    response = 1
        letter1 = letter.lower()
        if letter1 in selected:
            api.send_direct_message(ID,"Letter already guessed!")
        if letter1 not in selected:
            selected.append(letter1)
            break
    return letter,selected,stamp

###############################################################################

def hangman(ID,stamp):
    win = 0
    count=0
    fail = 0
    selected = []
    api.send_direct_message(ID,'Good luck! Generating word...')
    word,blank = wordgen()
    api.send_direct_message(ID," ".join(blank))
    api.send_direct_message(ID,'Six strikes remaining!')
    while win == 0:
        letter,selected,stamp = askletter(selected,ID,stamp)
        api.send_direct_message(ID, 'You have already selected: ' +str(selected))
        blank,count,fail = wordcheck(word,blank,letter,count,fail,ID)
        api.send_direct_message(ID," ".join(blank))
        win = victorycheck(word,count,fail,ID)        
    return

###############################################################################

def twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN,ACCESS_TOKEN_SECRET,worl=True,worln=True,speak = True):
    '''Authenticates to Twitter and creates API object.'''
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    
    api = tweepy.API(auth,wait_on_rate_limit=worl,wait_on_rate_limit_notify=worln)
    
    if speak == True: print("Creating API object...")
    
    api.verify_credentials()
    
    if speak == True: print("Authentication successful.")
    
    return api

###############################################################################

def readmessage(dm):
    '''gets relevant message data - time, sender, recipient, text.'''
    
    class Message:
        
        
        id_ = str(dm[0].id)
        
        epoch = float(dm[0].created_timestamp)/1000
        timestamp =  time.gmtime(epoch)
        datetime = time.strftime('%m/%d/%Y %H:%M:%S')
    
        text = dm[0].message_create['message_data']['text'].encode('utf-8')
    
        sender_id = int(dm[0].message_create['sender_id'])
        sender_username = str(api.get_user(sender_id).screen_name)
    
        recipient_id = int(dm[0].message_create['target']['recipient_id'])
        recipient_username = str(api.get_user(recipient_id).screen_name)
    
    return Message


###############################################################################

def readtweet(stat):
    '''gets relevant tweet tdata - time, poster, text'''
    
    class Tweet:
    
        id_ = stat[0].id_str
    
        datetime = stat[0].created_at
    
        text = stat[0].text.encode('utf-8')
    
        sender_id = int(stat[0].user.id_str)
    
        sender_username = stat[0].user.name.encode('utf-8')
    
    return Tweet

###############################################################################