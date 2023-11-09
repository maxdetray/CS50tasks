import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    task = State()
    delete = State()


TOKEN = '6895281906:AAGu2II3tvJx9tum8lcLr3WOXjw2e2NjSPU'
user_router = Router()
dp = Dispatcher()

# dict to store all tasks
tasks = {}

# help menu
HELP = ('Button Add task - to add a task.\n'
        'Button Delete task - to delete task from list.\n'
        'Button List of tasks - shows full list of tasks.\n'
        'What will you choose?')

# keyboard
main_kb = InlineKeyboardBuilder()
main_kb.add(types.InlineKeyboardButton(text='Add task', callback_data='/add'))
main_kb.add(types.InlineKeyboardButton(
    text='Delete task', callback_data='/delete'))
main_kb.add(types.InlineKeyboardButton(
    text='List of tasks', callback_data='/list'))
main_kb.add(types.InlineKeyboardButton(text='Help', callback_data='/help'))
main_kb.adjust(2)


def register_router(dp: Dispatcher) -> None:
    dp.include_router(user_router)


# Processing command /start
@user_router.message(CommandStart())
async def on_start(msg: types.Message) -> None:
    # user_id = msg.from_user.id
    # tasks[user_id] == []
    await msg.answer(
        f"Greetings {msg.from_user.first_name}! This is your To-Do List bot. Which command will you choose? If in "
        f"doubt, click the Help button.",
        reply_markup=main_kb.as_markup())


# Processing help button
@user_router.message(Command('help'))
async def on_entered_help(msg: types.Message):
    await msg.answer(text=HELP, reply_markup=main_kb.as_markup())
    return HELP


@user_router.callback_query(F.data == '/help')
async def send_help(callback: types.CallbackQuery):
    await callback.message.answer(text=HELP, reply_markup=main_kb.as_markup())


# Processing add button
@user_router.callback_query(F.data == '/add')
async def send_add(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.task)
    await callback.message.answer('Enter the task you want to add to the list.')


# Processing delete button
@user_router.callback_query(F.data == '/delete')
async def send_delete(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    # print(tasks)
    if user_id not in tasks or not tasks[user_id]:
        await callback.answer("Your task list is empty!")
        return
    else:
        await state.set_state(Form.delete)
        await callback.message.answer('Enter the number of the task you want to delete.')
        # print(len(tasks), tasks)


# Processing a text message with a task
@user_router.message(Form.task)
# @user_router.message(lambda message: not message.text.startswith('/'))
async def add_task(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    task_entered = message.text

    if user_id not in tasks:
        tasks[user_id] = []

        tasks[user_id].append(task_entered)
        await message.answer(f'The task "{task_entered}" has been added to the list.', reply_markup=main_kb.as_markup())
    else:
        tasks[user_id].append(task_entered)
        await message.answer(f'The task "{task_entered}" has been added to the list.', reply_markup=main_kb.as_markup())
    await state.clear()


# Processing list button
@user_router.callback_query(F.data == '/list')
async def on_list_tasks(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id in tasks and tasks[user_id]:
        task_list = tasks[user_id]

        # Use to enumerate tasks
        numbered_tasks = [f'{i + 1}. {task}' for i,
                          task in enumerate(task_list)]

        task_list_text = "\n".join(numbered_tasks)

        chat_id = callback.message.chat.id
        message_id = callback.message.message_id
        # list shows in same message
        await callback.bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                             text=f'Your task list:\n{task_list_text}',
                                             reply_markup=main_kb.as_markup())
        await callback.answer()
    else:
        await callback.answer("Your task list is empty!")


# Processing delete task from list
@user_router.message(Form.delete)
async def on_delete_task(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    task_list = tasks[user_id]
    try:
        task_index = int(message.text) - 1

        if 0 <= task_index < len(task_list):
            removed_task = task_list.pop(task_index)
            await message.answer(f'The task "{removed_task}" has been removed from the list.',
                                 reply_markup=main_kb.as_markup())
            await state.clear()
        else:
            await message.answer("Specify a valid task index to delete.", reply_markup=main_kb.as_markup())

    except (IndexError, ValueError):
        await message.answer("Enter the numeric number of a task from the list to delete a task.",
                             reply_markup=main_kb.as_markup())
    await state.clear()


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.MARKDOWN)
    register_router(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print('Exit', e)
