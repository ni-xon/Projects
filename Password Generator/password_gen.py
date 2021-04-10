import random


class passGen:
    def __init__(self):
        self.password = ''
        self.uppercase = [chr(i) for i in range(65, 91)]
        self.lowercase = [chr(i) for i in range(97, 123)]
        self.digits = [chr(i) for i in range(48, 58)]
        self.special = [chr(i) for i in range(33, 40)] + ['*', '+', ',', '.', '/'] + [':', ';', '=', '?', '@', chr(92), '^', '`', chr(126)]
        self.brackets = ['(', ')', '<', '>', '[', ']', '{', '}']

        self.bigger_list = []
        self.bigger_list.append(self.uppercase)
        self.bigger_list.append(self.lowercase)
        self.bigger_list.append(self.digits)
        self.bigger_list.append(self.special)
        self.bigger_list.append(self.brackets)

    def generate(self, length, criteria):
        self.characters_used = []
        for integer in criteria:
            integer = int(integer)
            self.characters_used += self.bigger_list[integer]

        for i in range(length):
            self.password += self.characters_used[random.randint(0, len(self.characters_used))]

        return self.password


if __name__ == '__main__':
    gen = passGen()
    print('=================================== PASSWORD GENERATOR ===================================')
    length = int(input('How long would you like your password to be? '))
    criteria = input('Select the criteria for constructing your password by typing in the number separated by spaces.'
                     '\nFor example, if you want to use upper and lower case, you would input: 0 1 '
                     '\n0. Upper case letters\n1. Lower case letters\n2. Numbers\n3. Special characters\n4. Brackets\n')
    criteria = criteria.split(' ')
    print('Your new password is: ' + '\n' + gen.generate(length, criteria))
    print('===========================================================================================')


# import criteria for generating password: e.g. letters only or numbers # refer to keepass criteria.
