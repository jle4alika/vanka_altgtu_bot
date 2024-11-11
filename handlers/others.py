import asyncio

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext
import database.requests.get as get
import database.requests.add as add
import database.requests.others as set
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
import keyboards.inline as kb
import keyboards.reply as kbr
from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from icalendar import Calendar
import datetime

import qrcode
import re
import os
from dotenv import load_dotenv, find_dotenv
from pyrogram import Client
from pyrogram.raw.functions.contacts import ResolveUsername
import random

load_dotenv(find_dotenv())

router = Router()

pyrogram_client = Client(
    "michael",
    api_id=25172187,
    api_hash="c163275c64658d29c719f13786a92cbb",
    bot_token=os.getenv('TOKEN'),
    in_memory=False
)
async def resolve_username_to_user_id(username: str) -> int | None:
    try:
        await pyrogram_client.start()
    finally:
        r = await pyrogram_client.invoke(ResolveUsername(username=username))
        if r.users:
            return r.users[0].id


class Reg(StatesGroup):
    faculty = State()
    group = State()

class Settings(StatesGroup):
    schedule = State()
    homework_edit = State()
    homework_add_and_edit = State()
    new_headman = State()
    mail = State()


@router.message(Command('donate'))
async def donate(message: Message):
    await message.answer('<b>💖 Поддержите автора @jle4alika! 💖</b>'
                         '\n\nЕсли вам нравится то, что я делаю, и вы хотите помочь мне продолжать создавать качественный контент, вы можете сделать пожертвование! Ваша поддержка очень важна для меня и поможет развиваться, вдохновляться новыми идеями и радовать вас свежими материалами.'
                         '\n\n<b>🌟 Как сделать пожертвование:</b>'
                         '\n\n1. Нажмите на кнопку "Пожертвовать" ниже.'
                         '\n\n2. Выберите сумму, которую хотите внести.'
                         '\n\n3. Следуйте инструкциям для завершения транзакции.'
                         '\n\nКаждый вклад, независимо от размера, имеет значение и помогает мне двигаться вперед. Спасибо за вашу поддержку!'
                         '\n\n🙏<b> Ваши пожертвования помогут мне:</b>'
                         '\n\n• Создавать больше уникального контента'
                         '\n\n• Улучшать качество дизайна бота'
                         '\n\n• Реализовывать новые идеи и проекты'
                         '\n\n• Оплачивать хостинг данного бота'
                         '\n\nСпасибо, что вы со мной! ❤️',
                         reply_markup=kb.donate,
                         parse_mode=ParseMode.HTML)

@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    user_bool = await get.get_user_bool(message.from_user.id)
    if not user_bool:
        await message.answer(
            '🎓 Привет, студент! Добро пожаловать в наш бот! Здесь ты можешь найти помощь с учебой, задать вопросы и получить советы. Чем могу помочь сегодня? 📚✨')
        start_command = message.text
        username = message.from_user.username
        referrer_id = str(start_command[7:])
        if str(referrer_id) != '':
            if str(referrer_id) != str(message.from_user.id):
                title = await get.get_group_title(referrer_id)
                await message.answer(f'Вы успешно вступили в группу {title} 📚✨',
                                     reply_markup=kbr.user_main)
                await set.set_user(message.from_user.id, int(referrer_id))
                await bot.send_message(referrer_id, f'В группу вступил новый пользователь @{username}')
            else:
                await message.answer('<ins>Нельзя</ins> регистрироваться по собственной ссылке!', parse_mode=ParseMode.HTML)
        else:
            await message.answer('\n\nВыбери одну из опций, чтобы начать:'
                                 '\n\n🎓 <b>Я студент</b> — доступ к расписанию и домашней работе.'
                                 '\n🧑‍🏫 <b>Я староста</b> — управление группой и важные обновления',
                                 reply_markup=kb.user,
                                 parse_mode=ParseMode.HTML)
    else:
        user = await get.get_group_headman(message.from_user.id)
        if user == message.from_user.id:
            await message.answer(
                '🎓 Привет, студент! Добро пожаловать в наш бот! Здесь ты можешь найти помощь с учебой, задать вопросы и получить советы. Чем могу помочь сегодня? 📚✨',
            reply_markup=kbr.main)
        else:
            await message.answer(
                '🎓 Привет, студент! Добро пожаловать в наш бот! Здесь ты можешь найти помощь с учебой, задать вопросы и получить советы. Чем могу помочь сегодня? 📚✨',
            reply_markup=kbr.user_main)

