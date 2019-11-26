from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from config import INFO_PSQL_DB_CONFIG as info_db_config, BOT_PSQL_DB_CONFIG as bot_db_config

info_engine = create_engine('%s://%s:%s@%s:%s/%s' % (info_db_config['DB_TYPE'],
                                                     info_db_config['USER'],
                                                     info_db_config['PASSWORD'],
                                                     info_db_config['HOST'],
                                                     info_db_config['PORT'],
                                                     info_db_config['DB']),
                            echo=info_db_config['echo'],
                            execution_options={'stream_results': True},
                            pool_recycle=info_db_config['pool_recycle'])

bot_engine = create_engine('%s://%s:%s@%s:%s/%s' % (bot_db_config['DB_TYPE'],
                                                    bot_db_config['USER'],
                                                    bot_db_config['PASSWORD'],
                                                    bot_db_config['HOST'],
                                                    bot_db_config['PORT'],
                                                    bot_db_config['DB']),
                           echo=bot_db_config['echo'],
                           pool_recycle=bot_db_config['pool_recycle'])

info_session = scoped_session(sessionmaker(bind=info_engine))()
bot_session = sessionmaker(bind=bot_engine)()
