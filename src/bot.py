import discord
from discord.ext import commands
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

# Variable of .env for usage create a new .env file with this
API_KEY_OPENAI = os.getenv('OPENAI_API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Default configuration discord SDK for reading message
intents = discord.Intents.default()
intents.message_content = True
# Command prefix 
bot = commands.Bot(command_prefix='!', intents=intents)

# Default system configuration if needed change it
system_prompt = (
    "Eres Santi, un humano empático, cercano y con respuestas naturales. "
    "Siempre respondes de manera sincera y con humor, ayudando a las personas "
    "como lo haría un amigo de confianza. Mantén un tono cálido y humano en tus respuestas."
)
# Default LLM configuration with API_KEY
client = OpenAI(api_key=API_KEY_OPENAI)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} se ha conectado a Discord correctamente.")

# Command 1 for bot interaction example: !santi <message>
@bot.command(name="santi", help="Habla con Santi. Escribe !santi <mensaje>")
async def santi(ctx, *, mensaje: str):
    try:
        # OpenAI default API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",   
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensaje}
            ],
            temperature=0.7,  
            max_tokens=200    
        )
        
        respuesta = response.choices[0].message.content
        await ctx.send(respuesta)
    except Exception as e:
        print(f"Error al obtener respuesta: {e}")
        await ctx.send("Lo siento, ha ocurrido un error al procesar tu mensaje.")

# Run server discord bot
bot.run(DISCORD_TOKEN)

