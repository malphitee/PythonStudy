import requests, json


def get_weather(city):
    api_url = "http://www.sojson.com/open/api/weather/json.shtml?city="
    request = requests.get(api_url + city)
    if request.status_code == 200:
        content = request.content
        result = json.loads(content)
        return result
    else:
        return "error!"


def handle_data(weather_info):
    data = weather_info['data']
    forecast = data['forecast']
    return "今日天气情况:\n" \
           + "温度     : " + str(data['wendu']) + "℃\n" \
           + "湿度     : " + str(data['shidu']) + "\n" \
           + "pm2.5   : " + str(data['pm25']) + "\n" \
           + "pm10    : " + str(data['pm10']) + "\n" \
           + "空气质量  : " + str(data['quality']) + "\n" \
           + "pm2.5   : " + str(data['pm25']) + "\n" \
           + "未来3天天气情况:\n" \
           + forecast[1]['date'] + "\n"\
           + "日出     : " + str(forecast[1]['sunrise']) + "\n" \
           + "日落     : " + str(forecast[1]['sunset']) + "\n" \
           + "日出     : " + str(forecast[1]['sunrise']) + "\n" \
           + "温度范围  : " + str(forecast[1]['low']) + " ~ " + str(forecast[1]['high']) + "\n" \
           + "风向     : " + str(forecast[1]['fx']) + "\n" \
           + "风力     : " + str(forecast[1]['fl']) + "\n" \
           + "天气     : " + str(forecast[1]['type']) + "\n" \
           + forecast[2]['date'] + "\n" \
           + "日出     : " + str(forecast[2]['sunrise']) + "\n" \
           + "日落     : " + str(forecast[2]['sunset']) + "\n" \
           + "日出     : " + str(forecast[2]['sunrise']) + "\n" \
           + "温度范围  : " + str(forecast[2]['low']) + " ~ " + str(forecast[2]['high']) + "\n" \
           + "风向     : " + str(forecast[2]['fx']) + "\n" \
           + "风力     : " + str(forecast[2]['fl']) + "\n" \
           + "天气     : " + str(forecast[2]['type']) + "\n" \
           + forecast[3]['date'] + "\n" \
           + "日出     : " + str(forecast[3]['sunrise']) + "\n" \
           + "日落     : " + str(forecast[3]['sunset']) + "\n" \
           + "日出     : " + str(forecast[3]['sunrise']) + "\n" \
           + "温度范围  : " + str(forecast[3]['low']) + " ~ " + str(forecast[3]['high']) + "\n" \
           + "风向     : " + str(forecast[3]['fx']) + "\n" \
           + "风力     : " + str(forecast[3]['fl']) + "\n" \
           + "天气     : " + str(forecast[3]['type']) + "\n" \
        # input_city = input("请输入要查询的城市名:")


res = get_weather("西安")
print(handle_data(res))
