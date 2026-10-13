"""LocalQuant 数据库初始化命令。"""

from src.database import DEFAULT_DB_PATH, initialize_database, get_table_names


def main() -> None:
    path = initialize_database()
    print(f"数据库已准备就绪：{path}")
    print("已创建的数据表：")
    for table_name in get_table_names(path):
        print(f" - {table_name}")


if __name__ == "__main__":
    main()
