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
            await ctx.respond("I am another dummy command.")

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


@run_test
def test_subgroup():
    bot = Bot()

    def check_tree(parent, subgroup_name: str, command_name: str):
        assert isinstance(parent, discord.SlashCommandGroup)
        subgroup = parent.subcommands[-1]
        assert isinstance(subgroup, discord.SlashCommandGroup)
        assert subgroup.name == subgroup_name
        command = subgroup.subcommands[-1]
        assert command.name == command_name
        assert command.parent == subgroup

    class FirstCog(discord.Cog):
        group = discord.SlashCommandGroup("group")
        subgroup = group.create_subgroup("subgroup")

        @subgroup.command()
        async def dummy(self, ctx):
            await ctx.respond("I am a dummy command.")

    class SecondCog(discord.Cog):
        @subcommand("group subgroup")
        @discord.slash_command()
        async def test_command(self, ctx):
            await ctx.respond("I am another dummy command.")

        @subcommand("another_group another_subgroup", independent=True)
        @discord.slash_command()
        async def test_command_2(self, ctx):
            await ctx.respond("I am yet another dummy command.")

    bot.add_cog(FirstCog())
    bot.add_cog(SecondCog())

    group = bot.pending_application_commands[0]
    check_tree(group, "subgroup", "test_command")
    another_group = bot.pending_application_commands[-1]
    check_tree(another_group, "another_subgroup", "test_command_2")
