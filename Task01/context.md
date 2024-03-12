# Контекст решения

![structurizr-SystemContext-001-001](https://github.com/EugIva/ProzorovEI109m_ArchitectureInfSys/assets/145147798/c2ad7a31-8da1-46b6-8090-fa134517eec5)

# Код
```
workspace {

    model {
        user = person "Пользователь"
        softwareSystem = softwareSystem "Сайт сервиса доставки" {
            webapp = container "Web Application" {
                user -> this "Регистрация, поиск пользователей, добавление посылки, получение и изменение информации о доставке"
            }
            container "Database" {
                webapp -> this "Reads from and writes to"
            }
        }
    }

    views {
        systemContext softwareSystem {
            include *
            autolayout lr
        }

        container softwareSystem {
            include *
            autolayout lr
        }

        theme default
    }

}
```
