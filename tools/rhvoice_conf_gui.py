#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GUI для настройки rhvoice.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import configparser
from os.path import exists as path_exists
from os.path import expanduser

from rhvoice_tools import rhvoice_say


class MainWindow(Gtk.Window):
    """
    Основное окно настроек.
    """
    def __init__(self):
        Gtk.Window.__init__(self, title="Настройки RHVoice")
        self.connect("delete-event", self.exit_app)

        self.config = Config()

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        # вкладка с настройками rhvoice_say
        # ====================================================================
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

        row += 1
        apply_btn = Gtk.Button(label='Применить')
        apply_btn.connect('clicked', self.apply_say_conf)
        apply_btn.set_halign(Gtk.Align.END)
        apply_btn.set_margin_top(20)
        conf_page_say.attach(apply_btn, 2, row, 1, 1)

        test_btn = Gtk.Button(label='Тест')
        test_btn.connect('clicked', self.run_test)
        test_btn.set_halign(Gtk.Align.START)
        test_btn.set_margin_top(20)
        conf_page_say.attach(test_btn, 0, row, 1, 1)

        self.notebook.append_page(conf_page_say,
                                  Gtk.Label(label='rhvoice_say'))
        # ====================================================================

        self.read_say_conf()

        self.show_all()

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

    def apply_say_conf(self, widget=None):
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
    Чтение и запись настроек.
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


def main():
    """
    Запуск.
    """
    win = MainWindow()
    Gtk.main()


if __name__ == '__main__':
    main()
