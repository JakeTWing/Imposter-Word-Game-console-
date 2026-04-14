from functions import file_to_list, game, clear_console
from player_class import Player
import random

#Gets input from user for the ammount of players
#input must be an integer greater than 2
while True:
    
    try:
        num_of_players = int(input("Enter the ammount of players: "))
        
        if num_of_players > 2:
            clear_console()
            break
        
        print("The number of players must be greater than 2\n")
        
    except ValueError:
        print("Inputed value must be an integer\n")



imposter_word_list = file_to_list("imposter_words.txt")
word_list = file_to_list("topic_words.txt")


game(num_of_players, word_list, imposter_word_list)
