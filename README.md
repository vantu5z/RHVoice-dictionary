RHVoice-dictionary
==================

Русский словарь в формате поддерживаемом [RHVoice](https://github.com/Olga-Yakovleva/RHVoice) v0.5+

## Установка словаря

### LINUX
* Пакет в AUR для Arch пользователей [rhvoice-dictionary-git](https://aur.archlinux.org/packages/rhvoice-dictionary-git/)
* Остальным, положить словари в директорию со словарями (по умолчанию `/etc/RHVoice/dicts/Russian/`)

### WINDOWS
* Путь для русских словарей: `%AppData%\RHVoice\dicts\Russian\`

### ANDROID
* Путь для русских словарей: `/sdcard/Android/data/com.github.olga_yakovleva.rhvoice.android/files/dicts/Russian/`

Примечание: После добавления словарей синтезатор необходимо перезагрузить (закрыть все программы, которые его используют), чтобы новые словари начали действовать.

## Дополнительные инструменты

Более подробное описание инструментов "[/tools](https://github.com/vantu5z/RHVoice-dictionary/tree/master/tools)"

* ### Предварительная обработка текста
    * Ведётся разработка предварительной обработки текста на Питоне "[/tools/preprocessing](https://github.com/vantu5z/RHVoice-dictionary/tree/master/tools/preprocessing)".

* ### Скрипты на Питоне
    * Вспомогательные скрипты.
    * Воспроизведение с помощью `rhvoice_say`.
    * GUI для настройки `rhvoice_config`.

## Обратная связь
Замечания, предложения, исправления и дополнения всегда приветствуются! <br>
Их можно оставить во вкладке [Issues](https://github.com/vantu5z/RHVoice-dictionary/issues).
