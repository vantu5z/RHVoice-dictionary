# Инструменты

## Описание

Вспомогательные иструменты разделены на несколько частей:

* Предварительная обработка текста "[/tools/preprocessing](https://github.com/vantu5z/RHVoice-dictionary/tree/master/tools/preprocessing)"
* Вспомогательые скрипты.
* Воспроизведение с помощью `rhvoice_say`.
* GUI для настройки `rhvoice_config`.

## Установка

Входит в AUR пакет для Arch пользователей [rhvoice-dictionary-git](https://aur.archlinux.org/packages/rhvoice-dictionary-git/).<br>
Для ручной установки в Linux (для пользователя):
```
git clone https://github.com/vantu5z/RHVoice-dictionary.git
cd RHVoice-dictionary/tools
python build.py
cp -R build/usr/lib ~/.local
cp -R build/usr/bin ~/.local
```

## Использование

* Для воспроизведения текста с предварительной обработкой:
```
    from rhvoice_tools import rhvoice_say
    rhvoice_say(text)
```
* Для воспроизвдения из терминала:
```
    rhvoice_say "текст для чтения"
    rhvoice_say -c
    echo "текст для чтения" | rhvoice_say
```
* Примеры использования скриптов "[/scripts/examples](https://github.com/vantu5z/RHVoice-dictionary/tree/master/tools/scripts/examples)"

## Настройка

Параметры `rhvoice_say` расположены в `~/.config/rhvoice_say.conf`, файл создается при первом запуске `rhvoice_say` или `rhvoice_config`.<br>
Для настройки в графическом режиме используйте `rhvoice_config`.

## Зависимости
* Python 3;
* Опционально [Pymorphy2](https://github.com/kmike/pymorphy2) (определение формы слова сторонней библиотекой, если не установлен, то будет использоваться встроенный словарь).
