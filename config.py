import configparser
import logging

logger = logging.getLogger(__name__)

class Config:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        # Video properties
        self.username = self.config.get('video', 'target_username', fallback=None)
        self.range = self._get_optional_int('video', 'range')
        self.interval = self._get_optional_int('video', 'interval')
        self.threads = self._get_optional_int('video', 'threads')

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
        self.accounts = self._get_optional_int('options', 'accounts')
        self.watch_time = self._get_optional_int('options', 'watch_time')
        self.likes = self._get_optional_int('options', 'likes')
        self.comments = self._get_optional_int('options', 'comments')
        self.subscribes = self._get_optional_int('options', 'subscribes')
        self.shares = self._get_optional_int('options', 'shares')

        # Settings properties
        self.headless = self.config.getboolean('settings', 'headless', fallback=True)

        self.validate()
        logger.info("Config loaded successfully.")

    def _get_optional_int(self, section, option):
        """Returns the value as an integer if present and non-zero, or None if empty or zero."""
        value = self.config.get(section, option, fallback=None)
        return int(value) if value and int(value) != 0 else None


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

        self.likes = self.likes * self.range
        self.comments = self.comments * self.range
