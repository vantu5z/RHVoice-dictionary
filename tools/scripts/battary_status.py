import psutil

def is_battery_low():
    """
    Проверка зарядки батареи.
    """
    battery = psutil.sensors_battery()

    if (not battery.power_plugged) and (battery.percent < 20):
        if  battery.percent > 10:
            return ("Низкий заряд батареи - battery.percent %%. "
                    "Подключите питание.")
        else:
            return ("Критический заряд батареи - battery.percent %%. "
                    "Срочно подключите питание.")
