#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

python3 -m venv env
source ./env/bin/activate
pip3 install -r api/requirements.txt
python3 api/manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python3 api/manage.py shell
python3 api/manage.py runserver
