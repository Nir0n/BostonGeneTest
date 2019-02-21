# Requirements
Python 3.7.2

virtualenv

pip
# SetUp
open terminal

commands for terminal below:

git clone https://github.com/man-with-a-plan/BostonGeneTest.git

cd BostonGeneTest/

virtualenv venv

. venv/bin/activate

pip install -r requirements.txt

python manage.py runserver
# Usage
open another terminal

commands for terminal and output below:

curl -X POST '127.0.0.1:8000/submit/?url=http://www.orimi.com/pdf-test.pdf&email=example@gmail.com'

output: "id: 31"

curl -X POST '127.0.0.1:8000/submit/?url=http://www.orimi.com/pdf-test.pdf'

output: "id: 31"

curl -X GET '127.0.0.1:8000/check/?id=31'

output:"state: complete, md5: 2f282b84-e7e6-08d5-8524-49ed940bfc51, url: http://speed.hetzner.de/100MB.bin"

-OR-

output:"state: task failed"

-OR-

output:"state: task in progress"

-OR-

output:"Such id doesn't exist in the system"

# P.S.
The email from which the letters come is called mbeinformer@gmail.com
