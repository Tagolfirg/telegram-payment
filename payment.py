from telebot.types import LabeledPrice


class Payment:
    def __init__(self, bot, payment_token):
        self.bot = bot
        self.labeledPrices = []
        self.paymentToken = payment_token

    def add_labeled_price(self, label, amount):
        new_label = LabeledPrice(label=label, amount=amount)
        self.labeledPrices.append(new_label)

    def send_invoice(self, chat_id, title, description,
                     invoice_payload):
        self.bot.send_invoice(chat_id=chat_id, title=title,
                              description=description,
                              invoice_payload=invoice_payload,
                              provider_token=self.paymentToken,
                              currency='UZS',
                              prices=self.labeledPrices,
                              start_parameter='start-parameter-todo',
                              photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
                              photo_height=512,
                              photo_width=512,
                              photo_size=512)

    def checkout(self, pre_checkout_query):
        self.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    def got_payment(self, message):
        text = 'Оплата прошла успешно! Будем обрабатывать ' +\
                'ваш заказ `{} {}` как можно быстрее!\n' +\
                'Номер заказа: `{}`\n' +\
                'Оставайтесь на связи.'
        self.bot.send_message(message.chat.id,
                              text.format(message.successful_payment.total_amount / 100,
                                          message.successful_payment.currency,
                                          message.successful_payment.provider_payment_charge_id),
                                          parse_mode='Markdown')

    def inform_managers(self, managers, reply_id, message):
        text = 'Оплата произведена клиентом через систему ' +\
               'PayMe.\nКод заказа: `{}`'
        for manager_id in managers:
            self.bot.send_message(manager_id,
                                  text.format(message.successful_payment.provider_payment_charge_id),
                                  reply_to_message_id=reply_id,
                                  parse_mode='Markdown')



#@bot.pre_checkout_query_handler(func=lambda query: True)
#@bot.message_handler(content_types=['successful_payment'])