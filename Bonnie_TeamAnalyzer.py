import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Connect to the pokemon.sqlite database
conn = sqlite3.connect('pokemon.sqlite')
c = conn.cursor()

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # Analyze the pokemon whose pokedex_number is in "arg"
    c.execute("SELECT against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water FROM imported_pokemon_data WHERE pokedex_number = ?", (arg,))
    pokemon = c.fetchone()

    if not pokemon:
        print("Could not find Pokemon with pokedex_number: " + arg)
        continue

    # Extract the values for the types of the current Pokemon
    type1 = pokemon[0] if pokemon[0] is not None else 1
    type2 = pokemon[1] if pokemon[1] is not None else 1
    types = [type1, type2]

    # Determine the types that this Pokemon is strong and weak against
    strong_against = []
    weak_against = []
    for j in range(len(types)):
        if types[j] > 1:
            strong_against.append(types[j])
        elif types[j] < 1:
            weak_against.append(types[j])


    for j in range(len(types)):
    if types_val[j] > 1:
        strong_against.append(types[j])
    elif types_val[j] < 1:
        weak_against.append(types[j])


    # Print out the results
    print("Analyzing " + arg)
    print(pokemon[2] + " is strong against " + str(strong_against) + " but weak against " + str(weak_against))

    team.append(int(arg))

# Prompt the user to save the team
answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    c.execute("INSERT INTO teams (name, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6) VALUES (?, ?, ?, ?, ?, ?, ?)", (teamName,) + tuple(team))
    conn.commit()
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

# Close the database connection
conn.close()