# Скрипты для исправления успеваемости [электронного дневника](https://github.com/toor09/e-diary) 

## Установка

- Скачайте код.
- Установите актуальную версию poetry в `UNIX`-подобных дистрибутивах с помощью команды:
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
```
или в `Windows Powershell`:
```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```
- Добавьте к переменной окружения `$PATH` команду poetry:
```
source $HOME/.poetry/bin
```
- Установите виртуальное окружение в директории с проектом командой:
```
poetry config virtualenvs.in-project true
```
- Установите все зависимости (для установки без dev зависимостей можно добавить аргумент `--no-dev`):
```
poetry install
```
- Активируйте виртуальное окружение командой: 
```
source .venv/bin/activate
```

## Запуск линтеров

```
isort . && flake8 . && mypy .
```

## Запуск

- Можно исправить оценки.
- Убрать замечания. 
- Добавить похвальные записи.

Скрипт должен лежать в корне сайта рядом с `manage.py`. Для запуска скрипта сайт должен быть поднят.
```
python3 manage.py shell
```
```python3
from scripts import main
main()
```

## Цели проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](https://dvmn.org).
