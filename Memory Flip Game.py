# =============================================================================
# A NICHE GAME — MEMORY FLIP GAME
# =============================================================================

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from tkinter import *
import random
import pygame
import time
import ast
import os


# -----------------------------------------------------------------------------
# File Locations
# -----------------------------------------------------------------------------
baseFolder=os.path.dirname(os.path.abspath(__file__))
leaderboardFolder=os.path.join(baseFolder, "leaderboards")+os.sep
iconFolder=os.path.join(baseFolder, "icon")+os.sep
imageFolder=os.path.join(baseFolder, "images")+os.sep
soundFolder=os.path.join(baseFolder, "sounds")+os.sep


# -----------------------------------------------------------------------------
# Root Window Setup
# -----------------------------------------------------------------------------
root=Tk()
#root=customtkinter.CTk()
root.rowconfigure(0, weight=1) # Row 0 and Column 0 are allowed to expand when the window grows.
root.columnconfigure(0, weight=1)
root.title("A Niche Game")
root.config(bg="#d3d3d3")
root.state("zoomed") # Ensure it pop up in full screen

# Safeguard
try:
    # Folder Path + File Name
    root.iconbitmap(iconFolder+"logo.ico")
except Exception as e: # There can be more than one error
    print(f"⚠️  Icon not loaded: {e}")
    pass # Go with default setting if error


# =============================================================================
# FRAME MANAGEMENT
# =============================================================================
mfgFrame=Frame(root, bg="#d3d3d3") # Memory Flip Game Frame
mfgFrame.grid(row=0, column=0, sticky="nsew")
mfgFrame.columnconfigure((0, 1), weight=1) # Centering the gadgets in mfg frame
mfgFrame.rowconfigure((0), weight=1)

# =============================================================================
# SOUND SYSTEM
# =============================================================================
# Sound player
pygame.mixer.init()
def play_sound(path):
    try:
        sound=pygame.mixer.Sound(path)
        sound.play()
    except Exception as e:
        print(f"⚠️   Sound not loaded: {e}")
        return


# Request for username
username=""

# =============================================================================
# TOOLS FOR MFG
# =============================================================================
# Timer
def stopwatch(frame):
    timer=Entry(frame)
    timer.insert(0, "0.0 sec")
    timer.config(state="readonly")
    return timer

# Timer variables
running=False
starttime=0
elapsed=0.0

def stop_stopwatch():
    global running
    
    running=False

def update_timer():
    global running, starttime, elapsed
    
    if running:
        elapsed=round(time.time() - starttime, 1)
        timer.config(state="normal")
        timer.delete(0, END)
        timer.insert(0, f"{elapsed} sec")
        timer.config(state="readonly")
        mfgFrame.after(100, update_timer)  # Updates every 0.1 second

def start_stopwatch():
    global running, starttime
    if not running:
        starttime=time.time()-elapsed  # Set starttime to time on timer before setting is clicked
        running=True
        update_timer()
        
def reset_stopwatch():
    global running, starttime, elapsed
    running=False
    starttime=0
    elapsed=0.0
        
# =============================================================================
# MEMORY FLIP GAME
# =============================================================================

# -----------------------------------------------------------------------------
# Frames for aligning gadgets easily
# -----------------------------------------------------------------------------
# Left
mfg_leftFrame=Frame(mfgFrame) # Reset and Options Frame
mfg_leftFrame.config(bg="#d3d3d3")

mfg_headerFrame=Frame(mfg_leftFrame) # Header Frame
mfg_headerFrame.config(bg="#d3d3d3")

mfg_cardFrame=Frame(mfg_leftFrame) # Cards Frame
mfg_headerFrame.config(bg="#d3d3d3")

# Right
mfg_rightFrame=Frame(mfgFrame) # Reset and Options Frame
mfg_rightFrame.config(bg="#d3d3d3")

mfg_functionFrame=Frame(mfg_rightFrame) # Reset and Options Frame
mfg_functionFrame.config(bg="#d3d3d3")


