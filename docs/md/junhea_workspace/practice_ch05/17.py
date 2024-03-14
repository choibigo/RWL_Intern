from faker import Faker
import random
import itertools

namee = Faker("ko-KR")
people = [(namee.name()) for i in range(5)]
work = ['청소', '빨래', '설거지']
random.shuffle(people)
print(list(itertools.zip_longest(people, work, fillvalue='휴식')))