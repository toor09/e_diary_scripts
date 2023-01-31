from datacenter.models import Chastisement, Mark, Schoolkid
from django.db.utils import DatabaseError


def fix_marks(schoolkid: Schoolkid) -> None:
    """Исправляет плохие оценки: 2 и 3 на 5."""
    bad_marks = Mark.objects.filter(schoolkid=schoolkid.pk, points__lt=4)
    start_bad_marks_count = len(bad_marks)
    if start_bad_marks_count > 0:
        for mark in bad_marks:
            mark.points = 5
        try:
            Mark.objects.bulk_update(bad_marks, ["points"])
        except DatabaseError as err:
            raise DatabaseError(f"Что-то пошло не так: {err}.")

        final_bad_marks_count = Mark.objects.filter(schoolkid=schoolkid.pk, points__lt=4).count()
        print(
            f"Было обработано {start_bad_marks_count} плохих оценок. Количество плохих оценок "
            f"после обработки {final_bad_marks_count}."
        )
    else:
        print("Отличная работа! У Вас нет плохих оценок.")


def remove_chastisements(schoolkid: Schoolkid) -> None:
    """Удаляет замечания."""
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid.pk)
    if len(chastisements) > 0:
        try:
            chastisements_count, _ = chastisements.delete()
            print(f"Было удалено {chastisements_count} замечаний.")
        except DatabaseError as err:
            raise DatabaseError(f"Что-то пошло не так: {err}.")
    else:
        print("Отличная работа! У Вас нет замечаний.")
