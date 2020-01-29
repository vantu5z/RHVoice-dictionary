# Пакет для предварительной обработки текста

## Описание
Приводит в соответствие текст содержащий:

* даты;
* числительные;
* единицы измерения;
* сокращения;
* фразы, неподдерживаемые стандартным словарём RHvoice;
* римские числа;
* греческие буквы;
* и д.р.

## Установка
* Входит в AUR пакет для Arch пользователей [rhvoice-dictionary-git](https://aur.archlinux.org/packages/rhvoice-dictionary-git/).
* Для ручной установки в Linux:
```
git clone https://github.com/vantu5z/RHVoice-dictionary.git
cd RHVoice-dictionary/tools
python build.py
cp -R build/lib ~/.local
sudo cp rhvoice_say /usr/local/bin
```

## Использование
* Для подготовки текста необходимо импортировать функцию `text_prepare` и передать ей текст:
```
    from rhvoice_tools import text_prepare
    new_text = text_prepare(text)
```
* Для воспроизведения текста с предварительной обработкой:
```
    from rhvoice_tools import rhvoice_say
    rhvoice_say(text)
```    
* Для воспроизвдения из терминала:
```
    rhvoice_say "текск для чтения"
```

## Настройка
Параметры `rhvoice_say` расположены в `~/.config/rhvoice-say.conf`, файл создается при первом запуске `rhvoice-say`.

## Зависимости
* Python 3;
* Опционально [Pymorphy2](https://github.com/kmike/pymorphy2) (определение формы слова сторонней библиотекой, если не установлен, то будет использоваться встроенный словарь).
