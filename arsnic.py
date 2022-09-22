from arsenic import get_session, keys, browsers, services
from arsenic.errors import Timeout
from asyncio import sleep
from informationdb import *
from pyromod import listen

kansel_text = "↪️ بازگشت به منوی اصلی 🏠"


def to_binery(file):
    with open(file, "rb") as phot:
        date = phot.read()
    return date


def to_english_number(number):
    dic = {"۱": "1", "۲": "2", "۳": "3", "۴": "4", "۵": "5", "۶": "6", "۷": "7", "۸": "8", "۹": "9", "۰": "0"}
    num = ""
    for i in number:
        try:
            num += dic[i]
        except:
            num += i
    return num


async def etlaie_food():
    browser = browsers.Firefox(**{'moz:firefoxOptions': {
        'args': ['-headless', '-log', "{'level': 'warning'}", '--no-sandbox']}
    })
    servic = services.Geckodriver(binary="/home/sadlord/Desktop/telegram-bot/univercity/geckodriver")
    async with get_session(servic, browser) as driver:
        try:
            await driver.get('http://self.kashmar.ac.ir')
        except TimeoutError as e:
            return 0
        div = await driver.get_element('div[id=hideNotification]')
        divs = await div.get_elements('div')
        list_element = []
        x = 0
        for i in divs:
            if x == 3:
                break
            if await i.get_attribute('ng-repeat') == 'itm in Notifications':
                await i.click()
                title = await i.get_text()
                di = await i.get_element('div[class=box-body]')
                des = await di.get_text()
                list_element.append({'title': title, 'des': des})
                x += 1
        return list_element


async def etlaie():
    browser = browsers.Firefox(**{'moz:firefoxOptions': {
        'args': ['-headless', '-log', "{'level': 'warning'}", '--no-sandbox']}
    })
    servic = services.Geckodriver(binary="/home/sadlord/Desktop/telegram-bot/univercity/geckodriver")
    async with get_session(servic, browser) as driver:
        await driver.get('http://kashmar.ac.ir/announcements')
        elements = await driver.get_element("section[class=col-md-8]")
        lists = []
        counter = 0
        divs = await elements.get_elements('div')
        for j in divs:
            if await j.get_attribute('class') == 'col-xs-12 col-sm-6 col-md-8':
                elem = {}
                a = await j.get_element('a')
                elem["title"] = await a.get_text()
                elem["link"] = await a.get_attribute('href')
                tarikh = await j.get_text()
                elem["date"] = tarikh.replace(await a.get_text() + "\n\n", "")
                lists.append(elem)
                counter += 1
                if counter == 10:
                    break
        return lists


async def login_food(user, passw, need, userid):
    browser = browsers.Firefox(**{'moz:firefoxOptions': {
        'args': ['-headless', '-log', "{'level': 'warning'}", '--no-sandbox']}
    })
    servic = services.Geckodriver(binary="/home/sadlord/Desktop/telegram-bot/univercity/geckodriver")
    async with get_session(servic, browser) as driver:
        await driver.set_window_size(1800, 1800)
        try:
            await driver.get("http://self.kashmar.ac.ir")
        except Timeout as er:
            return str(er)
        usr = await driver.get_element('input[id=username]')
        await usr.send_keys(str(user))
        pas = await driver.get_element('input[id=password]')
        await pas.send_keys(passw)
        await pas.send_keys(keys.ENTER)
        await sleep(3)
        try:
            alert = await driver.get_elements('div')
            for i in alert:
                if await i.get_attribute('class') == "text-red ng-binding":
                    return await i.get_text()
        except:
            pass
        await driver.get('http://self.kashmar.ac.ir/#!/UserIndex')
        await sleep(40)
        usr_panel = await driver.get_elements('a[class=dropdown-toggle]')
        name_user = await usr_panel[2].get_text()
        if str(type(get_food_name(user))) != "<class 'tuple'>":
            data = [
                (userid, user, passw, name_user)
            ]
            add_food(data)
        if need == "mony":
            return await get_money(driver)
        elif need == "photo":
            await get_gozaresh(driver, user)
            await get_revers(driver, user)
            return 1
        elif need == "all":
            await get_gozaresh(driver, user)
            await get_revers(driver, user)
            return await get_money(driver)


