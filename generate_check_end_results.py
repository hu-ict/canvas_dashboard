import sys
import json
from lib.file import read_start, read_course, read_progress, read_results, read_course_instance
from lib.lib_date import get_actual_date
from lib.lib_progress import get_overall_progress
from model.ProgressDay import ProgressDay
from model.perspective.Perspectives import Perspectives
from model.perspective.StudentPerspective import StudentPerspective
from model.perspective.StudentPerspectives import StudentPerspectives


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    # course = read_course(instances.course_file_name)
    results = read_results(instances.get_result_file_name(instances.current_instance))

    for student in results.students:
        # print(student.name, student.get_judgement("overall"))
        perspectives = StudentPerspectives()
        for perspective in student.perspectives.values():
            # print(perspective.name, "eind", student.get_judgement(perspective.name), "calc", perspective.progress)
            perspectives.perspectives[perspective.name] = StudentPerspective(perspective.name, student.get_judgement(perspective.name), 0, 0)
            if student.get_judgement(perspective.name) != perspective.progress:
                print(f"GCR2 - Voor {student.name} in perspectief {perspective.name} is eindbeoordeling {student.get_judgement(perspective.name)} inconsistent met berekende voortgang {perspective.progress}")
        perspectives = []
        for perspective in student.perspectives.values():
            perspectives.append(perspective.progress)

        judgement = get_overall_progress(perspectives)
        if student.get_judgement("overall") == judgement == student.progress:
            pass
        else:
            print(f"GCR3 - Voor {student.name} overall is de eindbeoordeling", student.get_judgement("overall"),
                  "inconsistent met de bepaalde beoordeling", judgement,
                  "of de berekende", student.progress, "voortgang")


    # with open(start.results_file_name, 'w') as f:
    #     dict_result = results.to_json([])
    #     json.dump(dict_result, f, indent=2)

    print("GC99 Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
