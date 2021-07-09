import time
from pynput import keyboard as keyboard_0
import pandas
import csv

class SpeedyGonzales:
    
    def __init__(self):
        self.history_score = self.read_leaderboard()
    
    def print_leaderboard(self):
        """Print out the leaderboard for user."""
        
        leaderboard = pandas.DataFrame(self.history_score.items(), columns=["Name", "Score"])
        leaderboard.index += 1
        
        print(leaderboard)
    
    def read_leaderboard(self):
        """Read the leaderboard from Leaderboard.csv."""
        
        with open("Leaderboard.csv", 'r') as in_file:
            reader = csv.reader(in_file)
            history_score = {rows[0]:float(rows[1]) for rows in reader}
        
        return history_score
            
    def update_leaderboard(self, name, score):
        """Update the leaderboard to Leaderboard.csv."""
        
        # Remove ranking no 10 if given name not in list.
        if name not in self.history_score.keys():
            self.history_score.popitem()
        
        # Add the highscore to leaderboard.
        self.history_score[name] = score
        
        # Sort the leaderboard.
        self.history_score = dict(sorted(self.history_score.items(), key=lambda x:x[1]))
        with open("Leaderboard.csv", 'w') as f:
            for key in self.history_score.keys():
                f.write("%s, %s\n"%(key, self.history_score[key]))
                
    def get_highscore(self, score):
        """ Get the current user's score and return
            0: Not in top 10 highscores
            1: In top 10 highscores
            2: Champion
        """
        scores = list(self.history_score.values())
        
        # Compare current score with the last placing in leaderboard.
        if score > max(scores):
            return 0
        else:
            if score < min(scores):
                return 2
            else:
                return 1
    
    def main(self):
        """Allow user to press 'a' and 'k' to move left and right leg respectively."""
        
        print("Welcome to Speedy Gonzales!")
        print("Press 'a' to move your left leg, 'k' to move your right leg.")
        print("Ready?")
        
        start = time.time()
        self.score = 0
        self.previous_key = None
        
        def on_key_release(key):
            try:
                if key == keyboard_0.Key.esc:
                    print("Good Bye!")
                    listener.stop()
                    exit()
                
                if key.char == "a" or key.char=='k':
                    msg = " . " if key.char=='a' else "   ."
                    print(msg)
                    # Main loop to run the program.
                    if key.char != self.previous_key:
                        self.score = self.score + 1
                        self.previous_key = key.char
                    else:
                        # Hit 'a' or 'k' two times in a row, fell for 2s.
                        self.previous_key = None
                        print("Ops! You fell down on your face!")
                        time.sleep(1)
                        print("Stand up!")
                        time.sleep(1)
                        print("Continue running!")
                    
                # Finish running.
                if self.score >= 40:
                    listener.stop()
                    end = time.time()
                    score = round(end - start, 2)
                    print("Congrats! You have run 100m in {}!".format(score))
                    
                    print("Check the previous winner...")
                    self.print_leaderboard() 
                    
                    score_flag = self.get_highscore(score)
                    if score_flag == 0:
                        # Not in leaderboard.
                        print("Thanks for playing.")
                    else:
                        if score_flag == 1:
                            # In top 10 leaderboard.
                            winner_msg = "\n\nYou have achieved top 10! "
                        else:
                            # Get champion.
                            winner_msg = "\n\nYou are the champion! "
                        
                        # Get winner's name and update leaderboard.
                        name = input(winner_msg + "Please enter your name:" )
                        self.update_leaderboard(name, score)
                        
                        print("Lets check the new leaderboard.... \n\n\n\n\n")
                        time.sleep(1)
                        self.print_leaderboard() 
                        
                        
                    # Ask for new game.
                    in_flag = input("New game? (Y/N)")
                    if in_flag.upper() == 'Y':
                        self.main()
                    else:
                        print("Good Bye!")
                        exit()
                
            except AttributeError:
                print(key)

        with keyboard_0.Listener(on_release = on_key_release, suppress=True) as listener:
            listener.join()
        
if __name__ == "__main__":
    speed = SpeedyGonzales()
    speed.main()