async def get_gozaresh(driver, user):
    await driver.get('http://self.kashmar.ac.ir/#!/Operations')
    await sleep(22)
    all = await driver.get_element('input[id=lstOperations]')
    await all.click()
    inp = await driver.get_element('input[id=txtFromDate]')
    await inp.send_keys('1401/01/01')
    butten = await driver.get_elements('button')
    for i in butten:
        if await i.get_attribute('ng-click') == 'Search()':
            await i.click()
            break
    await sleep(2)
    fort = await driver.get_element('th[class=sorting_asc]')
    await fort.click()
    await sleep(1)
    table_gozaresh = await driver.get_element('table[id=lstOperations]')
    table_gozaresh = await table_gozaresh.get_screenshot()
    with open(f"gozaresh_p{user}.png", "wb") as f:
        table_gozaresh.seek(0)
        f.write(table_gozaresh.read())


async def get_revers(driver, user):
    await driver.get('http://self.kashmar.ac.ir/#!/Reservation')
    await sleep(2)
    revers = await driver.get_element("label[class=text-muted]")
    await revers.click()
    table_revers = await driver.get_element('div[id=tab_Reserved]')
    table_revers = await table_revers.get_screenshot()
    with open(f"revers_p{user}.png", "wb") as f:
        table_revers.seek(0)
        f.write(table_revers.read())


async def get_money(driver):
    mony = await driver.get_element('header[class=main-header]')
    mony = await mony.get_elements("span")
    for u in mony:
        if await u.get_attribute('class') == "navbar-text text-white text-bold col-xs-5 col-md-2 ng-binding":
            return await u.get_text()


async def login(user: str, passw: str, need: str, userid: int, client):
    browser = browsers.Firefox(**{'moz:firefoxOptions': {
        'args': ['-headless', '-log', "{'level': 'warning'}", '--no-sandbox']}
    })
    service = services.Geckodriver(binary="/home/sadlord/Desktop/telegram-bot/univercity/geckodriver")
    async with get_session(service=service, browser=browser) as driver:
        await driver.set_window_size(1800, 1800)
        await driver.get("http://pooya.kashmar.ac.ir/gateway/PuyaAuthenticate.php")
        username = await driver.get_element('input[id=UserID]')
        await username.send_keys(user)
        password = await driver.get_element('input[id=DummyVar]')
        await password.send_keys(passw)
        security = await driver.get_element('img[id=secimg]')
        img = await security.get_screenshot()
        with open(f"security_s{user}.png", "wb") as f:
            img.seek(0)
            f.write(img.read())
        await client.send_photo(userid, f"security_s{user}.png")
        security_cod = await client.ask(userid, """
🔎 این عدد پنج رقمی توی تصویر رو بخون و برام بنویس تا بتونم رد بشم ازش : ( یادت باشه اعداد بصورت لاتین باشن )""")
        sec_code = to_english_number(security_cod.text)
        if security_cod.text == kansel_text:
            return 2
        security_code = await driver.get_element('input[id=mysecpngco]')
        await security_code.send_keys(sec_code)
        await security_code.send_keys(keys.ENTER)
        await sleep(2)
        try:
            alert = await driver.get_elements('div')
            for i in alert:
                if await i.get_attribute('class') == "alert alert-danger text-center":
                    return await i.get_text()
        except:
            pass
        if need == "info":
            await get_info(driver, user, passw, userid)
        elif need == "photo":
            await get_plan_class(driver, user)
            await get_axam(driver, user)
            await get_presence(driver, user)
            await get_numbers(driver, user)
            await get_ok(driver, user)
            if str(type(get_photos(user))) != "<class 'tuple'>":
                photos = [
                    (int(user), to_binery(f"class{user}.png"), to_binery(f"exam{user}.png"),
                     to_binery(f"presence{user}.png"), to_binery(f"numbers{user}.png"),
                     to_binery(f"ok{user}.png"))
                ]
                res = add_photos(photos)
            return 1
        elif need == "all":
            name = await get_info(driver, user, passw, userid)
            pim = await client.send_message(userid, f"اتصال به پرتال {name}\nگرفتن اطلاعات")
            await get_plan_class(driver, user)
            await pim.edit_text(pim.text+"\nگرفتن برنامه درسی")
            await get_axam(driver, user)
            await pim.edit_text(pim.text+"\nگرفتن برنامه امتحانی")
            await get_presence(driver, user)
            await pim.edit_text(pim.text+"\nگرفتن لیست حضور و غیاب")
            await get_numbers(driver, user)
            await pim.edit_text(pim.text+"\nگرفتن لیست نمرات")
            await get_ok(driver, user)
            await pim.edit_text(pim.text+"\nگرفتن تاییدیه درس ها")
            if str(type(get_photos(user))) != "<class 'tuple'>":
                photos = [
                    (int(user), to_binery(f"class_s{user}.png"), to_binery(f"exam_s{user}.png"),
                     to_binery(f"presence_s{user}.png"), to_binery(f"numbers_s{user}.png"),
                     to_binery(f"ok_s{user}.png"))
                ]
                add_photos(photos)
            return 1


