import datetime


def get_date_range(months):
    currentDate = datetime.date.today()
    currentYear = currentDate.year
    currentMonth = currentDate.month

    startDate = datetime.date(currentYear, currentMonth, 1)
    endDate = currentDate

    if months > 0:
        for i in range(1, months):
            prevMonth = currentMonth - i
            if prevMonth <= 0:
                prevMonth += 12
                currentYear -= 1
            startDate = datetime.date(currentYear, prevMonth, 1)

    return startDate, endDate
