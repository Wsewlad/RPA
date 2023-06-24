import datetime


def get_date_range(months):
    """
    Calculate the date range based on the number of past months.

    Args:
        `months (int)`: Number of past months to include in the date range.

    Returns:
        `tuple`: A tuple containing the start date and end date of the date range.

    Example:
    ```
        start_date, end_date = get_date_range(3)
        print(start_date)  # Output: 2023-03-01
        print(end_date)  # Output: 2023-05-30
    ```
    """
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
