import importlib.util
import time
from errors import CommandIsBuiltInError, CommandIsModOnlyError, CommandStillOnCooldownError

###
#   rasbot commands module
#   raspy#0292 - raspy_on_osu
###

class Command:
    def __init__(self, name:str, cooldown:int = 5, response:str='', requires_mod:bool=False):
        '''Creates a new command.

        :param name: The name of the command.

        :param cooldown: The cooldown of the command in seconds.

        :param response: The text response of the command. Encapsulate custom commands in &&.

        :param requires_mod: Whether the command requires the user to be a mod.
        '''
        self.name = name
        self.cooldown = int(cooldown)
        self.response = response
        self.requires_mod = requires_mod

        self.__last_used = 0

    def run(self, bot):
        # Make sure the command is not on cooldown before doing anything
        if not time.time()-self.__last_used > self.cooldown:
            raise CommandStillOnCooldownError(f"command {self.name} called while still on cooldown")
        
        if not bot.caller_ismod and self.requires_mod:
            raise CommandIsModOnlyError(f"mod-only command {self.name} called by non-mod {bot.caller_name}")

        # Apply any custom methods encased in &&
        returned_response = self.response
        for method_name, method in methods.items():
            if f'&{method_name}&' in returned_response:
                returned_response = returned_response.replace(f'&{method_name}&',method.main(bot))

        # Update the last usage time and return the response
        self.__last_used = time.time()
        return returned_response

class CustomMethod:
    def __init__(self, name:str):
        '''Creates a new custom method.

        :param name: The name of the custom method. File must be visible in the custommethods folder.
        '''
        self.name = name

        # Importing the method and setting this CustomMethod's main method
        spec = importlib.util.spec_from_file_location(f"{name}",f"custommethods/{name}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.main = module.main

    # To be replaced with the new main method.
    def main():
        pass

def command_modify(name:str, cooldown:int = 5, response:str = '', requires_mod:bool = False):
    '''Creates a new command (or modifies an existing one),
    and appends it to the commands dict.

    :param name: The name of the command.

    :param cooldown: The cooldown of the command in seconds.

    :param response: The text response of the command. Encapsulate custom commands in &&.
    '''
    # You cannot modify built-ins
    if name in builtins:
        raise CommandIsBuiltInError(f"command {name} is built in")

    commands[name] = Command(name,cooldown,response,requires_mod)

def command_del(name:str):
    '''Deletes a command and removes it from the dict.

    :param name: The name of the command.
    '''
    # You cannot modify built-ins
    if name in builtins:
        raise CommandIsBuiltInError(f"command {name} is built in")
    
    try:
        del(commands[name])
    except KeyError:
        raise ValueError(f'command {name} does not exist')

def custommethod_add(name:str):
    '''Creates a new custommethod and appends it to the commands dict.

    :param name: The name of the custom method. File must be visible in the custommethods folder.
    '''
    methods[name] = CustomMethod(name)

def custommethod_del(name:str):
    '''Deletes a custommethod and removes it from the dict.

    :param name: The name of the custommethod.
    '''
    try:
        del(methods[name])
    except KeyError:
        raise ValueError(f'custommethod {name} does not exist')

commands = dict()
methods = dict()

# Do not modify this! These are built-in commands.
builtins = ['help','uptime','cmdadd','cmddel','prefix']
commands["help"] = Command("help",5,"&help&")
commands["uptime"] = Command("uptime",5,"&uptime&")
commands["cmdadd"] = Command("cmdadd",5,"&cmdadd&",True)
commands["cmddel"] = Command("cmddel",5,"&cmddel&",True)
commands["prefix"] = Command("prefix",5,"&prefix&",True)