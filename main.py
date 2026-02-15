import time
import matplotlib.pyplot as plt
import random
import math

# =========================================
# 1. Алгоритмы
# =========================================

def algorithm_1(arr):
    """Линейный поиск максимума (O(n))"""
    max_val = arr[0]
    for x in arr:
        if x > max_val:
            max_val = x
    return max_val

def algorithm_2(arr):
    """Бинарный поиск числа (O(log n))"""
    arr.sort()  # отсортировка для бинарного поиска
    target = arr[-1]
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def binary_convert_wrapper(arr):
    """
    Обёртка для проекта анализа.
    arr — массив любых элементов, длина определяет размер входных данных.
    """
    n_bits = len(arr)
    return binary_convert(n_bits)



# =========================================
# Алгоритм перевода двоичного числа в 8/16-ричную систему
# =========================================
def binary_convert(n_bits):
    """
    Генерирует случайное двоичное число длиной n_bits
    и переводит его в восьмеричное и шестнадцатеричное.
    Возвращает tuple (octal, hexadecimal)
    """
    import random

    # Генерация двоичного числа
    binary = ''.join(random.choice('01') for _ in range(n_bits))

    # ========== ВОСЬМЕРИЧНАЯ СИСТЕМА ==========
    while len(binary) % 3 != 0:
        binary = "0" + binary

    dec = {
        "000": "0", "001": "1", "010": "2", "011": "3",
        "100": "4", "101": "5", "110": "6", "111": "7"
    }

    octal = ""
    for i in range(0, len(binary), 3):
        group = binary[i:i+3]
        octal += dec[group]

    # ========== ШЕСТНАДЦАТЕРИЧНАЯ СИСТЕМА ==========
    while len(binary) % 4 != 0:
        binary = "0" + binary

    hex_map = {
        "0000": "0", "0001": "1", "0010": "2", "0011": "3",
        "0100": "4", "0101": "5", "0110": "6", "0111": "7",
        "1000": "8", "1001": "9", "1010": "A", "1011": "B",
        "1100": "C", "1101": "D", "1110": "E", "1111": "F"
    }

    hexadecimal = ""
    for i in range(0, len(binary), 4):
        group = binary[i:i+4]
        hexadecimal += hex_map[group]

    return octal, hexadecimal


algorithms = {
    "Линейный поиск": algorithm_1,
    "Бинарный поиск": algorithm_2,
    "Перевод двоичного числа": binary_convert_wrapper
}

# =========================================
# 2. Экспериментальная проверка
# =========================================

sizes = [1000, 5000, 10000, 50000, 100000, 200000]
results = {name: [] for name in algorithms.keys()}

for size in sizes:
    arr = list(range(size))
    for name, func in algorithms.items():
        start = time.time()
        func(arr.copy())
        end = time.time()
        results[name].append(end - start)

# =========================================
# 3. Автоматическая оценка типа сложности 
# =========================================
def estimate_complexity(times, sizes):
    ratios = [times[i+1]/times[i] for i in range(len(times)-1)]
    size_ratios = [sizes[i+1]/sizes[i] for i in range(len(sizes)-1)]
    avg_growth = sum(math.log(r)/math.log(s) for r,s in zip(ratios, size_ratios)) / len(ratios)
    if avg_growth < 0.5:
        return "O(log n)"
    elif avg_growth < 1.5:
        return "O(n)"
    elif avg_growth < 2.5:
        return "O(n log n)"
    else:
        return "O(n^2+)"
    
# =========================================
# 4. Построение графика + таблицы
# =========================================

fig, (ax_plot, ax_table) = plt.subplots(1, 2, figsize=(14, 6))

# ===== График =====
for name in algorithms.keys():
    ax_plot.plot(
        sizes,
        results[name],
        marker='o',
        label=f"{name} ({estimate_complexity(results[name], sizes)})"
    )

ax_plot.set_xlabel("Размер входных данных (N)")
ax_plot.set_ylabel("Время выполнения (сек)")
ax_plot.set_title("Сравнение временной сложности")
ax_plot.grid(True)
ax_plot.legend()
ax_plot.set_xscale("log")
ax_plot.set_yscale("log")

# ===== Таблица =====
ax_table.axis('off')

# Сформировывает данные таблицы
table_data = []
for i, size in enumerate(sizes):
    row = [size]
    for name in algorithms.keys():
        row.append(f"{results[name][i]:.6f}")
    table_data.append(row)

columns = ["Размер"] + list(algorithms.keys())

table = ax_table.table(
    cellText=table_data,
    colLabels=columns,
    loc='center'
)

table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1.2, 1.2)

ax_table.set_title("Таблица замеров времени")

plt.tight_layout()
plt.savefig("algorithm_complexity_with_table.png")
plt.show()


# =========================================
# 5. Вывод результатов
# =========================================
print("Размер | " + " | ".join([f"{name}" for name in algorithms.keys()]))
for i, size in enumerate(sizes):
    row = f"{size:>7}"
    for name in algorithms.keys():
        row += f" | {results[name][i]:>10.6f}"
    print(row)

print("\nГрафик сохранён в 'algorithm_complexity_comparison.png'")
