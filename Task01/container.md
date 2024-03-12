# Диаграмма C2 - диаграмма контейнеров

![image](https://github.com/EugIva/ProzorovEI109m_ArchitectureInfSys/assets/145147798/1b8139fc-7da2-4dc4-b1e4-3b161b4de1ca)

# Код

```

@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml 

AddElementTag("microService", $shape=EightSidedShape(), $bgColor="CornflowerBlue", $fontColor="white", $legendText="microservice")
AddElementTag("storage", $shape=RoundedBoxShape(), $bgColor="lightSkyBlue", $fontColor="white")

Person(user, "Пользователь")

System_Ext(web_site, "Клиентский веб-сайт", "HTML, CSS, JavaScript, React", "Веб-интерфейс")

System_Boundary(conference_site, "Сайт сервиса доставки") {
   'Container(web_site, "Веб-сайт сервиса доставки", ")
   Container(client_service, "Сервис авторизации", "C++", "Сервис управления пользователями", $tags = "microService")
   Container(users_service, "Сервис пользователей", "C++", "Сервис поиска пользователей", $tags = "microService")
   Container(post_service, "Сервис оформления доставки", "C++", "Сервис создания посылок", $tags = "microService")
   Container(blog_service, "Сервис отслеживания доставки", "C++", "Сервис информирования о доставках пользователя", $tags = "microService")
   ContainerDb(db, "База данных", "MySQL", "Данные пользователей, посылок, доставок", $tags = "storage")

}

Rel(user, web_site, "Регистрация, поиск пользователей, добавление посылки, получение и изменение информации о доставке")

Rel(web_site, client_service, "Создание пользователя", "localhost/person")
Rel(client_service, db, "INSERT/SELECT/UPDATE/DELETE", "SQL")

Rel(web_site, users_service, "Работа с пользователями", "localhost/person")
Rel(users_service, db, "INSERT/SELECT/UPDATE/DELETE", "SQL")

Rel(web_site, post_service, "Работа с доставками", "localhost/pres")
Rel(post_service, db, "INSERT/SELECT/UPDATE/DELETE", "SQL")

Rel(web_site, blog_service, "Информация о доставке", "localhost/conf")
Rel(blog_service, db, "INSERT/SELECT/UPDATE", "SQL")

Rel(users_service, blog_service, "Информация о получателях и отправителях", "localhost/conf")
@enduml

```
