Написать docker compose, в котором работают: 
1. web приложение, на FastApi. 
У приложения должно быть несколько ендпоинтов: 
+ GET 'api/v1/messages/' показывает спосиок всех сообщений;
+ POST 'api/v1/message/' позволяет написать сообщение; 
2. Веб сервер должен быть Nginx. 
3. mongo как бд для сообщений. 
4. Телеграм бот (aiogram3), который показывает сообщения и позволяет создать сообщение 
3самому. 

Будет плюсом: 
+  Добавление кэширования при помощи Redis (кеш стирается, 
когда появляется новое сообщение) 
+ Развертывание на удалённом сервере и добавление ssl через certbot. 
+ Реализовать код так, чтобы было видно, кто написал сообщение. 
+ Добавление пагинации. 

Проект залить на Github с подробно описанным Readme