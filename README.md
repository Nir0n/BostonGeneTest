# SetUp

# Usage
input: "curl -X POST '127.0.0.1:8000/submit/?url=http://www.orimi.com/pdf-test.pdf&email=example@gmail.com'"

output: "id: 31"

input: "curl -X POST '127.0.0.1:8000/submit/?url=http://www.orimi.com/pdf-test.pdf'"

output: "id: 31"

input: "curl -X GET '127.0.0.1:8000/check/?id=31'"

output:"state: complete, md5: 2f282b84-e7e6-08d5-8524-49ed940bfc51, url: http://speed.hetzner.de/100MB.bin"
-OR-
output:"state: task failed"
-OR-
output:"state: task in progress"
-OR-
output:"Such id doesn't exist in the system"