async def get_ok(driver, username):
    await driver.get("http://pooya.kashmar.ac.ir/educ/educfac/IssueAck.php")
    table = await driver.get_element('center')
    img = await table.get_screenshot()
    with open(f"ok_s{username}.png", "wb") as f:
        img.seek(0)
        f.write(img.read())


async def get_numbers(driver, username):
    await driver.get("http://pooya.kashmar.ac.ir/educ/educfac/stuShowEducationalLogFromGradeList.php")
    table = await driver.get_element('center')
    img = await table.get_screenshot()
    with open(f"numbers_s{username}.png", "wb") as f:
        img.seek(0)
        f.write(img.read())


async def get_presence(driver, username):
    await driver.get("http://pooya.kashmar.ac.ir/educ/stu_portal/AbsReport.php")
    table = await driver.get_element('center')
    img = await table.get_screenshot()
    with open(f"presence_s{username}.png", "wb") as f:
        img.seek(0)
        f.write(img.read())


async def get_axam(driver, username):
    await driver.get("http://pooya.kashmar.ac.ir/educ/stu_portal/ShowStExamDays.php")
    table = await driver.get_element('table')
    img = await table.get_screenshot()
    with open(f"exam_s{username}.png", "wb") as f:
        img.seek(0)
        f.write(img.read())


async def get_plan_class(driver, username):
    await driver.get("http://pooya.kashmar.ac.ir/educ/educfac/ShowStSchedule.php")
    table = await driver.get_element('div[class=row]')
    img = await table.get_screenshot()
    with open(f"class_s{username}.png", "wb") as f:
        img.seek(0)
        f.write(img.read())


async def get_info(browser, username, password, userid):
    await browser.get(url="http://pooya.kashmar.ac.ir/educ/educfac/ShowStSpec.php")
    infors = await browser.get_elements('tr[class=alert-info]')
    list_word = ["شماره دانشجو :", "نام و نام خانوادگی :", "رشته :", "دوره :", "معدل آخرین ترم :", ""]
    info = []
    for i in infors:
        td = await i.get_elements('td')
        for j in td:
            text = await j.get_text()
            if text[:text.find(":") + 1] in list_word:
                info.append(text)
    image = await browser.get_element('img')
    image = await image.get_screenshot()
    with open(f"image_s{username}.png", "wb") as img:
        image.seek(0)
        img.write(image.read())
    await browser.get("http://pooya.kashmar.ac.ir/educ/stu_portal/ChangeAddress.php")
    mobil = await browser.get_element('input[id=mobile]')
    mobil = await mobil.get_attribute('value')
    await browser.get("http://pooya.kashmar.ac.ir/educ/stu_portal/ChangeNationalCode.php")
    meli = await browser.get_element('input[id=nid]')
    meli = await meli.get_attribute('value')
    info.append(mobil)
    info.append(meli)
    if str(type(get_information_username(username))) != "<class 'tuple'>":
        data = [
            (userid, username, password, info[1], info[2], info[3], info[4], info[5], info[6],
             to_binery(f"image_s{username}.png"))
        ]
        add_student(data)
    return info[1]


async def driver_close(driver):
    await driver.close()
