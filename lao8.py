import os
import random

from nonebot.exceptions import CQHttpError

from hoshino import R, Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter

_max = 10
EXCEED_NOTICE = f'您今天已经吃过{_max}次了，请明早5点后再来！'
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(5)

sv_help = '''
奥利给 干了 兄弟们，干净又卫生！！
'''.strip()


sv = Service(
    name = 'lao8',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = 'lao8', #属于哪一类
    help_ = sv_help #帮助文本
    )

lao8_folder = R.img('lao8/lao8').path
yongzi_folder = R.img('lao8/yongzi').path

def lao8_gener():
    while True:
        filelist = os.listdir(lao8_folder)
        random.shuffle(filelist)
        for filename in filelist:
            if os.path.isfile(os.path.join(lao8_folder, filename)):
                yield R.img('lao8/lao8/', filename)

def yongzi_gener():
    while True:
        filelist = os.listdir(yongzi_folder)
        random.shuffle(filelist)
        for filename in filelist:
            if os.path.isfile(os.path.join(yongzi_folder, filename)):
                yield R.img('lao8/yongzi/', filename)


lao8_gener = lao8_gener()

yongzi_gener = yongzi_gener()

def get_lao8():
    return lao8_gener.__next__()

def get_yongzi():
    return yongzi_gener.__next__()


@sv.on_prefix(("老八", "来点老八", "来点下饭", "下饭菜"))
async def lao8(bot, ev):
    uid = ev['user_id']
    if not _nlmt.check(uid):
        await bot.send(ev, EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ev, '您吃得太快了，请稍候再吃', at_sender=True)
        return
    _flmt.start_cd(uid)
    _nlmt.increase(uid)

    pic = get_lao8()
    try:
        await bot.send(ev, pic.cqcode)
    except CQHttpError:
        sv.logger.error(f"发送图片{pic.path}失败")
        try:
            await bot.send(ev, '太呕了，发不出去勒...')
        except:
            pass

@sv.on_prefix(("庸子", "来点庸子", "来点刘庸", "来点印度菜", "印度菜"))
async def yongzi(bot, ev):
    uid = ev['user_id']
    if not _nlmt.check(uid):
        await bot.send(ev, EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ev, '您吃得太快了，请稍候再吃', at_sender=True)
        return
    _flmt.start_cd(uid)
    _nlmt.increase(uid)

    pic = get_yongzi()
    try:
        await bot.send(ev, pic.cqcode)
    except CQHttpError:
        sv.logger.error(f"发送图片{pic.path}失败")
        try:
            await bot.send(ev, '太呕了，发不出去勒...')
        except:
            pass
