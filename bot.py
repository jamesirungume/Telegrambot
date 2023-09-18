import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "6420814914:AAFWfTLlq_a-VlyfsCiHlX-9QUNw7Z0sk7E"

# Define states for the conversation
START, CHOICE, RESULT = range(3)

# Define a dictionary to store user data
user_data = {}

# Define a function to start the conversation
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Hello! I am your Telegram bot. Send me a message or use /choice to make a choice.")
    return START

# Define a function to handle the /choice command
def choice(update: Update, context: CallbackContext) -> int:
    keyboard = [['Option 1', 'Option 2']]
    update.message.reply_text("Choose an option:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return CHOICE

# Define a function to handle the user's choice
def handle_choice(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text
    user_data['choice'] = user_choice
    update.message.reply_text(f"You chose: {user_choice}. Now, send me a message or use /result to see the result.")
    return RESULT

# Define a function to show the result
def result(update: Update, context: CallbackContext) -> int:
    user_choice = user_data.get('choice', 'No choice made')
    update.message.reply_text(f"Your choice was: {user_choice}. Thanks for using the bot!")
    return ConversationHandler.END

# Define a function to echo user messages
def echo(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    update.message.reply_text(f"You said: {user_message}")

def main() -> None:
    # Create the Updater
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register a command handler for the /start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Register a command handler for the /choice command
    dispatcher.add_handler(CommandHandler("choice", choice))

    # Define a conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('choice', choice)],
        states={
            CHOICE: [MessageHandler(Filters.text & ~Filters.command, handle_choice)],
            RESULT: [CommandHandler('result', result)],
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    # Register a message handler to echo user messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == "__main__":
    main()
