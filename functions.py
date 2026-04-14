from player_class import Player
import random
import os
import sys

#clears the console
def clear_console():
    
    if os.name == 'nt':  
        os.system('cls')
    else:  
        os.system('clear')
        
        
#converts the file to a list
def file_to_list(file_name):
    
    words = open(file_name, "r")
    word_list = [line.strip() for line in words]
    words.close()
    
    return word_list
    
#confirms word_list length == imposter_word_list length
#then returns the index of the randomly selected word
def get_random_topic_index(word_list, imposter_word_list, indexes_of_topics_not_used):
    #checks for a discontinuity between the lists
    if len(word_list) != len(imposter_word_list):
        print("\n***--------------------------------***\nError with the files: length of word list does not equal the length of the imposter word list\nDebug: This Exit is located in the 'get_random_topic_index' function\n***--------------------------------***\n\n")
        #ends program
        sys.exit()

    
    #selects an index from the list of words that have not been used
    index = indexes_of_topics_not_used[random.randint(0, len(indexes_of_topics_not_used) - 1)]
    
    return index
    

#*Adds a bias. Reduces the chance to get the same index twice in a row*    
#Math to calc probablity of consecutive indexes:
#p(1) = (1/total_indexes * bias_strength/100) 
#p(2) = (1/total_indexes * (100 - bias_strength)/100 * 1/total_indexes)
#p(total) = p1 + p2
def get_weighted_random(total_indexes, prev_index):
    #determines how strong the bias is. Higher => Greater Bias; Lower => Smaller Bias
    #Stronger bias means it is less likely to get the same index twice in a row
    bias_strength = 32
    
    index = random.randint(0, total_indexes - 1)
    
    if index != prev_index or random.randint(1,100) >= bias_strength:
        return index
        
    return random.randint(0, total_indexes - 1)



        
#single round of the game imposter
#input: players, topic, imposter_hint, starting_player
#this code is responsible for the loop through a single round; shows each player their topic/hint,
#Then allows the user to reveal the imposter. 
def single_round(players, topic, imposter_hint, starting_player_num):
    
    imposter_player_num = -1
    
    for i in range(len(players)):
        #clears, gets the current player, determines if they are an imposter
        clear_console()
        current_player = players[i]
        is_imposter = Player.get_info(current_player)[1]
        
        #gets the imposter number for later
        if is_imposter:
            imposter_player_num = i
           
        #Player must press enter to see topic    
        input(f"player {i+1}'s turn to see the topic, press enter to see the word: ")
        
        #prints topic/imposter_hint
        if is_imposter:
            print(f"\nYou are the *imposter*, your hint word is *{imposter_hint}*")
        else:
            print(f"\nThe Topic is *{topic}* ")
        
        #press enter to move on to the next player
        if i + 1 == len(players):
            input("press enter to close the word: ")
        else:
            input("press enter, then give to the next player: ")
    
    clear_console()
    
    #prints starting player
    print(f"*Player {starting_player_num + 1}* will talk first this round.")
    print(f"All players have seen the topic. Each player will state one word or phrase that describes the topic\n")    
    
    #prompts the user to input "r"; reveals the imposter
    reveal = input("When ready, input 'r' to Reveal the imposter: ")
    while reveal.lower() != ("r"):
        reveal = input("When ready, input 'r' to Reveal the imposter: ")
        
    clear_console()
    print(f"The topic was *{topic}*")
    print(f"The imposter was *player {imposter_player_num + 1}*")
    input("Press enter to start the next round: ")
    



#takes the string of imposter hints and chooses a random one
def get_rand_hint(imposter_word_list, word_index):
    
    #list of hints, splits each string from the original string
    imposter_hints = []
    orignal_string_hints = imposter_word_list[word_index]
    
    #point where the hints are split
    split_point = ","
    
    #loops until each string has been separated
    while orignal_string_hints.find(split_point) != -1:
        
        #finds the index of the first split point
        split_index = orignal_string_hints.find(split_point)
        #adds the word to the list
        imposter_hints.append(orignal_string_hints[:split_index])
        #updates the orignal_string_hints string by removing the added word
        orignal_string_hints = orignal_string_hints[split_index+1:]
    #add the final word
    imposter_hints.append(orignal_string_hints)


    #picks a random value through the list
    return imposter_hints[random.randint(0, len(imposter_hints) - 1)]
    



#inputs: num_of_players, word_list, imposter_word_list
#requirements: num_of_players must be > 0, word_list and imposter_word_list must equal in length
#This function starts the game
def game(num_of_players, word_list, imposter_word_list):
    print(f"welcome to the game of imposter. Please Chose your player number {1} - {num_of_players}")
    input("press enter to start a round: ")
    #creates varribles
    prev_index_imposter = -1
    prev_index_starting_player = -1
    #creates the list of indexes for topics not used yet. 
    #this list is appended to ensure duplicate topics are not selected
    indexes_of_topics_not_used = [i for i in range(len(word_list))]
    


    while True:
        
        #gets a random index based on the length of the file
        word_index = get_random_topic_index(word_list, imposter_word_list, indexes_of_topics_not_used)
        #updates the 'indexes_of_topics_not_used' to prevent dupes
        indexes_of_topics_not_used.remove(word_index)
        
        
        #gets the topic and imposter strings
        topic = word_list[word_index]
        imposter_hint = get_rand_hint(imposter_word_list, word_index)
        
        
        #Gets the imposter player. Uses 'get_weighted_random' to add a small bias against a 
        #player getting Imposter twice in a row. 
        imposter_player_num  = get_weighted_random(num_of_players, prev_index_imposter)
        prev_index_imposter = imposter_player_num
        
        #Gets the starting player. Uses 'get_weighted_random' to add a small bias against a 
        #player being the starting player twice in a row. 
        starting_player_num = get_weighted_random(num_of_players, prev_index_starting_player)
        prev_index_starting_player = starting_player_num
        
        #creates a list of 'Player' class objects, and sets the correct player to the imposter
        players = [Player(i, i == imposter_player_num) for i in range(num_of_players)]
        
        #Shows each player the topic/imposter_hint 
        single_round(players, topic, imposter_hint, starting_player_num)
        
        #tells the user that all topics in the file have been used, then resets the 
        #'indexes_of_topics_not_used' list to prevent errors
        if len(indexes_of_topics_not_used) == 0:
            indexes_of_topics_not_used = [i for i in range(len(word_list))]
            print("\n\n--------------------------------------------\n\n    *RESET* -  ALL WORDS HAVE BEEN USED       \n\n--------------------------------------------\n")
            input("")
