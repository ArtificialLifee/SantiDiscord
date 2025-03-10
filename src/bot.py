import discord
from discord.ext import commands
import openai
import os

# Variable of .env for usage create a new .env file with this
API_KEY_OPENAI = os.environ.get('OPENAI_API_KEY')
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

# Configuración de intents (nota: para leer el contenido de los mensajes se debe activar message_content)
intents = discord.Intents.default()
intents.message_content = True

# Inicializamos el bot con un prefijo, por ejemplo "!"
bot = commands.Bot(command_prefix='!', intents=intents)

# Este prompt define el contexto del LLM para que responda como Santi.
system_prompt = (
    "Eres Santi, un humano empático, cercano y con respuestas naturales. "
    "Siempre respondes de manera sincera y con humor, ayudando a las personas "
    "como lo haría un amigo de confianza. Mantén un tono cálido y humano en tus respuestas."
)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} se ha conectado a Discord correctamente.")

# Comando para interactuar con el bot: !santi <mensaje>
@bot.command(name="santi", help="Habla con Santi. Escribe !santi <mensaje>")
async def santi(ctx, *, mensaje: str):
    try:
        # Realizamos la petición a la API de OpenAI utilizando ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",   
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensaje}
            ],
            temperature=0.7,  
            max_tokens=200    
        )
        # Obtenemos el mensaje generado por OpenAI
        respuesta = response.choices[0].message.content
        await ctx.send(respuesta)
    except Exception as e:
        print(f"Error al obtener respuesta: {e}")
        await ctx.send("Lo siento, ha ocurrido un error al procesar tu mensaje.")

# Inicia el bot utilizando el token de Discord
bot.run(DISCORD_TOKEN)

