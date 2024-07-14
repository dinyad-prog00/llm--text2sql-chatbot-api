import csv

def read_examples_data(file_path='src/data/few_shot_examples.csv'):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file,delimiter=";")
        next(csv_reader)  
        examples = [{"input":row[0],"query": f"{row[1]};"} for row in csv_reader]  # Read the remaining rows

    return  examples