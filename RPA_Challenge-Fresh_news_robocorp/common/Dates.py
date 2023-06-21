import datetime


def get_date_range(months):
    current_date = datetime.date.today()
    current_year = current_date.year
    current_month = current_date.month

    start_date = datetime.date(current_year, current_month, 1)
    end_date = current_date

    if months > 0:
        for i in range(1, months):
            prev_month = current_month - i
            if prev_month <= 0:
                prev_month += 12
                current_year -= 1
            start_date = datetime.date(current_year, prev_month, 1)

    return start_date, end_date
