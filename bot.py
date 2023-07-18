import requests
import json
import discord

bot = discord.Bot()

# get the coordinates
def geoloc(location):
    API = 'https://geocode.maps.co/search?q={' + location + '}'

    coord = requests.get(API)

    return coord


# get the weather
def getWeather(lat, lon):
    API = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=Your API here&lang=en&units=metric'
    #to change language set &lang= // to change units set &units=

    weather = requests.get(API)

    return weather


#the proper command
@bot.command(description = 'get the weather')
async def weather(ctx, location: discord.Option(discord.SlashCommandOptionType.string, description = 'enter the location')):
    coord = geoloc(location)

    prsdCoord = json.loads(coord.content.decode('utf-8')) #parse the geolocation API response JSON

    weather = getWeather(prsdCoord[0]['lat'], prsdCoord[0]['lon'])

    prsdWeather = json.loads(weather.content.decode('utf-8')) #parse the weather API response JSON


    embed = discord.Embed(
        title = f'weather at {prsdWeather["name"]}',
        description = f'{prsdWeather["weather"][0]["description"]}',
        color = discord.Colour.blurple(),
    )
    #if you change the units don't forget to change here
    embed.add_field(name='feels like', value = f'{prsdWeather["main"]["feels_like"]} °C', inline = True)
    embed.add_field(name='temperature', value = f'{prsdWeather["main"]["temp"]} °C', inline = False)
    embed.add_field(name='minimum', value = f'{prsdWeather["main"]["temp_min"]} °C', inline = True)
    embed.add_field(name='maximum', value = f'{prsdWeather["main"]["temp_max"]} °C', inline = True)
    embed.add_field(name='humidity', value = f'{prsdWeather["main"]["humidity"]}%', inline = False)
    embed.add_field(name='cloudiness', value = f'{prsdWeather["clouds"]["all"]}%', inline = False)
    embed.add_field(name='wind', value = f'{prsdWeather["wind"]["speed"]} m/s', inline = True)
    embed.add_field(name='gust', value = f'{prsdWeather["wind"]["gust"]} m/s', inline = True)

    embed.set_thumbnail(url = f'https://openweathermap.org/img/wn/{prsdWeather["weather"][0]["icon"]}.png')

    await ctx.respond(embed = embed)



bot.run('Your token here')
