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
        stats.append(character["Stats prioryty"])  # Załóżmy, że kolumna z danymi nazywa się "Stats"
    return stats

def count_and_sort_statistics(stats):
    # Łączymy wszystkie statystyki w jeden ciąg
    all_stats = []
    for stat in stats:
        # Zakładamy, że statystyki są oddzielone przecinkiem
        stat_list = stat.split(',')  
        all_stats.extend([s.strip() for s in stat_list])  # Usuwamy ewentualne białe znaki

    # Liczymy wystąpienia poszczególnych statystyk
    stat_counts = Counter(all_stats)

    # Sortujemy statystyki w kolejności malejącej
    sorted_stats = stat_counts.most_common()

    return sorted_stats

file_path = "C:\\Users\\Dominik\\Documents\\GitHub\\SztucznaInteligecjaProjekt\\league_of_legends_characters.csv"

# Zmienna do przechowywania danych
data = []

# Odczyt pliku CSV
with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

input_names = ["Ahri", "Caitlyn", "Jhin", "Garen", "Diana"]

input_names = [name.strip() for name in input_names]

selected_characters = find_characters(input_names, data)

# Pobranie statystyk
stats = get_statistics(selected_characters)

sorted_stats = count_and_sort_statistics(stats)

# Wyświetlenie statystyk
print(sorted_stats)

your_character = ["Draven"]

your_character = [name.strip() for name in your_character]

selected_character = find_characters(your_character, data)

your_stats = get_statistics(selected_character)

print(your_stats)