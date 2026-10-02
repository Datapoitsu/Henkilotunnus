## -------------------- Personal identification number tools ------------------------- ##
#Written by: Aarni Junkkala.

#Tools for Finnish personal identification numbers.

import random

CONTROL_CHARACTERS = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","H","J","K","L","M","N","P","R","S","T","U","V","W","X","Y"]
CENTURY_CHARACTERS_1800 = ["+"]
CENTURY_CHARACTERS_1900 = ["-","Y","X","W","V","U"]
CENTURY_CHARACTERS_2000 = ["A","B","C","D","E","F"]
CENTURY_CHARACTERS = CENTURY_CHARACTERS_1800 + CENTURY_CHARACTERS_1900 + CENTURY_CHARACTERS_2000
MONTH_DAY_COUNT = [31,28,31,30,31,30,31,31,30,31,30,31]
GREATEST_POSSIBLE_YEAR = 2099
SMALLEST_POSSIBLE_YEAR = 1800

def is_leap_year(year:int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_sex(id:str) -> str or None:
    try:
        if int(id[9]) % 2 == 0:
            return "Female"
        return "Male"
    except:
        return None

def get_date(id:str) -> list[int] or None:
    global CENTURY_CHARACTERS_1800, CENTURY_CHARACTERS_1900, CENTURY_CHARACTERS_2000, MONTH_DAY_COUNT
    result = [None, None, None]
    try:
        if id[6] in CENTURY_CHARACTERS_1800:
            result[2] = int("18"+id[4:6])
        if id[6] in CENTURY_CHARACTERS_1900:
            result[2] = int("19"+id[4:6])
        if id[6] in CENTURY_CHARACTERS_2000:
            result[2] = int("20"+id[4:6])
    except:
        pass
    try:
        month = int(id[2:4])
        if month >= 1 and month <= 12:
            result[1] = month
    except:
        pass

    try:
        day = int(id[0:2])
        extra_day = 0 #Leap day.
        if get_month(id) == 2 and is_leap_year(get_year(id)):
            extra_day = 1
        if day >= 1 or day <= MONTH_DAY_COUNT[get_month(id) - 1] + extra_day:
            result[0] = day
    except:
        pass

    try:
        day = int(id[0:2])
        extra_day = 0 #Leap day.
        if get_month(id) == 2 and is_leap_year(get_year(id)):
            extra_day = 1
        if day >= 1 or day <= MONTH_DAY_COUNT[get_month(id) - 1] + extra_day:
            result[0] = day
    except:
        pass
    return result

def get_data(id:str) -> str:
    result = ""
    date = get_date(id)
    if date[2] != None:
        result += "Year: " + str(date[2]) + "\n"
    else:
        result += "Year: Unknown"
    if date[1] != None:
        result += "Month: " + str(date[1]) + "\n"
    else:
        result += "Month: Unknown"
    if date[0] != None:
        result += "Day: " + str(date[0]) + "\n"
    else:
        result += "Day: Unknown"
    sex = get_sex(id)
    if sex != None:
        result += "Sex: " + str(sex) + "\n"
    else:
        result += "Sex: Unknown"
    return result

def valid_id(id:str) -> bool:
    global CONTROL_CHARACTERS, CENTURY_CHARACTERS

    if not isinstance(id, str):
        return False

    if len(id) != 11: #Proper Finnish id is 11 characters long.
        return False

    id = id.upper() #Forcing to uppercase for simplicity.

    if id[6] not in CENTURY_CHARACTERS:
        return False

    if int(id[7:10]) < 2: #Indevidual number can't be less than 2.
        return False

    if None in get_date(id): #Validating the date.
        return False
            
    if id[10] != CONTROL_CHARACTERS[int(id[0:6] + id[7:10]) % 31]: #Valid control character.
        return False

    return True

def generateId(
        year_min:int = 1800, year_max:int = 2099, year:int or None = None,
        month_min:int = 1, month_max:int = 12, month:int or None = None,
        day_min:int = 1, day_max:int = 31, day:int or None = None,
        indevidual_number:int or None = None, sex:str or None = None,
        century_characters:list[str] or None = None
        ) -> str:
    #Prioritizes data in order of them appearing in a proper id.
    global GREATEST_POSSIBLE_YEAR, SMALLEST_POSSIBLE_YEAR, MONTH_DAY_COUNT, CENTURY_CHARACTERS_1800, CENTURY_CHARACTERS_1900, CENTURY_CHARACTERS_2000, CONTROL_CHARACTERS
    id = "0" * 11

    # ----- Year ----- #
    if year == None or year < SMALLEST_POSSIBLE_YEAR or year > GREATEST_POSSIBLE_YEAR:
        year = random.randint(max(year_min,SMALLEST_POSSIBLE_YEAR),min(year_max,GREATEST_POSSIBLE_YEAR))
    id = id[:4] + str(year)[2:4] + id[6:]

    # ----- Month ----- #
    if month == None or month < 1 or month > 12:
        month = random.randint(max(month_min,1), min(month_max,12))
    id = id[:2] + str(month).zfill(2) + id[4:]

    # ----- Day ----- #
    extra_day = 0
    if is_leap_year(year) and month == 2:
        extra_day = 1

    if day == None or day < 1 or day > MONTH_DAY_COUNT[month - 1] + extra_day:   
        day = random.randint(max(day_min, 1), min(day_max, MONTH_DAY_COUNT[month - 1] + extra_day))
    id = str(day).zfill(2) + id[2:]

    # ----- Century character ----- #     
    if century_characters != None: #Limited character set
        if year < 1900:
            century_characters = [x for x in century_characters if x in CENTURY_CHARACTERS_1800] #Limits symbols to only possible ones.
        elif year < 2000:
            century_characters = [x for x in century_characters if x in CENTURY_CHARACTERS_1900] #Limits symbols to only possible ones.
        elif year < 2100:
            century_characters = [x for x in century_characters if x in CENTURY_CHARACTERS_2000] #Limits symbols to only possible ones.
    else: #All possible character symbols
        if year < 1900:
            century_characters = CENTURY_CHARACTERS_1800
        elif year < 2000:
            century_characters = CENTURY_CHARACTERS_1900
        elif year < 2100:
            century_characters = CENTURY_CHARACTERS_2000
    id = id[:6] + random.choice(century_characters) + id[7:]

    # ----- Indevidual number ----- #
    if indevidual_number != None:
        match sex:
            case "m":
                indevidual_number = random.randrange(3, 999, 2)
            case "f":
                indevidual_number = random.randrange(2, 998, 2)
            case _:
                indevidual_number  = random.randint(2,999)
    id = id[:7] + str(indevidual_number).zfill(3) + id[10:]

    # ----- Control character ----- #
    return id[:10] + CONTROL_CHARACTERS[int(id[:6] + id[7:10]) % len(CONTROL_CHARACTERS)]

def test_id(id:str, expected_result:bool, explination:str = "") -> None:
    print("ID", id, "result", valid_id(id), "expected", expected_result, explination)

def test_series():
    test_id("290689-347P", True)
    test_id("290406+8895", True)
    test_id("070726-1335", True)
    test_id("300990-002W", True)
    test_id("260434+513A", True)

    test_id("420753-7715", False, "Incorrect day, can't be 42")
    test_id("1406897213", False, "Short")
    test_id("140608+3944M", False, "Long")
    test_id("251209-5607", False, "False incorrect control character")
    test_id("060916?753k", False, "Incorrect century character")

if __name__ == '__main__':
    test_series()