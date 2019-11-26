from db.info_orm.queries import InfoQueries
import multiprocessing
from config import POOL_COUNT


def get_csv(filters):
    ins = InfoQueries(filters)
    path = ins.get_csv()
    return path


Pool = multiprocessing.Pool(POOL_COUNT if POOL_COUNT < multiprocessing.cpu_count() else 1)

