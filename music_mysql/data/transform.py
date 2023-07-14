## 在piece中提取每首曲子的type（如果有的话）

import csv

categories = [
    "Symphony", "Serenade", "Variations", "Concerto", "Sonata", "March", "Quartet", "Suite", "Prelude", "Nocturne",
    "Rhapsody", "Fantasia", "Overture", "Dance", "Lieder", "Impromptu", "Trio", "Chorus", "Fugue", "Caprice", "Etude",
    "Waltz", "Ballade", "Mass", "Motet", "Oratorio", "Requiem", "Prelude and Fugue", "Nocturnes", "Chants", "Polonaise",
    "Lieder ohne Worte", "Scherzo", "Mazurka", "Intermezzo"
]

def process_csv(input_file, output_file):
    with open(input_file, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        for row in rows:
            for category in categories:
                if category in row[1]:
                    row[3] = category
        
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# 替换为您的输入和输出文件路径
input_file = 'piece.csv'
output_file = 'piece.csv'

process_csv(input_file, output_file)