# -----------------------------------------------------------------------------
# Cards randomizer
# -----------------------------------------------------------------------------
count=0

characters=["🎃", "✨", "🍬", "🧟", "🐈", "🧛", "🍫", "🧙"] # Given Characters

for addChars in range(len(characters)): # Double the characters
    characters.append(characters[addChars])

random.shuffle(characters)

row0=characters[0: 4] # Assigning them to individual row
row1=characters[4: 8]
row2=characters[8: 12]
row3=characters[12: 16]


# -----------------------------------------------------------------------------
# Initiating variables
# -----------------------------------------------------------------------------
first="" # To check if the two flip are correct
second=""

mark1="" # To mark the two flips
mark2=""

turns=0 # To count and display the number of turns
Paired=0 # To stop the game if everything is paired

elapsed=0 # Initiate elapsed start point
cheer_type="" # To ensure to only change message if it is a different cheer type


# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
# Turn Counter
turncounter=Entry(mfg_headerFrame, width=10, borderwidth=5, font=("Times New Roman", 18), justify=CENTER) 
turncounter.insert(0, "Turns: 0")
turncounter.config(state="readonly")

# Greet & Cheer Box
txt=Entry(mfg_headerFrame, width=35, borderwidth=5, font=("Times New Roman", 18), justify=CENTER) 

# Greeting message and initiate
greetings=["🎮 Welcome to Memory Flip Madness!", 
           "🧠 Ready to test that memory?", 
           "✨ Let’s see how sharp you are today!", 
           "🔥 Match them all — let’s go!", 
           "💫 Flip, focus, and find the pairs!", 
           "👀 Keep your eyes on the emojis!"]
txt.insert(0, str(random.choice(greetings)))
txt.config(state="readonly")

# -----------------------------------------------------------------------------
# Leaderboard
# -----------------------------------------------------------------------------
# Leaderboard system with recording features
leaderboard=Text(mfg_rightFrame, width=45, height=13, borderwidth=5, font=("Times New Roman", 18)) # Leaderboard

# Create a tag that centers text
leaderboard.tag_configure("center", justify="center")

