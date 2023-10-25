import sqlvalidator

def validate_sql(sql: str) -> bool:
    query = sqlvalidator.parse(sql)
    return query.is_valid()
    