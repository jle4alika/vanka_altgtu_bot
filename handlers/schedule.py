import datetime
import os
import time

from playwright.async_api import async_playwright
import asyncio

from aiogram import Router, Bot, F
import locale
from aiogram.types import Message, CallbackQuery
from icalendar import Calendar, Event
import database.requests.get as get
import database.requests.add as add
import keyboards.inline as kb
from aiogram.filters.command import Command
# from xvfbwrapper import Xvfb
from aiogram.enums import ParseMode
from bs4 import BeautifulSoup

from xvfbwrapper import Xvfb

# create fake X server

vdisplay = Xvfb()
vdisplay.start()


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
    await message.answer('Здравствуйте! В этом разделе вы найдете актуальное расписание ваших занятий. Пожалуйста, обратите внимание на время начала и окончания уроков, а также на аудитории.', reply_markup=kb.schedule)


@router.message(F.text.lower() == 'расписание')
async def schedule(message: Message):
    await message.answer('Здравствуйте! В этом разделе вы найдете актуальное расписание ваших занятий. Пожалуйста, обратите внимание на время начала и окончания уроков, а также на аудитории.', reply_markup=kb.schedule)


@router.callback_query(F.data == 'today')
async def schedule_today(callback: CallbackQuery):
    title = await get.get_group_title(callback.from_user.id)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://www.altstu.ru/m/s/')
        await page.get_by_placeholder('Группа').fill(f'{title}')
        await page.keyboard.press('Enter')

        await asyncio.sleep(1)

        response = await page.content()

        soup = BeautifulSoup(response, "lxml")
        # print(soup)
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        # locale.setlocale(locale.LC_ALL, 'ru_RU')
        # schedule = f'{datetime.datetime.now().strftime("%Y/%m/%d %A").title()}'
        schedule = datetime.datetime.now().strftime("%d.%m.%y %A").title()
        schedule = datetime.datetime.strptime(schedule, "%d.%m.%y %A")
        dates = soup.find_all('div', class_='block-index')
        # print(dates)

        for date in dates:
            data = str(date.find('h2').text)
            print(data)
            data = datetime.datetime.strptime(data, "%d.%m.%y %A")

            # print(data.__class__, data)
            # print(schedule.__class__, schedule)
            # print(data == schedule)

            if data == schedule:
                print('found schedule')
                xz = date.find_all('div', class_='list-group-item')
                text = f'📌 {datetime.datetime.now().strftime("%d.%m.%y %A").title()}\n\n'
                for item in xz:
                    date_start = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[0]
                    # print(" ".join(item.text.split()).split(' ', 1)[1])
                    date_finish = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[1]
                    lesson = f'{" ".join(item.text.split()).split(" ", 1)[1]}'
                    # print(f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n')
                    text += f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n'
                await callback.message.answer(text)
        await browser.close()
        


    # title = await get.get_group_title(callback.from_user.id)
    # url = 'https://www.altstu.ru/m/s/'
    # service = Service(executable_path=ChromeDriverManager().install())
    # options = ChromeOptions()
    #
    # options.add_argument("--no-sandbox")
    # options.headless = True
    # options.add_experimental_option(
    #     "prefs", {
    #         # block image loading
    #         "profile.managed_default_content_settings.images": 2,
    #     }
    # )
    #
    # browser = webdriver.Chrome(service=service, options=options)
    #
    # browser.get(url=url)
    #
    # # Get the full page source
    # response = browser.page_source
    #
    #
    # text = browser.find_element(by='id', value='schedule_input')
    # text.send_keys(f'{title}', Keys.ENTER)
    #
    # time.sleep(1)
    #
    # for handle in browser.window_handles:
    #     browser.switch_to.window(handle)
    #
    # response = browser.page_source
    # browser.quit()
    # soup = BeautifulSoup(response, "lxml")
    # # print(soup)
    #
    # locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    # # schedule = f'{datetime.datetime.now().strftime("%Y/%m/%d %A").title()}'
    # schedule = datetime.datetime.now().strftime("%d.%m.%y %A").title()
    # schedule = datetime.datetime.strptime(schedule, "%d.%m.%y %A")
    # dates = soup.find_all('div', class_='block-index')
    # # print(dates)
    #
    # for date in dates:
    #     data = str(date.find('h2').text)
    #     data = datetime.datetime.strptime(data, "%d.%m.%y %A")
    #
    #     # print(data.__class__, data)
    #     # print(schedule.__class__, schedule)
    #     # print(data == schedule)
    #
    #     if data == schedule:
    #         print('found schedule')
    #         xz = date.find_all('div', class_='list-group-item')
    #         text = f'📌 {datetime.datetime.now().strftime("%d.%m.%y %A").title()}\n\n'
    #         for item in xz:
    #             date_start = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[0]
    #             # print(" ".join(item.text.split()).split(' ', 1)[1])
    #             date_finish = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[1]
    #             lesson = f'{" ".join(item.text.split()).split(" ", 1)[1]}'
    #             # print(f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n')
    #             text += f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n'
    #         await callback.message.answer(text)

    # headman = await get.get_group_headman(callback.from_user.id)
    #
    # date_start = []
    # lessons = []
    # date_finish = []
    # locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    # schedule = f'{datetime.datetime.now().strftime("%A %Y/%m/%d").title()} \n'
    #
    # try:
    #     g = open(rf"schedules\{headman}.ics", 'rb')
    #     gcal = Calendar.from_ical(g.read())
    #     for component in gcal.walk():
    #         if component.name == "VEVENT":
    #             DTSTAMP = component.get("DTSTAMP").dt
    #             SUMMARY = component.get("SUMMARY")
    #             DTEND = component.get("DTEND").dt
    #             if DTSTAMP.strftime("%Y-%m-%d") == datetime.datetime.now().strftime("%Y-%m-%d"):
    #                 date_start.append(DTSTAMP.strftime("%H:%M"))
    #                 lessons.append(SUMMARY)
    #                 date_finish.append(DTEND.strftime("%H:%M"))
    #
    #     for i in range(0 , len(lessons)):
    #         schedule += f'\n🌅 Начало пары: {date_start[i]} \n' + f'📓 {lessons[i]} \n' + f'🌃 Конец пары: {date_finish[i]} \n'
    #
    #     if schedule != '':
    #         await callback.message.answer(schedule,
    #                                       parse_mode=ParseMode.HTML)
    #     else:
    #         await callback.answer('К сожалению или к вашему счастью расписания на сегодня нет')
    #
    # except FileNotFoundError:
    #     await callback.answer('Расписание ещё не загружено. Обратитесь к старосте.')
    #
    # finally:
    #     if os.path.exists(rf"schedules\{headman}.ics"):
    #         g.close()


