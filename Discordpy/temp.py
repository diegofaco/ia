from configparser import ConfigParser

config = ConfigParser()
config['DEFAULT'] = {
    'folder_path': 'C:/github/ia/Discordpy/Pool',
    'num_files': '5'
}

with open('config.ini', 'w', encoding='utf-8') as configfile:
    config.write(configfile)