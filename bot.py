#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import random
import time
import os.path
import BrainFuck as bfi
import wikipediaapi
import psutil
import requests
from time import sleep
from telebot import types
from time import time
from ping3 import ping


from lang import parse_mode as pmode
import tools
import config
from lang import lang

print('Init...')
wikipedia = wikipediaapi.Wikipedia('ru')
currenttime = time()
bot = telebot.TeleBot(config.botToken)
myid = bot.get_me().id
try:
    print("Logged in in GiHhub as " + requests.get("https://api.github.com/user", auth=(config.GITHUBusername, config.GITHUBpassword)).json()["login"])
except:
    print("Can't auth in GitHub.")
    exit(-1)

@bot.inline_handler(lambda query: len(query.query) >= 0)
def query_text(query):
    results = []
    if len(query.query) > 0:
        single_msg = telebot.types.InlineQueryResultArticle(
            id="echo", title="echo " + query.query,
            input_message_content=telebot.types.InputTextMessageContent(
                message_text=query.query)
        )
        results.append(single_msg)
        single_msg = telebot.types.InlineQueryResultArticle(
            id="FuckWord", title="fliptext",
            input_message_content=telebot.types.InputTextMessageContent(
                message_text=tools.fuckWord(query.query))
        )
        results.append(single_msg)
    single_msg = telebot.types.InlineQueryResultArticle(
        id="Shrug", title="¯\_(ツ)_ /¯",
        input_message_content=telebot.types.InputTextMessageContent(
            message_text="¯\_(ツ)_ /¯")
    )
    results.append(single_msg)
    single_msg = telebot.types.InlineQueryResultArticle(
        id="ascii2", title="( ͡° ͜ʖ ͡°)",
        input_message_content=telebot.types.InputTextMessageContent(
            message_text="( ͡° ͜ʖ ͡°)")
    )
    results.append(single_msg)
    single_msg = telebot.types.InlineQueryResultArticle(
        id="ascii3", title="ಠ_ಠ",
        input_message_content=telebot.types.InputTextMessageContent(
            message_text="ಠ_ಠ")
    )
    results.append(single_msg)
    bot.answer_inline_query(query.id, results)


