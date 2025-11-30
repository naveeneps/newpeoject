def check_password_strength(password):
    if len(password) < 12:
        return False
    elif len(password) >= 12:
        special_characters = "`^!@#$%&*()-_=+[]{};:,<.>/?"
        has_upper = False
        has_lower = False
        has_digit = False
        has_special = False

        for ch in password:
            if ch.isupper():
                has_upper = True
            elif ch.islower():
                has_lower = True
            elif ch.isdigit():
                has_digit = True
            elif ch in special_characters:
                has_special = True

        boolvalues = has_upper and has_lower and has_digit and has_special
        return boolvalues
    else:
        pass


def main():
    password = input("Enter your password: ")
    is_strong = check_password_strength(password)

    if is_strong:
        print(True)
        print("Password is Strong, It adhere to password policy")
    else:
        print(False)
        print("Password is Weak,Please update/change your password")
        print("Your password must meet below criteria(ALFA/NUMRIC/SPECIAL=12 characters):")
        print("--> At least 12 characters")
        print("--> At least one uppercase letter")
        print("--> At least one lowercase letter")
        print("--> At least one digit (0–9)")
        print("--> At least one special character (`^!@#$%&*()-_=+[]{};:,<.>/?)")


if __name__ == "__main__":
    main()
