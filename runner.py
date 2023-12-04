import sys

from lib.file import read_course_instance
from lib.lib_date import get_actual_date
from model.observer.observer_pattern import ConcreteEvent, ConcreteObserver
import subprocess


def main(instance_name):
    print("Only instance:", instance_name)
    course_instances = read_course_instance()
    # print(course_instances.current_instance)
    observers = []
    events = {}
    for event in course_instances.events.keys():
        events[event] = ConcreteEvent(event)
    for instance in course_instances.instances.values():
        for trigger in events.keys():
            if len(instance_name) > 0:
                if instance_name == instance.name:
                    observer = ConcreteObserver(instance.name, instance.listen[trigger])
                    observers.append(observer)
                    events[trigger].attach(observer)
            else:
                observer = ConcreteObserver(instance.name, instance.listen[trigger])
                observers.append(observer)
                events[trigger].attach(observer)

    # for event in course_instances.events.keys():
    events["results_create_event"].notify()

if __name__ == "__main__":
    l_actual_date = get_actual_date()
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("sep23_prop_a")
        # main("")
    str1 = str((get_actual_date() - l_actual_date).seconds // 60) + ":" + str((get_actual_date() - l_actual_date).seconds % 60)
    print("Time running:", str1, "(m:ss)")
    print("Time running:", (get_actual_date() - l_actual_date).seconds, "seconds")




