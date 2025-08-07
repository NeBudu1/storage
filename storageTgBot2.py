import telebot
import sqlite3
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot("8421288956:AAHBYP4bwtMVRMpM_5widtrwzW8PTwXt4sY")
userproducts = {}

def createDb():
    bd = sqlite3.connect("tovars2.db")

    cursor = bd.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TOVARY2 (
        Id INTEGER PRIMARY KEY,
        Name TEXT,
        Kolishestvo INTEGER,
        Weith INTEGER,
        Price INTEGER
    
    
    
    
    
         )
    
    
    
    
    
        """)
    bd.commit()
    bd.close()


@bot.message_handler(["start"])
def startt(message):
    buttons = ReplyKeyboardMarkup()
    b1 = KeyboardButton("/Добавить_товар")
    b2 = KeyboardButton("/Удалить_товар")
    b3 = KeyboardButton("/Посмотреть_склад")
    buttons.add(b1, b2, b3)
    bot.send_message(message.chat.id, "Выбери действие", reply_markup=buttons)
@bot.message_handler(["Добавить_товар"])
def addTovar(message):
    bot.send_message(message.chat.id, "Напиши название товара")
    bot.register_next_step_handler(message, getname)
def getname(message):
    userproducts[message.chat.id] = {"name": message.text}
    bot.send_message(message.chat.id, "Напиши количество товара")
    bot.register_next_step_handler(message, getkolko)
def getkolko(message):
    userproducts[message.chat.id]["kolko"] = int(message.text)
    bot.send_message(message.chat.id, "Напиши вес товара")
    bot.register_next_step_handler(message, getweith)
def getweith(message):
    userproducts[message.chat.id]["weith"] = int(message.text)
    bot.send_message(message.chat.id, "Напиши цену товара")
    bot.register_next_step_handler(message, getprice)
def getprice(message):
    userproducts[message.chat.id]["price"] = int(message.text)
    bd = sqlite3.connect("tovars2.db")
    data = userproducts[message.chat.id]
    cursor = bd.cursor()
    cursor.execute("INSERT INTO TOVARY2 (Name, Kolishestvo, Weith, Price) VALUES (?, ?, ?, ?)",
                   (data["name"], data["kolko"], data["weith"], data["price"] ))
    bdread = cursor.fetchall()
    for i in bdread:
        print(i)
    bd.commit()
    bd.close()
    print(userproducts)

@bot.message_handler(["Посмотреть_склад"])
def show(message):
    bd = sqlite3.connect("tovars2.db")
    cursor = bd.cursor()
    cursor.execute("SELECT Name, Kolishestvo, Weith, Price FROM TOVARY2")
    rols = cursor.fetchall()
    for i in rols:
        bot.send_message(message.chat.id, f"Имя товара: {i[0]}, количество товара: {i[1]}, вес товара: {i[2]}, цена товара: {i[3]}")

@bot.message_handler(["Удалить_товар"])
def delete(message):
    bot.send_message(message.chat.id, "Напиши имя товара")
    bot.register_next_step_handler(message, name)
def name(message):
    nameee = message.text
    bdd = sqlite3.connect("tovars2.db")
    cursor = bdd.cursor()
    cursor.execute("DELETE FROM TOVARY2 WHERE Name = ?", (nameee,))
    bot.send_message(message.chat.id, "Товар удалён")
    bdd.commit()
    bdd.close()


bot.polling(non_stop=True)