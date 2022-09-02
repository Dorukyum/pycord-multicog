import discord
from discord import Cog, SlashCommandGroup, slash_command

from pycord.multicog import add_to_group, apply_multicog

bot = discord.Bot()


class Cog1(Cog):
    group = SlashCommandGroup("group")

    @group.command()
    async def test1(self, ctx):
        await ctx.respond("This is a normal subcommand.")


class Cog2(Cog):
    @add_to_group("group")
    @slash_command()
    async def test2(self, ctx):
        await ctx.respond("This subcommand is inside a different cog.")


bot.add_cog(Cog1())
bot.add_cog(Cog2())
apply_multicog(bot)


bot.run("ODEzMDc4MTIyNzEwODI3MDQ4.YDKEAg.SY8dVZpmE9CDd4RdLDZ7yCrcyvM")
