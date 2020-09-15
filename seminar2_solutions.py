#1 Выведите элементы из a , которые есть в b
### input
a = [0, 1, 2, 3, 4, 5]
b = [3, 4, 5] 

### solution
print([x for x in a if x in b])


#2 Создайте новый массив с уникальными значениями
### input
a = [0, 0, 1, 1, 2, 2]

### solution
s = set()
_ = [s.add(x) for x in a]
s = list(s)
print(s)


#3 Создайте новый массив с четными элементами (ноль считаем нечётным)
### input
a = [0, 1, 2, 3, 4, 5]

### solution
b = [x for x in a if not x%2 and x > 0]
print(b)

#4 Создайте словарь из массива, где ключ — индекс элемента.
### input
a = ['foo', 'bar', 'baz']

### solution
b = {k:v for k,v in enumerate(a)}
print(b)


#5 Распечатайте приветствия.
### input
a = ['John', 'Allison', 'Brian', 'Claire', 'Andrew']

### solution
_ = [print(f'Hi, {name} \n') for name in a]


#6 Распечатайте элементы массива a, которые отсутствуют в b .
### input
a = ['foo', 'bar', 'baz', 'egg']
b = ['bar', 'baz']

### solution
_ = [print(f'{name} отсутствует!\n') for name in a if name not in b]


#7 Склейте два массива — результат отсортированный массив
### input
a = [0, 1, 2, 6, 7, 8]
b = [3, 4, 5]

### solution
i, j = 0, 0
len_a, len_b = len(a), len(b)
c = [0]*(len_a+len_b)

while i + j < len_a + len_b:
    if j == len_b or (i < len_a and a[i] < b[j]):
        c[i + j] = a[i]
        i += 1
    else:
        c[i + j] = b[j]
        j += 1
print(c)


#8 Создайте новый словарь из a с отсортированными ключами в обратном порядке
### input
a = {0: 'foo', 1: 'bar', 2: 'baz'}

### solution
b = {t[1]:t[0] for t in list(a.items())[::-1]}
print(b)
