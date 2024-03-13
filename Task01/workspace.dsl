workspace {
    name "Сервис доставки"

    !identifiers hierarchical


    model {

        properties { 
            structurizr.groupSeparator "/"
        }

        user = person "Пользователь"


        delivery_system = softwareSystem "Сервис доставки" {
            description "Сайс сервиса доставок"

            
            user_service = container "User service" {
                description "Сервис управления пользователями"
            }   

            deliver_service = container "Deliver service" {
                description "Сервис создания и отслеживания доставки"
            } 
            
            post_service = container "Post service" {
                description "Сервис оформления посылок"
            } 

            group "Базы данных" {
                user_database = container "User database" {
                    description "База данных с пользователями"
                    technology "PostgreSQL 15"
                    tags "database"
                }

                deliver_database = container "Deliver database" {
                    description "База данных доставок"
                    technology "MongoDB"
                    tags "database"
                }

                post_database = container "Post database" {
                    description "База данных посылок"
                    technology "MongoDB"
                    tags "database"
                }

                post_database -> deliver_database "Связь между доставками и посылками"
                post_database -> user_database "Связь между пользователями и посылками"

            }


            
            user -> user_service "Регистрация и авторизация"
            user -> deliver_service "Получение и изменение информации о доставке, создание посылки"

            deliver_service -> user_service "Информация о получателях и отправителях"
            deliver_service -> deliver_database "Получение и обновление данных о доставках"
            deliver_service -> post_service "Добавление и информация о посылках" 
            
            user_service -> user_database "Данные о пользователях" 
            
            post_service -> post_database "Хранение и получение информации о посылках"            
        }

        user -> delivery_system "Добавление посылки, Получение и изменение информации о доставке"

    }
    
    views {
        themes default

        properties {
            structurizr.tooltips true
        }

        systemContext delivery_system {
            autoLayout
            include *
        }

        container delivery_system {
            autoLayout
            include *
        }

        dynamic delivery_system "UC01" "Добавление нового пользователя" {
            autoLayout
            user -> delivery_system.user_service "Создание пользователя (POST /user)"
            delivery_system.user_service -> delivery_system.user_database "Сохранение данных о пользователе" 
        }

        dynamic delivery_system "UC02" "Поиск пользователя по логину" {
            autoLayout
            delivery_system.deliver_service -> delivery_system.user_service "Поиск пользователя по логину (GET /user)"
            delivery_system.user_service -> delivery_system.user_database "Получить данные о пользователе"
        }

        dynamic delivery_system "UC03" "Поиск пользователя по маске имя и фамилии" {
            autoLayout
            delivery_system.deliver_service -> delivery_system.user_service "Поиск пользователя по маске имя и фамилии"
            delivery_system.user_service -> delivery_system.user_database "SQL запрос в базу данных"
        }

        dynamic delivery_system "UC04" "Создание посылки" {
            autoLayout
           
            delivery_system.deliver_service -> delivery_system.user_service "Авторизация пользователем"
            delivery_system.deliver_service -> delivery_system.deliver_database "Оформление новой посылки"
        }

        dynamic delivery_system "UC05" "Получение посылок пользователя" {
            autoLayout
            user -> delivery_system.deliver_service "Получение посылок пользователя"
            delivery_system.deliver_service -> delivery_system.user_service "Аутентификация пользователя"
            delivery_system.deliver_service -> delivery_system.deliver_database "Получение доставок"
            delivery_system.deliver_service -> delivery_system.post_service "Получение информации о посылках"
            delivery_system.post_service -> delivery_system.post_database "Получение посылок"
        }

        dynamic delivery_system "UC06" "Создание доставки от пользователя к пользователю" {
            autoLayout
         
            //авторизируемся, создаём доставку, ищем пользователей чтобы заполнить соответствующие поля в доставке
            
            delivery_system.deliver_service -> delivery_system.deliver_database "Получение доставок"
            delivery_system.deliver_service -> delivery_system.user_service "Авторизация пользователем"
            // delivery_system.deliver_database -> delivery_system.deliver_database "Создание доставки"
            delivery_system.deliver_service -> delivery_system.user_service "Поиск пользователя"
            delivery_system.user_service -> delivery_system.user_database "Поиск пользователя"
        }
        
        dynamic delivery_system "UC07" "Получение информации о доставке по получателю" {
            autoLayout
            
            user -> delivery_system.deliver_service "Просмотр информации о доставках"
            delivery_system.deliver_service -> delivery_system.user_service "Авторизация пользователем"
            delivery_system.deliver_service -> delivery_system.user_service "Запрос по конкректному пользователю - получателю"
            delivery_system.user_service -> delivery_system.user_database "Поиск пользователя - получателя"
            delivery_system.deliver_service -> delivery_system.deliver_database "Поиск доставки по получателю"
        }
        
        dynamic delivery_system "UC08" "Получение информации о доставке по отправителю" {
            autoLayout
            
            user -> delivery_system.deliver_service "Просмотр информации о доставках"
            delivery_system.deliver_service -> delivery_system.user_service "Авторизация пользователем"
            delivery_system.deliver_service -> delivery_system.user_service "Запрос по конкректному пользователю - отправителю"
            delivery_system.user_service -> delivery_system.user_database "Поиск пользователя - отправителя"
            delivery_system.deliver_service -> delivery_system.deliver_database "Поиск доставки по отправителю"
        }

        styles {
            element "database" {
                shape cylinder
            }
        }
    }
}