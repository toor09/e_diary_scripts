from random import choice, randint

from datacenter.models import Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.utils import DatabaseError

COMMENDATIONS = (
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
    "Ты, как всегда, точен!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Ты сегодня прыгнул выше головы!",
    "Я поражен!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Замечательно!",
    "Прекрасное начало!",
    "Так держать!",
    "Ты на верном пути!",
    "Здорово!",
    "Это как раз то, что нужно!",
    "Я тобой горжусь!",
    "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!",
    "Ты растешь над собой!",
    "Ты многое сделал, я это вижу!",
    "Теперь у тебя точно все получится!",
)


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


def create_commendation(schoolkid_name: str, subject_title: str) -> None:
    """Добавляет похвалу."""
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Школьник с именем: {schoolkid_name} не найден.")

    except MultipleObjectsReturned:
        raise MultipleObjectsReturned(f"Найдено несколько школьников с именем: {schoolkid_name}.")

    try:
        subject = Subject.objects.get(title=subject_title, year_of_study=schoolkid.year_of_study)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Предмета с таким названием {subject_title} не существует.")

    subject_lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject.title
    ).order_by("-date")

    random_lesson = subject_lessons[randint(1, len(subject_lessons))]

    commendation = {
        "text": choice(COMMENDATIONS),
        "created": random_lesson.date,
        "schoolkid": schoolkid,
        "subject": random_lesson.subject,
        "teacher": random_lesson.teacher

    }

    try:
        new_commendation = Commendation.objects.create(**commendation)
    except DatabaseError as err:
        raise DatabaseError(f"Что-то пошло не так: {err}.")

    print(
        f"Была добавлена похвала с тесктом {new_commendation.text} по предмету "
        f"{new_commendation.subject} от {new_commendation.created}."
    )
