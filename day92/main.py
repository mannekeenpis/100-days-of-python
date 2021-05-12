from twitter_bot import TwitterBot

CHROME_DRIVER_PATH = "/Users/lenargasimov/Development/chromedriver"


def take_input(message):
    s = input(message)
    no_of_images = int(input("How many images do you want to download?: "))
    return (s, no_of_images)


print("===========================")
print("WELCOME TO IMAGE DOWNLOADER")
print("===========================")
print("1. By Username")
print("2. By Hashtag")
print("3. By Search")
choice = int(input("Enter ur choice: "))

bot = TwitterBot(CHROME_DRIVER_PATH)

if choice == 1:
    username, no_of_images = take_input("Enter username: ")
    bot.find_by_username(username, no_of_images=no_of_images)
elif choice == 2:
    hashtag, no_of_images = take_input("Enter hashtag: ")
    bot.find_by_hashtag(hashtag, no_of_images=no_of_images)
elif choice == 3:
    query, no_of_images = take_input("Enter search value: ")
    bot.find_by_search(query, no_of_images=no_of_images)
else:
    print("Invalid choice!")

bot.close()
