from datetime import date, datetime


def calculate_age(birth_date):

    print(birth_date)
    print(type(birth_date))

    today = date.today()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )

    return age


def calculate_value(age):
    if age < 21:
        return 100.00
    elif age < 60:
        return 150.00
    else:
        return 200.00
