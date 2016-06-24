# coding: utf8
import sys			# для разбора аргументов
import os			# для очистки экрана
import subprocess		# для функции RHVoice_say

# функция для произношения с использованием Speech Dispatcher
def RHVoice_say(text): 
  # -e, --pipe-mode (Pipe from stdin to stdout plus Speech Dispatcher)
  # -w, --wait (Wait till the message is spoken or discarded)
  p = subprocess.Popen(['spd-say', "-e", "-w"], stdin=subprocess.PIPE)
  p.communicate(text.encode('utf-8'))


# переменные
filename = sys.argv[1]
good = ''
bad = ''

# открываем файл
try:
  f = open(filename, 'r')   					# подгружаем файл для чтения
  line = f.readline()           				# читаем первую строку из файла
except:
  print('Ошибка открытия файла')
  exit()							# завершаем программу

# перебираем весь список
while line:

  os.system('clear')						# чистим экран
  print('Проверка набора фраз из:\n'+filename+'\n')

  RHVoice_say(line)						# произносим строку

  os.system('clear')						# т.к. RHVoice_say() выводит текст, то перерисуем вывод
  print('Проверка набора фраз из:\n'+filename+'\n')
  print('Фраза:  ' + line)

  print('[1]-хорошо, [2]-плохо, [3]-повторить, [4]-выйти')
  res = input('Решение: ')					# ждём реакцию

  if res=='1': good += line					# добавим строки в нужные списки
  if res=='2': bad  += line
  if res=='4': break						# выходим из цикла

  if (res=='1' or res=='2'): line = f.readline()		# читаем следующую строку, если не нужно повторить


print()		# выведем отступ

# если вышли раньше, чем прочитали весь файл, то запишем в файл непроверенные строки
if line:
  i=0
  try:
    f2 = open(filename + '.rest', 'w+') 			# создаём файл для записи
    while line:
      f2.write(line)
      line = f.readline()
      i+=1
    print('Записан файл с остатками: '+ os.path.basename(filename) + '.rest'+ '\nЗаписано: ' + str(i) + ' фраз(а)\n')
    f2.close() 				  
  except:
    print('Ошибка создания файла для записи остатков')

f.close()	# закрываем основной файл, т.к. весь прочитали и он нам больше не нужен

# запишем в файлы результаты нашего труда
if good!='':
  try:
    f3 = open(filename + '.good', 'w+')
    f3.write(good)  	
    f3.close()	
    print('Записан файл с хорошими фразами: '+ os.path.basename(filename) + '.good' + '\nЗаписано: ' + str(good.count('\n')) + ' фраз(а)\n')
  except:
    print('Ошибка создания файла для записи хороших фраз')

if bad!='':
  try:
    f4 = open(filename + '.bad', 'w+') 
    f4.write(bad)  	
    f4.close()	
    print('Записан файл с плохими фразами: '+ os.path.basename(filename) + '.bad' + '\nЗаписано: ' + str(bad.count('\n')) + ' фраз(а)\n')
  except:
    print('Ошибка создания файла для записи плохих фраз')

