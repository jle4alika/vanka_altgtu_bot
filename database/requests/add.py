from database.models import async_session
from database.models import User, Group
from sqlalchemy import select, update, text
import datetime


async def add_name(tg_id: int, name: str):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(name=name))
        await session.commit()


async def edit_homework(tg_id: int, homework: str):
    async with async_session() as session:
        await session.execute(update(Group).where(Group.headman == tg_id).values(homework=homework))
        await session.commit()

async def add_and_edit_homework(tg_id: int, homework: str):
    async with async_session() as session:
        await session.execute(update(Group).where(Group.headman == tg_id).values(homework=Group.homework + f'\n{homework}'))
        await session.commit()

async def new_headman(tg_id: int, new_headman: int):
    async with async_session() as session:
        await session.execute(update(Group).where(Group.headman == tg_id).values(headman=new_headman))
        await session.commit()


async def add_group_member(tg_id: int):
    async with async_session() as session:
        await session.execute(update(Group).where(Group.headman == tg_id).values(members=Group.members + 1))
        await session.commit()


