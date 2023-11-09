# FinalprojectCS50Bot
#### Video Demo:  <https://youtu.be/qSvREiOSr8M>
#### Description: To-Do list implemented as a telegram bot.

### This is a simple To-Do list implemented as a telegram bot. You may find this bot here [Bot](https://t.me/FinalprojectCS50_bot)
### The bot is implemented using an asynchronous library's aiogram and asyncio. It has four functions which are implemented with Inline keyboard buttons. It's “Add”, “List”, “Delete” and “Help” buttons. So, you don't need to write commands in the command line. But there are two commands that you can write. It's /start and /help.
### At the beginning bot welcomes user with a welcome message and short bot description and asks to press /start or write it. After this, the bot greets the user by his name in Telegram and offers a choice of four commands in the form of Inline buttons.
### When you press the “Help” button, brief instructions for each button appear on the screen. And in addition, this function is implemented as a Menu button on the left side of the command line.
### By clicking on the “Add” button, the bot sends the user a text with a proposal to add a task. After the user has entered it, the task is written into the dictionary, the key for the task is a unique user identifier. This way the user can create a list of tasks for himself.
### When you click on the “List” button, the bot displays a list of entered tasks. In this case, this list is numbered each time. If the list is empty, the user will be shown a pop-up message indicating this.
### When you click on the “Delete” button, the bot will display a message asking you to enter the number of the task that the user wants to delete. If the user enters a task number that is not in the list, the bot will display a message asking you to specify the valid index. If the user enters something other than a number, the bot will display a message that the input must be numeric. If the index is entered correctly, the bot will remove the task from the list and notify the user about this.

### These are the functions this simple bot can perform. I hope you will like it.

### *P.S. This is my first attempt at writing bots, as well as my own projects using Python, so don’t judge too harshly.*