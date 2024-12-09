import pyotp
import getpass
import qrcode

# Створюємо секретний ключ для TOTP
secret_key = pyotp.random_base32()  # Цей ключ потрібно зберігати безпечно!
totp = pyotp.TOTP(secret_key)

otp_uri = pyotp.totp.TOTP(secret_key).provisioning_uri(
    name='kyrylbarabash@gmail.com', issuer_name='MySecureApp'
)

# Створюємо QR-код
qr = qrcode.make(otp_uri)
qr.save(open('test_qrcode.png', '+wb'))

print(f'Ваш секретний ключ для MFA (зберігайте його безпечно!): {secret_key}')
print(f'Ваш одноразовий код (тільки для перевірки роботи): {totp.now()}')


# Імітуємо базу даних користувачів
user_data = {'username': 'admin', 'password': 'admin', 'mfa_key': secret_key}


def authenticate_user(username, password):
    """Перевірка основного фактора (пароля)"""
    return user_data['username'] == username and user_data['password'] == password


def verify_mfa_code(mfa_key, code):
    """Перевірка другого фактора (TOTP-коду)"""
    totp = pyotp.TOTP(mfa_key)
    return totp.verify(code)


# Логіка входу
def login():
    print('Ласкаво просимо! Виконайте аутентифікацію.')

    # Основний фактор: перевірка пароля
    username = input("Введіть ім'я користувача: ")
    password = getpass.getpass('Введіть пароль: ')  # Пароль не відображається

    if not authenticate_user(username, password):
        print("Невірне ім'я користувача або пароль.")
        return False

    # Другий фактор: перевірка TOTP
    mfa_code = input('Введіть одноразовий код із додатку: ')
    if not verify_mfa_code(user_data['mfa_key'], mfa_code):
        print('Невірний одноразовий код.')
        return False

    print('Успішна аутентифікація!')
    return True


# Виклик функції входу
if __name__ == '__main__':
    login()
