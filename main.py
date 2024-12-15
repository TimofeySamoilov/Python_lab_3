import datetime

alf = "qwertyuiopasdfghjklzxcvbnm1234567890 QWERTYUIOPASDFGHJKLZXCVBNM"

# функция для считывания с клавиатуры имени
def get_name():
    while True:
        print(" - Please write a name (only latin symbols and numbers) and First letter is upper - ")
        flag = True
        name = input().strip()
        if name == "":
            continue
        for i in name:
            if i not in alf:
                flag = False
                break
        if flag and (name[0] in "QWERTYUIOPASDFGHJKLZXCVBNM"):
            return name
# функция для считывания фамилии
def get_second_name():
    while True:
        print(" - Please write a second name (only latin symbols and numbers) and First letter is upper - ")
        flag = True
        second_name = input().strip()
        if second_name == "":
            continue
        for i in second_name:
            if i not in alf:
                flag = False
                break
        if flag and (second_name[0] in "QWERTYUIOPASDFGHJKLZXCVBNM"):
            return second_name
# для считывания номера телефона
def get_number():
    while True:
        print(" - Please write a correct phone number +7... or 8... - ")
        flag = True
        phone_number = input().strip()
        if phone_number == "":
            continue
        for i in phone_number:
            if i not in "+1234567890":
                flag = False
                break
        if flag and (len(phone_number.replace("+", "")) == 11):
            if "+7" in phone_number:
                phone_number = phone_number.replace("+7", "8")
            if "89" not in phone_number and "88" not in phone_number:
                pass
            if "+" in phone_number:
                phone_number = phone_number.replace("+", "")
            else:
                return phone_number
# для считывания даты рождения
def get_date():
    while True:
        print(" - Please write a date of birth : {dd.mm.yyyy} or skip it by pressing enter - ")
        flag = True
        birthday = input().strip()
        if birthday == "":
            return None
        for i in birthday:
            if i not in "1234567890.":
                flag = False
                break
        try:
            if flag and len(birthday) == 10 and birthday.count(".") == 2 and birthday[2] == "." and birthday[5] == ".":
                return str(datetime.datetime.strptime(birthday, "%d.%m.%Y").date())

        except ValueError as e:
            print(" - Wrong birthday! - ")
            continue

