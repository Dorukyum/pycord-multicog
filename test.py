import discord

from pycord.multicog import Bot, subcommand


def run_test(func):
    if __name__ == "__main__":
        func()

    return func


@run_test
def test_dependent():
    bot = Bot()

    class FirstCog(discord.Cog):
        group = discord.SlashCommandGroup("group")

        @group.command()
        async def dummy(self, ctx):
            await ctx.respond("I am a dummy command.")

    class SecondCog(discord.Cog):
        @subcommand("group")
        @discord.slash_command()
        async def test_command(self, ctx):
            await ctx.respond(f"I am another dummy command.")

    bot.add_cog(FirstCog())
    bot.add_cog(SecondCog())

    group = bot.pending_application_commands[0]
    assert isinstance(group, discord.SlashCommandGroup)
    test_command = group.subcommands[-1]
    assert test_command.name == "test_command"
    assert test_command.parent == group

    bot.remove_cog("FirstCog")

    assert not bot.pending_application_commands


@run_test
def test_independent():
    bot = Bot()

    class FirstCog(discord.Cog):
        @subcommand("group", independent=True)
        @discord.slash_command()
        async def test_command(self, ctx):
            await ctx.respond("Hello there.")

    bot.add_cog(FirstCog())

    group = bot.pending_application_commands[0]
    assert isinstance(group, discord.SlashCommandGroup)
    test_command = group.subcommands[0]
    assert test_command.name == "test_command"
    assert test_command.parent == group

    bot.remove_cog("FirstCog")

    group = bot.pending_application_commands[0]
    assert isinstance(group, discord.SlashCommandGroup)
    test_command = group.subcommands[0]
    assert test_command.name == "test_command"
    assert test_command.parent == group

