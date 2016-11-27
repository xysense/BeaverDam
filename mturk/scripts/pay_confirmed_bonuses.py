from mturk.models import FullVideoTask
from mturk.mturk_api import Server
from beaverdam import settings

mturk = Server(settings.AWS_ID, settings.AWS_KEY, settings.URL_ROOT, settings.MTURK_SANDBOX)


def calc_bonus(task):
    res = mturk.request('GetAssignmentsForHIT', {"HITId":tasks[0].hit_id})
    if res.has_path("GetAssignmentsForHITResult/Assignment") :
        res.store("GetAssignmentsForHITResult/Request/IsValid", "IsValid", bool)
        res.store("GetAssignmentsForHITResult/Assignment/AssignmentId", "AssignmentId")
        res.store("GetAssignmentsForHITResult/Assignment/WorkerId", "WorkerId")
        print("Is valid = " + str(res.IsValid)) 
        print("Assignment id = " + res.AssignmentId)
        print("worker id = " + res.WorkerId)
        task.approve_assignment(res.WorkerId, res.AssignmentId, 'Thanks for completing this - your bonus has been paid as {}'.format(task.calculate_bonus()))

def calc_bonuses(tasks):
    print("{} tasks to process".format(len(tasks)))
    for task in tasks:
        print("Paying id {} fn {}".format(task.video.id, task.video.filename))
        calc_bonus(task)

def mark_as_unpaid(ids):
    tasks = FullVideoTask.objects.filter(video__pk__in = ids)
    for task in tasks:
       task.paid = False
       task.bonus = task.calculate_bonus()
       task.save()
       print("task {} - paid = {}, bonus = {}".format(task.id, task.paid, task.bonus))

#calc_bonuses(tasks)
tasks = FullVideoTask.objects.filter(paid = False, video__verified = True).exclude(hit_id = '')
calc_bonuses(tasks)
#calc_bonuses([1142, 1145, 1146, 1159, 1156, 1155, 1163, 1164, 1621, 2010])
