#----------------------------------------------------------------------
# Contributors:
# Jewel Merriman, Rishabh Jain
#
#----------------------------------------------------------------------
import datetime
import pytz

def time_of_day(date, time):
    lunch_start = datetime.time(11, 0)       
    dinner_start = datetime.time(14, 0)
    is_weekend_var = is_weekend(date)

    if time > dinner_start:
         return 'Dinner'
    elif time > lunch_start:
        return 'Lunch'
    else:
        if is_weekend_var:
            return 'Lunch'
        else:
            return 'Breakfast'

def custom_strftime(date_obj):
    suffix = 'th' if 11 <= date_obj.day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(date_obj.day % 10, 'th')
    return date_obj.strftime('%A, %B %d') + suffix

def is_weekend(date):
    day_of_week = date.weekday()
    return (day_of_week >= 5)

# returns calories of carbs, fats, proteins
def gtocal(carbs, fats, proteins):
    return carbs*4, fats*9, proteins*4

# returns the arrays: cal, carb, prot, fat, date
# where cal carb prot fat are all arrays with non-zero values
# and date is the corresponding date array for those entries
def get_corresponding_arrays(cal, carb, prot, fat):
    # generate date array
    eastern = pytz.timezone('US/Eastern')
    today = datetime.now(eastern).date()
    date_array = [today - timedelta(days=i) for i in range(len(cal))]

    # filter date and array for non-zero entries
    filtered_date_array = []
    filtered_cal_array = []

    for date_val, cal_val in zip(date_array, cal):
        if cal_val != 0:
            filtered_date_array.append(date_val.strftime('%Y-%m-%d'))
            filtered_cal_array.append(cal_val)
    filtered_carb_array = [x for x in carb if x != 0]
    filtered_prot_array = [x for x in prot if x != 0]
    filtered_fat_array = [x for x in fat if x != 0]
    return filtered_cal_array, filtered_carb_array, filtered_prot_array, filtered_fat_array, filtered_date_array

# returns average of array over the past ndays
# if length of array is less that ndays, just returns average of the array
def get_average(array, ndays):
    length = 0
    sum = 0
    if (len(array) > ndays):
        array = array[:ndays]
    for el in array:
        if el != 0:
            sum = sum + el
            length = length + 1
    return sum/length

def main():
    # Unit testing checks of functions
    date = datetime.datetime(2024, 3, 25)
    time = datetime.time(4, 0)
    print(time_of_day(date, time) == 'Breakfast')

    date = datetime.datetime(2024, 3, 23)
    time = datetime.time(4, 0)
    print(time_of_day(date, time) == 'Lunch')

    date = datetime.datetime(2024, 3, 23)
    time = datetime.time(12, 0)
    print(time_of_day(date, time) == 'Lunch')

    date = datetime.datetime(2024, 3, 23)
    time = datetime.time(1, 0)
    print(time_of_day(date, time) == 'Lunch')
    
    date = datetime.datetime(2024, 3, 26)
    time = datetime.time(12, 0)
    print(time_of_day(date, time) == 'Lunch')

    date = datetime.datetime(2024, 3, 26)
    time = datetime.time(14, 1)
    print(time_of_day(date, time) == 'Dinner')

    date = datetime.datetime(2024, 3, 26)
    time = datetime.time(19, 0)
    print(time_of_day(date, time) == 'Dinner')
    return

if __name__ == "__main__":
    main()