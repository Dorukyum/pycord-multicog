import discord

from pycord.multicog import apply_multicog, add_to_group


def test_multicog():
    bot = discord.Bot()

    class FirstCog(discord.Cog):
        group = discord.SlashCommandGroup("group")

        @group.command()
        async def dummy(self, ctx):
            await ctx.respond("I am a dummy command.")

    class SecondCog(discord.Cog):
        @add_to_group("group")
        @discord.slash_command()
        async def test_command(self, ctx):
            await ctx.respond(f"I am inside the cog `{self.__class__.__name__}`.")

    bot.add_cog(FirstCog())
    bot.add_cog(SecondCog())

    apply_multicog(bot)

    assert isinstance(
        (group := bot.pending_application_commands[0]), discord.SlashCommandGroup
    )
    assert (test_command := group.subcommands[-1]).name == "test_command"
    assert test_command.parent is not None and test_command.parent == group


if __name__ == "__main__":
    test_multicog()
