my_list = [3, 5, 7, 8, 10.5]
print(my_list)
my_list.append('Python')
print(my_list)
print(len(my_list))

print(my_list[0])
print(my_list[-1])
print(my_list[1:5])
my_list.remove('Python')
print(my_list)

my_dict = {
	'city': "Москва",
	'temperature': 20,
}
print(my_dict['city'])
my_dict['temperature'] -= 5
print(my_dict)
print(my_dict.get('country'), 'Россия')
my_dict['date'] = '27.05.2019'
print(len(my_dict))
print(my_dict)