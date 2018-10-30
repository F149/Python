def is_isogram(text):
    text = text.lower()
    for letter in text:
        if letter.isalpha() and text.count(letter) > 1:
            return False
    return True



