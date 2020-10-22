#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GUI для настройки rhvoice.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

import configparser
import os
from os.path import exists as path_exists
from os.path import expanduser
from shlex import quote

from rhvoice_tools import rhvoice_say


class MainWindow(Gtk.Window):
    """
    Основное окно настроек.
    """
    def __init__(self):
        Gtk.Window.__init__(self, title="Настройки RHVoice")
        self.connect("delete-event", self.exit_app)

        self.config = Config()
        self.global_config = RHVoiceConfig()

        self.notebook = Gtk.Notebook()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.add(self.notebook)
        self.add(self.box)

        bottom_panel, self.test_btn, self.apply_btn = self.build_bottom_panel()
        self.box.add(bottom_panel)

        index = self.notebook.append_page(self.build_rhvoice_say_page(),
                                          Gtk.Label(label='rhvoice_say'))
        if len(self.global_config.options):
            self.gl_opts_grid = self.build_rhvoice_conf_page()
            self.notebook.append_page(self.gl_opts_grid,
                                      Gtk.Label(label='RHVoice.conf'))

        self.read_say_conf()
        self.show_all()
        self.notebook.set_current_page(index)

    def build_bottom_panel(self):
        """
        Нижняя панель с кнопками "Применить" и "Тест".
        """
        bottom_panel = Gtk.Box(hexpand=True)
        test_btn = Gtk.Button(label='Тест', margin=5)
        test_btn.connect('clicked', self.run_test)
        test_btn.set_halign(Gtk.Align.START)
        bottom_panel.pack_start(test_btn, True, True, 5)

        apply_btn = Gtk.Button(label='Применить', margin=5)
        apply_btn.set_halign(Gtk.Align.END)
        bottom_panel.pack_start(apply_btn, True, True, 5)
        apply_btn.connect('clicked', self.apply)

        return bottom_panel, test_btn, apply_btn

    def build_rhvoice_say_page(self):
        """
        Вкладка с настройками rhvoice_say.
        """
        conf_page_say = Gtk.Grid()
        conf_page_say.set_column_spacing(10)
        conf_page_say.set_row_spacing(5)
        conf_page_say.set_border_width(10)

        page_label = Gtk.Label(label='Настройки rhvoice_say')
        page_label.set_hexpand(True)
        page_label.set_margin_bottom(10)
        row = 0
        conf_page_say.attach(page_label, 0, row, 3, 1)
        
        row += 1
        use_spd_label = Gtk.Label(
            label='Использовать Speech Dispatcher:')
        use_spd_label.set_halign(Gtk.Align.START)
        conf_page_say.attach(use_spd_label, 0, row, 1, 1)
        self.use_spd_sw = Gtk.Switch()
        self.use_spd_sw.set_halign(Gtk.Align.END)
        conf_page_say.attach(self.use_spd_sw, 1, row, 1, 1)
        
        row += 1
        item_label = Gtk.Label(label='Громкость:')
        item_label.set_halign(Gtk.Align.START)
        conf_page_say.attach(item_label, 0, row, 1, 1)
        self.volume_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,
                                                     -100, 100, 1)
        self.volume_scale.set_size_request(100, -1)
        conf_page_say.attach(self.volume_scale, 1, row, 2, 1)

        row += 1
        item_label = Gtk.Label(label='Скорость:')
        item_label.set_halign(Gtk.Align.START)
        conf_page_say.attach(item_label, 0, row, 1, 1)
        self.rate_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,
                                                   -100, 100, 1)
        conf_page_say.attach(self.rate_scale, 1, row, 2, 1)

        row += 1
        item_label = Gtk.Label(label='Высота:')
        item_label.set_halign(Gtk.Align.START)
        conf_page_say.attach(item_label, 0, row, 1, 1)
        self.pitch_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,
                                                   -100, 100, 1)
        conf_page_say.attach(self.pitch_scale, 1, row, 2, 1)

        row += 1
        item_label = Gtk.Label(label='Голос:')
        item_label.set_halign(Gtk.Align.START)
        conf_page_say.attach(item_label, 0, row, 1, 1)
        self.combo_voice = Gtk.ComboBoxText()
        conf_page_say.attach(self.combo_voice, 1, row, 2, 1)

        row += 1
        item_label = Gtk.Label(label='Символ ударения:')
        item_label.set_halign(Gtk.Align.START)
        conf_page_say.attach(item_label, 0, row, 1, 1)
        self.use_stress_sw = Gtk.Switch()
        self.use_stress_sw.set_halign(Gtk.Align.END)
        conf_page_say.attach(self.use_stress_sw, 1, row, 1, 1)
        self.entry_stress = Gtk.Entry(xalign=0.5)
        self.entry_stress.set_max_length(1)
        conf_page_say.attach(self.entry_stress, 2, row, 1, 1)
        self.use_stress_sw.set_tooltip_text(
            'Включите для дополнительной обработки с использованием символа '
            'ударения.\n'
            '(cимвол должен совпадать с указанным в настройках rhvoice)')
        self.entry_stress.set_tooltip_text(
            'Cимвол должен совпадать с указанным в настройках rhvoice')
        self.use_stress_sw.connect('state-set', self.stress_changed)

        return conf_page_say

    def build_rhvoice_conf_page(self, conf_page=None):
        """
        Вкладка с глобальными настройками RHVoice.conf.
        conf_page - Gtk.Grid
        """
        if conf_page is None:
            conf_page = Gtk.Grid()
            conf_page.set_column_spacing(10)
            conf_page.set_row_spacing(5)
            conf_page.set_border_width(10)

        page_label = Gtk.Label(label='Настройки из файла RHVoice.conf')
        page_label.set_hexpand(True)
        page_label.set_margin_bottom(10)
        row = 0
        conf_page.attach(page_label, 0, row, 3, 1)

        row += 1
        section_lbl = Gtk.Label(label='Изменяемые параметры:')
        section_lbl.set_halign(Gtk.Align.START)
        conf_page.attach(section_lbl, 0, row, 3, 1)

        quality = self.global_config.get_option('quality')
        if quality is not None:
            row += 1
            item_label = Gtk.Label(label='Качество синтеза:')
            item_label.set_halign(Gtk.Align.START)
            item_label.set_margin_start(10)
            conf_page.attach(item_label, 0, row, 1, 1)

            self.combo_quality = Gtk.ComboBoxText()
            for i, value in enumerate(('min', 'standard', 'max')):
                self.combo_quality.append(str(i), value)
                if value == quality:
                    self.combo_quality.set_active(i)
            conf_page.attach(self.combo_quality, 1, row, 1, 1)

        stress_marker = self.global_config.get_option('stress_marker')
        if stress_marker is not None:
            row += 1
            item_label = Gtk.Label(label='Символ ударения:')
            item_label.set_halign(Gtk.Align.START)
            item_label.set_margin_start(10)
            conf_page.attach(item_label, 0, row, 1, 1)
            #self.use_stress_sw = Gtk.Switch()
            #self.use_stress_sw.set_halign(Gtk.Align.END)
            #conf_page.attach(self.use_stress_sw, 1, row, 1, 1)
            self.gl_entry_stress = Gtk.Entry(xalign=0.5)
            self.gl_entry_stress.set_max_length(1)
            self.gl_entry_stress.set_text(stress_marker)
            conf_page.attach(self.gl_entry_stress, 1, row, 1, 1)

        row += 1
        section_lbl = Gtk.Label(label='Остальные установленные параметры:')
        section_lbl.set_halign(Gtk.Align.START)
        section_lbl.set_margin_top(10)
        conf_page.attach(section_lbl, 0, row, 3, 1)

        for option, value in self.global_config.options.items():
            if option in ('stress_marker', 'quality'):
                continue    # пропускаем изменяемые
            row += 1
            item_label = Gtk.Label(label=option)
            item_label.set_halign(Gtk.Align.START)
            item_label.set_margin_start(10)
            conf_page.attach(item_label, 0, row, 1, 1)

            item_label = Gtk.Label(label=value)
            item_label.set_halign(Gtk.Align.CENTER)
            conf_page.attach(item_label, 1, row, 1, 1)

        row += 1
        open_editor = Gtk.Button(label='Открыть в редакторе', margin=10)
        open_editor.set_halign(Gtk.Align.CENTER)
        open_editor.connect("clicked", self.open_editor)
        conf_page.attach(open_editor, 0, row, 3, 1)

        conf_page.show_all()
        return conf_page

    def open_editor(self, widget=None):
        """
        Открывает редактор настроек и после обновляет данные в окне.
        """
        self.global_config.open_editor()
        self.update_data()

    def update_data(self):
        """
        Обновление данных на вкладке RHVoice.conf.
        """
        self.global_config.update()
        self.gl_opts_grid.foreach(self.gl_opts_grid.remove)
        self.build_rhvoice_conf_page(self.gl_opts_grid)

    def read_say_conf(self):
        """
        Обновление настроек из файла.
        """
        self.use_spd_sw.set_active(self.config.use_SD)
        self.volume_scale.set_value(self.config.volume)
        self.rate_scale.set_value(self.config.rate)
        self.pitch_scale.set_value(self.config.pitch)
        # заполняем комбобокс и устанавливаем текущий синтезатор в нём
        self.combo_voice.remove_all()
        for i, voice in enumerate(self.config.voices):
            self.combo_voice.append(str(i), voice)
            if voice == self.config.voice:
                self.combo_voice.set_active(i)
        self.stress_marker = self.config.stress_marker
        if self.stress_marker == False:
            self.use_stress_sw.set_active(False)
            self.entry_stress.set_text('')
            self.entry_stress.set_sensitive(False)
        else:
            self.use_stress_sw.set_active(True)
            self.entry_stress.set_text(self.stress_marker)
            self.entry_stress.set_sensitive(True)

    def stress_changed(self, widget, state):
        """
        Обработка переключателя "Символ ударения"
        """
        self.entry_stress.set_sensitive(state)

    def apply(self, widget=None):
        """
        Применение настроек в зависимости от открытой вкладки.
        """
        if self.notebook.get_current_page() == 0:
            self.apply_say_conf()
        else:
            self.global_config.write_conf(
                quality=self.combo_quality.get_active_text(),
                stress_marker=self.gl_entry_stress.get_text())
            self.update_data()

    def apply_say_conf(self):
        """
        Применение настроек для rhvoice_say.
        """
        self.config.use_SD = self.use_spd_sw.get_active()
        self.config.volume = self.volume_scale.get_value()
        self.config.rate = self.rate_scale.get_value()
        self.config.pitch = self.pitch_scale.get_value()
        self.config.voice = self.combo_voice.get_active_text()
        if self.use_stress_sw.get_active() and self.entry_stress.get_text():
            self.config.stress_marker = self.entry_stress.get_text()
        else:
            self.config.stress_marker = False
        self.config.write_conf()
        self.read_say_conf()

    def run_test(self, widget=None):
        """
        Воспроизведение тестового сообщения.
        """
        rhvoice_say('Проверка настройки синтезатора rhvoice')

    def exit_app(self, widget, event):
        """
        Выход.
        """
        Gtk.main_quit()


