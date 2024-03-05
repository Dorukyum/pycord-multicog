# pycord-multicog
[![Downloads](https://img.shields.io/pypi/dm/pycord-multicog?logo=pypi&logoColor=white)](https://pypi.org/project/pycord-multicog/)
[![Discord](https://img.shields.io/discord/789829818547175446?label=discord&logo=discord&color=5865F2&logoColor=white)](https://discord.com/invite/8JsMVhBP4W)

A pycord extension that allows splitting command groups into multiple cogs.

## Installation
Requires pycord v2.5 or higher.

```sh
$ pip install pycord-multicog
```

## Usage
### Initialising bot
```py
from pycord.multicog import Bot

bot = Bot(...)
```

### Creating commands
```py
# cog number 1, a normal cog with a slash command group
class Cog1(Cog):
    group = SlashCommandGroup("group")

    @group.command()
    async def subcommand1(self, ctx):
        await ctx.respond("This is a normal subcommand.")


# cog number 2, has a command used with add_to_group
from pycord.multicog import subcommand

class Cog2(Cog):
    @subcommand("group")  # this subcommand depends on the group defined in Cog1
    @slash_command()
    async def subcommand2(self, ctx):
        await ctx.respond("This subcommand is inside a different cog.")

    @subcommand("group", independent=True)  # this subcommand is independent
    @slash_command()
    async def subcommand2(self, ctx):
        await ctx.respond("This subcommand is also inside a different cog.")
```

