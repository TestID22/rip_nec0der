#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import upsidedown
import pickledb
import datetime
import config
import datetime
import calendar

welcome = pickledb.load("welcome.json", True)
left = pickledb.load("left.json", True)
rules = pickledb.load("rules.json", True)
welcomedis = pickledb.load("welcomedis.json", True)
ignorelist = pickledb.load("ignore.json", True)

def Ignore(message):
    if str(message.reply_to_message.from_user.id) in ignorelist.getall():
        ignorelist.rem(str(message.reply_to_message.from_user.id))
        return False
    else:
        ignorelist.set(str(message.reply_to_message.from_user.id), "ignore")
        return True

def GetUnixDelta(arg): # pCode now
    minutes = 0
    weeks = 0
    seconds = 0
    days = 0
    pArr = arg.split(" ")
    for j in pArr:
        try:
            if "mo" in j:
                days += ( int(j.split("mo")[0]) * 31)
            elif "s" in j:
                seconds += int(j.split("s")[0])
            elif "y" in j:
                days += ( int(j.split("y")[0]) * 365)
            elif "w" in j:
                weeks += int(j.split("w")[0])
            elif "m" in j:
                minutes += int(j.split("m")[0])
            elif "d" in j:
                days += int(j.split("d")[0])
        except:
            pass # for fix words in messages
    if minutes == 0 and weeks == 0 and seconds == 0 and days == 0:
        days = 367
    future = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes, weeks=weeks, seconds=seconds, days=days)
    return calendar.timegm(future.timetuple())

def CheckWelcome(message):
    if welcomedis.get(str(message.chat.id)) == "disabled":
        return False
    return True

def WelcomeCommand(message):
    if welcomedis.get(str(message.chat.id)) != "disabled":
        welcomedis.set(str(message.chat.id), "disabled")
        return False
    else:
        welcomedis.set(str(message.chat.id), "enabled")
        return True

def Logger(message):
    now = datetime.datetime.now()
    t = now.strftime('%Y-%m-%d %H:%M:%S.%f')
    logtext = "@{}({}) used {} command in {}".format(str(message.from_user.username), message.from_user.id, message.text.encode('utf-8'), str(message.chat.title).encode('utf-8'))
    print(t[:-7] + "] " + logtext)

def CheckAdmin(message, bot):
    administrators = bot.get_chat_administrators(message.chat.id)
    admins_id = []
    for i in range(len(administrators)):
        admins_id.append(administrators[i].user.id)
    if message.from_user.id not in admins_id and message.from_user.id != config.adminID:
        return False
    return True

def ThinkerMSG(message):
    if ignorelist.get(str(message.from_user.id)) != False:
        return
    if len(message.text.split(' ')[0].split('@')) > 1:
        if not message.text.split(' ')[0].split('@')[1].startswith(config.botID.replace('@', '')):
            return False
    Logger(message)
    return True

def fuckWord(str):
    if str == "":
        return "Передайте текст для функции, чтобы текст перевернулся"
    else:
        return upsidedown.transform(str)

def getName(message):
    if message.reply_to_message != None:
        if message.reply_to_message.forward_from != None:
            if message.reply_to_message.forward_from.username != None:
                name = '@' + message.reply_to_message.forward_from.username
            else:
                name = message.reply_to_message.forward_from.first_name
        else:
            if message.reply_to_message.from_user.username != None:
                name = '@' + message.reply_to_message.from_user.username
            else:
                name = message.reply_to_message.from_user.first_name
    else:
        if message.from_user.username != None:
            name = '@' + message.from_user.username
        else:
            name = message.from_user.first_name
    return name


def getID(message):
    id = 0
    if message.reply_to_message != None:
        if message.reply_to_message.forward_from != None:
            id = message.reply_to_message.forward_from.id
        else:
            id = message.reply_to_message.from_user.id
    else:
        id = message.from_user.id
    return id

def getleft(message):
    if left.get(str(message.chat.id)) != False:
        return str(left.get(str(message.chat.id)))
    else:
        if message.left_chat_member != None:
            return 'Прощай, {}'.format(message.left_chat_member.first_name)
        else:
            return 'Прощай, {}'.format(message.from_user.first_name)

def setWelcome(message, rules):
    welcome.set(str(message.chat.id), str(rules))

def getWelcome(message):
    if welcome.get(str(message.chat.id)) != False:
        return str(welcome.get(str(message.chat.id)))
    else:
        if message.new_chat_member != None:
            return 'welcome to the {}, {}'.format(message.chat.title, message.new_chat_member.first_name)
        else:
            return 'welcome to the {}, {}'.format(message.chat.title, message.from_user.first_name)

def sendrnd(message, name, bot):
    if message.reply_to_message != None:
        repl = message.reply_to_message.message_id
    else:
        repl = message.message_id
    bot.send_sticker(message.chat.id, random.choice(bot.get_sticker_set(name).stickers).file_id, reply_to_message_id=repl)

def setRules(message, rulestext):
    rules.set(str(message.chat.id), str(rulestext))

def setleft(message, rules):
    left.set(str(message.chat.id), str(rules))

def getRules(message):
    if rules.get(str(message.chat.id)) != False:
        return rules.get(str(message.chat.id))
    else:
        return 'Правила для данной беседы еще не заданы. Задайте их командой /setrules {правила}'