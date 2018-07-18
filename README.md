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

## Предварительная обработка текста
Ведётся разработка предварительной обработки текста на Питоне "[/tools/preprocessing](https://github.com/vantu5z/RHVoice-dictionary/tree/master/tools/preprocessing)".<br>
Включает в себя обработку:

- дат;
- числительных;
- единиц измерения;
- сокращений;
- фраз, неподдерживаемых стандартным словарём RHvoice;
- преобразование римских чисел;
- преобразование греческих букв;
- и д.р.

## Обратная связь
Замечания, предложения, исправления и дополнения всегда приветствуются! <br>
Их можно оставить во вкладке [Issues](https://github.com/vantu5z/RHVoice-dictionary/issues).