# Displaying leaderboard from txt
def load_leaderboard():
    leaderboard.config(state="normal") # Allow it to be written only by computer
    
    leaderboard.delete("1.0", END)
    leaderboard.insert("1.0", "🏆 Leaderboard (Top 10) 🏆\n====================================\n", "center")

    Fullleaderboard=[]
    # Load leaderboard safely
    try:
        # Check if the file exist
        with open(leaderboardFolder+"mfg_leaderboard.txt", "r", encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                try:
                    data=ast.literal_eval(line)
                    if isinstance(data, list) and len(data)==3:
                        Fullleaderboard.append(data)
                except (SyntaxError, ValueError):
                    continue
    except FileNotFoundError:
        # Create the file if it doesn't exist
        open(leaderboardFolder+"mfg_leaderboard.txt", "w", encoding="utf-8").close()
        leaderboard.insert(END, "No records yet — be the first to play!\n", "center")
        return

    # Sort leaderboard
    Fullleaderboard.sort(key=lambda x: (x[0], x[1]))

    if not Fullleaderboard:
        leaderboard.insert(END, "No records yet — be the first to play!\n", "center")
    else:
        for i, display in enumerate(Fullleaderboard[:10], start=1):
            leaderboard.insert(
                END,
                f"{i}. ⏱ {display[0]} sec | 🔄 {display[1]} turns | 👤 {display[2]}\n",
                "center"
            )
    
    leaderboard.config(state="disabled") # Make it read-only for user

load_leaderboard()

# -----------------------------------------------------------------------------
# Memory Flip Game related sub-programs
# -----------------------------------------------------------------------------         
# Recording all victory into the txt
def record():
    leaderboard.config(state="normal")
    
    global turns, elapsed, username

    Fullleaderboard=[]

    # Load leaderboard safely
    try:
        with open(leaderboardFolder+"mfg_leaderboard.txt", "r", encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                try:
                    data=ast.literal_eval(line)
                    if isinstance(data, list) and len(data)==3:
                        Fullleaderboard.append(data)
                except (SyntaxError, ValueError):
                    continue
    except FileNotFoundError:
        pass  # File will be created later

    # Add the new record
    Fullleaderboard.append([elapsed, turns, username])

    # Sort by best time, then least turns
    Fullleaderboard.sort(key=lambda x: (x[0], x[1]))

    # Update the Text leaderboard display
    leaderboard.delete("1.0", END)
    leaderboard.insert("1.0", "🏆 Leaderboard (Top 10) 🏆\n====================================\n", "center")

    for i, display in enumerate(Fullleaderboard[:10], start=1):
        leaderboard.insert(
            END,
            f"{i}. ⏱ {display[0]} sec | 🔄 {display[1]} turns | 👤 {display[2]}\n",
            "center"
        )

    # Re-write the full leaderboard back to file
    with open(leaderboardFolder+"mfg_leaderboard.txt", "w", encoding="utf-8") as f:
        for wr in Fullleaderboard:
            f.write(str(wr) + "\n")
            
    leaderboard.config(state="disabled")
    
    

# Cheering Statements
def cheering_message():
    global turns, Paired, cheer_type
    
    temp=""
    messages=["Keep going!"]  # Default fallback
    
    # Early game encouragement
    if Paired==0 and turns<=2:
        temp="encouragement"
    # First success
    elif Paired==1:
        temp="first success"
    # In progress
    elif 2<=Paired<4:
        temp="progress"
    # Halfway there
    elif Paired==4:
        temp="halfway"
    # Near the end
    elif 4<Paired<7:
        temp="close end"
    # All pairs found
    elif Paired==8:
        if turns<=16:
            temp="perfect success"
        else:
            temp="success"
    # If the player is struggling
    elif turns>24 and Paired<8:
        temp="struggle"
    
    if not temp or cheer_type==temp: # Exit the subprogram is there is nothing in temp and cheertype is the same as temp
        return
    
    cheer_type=temp
    if cheer_type=="encouragement":
        messages=["Let’s warm up!", "You got this!", "Take your time to memorize!"]
    # First success
    elif cheer_type=="first success":
        messages=["Nice start!", "First pair down!", "Great memory!"]
    # In progress
    elif cheer_type=="progress":
        messages=["Keep it going!", "Good job!", "Stay focused!", "You’re improving!"]
    # Halfway there
    elif cheer_type=="halfway":
        messages=["Halfway there!", "Nice rhythm!", "You’re on fire!"]
    # Near the end
    elif cheer_type=="close end":
        messages=["Almost done!", "You’re crushing it!", "Memory beast mode!", "Just a few left!"]
    # All pairs found
    elif cheer_type=="perfect success":
        messages=["🏆 Perfect memory!", "Flawless win!", "Unstoppable!", "You’re a legend!"]
    elif cheer_type=="success":
        messages=["🏁 Well done!", "Victory achieved!", "Persistence pays off!", "You did it!"]
    # If the player is struggling
    elif cheer_type=="struggle":
        messages=["Keep going!", "You’re doing great!", "Don’t give up now!"]
    
    text=str(random.choice(messages))
    txt.config(state="normal")
    
    txt.delete(0, END)
    txt.insert(0, text)
    
    txt.config(state="readonly")

# Check if the first and second number are the same
def check():
    global first, second, turns, Paired, mark1, mark2
    
    if first==second:
        mark1.config(state=DISABLED)
        mark2.config(state=DISABLED)
        Paired+=1
        
        # To notify the user if it is correct
        play_sound(soundFolder+"rightanswer-95219.mp3")
        
        
        if Paired==8:
            stop_stopwatch() # To stop the stopwatch
            record() # To record the win
            # Sound of victory
            play_sound(soundFolder+"winner-game-sound-404167.mp3")
    else:
        mark1.config(text="")
        mark2.config(text="")
        
        # To notify the user if it is wrong
        play_sound(soundFolder+"wronganswer-37702.mp3")
    
    first="" # Reset for another flip
    second=""
        
    mark1=""
    mark2=""
    cheering_message() # Call cheering message
    
# Flipping the card
def flip(num1, num2):      
    global first, second, username
    
    global r0c0, r0c1, r0c2, r0c3
    global r1c0, r1c1, r1c2, r1c3
    global r2c0, r2c1, r2c2, r2c3
    global r3c0, r3c1, r3c2, r3c3
    
    global running
    
    global mark1, mark2
    
    global turns
    global Paired
    
    if username=="":
        txt.config(state="normal")
        txt.delete(0, END)
        txt.insert(0, "Set your username before playing!")
        txt.config(state="readonly")
        usernameBox.focus_set()
        return
    
    if not running: # To start the timer
        start_stopwatch()
        
    if second=="": # To disable clicking after second is filled up (Spam proof)        
        # One section for one row
        if num1=="r0": # Button in row 0
            if num2=="c0": # In column 0
                r0c0.config(text=row0[0])
                if first=="":
                    first=row0[0] # Pick up emoji from row0 list at index 0 accordingly
                    mark1=r0c0 # Mark the button
                else:
                    second=row0[0] # Send it as second number if first number is filled
                    mark2=r0c0
            if num2=="c1":
                r0c1.config(text=row0[1])
                if first=="":
                    first=row0[1]
                    mark1=r0c1
                else:
                    second=row0[1]
                    mark2=r0c1
            if num2=="c2":
                r0c2.config(text=row0[2])
                if first=="":
                    first=row0[2]
                    mark1=r0c2
                else:
                    second=row0[2]
                    mark2=r0c2
            if num2=="c3":
                r0c3.config(text=row0[3])
                if first=="":
                    first=row0[3]
                    mark1=r0c3
                else:
                    second=row0[3]
                    mark2=r0c3
                    
        if num1=="r1": 
            if num2=="c0":
                r1c0.config(text=row1[0])
                if first=="":
                    first=row1[0]
                    mark1=r1c0
                else:
                    second=row1[0]
                    mark2=r1c0
            if num2=="c1":
                r1c1.config(text=row1[1])
                if first=="":
                    first=row1[1]
                    mark1=r1c1
                else:
                    second=row1[1]
                    mark2=r1c1
            if num2=="c2":
                r1c2.config(text=row1[2])
                if first=="":
                    first=row1[2]
                    mark1=r1c2
                else:
                    second=row1[2]
                    mark2=r1c2
            if num2=="c3":
                r1c3.config(text=row1[3])
                if first=="":
                    first=row1[3]
                    mark1=r1c3
                else:
                    second=row1[3]
                    mark2=r1c3
                    
        if num1=="r2": 
            if num2=="c0":
                r2c0.config(text=row2[0])
                if first=="":
                    first=row2[0]
                    mark1=r2c0
                else:
                    second=row2[0]
                    mark2=r2c0
            if num2=="c1":
                r2c1.config(text=row2[1])
                if first=="":
                    first=row2[1]
                    mark1=r2c1
                else:
                    second=row2[1]
                    mark2=r2c1
            if num2=="c2":
                r2c2.config(text=row2[2])
                if first=="":
                    first=row2[2]
                    mark1=r2c2
                else:
                    second=row2[2]
                    mark2=r2c2
            if num2=="c3":
                r2c3.config(text=row2[3])
                if first=="":
                    first=row2[3]
                    mark1=r2c3
                else:
                    second=row2[3]
                    mark2=r2c3
                    
        if num1=="r3": 
            if num2=="c0":
                r3c0.config(text=row3[0])
                if first=="":
                    first=row3[0]
                    mark1=r3c0
                else:
                    second=row3[0]
                    mark2=r3c0
            if num2=="c1":
                r3c1.config(text=row3[1])
                if first=="":
                    first=row3[1]
                    mark1=r3c1
                else:
                    second=row3[1]
                    mark2=r3c1
            if num2=="c2":
                r3c2.config(text=row3[2])
                if first=="":
                    first=row3[2]
                    mark1=r3c2
                else:
                    second=row3[2]
                    mark2=r3c2
            if num2=="c3":
                r3c3.config(text=row3[3])
                if first=="":
                    first=row3[3]
                    mark1=r3c3
                else:
                    second=row3[3]
                    mark2=r3c3

        if mark1==mark2:
            mark2=""
            second=""
        else:
            # To play sound effect when flipping
            play_sound(soundFolder+"20243__koops__page_turn_09.wav")
        
        if first!="" and second!="":
            turns+=1
            turncounter.config(state="normal")
            
            turncounter.delete(0, END)
            turncounter.insert(0, "Turns: "+str(turns))
            
            turncounter.config(state="readonly")
            mfgFrame.after(500, check)

def reset():
    global characters, count, row0, row1, row2, row3, first, second, mark1, mark2, turns, turncounter, Paired, txt
    global r0c0, r0c1, r0c2, r0c3, r1c0, r1c1, r1c2, r1c3, r2c0, r2c1, r2c2, r2c3, r3c0, r3c1, r3c2, r3c3
    global elapsed, pauseState
    
    fullList=[] # Resetting fullList for re-shuffle
    count=0 # Restart counting till 16
    
    random.shuffle(characters)
    
    row0=characters[0: 4] # Assigning them to individual row
    row1=characters[4: 8]
    row2=characters[8: 12]
    row3=characters[12: 16]
    
    # Resetting all neccessary variables
    first="" # To check if the two flip are correct
    second=""

    mark1="" # To mark the two flips
    mark2=""

    turns=0 # To count and display the number of turns
    turncounter.delete(0, END)
    turncounter.insert(0, "Turns: 0") # Reset turn counter
    
    Paired=0 # To stop the game if everything is paired
    
    # Special Resetting Statements
    resetState=["New board — round two!", 
                "Fresh start! Let’s go!", 
                "Try again, memory champ!", 
                "Reset done — focus up!", 
                "Clean slate, new luck!", 
                "They shuffled again 😏", 
                "Back to the start!", 
                "Board cleared — go win!", 
                "Fresh challenge ahead!", 
                "Let’s see you beat this!"]
    
    txt.config(state="normal")
    txt.delete(0, END)
    txt.insert(0, str(random.choice(resetState)))
    txt.config(state="readonly")
    
    # Enabling and clearig the flips
    r0c0.config(text="", state=NORMAL)
    r0c1.config(text="", state=NORMAL)
    r0c2.config(text="", state=NORMAL)
    r0c3.config(text="", state=NORMAL)
    
    r1c0.config(text="", state=NORMAL)
    r1c1.config(text="", state=NORMAL)
    r1c2.config(text="", state=NORMAL)
    r1c3.config(text="", state=NORMAL)
    
    r2c0.config(text="", state=NORMAL)
    r2c1.config(text="", state=NORMAL)
    r2c2.config(text="", state=NORMAL)
    r2c3.config(text="", state=NORMAL)
    
    r3c0.config(text="", state=NORMAL)
    r3c1.config(text="", state=NORMAL)
    r3c2.config(text="", state=NORMAL)
    r3c3.config(text="", state=NORMAL)
    

    stop_stopwatch() # To stop the stopwatch if running
    
    timer.config(state="normal")
    elapsed=0.0
    timer.delete(0, END) # Reset timer
    timer.insert(0, f"{elapsed} sec")
    timer.config(state="readonly")

# Confirm the username used when a victory is saved to the leaderboard
def enter_username(event=None):
    global username
    
    enteredUsername=usernameBox.get().strip()
    
    if enteredUsername=="" or enteredUsername=="Enter username":
        txt.config(state="normal")
        txt.delete(0, END)
        txt.insert(0, "Please enter a username first!")
        txt.config(state="readonly")
        return
    
    username=enteredUsername
    
    txt.config(state="normal")
    txt.delete(0, END)
    txt.insert(0, "Welcome, "+username+"!")
    txt.config(state="readonly")

# -----------------------------------------------------------------------------
# Cards
# -----------------------------------------------------------------------------
r0c0=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r0", "c0"), borderwidth=2, font=("Arial", 30))
r0c1=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r0", "c1"), borderwidth=2, font=("Arial", 30))
r0c2=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r0", "c2"), borderwidth=2, font=("Arial", 30))
r0c3=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r0", "c3"), borderwidth=2, font=("Arial", 30))

r1c0=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r1", "c0"), borderwidth=2, font=("Arial", 30))
r1c1=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r1", "c1"), borderwidth=2, font=("Arial", 30))
r1c2=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r1", "c2"), borderwidth=2, font=("Arial", 30))
r1c3=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r1", "c3"), borderwidth=2, font=("Arial", 30))

r2c0=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r2", "c0"), borderwidth=2, font=("Arial", 30))
r2c1=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r2", "c1"), borderwidth=2, font=("Arial", 30))
r2c2=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r2", "c2"), borderwidth=2, font=("Arial", 30))
r2c3=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r2", "c3"), borderwidth=2, font=("Arial", 30))

r3c0=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r3", "c0"), borderwidth=2, font=("Arial", 30))
r3c1=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r3", "c1"), borderwidth=2, font=("Arial", 30))
r3c2=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r3", "c2"), borderwidth=2, font=("Arial", 30))
r3c3=Button(mfg_cardFrame, text="", width=7, height=3, command=lambda: flip("r3", "c3"), borderwidth=2, font=("Arial", 30))

usernameBox=Entry(mfg_functionFrame, borderwidth=4, width=16, font=("TkDefaultFont", 20))
usernameBox.insert(0, "Enter username")
usernameBox.bind("<Return>", enter_username)
button_username=Button(mfg_functionFrame, text="Set Username", borderwidth=4, width=15, pady=2, font=("TkDefaultFont", 20), command=enter_username)
button_reset=Button(mfg_functionFrame, text="Retry", borderwidth=4, width=15, pady=2, font=("TkDefaultFont", 20), command=reset)
button_exit=Button(mfg_functionFrame, text="Quit", borderwidth=4, width=15, pady=2, font=("TkDefaultFont", 20), command=root.quit)

# -----------------------------------------------------------------------------
# Placement
# -----------------------------------------------------------------------------
# Largest Frame
mfg_leftFrame.grid(row=0, column=0, sticky="nsew", padx=(40, 0), pady=30)
mfg_rightFrame.grid(row=0, column=1, sticky="nsew", padx=(0, 40), pady=30)

# Placements of smaller frame in a largest frame
# Left
mfg_headerFrame.pack(side=TOP)
mfg_cardFrame.pack(side=BOTTOM)

# Right
timer=stopwatch(mfg_rightFrame) # Getting the timer into the frame
timer.config(width=20, borderwidth=5, font=("Times New Roman", 18), justify=CENTER)
timer.pack(side=TOP)
leaderboard.pack(pady=(40, 0))
mfg_functionFrame.pack(side=BOTTOM, padx=(0, 52))

# Placing within the Frames
# mfg card frame
r0c0.grid(row=1, column=0)
r0c1.grid(row=1, column=1)
r0c2.grid(row=1, column=2)
r0c3.grid(row=1, column=3)

r1c0.grid(row=2, column=0)
r1c1.grid(row=2, column=1)
r1c2.grid(row=2, column=2)
r1c3.grid(row=2, column=3)

r2c0.grid(row=3, column=0)
r2c1.grid(row=3, column=1)
r2c2.grid(row=3, column=2)
r2c3.grid(row=3, column=3)

r3c0.grid(row=4, column=0)
r3c1.grid(row=4, column=1)
r3c2.grid(row=4, column=2)
r3c3.grid(row=4, column=3)

# mfg header frame
turncounter.pack(side=LEFT, padx=10)
txt.pack(side=RIGHT, padx=10)

# mfg function frame
usernameBox.grid(row=0, column=1)
button_username.grid(row=1, column=1, pady=5)
button_reset.grid(row=2, column=1, pady=5)
button_exit.grid(row=3, column=1)

mfgFrame.tkraise()
root.mainloop()
