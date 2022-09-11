# pycord-multicog
A pycord extension that allows splitting command groups into multiple cogs.

## Installation
```sh
$ pip install pycord-multicog
```

## Usage
### Creating cogs
```py
# cog number 1, a normal cog with a slash command group
class Cog1(Cog):
    group = SlashCommandGroup("group")

    @group.command()
    async def subcommand1(self, ctx):
        await ctx.respond("This is a normal subcommand.")


# cog number 2, has a command used with add_to_group
from pycord.multicog import add_to_group

class Cog2(Cog):
    @add_to_group("group")  # the decorator that does the magic
    @slash_command()
    async def subcommand2(self, ctx):
        await ctx.respond("This subcommand is inside a different cog.")
```

### Applying multicog using apply_multicog
```py
from pycord.multicog import apply_multicog

my_bot.add_cog(Cog1())
my_bot.add_cog(Cog2())
...
apply_multicog(my_bot)  # manually apply multicog after cogs are loaded
```

### Applying multicog using Bot subclass
```py
from pycord.multicog import Bot

my_bot = Bot()  # will automatically apply multicog when commands are being synchronised
```
