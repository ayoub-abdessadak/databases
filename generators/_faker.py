from faker import Faker

faker = Faker("nl_NL")
print(faker.first_name(), faker.last_name())