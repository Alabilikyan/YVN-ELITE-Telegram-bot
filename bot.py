import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
import asyncio
import nest_asyncio

# Logging-ի կարգավորումները
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ողջույնի հաղորդագրության ֆունկցիա
async def welcome_new_member(update: Update, context: CallbackContext):
    try:
        welcome_message = """Բարի գալուստ ĔĽĬŦĔ | ÝVŊ կլան։
                1. Հարգեք միմյանց։
                2. Խուսափեք վիրավորանքներից։

                💬 Սեղմիր ներքևի կոճակը, որպեսզի ստանաս անվան կոդը, Կանոնադրություն։
        """
        
        # Կոճակ՝ STANAL
        keyboard = [
            [InlineKeyboardButton("📩 Կանոնադրություն", url=f"https://t.me/{context.bot.username}?start=welcome")],
            [InlineKeyboardButton("⚔️ Անվան կոդը", callback_data='stanal')]  # STANAL կոճակը
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        for new_member in update.message.new_chat_members:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Բարև {new_member.first_name}, {welcome_message}",
                parse_mode="Markdown",
                reply_markup=reply_markup,
                disable_notification=True  # Առանց ծանուցման
            )
            logger.info(f"Ուղարկվեց ողջույնի հաղորդագրություն {new_member.first_name}-ին")
    except Exception as e:
        logger.error(f"Սխալ ողջույնի հաղորդագրություն ուղարկելիս: {e}")

# STANAL կոճակի սեղմման հետևանք
async def handle_stanal_button(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        await query.answer()  # Ի պատասխան, որ կոճակը սեղմվել է
        
        # Ուղարկում ենք միայն STANAL հրամանի հետ կապված հաղորդագրությունը
        stanal_message = """ƳVƝ丨YOURNAME"""
        await query.message.reply_text(stanal_message)  # Ահա այստեղ ուղարկում ենք STANAL-ին վերաբերող հաղորդագրությունը
        logger.info(f"Ուղարկվեց STANAL հաղորդագրություն {query.from_user.first_name}-ին")
    except Exception as e:
        logger.error(f"Սխալ STANAL հաղորդագրություն ուղարկելիս: {e}")

# Կանոնադրության մասին հաղորդագրության ֆունկցիա
async def send_rules(update: Update, context: CallbackContext):
    try:
        # Ուղարկում ենք միայն կանոնադրության հաղորդագրությունը /start հրամանից
        rules_message = f"""Բարի գալուստ ĔĽĬŦĔ | ÝVŊ:
⚔️ ĔĽĬŦĔ | ÝVŊ Clan — Կանոնադրություն

1․ Պահպանեք հարգանք միմյանց նկատմամբ։
Բոլոր խաղացողներն այստեղ հավասար են՝ անկախ սեռից, փորձից կամ մակարդակից։

2․ Վիրավորանքներն ու անհարգալից պահվածքը արգելվում են։
Չեն թույլատրվում անձնական հարձակումներ, ատելության խոսք կամ վիրավորանքներ։

3․ Քննարկումները պետք է համապատասխանեն խաղի թեմային։
Խումբը նախատեսված է խաղի, ռազմավարությունների և կլանի կազմակերպչական հարցերի համար։

4․ Չի թույլատրվում անձնական բնույթի անհանգստացնող հաղորդագրություններ։
Խնդրում ենք հարգել բոլոր անդամներին, հատկապես հակառակ սեռի ներկայացուցիչներին։

5․ Խաղալիս հետևեք թիմային ռազմավարությանը։
Խաղացեք որպես թիմ՝ լավ արդյունքների համար։ 
---------------
Կլանին միանալու համար փոխեք Ձեր անունը 48 ժամվա ընթացքում այլապես կհեռացվեք կլանից։

Սեղմեք ⚔️ ƳVƝ丨 կոճակը անվան դիմացի կոդը ստանալու համար։

Սիրով ĔĽĬŦĔ | ÝVŊ բոտ։
        """
        
        # Կոճակ՝ STANAL
        keyboard = [
            [InlineKeyboardButton("⚔️ ƳVƝ丨", callback_data='stanal')]  # STANAL կոճակը
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Ուղարկում ենք կանոնադրության հաղորդագրությունը
        await update.message.reply_text(rules_message, parse_mode="Markdown", reply_markup=reply_markup)
        logger.info("Ուղարկվեց կանոնադրության հաղորդագրություն")
    except Exception as e:
        logger.error(f"Սխալ կանոնադրության հաղորդագրություն ուղարկելիս: {e}")

# Գլխավոր ֆունկցիա
async def main():
    try:
        # Այստեղ ներմուծեք ձեր բոտի API Token-ը
        application = Application.builder().token("7718585924:AAFandSJzHCtueAo5kb_07tc54aLgy2NYgY").build()

        # Ավելացնում ենք նոր անդամի ողջույնի հաղորդագրության գործիքը
        application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

        # Ավելացնում ենք /start հրամանը
        application.add_handler(CommandHandler("start", send_rules))

        # Ավելացնում ենք STANAL կոճակի callback query-ի գործիքը
        application.add_handler(CallbackQueryHandler(handle_stanal_button, pattern='^stanal$'))
        
        # Սկսում ենք բոտը
        logger.info("Բոտը պատրաստ է ընդունելու հրահանգներ...")
        await application.run_polling()
        logger.info("Բոտը սկսեց աշխատել...")
    except Exception as e:
        logger.error(f"Սխալ բոտի գործարկման ժամանակ: {e}")

# Ճիշտ asyncio event loop-ի գործարկում
if __name__ == "__main__":
    nest_asyncio.apply()
    try:
        if not asyncio.get_event_loop().is_running():
            asyncio.run(main())
        else:
            loop = asyncio.get_running_loop()
            loop.create_task(main())
    except Exception as e:
        logger.critical(f"Անսպասելի սխալ: {e}")
