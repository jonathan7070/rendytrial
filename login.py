from linepy import *
from akad.ttypes import OpType, Message, TalkException
from threading import Thread
from data import commands
import os, livejson, traceback, time, sys

fileName = os.path.splitext(os.path.basename(__file__))[0]
db = livejson.File("token/%s.json" % fileName)
if ":" in db['token']:app = "ANDROIDLITE\t2.11.1\tAndroid OS\t5.1.1"
else:app = "DESKTOPWIN\t5.24.1\tWindows\t10"
if db['token'] != "":
    client = LINE(idOrAuthToken=db["token"], appName=app)
else:
    try:client = LINE(db["mail"],db["pass"],certificate='{}.crt'.format(db["mail"]),appName=app);db['token'] = client.authToken
    except:traceback.print_exc()
OT = OpType
uid = client.profile.mid
poll = OEPoll(client)
good = commands(fileName, client, app, uid)
print("LOGIN SUCCESS")

def main_loop(op):
    if op.type == OT.RECEIVE_MESSAGE:good.receive_message(op)
    elif op.type == OT.NOTIFIED_KICKOUT_FROM_GROUP or op.type == 133:good.notif_kick_from_group(op)
    elif op.type == OT.NOTIFIED_INVITE_INTO_GROUP or op.type == 124:good.notif_invite_into_group(op)
    elif op.type == OT.NOTIFIED_CANCEL_INVITATION_GROUP or op.type == 126:good.notif_cancel_invite_group(op)
    elif op.type == OT.NOTIFIED_UPDATE_GROUP or op.type == 122:good.notif_update_group(op)
    elif op.type == OT.NOTIFIED_ACCEPT_GROUP_INVITATION or op.type == 130:good.notif_accept_group_invite(op)
    elif op.type == OT.ACCEPT_GROUP_INVITATION or op.type == 129:good.accept_group_invite(op)
    elif op.type == OT.NOTIFIED_LEAVE_GROUP or op.type == 128:good.notif_leave_group(op)
    elif op.type == OT.END_OF_OPERATION:pass

while 1:
    try:
        ops = client.poll.fetchOperations(client.revision, 50)
        for op in ops:
            client.revision = max(client.revision, op.revision)
            t1 = Thread(target=main_loop(op,))
            t1.start()
            t1.join()
    except Exception as e:
        e = traceback.format_exc()
        if "EOFError" in e:pass
        elif "ShouldSyncException" in e or "LOG_OUT" in e:python3 = sys.executable;os.execl(python3, python3, *sys.argv)
        else:traceback.print_exc()
