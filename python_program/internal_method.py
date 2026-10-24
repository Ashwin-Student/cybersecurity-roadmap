class SmartPhone:
    def __init__(self):
        self.battery_level = 100

    def check_battery(self):
        if self.battery_level < 20:
            print("Warning: Battery is low!")

    def play_game(self):
        self.battery_level -= 30
        print("Battery level:", self.battery_level, "%")
        self.check_battery()


# Create an object
phone = SmartPhone()

# Play the game three times
phone.play_game()
phone.play_game()
phone.play_game()