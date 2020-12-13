from chatterbot import ChatBot
from chatterbot.response_selection import get_first_response, get_random_response
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, render_template, request
from chatterbot.response_selection import get_most_frequent_response
from datetime import date
 

app = Flask(__name__)

my_bot = ChatBot("MyChatterBot", 
				storage_adapter='chatterbot.storage.SQLStorageAdapter',
				
				 logic_adapters=[
					 {
						 'import_path': 'chatterbot.logic.BestMatch',
						 'default_response': 'Mình chưa hiểu rõ lắm, bạn vui lòng nhắc lại được không ạ'
					 }
				 ],
				 response_selection_method=get_random_response,
				 #response_selection_method=get_first_response,
				 read_only=True)
trainer = ChatterBotCorpusTrainer(my_bot)

my_bot.storage.drop()
trainer.train("pcshop")
trainer.train('Warranty')

def check_warranty(str):
	today = date.today()
	today = today.strftime('%d/%m/%Y')
	list_today = today.split('/')
	
	list2 = str.split(' ')
	list1 = [int(s) for s in str.split() if s.isdigit()]
	length = len(list1)
	print(list_today)
	print(list1)
	if length < len(list_today):
		return True
	elif length == len(list_today):
		for i in range(0, length):
			if (int(list1[length - 1 - i])) > (int(list_today[length - 1 - i])):
				return False
				break
	return True

@app.route("/")
def home():
	return render_template("index.html")

print(check_warranty('ngày 15 tháng 7 năm 2021'))
@app.route("/get")
def get_bot_response():
	userText = request.args.get('msg')

	userText = str.lower(userText)
	output = 'unknown'
	
	if 'xin chào' in userText or 'chào' in userText:
		output = 'xin chào'
	elif 'bảo hành' in userText:
		output = 'bảo hành'
		if 'bao giờ' in userText or 'bao giờ hết hạn bảo hành' in userText or 'vẫn còn' in userText:
			output = 'kiểm tra'
		elif 'muốn' in userText or 'muốn bảo hành' in userText:
			output = 'muốn bảo hành'
		elif 'sản phẩm này' in userText:
			output = 'thông tin bảo hành sản phẩm'
		elif 'bảo hành theo' in userText:
			output = 'bảo hành theo số serial'
		elif ('laptop' in userText and 'bị hỏng' in userText) or ('laptop bị hỏng' in userText) or ('liệt phím' in userText) or ('màn hình' in userText) or ('đơ' in userText) or ('lag' in userText) or ('chậm' in userText) or ('màn hinh bị' in userText):
			output = 'laptop bị hỏng'
		elif 'laptop' in userText:
			if 'mang qua shop' in userText and 'bị hỏng' in userText:
				output = 'laptop vẫn bị hỏng dù đã sửa chữa'
		elif 'mình yêu nhau' in userText:
			output = 'mình yêu nhau đi'
		elif check_warranty(userText) == True:
			output = 'vẫn còn thời hạn bảo hành'
		else:
			output = 'unknown'
	print(check_warranty(userText))
	print('output = ' + output)
	respon_str = str(my_bot.get_response(output))		
	return respon_str
if __name__ == "__main__":
 	app.run()