@router.callback_query(F.data == 'tomorrow')
async def schedule_tomorrow(callback: CallbackQuery):
    title = await get.get_group_title(callback.from_user.id)
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome', headless=True)
        page = await browser.new_page()
        await page.goto('https://www.altstu.ru/m/s/')
        await page.get_by_placeholder('Группа').fill(f'{title}')
        await page.keyboard.press('Enter')

        await asyncio.sleep(1)

        response = await page.content()
        soup = BeautifulSoup(response, "lxml")
        # print(soup)

        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        # schedule = f'{datetime.datetime.now().strftime("%Y/%m/%d %A").title()}'
        schedule = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d.%m.%y %A").title()
        schedule = datetime.datetime.strptime(schedule, "%d.%m.%y %A")
        dates = soup.find_all('div', class_='block-index')
        # print(dates)

        for date in dates:
            data = str(date.find('h2').text)
            data = datetime.datetime.strptime(data, "%d.%m.%y %A")

            # print(data.__class__, data)
            # print(schedule.__class__, schedule)
            # print(data == schedule)

            if data == schedule:
                print('found schedule')
                xz = date.find_all('div', class_='list-group-item')
                text = f'📌 {(datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d.%m.%y %A").title()}\n\n'
                for item in xz:
                    date_start = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[0]
                    # print(" ".join(item.text.split()).split(' ', 1)[1])
                    date_finish = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[1]
                    lesson = f'{" ".join(item.text.split()).split(" ", 1)[1]}'
                    # print(f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n')
                    text += f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n'
                await callback.message.answer(text)


    # headman = await get.get_group_headman(callback.from_user.id)
    #
    # date_start = []
    # lessons = []
    # date_finish = []
    # locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    # schedule = f'{(datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%A %Y/%m/%d").title()} \n'
    # tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    # try:
    #     g = open(rf"schedules\{headman}.ics", 'rb')
    #     gcal = Calendar.from_ical(g.read())
    #     for component in gcal.walk():
    #         if component.name == "VEVENT":
    #             DTSTAMP = component.get("DTSTAMP").dt
    #             SUMMARY = component.get("SUMMARY")
    #             DTEND = component.get("DTEND").dt
    #
    #             if DTSTAMP.strftime("%Y-%m-%d") == tomorrow:
    #                 date_start.append(DTSTAMP.strftime("%H:%M"))
    #                 lessons.append(SUMMARY)
    #                 date_finish.append(DTEND.strftime("%H:%M"))
    #
    #     for i in range(0, len(lessons)):
    #         schedule += f'\n🌅 Начало пары: {date_start[i]} \n' + f'📓 {lessons[i]} \n' + f'🌃 Конец пары: {date_finish[i]} \n'
    #
    #     if schedule != '':
    #         await callback.message.answer(schedule,
    #                                       parse_mode=ParseMode.HTML)
    #     else:
    #         await callback.answer('К сожалению или к вашему счастью расписания на завтра нет')
    #
    # except FileNotFoundError:
    #     await callback.answer('Расписание ещё не загружено. Обратитесь к старосте.')
    #
    # finally:
    #     if os.path.exists(rf"schedules\{headman}.ics"):
    #         g.close()


