from threading import Event
import time
from Alert import Alert

def main():
    flag1 = Event()
    flag2 = Event()
    all_flags = list()
    all_flags.append(flag1)
    all_flags.append(flag2)
    t1 = Alert(flag1, 60, "STT", "351")
    t2 = Alert(flag2, 60, "CSE", "498")
    t1.start()
    t2.start()
    #t1.update_timer(1) #updating the timer only works after the current timer finishes.
    time.sleep(1)
    t1.print_data()
    t2.print_data()
    print("Stopping all threads: ")
    for flag in all_flags:
        flag.set()
    print("All done.")

if __name__ == "__main__":
    main()

