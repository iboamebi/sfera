from unittest.mock import MagicMock

from app.infrastructure.control_panel.control_panel_read_repository import (
    ControlPanelReadRepositorySQLAlchemy,
)


def test_control_panel_repository_uses_grouped_queries_and_preserves_archive_scope():
    session = MagicMock()
    query_results = [
        [("NEW", 2), ("IN_WORK", 3)],
        [("CREATED", 4), ("DECIDED", 5)],
        [("SUITABLE", 3)],
        [(False, 7), (True, 2)],
        [("AVAILABLE", 8)],
    ]
    queries = []
    for rows in query_results:
        query = MagicMock()
        query.filter.return_value = query
        query.group_by.return_value = query
        query.all.return_value = rows
        queries.append(query)
    session.query.side_effect = queries

    result = ControlPanelReadRepositorySQLAlchemy(session).get_overview()

    assert [query.all.call_count for query in queries] == [1, 1, 1, 1, 1]
    assert [query.group_by.call_count for query in queries] == [1, 1, 1, 1, 1]
    assert [query.filter.call_count for query in queries] == [1, 1, 1, 0, 0]
    assert [(item.key, item.count) for item in result.order_status_counts] == [
        ("NEW", 2),
        ("IN_WORK", 3),
    ]
    assert [(item.key, item.count) for item in result.verification_status_counts] == [
        ("CREATED", 4),
        ("DECIDED", 5),
    ]
    assert [(item.key, item.count) for item in result.verification_result_counts] == [
        ("SUITABLE", 3)
    ]
    assert [(item.archived, item.count) for item in result.customer_archive_counts] == [
        (False, 7),
        (True, 2),
    ]
    assert [(item.key, item.count) for item in result.instrument_status_counts] == [
        ("AVAILABLE", 8)
    ]
