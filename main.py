import csv
from collections import Counter

#####################
#LEGENDA I OZNACZENIA
#####################
#AD - Attack Damage - kontrowane przez Armor, kontruje HP
#AP - Ability Power - kontrowane przez MR , kontruje HP
#HP - Health Points - kontrowane przez AD, kontruje Armor
#Armor -  kontruje AD, kontrowane przez ArPen
#MR  - Magic Resist -  kontruje AP, kontrowane przez ApPen
#ArPen - Armor Penetration - kontruje Armor, Kontrowane przez HP
#MrPen - Magic Resist Penetration - kontruje 
#Mana - zasób nie kontruje ani nie ma kontr




def find_characters(names, database):
    selected_characters = []
    for name in names:
        for character in database:
            if character["Champion"].lower() == name.lower():
                selected_characters.append(character)
    return selected_characters

def get_statistics(characters):
    stats = []
    for character in characters:
        stats.append(character["Stats prioryty"])
    return stats

def count_and_sort_statistics(stats):
    all_stats = []
    for stat in stats:
        stat_list = stat.split(',')
        all_stats.extend([s.strip() for s in stat_list])

    stat_counts = Counter(all_stats)
    sorted_stats = stat_counts.most_common()
    return sorted_stats

def extract_stats(raw_stats):
    return [stat.split()[1] if ' ' in stat else stat for stat in raw_stats]

def find_items(stats, item_database, your_stats):
    item_scores = []

    if isinstance(your_stats, list) and len(your_stats) > 0:
        your_stats = [stat.strip() for stat in your_stats[0].split(',')]
    else:
        your_stats = []

    opponent_stat_counts = Counter({stat: count for stat, count in stats})

    max_opponent_stat = max(opponent_stat_counts.values(), default=0)

    for item in item_database:
        item_stats = item["Stats"].split(',')
        cleaned_item_stats = extract_stats([stat.strip() for stat in item_stats])
        score = 0

        # Dopasowanie do statystyk bohatera
        matching_hero_stats = sum(1 for your_stat in your_stats 
                                  if any(your_stat in stat for stat in cleaned_item_stats))
        if matching_hero_stats > 0:
            score += matching_hero_stats * 7

        # Dopasowanie do statystyk przeciwników
        for stat, count in opponent_stat_counts.items():
            for item_stat in cleaned_item_stats:
                if (stat == "AD" and item_stat == "Armor") or \
                   (stat == "AP" and item_stat == "MR") or \
                   (stat == "HP" and item_stat == "AD") or \
                   (stat == "HP" and item_stat == "AP") or \
                   (stat == "Armor" and item_stat == "ArPen") or \
                   (stat == "ArPen" and item_stat == "HP") or \
                   (stat == "ApPen" and item_stat == "HP") or \
                   (stat == "MR" and item_stat == "MrPen"):

                    score += count * 4

                # Premia za częste statystyki przeciwników
                if stat == item_stat:
                    score += count * 3

        # Premia za dominującą statystykę przeciwników
        for stat in opponent_stat_counts:
            if opponent_stat_counts[stat] == max_opponent_stat:
                for item_stat in cleaned_item_stats:
                    if stat == item_stat:
                        score += 5

        
        #print(f"Item: {item['Name']}, Hero Match: {matching_hero_stats}, Opponent Score: {score}, Stats: {cleaned_item_stats}")

        if score > 0:
            item_scores.append((item["Name"], score))

    item_scores = sorted(item_scores, key=lambda x: (x[1], x[0]), reverse=True)

    #print("\nSzczegóły oceny przedmiotów:")
    #for item, score in item_scores:
    #    print(f"{item}: {score}")

    return [item[0] for item in item_scores[:6]]

file_path_characters = "C:\\Users\\Dominik\\Documents\\GitHub\\SztucznaInteligecjaProjekt\\league_of_legends_characters.csv"
file_path_items = "C:\\Users\\Dominik\\Documents\\GitHub\\SztucznaInteligecjaProjekt\\league_of_legends_items.csv"

data_characters = []
with open(file_path_characters, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data_characters.append(row)

data_items = []
with open(file_path_items, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data_items.append(row)

input_names = ["Ahri","Amumu","Garen","Caitlyn","Diana","Janna","Draven"]
input_names = [name.strip() for name in input_names]
selected_characters = find_characters(input_names, data_characters)

stats = get_statistics(selected_characters)
sorted_stats = count_and_sort_statistics(stats)

your_character = ["Amumu"]
your_character = [name.strip() for name in your_character]
selected_character = find_characters(your_character, data_characters)

your_stats = get_statistics(selected_character)

selected_items = find_items(sorted_stats, data_items, your_stats)

print("Statystyki przeciwników:", sorted_stats)
print("Twoje statystyki:", your_stats)
print("Wybrane przedmioty:", selected_items)
