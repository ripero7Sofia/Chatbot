import datetime
import vk_api
import sqlite3
from vk_api.longpoll import VkLongPoll, VkEventType
class VKBot:
	def __init__(self, bot_name, api_token):
		self.session = vk_api.VkApi(token=api_token)
		self.longpoll = VkLongPoll(self.session)
		self.vk = self.session.get_api()
		self.bot_name = bot_name
		self.conn = sqlite3.connect(self.bot_name + ".db")

	def send_message(self, message, id):
		self.vk.messages.send(user_id=id, message=message, random_id=datetime.datetime.now().microsecond)

	def start(self):
		init_db = open("init_db.sql")
		raw_init = init_db.readlines()
		init = ""
		for line in raw_init:
			init += line.replace("\n", " ")
		self.conn.execute(init)
		for event in self.longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.to_me:
				command_words = event.text.split(" ")
				if command_words[0] == self.bot_name:
					if len(command_words) > 3 and command_words[1] == "сохрани" and command_words[2] == "соц.сеть":
						raspisanie = event.text[18 + len(self.bot_name):]
						self.conn.execute(f'INSERT OR REPLACE INTO user_info(vk_id, sentence) VALUES ({event.user_id}, "{raspisanie}")')
						self.conn.commit()
						self.send_message(f'Привет, cоц.сеть {raspisanie} успешно сохранена!', event.user_id)
					if len(command_words) > 2 and command_words[1] == "напиши" and command_words[2] == "соц.сеть":
						answer = self.conn.execute(f"SELECT sentence FROM user_info WHERE vk_id = {event.user_id}").fetchall()
						if len(answer) > 0:
							answer = answer[0][0]
							self.send_message(f'Да, конечно! Вот ваша соц.сеть: {answer}', event.user_id)
						else:
							self.send_message('Ошибка: вы не сохраняли никакую соц.сеть', event.user_id)
					if len(command_words) > 2 and command_words[1] == "удали" and command_words[2] == "соц.сеть":
						self.conn.execute("DROP TABLE user_info",)
						self.conn.commit()
						self.send_message(f'Да, конечно!Соц.сеть удалена ', event.user_id)








bot = VKBot("Bot", "vk1.a.BE3bKi9reNDyzOhkWNRVKfyjw25hs8sfK6aiOSmnAvl7Anj7seAQjp7NLxGNYaGJJ3cj9wufgVi2zf8eq1bcoirr8W5JhUjxReMtrRodz6P3CJSQMu3lcqT1FLg383jUg7Vief7oX73WVM4jmxo_S-EbI32s5t4RaGheIpa6UhHCVDkZDvCfXPlLq-ZKdpySWX7ly1gZgHzWCe8cixhTEA")
bot.start()
