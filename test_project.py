import pytest
from project import on_entered_help, on_start, send_add, Form
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_on_entered_help():
    message = AsyncMock()
    message.message_id = 789
    message.date = 1234567890
    message.chat.id = 456
    message.chat.type = 'private'
    message.from_user.id = 123
    message.from_user.is_bot = False
    message.from_user.first_name = 'Dave'
    message.text = '/help'

    # call function
    response = await on_entered_help(message)

    # without return
    # assert response is None

    # with return
    assert ('Button Add task - to add a task.\nButton Delete task - to delete task from list.\nButton List of tasks - '
            'shows full list of tasks.\nWhat will you choose?') in response


@pytest.mark.asyncio
async def test_start_command_handling():
    # Create types.Message with attr
    message = AsyncMock()
    message.message_id = 789
    message.date = 1234567890
    message.chat.id = 456
    message.chat.type = 'private'
    message.from_user.id = 123
    message.from_user.is_bot = False
    message.from_user.first_name = 'Dave'
    message.text = '/start'

    # Call func
    response = await on_start(message)

    # result
    assert response is None


@pytest.mark.asyncio
async def test_send_add():
    # create async mok-obj for types.CallbackQuery
    callback = AsyncMock()
    callback.message.answer.return_value = None

    # create async mok-obj for FSMContext
    fsm_context = AsyncMock()

    # Call func with two async obj
    await send_add(callback, fsm_context)

    # Check what func 'return'
    callback.message.answer.assert_awaited_once_with(
        'Enter the task you want to add to the list.')
    fsm_context.set_state.assert_awaited_once_with(Form.task)
