import asyncio
import json
import logging
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# --- CONFIGURACIÓN ---
TOKEN = "TOKEN"  #Añadir el token generado por @BotFather al crear el bot
CONFIG_FILE = Path("config.json")
# --------------------

# Variable global para guardar la configuración cargada
config_data = {}

# Configuración de logging 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FUNCIONES PARA MANEJAR LA CONFIGURACIÓN ---

def load_config():
    """Carga la configuración desde el archivo JSON."""
    global config_data
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                config_data = json.load(f)
                logger.info("Configuración cargada exitosamente.")
        else:
            config_data = {"master_group_id": None, "slave_group_id": None}
            logger.warning("No se encontró config.json. Se usará una configuración vacía.")
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error al cargar config.json: {e}")
        config_data = {"master_group_id": None, "slave_group_id": None}

def save_config():
    """Guarda la configuración actual en el archivo JSON."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=4)
            logger.info("Configuración guardada exitosamente.")
    except IOError as e:
        logger.error(f"Error al guardar config.json: {e}")

# --- HANDLERS DEL BOT ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra los botones para definir el rol del grupo."""
    keyboard = [
        [InlineKeyboardButton("Definir como Grupo Maestro 👑", callback_data="set_master")],
        [InlineKeyboardButton("Definir como Grupo Esclavo 💾", callback_data="set_slave")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Por favor, define el rol de este grupo:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Procesa la selección del botón (Maestro o Esclavo)."""
    query = update.callback_query
    await query.answer()  # Responde al callback para que el botón deje de "cargar"

    role = query.data
    chat_id = query.message.chat_id
    chat_title = query.message.chat.title

    if role == "set_master":
        config_data["master_group_id"] = chat_id
        save_config()
        await query.edit_message_text(text=f"✅ ¡Confirmado! Este grupo ('{chat_title}') ahora es el **Grupo Maestro** 👑.")
        logger.info(f"Grupo {chat_id} ('{chat_title}') definido como Maestro.")

    elif role == "set_slave":
        config_data["slave_group_id"] = chat_id
        save_config()
        await query.edit_message_text(text=f"✅ ¡Confirmado! Este grupo ('{chat_title}') ahora es el **Grupo Esclavo** 💾.")
        logger.info(f"Grupo {chat_id} ('{chat_title}') definido como Esclavo.")

async def forwarder_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reenvía mensajes del grupo Maestro al Esclavo."""
    master_id = config_data.get("master_group_id")
    slave_id = config_data.get("slave_group_id")
    
    # Si no se han definido ambos roles, no hace nada
    if not master_id or not slave_id:
        return

    # Si el mensaje viene del grupo maestro, lo reenvía al esclavo
    if update.message.chat_id == master_id:
        try:
            await context.bot.forward_message(
                chat_id=slave_id,
                from_chat_id=master_id,
                message_id=update.message.message_id
            )
            logger.info(f"Mensaje reenviado desde Maestro ({master_id}) a Esclavo ({slave_id}).")
        except Exception as e:
            logger.error(f"No se pudo reenviar el mensaje: {e}")

def main():
    """Función principal que inicia el bot."""
    # Carga la configuración al iniciar
    load_config()

    print("Iniciando bot de backup...")
    application = Application.builder().token(TOKEN).build()

    # Añade los handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forwarder_handler))

    # Inicia el bot
    application.run_polling()

if __name__ == '__main__':
    main()