def work():
    try:
        # Открываем файл
        base = open("base.phonebook", "r")
        # Считываем все данные
        data = [i.strip() for i in base.readlines()]
        print(data)
        base.close()
        word = ""
        fl = False
        while True:
            if not fl:
                print(" - Please choose a number of operation: - ")
            fl = False
            print("1 : Show all recordings in phonebook")
            print("2 : Find a record by parameters")
            print("3 : Add new record to phonebook")
            print("4 : Remove record from phonebook by name")
            print("5 : Show next birthday")
            print("6 : Change recording")
            print("7 : Show age by name and second name")
            print("Or write 'quit' to quit")

            word = input()
            if word == "quit":
                break

            if word == "1":
                base = open("base.phonebook", "r")
                data = base.readlines()
                print()
                print(" - ********************* - ")
                if len(data) > 0:
                    print(" - All of the recordings: - ")
                    for i in data:
                        print(i[1:-2].replace("|", "  "))
                else:
                    print(" - No recordings - ")
                print(" - ********************* - ")
                print()
                base.close()

            elif word == "2":
                final_parameter = ""
                while True:
                    print(" - Please write a parameter (only latin symbols and numbers) or a part of it - ")
                    flag = True
                    parameter = input().strip()
                    if parameter == "":
                        continue
                    for i in parameter:
                        if i not in alf:
                            flag = False
                            break
                    if flag:
                        final_parameter = parameter
                        break

                base = open("base.phonebook", "r")
                data = base.readlines()
                base.close()
                _ = False
                print()
                print(" - ********************* - ")
                print(" - Found: -")
                for i in data:
                    if final_parameter in i[1:-2].replace("|", "  "):
                        _ = True
                        print(i[1:-2].replace("|", "  "))
                if not _:
                    print(" - No recordings - ")
                print(" - ********************* - ")
                print()

            elif word == "3":
                # считываем имя
                final_name = get_name()

                # считываем фамилию
                final_second_name = get_second_name()

                # считываем номер телефона
                final_phone_number = get_number()

                # считываем дату рождения
                final_birthday = get_date()

                # открываем файл
                base = open("base.phonebook", "r+")
                data = base.readlines()

                # проверка на существование такой записи
                _ = False
                for i in data:
                    name, second_name = (i[1:]).split("|")[:2]
                    if name == final_name and second_name == final_second_name:
                        _ = True
                        print()
                        print(" - This record is already present!!! - ")
                        print()
                        break
                if _:
                    base.close()
                    continue

                # сразу сохраняем в файл новые данные если такой записи не существует
                base.seek(0, 2)
                base.write(f'@{final_name}|{final_second_name}|{final_phone_number}|{final_birthday}@\n')
                base.close()


            elif word == "4":
                # считываем имя
                final_name = get_name()

                # считываем фамилию
                final_second_name = get_second_name()

                base = open("base.phonebook", "r+")
                data = base.readlines()
                # поиск имени и фамилии
                _ = False
                for i in range(len(data)):
                    name, second_name = (data[i][1:]).split("|")[:2]
                    if name == final_name and second_name == final_second_name:
                        _ = True
                        data[i] = ""
                        break
                print()
                print(" - This recording with name", final_name, final_second_name, "was found and deleted - " if _ else "was not found - ")
                print()
                base.close()
                base = open("base.phonebook", "w")
                base.write("".join(data))
                base.close()


            elif word == "5":
                base = open("base.phonebook", "r")
                data = base.readlines()
                base.close()
                closest_birthday = None
                min_days_diff = float('inf')  # инициализируем очень большим числом
                now = datetime.date.today()
                for item in data:
                    try:
                        parts = item[1:-2].split("|")
                        birthdate_str = parts[3]
                        if birthdate_str != "None":
                            birthdate = datetime.datetime.strptime(birthdate_str, "%Y-%m-%d").date()
                            # считаем разницу
                            this_year_birthdate = birthdate.replace(year=now.year)
                            days_diff = (this_year_birthdate - now).days
                            # Если уже было др в этом году
                            if days_diff < 0:
                                this_year_birthdate = birthdate.replace(year=now.year + 1)
                                days_diff = (this_year_birthdate - now).days
                            if days_diff < min_days_diff:
                                min_days_diff = days_diff
                                closest_birthday = parts
                    except (ValueError, IndexError):
                        print(f"Error parsing line: {item}")
                if closest_birthday:
                    print("\n- Near birthday: -")
                    print("Name:", closest_birthday[0])
                    print("Last Name:", closest_birthday[1])
                    print("Phone:", closest_birthday[2])
                    print("Birthdate:", closest_birthday[3])
                    print(f"Days until next birthday: {min_days_diff}")
                    print()
                else:
                    print(" - There is no info about date - ")


            elif word == "6":
                # Получаем имя и фамилию
                final_name = get_name()
                final_second_name = get_second_name()
                base = open("base.phonebook", "r+")
                data = base.readlines()
                base.close()
                found_data = None
                index_of_found_data = -1  # Initialize to -1 to indicate not found
                for i in range(len(data)):
                    name, second_name = (data[i][1:]).split("|")[:2]
                    # Находим совпадение
                    if name == final_name and second_name == final_second_name:
                        found_data = data[i][1:-2]
                        final_phone_number = data[i][1:-2].split("|")[2]
                        final_birthday = data[i][1:-2].split("|")[3]
                        index_of_found_data = i
                        break
                if found_data is not None:
                    print()
                    print(" - The recording was found - ")
                    is_name_changed = False
                    while True:
                        print(" - What do you want to change? Choose (1-4) - ")
                        print("1: Name")
                        print("2: Second name")
                        print("3: Phone number")
                        print("4: Date of birthday")
                        inp = input()
                        if inp == "1":
                            final_name = get_name()
                            is_name_changed = True
                            break
                        elif inp == "2":
                            final_second_name = get_second_name()
                            is_name_changed = True
                            break
                        elif inp == "3":
                            final_phone_number = get_number()
                            break
                        elif inp == "4":
                            final_birthday = get_date()
                            break
                        else:
                            continue
                    # Проверяем, нет ли такого имени и фамилии уже в книге
                    if is_name_changed:
                        # проверяем чтобы такого имени не существовало
                        base = open("base.phonebook", "r")
                        data = base.readlines()
                        base.close()
                        duplicate_found = False
                        for i in data:
                            name, second_name = (i[1:]).split("|")[:2]
                            if name == final_name and second_name == final_second_name:
                                duplicate_found = True
                                print("\n - The name is already present!!! - \n")
                                break
                        if duplicate_found:
                            continue
                    # Update the record
                    data[index_of_found_data] = f'@{final_name}|{final_second_name}|{final_phone_number}|{final_birthday}@\n'
                    # Write the updated data back to the file
                    base = open("base.phonebook", "w")
                    base.writelines(data)
                    base.close()
                else:
                    print()
                    print(f" - No recordings were found with name: {final_name}, {final_second_name} - ")
                    print()


            elif word == "7":
                # получаем имя и фамилию
                final_name = get_name()
                final_second_name = get_second_name()
                base = open("base.phonebook", "r")
                data = base.readlines()
                base.close()
                found = False
                now = datetime.date.today()
                # перебираем данные в файле
                for item in data:
                    try:
                        parts = item[1:-2].split("|")
                        name = parts[0]
                        second_name = parts[1]
                        birthdate_str = parts[3]
                        # проверяем совпадения
                        if name == final_name and second_name == final_second_name:
                            found = True
                            birthdate = datetime.datetime.strptime(birthdate_str, "%Y-%m-%d").date()
                            # считаем возраст
                            age = now.year - birthdate.year - ((now.month, now.day) < (birthdate.month, birthdate.day))
                            print(" - Data was found - ")
                            print(f"Name: {name}, Last Name: {second_name}, Age: {age}")
                            break
                    except (ValueError, IndexError):
                        print(f"Error parsing line: {item}")
                if not found:
                    print(f" - No recordings found for {final_name} {final_second_name} - ")
                print()
            else:
                print(" - Wrong number, please try again, you should choose (1-6) - ")
                fl = True
        base.close()

    except FileNotFoundError as e:
        print("(!)Phone book file not found! The new file will be created.")
        base = open("base.data", "w+")
        base.close()
        exit(0)
    except Exception as e:
        print("(!)Failed to read data from phone book file!", e)
        exit(0)

if __name__ == "__main__":
    work()