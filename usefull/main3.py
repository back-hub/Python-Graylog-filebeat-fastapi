import package1
import app_logger

logger = app_logger.get_logger(__name__)


def main():
    logger.info("Программа стартует")
    package1.process(msg="Салам Алейкум. Мир вам братья!")
    logger.warning("Это должно появиться как в консоли, так и в файле журнала")
    logger.info("Программа завершила работу")
    try:
        1/0
    except Exception as ex:
        raise logger.exception(ex)

if __name__ == "__main__":
    main()