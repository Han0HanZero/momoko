from os import listdir

__all__ = []
bot_list = listdir('BOTs')

for filename in bot_list:
    if filename != '__init__.py' and 'BOT' in filename and '.py' in filename:
        __all__.append(filename.removesuffix('.py'))
