from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import dateutil.parser
from config import INFO_PSQL_DB_CONFIG as info_db_config

info_engine = create_engine('%s://%s:%s@%s:%s/%s' % (info_db_config['DB_TYPE'],
                                                     info_db_config['USER'],
                                                     info_db_config['PASSWORD'],
                                                     info_db_config['HOST'],
                                                     info_db_config['PORT'],
                                                     info_db_config['DB']),
                            echo=info_db_config['echo'],
                            pool_recycle=info_db_config['pool_recycle'])

Session = sessionmaker(bind=info_engine)
session = Session()

QUERY_TIMEOUT = 30  # in seconds
COLUMNS = ["datname", "pid", "query_start", "query", "state"]

query_template = """
    select {columns} from pg_stat_activity where state = 'active';
"""
cancel_query_template = """
    select pg_cancel_backend({pid});
"""
terminate_query_template = """
    select pg_terminate_backend({pid});
"""


def check_row(row):
    now = datetime.datetime.now(datetime.timezone.utc)
    return (row["state"] == "active"
            and row["datname"] == "info_psql"
            and row["query"].lower().startswith("select")
            and (now - row["query_start"].astimezone(datetime.timezone.utc)) > datetime.timedelta(seconds=QUERY_TIMEOUT)
            )


def parse_row(row):
    result = {x: row[x] for x in COLUMNS}
    if "query_start" in COLUMNS:
        result["query_start"] = dateutil.parser.parse(row["query_start"])
    return result


def cancel_query(con, pid):
    con.execute(cancel_query_template.format(pid=pid))
    return True


def terminate_query(con, pid):
    con.execute(terminate_query_template.format(pid=pid))
    return True


def main():
    connection = info_engine.connect()
    result = connection.execute(query_template.format(columns=",".join(COLUMNS)))
    canceled = []
    for row in result:
        # row = parse_row(row)
        if (check_row(row)):
            cancel_query(connection, row["pid"])
            canceled.append(row["pid"])
    new_result = connection.execute(query_template.format(columns=",".join(COLUMNS)))
    list(map(lambda x: terminate_query(connection, x["pid"]) if x["pid"] in canceled else None, new_result))
    connection.close()
    print("{num} queries canceled!".format(num=len(canceled)))


if __name__ == "__main__":
    main()