@router.callback_query(F.data == 'student')
async def student(callback: CallbackQuery):
    await callback.message.answer(
        'Чтобы получить доступ к группе, пожалуйста, <b>свяжись со старостой</b> и попроси у него ссылку или отсканируй QR-код. 📲'
        '\n\nУдачи в учебе! 🍀',
        parse_mode=ParseMode.HTML)
    await asyncio.sleep(1)
    await callback.message.answer('🌟<b> Не забудьте подписаться на наш канал с новостями! </b>🌟'
                                  '\n\nЧтобы всегда быть в курсе последних обновлений и новостей о нашем боте, подписывайтесь на наш канал: @vankavstankaaltgtunews (https://t.me/vankavstanka_altgtu_news).'
                                  '\n\nБудьте первыми, кто узнает о новых функциях и улучшениях! 🚀'
                                  '\n\nСпасибо, что вы с нами! ❤️',
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=kb.news)

@router.callback_query(F.data == 'headman')
async def headman(callback: CallbackQuery):
    await set.set_user(callback.from_user.id)
    await callback.message.answer('При добавлении группы ты сможешь:'
                                  '\n\n• Изменять расписание 🗓️'
                                  '\n\n• Добавлять домашнюю работу 📚'
                                  '\n\n• Делать рассылку своим одногруппникам 🚀',
                                  reply_markup=kb.start)
# @router.message(Reg.name)
# async def nickname(message: Message, state: FSMContext):
#     names = await get.get_all_names(message.from_user.id)
#     await state.update_data(name=message.text)
#     data = message.text
#     counter = 0
#     for item in names:
#         if item == data:
#             counter += 1
#
#     if counter == 1:
#         await message.answer('Эй, такое ФИО уже зарегистрированно!')
#     else:
#         await add.add_name(message.from_user.id, str(data))
#         await state.clear()
#         await message.answer(f'<b>{data}</b>, вашe ФИО успешно сохранён.\nТак же вы можете поменять ваше ФИО в любое время в настройках.', parse_mode=ParseMode.HTML)
#         await message.answer('Теперь ты <ins>на последнем шаге</ins>! Осталось найти свою группу.\n Или ты можешь создать её, <ins>если ты староста</ins>!', reply_markup=kb.start, parse_mode=ParseMode.HTML)


