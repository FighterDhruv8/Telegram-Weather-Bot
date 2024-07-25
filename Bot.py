def main():
    
    import requests
    import telebot
    
    def load_api_key():
        """Loads the API key from a config file."""
        with open(".\\config\\Telegram_API.txt", "r") as f:
            api_key = f.read().strip()
        return api_key
    
    def load_weather_api_key():
        """Loads the API key from a config file."""
        with open(".\\config\\OpenWeatherMap_API.txt", "r") as f:
            api_key = f.read().strip()
        return api_key
    
    
    BOT_TOKEN = load_api_key()
    bot = telebot.TeleBot(BOT_TOKEN)
    
    
    @bot.message_handler(commands=['start', 'hello'])
    def send_welcome(message):
        bot.reply_to(message, "Hello! Type \"Weather\" to begin!")
    
    state = 0
    city = None
    
    def get_weather(city, api_key):
        base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(base_url)
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["main"]
        return [temperature, description]
    
    @bot.message_handler(content_types= 'text')
    def check(message):
        global state
        global city
        global country_code
        if(message.text == "Weather" or message.text == 'weather'):
            state = 1
            bot.reply_to(message, "What is your city?")
        elif(state == 1):
            city = message.text
            state = 0
            curr_weather = get_weather(city, load_weather_api_key())
            bot.reply_to(message, f"{round(curr_weather[0])} degrees Celsius, {curr_weather[1]}")    
    
    bot.infinity_polling()

if __name__ == '__main__':
    main()