import requests
from tkinter import *
from PIL import Image,ImageTk
import shutil
import random
import sys
import time

# Importing the required modules


def poke(p):
    '''
    The function takes the parameter  p, which is the JSON file provided by the API.
    It initiates a tkinter window for a GUI.
    Then, it gets the various object properties from the JSON file.
    After that, it prints the properties and the sprite on to the tkinter Window

    '''

    tk = Tk()
    canvas = Canvas(tk, width=570, height=450, bd=0, highlightthickness=0)
    canvas.pack()
    tk.title("Pokedex v1.0")
    tk.resizable(0,0)
    pokename =p["name"]
    id = p["national_id"]
    description = requests.get("http://pokeapi.co" + p["descriptions"][0]["resource_uri"]).json()
    description = description["description"]

    stats = [p["hp"],p["attack"],p["defense"],p["sp_atk"],p["sp_def"]]
    statnames = ["HP : ","Attack : ","Defense : ","Spl. Attack : ","Spl. Defense : "]

    sprout = requests.get("http://pokeapi.co" + p["sprites"][0]["resource_uri"]).json()
    sprite = "http://pokeapi.co"+ sprout["image"]

    response = requests.get(sprite, stream=True)

    with open('img.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    photoimage = ImageTk.PhotoImage(file="img.png")
    canvas.create_image(380, 150, image=photoimage)


    canvas.create_text(270,60,text=pokename,font=("Roboto",15))
    canvas.create_text(100,130,text="Pokedex No.  :    " + str(id),font=("Roboto",13))
    canvas.create_text(90,170,text="Description  :    ",font=("Roboto",13))
    canvas.create_text(260,210,text=description,font=("Roboto",7))
    canvas.create_text(100,250,text="Stats :   ",font=("Roboto",13))
    canvas.create_text(90,290,text=statnames[0] + str(stats[0]),font=("Roboto",10))
    canvas.create_text(90,310,text=statnames[1] + str(stats[1]),font=("Roboto",10))
    canvas.create_text(90,330,text=statnames[2] + str(stats[2]),font=("Roboto",10))
    canvas.create_text(80,350,text=statnames[3] + str(stats[3]),font=("Roboto",10))
    canvas.create_text(80,380,text=statnames[4] + str(stats[4]),font=("Roboto",10))
    canvas.create_text(380,260,text="Types : ",font=("Roboto",13))

    types = []

    for x in p["types"]:
        x = x["name"].title()
        types.append(x)
    canvas.create_text(380,300,text=types[0],font=("Roboto",11))

    if len(types)==2:

        canvas.create_text(380,320,text=types[1],font=("Roboto",11))
    tk.mainloop()
    time.sleep(10)
def main():
    print("Hello! Welcome to Prof. Oak's Pykedex! ")

    # Taking the user input on what action they want to perform, and then converting it to lower case for uniformity
    user_input = input("Enter a Pokemon'name or its Dex No. to find out more about it.\nEnter random to see a random Pokemon's Pokedex entry\n" +"Enter exit to exit the program \n>>> ")
    user_input = user_input.lower()

    # Checking what the user input is

    if user_input == "random":
        # The random.randint command gets a random number from the provided range. The str() command converts it to a string
        pokemon_name = str(random.randint(1,717))

        # Getting the response from the API for the specified Pokemon
        r = requests.get("http://pokeapi.co/api/v1/pokemon/" + pokemon_name + "/")

    elif user_input =="exit":
        print("Okay! Enjoy your journey as a Pokemon Noob!")
        sys.exit()

    else:
        pokemon_name = user_input

        r = requests.get("http://pokeapi.co/api/v1/pokemon/" + pokemon_name + "/")



    # Checking if the url is a valid one, and executing the function if it is. Else, it returns an error message.
    if r.status_code == 200:
        r = r.json()
        poke(r)
    else:
        print("Please enter a correct Pokemon name or Pokedex No. (1-717)")

if __name__ == "__main__":
    main()
