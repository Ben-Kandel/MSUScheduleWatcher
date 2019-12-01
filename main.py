from threading import Event
#import time
from Alert import Alert

def terminate_threads(all_flags):
    for flag in all_flags:
        flag.set()
    #...

def get_alert_parameters():
    result = [] #the list we are returning
    class_code = str(input("Enter class code (q to quit): ")).upper()
    if class_code == "Q":
        return []
    print("You can specify multiple classes in this course by separating them by space, ie. 351 430 441")
    course_num = str(input("Enter course number(s) (q to quit): "))
    if course_num.lower() == "q":
        return []
    #now we should figure out if we were given multiple classes.
    course_num = course_num.split()
    """
    okay, we need to think. we're returning a list of lists,
    """

    refresh_time = 10 #default refresh time.
    try:
        refresh_time = int(input("Enter refresh time for alert (in min): "))
    except ValueError:
        print("Error: You didn't enter an integer.")
        return []  #return false if we just had an input error
    result.append(class_code)
    for num in course_num:
        result.append(num)
    result.append(refresh_time)
    return result
    #return [class_code, course_num, refresh_time] #return this list.

def update_alert_time(all_alerts, index):
    new_time = 1
    try:
        new_time = int(input("Please enter new refresh time (in min): "))
    except ValueError:
        print("Error: You didn't enter an integer.")
        return
    all_alerts[index].update_timer(new_time)
    print("New refresh time will be implemented whenever that alert updates next.")

def update_alert_notifications(all_alerts, index):
    new_method = str(input("Turn notifications on or off? (y for on, n for off): ")).lower()
    if new_method == 'y':
        all_alerts[index].should_notify(True)
        print("Enabled text notifications for {} {}".format(all_alerts[index].course_code, all_alerts[index].class_num))
    elif new_method == 'n':
        all_alerts[index].should_notify(False)
        print("Disabled text notifications for {} {}".format(all_alerts[index].course_code, all_alerts[index].class_num))
    else:
        print("Error: y/n not entered.")

def print_alerts(all_alerts):
    for i in range(len(all_alerts)):
        print("[{}]: {} {}".format(i, all_alerts[i].course_code, all_alerts[i].class_num))
    print() #print a newline at the end.


def main():
    valid_commands = {"help" : "shows the list of available commands", "alert" :
        "set up a new alert", "status" : "see the status of "
                    "alerts", "update" : "update an alert's refresh time", "q" : "quit the program"}
    all_flags = list()
    all_alerts = list()

    print("Welcome to MSU-Schedule-Watcher. Interact with the console by typing. To get a list of commands,")
    print("Type 'help'. Text notifications are off by default. Please use the 'update' command to change that.")
    print("Please refer to schedule.msu.edu to see a list of acceptable course codes and class numbers.")

    print("Please enter a phone number to receive alerts at, ", end="")
    phone_num = input("including country and area code: ")

    while True:
        cmd = input("Please enter a command: ").strip().lower()
        if cmd == "help":
            for k,v in valid_commands.items():
                print("{}: {}".format(k, v))
        elif cmd == "alert":
            inputs = get_alert_parameters()
            if len(inputs) == 0:
                continue
            #otherwise, we got valid inputs,
            courses = inputs[1:len(inputs)-1] #grab all of the courses the user supplied
            if len(courses) > 1:
                print("Setting up alerts...", end="")
            else:
                print("Setting up alert...", end="")
            for c in courses:
                f = Event()
                a = Alert(f, inputs[0], c, inputs[-1], phone_num)
                all_flags.append(f)
                a.start()
                all_alerts.append(a)
            print("Done.")
        elif cmd == "status":
            for alert in all_alerts:
                alert.print_data()
        elif cmd == "update":
            #we're going to let users update the refresh time and notification method.
            #any maybe other stuff in the future, but for now, this works.
            #let's print alerts with indices first:
            if len(all_alerts) == 0:
                print("There are currently no active alerts.")
                continue
            print("0: Update refresh time | 1: Turn on/off text notifications |")
            choice = 0
            try:
                choice = int(input("Please specify type of update: "))
            except ValueError:
                print("Error: Please enter an integer.")
                continue
            if choice < 0 or choice > 1:
                print("Error: Please enter a valid number.")
                continue

            index = 0
            print_alerts(all_alerts)
            try:
                index = int(input("Enter index of the alert to update: "))
            except ValueError:
                print("Error: You didn't enter an integer.")
                continue
            if index < 0 or index >= len(all_alerts):
                print("Error: Index out of bounds.")
                continue

            if choice == 0:
                update_alert_time(all_alerts, index)
            elif choice == 1:
                update_alert_notifications(all_alerts, index)
        elif cmd == "q" or cmd == "quit" or cmd == "exit" or cmd == "end":
            print("Quitting...")
            terminate_threads(all_flags)
            break
        else:
            print("{}: not recognized.".format(cmd))
    pass #end of while loop.

if __name__ == "__main__":
    main()

