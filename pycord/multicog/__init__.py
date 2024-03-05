"""A pycord extension that allows splitting command groups into multiple cogs."""

from collections import namedtuple
from typing import Any, Callable, Dict, List, Optional

import discord
from discord.utils import get

__all__ = ("subcommand", "Bot")

MulticogMeta = namedtuple("MultiCogCommand", ["group", "independent", "group_options"])

multicog_commands: List[discord.SlashCommand] = []
multicog_metas: List[MulticogMeta] = []


def subcommand(
    group: str,
    *,
    independent: bool = False,
    group_options: Optional[Dict[str, Any]] = None,
) -> Callable[[discord.SlashCommand], discord.SlashCommand]:
    """A decorator to add a slash command to a slash command group.

    Arguments
    ---------
    group: :class:`str`
        The name of the group to attach the slash command to. If none found,
        one will be created.
    independent: :class:`bool`
        Whether the command should stay available when the cog containing
        the parent command group gets unloaded. Defaults to ``False``.
    group_options: Optional[:class:`dict`]
        The options to create the new slash command group with, if needed.
    """

    def decorator(command: discord.SlashCommand) -> discord.SlashCommand:
        if command.parent:
            raise TypeError(f"Command {command.name} is already in a group.")

        multicog_commands.append(command)
        meta = MulticogMeta(group=group, independent=independent, group_options=group_options)
        multicog_metas.append(meta)

        return command

    return decorator


class Bot(discord.Bot):
    """A subclass of `discord.Bot` that supports splitting command groups
    into multiple cogs.
    """

    def _add_to_group(self, command: discord.SlashCommand, group: discord.SlashCommandGroup) -> None:
        """A helper funcion to change attributes of a command to match those of the target group's."""

        index = multicog_commands.index(command)
        command.cog, command.parent, command.guild_ids = group.cog, group, group.guild_ids
        group.add_command(command)
        multicog_commands[index] = command

    def _find_group(self, name: str) -> Optional[discord.SlashCommandGroup]:
        """A helper function to find and return a slash command group with the
        provided name.
        """

        if name.count(" ") == 0:
            return get(self._pending_application_commands, name=name)

        group_name, subgroup_name = name.split("")
        if group := get(self._pending_application_commands, name=group_name):
            return get(group.subcommand, name=subgroup_name)

    def _get_meta(self, command: discord.SlashCommand) -> Optional[MulticogMeta]:
        """A helper funcion to retrieve multicog meta information of a command."""
        if command in multicog_commands:
            return multicog_metas[multicog_commands.index(command)]

    def add_application_command(self, command: discord.ApplicationCommand) -> None:
        if isinstance(command, discord.SlashCommandGroup) and (
            group := self._find_group(command.name)
        ):
            for subcommand in group.subcommands:
                command.subcommands.append(subcommand)
                subcommand.cog = group.cog

            super().remove_application_command(group)

        if not (
            isinstance(command, discord.SlashCommand)
            and (meta := self._get_meta(command))
        ):
            return super().add_application_command(command)

        if group := self._find_group(meta.group):
            return self._add_to_group(command, group)
        elif meta.independent:
            group = discord.SlashCommandGroup(meta.group, **meta.group_options or {})
            group.cog = command.cog
            self._add_to_group(command, group)
            return super().add_application_command(group)

        raise ValueError(
            f"Command {command.name} is dependent yet group {meta.group} could "
            "not be found. If you'd like to create a group when this command is "
            "being added to the bot, set independent=True in the add_to_group decorator."
        )

    def remove_application_command(
        self, command: discord.ApplicationCommand
    ) -> Optional[discord.ApplicationCommand]:
        if not isinstance(command, discord.SlashCommandGroup):
            return super().remove_application_command(command)

        for subcommand in command.subcommands.copy():
            if (
                not (isinstance(subcommand, discord.SlashCommand))
                or not (meta := self._get_meta(subcommand))
                or not meta.independent
            ):
                command.subcommands.remove(subcommand)

        if command.subcommands:
            command.cog = command.subcommands[0].cog
            return

        return super().remove_application_command(command)
