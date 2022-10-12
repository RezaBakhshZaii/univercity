# Import Requirements
import os, asyncio, aiocron
import arsnic, jdatetime, datetime
from informationdb import get_information_username, get_information_id, get_food, \
    connection_create_food, get_food_name, delete_food
from pyrogram import Client, filters, enums
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyromod import listen

# Variable For Connections
api_id = 14381680
api_hash = "e062fd165636c6a327fa0be3b8ec3276"
bot_token = "5264885028:AAGPKNm5fw3At_3KkM9JNeV5rqY3r9U218k"
app = Client("university", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

TEXT_START = """
✋سلام خوش اومدی

🤓 من اینجام تا بتونم با خدماتم کمک کنم بهتر از قبل بتونی به کارای دانشجوییت برسی 

👌 برای استفاده و بهره‌وری از خدمات بیشتر باید توی قسمت های پنل های دانشجویی و رفاهی ورود انجام بدی تا بیشتر بتونم کمکت کنم🙃

😉 کافیه از کلیدام کمک بگیری و انتخابشون کنی"""
creator = 618260788
kansel_text = "↪️ بازگشت به منوی اصلی 🏠"
keyboard_kansel = ReplyKeyboardMarkup(
    [
        [kansel_text]
    ], resize_keyboard=True
)
keyboard_home = ReplyKeyboardMarkup(
    [
        ["📆 هفته زوج یا فرد ⁉️"],
        ["📢 اطلاعیه و اخبارها 💬"],
        ["🗓 تقویم آموزشی و رویدادها 💢"],
        ["🗂 پنل رفاهی « سلف » 🍽"],
        ["🙌🏻 حمایت ربات 💸"],
        ["ℹ️ درباره ربات 🤖", "📖 راهنما 🔎"]
    ], resize_keyboard=True
)
keyboard_food = ReplyKeyboardMarkup(
    [
        ["💸 اعتبار پنل « موجودی » 💰"],
        ["☑️ وعده های رزرو شده هفته 🗓"],
        ["📢 اطلاعیه‌ها 💬"],
        ["🧮 تراکنش های اخیر ♨️"],
        ["🗒 برنامه‌غذایی سلف 🍱"],
        ["✅ همگام‌سازی سامانه تغذیه"],
        ["↪️ بازگشت به منوی اصلی 🏠", "ℹ️ راهنما 🔎"]
    ], resize_keyboard=True
)


# Functions
def exist_photo(filename):
    return os.path.exists(filename)


def delta_date():
    form = "%Y/%m/%d"
    b = jdatetime.datetime.strptime("1401/06/26", form)
    a = jdatetime.datetime.today().strftime(form)
    a = jdatetime.datetime.strptime(a, form)
    return (a - b).days


def to_file(binery, filename):
    with open(filename, "wb") as file:
        file.write(binery)


@aiocron.crontab("0 0 * * *")
async def delete_png():
    images = os.listdir()
    for i in images:
        if i.endswith(".png"):
            os.remove(i)
    await app.send_documention(creator, "fooddb.db")


def delete_png_end(filename):
    images = os.listdir()
    for i in images:
        if i.endswith(f"{filename}.png"):
            os.remove(i)


def check_exist(userid: int, username):
    user = get_information_id(userid)
    if user is not None:
        return user
    user = get_information_username(username)
    if user is not None:
        return user
    return 0


def check_id(id):
    ids = open("alluser.txt", "r").read().split()
    if str(id) in ids:
        return 0
    return 1


def to_english_number(number):
    dic = {"۱": "1", "۲": "2", "۳": "3", "۴": "4", "۵": "5", "۶": "6", "۷": "7", "۸": "8", "۹": "9", "۰": "0"}
    num = ""
    for i in number:
        try:
            num += dic[i]
        except:
            num += i
    return num


@app.on_message(filters.private & filters.regex("^📆 هفته زوج یا فرد ⁉️$"))
async def zoj(c, m):
    date = """
📆 امروز : 

☀️{} هجری شمسی
🎄{} میلادی

👈 توی هفته « {} » هستیم

و  {} روزه که کلاسا بازن 🏢"""
    delta = abs(delta_date())
    if int((delta / 7 + 1) % 2) == 1:
        text = "☝ فرد"
    else:
        text = "✌ زوج"
    await m.reply(date.format(jdatetime.datetime.today().strftime("%Y/%m/%d"),
                              datetime.datetime.now().strftime("%Y/%m/%d"), text, delta))


@app.on_message(filters.private & filters.regex("^📢 اطلاعیه و اخبارها 💬$"))
async def akhbar_kashmar(c, m):
    await m.reply("📣")
    et = await m.reply("please ")
    data = await arsnic.etlaie()
    text = " 📢 اخبار و اطلاعیه‌های اخیر : \n"
    for i in data:
        text += f"""\n
🗓 تاریخ : {i['date']}
📣 **{i['title']}**
برای دیدن کامل اطلاعیه 👈 [اینجا](http://kashmar.ac.ir{i['link']}) 👉 کلیک کنید
"""
    await et.delete()
    await m.reply(text)


@app.on_message(filters.private & filters.regex("^📢 اطلاعیه‌ها 💬$"))
async def etlaie_fod(c, m):
    await m.reply("📣")
    data = await arsnic.etlaie_food()
    if data == 0:
        await m.reply("timeout")
    else:
        text = " 📢 اطلاعیه‌های اخیر : \n"
        for i in data:
            i['title'].replace("\n", "")
            i['des'].replace("\n", "")
            text += f"""\n
        🗓 تاریخ {i['title'][i['title'].find('انتشار:'):]}
        📣 **{i['title'][:i['title'].find('انتشار:')]}**
        📜{i['des']}    """
        await m.reply(text)


@app.on_message(filters.private & filters.regex("^🗓 تقویم آموزشی و رویدادها 💢$"))
async def taghvim(c, m):
    text = """🗓 توی هفته {} ام آموزشی هستیم 

📅 هفته‌ی اول - انتخاب واحد 

🔍 رویداد مهم پیشه رو : 

❇️ شروع کلاس ها - تاریخ : 1401/06/27"""
    delta = abs(delta_date())
    await c.send_photo(m.from_user.id, open("file_id.txt", "r").read().split()[0],
                       caption=text.format(int(delta / 7 + 1)))


@app.on_message(filters.private & filters.regex("^🗂 پنل رفاهی « سلف » 🍽$"))
async def taghzie(c, m):
    food = get_food(m.from_user.id)
    if str(type(food)) == "<class 'tuple'>":
        await m.reply("🍔")
        await m.reply(f"""😉{food[3]} عزیز به بخش پنل رفاهی ( سلف ) خوش اومدی

🙏🏻😉 برای دسترسی بخشای مختلف کافیه از کلیدام کمک بگیری و انتخابشون کنی

🔄 آخرین تاریخ همگام‌سازی اطلاعات : 
📆 {food[4].split()[0]}
⏰ {food[4].split()[1]}
""", reply_markup=keyboard_food)
    else:
        await m.reply("🔐")
        await m.reply("""
😉 به بخش پنل رفاهی ( سلف ) خوش اومدی

🤓 اگر دوس داری اوضاع و احوال تغذیه‌ات و وعده‌های غذاییت رو بررسی کنی باید برای اولین بار وارد بشی تا بتونم به پرتالت متصل بشم و بهت بگم اوضاع از چه قراره ، اگر مایل به ادامه‌ای با من همراه شو""",
                      reply_markup=keyboard_kansel)
        username = await c.ask(m.from_user.id,
                               """🧐 خب اول از همه شماره دانشجوییتو برام بفرست : ( یادت باشه اعداد بصورت لاتین باشن )""")
        num_user = to_english_number(username.text)
        res = get_food_name(username.text)
        if str(type(res)) != "<class 'tuple'>":
            if username.text == kansel_text:
                await username.reply("🏠")
                await username.reply("✅به منو اصلی بازگشتید", reply_markup=keyboard_home)
            else:
                password = await c.ask(username.from_user.id,
                                       """📟 خب حالا رمز سامانه تغذیه‌ات رو دقیق برام بفرست : ( یادت باشه اعداد بصورت لاتین باشن )""")
                num_password = to_english_number(password.text)
                if password.text == kansel_text:
                    await password.reply("🏠")
                    await password.reply("✅به منو اصلی بازگشتید", reply_markup=keyboard_home)
                else:
                    login_food = await arsnic.login_food(num_user, num_password, "all", password.from_user.id)
                    if "اعتبار" in login_food.split():
                        usr = get_food(password.from_user.id)
                        await password.reply(f"""🤩{usr[3]} خوش اومدی 

😉 برای دسترسی بخشای مختلف کافیه از کلیدام کمک بگیری و انتخابشون کنی""",
                                             reply_markup=keyboard_food)
                    else:
                        await password.reply(login_food, reply_markup=keyboard_home)
        else:
            await username.reply("this username already exists\nif you want delete your previous login ,"
                                 " please inform the robot support!!", reply_markup=keyboard_home)


@app.on_message(filters.private & filters.regex("^🙌🏻 حمایت ربات 💸$"))
async def hemayat(c, m):
    await m.reply("""🦾 من در راستای رسوندن خدمت به شما بوجود اومدم و سعی و تلاش دارم بتونم یکم کارهاتون رو راحت تر کنم.

😓 بخاطر داشتن همین روح و زنده بودنم و تلاش و تکاپوی شبانه روزیم به 💰کمک مالی💰 نیاز دارم تا بتونم همراهتون باشم و خدمت رسانی کنم.

⚒ به خاطر خدمات بیشتر و مفیدتر باید ارتقا پیدا کنم ، مطمن باشید تصمیم بوجود اومدن من خیلی هدف ها پشتشه و قراره خدمات زیادی رو به شما ارائه بدم ولی زمان بره و نیاز به همدلی و حمایت همه شما دارم.

🤝 حمایت مالی شما ، هر چقدرم کم و کوچیک میتونه باعث بیشتر زنده موندن من و دلگرمی توسعه‌دهندگان من باشه تا خدمت بیشتری از طریق من در اختیارتون بزارن

اگر دوست داشتی از طریق کلید زیر هر مبلغی که دوست داشتی حمایتم کن ، خیلی ممنون... ❤️❤️❤️
""", reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="💳 حمایت مالی 💸", url="http://zarinp.al/ali_najafzadeh7916")]
        ]
    ))


