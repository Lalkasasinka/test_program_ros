import yaml


# Преобразование данных скоростей в скорости вращения и углы поворота
def convert_speeds(linear_speed, angular_speed):
    rotation_speed = 0
    rotation_angle = 0
    # Если робот не стоял на месте
    if angular_speed != 0:
        # Находим радиус
        wheel_radius = linear_speed / angular_speed
        # Находим скорость вращения
        rotation_speed = linear_speed / wheel_radius
        # Находим угол поворота
        rotation_angle = angular_speed * wheel_radius
        return rotation_speed, rotation_angle
    return rotation_speed, rotation_angle


# Чтение данных yaml и преобразование в python-объекты
def read_input(filename):
    with open(filename, 'r') as f:
        return list(yaml.safe_load_all(f))


# Запись и преобразование python-объектов в yaml формат
def write_output(filename, data):
    with open(filename, 'w') as f:
        yaml.dump_all(data, f, default_flow_style=False, sort_keys=False)
        f.write('---\n')


def main():
    input_data = read_input('input_lite_example.yaml')
    output_data = []
    for obj in input_data:
        linear_speed = obj['twist']['linear']['x']
        angular_speed = obj['twist']['angular']['z']
        rotation_speed, rotation_angle = convert_speeds(linear_speed,
                                                        angular_speed)
        output_data.append({
            'linear': {
                'x': rotation_speed,
                'y': 0.0,
                'z': 0.0
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
