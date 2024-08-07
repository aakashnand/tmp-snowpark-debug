from snowflake.snowpark import Session

from ml_project.utils import log_snowflake_connection_info


def register_procedures(session: Session) -> str:
    session.clear_imports()
    session.add_import("ml_project")
    session.sproc.register_from_file(
        "ml_project/train.py",
        func_name="main",
        name="COMMON.TRAIN_PROPHET_MODEL",
        is_permanent=True,
        stage_location="@COMMON.PYTHON_CODE",
        imports=["ml_project"],
        packages=["snowflake-ml-python", "prophet"],
        replace=True,
        execute_as="caller",
    )
    return "Registered stored procedures."


if __name__ == "__main__":
    session = Session.builder.create()
    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    session.use_database("ML_EXAMPLE_PROJECT")
    session.use_schema("COMMON")
    log_snowflake_connection_info(session)
    print(register_procedures(session))
    raise SystemExit()
