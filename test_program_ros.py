import yaml


# Чтение данных yaml и преобразование в python-объекты
def read_input(filename):
    with open(filename, 'r') as f:
        return list(yaml.safe_load_all(f))


# Запись и преобразование python-объектов в yaml формат
def write_output(filename, data):
    with open(filename, 'w') as f:
        yaml.dump_all(data, f, default_flow_style=False, sort_keys=False)
        f.write('---\n')


# Находим скорость варщение и угол поворота
def convert_speeds(data, time):
    
    #Извлекаем линейную и угловую скорости
    linear_speed = data['twist']['linear']['x']
    angular_speed = data['twist']['angular']['z']

    # Рассчитываем скорость вращения приводного колеса
    rotation_speed = 0
    if angular_speed != 0:
        r = linear_speed / angular_speed
        rotation_speed = linear_speed / r

    # Рассчитываем угол поворота за это время
    rotation_angle = angular_speed * time

    return rotation_speed, rotation_angle


# Вычисление разницы во времени между двумя временными метками
def calc_time(start_stamp, end_stamp):
    start_time = start_stamp
    end_time = end_stamp
    time = end_time - start_time
    return time


def main():
    input_data = read_input('input_lite.yaml')
    output_data = []
    for i in range(len(input_data)-1):
        time = 0
        if input_data[i+1] is not None and input_data[i]['twist']['angular']['z'] != 0.0:

            # Рассчитываем разницу во времени между текущей и следующей меткой
            time = calc_time(input_data[i]['header']['stamp']
                             ['secs'] + (input_data[i]['header']['stamp']
                             ['nsecs'])/1e9, input_data[i+1]['header']['stamp']
                             ['secs'] + (input_data[i+1]['header']['stamp']
                                         ['nsecs']) / 1e9)
         
        rotation_speed, rotation_angle = convert_speeds(input_data[i], time)
        output_data.append({
            'linear': {
                'x': rotation_speed,
                'y': 0.0,
                'z': 0.0,
            },
            'angular': {
                'x': 0.0,
                'y': 0.0,
                'z': rotation_angle
            }
        })

        # Запись преобразованных данных в output_lite.yaml
    write_output('output_lite.yaml', output_data)


if __name__ == '__main__':
    main()
