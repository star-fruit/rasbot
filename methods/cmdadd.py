from errors import CommandIsBuiltInError
import config

# This is a built-in function.
# Please do not modify this unless you really know what you're doing.

MODONLY_ARG = "-modonly"

def main(bot):
    cmd = bot.cmdargs
    
    if MODONLY_ARG in cmd:
        modonly=True
        cmd.remove(MODONLY_ARG)
    else:
        modonly=False

    try:
        bot.commands.command_modify(cmd[0],cmd[1]," ".join(cmd[2:]),modonly)
        config.write(bot)
        #bot.db.create_or_update_command(cmd[0],cmd[1]," ".join(cmd[2:]))
        return f'Command {cmd[0]} added successfully.'

    except CommandIsBuiltInError:
        return 'You cannot modify built-in commands.'

    except IndexError:
        return f'Please specify the name, cooldown in seconds, and response. Add {MODONLY_ARG} in the command if you wish for the command to be mod-only.'