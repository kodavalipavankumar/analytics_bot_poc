from src.sql_validator import validate_sql


def test_valid_sql() -> None:
    result = validate_sql("SELECT region, SUM(sales_amount) AS revenue FROM sales GROUP BY region")
    assert result.is_valid is True


def test_invalid_delete() -> None:
    result = validate_sql("DELETE FROM sales")
    assert result.is_valid is False


def test_invalid_table() -> None:
    result = validate_sql("SELECT * FROM users")
    assert result.is_valid is False
