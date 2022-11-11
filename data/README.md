### MongoDB import/export
```sh
mongodump -d vantu -o mongodb
mongorestore --drop mongodb

mongoimport -d vantu -c phrases ../data/with_svg.json
mongoexport -d vantu -c phrases -o export.json
```

### SqLite import
```
python3 ../scripts/sql_import.py
```