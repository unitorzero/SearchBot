import logging
from os.path import join, dirname

errors_file_handler = logging.FileHandler(join(dirname(__file__), 'logs/errors.log'))
errors_file_handler.setLevel(logging.ERROR)

auth_logger = logging.getLogger('auth')
auth_logger.setLevel(logging.INFO)
auth_file_handler = logging.FileHandler(join(dirname(__file__), "logs/auth.log"))
f_format = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s| %(message)s')
f_format_without_name = logging.Formatter('%(asctime)s|%(levelname)s| %(message)s')
auth_file_handler.setFormatter(f_format)
auth_logger.addHandler(auth_file_handler)

administration_logger = logging.getLogger('admin')
administration_logger.setLevel(logging.INFO)
administration_file_handler = logging.FileHandler(join(dirname(__file__), "logs/administration.log"))
administration_file_handler.setFormatter(f_format)
administration_logger.addHandler(administration_file_handler)
