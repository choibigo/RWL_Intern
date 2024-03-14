import itertools
from faker import Faker

namee = Faker("ko-KR")
people = [(namee.name()) for i in range(4)]
print(list(itertools.combinations(people, 2)))