class Config():
    """
    Чтение и запись настроек rhvoice_say.
    """
    def __init__(self):
        # файл конфигурации
        self.file_name = expanduser("~") + '/.config/rhvoice_say.conf'
            
        self.config = configparser.ConfigParser(allow_no_value=True)
        # с учетом регистра
        self.config.optionxform = str

        self.voices = ['Aleksandr', 'Aleksandr+Alan', 'Artemiy', 'Anna',
                       'Elena', 'Elena+Clb', 'Irina']
        
        # установка настроек по-умолчанию
        self.use_SD = False
        self.voice = 'Aleksandr+Alan'
        self.volume = 0
        self.rate = 0
        self.pitch = 0
        self.stress_marker = False

        self.read_conf()

    def read_conf(self):
        """
        Чтение настроек из файла.
        """
        # открываем файл конфигурации
        if not path_exists(self.file_name):
            # если его нет - создаем новый
            self.write_conf()

        self.config.read(self.file_name)
        settings = self.config['Settings']

        self.use_SD = settings.getboolean('use_speech_dispatcher')
        self.voice = settings.get('voice')
        self.volume = settings.getint('volume')
        self.rate = settings.getint('rate')
        self.pitch = settings.getint('pitch')

        self.stress_marker = settings.get('use_stress_marker')
        if (self.stress_marker is None) or (self.stress_marker == 'False'):
            self.stress_marker = False

    def write_conf(self):
        """
        Запись в файл настроек.
        """
        self.config['Settings'] = {
            "; Использовать Speech Dispatcher для чтения ('True' или 'False')": None,
            'use_speech_dispatcher': self.use_SD,
            '; Громкость в процентах (от -100 до 100)': None,
            'volume': int(self.volume),
            '; Скорость в процентах (от -100 до 100)': None,
            'rate': int(self.rate),
            '; Высота в процентах (от -100 до 100)': None,
            'pitch': int(self.pitch),
            '; Голос для чтения': None,
            'voice': self.voice,
            '; Использовать символ для указания ударения (False или символ)': None,
            'use_stress_marker': self.stress_marker}
        with open(self.file_name, 'w') as configfile:
            self.config.write(configfile)


