# ZM TG Event

Спасибо [DanielBorgesOliveira](https://gist.github.com/DanielBorgesOliveira/d3e578e2b677245cec550e965eae1755)

Обернуто в докер для удобства

Переменные окружения

| ENV            | DEFAULT | DESC                                                                                       |
| -------------- | ------- | ------------------------------------------------------------------------------------------ |
| TOKEN          |         | Токен телеграм бота                                                                        |
| ZM_FOLDER      | /zm     | Путь к папке евентов zoneminder                                                            |
| ZM_URL         |         | Публичный урл zoneminder                                                                   |
| LOG_LEVEL      | INFO    | Уровень логов                                                                              |
| FILE_CHAT_PATH | chat_id | Путь к файлу для списка chat_id телеграмма, нужен чтобы рассылка была только для опр чатов |
| CHAT_IDS       |         | Альтернатива файлу                                                                         |
