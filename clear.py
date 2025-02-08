# SISTEMA DE !CLEAR COMPLETO PARA SEU SERVIDOR
# BY: Crazy_ArKzX
# GitHub: https://github.com/crazy-arkzx

import discord
from discord.ext import commands
from datetime import datetime
from colorama import Fore, Style

TOKEN = "SEU_TOKEN"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class ClearView(discord.ui.View):
    def __init__(self, ctx, amount, msg):
        super().__init__(timeout=30) 
        self.ctx = ctx
        self.amount = amount
        self.msg = msg

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author

    @discord.ui.button(label="✅ Confirmar", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        deleted = await self.ctx.channel.purge(limit=self.amount)
        msg = await self.ctx.send(f"O Chat Teve {len(deleted)} Mensagens Apagadas!")
        await msg.delete(delay=3) 

        now = datetime.now()
        date_str = now.strftime("%d-%m-%Y")
        time_str = now.strftime("%H:%M")

        log_message = (
            f"{Fore.CYAN}╔═══════════════════════════════════════╗\n"
            f"║ {Fore.LIGHTYELLOW_EX}▪︎Data: {date_str} às {time_str} {Fore.CYAN}\n"
            f"║ {Fore.LIGHTGREEN_EX}▪︎Usuário: {interaction.user} {Fore.CYAN}\n"
            f"║ {Fore.LIGHTRED_EX}▪︎Apagou: {len(deleted)} Mensagens {Fore.CYAN}\n"
            f"║ {Fore.LIGHTBLUE_EX}▪︎Canal: {self.ctx.channel.name} {Fore.CYAN}\n"
            f"╚═══════════════════════════════════════╝{Style.RESET_ALL}"
        )
        print(log_message)

        self.stop()

    @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.msg.delete()
        self.stop()

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if amount < 1:
        return await ctx.send("O Número tem que ser Maior que 0 Jumento!", delete_after=3)

    msg = await ctx.send(f"Você tem Certeza que Deseja Apagar {amount} Mensagens?")
    view = ClearView(ctx, amount, msg)  
    await msg.edit(view=view)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem Permissão!", delete_after=3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Uso Correto: `!clear {número}`", delete_after=3)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Digite um Número Válido!", delete_after=3)

@bot.event
async def on_ready():
    print(f"{Fore.GREEN}Sistema Carregado com Sucesso!{Style.RESET_ALL}")

bot.run(TOKEN)