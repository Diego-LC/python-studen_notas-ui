import random
import string

code_str = string.ascii_letters + string.digits
## Imprime 4 letras o números aleatorios
print(''.join(random.sample(code_str,6)))
p = 'asdfsdsd@gmail.com'
print('@' in p or '.c' in p)