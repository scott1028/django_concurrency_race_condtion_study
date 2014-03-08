kill -9 $(ps aux | grep python | awk '{print $2}')
./manage.py test
