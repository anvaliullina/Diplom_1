# Задание 1 — юнит-тесты Burger

25 параметризованных запусков. Моки `unittest.mock.Mock(spec=Bun/Ingredient)`
изолируют Burger от реализации булочек и начинок.
Проверяются начальное состояние, установка/замена булки, добавление/удаление/перемещение,
цена двух половинок булки и всех ингредиентов, точный формат чека и изменение порядка слоёв.

Исходники взяты из https://github.com/Yandex-Practicum/qa-python-diplom
(ссылка перенаправляет на qa-python-project), commit
`c7c7e92ac4cbbe887236dbb76c4c87e7792edab5`.
Файлы программы перенесены в пакет `praktikum/`, чтобы существующие абсолютные импорты
`from praktikum...` работали. Содержимое исходных Python-файлов не изменено.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
```

Покрытие измеряется для **класса Burger / praktikum.burger**, как указано в задании.
Не заявляется 100% покрытия вспомогательных Bun, Ingredient, Database и демонстрационного main.
В pytest.ini включены branch coverage и порог 100%; при снижении покрытия команда падает.
Отчёты: `htmlcov/index.html`, `coverage.xml`.

На проверке в среде подготовки: 25 passed, 27 строк, 4 ветви, 100%.
Ветка для сдачи: develop1. См. общую инструкцию GITHUB_NEXT.md.
