import datetime
from aiogram import Router, Bot, F
import locale
from aiogram.types import Message, CallbackQuery
from icalendar import Calendar, Event
import database.requests.get as get
import database.requests.add as add
import keyboards.inline as kb

from aiogram.enums import ParseMode

router = Router()


# g = open('grp.ics', 'rb')
# gcal = Calendar.from_ical(g.read())
# for component in gcal.walk():
#     if component.name == "VEVENT":
#         print(component.get('DTSTAMP').dt)
#         print(component.get('SUMMARY'))
#         print(component.get('DTEND').dt, '\n')
#
# g.close()


@router.message(F.text == 'Расписание 📌')
async def schedule(message: Message):
    headman = await get.get_group_headman(message.from_user.id)

    date_start = []
    lessons = []
    date_finish = []

    await message.answer('Вот и ваше расписание подъехало!\nВыбери кнопочками снизу какое расписание хочешь увидеть!', reply_markup=kb.schedule)

@router.callback_query(F.data == 'today')
async def schedule_today(callback: CallbackQuery):
    headman = await get.get_group_headman(callback.from_user.id)

    date_start = []
    lessons = []
    date_finish = []
    locale.setlocale(locale.LC_ALL, '')
    schedule = f'{datetime.datetime.now().strftime("%A %Y/%m/%d").title()} \n'

    try:
        g = open(rf"schedules\{headman}.ics", 'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                DTSTAMP = component.get("DTSTAMP").dt
                SUMMARY = component.get("SUMMARY")
                DTEND = component.get("DTEND").dt
                if DTSTAMP.strftime("%Y-%m-%d") == datetime.datetime.now().strftime("%Y-%m-%d"):
                    date_start.append(DTSTAMP.strftime("%H:%M"))
                    lessons.append(SUMMARY)
                    date_finish.append(DTEND.strftime("%H:%M"))

        for i in range(0 , len(lessons)):
            schedule += f'\n🌅 Начало пары: {date_start[i]} \n' + f'📓 {lessons[i]} \n' + f'🌃 Конец пары: {date_finish[i]} \n'

        if schedule != '':
            await callback.message.answer(schedule,
                                          parse_mode=ParseMode.HTML)
        else:
            await callback.answer('К сожалению или к вашему счастью расписания на завтра нет :(')

    except FileNotFoundError:
        await callback.answer('Расписание ещё не загружено. Обратитесь к старосте.')

    finally:
        g.close()


@router.callback_query(F.data == 'tomorrow')
async def schedule_tomorrow(callback: CallbackQuery):
    headman = await get.get_group_headman(callback.from_user.id)

    date_start = []
    lessons = []
    date_finish = []
    locale.setlocale(locale.LC_ALL, '')
    schedule = f'{(datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%A %Y/%m/%d").title()} \n'
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    try:
        g = open(rf"schedules\{headman}.ics", 'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                DTSTAMP = component.get("DTSTAMP").dt
                SUMMARY = component.get("SUMMARY")
                DTEND = component.get("DTEND").dt

                if DTSTAMP.strftime("%Y-%m-%d") == tomorrow:
                    date_start.append(DTSTAMP.strftime("%H:%M"))
                    lessons.append(SUMMARY)
                    date_finish.append(DTEND.strftime("%H:%M"))

        for i in range(0, len(lessons)):
            schedule += f'\n🌅 Начало пары: {date_start[i]} \n' + f'📓 {lessons[i]} \n' + f'🌃 Конец пары: {date_finish[i]} \n'

        if schedule != '':
            await callback.message.answer(schedule,
                                          parse_mode=ParseMode.HTML)
        else:
            await callback.answer('К сожалению или к вашему счастью расписания на завтра нет :(')

    except FileNotFoundError:
        await callback.answer('Расписание ещё не загружено. Обратитесь к старосте.')

    finally:
        g.close()


@router.callback_query(F.data == 'week')
async def schedule_tomorrow(callback: CallbackQuery):
    headman = await get.get_group_headman(callback.from_user.id)

    schedule = ''
    locale.setlocale(locale.LC_ALL, '')

    try:
        g = open(rf"schedules\{headman}.ics", 'rb')
        gcal = Calendar.from_ical(g.read())
        for i in range(0, 7):
            date_start = []
            lessons = []
            date_finish = []
            day = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            schedule += f'\n\n📌 {(datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%A %Y/%m/%d").title()}\n'
            for component in gcal.walk():
                if component.name == "VEVENT":
                    DTSTAMP = component.get("DTSTAMP").dt
                    SUMMARY = component.get("SUMMARY")
                    DTEND = component.get("DTEND").dt

                    if DTSTAMP.strftime("%Y-%m-%d") == day:
                        date_start.append(DTSTAMP.strftime("%H:%M"))
                        lessons.append(SUMMARY)
                        date_finish.append(DTEND.strftime("%H:%M"))

            for i in range(0, len(lessons)):
                schedule += f'\n🌅 Начало пары: {date_start[i]} \n' + f'📓 {lessons[i]} \n' + f'🌃 Конец пары: {date_finish[i]} \n'

        if schedule != '':

            await callback.message.answer(schedule)
        else:
            await callback.answer('К сожалению или к вашему счастью расписания на неделю нет :(')

    except FileNotFoundError:
        await callback.answer('Расписание ещё не загружено. Обратитесь к старосте.')

    finally:
        g.close()





