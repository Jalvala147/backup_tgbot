# Telegram Backup Bot

A bot to create a backup of messages (text, images, video) from a Master group to a Slave group.

## Setup

1.  Create a bot with **@BotFather** to get your **TOKEN**.
2.  Add the bot to both groups.
3.  Install the required library:
    ```bash
    pip install python-telegram-bot
    ```
4.  Run `backup_bot.py` and use the `/start` command in each group to assign the roles.

## Hosting

To run the bot 24/7, using a service like **PythonAnywhere** is recommended.

---

# Bot de Backup para Telegram

Un bot para crear una copia de seguridad de mensajes (texto, imágenes, video) desde un grupo Maestro a un grupo Esclavo.

## Configuración

1.  Crear un bot en **@BotFather** para obtener tu **TOKEN**.
2.  Añadir el bot a ambos grupos.
3.  Instalar la librería:
    ```bash
    pip install python-telegram-bot
    ```
4.  Ejecutar `backup_bot.py` y usa el comando `/start` en cada grupo para asignar los roles.

## Hosting

Para que el bot funcione 24/7, se recomienda usar un servicio como **PythonAnywhere**.

IDEAS a agregar:
1. manejo de mas de un grupo mediante algun identificador para agrupar ids de grupos 
2. metodo para scrapear contenido anterior y reenviar automaticamente

