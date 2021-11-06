from random import randint
import discord
from discord.ext import commands
from math import ceil
TOKEN = ""

bot = commands.Bot(command_prefix=('+'))
bot.remove_command( 'help' )
#генерация достопримечательности даёт список содержащий в первом значении множество карт которые уже были розданы юзеры/врагу и второе даёт новую карту
class Player():
    deck={1:'<:1_:906135892652072980>', 2:'<:2_:906135897806864384>', 3:'<:3_:906135897425207337>', 4:'<:4_:906135898771583026>', 5:'<:5_:906135897211281429>', 6:'<:6_:906135898872234034>', 7:'<:7_:906135895491608586>', 8:'<:8_:906135894082347049>', 9:'<:9_p:906135897957875722>', 10:'<:10_:906135899719467068>', 11:'<:11_:906135898377322508>', 12:'<:12_:906135896024313866>', 13:'<:13_:906135898918379570>'}
    score=int()
    shield=int()
    cards=set()
    his_cards=str()
    effects=str()
    def __init__(self):
        n=randint(1,13)
        self.cards.add(n)
        self.gen_card=self.deck.get(n)
        self.score=self.score+n
        n=randint(1,13)
        self.his_cards+=self.deck.get(n)
        while self.gen_card == self.his_cards:
            n=randint(1,13)
            self.his_cards=self.deck.get(n)
        self.cards.add(n)
        self.score=self.score+n
        self.his_cards=str(self.his_cards)+str(self.gen_card)
#Ключевые переменные идут далее
user=Player()
enemy=Player()
win_score=int(100)
@bot.event
async def on_ready():
    print("Я запущен!")
@bot.command()
async def play(ctx):
    global user,enemy,win_score, msg #win_score очки для победы
    embed1=discord.Embed(title='Игра "Убеги из Омска."')
    embed1.add_field(name="Карты игрока:", value=user.his_cards, inline=False)
    embed1.add_field(name="Карты И.И.", value=str(enemy.his_cards), inline=False)
    embed1.add_field(name="Счёт игрока:", value=str(user.score), inline=False)
    embed1.add_field(name="Счёт И.И.:", value=str(enemy.score), inline=False)
    embed1.add_field(name="Счёт для победы:", value=str(win_score), inline=False)
    embed1.add_field(name="Эффекты игрока:", value='Эффектов нет', inline=False)
    embed1.add_field(name="Эффекты И.И.:", value='Эффектов нет',inline=False)
    embed1.add_field(name="Щит игрока:", value='Щита нет.',inline=False)
    embed1.add_field(name="Щит И.И.:", value='Щита нет.',inline=False)
    msg=await ctx.send(embed=embed1)

