import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject

# Включите логирование, чтобы видеть ошибки в консоли
logging.basicConfig(level=logging.INFO)

# Токен вашего бота (замените на свой токен от @BotFather)
BOT_TOKEN = "7715617821:AAEQKUbO_YY9_5kwP1t09zjVA_2wSBjPuDc"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция проверки: является ли отправитель админом
async def is_admin(message: types.Message) -> bool:
    member = await message.chat.get_member(message.from_user.id)
    return member.status in ["creator", "administrator"]

# --- КОМАНДА: БАН (/ban) ---
@dp.message(Command("ban"))
async def cmd_ban(message: types.Message):
    if not await is_admin(message):
        return await message.reply("❌ Эта команда только для администраторов.")
    
    if not message.reply_to_message:
        return await message.reply("❌ Эта команда должна быть ответом на сообщение пользователя, которого нужно забанить.")

    user_to_ban = message.reply_to_message.from_user
    try:
        await message.chat.ban(user_id=user_to_ban.id)
        await message.reply(f"ℹ️ Пользователь <b>{user_to_ban.full_name}</b> успешно забанен.", parse_mode="HTML")
    except Exception as e:
        await message.reply(f"❌ Не удалось забанить пользователя. Ошибка: {e}")

# --- КОМАНДА: МУТ (/mute) ---
# Использование: /mute (на 15 минут) или /mute 10 (на 10 минут)
@dp.message(Command("mute"))
async def cmd_mute(message: types.Message, command: CommandObject):
    if not await is_admin(message):
        return await message.reply("❌ Эта команда только для администраторов.")
    
    if not message.reply_to_message:
        return await message.reply("❌ Эта команда должна быть ответом на сообщение пользователя, которого нужно замутить.")

    user_to_mute = message.reply_to_message.from_user
    
    # Определение времени мута (по умолчанию 15 минут)
    duration = 15
    if command.args and command.args.isdigit():
        duration = int(command.args)

    until_date = datetime.now() + timedelta(minutes=duration)
    
    # Ограничиваем права (запрещаем отправку сообщений)
    permissions = types.ChatPermissions(can_send_messages=False)

    try:
        await message.chat.restrict(
            user_id=user_to_mute.id,
            permissions=permissions,
            until_date=until_date
        )
        await message.reply(f"🔇 Пользователь <b>{user_to_mute.full_name}</b> замучен на {duration} мин.", parse_mode="HTML")
    except Exception as e:
        await message.reply(f"❌ Не удалось замутить пользователя. Ошибка: {e}")

# --- КОМАНДА: РАЗМУТ (/unmute) ---
@dp.message(Command("unmute"))
async def cmd_unmute(message: types.Message):
    if not await is_admin(message):
        return await message.reply("❌ Эта команда только для администраторов.")
    
    if not message.reply_to_message:
        return await message.reply("❌ Эта команда должна быть ответом на сообщение пользователя, которого нужно размутить.")

    user_to_unmute = message.reply_to_message.from_user
    
    # Возвращаем полные права
    permissions = types.ChatPermissions(
        can_send_messages=True,
        can_send_audios=True,
        can_send_documents=True,
        can_send_photos=True,
        can_send_videos=True,
        can_send_video_notes=True,
        can_send_voice_notes=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )

    try:
        await message.chat.restrict(user_id=user_to_unmute.id, permissions=permissions)
        await message.reply(f"🔊 С пользователя <b>{user_to_unmute.full_name}</b> сняты ограничения.", parse_mode="HTML")
    except Exception as e:
        await message.reply(f"❌ Не удалось размутить пользователя. Ошибка: {e}")

# Запуск бота
async def main():
    print("Бот успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())