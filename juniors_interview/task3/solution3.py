""" Здесь требуется глобальный подход, лично я, будучи, пускай, немного, но знаком с принципами SOLID, скажу следующее:
    Для решения этой задачи нужно объединить интервалы присутствия всех участников и найти пересечение между интервалами
    ученика,учителя и урока. Поэтому я считаю необходимым разбить задачу на 2 функции:
    Функция для пересечения двух интервалов и функция для объединения интервалов. Окееей, летсгоу."""

def merge(intervals):
    #Объединяю пересекающиеся интервалы
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        last_end = merged[-1][1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
    return merged

def intersection(intervals1, intervals2):
    #Ищу пересечение двух списков интервалов
    result = []
    i, j = 0, 0
    while i < len(intervals1) and j < len(intervals2):
        start1, end1 = intervals1[i]
        start2, end2 = intervals2[j]
        start_overlap = max(start1, start2)
        end_overlap = min(end1, end2)
        if start_overlap < end_overlap:
            result.append([start_overlap, end_overlap])
        if end1 < end2:
            i += 1
        else:
            j += 1
    return result

def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = [[intervals['lesson'][0], intervals['lesson'][1]]]
    pupil_intervals = [[intervals['pupil'][i], intervals['pupil'][i + 1]] for i in range(0, len(intervals['pupil']), 2)]
    tutor_intervals = [[intervals['tutor'][i], intervals['tutor'][i + 1]] for i in range(0, len(intervals['tutor']), 2)]

    # Ограничиваю интервалы учеников и учителей временем урока
    pupil_intervals = intersection(pupil_intervals, lesson)
    tutor_intervals = intersection(tutor_intervals, lesson)

    # Объединяю интервалы после ограничения
    pupil_intervals = merge(pupil_intervals)
    tutor_intervals = merge(tutor_intervals)

    # Пересечения учеников и учителей
    common_intervals = intersection(pupil_intervals, tutor_intervals)

    # Подсчёт времени
    total_time = sum(end - start for start, end in common_intervals)

    # Вывод результатов
    print(f"Урок: {lesson}")
    print(f"Интервалы ученика (ограниченные): {pupil_intervals}")
    print(f"Интервалы учителя (ограниченные): {tutor_intervals}")
    print(f"Общие интервалы: {common_intervals}")
    print(f"Общее время пересечения: {total_time}")
    print() #Чисто отступ

    return total_time

# Тесты
tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                             1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                             1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                             1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Ошибка в тесте {i}, получили {test_answer}, ожидали {test["answer"]}' #Финальная проверка со сравнением ответов
    print("Все тесты пройдены, всё отлично")
