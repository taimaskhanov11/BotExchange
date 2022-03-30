pybabel extract .\botexchange\ -o .\botexchange\apps\bot\locales\botexchange.pot
pybabel init -i .\botexchange\apps\bot\locales\botexchange.pot -d .\botexchange\apps\bot\locales\ -D botexchange -l ru
pybabel init -i .\botexchange\apps\bot\locales\botexchange.pot -d .\botexchange\apps\bot\locales\ -D botexchange -l en
# Собрать переводы
pybabel compile -d .\botexchange\apps\bot\locales\ -D botexchange


Обновляем переводы
1. Вытаскиваем тексты из файлов, Добавляем текст в переведенные версии
# Обновить переводы
pybabel extract .\botexchange\apps\ -o .\botexchange\apps\bot\locales\botexchange.pot
pybabel update -d .\botexchange\apps\bot\locales -D botexchange -i .\botexchange\apps\bot\locales\botexchange.pot
# После перевода
pybabel compile -d .\botexchange\apps\bot\locales\ -D botexchange