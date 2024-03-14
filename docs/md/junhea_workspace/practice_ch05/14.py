from faker import Faker
from operator import itemgetter

randd = Faker('ko-KR')
data = [(randd.name(), randd.pyint(min_value=1300, max_value=1800)/100) for i in range(20)]

answer = sorted(data, key=itemgetter(1))
print(answer)