@router.callback_query(F.data == 'week')
async def schedule_tomorrow(callback: CallbackQuery):
    title = await get.get_group_title(callback.from_user.id)
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome', headless=True)
        page = await browser.new_page()
        await page.goto('https://www.altstu.ru/m/s/')
        await page.get_by_placeholder('Группа').fill(f'{title}')
        await page.keyboard.press('Enter')

        await asyncio.sleep(1)

        response = await page.content()
        soup = BeautifulSoup(response, "lxml")
        # print(soup)

        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        # schedule = f'{datetime.datetime.now().strftime("%Y/%m/%d %A").title()}'
        # schedule = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d.%m.%y %A").title()
        # schedule = datetime.datetime.strptime(schedule, "%d.%m.%y %A")
        dates = soup.find_all('div', class_='block-index')
        # print(dates)
        #
        # for date in dates:
        #     data = str(date.find('h2').text)
        #     data = datetime.datetime.strptime(data, "%d.%m.%y %A")

            # print(data.__class__, data)
            # print(schedule.__class__, schedule)
            # print(data == schedule)
        try:
            text = ''
            for i in range(0, 7):
                text += f'<b>\n📌 {(datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%d.%m.%y %A").title()}\n</b>'
                schedule = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%d.%m.%y %A").title()
                schedule = datetime.datetime.strptime(schedule, "%d.%m.%y %A")
                for date in dates:
                    data = str(date.find('h2').text)
                    data = datetime.datetime.strptime(data, "%d.%m.%y %A")
                    if data == schedule:
                        print('found schedule')
                        xz = date.find_all('div', class_='list-group-item')

                        for item in xz:
                            date_start = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[0]
                            # print(" ".join(item.text.split()).split(' ', 1)[1])
                            date_finish = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[1]
                            lesson = f'{" ".join(item.text.split()).split(" ", 1)[1]}'
                            # print(f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n')
                            text += f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n'
        finally:
            await callback.message.answer(text,
                                          parse_mode=ParseMode.HTML)
    # headman = await get.get_group_headman(callback.from_user.id)
    #
    # schedule = ''
    # locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    #
    # try:
    #     g = open(rf"schedules\{headman}.ics", 'rb')
    #     gcal = Calendar.from_ical(g.read())
    #     for i in range(0, 7):
    #         date_start = []
    #         lessons = []
    #         date_finish = []
    #         day = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
    #         schedule += f'\n\n📌 {(datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%A %Y/%m/%d").title()}\n'
    #         for component in gcal.walk():
    #             if component.name == "VEVENT":
    #                 DTSTAMP = component.get("DTSTAMP").dt
    #                 SUMMARY = component.get("SUMMARY")
    #                 DTEND = component.get("DTEND").dt
    #
    #                 if DTSTAMP.strftime("%Y-%m-%d") == day:
    #                     date_start.append(DTSTAMP.strftime("%H:%M"))
    #                     lessons.append(SUMMARY)
    #                     date_finish.append(DTEND.strftime("%H:%M"))
    #
    #         for i in range(0, len(lessons)):
    #             schedule += f'\n🌅 Начало пары: {date_start[i]} \n' + f'📓 {lessons[i]} \n' + f'🌃 Конец пары: {date_finish[i]} \n'
    #
    #     if schedule != '':
    #
    #         await callback.message.answer(schedule)
    #     else:
    #         await callback.answer('К сожалению или к вашему счастью расписания на неделю нет')
    #
    # except FileNotFoundError:
    #     await callback.answer('Расписание ещё не загружено. Обратитесь к старосте.')
    #
    # finally:
    #     if os.path.exists(rf"schedules\{headman}.ics"):
    #         g.close()



