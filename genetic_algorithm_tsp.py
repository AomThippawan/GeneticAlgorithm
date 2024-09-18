import numpy as np
import random

# ค่าพารามิเตอร์ของ GA
POPULATION_SIZE = 10  # เปลี่ยนค่าเป็น 10
MUTATION_RATE = 0.01
GENERATIONS = 80

# ข้อมูลระยะทางระหว่างสถานที่
distance_matrix = np.array([
    [0, 0.28, 0.55, 4.7, 7.4, 7.4, 7.5, 7.5, 4.4, 14.5],
    [0.28, 0, 0.8, 5.1, 7.8, 7.9, 7.9, 8.0, 4.0, 14.1],
    [0.55, 0.8, 0, 5.5, 8.2, 8.2, 8.3, 8.3, 3.2, 14.1],
    [4.7, 5.1, 5.5, 0, 5.1, 7.4, 7.4, 7.5, 7.9, 19.0],
    [7.4, 7.8, 8.2, 5.1, 0, 2.2, 1.9, 2.3, 5.9, 21.8],
    [7.4, 7.9, 8.2, 7.4, 2.2, 0, 0.072, 0.21, 7.3, 23.2],
    [7.5, 7.9, 8.3, 7.4, 1.9, 0.072, 0, 0.29, 7.3, 23.3],
    [7.5, 8.0, 8.3, 7.5, 2.3, 0.21, 0.29, 0, 7.4, 23.3],
    [4.4, 4.0, 3.2, 7.9, 5.9, 7.3, 7.3, 7.4, 0, 14.9],
    [14.5, 14.1, 14.1, 19.0, 21.8, 23.2, 23.3, 23.3, 14.9, 0]
])

# ชื่อสถานที่
locations = [
    "หอนาฬิกาหาดใหญ่",
    "วงเวียนน้ำพุ",
    "ตลาดกิมหยง",
    "ตลาดน้ำคลองแห",
    "สวนสาธารณะเทศบาลนครหาดใหญ่",
    "พระพุทธมงคลมหาราช",
    "จุดชมวิวคอหงส์",
    "จุดชมวิวหลังหอดูดาวหาดใหญ่",
    "ตลาดกรีนเวย์ ไนท์มาร์เก็ต",
    "ทุ่งสายฮ้าง"
]

# คำนวณระยะทางทั้งหมดของเส้นทาง
def calculate_path_length(path, distance_matrix):
    return sum(distance_matrix[path[i], path[i + 1]] for i in range(len(path) - 1)) + distance_matrix[path[-1], path[0]]

# สร้างประชากรเริ่มต้น
def create_population(num_cities):
    population = []
    for _ in range(POPULATION_SIZE):
        individual = list(range(num_cities))
        random.shuffle(individual)
        population.append(individual)
    return population

# แบบ 2-point crossover
def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [-1] * len(parent1)
    child[start:end + 1] = parent1[start:end + 1]
    
    current_pos = (end + 1) % len(parent2)
    for i in range(len(parent2)):
        gene = parent2[(current_pos + i) % len(parent2)]
        if gene not in child:
            insert_pos = child.index(-1)
            child[insert_pos] = gene
    return child

# การกลายพันธุ์
def mutate(individual):
    idx1, idx2 = random.sample(range(len(individual)), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

# ทำงานของ GA
def genetic_algorithm(distance_matrix):
    num_cities = len(distance_matrix)
    population = create_population(num_cities)
    for generation in range(GENERATIONS):
        population = sorted(population, key=lambda path: calculate_path_length(path, distance_matrix))
        new_population = population[:POPULATION_SIZE // 2]
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(population[:POPULATION_SIZE // 2], 2)
            child = crossover(parent1, parent2)
            if random.random() < MUTATION_RATE:
                mutate(child)
            new_population.append(child)
        population = new_population
        if generation % 10 == 0:
            print(f"Generation {generation}: Best path length = {calculate_path_length(population[0], distance_matrix)}")
    return sorted(population, key=lambda path: calculate_path_length(path, distance_matrix))[0]

# แสดงเส้นทางที่ดีที่สุดในรูปแบบชื่อสถานที่
def print_best_path(path, locations):
    best_path_info = "Best path found:\n"
    for idx in path:
        best_path_info += f" - {locations[idx]}\n"
    best_path_info += f"Length of best path: {calculate_path_length(path, distance_matrix)}\n"
    return best_path_info

# ทดสอบ
num_cities = len(distance_matrix)
best_path = genetic_algorithm(distance_matrix)
best_path_info = print_best_path(best_path, locations)
print(best_path_info)
