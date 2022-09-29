def process_message(msg):
    if "biletik" in msg:
        words = msg.split(" ")
        pos = words.index("biletik")
        if pos != -1 and pos + 1 < len(words):
            user = words[pos + 1]
            return user
    return None