@router.message(Command('today'))
async def schedule_today(message: Message):
    title = await get.get_group_title(message.from_user.id)
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome', headless=True)
        page = await browser.new_page()
        await page.goto('https://www.altstu.ru/m/s/')
        await page.get_by_placeholder('Группа').fill(f'{title}')
        await page.keyboard.press('Enter')

        await asyncio.sleep(1)

        response = await page.content()
        soup = BeautifulSoup(response, "lxml")
        # print(soup)

        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        # schedule = f'{datetime.datetime.now().strftime("%Y/%m/%d %A").title()}'
        schedule = datetime.datetime.now().strftime("%d.%m.%y %A").title()
        schedule = datetime.datetime.strptime(schedule, "%d.%m.%y %A")
        dates = soup.find_all('div', class_='block-index')
        # print(dates)

        for date in dates:
            data = str(date.find('h2').text)
            data = datetime.datetime.strptime(data, "%d.%m.%y %A")

            # print(data.__class__, data)
            # print(schedule.__class__, schedule)
            # print(data == schedule)

            if data == schedule:
                print('found schedule')
                xz = date.find_all('div', class_='list-group-item')
                text = f'📌 {datetime.datetime.now().strftime("%d.%m.%y %A").title()}\n\n'
                for item in xz:
                    date_start = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[0]
                    # print(" ".join(item.text.split()).split(' ', 1)[1])
                    date_finish = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[1]
                    lesson = f'{" ".join(item.text.split()).split(" ", 1)[1]}'
                    # print(f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n')
                    text += f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n'
                await message.answer(text)



@router.message(Command('tomorrow'))
async def schedule_tomorrow(message: Message):
    title = await get.get_group_title(message.from_user.id)

    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome', headless=True)
        page = await browser.new_page()
        await page.goto('https://www.altstu.ru/m/s/')
        await page.get_by_placeholder('Группа').fill(f'{title}')
        await page.keyboard.press('Enter')

        await asyncio.sleep(1)

        response = await page.content()
        soup = BeautifulSoup(response, "lxml")
        # print(soup)

        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        # schedule = f'{datetime.datetime.now().strftime("%Y/%m/%d %A").title()}'
        schedule = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d.%m.%y %A").title()
        schedule = datetime.datetime.strptime(schedule, "%d.%m.%y %A")
        dates = soup.find_all('div', class_='block-index')
        # print(dates)

        for date in dates:
            data = str(date.find('h2').text)
            data = datetime.datetime.strptime(data, "%d.%m.%y %A")

            # print(data.__class__, data)
            # print(schedule.__class__, schedule)
            # print(data == schedule)

            if data == schedule:
                print('found schedule')
                xz = date.find_all('div', class_='list-group-item')
                text = f'📌 {(datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d.%m.%y %A").title()}\n\n'
                for item in xz:
                    date_start = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[0]
                    # print(" ".join(item.text.split()).split(' ', 1)[1])
                    date_finish = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[1]
                    lesson = f'{" ".join(item.text.split()).split(" ", 1)[1]}'
                    # print(f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n')
                    text += f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n'
                await message.answer(text)


@router.message(Command('week'))
async def schedule_tomorrow(message: Message):
    title = await get.get_group_title(message.from_user.id)
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome', headless=True)
        page = await browser.new_page()
        await page.goto('https://www.altstu.ru/m/s/')
        await page.get_by_placeholder('Группа').fill(f'{title}')
        await page.keyboard.press('Enter')

        await asyncio.sleep(1)

        response = await page.content()
        soup = BeautifulSoup(response, "lxml")
        # print(soup)

        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        # schedule = f'{datetime.datetime.now().strftime("%Y/%m/%d %A").title()}'
        # schedule = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d.%m.%y %A").title()
        # schedule = datetime.datetime.strptime(schedule, "%d.%m.%y %A")
        dates = soup.find_all('div', class_='block-index')
        # print(dates)
        #
        # for date in dates:
        #     data = str(date.find('h2').text)
        #     data = datetime.datetime.strptime(data, "%d.%m.%y %A")

        # print(data.__class__, data)
        # print(schedule.__class__, schedule)
        # print(data == schedule)
        try:
            text = ''
            for i in range(0, 7):
                text += f'<b>\n📌 {(datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%d.%m.%y %A").title()}\n</b>'
                schedule = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%d.%m.%y %A").title()
                schedule = datetime.datetime.strptime(schedule, "%d.%m.%y %A")
                for date in dates:
                    data = str(date.find('h2').text)
                    data = datetime.datetime.strptime(data, "%d.%m.%y %A")
                    if data == schedule:
                        print('found schedule')
                        xz = date.find_all('div', class_='list-group-item')

                        for item in xz:
                            date_start = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[0]
                            # print(" ".join(item.text.split()).split(' ', 1)[1])
                            date_finish = " ".join(item.text.split()).split((' - '))[0].split(' ', 1)[0].split('-')[1]
                            lesson = f'{" ".join(item.text.split()).split(" ", 1)[1]}'
                            # print(f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n')
                            text += f'\n🌅 Начало пары: {date_start} \n' + f'📓 {lesson} \n' + f'🌃 Конец пары: {date_finish} \n'
        finally:
            await message.answer(text,
                                 parse_mode=ParseMode.HTML)


