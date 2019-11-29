from threading import Event
import time
from Alert import Alert


def terminate_threads(all_flags):
    for flag in all_flags:
        flag.set()
    #...

def get_alert_parameters():
    class_code = str(input("Enter class code (q to quit): ")).upper()
    if class_code == "Q":
        return []
    course_num = str(input("Enter course number (q to quit: "))
    if course_num.lower() == "q":
        return []
    refresh_time = 10
    try:
        refresh_time = int(input("Enter refresh time for alert (in min): "))
    except ValueError:
        print("Error: You didn't enter an integer.")
        return []  #return false if we just had an input error
    return [class_code, course_num, refresh_time] #return this list.

def get_update_parameters(all_alerts):
    index = 0
    try:
        index = int(input("Enter index of the alert to update: "))
    except ValueError:
        print("Error: You didn't enter an integer.")
    if index < 0 or index >= len(all_alerts):
        print("Error: Index out of bounds.")
        return []
    new_time = 1
    try:
        new_time = int(input("Please enter new refresh time (in min): "))
    except ValueError:
        print("Error: You didn't enter an integer.")
        return []
    return [index, new_time]

def print_alerts(all_alerts):
    for i in range(len(all_alerts)):
        print("[{}]: {} {}".format(i, all_alerts[i].course_code, all_alerts[i].class_num))
    print() #print a newline at the end.


def main():
    #let's work on user input
    valid_commands = {"help" : "shows the list of available commands", "alert" :
        "set up a new alert", "status" : "see the status of "
                    "alerts", "update" : "update an alert's refresh time", "q" : "quit the program"}
    all_flags = list()
    all_alerts = list()
    while True:
        cmd = input("Please enter a command (help to get help): ").strip().lower()
        if cmd == "help":
            for k,v in valid_commands.items():
                print("{}: {}".format(k, v))
        elif cmd == "alert":
            inputs = get_alert_parameters()
            if len(inputs) == 0:
                continue
            #otherwise, we got valid inputs,
            print("Setting up alert...", end="")
            f = Event()
            a1 = Alert(f, inputs[0], inputs[1], inputs[2])
            all_flags.append(f)
            a1.start()
            all_alerts.append(a1)
            print("Done.")
        elif cmd == "status":
            for alert in all_alerts:
                alert.print_data()
        elif cmd == "update":
            #we're going to let users update the refresh time.
            #any maybe other stuff in the future, but for now, this works.
            #let's print alerts with indices first:
            if len(all_alerts) == 0:
                print("There are currently no active alerts.")
            print_alerts(all_alerts)
            inputs = get_update_parameters(all_alerts)
            if len(inputs) == 0:
                continue
            all_alerts[inputs[0]].update_timer(inputs[1])
            print("New refresh time will be implemented whenever that alert updates next.")
        elif cmd == "q" or cmd == "quit" or cmd == "exit":
            print("Quitting...")
            terminate_threads(all_flags)
            break
        else:
            print("{}: not recognized.".format(cmd))
    pass
if __name__ == "__main__":
    main()

