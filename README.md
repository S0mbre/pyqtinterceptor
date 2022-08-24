## Установка

```
git clone https://github.com/S0mbre/pyqtinterceptor.git
cd pyqtinterceptor
pip install -r requirements.txt
```

### Сборка EXE для Windows

```
cd pyqtinterceptor
call buildexe.bat
```

После сборки программа `interceptor.exe` появится в директории `/dist/interceptor` вместе с необходимыми библиотеками.

## Запуск

### Из Python
```
python main.py
```

### Запуск EXE
```
./dist/interceptor/interceptor.exe
```

## Обновление

```
cd pyqtinterceptor
git pull
```

## Конфигурация

По умолчанию лог выводится и в консоль, и в файл `log.txt`. 

- Чтобы не выводить лог в консоль, в файле `config.ini` надо установить `debug = false`.
- Чтобы не выводить лог в файл, в файле `config.ini` надо убрать (или закомментировать при помощи "#") строку `logfile = log.txt`
