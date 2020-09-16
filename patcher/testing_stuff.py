class Robots:
    def __init_(self):
        self.ai = ai

    def define_robot(self, name, eye_color, weight):
        self.name = name
        self.eye_color = eye_color
        self.weight = weight

    def introduce(self):
        print(f"Hi my name is {self.name} ,", f"my eyes are {self.eye_color}", f"and I weigh {self.weight}.")


robot_one = Robots()

robot_one.define_robot("sally", "blue", 100)

robot_one.introduce()

robot_two = Robots()

robot_two.define_robot("Billy", "not blue", "not 100")

robot_two.introduce()
robot_one.introduce()
