# coin_keeper_bot
Telegram bot that allows you to control your expenses and incomes


Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/andrewvect/coin_keeper_bot
```
2. Create token in telegram with @botfather

3. Add in file app/config.py configuration settings<br />
   SECRET_KEY <br />
   SQLALCHEMY_DATABASE_URI <br />
   token 

5. Build doker container with command
```bash
docker build -t coin_bot -f Dockerfile.prod .
```
4. Run docker
```bash
docker run -p 5000:5000 coin_bot
```
5. Now your bot can get telegram updates with webhook on
```bash
http://localhost:5000/webhook/  
```

How to use it

Find your bot in telgram, press button start or send /start message.

![img](github/screenshots/screenshot1.jpeg)

1. First you need to create category

![img](github/screenshots/screenshot2.jpeg)

2. Second you need to add subcategory in your created category
![img](github/screenshots/screenshot3.jpeg)

3. That's it. Now you can add values in your created subcategory
![img](github/screenshots/screenshot4.jpeg)

4.You can rename category/subcategory
![img](github/screenshots/screenshot5.jpeg)

5.You can delete category/subcategory
![img](github/screenshots/screenshot6.jpeg)

6.Bot can draw pipe graphic with your data
![img](github/screenshots/screenshot7.jpeg)

7. You can get your data for number of days in category/subcategory
![img](github/screenshots/screenshot8.jpeg)



