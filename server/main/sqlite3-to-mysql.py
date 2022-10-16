import sys
### Sqllite.dump -> mysql.dump
# 해당 파일은 sqllite의 dump파일을 mysql의 dump형식으로 변경해준다
# 실행 명령어 
# cat dump.sql | python sqlite3-to-mysql.py > mysql.sql

### Mysql에 변환한  dump 파일을 넣는다
# mysql> CREATE DATABASE planmon CHARACTER SET utf8mb4;
# mysql> USE planmon;
# mysql> source /path/to/mysql.sql;

def main():
    print("SET sql_mode='NO_BACKSLASH_ESCAPES';")
    lines = sys.stdin.read().splitlines()
    for line in lines:
        processLine(line)

def processLine(line):
    if (
        line.startswith("PRAGMA") or 
        line.startswith("BEGIN TRANSACTION;") or
        line.startswith("COMMIT;") or
        line.startswith("DELETE FROM sqlite_sequence;") or
        line.startswith("INSERT INTO \"sqlite_sequence\"")
       ):
        return
    line = line.replace("AUTOINCREMENT", "AUTO_INCREMENT")
    line = line.replace("DEFAULT 't'", "DEFAULT '1'")
    line = line.replace("DEFAULT 'f'", "DEFAULT '0'")
    line = line.replace(",'t'", ",'1'")
    line = line.replace(",'f'", ",'0'")
    in_string = False
    newLine = ''
    for c in line:
        if not in_string:
            if c == "'":
                in_string = True
            elif c == '"':
                newLine = newLine + '`'
                continue
        elif c == "'":
            in_string = False
        newLine = newLine + c
    print(newLine)

if __name__ == "__main__":
    main()