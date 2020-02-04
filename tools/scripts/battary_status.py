import psutil

def is_battery_low():
    """
    Проверка зарядки батареи.
    """
    battery = psutil.sensors_battery()

    if (not battery.power_plugged) and (battery.percent < 20):
        if  battery.percent > 10:
            return ("Низкий заряд батареи - %d %%. "
                    "Подключите питание." % battery.percent)
        else:
            return ("Критический заряд батареи - %d %%. "
                    "Срочно подключите питание." % battery.percent)
