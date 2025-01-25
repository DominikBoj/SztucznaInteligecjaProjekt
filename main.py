import csv
from collections import Counter

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

def find_items(stats, item_database, your_stats):
    item_scores = []

    print("\nStatystyki przeciwników:", stats)

    # Rozbij statystyki bohatera na listę
    your_stats = your_stats[0].split(',')
    your_stats = [stat.strip() for stat in your_stats]

    for item in item_database:
        item_stats = item["Stats"].split(',')
        cleaned_item_stats = [stat.strip() for stat in item_stats]
        score = 0

        # Dopasowanie do statystyk przeciwników
        for stat, count in stats:
            for item_stat in cleaned_item_stats:
                if (stat == "AD" and item_stat == "Armor") or \
                   (stat == "AP" and item_stat == "MR") or \
                   (stat == "HP" and item_stat == "AD") or \
                   (stat == "Armor" and item_stat == "ArPen") or \
                   (stat == "MR" and item_stat == "ApPen"):
                    score += count
                    print(f"Dopasowanie: Stat przeciwnika '{stat}' -> Przedmiot '{item['Name']}' ({item_stat})")

        # Dopasowanie do statystyk bohatera
        for your_stat in your_stats:
            for item_stat in cleaned_item_stats:
                if your_stat in item_stat:
                    score += 2  # Dodaj większą wagę dla statystyk bohatera
                    print(f"Wsparcie bohatera: Stat '{your_stat}' -> Przedmiot '{item['Name']}' ({item_stat})")

        item_scores.append((item["Name"], score))
        print(f"Przedmiot: {item['Name']}, Statystyki: {cleaned_item_stats}, Wynik: {score}")

    # Sortowanie wyników
    item_scores = sorted(item_scores, key=lambda x: x[1], reverse=True)
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

input_names = ["Ahri", "Caitlyn", "Jhin", "Garen", "Diana"]
input_names = [name.strip() for name in input_names]
selected_characters = find_characters(input_names, data_characters)

stats = get_statistics(selected_characters)
sorted_stats = count_and_sort_statistics(stats)

your_character = ["Ahri"]
your_character = [name.strip() for name in your_character]
selected_character = find_characters(your_character, data_characters)

your_stats = get_statistics(selected_character)

print("Dane wejściowe do find_items:")
print("Statystyki przeciwników:", sorted_stats)
print("Przedmioty w bazie:", [(item["Name"], item["Stats"]) for item in data_items])

selected_items = find_items(sorted_stats, data_items, your_stats)

print("Statystyki przeciwników:", sorted_stats)
print("Twoje statystyki:", your_stats)
print("Wybrane przedmioty:", selected_items)
