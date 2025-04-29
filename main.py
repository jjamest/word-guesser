# ------------------------ Import statements ---------------------
from tkinter import *
import winsound # For background music
import random
import sys # For closing program down
import os # For restarting the program

# ------------------------ Global variables ---------------------
# Set root window dimensions. Allows for them to change since all dimensions depend on these two variables 
width = 1200
height = 800

# Set x and y coordinates for the back button
bk_btn_x = 70
bk_btn_y = height - 50

name = "" # Store player name
chosen_word = "" # Will store the randomly generated word
guesses_count = 0 # Count the number of guessed taken

# Keep current strikes. Makes sure it doesn't go over the limit
strikes = 0

# The word length set by the user
short = 5
normal = 10
long = 15
word_length = "normal" # Store current choice for word length. Default is normal

# Available difficulties that determines the strike limit
difficulties = ["Easy", "Medium", "Hard"]
difficulty = difficulties[0] # Chosen difficulty

# Strikes for difficulties
easy_strike_limit = 15 
medium_strike_limit = 10 
hard_strike_limit = 5
strikes_limit = 0 # Will be set later to store the current limit for strikes

# Available word categories
categories = ["Country", "Food", "Vocabulary", "All"]
category = "All" # Default category set at "all"

# Stores the user's guess to the whole word
guess_whole = ""

# Check if a game has been started. Helps prevent keyboard event checker errors before the game starts
IN_GAME = False

# Font settings
terminal_tiny = ("terminal", 8)
terminal_small = ("terminal", 10)
terminal_medium = ("terminal", 15)
terminal_large = ("terminal", 20)
terminal_huge = ("terminal", 30)

# Word banks
bank_countries = []
with open("bank_countries.txt", "r") as file:
    for i in file:
        bank_countries.append(i.strip().lower())
bank_foods = []
with open("bank_foods.txt", "r") as file:
    for i in file:
        bank_foods.append(i.strip().lower())
bank_vocabs = []
with open("bank_vocabs.txt", "r") as file:
    for i in file:
        bank_vocabs.append(i.strip().lower())

# ------------------------ Popup window ---------------------
def guess_popup():
    """ Function to create the popup window whose function is to let the user guess a word completly """
    def popup_confirm():
        """ Function that submits the guessed word. If it is wrong the player loses but if it is right then the player wins immediatly """
        global guess_whole
        global chosen_word
        global IN_GAME
        global game_canvas
        global ending_canvas
        global player_won
        global player_lost
        global setup_ending
        
        # Close the current popup
        popup.destroy()
        
        # Close the game, close the game canvas, and display the ending screen
        IN_GAME = False
        game_canvas.pack_forget()
        ending_canvas.pack()
        
        # Retreive the guessed word and setup the ending screen depending on whether the guess was right or wrong
        guess_whole = popup_var.get()
        print("GUESS:", guess_whole)
        if guess_whole == chosen_word:
            print("Guess is correct")
            player_won()
        else:
            print("Guess is incorrect")
            player_lost()
        
        # Display the ending
        setup_ending()
    
    # Configure popup properties
    popup = Toplevel() # Makes a popup window separate from the main window
    popup.grab_set() # Makes the popup window focused. User cannot press anywere else on the main game window
    popup.wm_title("Guess the whole word!") # Change window title
    popup.iconbitmap("guess.ico") # Change icon
    popup.resizable(False, False)
    
    # Create title text
    title = Label(popup, text="Guess the whole word, but if you get it wrong you will lose...", font=terminal_large)
    title.pack(side="top", fill="x", padx=20, pady=15)
    
    # Create sub text below
    subttext = Label(popup, text="Enter your guess below", font=terminal_medium)
    subttext.pack()
    
    # Create entry box to enter word guess
    popup_var = StringVar()
    entry = Entry(popup, textvariable=popup_var, bg="cyan")
    entry.pack()
        
    # Create button to guess
    confirm_btn = Button(popup, text="Confirm", command=popup_confirm, bg="green", activebackground="cyan")
    confirm_btn.pack(pady=10)
    
    # Create button to cancel
    cancel_btn = Button(popup, text="Cancel", command=popup.destroy, bg="red", activebackground="cyan")
    cancel_btn.pack(pady=20)
        
    
    popup.mainloop()