class RHVoiceConfig:
    """
    Глобальные настройки RHVoice.
    """
    def __init__(self):
        """
        Инициализация.
        """
        self.conf_file = None
        self.options = {}

        self.find_file()
        self.parse_conf()

    def find_file(self):
        """
        Поиск конфигурационного файла.
        """
        for path in ('/etc/RHVoice/RHVoice.conf',
                     '/usr/local/etc/RHVoice/RHVoice.conf'):
            if path_exists(path):
                self.conf_file = quote(path)
                break
        # TODO: доделать поиск в других местах и организовать выбор расположения

    def parse_conf(self):
        """
        Чтение всех найденных параметров из настроек в словарь.
        """
        if self.conf_file is None:
            return

        try:
            f = open(self.conf_file, 'r')     # открываем файл на чтение
        except:
            f = None
            return

        for line in f:
            # удаление пробелов в начале и конце строки
            line = line.strip()
            # пропуск комментариев и пустых строк
            if line.startswith(';') or len(line) == 0:
                continue
            # удаление лишних пробелов
            line = " ".join(line.split())

            option = line.split('=')
            self.options[option[0]] = option[1]

        if f is not None:
            f.close

    def get_option(self, option):
        """
        Чтение параметра по имени.
        Если параметр не задан или отсутсвует возвращает "None".
        """
        return self.options.get(option)

    def open_editor(self, widget=None):
        """
        Открывает файл настроек в редакторе (по умолчанию для пользователя).
        """
        if self.conf_file is not None:
            if os.access(self.conf_file, os.W_OK):
                os.system("xdg-open " + self.conf_file)
            else:
                # поиск редактора пользователя
                mime_type = Gio.content_type_guess(self.conf_file)
                app_infos = Gio.app_info_get_all_for_type(mime_type[0])
                if len(app_infos) > 0:
                    app_bin = app_infos[0].get_executable()
                    # запуск редактора с правами root
                    env = 'DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY'
                    os.system("pkexec env %s %s %s"
                              % (env, quote(app_bin), self.conf_file))

    def write_conf(self, quality, stress_marker):
        """
        Запись изменений в файл.
        """
        if self.conf_file is None:
            return

        try:
            f = open(self.conf_file, 'r')     # открываем файл на чтение
        except:
            f = None
            return

        content = ''

        for line in f:
            # удаление пробелов в начале и конце строки
            line = line.strip()
            # обработка комментариев и пустых строк
            if line.startswith(';') or len(line) == 0:
                content += line + '\n'
                continue
            # удаление лишних пробелов
            line = " ".join(line.split())

            option = line.split('=')
            if len(option) == 2:
                if option[0] == 'quality':
                    content += 'quality=' + quality + '\n'
                elif option[0] == 'stress_marker':
                    content += 'stress_marker=' + stress_marker + '\n'
                else:
                    content += line + '\n'
            else:
                content += line + '\n'

        if f is not None:
            f.close

        # запись изменений в файл из-под root
        os.system("echo %s > /tmp/rhvoice_conf_tmp" % quote(content))
        os.system("pkexec cp /tmp/rhvoice_conf_tmp %s" % self.conf_file)

    def update(self):
        """
        Обновление данных из изменённого файла.
        """
        self.options.clear()
        self.parse_conf()


def main():
    """
    Запуск.
    """
    win = MainWindow()
    Gtk.main()


if __name__ == '__main__':
    main()
