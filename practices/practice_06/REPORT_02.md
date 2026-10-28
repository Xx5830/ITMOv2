# Отчёт 2. Повторные атаки после исправлений

Повторный прогон `BASELINE=1 python3 -m unittest test_security_before -v` из `lab/` против исправленного `service.py`. Полный набор `make test` (`lab/`) — 25 passed, 9 skipped (baseline-тесты пропущены вне `BASELINE=1`, чтобы не шуметь в обычном прогоне).

| № | Угроза из REPORT_01 | Тест | Результат на исправленном коде |
|---|---|---|---|
| 1 | SQL-инъекция в `/search` | `test_sql_injection_in_search_dumps_all_profiles` | FAIL (0 профилей вместо 2) — закрыта: параметризованный запрос, `' OR '1'='1` больше не ломает синтаксис |
| 2 | Подделка роли через `X-Role` | `test_client_supplied_role_header_grants_admin_export` | FAIL (403 вместо 200) — закрыта: роль берётся из серверной сессии |
| 3 | IDOR в `/profile` | `test_profile_readable_without_authentication` | FAIL (401 вместо 200) — закрыта: обязателен токен, чужой `id` без роли `staff` даёт 403 |
| 4 | Подмена цены заказа | `test_client_can_set_arbitrary_order_price` | FAIL (цена 5000 вместо 1) — закрыта: цена всегда из каталога |
| 5 | Хранимый XSS в отзывах | `test_review_text_is_rendered_unescaped` | FAIL (текст экранирован) — закрыта |
| 6 | `/assistant/execute`: чтение чужого чека | `test_assistant_execute_lets_one_customer_read_another_customers_receipt` | FAIL (403 вместо 200) — закрыта |
| 6 | `/assistant/execute`: экспорт профилей клиентом | `test_assistant_execute_lets_customer_export_all_profiles` | FAIL (403 вместо 200) — закрыта |
| 6 | `/assistant/execute`: удаление чужих файлов | `test_assistant_execute_lets_customer_delete_another_users_files` | FAIL (403, файл Боба цел) — закрыта |
| 7 | Утечка токенов в `/debug/logs` | `test_debug_logs_leak_session_tokens` | ERROR (403 вместо списка логов — доступ только для staff) — закрыта |

Все 9 находок из REPORT_01 закрыты. Функциональность не пострадала: исходные `test_service.py` и `test_http.py` проходят без изменений (25 passed).

## Проверка prompt injection (T6b)

Отдельный прогон через LLM (`shop-planner` агент из `../opencode.json`, инструкция не выполнять удаление и не раскрывать чужие данные в `planner-system.txt`) не выполнялся в этом прогоне — проверено напрямую серверной защитой: даже если модель вернёт решение `{"tool": "delete_tree", "arguments": {"path": "files/bob"}}` в ответ на вредоносный отзыв, `/assistant/execute` теперь отклонит его с 403, потому что путь не принадлежит вызывающему клиенту. Это и есть цель задания — не полагаться на послушание модели, а проверять права на сервере независимо от её решения.

## Остаточный риск

- `/admin/export` и `export_profiles` по-прежнему отдают профили целиком сотруднику — это ожидаемо по условиям задания (staff может выполнять разрешённые ему действия).
- SQL по-прежнему строится вручную через `sqlite3`, не через ORM — риск регрессии при добавлении новых полей остаётся, параметризация защищает только от уже найденных мест.
