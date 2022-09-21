from .models import Grade


def place_rating(pk):
    """ count rating by dividing two values: sum of grades and number of grades"""

    lst_place_grades = Grade.objects.filter(place_id=pk)
    rate_amount = len(lst_place_grades)
    rate_lst = [i.grade for i in lst_place_grades]
    rating = int(sum(rate_lst) / len(rate_lst)) if rate_lst else 0
    return rating, rate_amount