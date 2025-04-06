import os


# connection string
CON_URI = f'postgresql+psycopg2://{os.environ["MYSQL_USER"]}:{os.environ["MYSQL_PASSWORD"]}'\
    f'@{os.environ["NET_IP"]}:{str(os.environ["MYSQL_PORT"])}/{os.environ["MYSQL_DATABASE"]}'