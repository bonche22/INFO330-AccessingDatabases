import sqlite3
import sys

# All the "against" column suffixes:
types = ["bug", "dark", "dragon", "electric", "fairy", "fight",
         "fire", "flying", "ghost", "grass", "ground", "ice", "normal",
         "poison", "psychic", "rock", "steel", "water"]

# Connect to the pokemon.sqlite database
conn = sqlite3.connect('pokemon.sqlite')
c = conn.cursor()

# Take six parameters from the command-line
if len(sys.argv) < 7:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i in range(1, 7):
    arg = sys.argv[i]

    # Analyze the pokemon whose pokedex_number is in "arg"
    query = "SELECT name, type1, type2, " + ", ".join(["against_" + t for t in types]) + " FROM imported_pokemon_data WHERE pokedex_number = ?"
    c.execute(query, (arg,))
    pokemon = c.fetchone()

    if not pokemon:
        print("Could not find Pokemon with pokedex_number: " + arg)
        continue

    # Extract the values for the types of the current Pokemon
    name = pokemon[0]
    type1 = pokemon[1] if pokemon[1] is not None else ""
    type2 = pokemon[2] if pokemon[2] is not None else ""
    against_types = pokemon[3:]

    # Determine the types that this Pokemon is strong and weak against
    strong_against = [types[j] for j in range(len(against_types)) if float(against_types[j]) > 1]
    weak_against = [types[j] for j in range(len(against_types)) if float(against_types[j]) < 1]

    # Print out the results
    print("Analyzing " + arg)
    print(name + " (" + type1 + " " + type2 + ") is strong against " + str(strong_against) + " but weak against " + str(weak_against))

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