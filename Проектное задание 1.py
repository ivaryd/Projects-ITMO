try:
    file_employees = open(r"employees.txt", encoding='utf-8')
    file_tasks = open(r"tasks.txt", encoding='utf-8')
except IOError:  # проверка на ошибку
    print("Не удалось открыть один из файлов :(")
else:
    employees_data = file_employees.readlines()  # считывает программу построчно и возвращает все строки в виде списка
    tasks_data = file_tasks.readlines()
    tasks_data = [x.strip('\n') for x in tasks_data] #удаляет символ переноса строки
    file_employees.close()  # закрывает программу
    file_tasks.close()
    hours, task_num, hour, n, num, wn = 0, 0, 0, 0, 0, 0
    name, tech_e, task, tech_t, alltasks, info_for_file, nobody_tasks, emp_no_task = '', '', '', '', '', '', '', ''
    list_with_tasks = []
    employees_data.sort() #сортирует в алфавитном порядке
    for inform in employees_data:  # для каждого элемента списка работников
        hours, task_num, hour = 0, 0, 0
        task, alltasks = '', ''
        if 'senior' in inform: ### FOR SENIOR
            name = ' '.join(inform[:inform.find('senior')].split())  # выделение имени работника без лишних пробелов
            tech_e = set(inform.replace(f'{name}', '').replace(' senior ', '').split(', '))  # выделение технологий работника
            tech_e = {x.strip('\n') for x in tech_e} #удаление переноса строки
            for techinfo in tasks_data:  # для каждого элемента списка задач
                if 'senior' in techinfo:
                    task = ' '.join(techinfo[:techinfo.find('senior')].split())  # выделение названия задачи без лишних пробелов
                    tech_t = set(techinfo.lstrip(task).replace('senior ', '')[:-2].split(', '))  # выделение технологий задачи
                if 'middle' in techinfo:
                    task = ' '.join(techinfo[:techinfo.find('middle')].split())
                    tech_t = set(techinfo.lstrip(task).replace('middle ', '')[:-2].split(', '))
                if 'junior' in techinfo:
                    task = ' '.join(techinfo[:techinfo.find('junior')].split())
                    tech_t = set(techinfo.lstrip(task).replace('junior ', '')[:-2].split(', '))
                if tech_t.issubset(tech_e) and task not in info_for_file:
                    hour = int(techinfo[-1])
                    hours += hour
                    task_num += 1
                    alltasks += f'{task_num}. {task} - {hour}\n' # запись задачи в локальную переменную
                if task not in list_with_tasks:
                    list_with_tasks.append(task) #запись задачи в список, который потребуется в дальнейшем
        if 'middle' in inform:  ### FOR MIDDLE
            name = ' '.join(inform[:inform.find('middle')].split())
            tech_e = set(inform.replace(f'{name}', '').replace(' middle ', '').split(', '))
            tech_e = {x.strip('\n') for x in tech_e}
            for techinfo in tasks_data:
                if 'middle' in techinfo or 'junior' in techinfo:
                    if 'middle' in techinfo:
                        task = ' '.join(techinfo[:techinfo.find('middle')].split())
                        tech_t = set(techinfo.lstrip(task).replace('middle ', '')[:-2].split(', '))
                    if 'junior' in techinfo:
                        task = ' '.join(techinfo[:techinfo.find('junior')].split())
                        tech_t = set(techinfo.lstrip(task).replace('junior ', '')[:-2].split(', '))
                    if tech_t.issubset(tech_e) and task not in info_for_file:
                        hour = int(techinfo[-1])
                        hours += hour
                        task_num += 1
                        alltasks += f'{task_num}. {task} - {hour}\n'
                    if task not in list_with_tasks:
                        list_with_tasks.append(task)
        if 'junior' in inform:  ### FOR JUNIOR
            name = ' '.join(inform[:inform.find('junior')].split())
            tech_e = set(inform.replace(f'{name}', '').replace(' junior ', '').split(', '))
            tech_e = {x.strip('\n') for x in tech_e}
            for techinfo in tasks_data:
                if 'junior' in techinfo:
                    task = ' '.join(techinfo[:techinfo.find('junior')].split())
                    tech_t = set(techinfo.lstrip(task).replace('junior ', '')[:-2].split(', '))
                    if tech_t.issubset(tech_e) and task not in info_for_file:
                        hour = int(techinfo[-1])
                        hours += hour
                        task_num += 1
                        alltasks += f'{task_num}. {task} - {hour}\n'
                    if task not in list_with_tasks:
                        list_with_tasks.append(task)
        if hours == 0:
            wn += 1
            emp_no_task += f'{wn}. {name}\n'
        else:
            info_for_file += f'• {name} - {hours}\n{alltasks}\n'
    if emp_no_task != '':
        info_for_file += f'• {wn} работников оказались без задач:\n{emp_no_task}\n'
    for x in list_with_tasks:  # цикл проверяет, распределена ли задача кому-то
        num += 1
        if x not in info_for_file:
            n += 1
            nobody_tasks += f'{n}. {x}\n'
        if num == len(list_with_tasks) and nobody_tasks != '':
            info_for_file += f'• Задачи, которые никто не может решить:\n{nobody_tasks}\n'
    info_for_file += f'• Дополнительная информация:\nВсего было {num} задач, из которых распределено между работниками {num-n}.\n{n} задач оказались нераспределёнными.'
    file_plans = open("plans.txt", "w")
    file_plans.write(info_for_file)
    file_plans.close()
    print('Все задачи успешно распределены между работниками и записаны в файл')
