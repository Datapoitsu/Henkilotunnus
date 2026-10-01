## -------------------- Personal identification number tools ------------------------- ##
#Written by: Aarni Junkkala.

#Tools for Finnish personal identification numbers.

import random

control_characters = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","H","J","K","L","M","N","P","R","S","T","U","V","W","X","Y"]
decade_characters_1800 = ["+"]
decade_characters_1900 = ["-","Y","X","W","V","U"]
decade_characters_2000 = ["A","B","C","D","E","F"]
decade_characters = decade_characters_1800 + decade_characters_1900 + decade_characters_2000
month_day_count = [31,28,31,30,31,30,31,31,30,31,30,31]

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_sex(id:str) -> str or None:
    if int(id[9]) % 2 == 0:
        return "Female"
    return "Male"

def get_year(id:str) -> int or None:
    global decade_characters_1800, decade_characters_1900, decade_characters_2000
    if id[6] in decade_characters_1800:
        return int("18"+id[4:6])
    if id[6] in decade_characters_1900:
        return int("19"+id[4:6])
    if id[6] in decade_characters_2000:
        return int(20+id[4:6])
    return None

def get_month(id:str) -> int or None:
    try:
        month = int(id[2:4])
        if month < 1 or month > 12:
            return None
        return month
    except:
        return None

def get_day(id:str) -> int or None:
    try:
        return int(id[0:2])
    except:
        return None

def valid_id(id:str) -> bool:
    global control_characters, decade_characters_1800, decade_characters_1900, decade_characters_2000, decade_characters, month_day_count

    if len(id) != 11: #Proper Finnish id has lenght of 11.
        return False
    if not isinstance(id, str):
        return False
    
    id = id.upper() #Forcing to uppercase for simplicity.

    for i in range(6): #First 6 characters are numbers.
        if not id[i].isnumeric():
            return False

    if id[6] not in decade_characters:
        return False

    for i in range(7,10):
        if not id[i].isnumeric():
            return False

    if int(id[7:10]) < 2:
        return False

    if not id[10] in control_characters:
        return False

    year = get_year(id)
    if year == None:
        return False

    month = get_month(id)
    if month == None:
        return False

    
    if is_leap_year(year):
        month_day_count[1] += 1
    
    day = int(id[0:2])
    if day < 1 or day > month_day_count[month - 1]:
        return False
        
    if id[10] != control_characters[int(id[0:6] + id[7:10]) % 31]:
        return False

    return True

def generateId(
        year_min:int = 1800, year_max:int = 2099, year:int or None = None,
        month_min:int = 1, month_max:int = 12, month:int or None = None,
        day_min:int = 1, day_max:int = 31, day:int or None = None,
        sex:str or None = None,
        century_characters:list[str] or None = None
        ) -> str:
    global control_characters, decade_characters_1800, decade_characters_1900, decade_characters_2000, decade_characters, month_day_count

    id = "0" * 11
    
    if year == None or year < 1800 or year > 2099:
        if year_min < 1800:
            year_min = 1800
        if year_max > 2099:
            year_max = 2099
        year = random.randint(year_min,year_max)

    id = id[:4] + str(year)[2:4] + id[6:]

    if month == None or month < 1 or month > 12:
        if month_min < 1:
            month_min = 1
        if month_max > 12:
            month_max = 12
        month = random.randint(month_min,month_max)

    if month < 10:
        id = id[:3] + str(month) + id[4:]
    else:
        id = id[:2] + str(month) + id[4:]

    if is_leap_year(year):
        month_day_count[1] += 1

    if day == None or day < 1 or day > month_day_count[month - 1]:
        if day_min < 1:
            day_min = 1
        if day_max > month_day_count[month - 1]: #Limits the day to fit the month.
            day_max = month_day_count[month - 1]
    
        day = random.randint(day_min,day_max)

    if day < 10:
        id = id[:1] + str(day) + id[2:]
    else:
        id = str(day) + id[2:]

    # ----- Century character ----- #
    if year < 1900:
        id = id[:6] + "+" + id[7:]
    elif year < 2000:
        if century_characters != None:
            century_characters = [x for x in century_characters if x in decade_characters_1900] #Limits symbols to only possible ones.
        else:
            century_characters = decade_characters_1900
        id = id[:6] + random.choice(century_characters) + id[7:]
    elif year < 2100:
        if century_characters != None:
            century_characters = [x for x in century_characters if x in decade_characters_2000] #Limits symbols to only possible ones.
        else:
            century_characters = decade_characters_2000
        id = id[:6] + random.choice(century_characters) + id[7:]

    # ----- Indevidual number ----- #
    indevidual_number  = random.randint(2,999)
    if sex == "m":
        indevidual_number = random.randrange(3, 999, 2)
    elif sex == "f":
        indevidual_number = random.randrange(2, 998, 2)
    id = id[:7] + str(indevidual_number).zfill(3) + id[10:]

    # ----- Control character ----- #
    return id[:10] + control_characters[int(id[:6] + id[7:10]) % len(control_characters)]

def TestId():
    print(valid_id("290689-347P")) #True
    print(valid_id("290406+8895")) #True
    print(valid_id("070726-1335")) #True
    print(valid_id("300990-002W")) #True
    print(valid_id("260434+513A")) #True
    print(valid_id("420753-7715")) #False --> Incorrect day, can't be 42
    print(valid_id("1406897213")) #False --> Short
    print(valid_id("140608+3944M")) #False --> Long
    print(valid_id("251209-5607")) #False incorrect control character
    print(valid_id("060916?753k")) #Incorrect century character

if __name__ == '__main__':
    TestId()