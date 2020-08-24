import configparser


def create_config():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'name': 'MagicBall',
        'width': '1080',
        'height': '720',
        'tps': '60'
    }
    config['FILENAMES'] = {
        'background': 'bg.jpg'
    }
    with open('config.cfg', 'w') as cfg_file:
        config.write(cfg_file)

