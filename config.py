import configparser
import logging
import random

logger = logging.getLogger(__name__)

class Config:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        # Video properties
        self.username = self.config.get('video', 'target_username', fallback=None)
        self.use_search = self.config.getboolean('video', 'use_search', fallback=False)
        if self.use_search:
            keys = self.config.get('video', 'search_keywords', fallback=None)
            key_list = keys.split(',')
            self.search_keywords = [key.strip() for key in key_list]
        self.range = self._get_optional_int('video', 'range')
        self.interval = self._get_optional_int('video', 'interval')
        self.threads = self._get_optional_int('video', 'threads')

        # Human Activity properties
        self.human_activity = self.config.getboolean('human activity', 'human_activity', fallback=False)

        # monitor properties
        self.monitor_mode = self.config.getboolean('monitor', 'monitor_mode', fallback=False)

        # content properties
        self.long_videos = self.config.getboolean('content', 'long_videos', fallback=False)
        self.shorts = self.config.getboolean('content', 'shorts', fallback=False)

        # csv properties
        self.use_csv = self.config.getboolean('csv', 'use_csv', fallback=False)
        self.csv_file = self.config.get('csv', 'csv_file', fallback=None)

        # Livestream properties
        self.livestream_link = self.config.get('livestream', 'livestream_link', fallback=None)

        # Options properties
        self.accounts = self._get_int_from_range('options', 'accounts')
        self.watch_time = self._get_int_from_range('options', 'watch_time')
        self.likes = self._get_int_from_range('options', 'likes')
        self.comments = self._get_int_from_range('options', 'comments')
        self.subscribes = self._get_int_from_range('options', 'subscribes')
        self.shares = self._get_int_from_range('options', 'shares')

        # Proxy properties
        self.use_proxy = self.config.getboolean('proxy', 'use_proxy', fallback=False)
        if self.use_proxy:
            self.rotating_proxies = self.config.getboolean('proxy', 'rotating_proxies', fallback=False)
            if self.rotating_proxies:
                self.ip = self.config.get('proxy', 'ip', fallback=None)
                self.port = self.config.get('proxy', 'port', fallback=None)
                self.proxy_username = self.config.get('proxy', 'username', fallback=None)
                self.proxy_password = self.config.get('proxy', 'password', fallback=None)
            else:
                self.proxy_file = self.config.get('proxy', 'proxy_file', fallback=None)

        # Settings properties
        self.headless = self.config.getboolean('settings', 'headless', fallback=True)

        # Search mode properties
        self.search_mode = self.config.getboolean('search mode', 'search_mode', fallback=False)
        if self.search_mode:
            self.video_link = self.config.get('search mode', 'video_link', fallback=None)
            keywords = self.config.get('search mode', 'search_keywords', fallback=None)
            key_list = keywords.split(',')
            self.search_keywords = [key.strip() for key in key_list]
            self.search_page_link = self.config.get('search mode', 'search_page_link', fallback=None)

        self.validate()
        logging.info("Config loaded successfully.")

    def _get_optional_int(self, section, option):
        """Returns the value as an integer if present and non-zero, or None if empty or zero."""
        value = self.config.get(section, option, fallback=None)
        return int(value) if value and int(value) != 0 else None
    
    def _get_int_from_range(self, section, option):
        """Returns the value as an integer if present and non-zero, or None if empty or zero."""
        value = self.config.get(section, option, fallback=None)
        if value:
            try:
                start, end = value.split('-')
                return random.randint(int(start), int(end))
            except ValueError:
                if value == '0':
                    return None
                logger.error(f"Invalid range value for {option}: {value}")
                exit()
        else:
            return None


    def validate(self):
        """Validates all the config fields at once."""
        # Validate video section
        if self.username and self.livestream_link:
            logger.warning("Both 'target_username' and 'livestream_link' are set. Ignoring 'livestream_link'.")
            self.livestream_link = None

        if not self.accounts:
            logger.error("'accounts' must be provided.")
            exit()

        if self.username:
            if not self.range:
                logger.error("'range' must be provided for 'target_username'.")
                exit()
            
            if not self.interval:
                logger.error("'interval' must be provided for 'target_username'.")
                exit()

        if self.use_csv and not self.csv_file:
            logger.error("'csv_file' must be provided for 'use_csv'.")
            exit()

        if self.use_proxy:
            if self.rotating_proxies and None in [self.ip, self.port, self.username, self.password]:
                logger.error("All the fields for 'rotating_proxies' must be provided.")
                exit()
            if not self.rotating_proxies and not self.proxy_file:
                logger.error("'proxy_file' must be provided if using datacenter proxies.")
                exit()

        if self.search_mode:
            self.use_search = False

        if self.search_mode and None in [self.search_page_link, self.video_link, self.search_keywords]:
            logger.error("All the fields for 'search_mode' must be provided.")
            exit()

        self.likes = self.likes * self.range
        self.comments = self.comments * self.range
        
        # keys = self.search_keywords.split(',')
        # self.search_keywords = [key.strip() for key in keys]

if __name__ == "__main__":
    config = Config()
    # config.display
    print(config.search_keywords)
