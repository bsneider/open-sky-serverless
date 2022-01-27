

destination_sql = '''SELECT destination, COUNT(*) AS magnitude 
FROM flight.flightlist 
GROUP BY column 
ORDER BY magnitude DESC
LIMIT 1'''

row_count_sql = '''SELECT Count(1) FROM flight.flightlist'''

max_lastseen = '''SELECT STR_TO_DATE(lastseen, '%Y-%m-%d %H:%i:%s+%TZ') AS max_lastseen 
from flight.flightlist order by 1 desc limit 1;'''