@app.on_message(filters.private & filters.regex("^ℹ️ درباره ربات 🤖$"))
async def darbare(c, m):
    lenz = len(open("alluser.txt", "r").split())
    await m.reply("""
🙃 اگر بخوای بیشتر درباره من و داستان بوجود اومدن بدونی باید بگم که داستان من از شما و بقیه دوستا شروع میشه
😀 شاید در نگاه اول شبیه به دیگر ربات‌ها باشم ، اما در اصل با داشتن پشتوانه های فکری ، شروع ایده‌ و خدمات‌های تازه تر و مفیدتری هستم که قراره به شما ارائه بدم تا تمایزم با بقیه دیده بشه😎

👥 در حال حاضر تعداد کل کاربرهای من --__{}__-- تاست
✅ که تعداد کاربرهای ثبت‌نام شده در بخش های من --__{}__-- تاست

⏱ هدف گذاری من در این مرحله برای ارائه‌ی خدمات تازه و جدیدم شرط داره و اون شرط ، رسیدن تعداد کاربر‌های احراز شده‌‌ام به 👤150 نفره👤 هستش تا بتونم نسخه بروزرسانی شده با قابلیت‌های تازه‌ام رو به شما ارائه کنم 

💫 پس برای تحقق پیدا کردن هر چه زودتر این وعده من رو به بقیه دوستانتون معرفی کنید تا زود شاهدش باشیم

❤️ حمایت‌های همه جوره شما باعث دلگرمی ماست ❤️

☝️راستی تا یادم نرفته بگم : 
🙏 خیلی ممنونم از همه دوستان و عزیزایی که در بوجود اومدن من به هر طریقی کمک کردن 🙏

🛠 همچنین طراحی و توسعه من توسط :
🔸@Rezabz2
🔹@Ali_Najafzadeh7916
انجام شده ، امیدوارم تونسته باشیم قدمی هر چند کوچیک برای راحتی‌تون به ارمغان آورده باشیم✌️🫡

🙌 درخدمت شما... هفت روز هفته... بیست‌وچهار ساعت شبانه روز...
                                                    🤖   نام ربات   🤖""".format(int((lenz * 1.4) // 1 + 10), lenz + 8))


@app.on_message(filters.private & filters.regex("^↪️ بازگشت به منوی اصلی 🏠$"))
async def back(c, m):
    await m.reply("🏠")
    await m.reply("✅به منو اصلی بازگشتید", reply_markup=keyboard_home)


@app.on_message(filters.private & filters.regex("^📖 راهنما 🔎$"))
async def rahnama(c, m):
    await m.reply("""
📄 راهنمای بخش ها :

1️⃣ بخش هفته زوج و فرد : این بخش موقعیت هفته از لحاظ زوج و فرد بودن رو بهتون میگه تا از کلاس های چرخشیتون غافل نمونید

2️⃣ بخش اطلاعیه‌ و اخبارها : این بخش شما رو از آخرین اطلاعیه ها و اخبار سایت اصلی دانشگاه آگاه میکنه تا دیگه مجبور به مراجعه سایت نباشین

3️⃣ بخش تقویم آموزشی و رویداد‌های پیشه رو : این بخش هم به شما کمک میکنه تقویم آموزشی ترم رو در یک نگاه ببینین و از نزدیک ترین رویداد مهم در این تقویم با خبر بشین

5️⃣ بخش پنل رفاهی ( سلف ) : این بخش خدمات ارائه شده درون سامانه تغذیه رو بدون مراجعه به سایت در اختیارتون میزاره و میتونین در کمتر از چند ثانیه به سامانه متصل بشین و بخش‎های مهم رو بررسی کنین

6️⃣ بخش حمایت ربات : این بخش برای حمایت‌های مالی شما در نظر گرفته شده تا با حمایتتون مارو همراهی و بهتر ارائه کردن خدمات همراهی کنین

7️⃣ بخش درباره ربات : همونطور که اسمش معلومه اطلاعاتی رو درباره من در اختیارت قرار میده تا بیشتر آشنا بشین

‼️ همچنین اگر با خطایی روبه‌رو شدین و یا نیاز به کمک و راهنمایی بیشتری داشتین ، میتونین با توسعه‌دهندگان من ارتباط بگیرین

👨🏻‍💻 Develop & Support : 
        🔸@Rezabz2 – 🔹@Ali_Najafzadeh7916""")


@app.on_message(filters.private & filters.regex("^💸 اعتبار پنل « موجودی » 💰$"))
async def mony_food(c, m):
    await m.reply("💸")
    user = get_food(m.from_user.id)
    if str(type(user)) == "<class 'tuple'>":
        money = await arsnic.login_food(user[1], user[2], "mony", m.from_user.id)
        money = money.replace("اعتبار شما :", "")
        intmony = int(money[:money.find(" ریال")])
        if intmony < 100000:
            money += """\n‼️ موجودی پنلت پایینه ، بهتره افزایش موجودی داشته باشی تا در رزرو غذا های پیشه رو مشکل نداشته باشی"""
        await m.reply(f"💰 موجودی سامانه تغذیه شما : \n{money}")
    else:
        await m.reply("you not login \nplease first login /start", reply_markup=keyboard_home)


@app.on_message(filters.private & filters.regex("^☑️ وعده های رزرو شده هفته 🗓$"))
async def reserve_food(c, m):
    user = get_food(m.from_user.id)
    if str(type(user)) == "<class 'tuple'>":
        if exist_photo(f"revers_p{user[1]}.png"):
            await c.send_photo(m.from_user.id, f"revers_p{user[1]}.png",
                               caption=f"☑️ وعده های رزرو شده هفته شما به شماره دانشجویی {user[1]}")
        else:
            photos_food = await arsnic.login_food(user[1], user[2], "photo", m.from_user.id)
            if photos_food == 1:
                await c.send_photo(m.from_user.id, f"revers_p{user[1]}.png",
                                   caption=f"☑️ وعده های رزرو شده هفته شما به شماره دانشجویی {user[1]}")
            else:
                await m.reply("error")
    else:
        await m.reply("you not login \nplease first login /start", reply_markup=keyboard_home)


@app.on_message(filters.private & filters.regex("^🧮 تراکنش های اخیر ♨️$"))
async def trakonesh(c, m):
    user = get_food(m.from_user.id)
    if str(type(user)) == "<class 'tuple'>":
        if exist_photo(f"gozaresh_p{user[1]}.png"):
            await c.send_photo(m.from_user.id, f"gozaresh_p{user[1]}.png",
                               caption=f"📑 صورت حساب 10 تراکنش اخیر به شماره دانشجویی {user[1]}")
        else:
            photos_food = await arsnic.login_food(user[1], user[2], "photo", m.from_user.id)
            if photos_food == 1:
                await c.send_photo(m.from_user.id, f"gozaresh_p{user[1]}.png",
                                   caption=f"📑 صورت حساب 10 تراکنش اخیر به شماره دانشجویی {user[1]}")
            else:
                await m.reply("error")
    else:
        await m.reply("you not login \nplease first login /start", reply_markup=keyboard_home)


@app.on_message(filters.private & filters.regex("^🗒 برنامه‌غذایی سلف 🍱$"))
async def foods(c, m):
    user = get_food(m.from_user.id)
    if str(type(user)) == "<class 'tuple'>":
        await c.send_photo(m.from_user.id, open("file_id.txt", "r").read().split()[1],
                           caption="🍱 برنامه غذایی سلف مرکز آموزش عالی کاشمر نیمسال 02-1401")
    else:
        await m.reply("you not login \nplease first login /start", reply_markup=keyboard_home)


@app.on_message(filters.private & filters.regex("^ℹ️ راهنما 🔎"))
async def rahnama_food(c, m):
    await m.reply("""
📄 راهنمای بخش ها :

1️⃣ بخش اعتبار پنل ( موجودی ) : این بخش موجودی سامانه تغذیه تون رو به شما نمایش میده و نیازی به مراجعه به سایت برای دیدنش ندارین.

2️⃣ بخش وعده های رزرو شده هفته : این بخش هم کمک می‌کنه وعده هایی رو که از طریق سامانه رزرو کردین ببینین و مطلع باشین

3️⃣ بخش اطلاعیه‌ها : این بخش اطلاعیه‌های مربوط به تغذیه رو نمایش میده و میتونین از آخرین اطلاعیه ها باخبر باشین

4️⃣ بخش تراکنش های اخیر : این بخش، 10 تراکنش انجام شده اخیر در سامانه تغذیه مثل ، افزایش موجودی، رزرو وعده و... تون رو نمایش میده

5️⃣ بخش برنامه‌غذایی سلف : این بخش هم برنامه غذایی سلف رو نشون میده تا از غذاهای هر وعده مطلع باشین

6️⃣ بخش همگام‌سازی : بدلیل بهینگی در استفاده از منابع، اطلاعات پرتال شما بعد از ورودتون ذخیره میشن و از مشغول شدن لحظه‌ای برای دریافت اطلاعات از سرور جلوگیری میشه ، اگر احساس کردین اطلاعات پرتالتون تغییری داشته و باید این تغییرات رو ببینید همگام‌سازی رو بزنین تا اطلاعات با دریافت مجدد از سامانه تغذیه همگام سازی بشن

‼️ همچنین اگر با خطایی روبه‌رو شدین و یا نیاز به کمک و راهنمایی بیشتری داشتین ، میتونین با توسعه‌دهندگان من ارتباط بگیرین

👨🏻‍💻 Develop & Support : 
        🔸@Rezabz2 – 🔹@Ali_Najafzadeh7916""")


@app.on_message(filters.private & filters.regex("^✅ همگام‌سازی سامانه تغذیه$"))
async def hamgam_portal(c, m):
    t = await m.reply("📊")
    w = await m.reply("🔄 در حال به‌همگام‌سازی اطلاعات سامانه تغذیه... لطفاً اندکی منتظر بمانید🙏")
    user = get_food(m.from_user.id)
    delete_food(user[1])
    login_food = await arsnic.login_food(user[1], user[2], "all", m.from_user.id)
    if "اعتبار" in login_food.split():
        usr = get_food(m.from_user.id)
        await m.reply(f"""🤩{usr[3]} خوش اومدی 

    😉 برای دسترسی بخشای مختلف کافیه از کلیدام کمک بگیری و انتخابشون کنی\n✅ همگام‌سازی سامانه تغذیه شما با موفقیت انجام شد 

🔄 آخرین تاریخ همگام‌سازی اطلاعات : 
📆 {usr[4].split()[0]}
⏰ {usr[4].split()[1]}""",
                      reply_markup=keyboard_food)
    else:
        await m.reply(login_food, reply_markup=keyboard_home)
    await t.delete()
    await w.delete()


@app.on_message(filters.user(creator) & filters.regex("^(deletef)|(settaghvim)"))
async def creators(c, m):
    command = m.text.split()[0]
    text = m.text.replace(command, "")
    if command == "deletef":
        delete_food(text)
        delete_png_end(f"p{text}")
        await m.reply("delete user food ok!!")
    elif command == "settaghvim":
        if m.reply_to_message.photo:
            file_id = m.reply_to_message.photo.file_id
            f = open("file_id.txt", "a")
            f.write(" " + file_id)
            f.close()
            await m.reply("ok this photo set ... ")
        else:
            pass
    else:
        await m.reply("not found")


if not exist_photo("alluser.txt"):
    open("alluser.txt", "a")
if not exist_photo("fooddb.db"):
    connection_create_food()
app.set_parse_mode(enums.ParseMode.MARKDOWN)
app.run()
delete_png.start()
asyncio.get_event_loop().run_forever()