@bot.command()
async def draw(ctx):
    global win_score, msg #костыль с переменными не трогать
    n=randint(1,13)
    user.score+=n
    if n in user.cards:
        if enemy.shield>0:
            enemy.shield-=1
            user.effects='Комбо не сработало.'
        elif n==1:
            enemy.score=ceil(enemy.score/1.2)
            user.effects='Счёт И.И./1.2'
        elif n==2:
            win_score=win_score-10
            user.effects='Счёт для победы стал меньше на 10'
        elif n==3:
            user.score+=randint(1,13)*2
            user.effects='Счёт игрока увеличивается на случайное число от 1 до 13 *2'
        elif n==4:
            if enemy.score>user.score:
                a=int()
                s=set()
                st=str()
                a=user.score
                user.score=enemy.score
                enemy.score=a
                s=user.cards
                user.cards=enemy.cards
                enemy.cards=s
                st=user.his_cards
                user.his_cards=enemy.his_cards
                enemy.his_cards=st
                user.effects='Игрок меняется с И.И. картами'
        elif n==5:
            user.score+=randint(1,13)+randint(1,13)
            user.effects='Счёт игрока увеличивается на два случайных числа от 1 до 13'
        elif n==6:
            user.score=ceil(user.score*1.2)
            user.effects='Счёт игрока увеличивается в 1.2 раза'
        elif n==7:
            enemy.score+=10
            user.score=ceil(user.score*1.5)
            user.effects='Счёт И.И. +10, счёт игрока *1.5'
        elif n==8:
            n=randint(1,7)
            enemy.score-=n
            user.score+=n
            user.effects='Счёт игрока увеличивается, а счёт И.И. уменьшается на случайное число от 1 до 7'
        elif n==9:
            enemy.score=ceil(enemy.score*1.2)
            user.score=ceil(user.score*1.5)
            user.effects='Счёт И.И.*1.2, счёт игрока *1.5'
        elif n==10:
            win_score+=50
            user.effects='Счёт для победы +50'
        elif n==11:
            user.shield+=1
            user.effects='Есть'
        elif n==12:
            user.score+=20
            user.effects='Счёт игрока +20'
        else:
            enemy.score-=15
            user.effects='Счёт врага-15'
    else:
        user.cards.add(n)
        user.his_cards=user.his_cards+user.deck.get(n)
        enemy.effects='Эффектов нет.'

    n=randint(1,13)
    enemy.score+=n
    if n in enemy.cards:

        if user.shield>0:
            enemy.shield-=1
            enemy.effects='Комбо не сработало.'
        if n==1:
            user.score=ceil(user.score/1.2)
            enemy.effects='Счёт игрока./1.2'
        elif n==2:
            win_score-=10
            enemy.effects='Счёт для победы стал меньше на 10'
        elif n==3:
            enemy.score+=randint(1,13)*2
            enemy.effects='Счёт игрока увеличивается на случайное число от 1 до 13 *2'
        elif n==4:
            if user.score>enemy.score:
                a=int()
                s=set()
                st=str()
                a=user.score
                user.score=enemy.score
                enemy.score=a
                s=user.cards
                user.cards=enemy.cards
                enemy.cards=s
                st=user.his_cards
                user.his_cards=enemy.his_cards
                enemy.his_cards=st
                enemy.effects='И.И. меняется с игроком картами'

        elif n==5:
            enemy.score+=randint(1,13)+randint(1,13)
            enemy.effects='Счёт И.И. увеличивается на два случайных числа от 1 до 13'
        elif n==6:
            enemy.score=ceil(enemy.score*1.2)
            enemy.effects='Счёт И.И. увеличивается в 1.2 раза'
        elif n==7:
            user.score+=10
            enemy.score=ceil(enemy.score*1.5)
            enemy.effects='Счёт игрока +10, счёт И.И. *1.5'
        elif n==8:
            n=randint(1,7)
            user.score-=n
            enemy.score+=n
            enemy.effects='Счёт И.И увеличивается, а счёт игрока уменьшается на случайное число от 1 до 7'
        elif n==9:
            user.score=ceil(enemy.score*1.2)
            enemy.score=ceil(user.score*1.5)
            enemy.effects='Счёт игрока*1.2, счёт И.И. *1.5'
        elif n==10:
            win_score+=50
            enemy.effects='Счёт для победы+50'
        elif n==11:
            enemy.shield+=1
            enemy.effects='Есть'
        elif n==12:
            enemy.score+=20
            user.effects='Cчёт И.И. +20'
        else:
            user.score-=15
            enemy.effects='Счёт игрока-15'
    else:
        enemy.cards.add(n)
        enemy.his_cards+=str(user.deck.get(n))
        enemy.effects='Эффектов нет.'

    embed2=discord.Embed(title='Игра "Убеги из Омска."')
    embed2.add_field(name="Карты И.И.", value=enemy.his_cards, inline=False)
    embed2.add_field(name="Карты игрока:", value=user.his_cards, inline=False)
    embed2.add_field(name="Счёт игрока:", value=str(user.score), inline=False)
    embed2.add_field(name="Счёт И.И.:", value=str(enemy.score), inline=False)
    embed2.add_field(name="Счёт для победы:", value=str(win_score), inline=False)
    embed2.add_field(name="Эффекты игрока:", value=user.effects, inline=False)
    embed2.add_field(name="Эффекты И.И.:", value=enemy.effects,inline=False)
    embed2.add_field(name="Щит игрока:", value='Количество щитов '+str(user.shield),inline=False)
    embed2.add_field(name="Щит И.И.:", value='Количество щитов '+str(user.shield),inline=False)
    await msg.edit(embed=embed2)
    if user.score>win_score and enemy.score<win_score:
        await ctx.send('You win! Congratulations from creators of this game.')
    elif enemy.score>win_score:
        await ctx.send('ХАХАХАХ, будешь жить в Омске. Соболезную.')
    await ctx.send(str(user.score)+' '+str(enemy.score))

bot.run(TOKEN)
