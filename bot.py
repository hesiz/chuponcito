import discord
from discord.ext import commands, tasks
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

activities = [
    discord.Activity(type=discord.ActivityType.playing, name="hesiz"),
    discord.Activity(type=discord.ActivityType.playing, name="@chuponcito"),
    discord.Activity(type=discord.ActivityType.watching, name="hesiz"),
    discord.Activity(type=discord.ActivityType.watching, name="@chuponcito"),
    discord.Activity(type=discord.ActivityType.listening, name="hesiz"),
    discord.Activity(type=discord.ActivityType.listening, name="@chuponcito")
]

@tasks.loop(seconds=5)
async def change_status():
    activity = random.choice(activities)
    await bot.change_presence(activity=activity, status=discord.Status.online)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    change_status.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if bot.user in message.mentions:
        if not message.reference:
            await message.channel.send("hazme ping en la respuesta de un mensaje verga")
            return
        
        try:
            referenced_message = await message.channel.fetch_message(message.reference.message_id)
            text_to_add = referenced_message.content
            
            if not text_to_add:
                await message.channel.send("No hay texto imbécil")
                return
            
            image = Image.open('chuponcito.png')
            draw = ImageDraw.Draw(image)
            
            x1, y1 = 10, 252
            x2, y2 = 319, 383
            max_width = x2 - x1
            max_height = y2 - y1
            
            font_size = 20
            try:
                font = ImageFont.truetype("FontChuponcito.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            lines = []
            words = text_to_add.split()
            current_line = ""
            
            for word in words:
                test_line = current_line + word + " "
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] - bbox[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
            
            if current_line:
                lines.append(current_line.strip())
            
            total_text_height = len(lines) * (font_size + 5)
            
            while total_text_height > max_height and font_size > 8:
                font_size -= 2
                try:
                    font = ImageFont.truetype("FontChuponcito.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                lines = []
                current_line = ""
                
                for word in words:
                    test_line = current_line + word + " "
                    bbox = draw.textbbox((0, 0), test_line, font=font)
                    if bbox[2] - bbox[0] <= max_width:
                        current_line = test_line
                    else:
                        if current_line:
                            lines.append(current_line.strip())
                        current_line = word + " "
                
                if current_line:
                    lines.append(current_line.strip())
                
                total_text_height = len(lines) * (font_size + 5)
            
            y_offset = y1
            for line in lines:
                draw.text((x1, y_offset), line, fill='white', font=font)
                y_offset += font_size + 5
            
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            file = discord.File(img_buffer, filename='chuponcito_with_text.png')
            await message.channel.send(file=file)
                
        except Exception as e:
            await message.channel.send(f"Error: {str(e)}")
    
    await bot.process_commands(message)

bot.run('MTQ2ODEzNDM1NjYxNzkyMDUzNA.GAMWPr.ZnQSO1DhwX1SxKRjsHWz3N8-YPSCRHHcrR_bEE')
