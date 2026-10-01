# Content Generator

Цей генератор перетворює розпарсені розділи FAA-посібників на готові MDX-сторінки для навчального застосунку Aviation Camp.

## Що робить генератор

Скрипт `scripts/generate_content.py`:

1. Читає розділи з `resources/parsed/<BookName>`.
2. Завантажує текст розділу з `content.md` або резервного файлу `content_raw.txt`; для нового парсерного виводу зберігає inline emphasis та позиції вбудованих figure-блоків.
3. Завантажує доступні зображення з `images_manifest.json`.
4. Формує запит до Gemini з правилами для навчального авіаційного контенту.
5. Генерує англомовну MDX-сторінку з:
   - YAML frontmatter;
   - поясненням ключових понять;
   - практичним застосуванням і застереженнями;
   - callout-блоками;
   - зображеннями, якщо вони доступні;
   - компонентом `Quiz` із 3–5 питаннями.
6. Перевіряє результат: наявність frontmatter, обов’язкових полів, англійської мови, правильного subject і `translationKey`.
7. Зберігає результат у `src/content/docs/<BookName>/<chapter>.mdx`.

## Вхідні дані

Перед запуском потрібно виконати PDF-парсер. Для кожної книги очікується така структура:

```text
resources/parsed/PHAK/
  book_manifest.json
  ch01/
    content.md
    images_manifest.json
  ch02/
    content.md
```

Назви книг мають відповідати підтриманим ідентифікаторам: `AFH`, `Instrument`, `InstrumentProcedures`, `PHAK`, `RiskManagement`, `Weather`, `WeightBalance`.

## Налаштування Gemini

Створіть `.env` у корені проєкту та додайте API-ключ:

```env
GEMINI_API_KEY=your_api_key_here
```

Також можна використати `GOOGLE_API_KEY`. Модель за замовчуванням визначається змінною `GEMINI_MODEL`; якщо її не задано, використовується `gemini-3.8-flash`.

Встановіть Python-залежності та активуйте віртуальне середовище:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

Згенерувати контент для всіх доступних книг:

```bash
python scripts/generate_content.py
```

Згенерувати контент лише для однієї книги:

```bash
python scripts/generate_content.py --book PHAK
```

Перевірити список розділів без запису MDX-файлів:

```bash
python scripts/generate_content.py --book PHAK --dry-run
```

Обробляти розділи послідовно з паузою між API-запитами:

```bash
python scripts/generate_content.py --book PHAK --serial --delay-seconds 5
```

Параметри командного рядка:

| Параметр | Призначення |
| --- | --- |
| `--book NAME` | Обробити лише книгу з `resources/parsed/NAME` |
| `--dry-run` | Показати метадані без створення MDX-файлів |
| `--serial` | Додавати паузу між розділами |
| `--delay-seconds N` | Тривалість паузи в режимі `--serial`, за замовчуванням `5` секунд |

## Результат

Для кожної книги генератор створює MDX-файли в окремій директорії:

```text
src/content/docs/PHAK/
  ch01.mdx
  ch02.mdx
```

Кожен файл містить обов’язкові поля:

```yaml
title: "Principles of Flight — Chapter 1"
description: "..."
subject: "Pilot's Handbook of Aeronautical Knowledge"
chapterNumber: 1
readTimeMinutes: 8
lang: "en"
translationKey: "phak-ch01"
```

`translationKey` формується стабільно з назви книги та розділу, щоб у майбутньому можна було додати переклади.

## Обробка помилок і fallback

Gemini викликається максимум тричі. Для тимчасових помилок або перевищення квоти генератор автоматично чекає перед повторною спробою.

Якщо API не повернув коректний MDX, результат не втрачається: генератор створює fallback-сторінку на основі вихідного тексту. Вона також містить frontmatter, короткий виклад, базові callout-блоки та quiz.

Якщо розділ порожній, fallback-сторінка створюється без використання API.

## Валідація

Тести генератора перевіряють завантаження parsed-файлів, формування metadata, стабільні translation keys, назви посібників, оцінку часу читання та захист від неангломовного результату:

```bash
python -m unittest tests.test_generate_content -v
```

Перед генерацією контенту переконайтеся, що парсер уже завершив роботу. Опис підготовки PDF і створення `resources/parsed` наведено в [README_parser.md](README_parser.md).