from random import choice, randint

from datacenter.models import Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject

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


def _get_schoolkid_instance(schoolkid_name: str) -> Schoolkid:
    """Возвращает инстанс модели Schoolkid."""
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        return schoolkid
    except Schoolkid.ObjectDoesNotExist:
        raise Schoolkid.ObjectDoesNotExist(f"Школьник с именем: {schoolkid_name} не найден.")
    except Schoolkid.MultipleObjectsReturned:
        raise Schoolkid.MultipleObjectsReturned(
            f"Найдено несколько школьников с именем: {schoolkid_name}. "
            f"Уточните имя."
        )


def _get_subject_instance(subject_title: str, schoolkid: Schoolkid) -> Subject:
    """Возвращает инстанс модели Subject."""
    try:
        subject = Subject.objects.get(title=subject_title, year_of_study=schoolkid.year_of_study)
        return subject
    except Subject.ObjectDoesNotExist:
        raise Subject.ObjectDoesNotExist(
            f"Предмета с таким названием {subject_title} не существует."
        )


def fix_marks(schoolkid: Schoolkid) -> None:
    """Исправляет плохие оценки: 2 и 3 на 5."""
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    start_count = bad_marks.count()
    if bad_marks:
        final_count = bad_marks.update(points=5)
        print(
            f"Было обработано {start_count} плохих оценок. Количество плохих оценок "
            f"после обработки {final_count - start_count}."
        )
    else:
        print("Отличная работа! У Вас нет плохих оценок.")


def remove_chastisements(schoolkid: Schoolkid) -> None:
    """Удаляет замечания."""
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    if chastisements:
        chastisements_count = chastisements.delete()
        print(f"Было удалено {chastisements_count} замечаний.")
    else:
        print("Отличная работа! У Вас нет замечаний.")


def create_commendation(schoolkid_name: str, subject_title: str) -> None:
    """Добавляет похвалу."""
    schoolkid = _get_schoolkid_instance(schoolkid_name=schoolkid_name)
    subject = _get_subject_instance(subject_title=subject_title, schoolkid=schoolkid)
    subject_lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject.title
    )
    random_lesson = subject_lessons[randint(1, len(subject_lessons))]
    commendation = {
        "text": choice(COMMENDATIONS),
        "created": random_lesson.date,
        "schoolkid": schoolkid,
        "subject": random_lesson.subject,
        "teacher": random_lesson.teacher

    }
    new_commendation = Commendation.objects.create(**commendation)
    print(
        f"Была добавлена похвала с тесктом {new_commendation.text} по предмету "
        f"{new_commendation.subject} от {new_commendation.created}."
    )


def run_fix_marks() -> None:
    """Запуск процесса корректировки оценок."""
    schoolkid_name = input("Введите имя: ")
    schoolkid = _get_schoolkid_instance(schoolkid_name=schoolkid_name)
    fix_marks(schoolkid=schoolkid)


def run_remove_chastisements() -> None:
    """Запуск процесса удаления замечаний."""
    schoolkid_name = input("Введите имя: ")
    schoolkid = _get_schoolkid_instance(schoolkid_name=schoolkid_name)
    remove_chastisements(schoolkid=schoolkid)


def run_create_commendation() -> None:
    """Запуск процесса добавления похвалы."""
    schoolkid_name = input("Введите имя: ")
    subject_title = input("Введите название предмета: ")
    create_commendation(schoolkid_name=schoolkid_name, subject_title=subject_title)


def main() -> None:
    """Запуск всех процессов для исправления оценок, удаления замечаний и добавление похвалы."""
    schoolkid_name = input("Введите имя: ")
    schoolkid = _get_schoolkid_instance(schoolkid_name=schoolkid_name)
    fix_marks(schoolkid=schoolkid)
    remove_chastisements(schoolkid=schoolkid)
    subject_title = input("Введите название предмета: ")
    create_commendation(schoolkid_name=schoolkid_name, subject_title=subject_title)


if __name__ == "__main__":
    main()
