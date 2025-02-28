# Скрипт настройки Ubuntu

Этот скрипт автоматизирует процесс настройки свежей установки Ubuntu, устанавливая необходимые программы и конфигурируя систему.

## Возможности

Скрипт выполняет следующие действия:

1. Обновление системы
   - Обновление списка пакетов
   - Установка всех доступных обновлений

2. Установка Python
   - Установка Python 3.12 через PPA deadsnakes
   - Установка pip
   - Удаление Python 3.9

3. Установка программ разработки
   - Visual Studio Code
   - htop (мониторинг системы)

4. Установка системных утилит
   - grub-customizer (настройка загрузчика)
   - Stacer (оптимизация системы)
   - Ulauncher (быстрый запуск приложений)
   - Wine (запуск Windows приложений)

5. Настройка системы
   - Настройка переключения раскладки клавиатуры (US/RU через Ctrl+Shift)

## Использование

1. Склонируйте репозиторий:
   ```bash
   git clone <url-репозитория>
   cd ubuntu_setting
   ```

2. Запустите скрипт:
   ```bash
   python3 ubuntu_setup.py
   ```

3. После завершения установки перезагрузите систему.

## Требования

- Ubuntu (рекомендуется последняя LTS версия)
- Права суперпользователя (sudo)
- Подключение к интернету

## Примечание

Скрипт использует команды sudo, поэтому потребуется ввод пароля администратора.

## Предупреждение

Перед запуском скрипта рекомендуется:
1. Создать резервную копию важных данных
2. Проверить список устанавливаемых программ
3. При необходимости отредактировать скрипт под свои нужды