# ------------------------ Reuseable functions ---------------------
# Reuseable function to set the background to paper
def set_bknd_paper(canvas):
    """ Switches to a paper image that acts as the background """
    return canvas.create_image(width // 2, height // 2, image=img_bknd)

# Create a back button at a fixed location
def create_bk_btn(canvas, cmd, x=bk_btn_x, y=bk_btn_y):
    """ Create a small back button that goes back to the previous canvas on most of the canvases """
    def after_wait():
        obj.configure(text="Back", command=on_btn_before)
    
    def on_btn_after():
        cmd()
        obj.configure(text="Back", command=on_btn_before)
        
    def on_btn_before():
        obj.configure(text="Are you sure?", command=on_btn_after)
        obj.after(1500, after_wait)
    
    obj = Button(canvas, bg="light gray", text="Back", command=on_btn_before, borderwidth=0, font=terminal_small)
    return canvas.create_window(x, y, window=obj)

# Create an end button similar to the back button
def create_end_btn(canvas, x=bk_btn_x, y=bk_btn_y):
    """ Creates a small end button that ends the entire game on most of the canvases """
    def after_wait():
        obj.configure(text="End", font=terminal_medium, command=on_btn_before)
    
    def on_btn_after():
        sys.exit()
        
    def on_btn_before():
        obj.configure(text="Are you sure?", font=terminal_small, command=on_btn_after)
        obj.after(1500, after_wait)
    
    obj = Button(canvas, bg="light gray", fg="red", text="End", command=on_btn_before, borderwidth=0, font=terminal_medium)
    return canvas.create_window(x, y, window=obj)

# ------------------------ Game functions ---------------------
def intro(root):
    global intro_canvas
    global home_canvas
    global rules_canvas
    
    def on_intro_start():
        intro_canvas.itemconfig(start_btn, state=HIDDEN)
        intro_canvas.itemconfig(instruct_text, state=NORMAL)
        intro_canvas.itemconfig(name_entry, state=NORMAL)
        intro_canvas.itemconfig(ok_btn, state=NORMAL)
        intro_canvas.itemconfig(intro_bk_btn, state=NORMAL)
        
    def on_ok():
        global name
        if player_name.get():
            name = player_name.get()
            
            intro_canvas.pack_forget()
            rules_canvas.pack(side="left", fill="both", expand=True)
            
            print("Player name is: ", name)
        else:
            intro_canvas.itemconfig(error_text, state=NORMAL)
            
    def on_intro_bk():
        intro_canvas.itemconfig(start_btn, state=NORMAL)
        intro_canvas.itemconfig(intro_bk_btn, state=HIDDEN)
        intro_canvas.itemconfig(instruct_text, state=HIDDEN)
        intro_canvas.itemconfig(name_entry, state=HIDDEN)
        intro_canvas.itemconfig(ok_btn, state=HIDDEN)
        intro_canvas.itemconfig(error_text, state=HIDDEN)
        print("Going back to intro screen")        
    
    # Create intro canvas
    intro_canvas = Canvas(root, height=height, width=width)
    
    # Reset background
    set_bknd_paper(intro_canvas)
    
    # Load the title image and put it in the center of the window
    intro_canvas.create_image(width // 2, 200, image=img_title)
    
    # Load the start button
    obj = Button(intro_canvas, image=img_start_btn, command=on_intro_start, borderwidth=0)
    start_btn = intro_canvas.create_window(width // 2, 500, window=obj)
    
    # Display the text and text field where the user can input their name
    instruct_text = intro_canvas.create_text(width // 2, 445, text="To start, please enter your name", font=terminal_large, fill="brown", state=HIDDEN)
    player_name = StringVar()
    obj = Entry(intro_canvas, font=terminal_huge, fg="blue", bg="cyan", justify=CENTER, textvariable=player_name)
    name_entry = intro_canvas.create_window(width // 2, 510, width=350, height=50, window=obj, state=HIDDEN)
    
    # Load ok button after player enters their name
    obj = Button(intro_canvas, image=img_start_btn, command=on_ok, borderwidth=0)
    ok_btn = intro_canvas.create_window(width // 2, 600, window=obj, state=HIDDEN)
    
    # Create a back button to go back to the previous page
    intro_bk_btn = create_bk_btn(intro_canvas, on_intro_bk)
    intro_canvas.itemconfig(intro_bk_btn, state=HIDDEN)

    # Create a space for error messages to show up
    error_text = intro_canvas.create_text(width // 2, height - 50, font=("impact", 15), fill="red", text="Error, you must enter your name before starting!", state=HIDDEN)


    return intro_canvas

def rules(root):
    global rules_canvas
    global home_canvas
    
    def on_mousewheel(event):
        """ Add scrollwheel function to the scrollbar """
        rules_canvas.yview_scroll(int(-1 * (event.delta / 100)), "units")
        
    def on_rules_start():
        print("Finished reading rules page")
        rules_canvas.pack_forget()
        home_canvas.pack()
        home_canvas.create_text(width // 2, 195, text="Hello " + name, font=terminal_medium, fill="orange")
    
    # Create rules canvas
    rules_canvas = Canvas(root, height=height, width=width)

    # Create scrollbar widget
    scrollbar = Scrollbar(rules_canvas, orient="vertical", command=rules_canvas.yview)
    rules_canvas.configure(yscrollcommand=scrollbar.set)
    rules_canvas.bind_all("<MouseWheel>", on_mousewheel)
    scrollbar.pack(side="right", fill="y")

    # Load the rules page onto the canvas
    rules_image = rules_canvas.create_image(0, 0, image=img_rules_page, anchor="nw")

    # Set the scroll region of the window
    rules_canvas.config(scrollregion=rules_canvas.bbox(rules_image))
    
    # Create button that exists the rules page
    obj = Button(rules_canvas, bg="yellow", image=img_start_btn, command=on_rules_start, borderwidth=10)
    rules_btn = rules_canvas.create_window(width // 2, 2900, window=obj)
    
    
    return rules_canvas

def home(root):
    global height, width
    global home_canvas
    global rules_canvas
    global game_canvas
    
    global scoreboard
    global show_scoreboard
    global name
    
    def on_change_difficulty(event):
        global difficulty
        difficulty = chosen_value.get()
        print("Difficulty changed to", difficulty)
        
    def on_change_category(event):
        global category
        category = chosen_category.get()
        print("Changed category to", category)
        
        if category == "Country":
            category_image.config(image=img_country)
        elif category == "Food":
            category_image.config(image=img_food)
        elif category == "Vocabulary":
            category_image.config(image=img_vocab)
        else:
            category_image.config(image=img_all)
        
    def on_start():
        global difficulty, setup, chosen_word, strikes_limit, easy_strike_limit, medium_strike_limit, hard_strike_limit
        global word_length, short, normal, long
        global chosen_category, bank_countries, bank_foods, bank_vocabs
        
        print("Starting game on " + difficulty + " mode")
        
        if difficulty == "Easy":
            strikes_limit = easy_strike_limit
        elif difficulty == "Medium":
            strikes_limit = medium_strike_limit
        elif difficulty == "Hard":
            strikes_limit = hard_strike_limit
        
        print("Current strike limit:", strikes_limit)
        print("Current word length:", word_length)
        
        # Choose a word from the bank according to the word length
        new_list = [] # Make a new list to choose a random word from
        bank = []
        if category == "Country":
            bank = bank_countries
        elif category == "Food":
            bank = bank_foods
        elif category == "Vocabulary":
            bank = bank_vocabs
        else:
            bank = bank_countries + bank_foods + bank_vocabs
        
        # Create a new bank of words that fits the word length criteria and later randomly pick from this list
        for i in range(0, len(bank)):
            length = len(bank[i])
            if word_length == "short" and length <= short:
                new_list.append(bank[i])
            elif word_length == "normal" and short <= length <= normal:
                new_list.append(bank[i])
            elif word_length == "long" and normal < length:
                new_list.append(bank[i])
        print("New list:", new_list)
        
        # Randomly pick a word from the list using the random module
        chosen_word = random.choice(new_list)
        print("Random word chosen:", chosen_word)
        
        # Switch canvases between the home and game pages
        home_canvas.pack_forget()
        game_canvas.pack()
        
        # Setup the game canvas that uses the currently selected properties
        setup()
        
    def on_rules():
        rules_canvas = rules(root)
        rules_canvas.pack(side="left", fill="both", expand=True)
        home_canvas.pack_forget()
        
    def on_radio():
        global word_length
        word_length = radio_var.get()
        print("Selected", radio_var.get())
        
    def show_scoreboard():
        score_frame = Frame(home_canvas, height=300, width=250)
        score_frame.configure(bg="cyan")
        score_title = Label(score_frame, text="Scoreboard", font=("ariel", 15), bg="cyan")
        score_title.pack()
         
        # Open the scoreboard text file and reverse it to make the first line the most recent
        scoreboard = open("scoreboard.txt", "r")
        lines = scoreboard.readlines() # Read scoreboard list backwards to show most recent on the top
        lines.reverse()
        
        # Create a limit on how many lines the scoreboard will have to avoid some going off the page
        upper_limit = len(lines)
        if len(lines) > 20:
            upper_limit = 20
        
        # Display each line on the scoreboard
        for i in range(0, upper_limit): # Only show first 20 items so lines won't go out of the dimensions
            elements = lines[i].split(" ") 
            new = elements[0] + " took " + elements[1] + " tries " + elements[2].lower() + " " + elements[3] + " " + elements[4]
            line = Label(score_frame, text=new, bg="cyan")
            line.pack()
        
        # Check if the list is empty
        if lines == []:
            line = Label(score_frame, text="Nothing here...", bg="orange")
            line.pack()
        
        # Display the scoreboard on the right side of the home canvas
        home_canvas.create_window(width - 200, height // 2, window=score_frame)
    
    # Create home canvas
    home_canvas = Canvas(root, height=height, width=width)

    # Reset background
    set_bknd_paper(home_canvas)
    
    # Create end button
    create_end_btn(home_canvas)

    # Load the title image and put it in the center of the window. Also add the welcome text
    home_canvas.create_image(width // 2, 100, image=img_title_small)

    # Create text that welcomes the player
    welcome_text = home_canvas.create_text(width // 2, 195, font=terminal_medium, fill="orange")

    # Allow the user to choose difficulty
    chosen_value = StringVar(value=difficulties[0])
    home_canvas.create_text(width // 2, 230, text="Choose your difficulty", font=terminal_large, fill="black")
    obj = OptionMenu(home_canvas, chosen_value, *difficulties, command=on_change_difficulty)
    obj.config(width=10, fg="blue", bg="cyan", font=terminal_medium, borderwidth=0)
    difficulty_menu = home_canvas.create_window(width // 2, 270, window=obj)
    
    # Create radio buttons to choose word length
    home_canvas.create_text(width // 2, 315, font=terminal_large, text="Choose your word length")
    radio_var = StringVar(value="normal")
    short_radio = Radiobutton(home_canvas, text="Short", font=terminal_small, variable=radio_var, value="short", bg="light blue", activebackground="green", highlightcolor="yellow", indicator=0, command=on_radio)
    normal_radio = Radiobutton(home_canvas, text="Normal", font=terminal_small, variable=radio_var, value="normal", bg="light blue", activebackground="green", highlightcolor="yellow", indicator=0, command=on_radio)
    long_radio = Radiobutton(home_canvas, text="Long", font=terminal_small, variable=radio_var, value="long", bg="light blue", activebackground="green", highlightcolor="yellow", indicator=0, command=on_radio)
    home_canvas.create_window(width // 2 - 60, 350, window=short_radio)
    home_canvas.create_window(width // 2, 350, window=normal_radio)
    home_canvas.create_window(width // 2 + 60, 350, window=long_radio)
    
    # Create an OptionMenu to chose category
    chosen_category = StringVar(value="All")
    home_canvas.create_text(width // 2, 400, text="Choose your word category", font=terminal_large, fill="black")
    obj = OptionMenu(home_canvas, chosen_category, *categories, command=on_change_category)
    obj.config(width=10, fg="blue", bg="cyan", font=terminal_medium, borderwidth=0)
    category_menu = home_canvas.create_window(width // 2, 440, window=obj)
    
    # Create a system that displays an image related to the chosen category
    category_image = Label(home_canvas, image=img_all, bg="green")
    category_image.place(x=width // 2 - 140, y=420)
        
    # Load the start button as an image
    obj = Button(home_canvas, bg="green", image=img_start_btn2, command=on_start, borderwidth=0)
    home_btn = home_canvas.create_window(width // 2, 600, window=obj)

    # Create a button that goes back to the rules page
    obj = Button(home_canvas, image=img_rules_btn, command=on_rules, borderwidth=0)
    rules_btn = home_canvas.create_window(100, 50, window=obj)
    
    # Create scoreboard section which is also scrollable
    show_scoreboard()


    return home_canvas

def game(root):
    # Global canvases
    global game_canvas, ending_canvas, home_canvas
    # Global variables
    global width, height
    global chosen_word
    global positions
    global strikes
    global guessed_bools
    global no_spaces
    global guessed_incorrect
    global strikes_limit
    global terminal_large
    # Global functions
    global setup, generate_incorrect
    
    positions = []
    guessed = 0
    guessed_bools = []
    guessed_incorrect = []
    
    no_spaces = ""
    
    x1s = []
    x2s = []
    
    def keypress(event):
        global strikes
        global strikes_limit
        global IN_GAME
        global guessed_bools
        global no_spaces
        global guessed_incorrect
        global player_lost
        global player_won
        global setup_ending
        global guesses_count
        
        # Don't do anything if the game hasn't started yet. Avoids the intro screen where the player is asked their name
        if not IN_GAME or not event.char.isalpha() or event.char.isupper():
            return

        # Condition to check if the character pressed is valid and followed by showing the character if it is
        if event.char in no_spaces and guessed_bools[no_spaces.index(event.char)] == False:
            print("Letter (" + event.char + ") Guessed correctly")
            
            # Show the character on the screen above each character line
            for i in range(0, len(no_spaces)):
                if no_spaces[i] == event.char:
                    game_canvas.create_text(positions[i], 280, text=event.char, font=terminal_large)
                    guessed_bools[i] = True
                    
            # Use positions to compare because it does not include any spaces
            if all(guessed_bools):
                # This is when all letters have been guessed
                print("Guessed all letters")
                IN_GAME = False
                game_canvas.pack_forget()
                ending_canvas.pack()
                player_won()
                setup_ending()
                
            # Increase the guess count by one
            guesses_count = guesses_count + 1
            print("GUESSES_COUNT:", guesses_count)
        # Condition to check if the character pressed is not valid
        elif event.char not in no_spaces and event.char not in guessed_incorrect:
            print("Guessed incorrectly")
            
            # Add to the strikes cound
            strikes = strikes + 1
            
            # Update the screen showing the number of strikes
            game_canvas.itemconfig(strikes_txt, text=str(strikes) + "/" + str(strikes_limit))
            
            # Check if the character is already pressed before. If not, add it to the list containing incorrectly pressed characters
            exist = False
            for i in range(0, len(guessed_incorrect)):
                if guessed_incorrect[i] == event.char:
                    exist = True
                    break
            if exist == False:
                guessed_incorrect.append(event.char)
            
            # Check if the the strike limit has been reached.
            if strikes == strikes_limit:
                print("You lost")
                IN_GAME = False
                game_canvas.pack_forget()
                ending_canvas.pack()
                player_lost() # Configure the ending screen before showing
                setup_ending()
            
            # Increase the guess count by one
            guesses_count = guesses_count + 1
            print("GUESSES_COUNT:", guesses_count)
        
        # Update the incorrectly guessed letters
        game_canvas.itemconfig(incorrect_txt, text=guessed_incorrect)
            
    def setup():
        global positions
        global chosen_word
        global IN_GAME
        global guessed_bools
        global no_spaces
        global strikes_limit
        global strikes
        global terminal_large
        
        IN_GAME = True
        
        # Remove all spaces in the chosen word
        no_spaces = chosen_word.replace(" ", "")
        
        # Set properties for the character lines
        line_length = 30
        gap = 20
        
        # Draw the lines for each character in the chosen word
        total_width = (len(chosen_word) * line_length) + ((len(chosen_word) - 1) * gap)
        start_x = (width - total_width) // 2
        for i in range(0, len(chosen_word)):
            x1 = start_x + (line_length + gap) * i
            x2 = x1 + line_length # left x point + line length
            if chosen_word[i] != " ":
                x1s.append(x1)
                x2s.append(x2) 
                positions.append(x2 - (line_length / 2))
        
        # Create the lines from the positions declared by the loop above. They are separated because spaces will cause problems
        for i in range(0, len(no_spaces)):
            game_canvas.create_line(x1s[i], 300, x2s[i], 300, width=3)
            # At the start add all as False. When the player guesses each then switch elements accordingly
            guessed_bools.append(False)
        
        # Update the strikes number
        game_canvas.itemconfig(strikes_txt, text=str(strikes) + "/" + str(strikes_limit))
    
    def on_game_bk():
        global game_canvas
        global home_canvas
        global strikes
        game_canvas.pack_forget()
        home_canvas.pack()
        game_canvas = game(root)
        strikes = 0
    
    # Create game canvas
    game_canvas = Canvas(root, height=height, width=width)
    
    # Detect keyboard presses
    root.bind("<KeyPress>", keypress)
    
    # Reset background
    set_bknd_paper(game_canvas)
    
    # Load title image
    game_canvas.create_image(width // 2, 100, image=img_title_small)
    
    # Load button that lets the user guess the whole word
    obj = Button(game_canvas, text="Know the word already?", command=guess_popup, bg="yellow", font=terminal_small)
    guess_btn = game_canvas.create_window(width // 2, 220, window=obj)
    
    # Create text
    game_canvas.create_text(width // 2, 330, text="Use your keyboard to guess", font=terminal_medium)
    
    # Display the number of strikes left
    game_canvas.create_text(width // 2, 390, text="Your strikes", font=terminal_medium)
    strikes_txt = game_canvas.create_text(width // 2, 420, font=terminal_large)
    
    # Create back button
    back_btn = create_bk_btn(game_canvas, on_game_bk)
    
    # Display a list of incorrectly guessed letters
    game_canvas.create_text(width // 2, 450, text="Guessed incorrectly", font=terminal_medium)
    incorrect_txt = game_canvas.create_text(width // 2, 480, text="", font=terminal_large)
    
    
    return game_canvas

def ending(root):
    global player_lost
    global name
    global player_won
    global setup_ending
    global chosen_word
    global strikes
    global show_scoreboard
    
    def player_lost():
        ending_canvas.create_image(width // 2, 180, image=img_lost)
        
    def player_won():
        global guesses_count
        global difficulty
        
        # Write a new entry to the scoreboard file to save the player's win
        scoreboard = open("scoreboard.txt", "a")
        scoreboard.write(name + " " + str(guesses_count) + " " + difficulty + " (Word: " + chosen_word + ")" + "\n")
        scoreboard.close()
        
        ending_canvas.create_image(width // 2, 180, image=img_won)
        
    def setup_ending():
        global game_canvas
        global strikes
        global guesses_count
        
        # Reset the game canvas for next rounds
        strikes = 0
        game_canvas = game(root)
        guesses_count = 0
        
        # Show the correct word
        ending_canvas.create_text(width // 2, 360, font=terminal_huge, text="The word was")
        ending_canvas.create_text(width // 2, 410, font=terminal_large, fill="orange", text=chosen_word)
    
    def back_home():
        global home_canvas
        global ending_canvas
        global show_scoreboard
        
        print("Going back home")
        
        ending_canvas.pack_forget()
        home_canvas.pack()
        ending_canvas = ending(root)
        
        # Update the scoreboard
        show_scoreboard()
    
    # Create the canvas for the ending screen
    ending_canvas = Canvas(root, height=height, width=width)
    
    # Set background to the paper image
    set_bknd_paper(ending_canvas)
    
    # Button to go to the home page
    obj = Button(ending_canvas, command=back_home, borderwidth=0, text="Home?", font=terminal_huge)
    ending_canvas.create_window(width // 2, 500, window=obj)
    
    # Create button to exit the program entirely
    create_end_btn(ending_canvas)
    
    
    return ending_canvas

def main():
    global width, height
    
    # Image assets
    global img_bknd, img_title, img_title_small, img_rules_page
    # Button assets
    global img_start_btn, img_start_btn2, img_rules_btn, img_won, img_lost
    # Icon assets
    global img_country, img_food, img_vocab, img_all
    
    # Set defaults for the game window and create the "root" window
    root = Tk()
    root.title("Word Guesser Game")
    root.resizable(False, False)
    root.geometry(str(width) + "x" + str(height))
    root.iconbitmap("icon.ico")
    
    # Create menu bar widget with a 'file' dropdown menu
    menu = Menu(root)
    
    file_menu = Menu(menu, tearoff=0)
    file_menu.add_command(label="Restart", command=lambda: os.execl(sys.executable, sys.executable, *sys.argv)) # Lambda command restarts the entire program
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=lambda: sys.exit())
    
    menu.add_cascade(label="File", menu=file_menu)
    root.config(menu=menu)
    
    # Load image assets
    img_bknd = PhotoImage(file="bknd.png")
    img_title = PhotoImage(file="title.png")
    img_title_small = PhotoImage(file="title_small.png")
    img_start_btn = PhotoImage(file="start_btn.png")
    img_start_btn2 = PhotoImage(file="start_btn2.png")
    img_rules_page = PhotoImage(file="rules_page.png")
    img_rules_btn = PhotoImage(file="rules_btn.png")
    img_won = PhotoImage(file="won.png")
    img_lost = PhotoImage(file="lost.png")
    img_country = PhotoImage(file="country.png")
    img_food = PhotoImage(file="food.png")
    img_vocab = PhotoImage(file="vocab.png")
    img_all = PhotoImage(file="all.png")
    
    # Load and create canvases
    global intro_canvas, rules_canvas, home_canvas, game_canvas, ending_canvas
    intro_canvas = intro(root)
    intro_canvas.pack()
    
    rules_canvas = rules(root)
    home_canvas = home(root)
    game_canvas = game(root)
    ending_canvas = ending(root)
    
    # Loop background music continuously 
    winsound.PlaySound("music.wav", winsound.SND_LOOP | winsound.SND_ASYNC)


    mainloop()

# ------------------------ Start main game with function ---------------------
main()

# Stop all sounds when the program is done
winsound.PlaySound(None, winsound.SND_PURGE)