@router.callback_query(F.data == 'new_group')
async def new_group(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('📝 Введите факультет здесь:')
    await state.set_state(Reg.faculty)

@router.message(Reg.faculty)
async def faculty(message: Message, state: FSMContext):
    await state.update_data(faculty=message.text)
    await message.answer('📝 Введите название группы здесь:')
    await state.set_state(Reg.group)


@router.message(Reg.group)
async def group(message: Message, state: FSMContext):
    counter = 0
    for title in await get.get_groups_titles():
        if title == message.text:
            counter += 1
    if counter == 0:
        await state.update_data(group=message.text)
        data = await state.get_data()
        await message.answer(f'Вы создали группу {data["group"]} ✨', reply_markup=kbr.main)
        await state.clear()
        await set.set_group(message.from_user.id, data["group"], data["faculty"])
        await set.set_user_group(message.from_user.id, message.from_user.id)
        await add.add_group_member(message.from_user.id)
        await asyncio.sleep(1)
        link = f'https://t.me/Alina_best_tutor_ever_bot?start={message.from_user.id}'
        # имя конечного файла
        filename = f"qr-codes/{message.from_user.id}.jpg"
        # генерируем qr-код
        img = qrcode.make(link)
        # сохраняем img в файл
        img.save(filename)
        qr = FSInputFile(rf"qr-codes\{message.from_user.id}.jpg")
        await message.answer_photo( photo=qr,
                                    caption=f'Привет, {message.from_user.first_name}! 👋'
                                            '\n\nНадеюсь, у тебя всё хорошо!'
                                            '\n\nЯ подготовил(а) QR-код и ссылку для вступления в нашу группу. Пожалуйста, поделись ими с новыми участниками, чтобы они могли легко присоединиться!'
                                            f'\n\n🔗 Ссылка для вступления:\n{link}'
                                            f'\n\nЕсли у тебя возникнут вопросы или понадобится помощь, дай знать!'
                                            f'\n\nСпасибо за твою работу! 💪')

        await asyncio.sleep(1)
        await message.answer('🌟<b> Не забудьте подписаться на наш канал с новостями! </b>🌟'
                             '\n\nЧтобы всегда быть в курсе последних обновлений и новостей о нашем боте, подписывайтесь на наш канал: @vankavstankaaltgtunews (https://t.me/vankavstanka_altgtu_news).'
                             '\n\nБудьте первыми, кто узнает о новых функциях и улучшениях! 🚀'
                             '\n\nСпасибо, что вы с нами! ❤️',
                             parse_mode=ParseMode.HTML,
                             reply_markup=kb.news)
    else:
        await message.answer('Данная группа уже зарегестрированна.\nВведите другое название группы, либо обратитесь к старосте.')


@router.message(F.text == 'Настройки ⚙️')
async def settings(message: Message):
    headman = await get.get_group_headman(message.from_user.id)

    if headman:
        await message.answer('Добро пожаловать в Настройки ⚙️! \n'
                             'Как вы видите, вы можете передать права старосты, поменять домашнее задание и сделать рассылку свои одногруппникам и загрузить расписание',
                             reply_markup=kb.headman_settings)



# @router.callback_query(F.data  == 'upload_schedule')
# async def upload_schedule(callback: CallbackQuery, state: FSMContext):
#     await callback.message.answer('Отправиьте файл в формате <ins>ics</ins>\n\n'
#                                   'ЛК -> Расписание студента -> Дополнительно (в правом углу) ->\n'
#                                   'Экспорт расписания в ics', parse_mode=ParseMode.HTML)
#     await state.set_state(Settings.schedule)


# @router.message(Settings.schedule)
# async def schedule_download(message: Message, bot: Bot, state: FSMContext):
#     file_id = message.document.file_id
#     await state.update_data(schedule=file_id)
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#     path = rf"schedules\{message.from_user.id}.ics"
#     document = message.document
#     await bot.download_file(file_path=file_path, destination=path)
#     await message.answer('Вы успешно загрузили новое расписание! ✨')
#     await state.clear()


@router.callback_query(F.data == 'change_homework')
async def set_homework(callback: CallbackQuery, state: FSMContext):
    homework = await get.get_homework(callback.from_user.id)
    await callback.message.answer(f'Текущее домашнее задание:\n\n {homework}', reply_markup=kb.set_homework)

@router.callback_query(F.data == 'edit')
async def set_homework(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Settings.homework_edit)
    await callback.message.answer('Введите <ins>новое домашнее задание</ins>', parse_mode=ParseMode.HTML)

@router.callback_query(F.data == 'add_and_edit')
async def set_homework(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Settings.homework_add_and_edit)
    await callback.message.answer('Введите то, <ins>что хотите добавить</ins>', parse_mode=ParseMode.HTML)


@router.message(Settings.homework_add_and_edit)
async def get_new_homework(message: Message, state: FSMContext):
    await state.update_data(homework_add_and_edit=message.text)
    data = message.text
    await add.add_and_edit_homework(message.from_user.id, data)
    homework = await get.get_homework(message.from_user.id)
    await message.answer(f'Вы изменили домашнее задание на: \n\n {homework}', reply_markup=kb.finish_homework_add_and_edit)


@router.message(Settings.homework_edit)
async def get_new_homework(message: Message, state: FSMContext):
    await state.update_data(homework_edit=message.text)
    data = message.text
    await add.edit_homework(message.from_user.id, data)
    homework = await get.get_homework(message.from_user.id)
    await message.answer(f'Вы изменили домашнее задание на: \n\n {homework}', reply_markup=kb.finish_homework_edit)



@router.callback_query(F.data == 'save_homework_edit')
async def save_homework(callback: CallbackQuery, state: FSMContext):
    homework = await get.get_homework(callback.from_user.id)
    await state.clear()
    await callback.message.answer(f'Вы успешно изменили домашнее задание на: \n\n {homework}')


@router.callback_query(F.data == 'save_homework_add_and_edit')
async def save_homework(callback: CallbackQuery, state: FSMContext):
    homework = await get.get_homework(callback.from_user.id)
    await state.clear()
    await callback.message.answer(f'Вы успешно изменили домашнее задание на: \n\n {homework}')


@router.callback_query(F.data == 'change_headman')
async def change_headman(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите юз нового старосты:')
    await state.set_state(Settings.new_headman)


@router.message(Settings.new_headman)
async def get_new_homework(message: Message, state: FSMContext, bot: Bot):
    mention = re.search(r'@(\w+)', message.text)
    print(mention)
    await state.update_data(new_headman=message.text)
    if mention:
        username = mention.group(1)
        print(username)
        headman = await resolve_username_to_user_id(username)
        print(headman)

        if headman != message.from_user.id:
            await add.new_headman(message.from_user.id, headman)
            await message.answer(f'Вы успешно передали права старосты - @{username}!', reply_markup=kbr.user_main)
            await bot.send_message(headman, 'Вам передали права старосты в группе!', reply_markup=kbr.main)


@router.callback_query(F.data == 'link')
async def change_headman(callback: CallbackQuery):
    link = f'https://t.me/Alina_best_tutor_ever_bot?start={callback.from_user.id}'

    if os.path.exists(rf"qr-codes\{callback.from_user.id}.jpg"):
        qr = FSInputFile(f"qr-codes/{callback.from_user.id}.jpg")
        await callback.message.answer_photo(photo=qr,
                                            caption=f'Привет, {callback.from_user.first_name}! 👋'
                                                    '\n\nНадеюсь, у тебя всё хорошо!'
                                                    '\n\nЯ подготовил(а) QR-код и ссылку для вступления в нашу группу. Пожалуйста, поделись ими с новыми участниками, чтобы они могли легко присоединиться!'
                                                    f'\n\n🔗 Ссылка для вступления:\n{link}'
                                                    f'\n\nЕсли у тебя возникнут вопросы или понадобится помощь, дай знать!'
                                                    f'\n\nСпасибо за твою работу! 💪')
    else:
        # имя конечного файла
        filename = f"qr-codes/{callback.from_user.id}.jpg"
        # генерируем qr-код
        img = qrcode.make(link)
        # сохраняем img в файл
        img.save(filename)
        qr = FSInputFile(rf"qr-codes\{callback.from_user.id}.jpg")
        await callback.message.answer_photo(photo=qr,
                                            caption=f'Привет, {callback.from_user.first_name}! 👋'
                                                    '\n\nНадеюсь, у тебя всё хорошо!'
                                                    '\n\nЯ подготовил(а) QR-код и ссылку для вступления в нашу группу. Пожалуйста, поделись ими с новыми участниками, чтобы они могли легко присоединиться!'
                                                    f'\n\n🔗 Ссылка для вступления:\n{link}'
                                                    f'\n\nЕсли у тебя возникнут вопросы или понадобится помощь, дай знать!'
                                                    f'\n\nСпасибо за твою работу! 💪')

@router.callback_query(F.data == 'mailing_list')
async def change_headman(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('🚀 Введите сообщение для рассылки')
    await state.set_state(Settings.mail)


@router.message(Settings.mail)
async def mailing(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(mail=message.text)
    mail = f'📢 Привет, друзья! 🌟 Это ваш староста, и у меня для вас важные новости! \n\n<blockquote><b>{message.text}</b></blockquote>'

    users = await get.get_group_users(message.from_user.id)
    for user in users:
        await bot.send_message(user, mail, parse_mode=ParseMode.HTML)

# async def group_kb(callback: CallbackQuery):
#     all_groups = await get.get_groups()
#     length = len(all_groups)
#
#     if callback.data.startswith('Далее_') or callback.data.startswith('Назад_'):
#         if str(callback.data[:6]) == 'Далее_':
#             i = int(callback.data[6:])
#             i += 1
#         else:
#             i = int(callback.data[6:])
#             i -= 1
#     else:
#         i = 1
#
#     key = InlineKeyboardBuilder()
#     if i == 1:
#         for group in all_groups[:8]:
#             title = await get.get_group_title(group)
#             members = await get.get_group_members(group)
#             groups = key.add(InlineKeyboardButton(text=f'{title} {members} участников', callback_data=f'name_{group}'))
#             groups.adjust(2)
#         if length / i > 8:
#             next = key.add(InlineKeyboardButton(text='Далее', callback_data=f'Далее_{i}'))
#             next.adjust(2)
#     else:
#         if i*8 >= length:
#             for group in all_groups[(i - 1) * 8:i * 8]:
#                 members = await get.get_group_members(group)
#                 title = await get.get_group_title(group)
#                 groups = key.add(InlineKeyboardButton(text=f'{title} {members} участников', callback_data=f'name_{group}'))
#                 groups.adjust(2)
#             if length / i > 8:
#                 next = key.add(InlineKeyboardButton(text='Далее', callback_data=f'Далее_{i}'))
#                 next.adjust(2)
#         elif i*8 <= length:
#             if length < (i+1)*8:
#                 for group in all_groups[(i - 1) * 8:length]:
#                     members = await get.get_group_members(group)
#                     title = await get.get_group_title(group)
#                     groups = key.add(InlineKeyboardButton(text=f'{title} {members} участников', callback_data=f'name_{group}'))
#                     groups.adjust(2)
#             for group in all_groups[(i-1)*8:length-1]:
#                 members = await get.get_group_members(group)
#                 title = await get.get_group_title(group)
#                 groups = key.add(InlineKeyboardButton(text=f'{title} {members} участников', callback_data=f'name_{group}'))
#                 groups.adjust(2)
#             if length / i > 8:
#                 next = key.add(InlineKeyboardButton(text='Далее', callback_data=f'Далее_{i}'))
#                 next.adjust(2)
#         back = key.add(InlineKeyboardButton(text='Назад', callback_data=f'Назад_{i}'))
#         back.adjust(2)
#     if length == 0:
#         await callback.answer('Групп нету.', show_alert=True)
#         return None
#     else:
#         return groups.as_markup()


# @router.callback_query(F.data == 'choose_group')
# async def clan_open_clan(callback: CallbackQuery):
#     if await group_kb(callback) != None:
#         await callback.message.edit_reply_markup(reply_markup=await group_kb(callback))
#
#
# @router.callback_query(F.data.startswith('name_'))
# async def clan_open_clan(callback: CallbackQuery):
#     # Clan_add.name = str(callback.data.replace('name_', ''))
#     group = str(callback.data.replace('name_', ''))
#     title = await get.get_group_title(group)
#     yes = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text='Вступить', callback_data=f'Вступить_{group}'),
#                 InlineKeyboardButton(text='Назад', callback_data='Назад')
#             ]
#         ]
#     )
#     await callback.message.answer(f'Вы хотите вступить в {title}?', reply_markup=yes)
#
# @router.callback_query(F.data.startswith('Вступить'))
# async def join(callback: CallbackQuery):
#     group = str(callback.data.replace('Вступить_', ''))
#     title = await get.get_group_title(group)
#     await set.set_user_group(callback.from_user.id, group)
#     await callback.message.answer(f'Вы успешно вступили в группу {title}',
#                                   reply_markup=kbr.user_main)
#
# @router.callback_query(F.data == 'Назад')
# async def back(callback: CallbackQuery):
#     await callback.message.answer('Воть тебе новый список групп)', reply_markup=await group_kb(callback))