@bot.message_handler(commands=['hmm'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    tools.sendrnd(message, "thonkang", bot)


@bot.message_handler(commands=['f'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    tools.sendrnd(message, "FforRespect", bot)


@bot.message_handler(commands=['g'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    tools.sendrnd(message, random.choice(["ricardo_milos_gay", "Gachimuchi", "Gachigum"]), bot)


@bot.message_handler(commands=['welcome'])
def onstart(message):
    if not tools.ThinkerMSG(message) and message.chat.title == None:
        return
    if not tools.CheckAdmin(message, bot):
        bot.reply_to(message, lang["not_admin"], parse_mode=pmode)
    else:
        if tools.WelcomeCommand(message):
            bot.reply_to(message, lang["enabled"], parse_mode=pmode)
        else:
            bot.reply_to(message, lang["disabled"], parse_mode=pmode)


@bot.message_handler(commands=['start'])
def onstart(message):
    if not tools.ThinkerMSG(message) and message.chat.title != None:
        return
    bot.reply_to(message, lang["on_start"], parse_mode=pmode)


@bot.message_handler(commands=['help'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    res = lang["help_header"] + "\n"
    for h in config.comm:
        res += "/" + h + "\n"
    bot.reply_to(message, res)


@bot.message_handler(commands=['try'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    bot.reply_to(message, random.choice([lang["success"], lang["failed"]]), parse_mode=pmode)


@bot.message_handler(commands=['roulette'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    if message.from_user.username == None:
        name = message.from_user.first_name
    else:
        name = '@' + message.from_user.username
    bot.reply_to(message, lang["roulette_start"].format(name), parse_mode=pmode)
    sleep(2)
    bot.reply_to(message, random.choice([lang["roulette_failed"].format(name), lang["roulette_success"].format(name)]), parse_mode=pmode)


@bot.message_handler(commands=['rate'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    bot.reply_to(message, random.choice(lang["rate_list"]), parse_mode=pmode)


@bot.message_handler(commands=['coin'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    bot.reply_to(message, random.choice(lang["coin_list"]), parse_mode=pmode)


@bot.message_handler(commands=['echo']) # Костыль
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    if message.text == '/echo' or message.text == '/echo{}'.format(config.botID):
        return
    if message.text.startswith('/echo{}'.format(config.botID)):
        if message.reply_to_message != None:
            bot.reply_to(message.reply_to_message, message.text.replace('/echo{} '.format(config.botID), '').replace('/', ''), parse_mode=pmode)
        else:
            bot.send_message(message.chat.id, message.text.replace('/echo{} '.format(config.botID), '').replace('/', ''), parse_mode=pmode)
    elif message.text.startswith('/echo'):
        if message.reply_to_message != None:
            bot.reply_to(message.reply_to_message, message.text.replace('/echo ', '').replace('/', ''), parse_mode=pmode)
        else:
            bot.send_message(message.chat.id, message.text.replace('/echo ', '').replace('/', ''), parse_mode=pmode)


@bot.message_handler(commands=['acho']) # Такой же костыль как и echo
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    if message.text == '/acho' or message.text == '/acho{}'.format(config.botID):
        return
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    if message.text.startswith('/acho{}'.format(config.botID)):
        if message.reply_to_message != None:
            bot.reply_to(message.reply_to_message, message.text.replace('/acho{} '.format(config.botID), ''), parse_mode=pmode)
        else:
            bot.send_message(message.chat.id, message.text.replace('/acho{} '.format(config.botID), ''), parse_mode=pmode)
    elif message.text.startswith('/acho'):
        if message.reply_to_message != None:
            bot.reply_to(message.reply_to_message, message.text.replace('/acho ', ''), parse_mode=pmode)
        else:
            bot.send_message(message.chat.id, message.text.replace('/acho ', ''), parse_mode=pmode)


@bot.message_handler(commands=['random'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    if message.text.startswith('/random{}'.format(config.botID)):
        std = message.text.replace('/random{} '.format(config.botID), '')
    else:
        std = message.text.replace('/random ', '')
    std = std.replace(' ', '')
    n = std
    if n.isdigit():
        n = int(n)
        bot.send_message(message.chat.id, lang["random_header"].format(random.randint(1, n)), parse_mode=pmode)
    else:
        bot.send_message(message.chat.id, lang["random_header"].format(random.randint(1, 999999999)), parse_mode=pmode)


@bot.message_handler(content_types=['new_chat_members'])
def qq(message):
    if not tools.CheckWelcome(message):
        return
    if message.new_chat_member.username == config.botID.replace("@", ''):
        bot.reply_to(message, lang["added_to_chat"].format(config.botID), parse_mode=pmode)
        return
    bot.reply_to(message, tools.getWelcome(message), parse_mode=pmode)


@bot.message_handler(content_types=['left_chat_member'])
def goodbye(message):
    if not tools.CheckWelcome(message):
        return
    bot.reply_to(message, tools.getleft(message), parse_mode=pmode)


@bot.message_handler(commands=['passgen'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    password = ''
    random_password = password.join(
        [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890') for i in range(12)])
    bot.send_message(message.chat.id, lang["passgen_header"].format(random_password), parse_mode=pmode)


@bot.message_handler(commands=['id'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    bot.reply_to(message, lang["id"].format(tools.getName(message), str(tools.getID(message))), parse_mode=pmode)


@bot.message_handler(commands=['chatid'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    if message.chat.title != None:
        bot.reply_to(message, lang["chatid_chat"].format(message.chat.title, message.chat.id), parse_mode=pmode)
    else:
        bot.reply_to(message, lang["chatid_pm"].format(message.chat.id), parse_mode=pmode)


@bot.message_handler(commands=['status'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    uptime = time() - currenttime
    uptimesec = round(uptime % 60)
    uptimeday = round(uptime // 86400)
    uptimehour = round((uptime % 86400) // 3600)
    uptimemin = round(((uptime % 86400) % 3600) // 60)
    uptimemonth = round(uptime // 2630000)
    uptimeyear = round(uptime // 31500000)
    answerUptime = ""
    if uptimeyear != 0:
        answerUptime += lang["uptime_year"].format(uptimeyear)
    if uptimemonth != 0:
        answerUptime += lang["uptime_month"].format(uptimemonth)
    if uptimeday != 0:
        answerUptime += lang["uptime_day"].format(uptimeday)
    if uptimehour != 0:
        answerUptime += lang["uptime_hour"].format(uptimehour)
    if uptimemin != 0:
        answerUptime += lang["uptime_min"].format(uptimemin)
    if uptimesec != 0:
        answerUptime += lang["uptime_sec"].format(uptimesec)
    ram = str(psutil.virtual_memory()).split('percent=')[1].split(',')[0]
    bot.reply_to(message, lang["status_text"].format(psutil.cpu_percent(), ram, answerUptime), parse_mode=pmode)


@bot.message_handler(commands=['weather'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    if message.text == "/weather" or message.text == '/weather{}'.format(config.botID):
        return
    if message.text.startswith('/weather{}'.format(config.botID)):
        std = message.text.replace('/weather{} '.format(config.botID), '')
    elif message.text.startswith('/weather'):
        std = message.text.replace('/weather ', '')
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?q={0}&appid=02041d0ae314c77bfed5ab5fcd9d5a2f'.format(std))
    json_data = r.json()
    try:
        temp = float(json_data['main']['temp']) - 273.15
        wind = json_data['wind']['speed']
        humidity = json_data['main']['humidity']
        city = json_data['name']
        temp = int(temp)
        temp = round(temp)
        weather = lang["weather_text"].format(str(city), str(temp), str(wind), str(humidity))
        bot.reply_to(message, weather, parse_mode=pmode)
    except KeyError:
        bot.reply_to(message, lang["weather_error"], parse_mode=pmode)


@bot.message_handler(commands=['answer'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    if message.text == "/answer" or message.text == '/answer{}'.format(config.botID):
        return
    text = ''
    if message.text.startswith('/answer{}'.format(config.botID)):
        text = message.text.replace('/answer{} '.format(config.botID), '')
    elif message.text.startswith('/answer'):
        text = message.text.replace('/answer ', '')
    try:
        bot.send_chat_action(message.chat.id, action='typing')
        mathjs = requests.get("http://api.mathjs.org/v4/?expr={}".format(text).replace("+", "%2B")).content
        if mathjs.isdigit():
            bot.reply_to(message, '`{} = {}`'.format(text, str(mathjs, encoding='utf8')), parse_mode=pmode)
        else:

            ssilka = 'https://api.wolframalpha.com/v1/result?i={}%3F&appid='.format(text) + config.WolframToken
            answer = requests.get(ssilka).content
            answer = str(answer, encoding="utf-8")
            if answer == 'Wolfram|Alpha did not understand your input':
                answer = lang["answer_dont_understand"]
            elif answer == 'No short answer available':
                answer = lang["answer_no_short_answers"]
            bot.reply_to(message, '`{}`'.format(answer), parse_mode=pmode)
    except Exception as e:
        bot.reply_to(message, lang["error_to_user"], parse_mode=pmode)
        bot.send_message(config.logchannel, lang["error_to_log"].format(str(e)), parse_mode=pmode)


@bot.message_handler(commands=['wiki'])
def onstart(message):
    if not tools.ThinkerMSG(message) or message.text == '/wiki' or message.text == '/wiki{}'.format(config.botID):
        return
    bot.send_chat_action(message.chat.id, action='typing')
    std = message.text.replace('/wiki{}'.format(config.botID), '')
    std = std.replace('/wiki', '')
    try:
        p = wikipedia.page(std)
        answer = lang["wiki_answer"].format(p.title, p.summary[0:200], p.fullurl)
    except Exception as e:
        if str(e) == 'fullurl':
            answer = lang["wiki_not_found"]
        else:
            try:
                if p.fullurl == None:
                    answer = lang["wiki_not_found"]
                else:
                    answer = lang["wiki_answer"].format(p.title, p.text, p.fullurl)
            except:
                answer = lang["wiki_not_found"]
    bot.reply_to(message, answer, parse_mode=pmode)


@bot.message_handler(commands=['choice'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    if message.text == "/choice" or message.text == '/choice{}'.format(config.botID):
        return
    std = ''
    if message.text.startswith('/choice{}'.format(config.botID)):
        std = message.text.replace('/choice{} '.format(config.botID), '')
    elif message.text.startswith('/choice'):
        std = message.text.replace('/choice ', '')
    try:
        choosearr = std.split(' или ')
        chooseru = random.choice(choosearr)
        if choosearr[0] == choosearr[1]:
            bot.reply_to(message, lang["choice_error_same_args"], parse_mode=pmode)
        else:
            res = lang["choice_answer"].format(chooseru)
            bot.reply_to(message, res, parse_mode=pmode)
    except IndexError:
        bot.reply_to(message, lang["choice_error_arguments"], parse_mode=pmode)


@bot.message_handler(commands=['rules'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    bot.reply_to(message, tools.getRules(message), parse_mode=pmode)


@bot.message_handler(commands=['setleft'])
def onstart(message):
    if not tools.ThinkerMSG(message) or message.chat.title == None:
        return
    if not tools.CheckAdmin(message, bot):
        bot.reply_to(message, lang["not_admin"], parse_mode=pmode)
    else:
        try:
            std = ''
            if message.text.startswith('/setleft{}'.format(config.botID)):
                std = message.text.replace('/setleft{} '.format(config.botID), '').replace('/setleft{}',format(config.botID), "")
            elif message.text.startswith('/setleft'):
                std = message.text.replace('/setleft ', '').replace("/setleft", "")
            tools.setleft(message, std)
            bot.reply_to(message, lang["setleft_success"], parse_mode=pmode)
        except Exception as e:
            bot.reply_to(message, lang["error_to_user"], parse_mode=pmode)
            bot.send_message(config.logchannel, lang["error_to_log"].format(str(e)), parse_mode=pmode)


@bot.message_handler(commands=['setwelcome'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    if not tools.CheckAdmin(message, bot):
        bot.reply_to(message, lang["not_admin"], parse_mode=pmode)
    else:
        try:
            std = ''
            if message.text.startswith('/setwelcome{}'.format(config.botID)):
                std = message.text.replace('/setwelcome{} '.format(config.botID), '').replace('/setwelcome{}',format(config.botID), "")
            elif message.text.startswith('/setwelcome'):
                std = message.text.replace('/setwelcome ', '').replace("/setwelcome", "")
            tools.setWelcome(message, std)
            bot.reply_to(message, lang["setwelcome_success"], parse_mode=pmode)
        except Exception as e:
            bot.reply_to(message, lang["error_to_user"], parse_mode=pmode)
            bot.send_message(config.logchannel, lang["error_to_log"].format(str(e)), parse_mode=pmode)


@bot.message_handler(commands=['setrules'])
def onstart(message):
    if not tools.ThinkerMSG(message) or message.chat.title == None:
        return
    if not tools.CheckAdmin(message, bot):
        bot.reply_to(message, lang["not_admin"], parse_mode=pmode)
    else:
        try:
            std = ''
            std = message.text.replace('/setrules{} '.format(config.botID), '').replace('/setrules{}',format(config.botID), "")
            std = std.replace('/setrules ', '').replace("/setrules", "")
            tools.setRules(message, std)
            bot.reply_to(message, lang["setrules_success"], parse_mode=pmode)
        except Exception as e:
            bot.reply_to(message, lang["error_to_user"], parse_mode=pmode)
            bot.send_message(config.logchannel, lang["error_to_log"].format(str(e)), parse_mode=pmode)


@bot.message_handler(commands=['del'])
def onkick(message):
    if not tools.ThinkerMSG(message):
        return
    if message.reply_to_message == None:
        bot.reply_to(message, lang["del_error_arguments"], parse_mode=pmode)
        return
    if not tools.CheckAdmin(message, bot):
        bot.reply_to(message, lang["not_admin"], parse_mode=pmode)
    else:
        bot.delete_message(message.chat.id, message.reply_to_message.message_id)


@bot.message_handler(commands=['bfi'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    std = message.text.replace('/bfi{} '.format(config.botID), '')
    std = std.replace('/bfi', '')
    try:
        bot.reply_to(message, lang["brainfuck_imp_res"].format(std, bfi.run(std)), parse_mode=pmode)
    except:
        bot.reply_to(message, lang["brainfuck_imp_res"].format(std, 'Error occured'), parse_mode=pmode)


@bot.message_handler(commands=['bfe'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    std = message.text.replace('/bfe{}'.format(config.botID), '')
    std = std.replace('/bfe ', '')
    try:
        bot.reply_to(message, lang["brainfuck_enc_res"].format(std, bfi.encode(std)), parse_mode=pmode)
    except:
        bot.reply_to(message, lang["brainfuck_enc_res"].format(std, 'Error occured'), parse_mode=pmode)


@bot.message_handler(commands=['bug'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    if message.text == '/bug' or message.text == '/bug{}'.format(config.botID):
        return
    std = ''
    if message.text.startswith('/bug{}'.format(config.botID)):
        std = message.text.replace('/bug{} '.format(config.botID), '')
    elif message.text.startswith('/bug'):
        std = message.text.replace('/bug ', '')
    if std == "":
        return
    bot.send_message(config.logchannel, lang["bug_log"].format(message.from_user.username, std), parse_mode=pmode)
    bot.reply_to(message, lang["bug_sent"], parse_mode=pmode)


@bot.message_handler(commands=['ping'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    a = message.text.split(" ")
    if len(a) == 1:
        bot.send_message(message.chat.id, lang["pong"], parse_mode=pmode)
        return
    try:
        p = ping(a[1])
        sec = p * 1000
        sec = round(sec)
        bot.reply_to(message, lang["ping_answer_with_host"].format(a[1], str(sec)), parse_mode=pmode)
    except:
        bot.reply_to(message, lang["ping_timed_out"], parse_mode=pmode)


@bot.message_handler(commands=['pong'])
def onstart(message):
    if not tools.ThinkerMSG(message):
        return
    bot.send_message(message.chat.id, lang["ping"], parse_mode=pmode)

@bot.message_handler(commands=['kick'])
def mute(message):
    if not tools.ThinkerMSG(message):
        return
    if not tools.CheckAdmin(message, bot):
        bot.reply_to(message, lang["not_admin"], parse_mode=pmode)
    else:
        if message.reply_to_message == None:
            bot.reply_to(message, lang["kick_error_args"], parse_mode=pmode)
            return
        kb = types.InlineKeyboardMarkup()
        callback_data = "kick_{}_{}".format(str(message.reply_to_message.from_user.id), message.from_user.id)
        decline = "declineKick_{}_{}".format(str(message.reply_to_message.from_user.id), message.from_user.id)
        kb.add(types.InlineKeyboardButton(text=lang["kick_accept_button_text"], callback_data=callback_data))
        kb.add(types.InlineKeyboardButton(text=lang["kick_decline_button_text"], callback_data=decline))
        bot.reply_to(message, lang["kick_accept_text"].format(tools.getName(message)), parse_mode=pmode, reply_markup=kb)

@bot.message_handler(commands=['ban'])
def mute(message):
    if not tools.ThinkerMSG(message):
        return
    if not tools.CheckAdmin(message, bot):
        bot.reply_to(message, lang["not_admin"], parse_mode=pmode)
    else:
        if message.reply_to_message == None:
            bot.reply_to(message, lang["ban_error_args"], parse_mode=pmode)
            return
        kb = types.InlineKeyboardMarkup()
        callback_data = "ban_{}_{}".format(str(message.reply_to_message.from_user.id), message.from_user.id)
        decline = "declineBan_{}_{}".format(str(message.reply_to_message.from_user.id), message.from_user.id)
        kb.add(types.InlineKeyboardButton(text=lang["ban_accept_button_text"], callback_data=callback_data))
        kb.add(types.InlineKeyboardButton(text=lang["ban_decline_button_text"], callback_data=decline))
        bot.reply_to(message, lang["ban_accept_text"].format(tools.getName(message)), parse_mode=pmode, reply_markup=kb)

@bot.message_handler(commands=['unmute'])
def mute(message):
    if not tools.ThinkerMSG(message):
        return
    if not tools.CheckAdmin(message, bot):
        bot.reply_to(message, lang["not_admin"], parse_mode=pmode)
    else:
        if message.reply_to_message == None:
            bot.reply_to(message, lang["unmute_error_args"], parse_mode=pmode)
            return
        kb = types.InlineKeyboardMarkup()
        callback_data = "unmute_{}_{}".format(str(message.reply_to_message.from_user.id), message.from_user.id)
        decline = "declineUnmute_{}_{}".format(str(message.reply_to_message.from_user.id), message.from_user.id)
        kb.add(types.InlineKeyboardButton(text=lang["unmute_accept_button_text"], callback_data=callback_data))
        kb.add(types.InlineKeyboardButton(text=lang["unmute_decline_button_text"], callback_data=decline))
        bot.reply_to(message, lang["unmute_accept_text"].format(tools.getName(message)), parse_mode=pmode, reply_markup=kb)

@bot.message_handler(commands=['mute'])
def mute(message):
    if not tools.ThinkerMSG(message):
        return
    if not tools.CheckAdmin(message, bot):
        bot.reply_to(message, lang["not_admin"], parse_mode=pmode)
    else:
        if message.reply_to_message == None:
            bot.reply_to(message, lang["mute_error_args"], parse_mode=pmode)
            return
        if message.reply_to_message.from_user.id == message.from_user.id:
            bot.reply_to(message, lang["mute_error_same_users"], parse_mode=pmode)
            return
        if message.reply_to_message.from_user.id == myid:
            bot.reply_to(message, lang["mute_error_bot"], parse_mode=pmode)
            return
        kb = types.InlineKeyboardMarkup()
        try:
            callback_data = "mute_{}_{}_{}".format(
                str(message.reply_to_message.from_user.id), message.from_user.id,
                      tools.GetUnixDelta(message.text.split(" ", maxsplit=1)[1]))
            decline = "declineBan_{}_{}_{}".format(
                str(message.reply_to_message.from_user.id), message.from_user.id,
                      tools.GetUnixDelta(message.text.split(" ", maxsplit=1)[1]))
        except:
            bot.reply_to(message, lang["mute_error_parsing"], parse_mode=pmode)
            return
        kb.add(types.InlineKeyboardButton(text=lang["mute_accept_button_text"], callback_data=callback_data))
        kb.add(types.InlineKeyboardButton(text=lang["mute_decline_button_text"], callback_data=decline))
        bot.reply_to(message, lang["mute_accept_text"].format(tools.getName(message)), parse_mode=pmode, reply_markup=kb)

@bot.message_handler(commands=['kickme'])
def mute(message):
    if not tools.ThinkerMSG(message):
        return
    kb = types.InlineKeyboardMarkup()
    callback_data = "kick_{}_{}".format(message.from_user.id, message.from_user.id)
    decline = "declineKick_{}_{}".format(message.from_user.id, message.from_user.id)
    kb.add(types.InlineKeyboardButton(text=lang["kickme_accept_button_text"], callback_data=callback_data))
    kb.add(types.InlineKeyboardButton(text=lang["kickme_decline_button_text"], callback_data=decline))
    bot.reply_to(message, lang["kickme_accept_text"].format(tools.getName(message)), parse_mode=pmode, reply_markup=kb)

@bot.message_handler(commands=['banme'])
def mute(message):
    if not tools.ThinkerMSG(message):
        return
    kb = types.InlineKeyboardMarkup()
    callback_data = "ban_{}_{}".format(message.from_user.id, message.from_user.id)
    decline = "declineBan_{}_{}".format(message.from_user.id, message.from_user.id)
    kb.add(types.InlineKeyboardButton(text=lang["banme_accept_button_text"], callback_data=callback_data))
    kb.add(types.InlineKeyboardButton(text=lang["banme_decline_button_text"], callback_data=decline))
    bot.reply_to(message, lang["banme_accept_text"].format(tools.getName(message)), parse_mode=pmode, reply_markup=kb)

@bot.message_handler(commands=['muteme'])
def mute(message):
    if not tools.ThinkerMSG(message):
        return
    kb = types.InlineKeyboardMarkup()
    try:
        callback_data = "mute_{}_{}_{}".format(
            message.from_user.id, message.from_user.id,
                  tools.GetUnixDelta(message.text.split(" ", maxsplit=1)[1]))
        decline = "declineBan_{}_{}_{}".format(
            message.from_user.id, message.from_user.id,
                  tools.GetUnixDelta(message.text.split(" ", maxsplit=1)[1]))
    except:
        bot.reply_to(message, lang["muteme_error_parsing"], parse_mode=pmode)
        return
    kb.add(types.InlineKeyboardButton(text=lang["muteme_accept_button_text"], callback_data=callback_data))
    kb.add(types.InlineKeyboardButton(text=lang["muteme_decline_button_text"], callback_data=decline))
    bot.reply_to(message, lang["muteme_accept_text"].format(tools.getName(message)), parse_mode=pmode, reply_markup=kb)

@bot.message_handler(commands=['ignore'])
def ignore(message):
    if not tools.ThinkerMSG(message) or message.from_user.id != config.adminID:
        return
    if message.reply_to_message == None:
        return
    if(tools.Ignore(message)):
        bot.reply_to(message, lang["ignore_added"], parse_mode=pmode)
    else:
        bot.reply_to(message, lang["ignore_removed"], parse_mode=pmode)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        pArg = call.data.split("_")
        command = pArg[0]
        who = pArg[1]
        #delta = pArg[2]
        #adminid = pArg[3]
        adminid = pArg[2]
        delta = 0
        try:
            delta = pArg[3]
        except:
            pass
        if call.from_user.id != int(adminid):
            return
        #part 1
        if command == "delcineUnmute":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang["unmute_declined_text"], parse_mode=pmode)
        elif command == "declineMute":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang["mute_declined_text"], parse_mode=pmode)
        elif command == "declineBan":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang["ban_declined_text"], parse_mode=pmode)
        elif command == "declineKick":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang["kick_declined_text"], parse_mode=pmode)

        #part 2
        elif command == "mute":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang["mute_accepted"], parse_mode=pmode)
            bot.restrict_chat_member(call.message.chat.id, int(who), until_date=delta, can_send_messages=False)
        elif command == "unmute":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang["unmute_accepted"], parse_mode=pmode)
            bot.restrict_chat_member(call.message.chat.id, int(who), can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        elif command == "ban":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang["unmute_accepted"], parse_mode=pmode)
            bot.kick_chat_member(call.message.chat.id, int(who))
        elif command == "kick":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang["kick_accepted"], parse_mode=pmode)
            bot.kick_chat_member(call.message.chat.id, int(who))
            bot.restrict_chat_member(call.message.chat.id, int(who), can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)

@bot.message_handler(commands=['ghrepoinfo'])
def gh(message):
    if not tools.ThinkerMSG(message):
        return
    bot.send_chat_action(message.chat.id, 'typing')
    std = message.text.replace('/ghrepoinfo{} '.format(config.botID), '')
    std = std.replace('/ghrepoinfo ', '').replace("/ghrepoinfo", '').replace("/ghrepoinfo{}".format(config.botID), '')
    pArr = std.split("/", maxsplit=1)
    if len(pArr) == 1:
        bot.reply_to(message, "Пожалуйста укажите создателя репозитория через / к примеру github/VisualStudio", parse_mode=pmode)
        return
    r = requests.get('https://api.github.com/repos/{}/{}'.format(pArr[0], pArr[1]), auth=(config.GITHUBusername, config.GITHUBpassword), headers={ "Content-Type": "application/json" })
    try:
        if not r.ok or "message" in r.json():
            bot.reply_to(message, "Указан неверный репозиторий.", parse_mode=pmode)
            return
    except:
        pass
    repoItem = r.json()
    name = repoItem["name"]
    owner = repoItem["owner"]["login"]
    forks_count = repoItem["forks_count"]
    stars = repoItem["stargazers_count"]
    upd = repoItem["updated_at"]
    lang = repoItem["language"]
    isfork = repoItem["fork"]
    desc = repoItem["description"]
    answer = "Name - `{}`\nOwner - `{}`\nIs fork - `{}`\nDescription - `{}`\nForks - `{}`\nStars - `{}`\nLanguage - `{}`\nLatest update - `{}`"
    bot.reply_to(message, answer.format(name, owner, str(isfork), desc, str(forks_count), str(stars), lang, upd), parse_mode=pmode)

@bot.message_handler(commands=['csgo'])
def CsGo(message):
    if not tools.ThinkerMSG(message):
        return
    bot.reply_to(message, str(requests.get("https://raw.githubusercontent.com/SteamDatabase/GameTracking-CSGO/master/csgo/steam.inf").content, encoding='utf-8'))

print('skipping...')
bot.skip_pending = True
print('Sending message')
bot.send_message(config.logchannel, lang["log_rebooted_message"])
print('Started!!')
sleep(2)
os.system("cls")
os.system("title Telegram bot by @es3n1n loaded.")

try:
    bot.polling(none_stop=True, timeout=60)
except Exception as e:
    bot.send_message(config.logchannel, lang["error_to_log"].format(str(e)), parse_mode=pmode)
    print(lang["error_to_log"].format(str(e)))
    bot.stop_bot()
    import os
    os.system("py bot.py")
    exit(-1)
