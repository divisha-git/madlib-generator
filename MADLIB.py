from tkinter import *
import tkinter.messagebox as MessageBox
import sqlite3

root = Tk()
root.withdraw() 

def setup_database():
    """Create the users table in the database if it doesn't exist."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def login(login_window):
    """Authenticate the user and open the Madlibs game upon successful login."""
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        MessageBox.showinfo("Login Success", f"Welcome, {username}!")
        login_window.destroy() 
        open_madlibs()         
    else:
        MessageBox.showerror("Login Failed", "Invalid Username or Password")


def register_and_open_madlibs(reg_window):
    """Register a new user and open the Madlibs game."""
    
    if not en1.get() or not en3.get() or not en4.get() or not en6.get() or not en7.get():
        MessageBox.showerror("Input Error", "Please fill all fields.")
        return
    if en6.get() != en7.get():
        MessageBox.showerror("Password Error", "Passwords do not match.")
        return

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (en3.get(), en6.get()))
        conn.commit()
        MessageBox.showinfo("Registration Success", "Account created successfully!")
        reg_window.destroy()   
        open_madlibs()         
    except sqlite3.IntegrityError:
        MessageBox.showerror("Registration Failed", "Username already exists.")
    finally:
        conn.close()

def open_madlibs():
    """Create the main Madlibs game window."""
    madlibs_window = Toplevel(root)
    madlibs_window.geometry("600x800") 
    madlibs_window.title("Madlibs Game")
    madlibs_window.config(bg='#E6E6FA')

    Label(madlibs_window, text="Madlibs Stories", font=('Arial', 24, 'bold'), bg='#8B8386', fg='White', width=30).pack(pady=10)
    labels = ["Name", "Noun", "Adjective", "Verb", "Noun", "Candy", "Food", "Adjective", "Noun", "Adjective"]
    entries = []
    for i, label in enumerate(labels):
        frame = Frame(madlibs_window, bg='#E6E6FA')
        frame.pack(pady=5)
        lb = Label(frame, text=label + ":", font=('Arial', 14, 'bold'), bg='#E6E6FA')
        lb.pack(side=LEFT, padx=10)
        en = Entry(frame, width=30, relief='solid', font=('Arial', 12))
        en.pack(side=LEFT, padx=10)
        entries.append(en)

    en1, en2, en3, en4, en5, en6, en7, en8, en9, en10 = entries

    def clear_fields():
        """Clear all input fields."""
        for entry in entries:
            entry.delete(0, END)

    def display_story(txt):
        """Display the generated story in a new window."""
        nx = Toplevel(madlibs_window)
        nx.geometry("500x400")
        nx.title("Your Story")
        nx.config(bg='#EEE0E5')
        Label(nx, text="Your Story", font=('Arial', 20, 'bold'), bg='#EEE0E5').pack(pady=15)
        story_text = Label(nx, text=txt, font=('Arial', 14), bg='#EEE0E5', justify='left', wraplength=480)
        story_text.pack(pady=10, padx=10)

    def open_shopping_stories():
        """Open Shopping Stories."""
        shopping_page = Toplevel(madlibs_window)
        shopping_page.geometry("500x500")
        shopping_page.title("Shopping Stories")
        shopping_page.config(bg='#EEE0E5')

        shopping_stories = [
           ("A Day at the Mall",
             f"{en1.get()} woke up excited for a day of shopping. They decided to head to the {en2.get()} mall, known for its endless options. Upon arriving, they were amazed by the vast selection of {en3.get()} stores. After exploring a few shops, they found the perfect {en4.get()} they had been searching for. With a bag full of {en5.get()} goodies, they couldn't wait to share their adventures with friends."),
            ("The Crowded Experience",
             f"Last Saturday, {en1.get()} decided to go shopping for some {en2.get()} supplies. The mall was incredibly crowded, filled with people eager to find deals. After wandering through countless stores, they finally spotted a fantastic {en3.get()} on sale. But just as they were about to purchase it, they had to dodge a group of {en4.get()} racing through the aisle, making it quite the adventure."),
            ("Snack Attack",
             f"As {en1.get()} roamed the mall, their stomach began to rumble. They made a quick stop at the food court, where the scent of delicious {en2.get()} filled the air. {en1.get()} couldn't resist trying some {en3.get()} candy, and it was the best decision ever! They ended the day with a full stomach and a bag of {en4.get()} to take home, eager for the next shopping trip."),
            ("The Shopping Adventure",
             f"On a sunny afternoon, {en1.get()} decided it was time to refresh their wardrobe. They visited a popular {en2.get()} store where the staff were extremely helpful. With a fantastic selection of {en3.get()} clothes and accessories, {en1.get()} spent hours trying on different styles. They left the store feeling fabulous with a bag full of new outfits that were all {en4.get()} and stylish.")
        ]

        for title, story in shopping_stories:
            Button(shopping_page, text=title, font=('Arial', 12, 'bold'), width=50,
                   command=lambda s=story: display_story(s)).pack(pady=10)

    def open_drama_stories():
        """Open Drama Stories."""
        drama_page = Toplevel(madlibs_window)
        drama_page.geometry("500x500")
        drama_page.title("Drama Stories")
        drama_page.config(bg='#EEE0E5')

        drama_stories = [
            ("Facing Challenges", f"In a world where {en1.get()} faced {en2.get()} challenges, they had to {en3.get()} to overcome it all."),
            ("The Big Secret", f"The drama unfolded when {en1.get()} discovered a {en4.get()} secret that changed everything."),
            ("A Moment of Clarity", f"Amidst the chaos, {en1.get()} had a {en5.get()} moment that led to an unexpected {en6.get()}."),
            ("Unity in Storm", f"In the end, it was {en1.get()}'s {en7.get()} that brought everyone together after the storm.")
        ]

        for title, story in drama_stories:
            Button(drama_page, text=title, font=('Arial', 12, 'bold'), width=50,
                   command=lambda s=story: display_story(s)).pack(pady=10)

    def open_action_stories():
        """Open Action Stories."""
        action_page = Toplevel(madlibs_window)
        action_page.geometry("500x500")
        action_page.title("Action Stories")
        action_page.config(bg='#EEE0E5')

        action_stories = [
            ("Jumping Into Action", f"{en1.get()} jumped into action when {en2.get()} appeared, ready to {en3.get()} at any moment!"),
            ("Courageous Encounter", f"With a {en4.get()} in hand, {en1.get()} faced the enemy with {en5.get()} courage."),
            ("Saving the Day", f"Explosions rocked the city as {en1.get()} ran towards the {en6.get()} to save the day!"),
            ("The Final Showdown", f"In the final showdown, it was {en7.get()}'s {en8.get()} that made the difference.")
        ]

        for title, story in action_stories:
            Button(action_page, text=title, font=('Arial', 12, 'bold'), width=50,
                   command=lambda s=story: display_story(s)).pack(pady=10)

    def open_humor_stories():
        """Open Humor Stories."""
        humor_page = Toplevel(madlibs_window)
        humor_page.geometry("500x500")
        humor_page.title("Humor Stories")
        humor_page.config(bg='#EEE0E5')

        humor_stories = [
            ("Why Did the Chicken?", f"Why did {en1.get()} cross the road? To get to the {en2.get()} on the other side!"),
            ("Baking Fiasco", f"{en1.get()} tried to make a {en3.get()} cake, but ended up with a {en4.get()} disaster!"),
            ("Slippery Situation", f"At the {en5.get()}, {en1.get()} slipped on a {en6.get()} and fell into a {en7.get()} pool!"),
            ("Sharing Laughter", f"Finally, {en1.get()} realized that the best {en8.get()} is the one shared with friends!")
        ]

        for title, story in humor_stories:
            Button(humor_page, text=title, font=('Arial', 12, 'bold'), width=50,
                   command=lambda s=story: display_story(s)).pack(pady=10)

    def open_fantasy_stories():
        """Open Fantasy Stories."""
        fantasy_page = Toplevel(madlibs_window)
        fantasy_page.geometry("500x500")
        fantasy_page.title("Fantasy Stories")
        fantasy_page.config(bg='#EEE0E5')

        fantasy_stories = [
           ("A Magical Journey",
             f"Once upon a time, {en1.get()} found a {en2.get()} that led to a hidden kingdom. As they stepped through, they were greeted by {en3.get()} creatures and enchanted {en4.get()} that sparkled in the sunlight. Each day was filled with adventures, from flying on {en5.get()} to battling {en6.get()} that threatened their newfound friends. {en1.get()} learned that true magic lies in courage and friendship."),
            ("The Prophecy Unfolds",
             f"In a world filled with {en1.get()} creatures, it was foretold that only a hero could save the realm from darkness. When {en2.get()} discovered their unique {en3.get()} abilities, they knew it was time to embrace their destiny. With the help of a wise {en4.get()} and loyal companions, they embarked on a quest to defeat the {en5.get()} threatening their homeland."),
            ("The Hero's Call",
             f"With a {en1.get()} in hand, the journey began for {en2.get()} and their loyal {en3.get()}. They traversed mystical forests and treacherous mountains, facing trials that tested their {en4.get()} and bravery. Along the way, they encountered {en5.get()} who joined their cause, creating an unbreakable bond. Together, they would face the ultimate challenge to restore peace to their world."),
            ("Quest for Knowledge",
             f"{en1.get()} sought the {en2.get()} of wisdom from the ancient {en3.get()} elder who lived atop a mountain. The journey was fraught with challenges, including {en4.get()} that tried to stop them at every turn. But with determination and the help of unexpected allies, {en1.get()} discovered secrets that would change their destiny and the fate of the kingdom forever.")
        ]

        for title, story in fantasy_stories:
            Button(fantasy_page, text=title, font=('Arial', 12, 'bold'), width=50,
                   command=lambda s=story: display_story(s)).pack(pady=10)

    def open_fairy_tale_stories():
        """Open Fairy Tale Stories."""
        fairy_tale_page = Toplevel(madlibs_window)
        fairy_tale_page.geometry("500x500")
        fairy_tale_page.title("Fairy Tale Stories")
        fairy_tale_page.config(bg='#EEE0E5')

        fairy_tale_stories = [
            ("The Brave Hero", f"Once upon a time, {en1.get()} lived in a {en2.get()} castle with a {en3.get()} dragon."),
            ("The Enchanted Forest", f"Every day, {en1.get()} would {en4.get()} to the enchanted {en5.get()} to seek adventure."),
            ("A Wish Granted", f"One fateful night, a {en6.get()} arrived, promising to grant {en1.get()} a {en7.get()} wish."),
            ("The Kingdom's Savior", f"In the end, it was the love of a {en8.get()} that saved the kingdom from darkness.")
        ]

        for title, story in fairy_tale_stories:
            Button(fairy_tale_page, text=title, font=('Arial', 12, 'bold'), width=50,
                   command=lambda s=story: display_story(s)).pack(pady=10)

    Button(madlibs_window, text="Shopping", font=('Arial', 15, 'bold'), bd=5, command=open_shopping_stories).place(x=50, y=600)
    Button(madlibs_window, text="Drama", font=('Arial', 15, 'bold'), bd=5, command=open_drama_stories).place(x=300, y=600)
    Button(madlibs_window, text="Action", font=('Arial', 15, 'bold'), bd=5, command=open_action_stories).place(x=50, y=660)
    Button(madlibs_window, text="Humor", font=('Arial', 15, 'bold'), bd=5, command=open_humor_stories).place(x=300, y=660)
    Button(madlibs_window, text="Fantasy", font=('Arial', 15, 'bold'), bd=5, command=open_fantasy_stories).place(x=50, y=720)
    Button(madlibs_window, text="Fairy Tale", font=('Arial', 15, 'bold'), bd=5, command=open_fairy_tale_stories).place(x=300, y=720)
    Button(madlibs_window, text="Clear Fields", font=('Arial', 15, 'bold'), bd=5, command=clear_fields).place(x=175, y=780)

def open_login_page():
    """Create the login window."""
    global login_window, username_entry, password_entry
    login_window = Toplevel(root)
    login_window.geometry("400x300")
    login_window.title("Login")
    login_window.config(bg='#F7F7F7')

    Label(login_window, text="Login to Madlibs", font=('Arial', 20, 'bold'), bg='#F7F7F7').pack(pady=20)

    frame_username = Frame(login_window, bg='#F7F7F7')
    frame_username.pack(pady=10)
    Label(frame_username, text="Username:", font=('Arial', 12), bg='#F7F7F7').pack(side=LEFT, padx=10)
    username_entry = Entry(frame_username, font=('Arial', 12))
    username_entry.pack(side=LEFT)

    frame_password = Frame(login_window, bg='#F7F7F7')
    frame_password.pack(pady=10)
    Label(frame_password, text="Password:", font=('Arial', 12), bg='#F7F7F7').pack(side=LEFT, padx=10)
    password_entry = Entry(frame_password, show='*', font=('Arial', 12))
    password_entry.pack(side=LEFT)

    Button(login_window, text="Login", width=15, font=('Arial', 12, 'bold'), command=lambda: login(login_window)).pack(pady=20)
    Button(login_window, text="Register", width=15, font=('Arial', 12, 'bold'), command=open_registration_page).pack()

def open_registration_page():
    """Create the registration window."""
    reg_window = Toplevel(root)
    reg_window.geometry("500x500")
    reg_window.title("Registration Form")
    reg_window.config(bg='#F7F7F7')

    Label(reg_window, text="Create an Account", font=("Arial", 20, "bold"), bg='#F7F7F7').pack(pady=20)

    fields = [
        ("Enter Name:", "name"),
        ("Enter Username:", "username"),
        ("Contact Number:", "contact"),
        ("Enter Password:", "password"),
        ("Re-Enter Password:", "confirm_password")
    ]

    entries = {}
    for label_text, key in fields:
        frame = Frame(reg_window, bg='#F7F7F7')
        frame.pack(pady=10)
        Label(frame, text=label_text, font=("Arial", 12), bg='#F7F7F7').pack(side=LEFT, padx=10)
        entry = Entry(frame, show='*' if 'Password' in label_text else '', font=("Arial", 12))
        entry.pack(side=LEFT)
        entries[key] = entry

    global en1, en3, en4, en6, en7
    en1 = entries["name"]
    en3 = entries["username"]
    en4 = entries["contact"]
    en6 = entries["password"]
    en7 = entries["confirm_password"]

    Button(reg_window, text="Register", width=15, font=("Arial", 12, "bold"),
           command=lambda: register_and_open_madlibs(reg_window)).pack(pady=30)

setup_database()

open_login_page()

root.mainloop()