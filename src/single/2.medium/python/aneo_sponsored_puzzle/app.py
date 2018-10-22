import sys
import copy
from fractions import Fraction


class Light:
    def __init__(self, distance, duration, is_green):
        self.distance = distance
        self.duration = duration
        self.is_green = is_green

    def __str__(self):
        return "is_green: {is_green}, distance: {distance}, duration: {duration}".format(is_green=self.is_green,
                                                                                         distance=self.distance,
                                                                                         duration=self.duration)

    def switch(self):
        self.is_green = not self.is_green


class Car:
    def __init__(self, speed):
        self.speed = speed  # km/h
        self.converted_speed = self.km_h_2_m_s(self.speed)  # m/s
        self.distance = Fraction(0)

    def __str__(self):
        return "speed: {speed}, converted_speed: {converted_speed}, distance: {distance}".format(speed=self.speed,
                                                                                                 converted_speed=self.converted_speed,
                                                                                                 distance=self.distance)

    def km_h_2_m_s(self, speed):
        return Fraction(speed * 1000, 3600)

    def set_speed(self, speed):
        self.speed = speed
        self.converted_speed = self.km_h_2_m_s(speed)


class Game:
    def __init__(self, max_speed, lights, car):
        self.max_speed = max_speed
        self.lights = lights
        self.car = car

    def __str__(self):
        return "max_speed: {max_speed}, car: {car}\nlights: {lights}".format(max_speed=self.max_speed,
                                                                             car=self.car,
                                                                             lights="\n".join([str(light) for light in self.lights]))

    def print_debug(self, description):
        print(description, file=sys.stderr)

    def simulate(self, car, lights):
        max_distance = lights[-1].distance
        max_time = round(max_distance / car.converted_speed)

        go_through = True
        for time_trigger in range(max_time + 1):

            # switch lights if needed
            filtered_lights = [light for light in lights if max(1, time_trigger) % light.duration == 0]
            for light in filtered_lights:
                light.switch()

            # check car can pass
            next_lights = [light for light in lights if light.distance >= car.distance]
            if len(next_lights) != 0:
                next_light = next_lights[0]
                if (Fraction(car.distance) + Fraction(car.converted_speed) > next_light.distance) and not next_light.is_green:
                    go_through = False
                    break
            # move the car
            car.distance = Fraction(car.distance) + Fraction(car.converted_speed)
        return go_through

    def play(self):
        for speed in range(self.max_speed, 0, -1):
            self.car.set_speed(speed)
            res = self.simulate(copy.deepcopy(self.car), copy.deepcopy(self.lights))
            if res:
                return speed


def my_main():
    max_speed = int(input())

    light_count = int(input())
    lights = []
    for i in range(light_count):
        distance, duration = [int(j) for j in input().split()]
        lights.append(Light(distance, duration, True))

    car = Car(0)
    game = Game(max_speed, lights, car)

    res = game.play()
    print(res)


if __name__ == '__main__':
    my_main()
