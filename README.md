# EntityLinkToolBackend
## 常用命令
## docker启动
sudo docker-compose up -d  
sudo docker-compose up
## 更新代码后重新安装环境
sudo docker-compose up --build -d
## 进入容器命令行
sudo docker-compose exec web sh    
sudo docker-compose exec mysql sh
## 查看容器状态
sudo docker ps
## django配置数据库
python manage.py makemigrations  
python manage.py migrate
## 导入数据
python loadkb.py  
python loadtrainingset.py
## 生成excel
python makeexcel.py
## 启动django
python manage.py runserver
## mysql命令
mysqlsh --user root --host localhost --port 3306
## 数据库迁移的问题
不行的话直接删库。。。。然后创建个空的重新导入数据