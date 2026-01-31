from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import urllib.parse

# ===============================
# CONFIGURAÇÕES
# ===============================
TOKEN = "8540728145:AAFQ8k6tm81CEE_BrgseSHB0oX9-8X9kxqU"
AFILIADO_ID = "18391510152"

# ===============================
# FUNÇÕES AUXILIARES
# ===============================
def gerar_link(produto, modo):
    produto_encoded = urllib.parse.quote(produto)

    base = f"https://shopee.com.br/search?keyword={produto_encoded}"

    if modo == "barato":
        base += "&sortBy=price_asc"
    elif modo == "vendido":
        base += "&sortBy=sales"
    elif modo == "avaliado":
        base += "&sortBy=relevancy"

    afiliado = (
        f"&mmp_pid={AFILIADO_ID}"
        f"&utm_source={AFILIADO_ID}"
        f"&utm_medium=affiliates"
    )

    return base + afiliado


# ===============================
# COMANDO /start
# ===============================
def start(update: Update, context: CallbackContext):
    mensagem = (
        "👋 Olá! Seja bem-vindo(a) 😄\n\n"
        "Sou seu assistente de ofertas da Shopee 🛍️\n"
        "Me diga o nome de qualquer produto e eu encontro:\n\n"
        "💸 O menor preço\n"
        "🔥 O que todo mundo está comprando\n"
        "⭐ Os melhor avaliados\n\n"
        "👉 Exemplo:\n"
        "mouse sem fio\n"
        "blusa feminina\n\n"
        "Vamos achar a melhor oferta pra você 😉"
    )

    update.message.reply_text(mensagem)


# ===============================
# MENSAGEM DO USUÁRIO
# ===============================
def responder(update: Update, context: CallbackContext):
    produto = update.message.text.strip()

    if len(produto) < 2:
        update.message.reply_text("Digite o nome de um produto 🙂")
        return

    context.user_data["produto"] = produto

    texto = (
        f"🔎 Procurando as melhores opções de:\n\n"
        f"🛍️ {produto}\n\n"
        f"Como você prefere ver as ofertas?"
    )

    teclado = [
        [InlineKeyboardButton("💸 Quero pagar o menor preço", callback_data="barato")],
        [InlineKeyboardButton("🔥 O que todo mundo compra", callback_data="vendido")],
        [InlineKeyboardButton("⭐ Qualidade bem avaliada", callback_data="avaliado")]
    ]

    update.message.reply_text(
        texto,
        reply_markup=InlineKeyboardMarkup(teclado)
    )


# ===============================
# CALLBACK DOS BOTÕES
# ===============================
def botoes(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    produto = context.user_data.get("produto")

    if not produto:
        query.edit_message_text("Digite o produto novamente 🙂")
        return

    modo = query.data
    link = gerar_link(produto, modo)

    resposta = (
        f"✅ Pronto! Separei as melhores opções de:\n\n"
        f"🛍️ {produto}\n\n"
        f"👉 Toque no link abaixo para ver as ofertas:\n\n"
        f"{link}\n\n"
        f"Se quiser outro produto, é só digitar 😉"
    )

    query.edit_message_text(resposta)


# ===============================
# MAIN
# ===============================
def main():
    print("🤖 BOT SHOPEE FINAL ATIVO (ESTÁVEL + CONVERSÃO ALTA)")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, responder))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, start))
    dp.add_handler(
        telegram.ext.CallbackQueryHandler(botoes)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    import telegram.ext
    main()
