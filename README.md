# urllogpass_sorter
Данный скрипт предназначен исключительно для использования свои личных данных, автор скрипта ни в коем случае не поддерживает использование скрипта в корыстных целях
Update list
v0.1
Есть drag and drop [Пока только папка, потом добавлю для отдельных файлов]
Парсинг ключевых слов
Парсинг всего
Есть возможность сохранить всё что спарсило как в один файл так и сортировать по email:password/login:password/number:password
Проверка осуществлена через регулярные выражения
v0.2
Улучшен парсинг благодаря чтению файла блоками и записи строк в словари с последующей записью в файл что ускоряет обработку файла в отличии от построчной записи в файл с гонкой за ресурсы
Оптимизированы регулярные выражения
Очистка словарей после каждого обработанного файла что уменьшает нагрузку на озу
Добавлен парсинг плохих строк
Добавлен вывод результатов обработки каждого файла (кол-во mail:pass/login:pass/number:pass, кол-во строк и вес файла)
Перед записью словари очищаються от дублей
v0.3
Улучшена проверка строк через регулярные выражения
Добавлен кастомный выбор мб в блоке
Добавлен вывод скорости обработки и колличество обработанных данных в mb
v0.4
Улучшена проверка строк через регулярные выражения
Оптимизация подсчёта mail:pass/login:pass/number:pass
