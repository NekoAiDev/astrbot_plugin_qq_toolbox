"""
AstrBot QQ 功能工具箱
娱乐 / 实用查询 / 内容生成 / 群管工具
作者: 小红蛋
"""

import random
import hashlib
import time
import datetime
from pathlib import Path
from io import BytesIO

import httpx
from PIL import Image, ImageDraw, ImageFont
import qrcode

from astrbot.api.event import filter, AstrMessageEvent, EventMessageType
from astrbot.api.star import Star, register, Context
from astrbot.api import AstrBotConfig
from astrbot.api.logger import logger


@register(
    "astrbot_plugin_qq_toolbox",
    "小红蛋",
    "QQ 功能工具箱：娱乐、实用查询、内容生成、群管工具，20+ 指令一站式集成",
    "1.0.0",
    "https://github.com/xiaohondan/astrbot_plugin_qq_toolbox",
)
class QQToolbox(Star):
    """QQ 功能工具箱主类"""

    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        # 复读机状态 {group_id: {"last_msg": str, "count": int}}
        self.repeater_state: dict = {}
        # 猜数字游戏 {user_id: {"target": int, "attempts": int, "max": int}}
        self.guess_games: dict = {}
        # 摇一摇冷却 {user_id: float}
        self.shake_cooldown: dict = {}

    # ==================== 工具方法 ====================

    def _get_conf(self, key: str, default=None):
        """安全读取配置项"""
        try:
            plugin_conf = self.config.get("astrbot_plugin_qq_toolbox", {})
            if isinstance(plugin_conf, dict):
                return plugin_conf.get(key, default)
        except Exception:
            pass
        return default

    def _get_user_id(self, event: AstrMessageEvent) -> str:
        """获取用户唯一标识"""
        try:
            return str(event.get_sender_id())
        except Exception:
            return "unknown"

    def _get_group_id(self, event: AstrMessageEvent) -> str:
        """获取群组标识"""
        try:
            return str(event.get_group_id())
        except Exception:
            return ""

    def _is_group(self, event: AstrMessageEvent) -> bool:
        """判断是否在群聊中"""
        return bool(self._get_group_id(event))

    def _daily_hash(self, user_id: str, salt: str = "") -> int:
        """基于用户ID和日期的每日固定随机数种子"""
        today = datetime.date.today().isoformat()
        seed_str = f"{user_id}_{today}_{salt}"
        h = hashlib.md5(seed_str.encode()).hexdigest()
        return int(h, 16)

    async def _fetch_json(self, url: str, timeout: float = 10.0) -> dict:
        """安全 GET 请求 JSON"""
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.get(url, follow_redirects=True)
            r.raise_for_status()
            return r.json()

    # ==================== 娱乐趣味 ====================

    @filter.command("毒鸡汤")
    async def _(self, event: AstrMessageEvent):
        """随机毒鸡汤"""
        soups = [
            "只要你每天坚持早起，就会发现……真的起不来。",
            "努力不一定成功，但不努力真的好轻松。",
            "比你优秀的人还在努力，那你努力还有什么用。",
            "不要看别人表面上一帆风顺，实际上他们背地里……也是一帆风顺。",
            "有时候你不努力一下，都不知道什么叫绝望。",
            "失败并不可怕，可怕的是你还相信这句话。",
            "生活不止眼前的苟且，还有读不懂的诗和到不了的远方。",
            "当你觉得自己又丑又穷的时候，不要难过，至少你的判断是对的。",
            "上帝为你关上了一扇门，还会顺手帮你把窗户也关上。",
            "别灰心，人生就是这样起起落落落落落落的。",
            "有时候你不努力一下，就不知道什么叫绝望。",
            "虽然你单身，但是你胖若两人啊。",
            "你以为只要长得漂亮就有男生喜欢？对不起，这是真的。",
            "别人都在假装正经，那我就只有假装不正经了。",
            "好人成佛需要九九八十一难，坏人只需要放下屠刀。",
            "你只看到别人在表面上活得春风得意，却不知道人家在背地里也是……过得有滋有味。",
            "当你觉得整个世界都在背弃你的时候，请相信，她真的在背弃你。",
            "不要给自己太大压力，毕竟连空气都有重量。",
            "人生就像愤怒的小鸟，当你失败时，总有几头猪在笑。",
            "你以为岁月静好，其实是有人在替你负重前行。",
        ]
        yield event.plain_result(random.choice(soups))

    @filter.command("彩虹屁")
    async def _(self, event: AstrMessageEvent):
        """随机彩虹屁"""
        praises = [
            "你的才华简直溢出屏幕了！",
            "你这个人除了好看，还有什么是没有的？哦，还有才华。",
            "和你聊天感觉整个人都被净化了。",
            "你是我见过最聪明的人，不接受反驳。",
            "你的存在就是这世界上最美好的事情。",
            "你笑起来的样子真好看，像春天的花一样。",
            "你是不是吃了什么仙丹？怎么能这么优秀。",
            "如果优秀是一种病，你一定是病入膏肓了。",
            "每天能看到你的消息就是我最大的快乐。",
            "你这么厉害，干脆把天花板也一起封了吧。",
            "你简直就是行走的百科全书，什么都知道！",
            "你的品味真好，和你在一起总能学到很多。",
            "认识你之后，我的世界都变得不一样了。",
            "你就是传说中的宝藏男孩/女孩吧！",
            "你的发言简直就是教科书级别的，建议出版。",
        ]
        yield event.plain_result(random.choice(praises))

    @filter.command("土味情话")
    async def _(self, event: AstrMessageEvent):
        """随机土味情话"""
        quotes = [
            "你知道你和星星的区别吗？星星在天上，你在我心里。",
            "我怀疑你是一本书，不然为什么让我越看越想睡。",
            "你今天有点怪，怪好看的。",
            "你知道我的缺点是什么吗？缺点你。",
            "你闻到什么味道了吗？没有啊。怎么你一出来空气都是甜的。",
            "我想在你那里买一块地。买什么地？买你的死心塌地。",
            "你是什么血型？你是我的理想型。",
            "我最近想去配个眼镜，因为我发现除了你什么也看不清。",
            "你的脸上有点东西。有什么？有点好看。",
            "我对你的感情就像拖拉机上山，轰轰烈烈。",
            "你知道为什么我最近没找你吗？因为我在找你。",
            "我有一份关于你的文件，要不要看看？什么文件？我的心愿单。",
            "你今天特别讨厌，讨人喜欢和百看不厌。",
            "你知道你和猴子有什么区别吗？猴子住在树上，你住在我心里。",
            "你是不是电脑病毒？因为你不在我脑子里的时候，我的脑子就坏了。",
        ]
        yield event.plain_result(random.choice(quotes))

    @filter.command("抽签")
    async def _(self, event: AstrMessageEvent):
        """随机抽签，每天结果固定"""
        user_id = self._get_user_id(event)
        if self._get_conf("fortune_seed_by_user", True):
            seed = self._daily_hash(user_id, "omikuji")
            idx = seed % 7
        else:
            idx = random.randint(0, 6)

        results = [
            ("大吉", 100, "万事如意，心想事成！今天是你的幸运日！"),
            ("中吉", 80, "运势不错，努力会有回报！"),
            ("小吉", 60, "平稳顺利，保持好心态。"),
            ("吉", 50, "还不错，继续加油！"),
            ("末吉", 40, "稍有波折但终会顺利。"),
            ("凶", 30, "今天宜静不宜动，注意休息。"),
            ("大凶", 20, "别担心，倒霉到极致就是转运的开始！"),
        ]
        name, score, desc = results[idx]
        yield event.plain_result(f"今日签运: {name}（运势指数: {score}/100）\n{desc}")

    @filter.command("运势")
    async def _(self, event: AstrMessageEvent):
        """今日运势详情"""
        user_id = self._get_user_id(event)
        seed = self._daily_hash(user_id, "fortune")

        aspects = [
            ("综合运势", ["极好", "很好", "不错", "一般", "较差"]),
            ("爱情运势", ["桃花运爆棚", "甜蜜满满", "小有暧昧", "波澜不惊", "独自美丽"]),
            ("事业学业", ["灵感爆发", "效率拉满", "稳步前行", "平平无奇", "摸鱼的一天"]),
            ("财富运势", ["偏财运极佳", "小有进账", "收支平衡", "破财预警", "钱包哭泣"]),
            ("健康运势", ["元气满满", "精力充沛", "状态良好", "注意休息", "早点睡觉"]),
        ]
        lines = [f"今日运势 — {datetime.date.today().strftime('%m月%d日')}\n"]
        for i, (name, levels) in enumerate(aspects):
            idx = (seed >> (i * 4)) % len(levels)
            stars = "★" * (5 - idx) + "☆" * idx
            lines.append(f"  {name}: {levels[idx]} {stars}")
        tips = [
            "今天适合大胆尝试新事物",
            "给重要的人发条消息吧",
            "出门走走运气会更好",
            "今天适合早睡早起",
            "记得喝水保持好心情",
            "今天的学习效率会很高",
            "适合整理房间换换风水",
            "今天适合做顿好吃的犒劳自己",
        ]
        lines.append(f"\n幸运提示: {random.choice(tips)}")
        yield event.plain_result("\n".join(lines))

    @filter.command("骰子")
    async def _(self, event: AstrMessageEvent, expr: str = ""):
        """掷骰子，支持 ndm 格式，如: /骰子 2d6"""
        count, sides = 1, 6
        if expr:
            try:
                expr = expr.strip().lower().replace(" ", "")
                if "d" in expr:
                    parts = expr.split("d")
                    count = int(parts[0]) if parts[0] else 1
                    sides = int(parts[1])
                else:
                    sides = int(expr)
                count = max(1, min(count, 20))
                sides = max(2, min(sides, 100))
            except (ValueError, IndexError):
                count, sides = 1, 6

        results = [random.randint(1, sides) for _ in range(count)]
        total = sum(results)
        if count == 1:
            yield event.plain_result(f"掷骰子: {total}")
        else:
            detail = " + ".join(str(r) for r in results)
            yield event.plain_result(f"掷 {count}d{sides}: {detail} = {total}")

    @filter.command("抛硬币")
    async def _(self, event: AstrMessageEvent):
        """抛硬币"""
        user_id = self._get_user_id(event)
        if user_id and self._get_conf("fortune_seed_by_user", True):
            seed = self._daily_hash(user_id, "coin")
            result = "正面" if seed % 2 == 0 else "反面"
        else:
            result = random.choice(["正面", "反面"])
        yield event.plain_result(f"抛硬币结果: {result}")

    @filter.command("摇一摇")
    async def _(self, event: AstrMessageEvent):
        """摇一摇，随机选人（群聊可用）"""
        if not self._is_group(event):
            yield event.plain_result("该功能仅在群聊中可用哦~")
            return

        user_id = self._get_user_id(event)
        now = time.time()
        if user_id in self.shake_cooldown and now - self.shake_cooldown[user_id] < 30:
            remain = int(30 - (now - self.shake_cooldown[user_id]))
            yield event.plain_result(f"摇一摇冷却中，{remain} 秒后再试~")
            return

        self.shake_cooldown[user_id] = now
        comments = [
            "被选中了！命运的齿轮开始转动！",
            "恭喜被摇中！今天的幸运儿就是你！",
            "命运的骰子指向了你！",
            "叮~ 你被随机点名了！",
            "摇一摇，摇到你就是天意！",
        ]
        yield event.plain_result(
            f"摇一摇！随机选人中……\n"
            f"\n{random.choice(comments)}\n"
            f"提示: 请被选中的朋友出来冒个泡吧！"
        )

    @filter.command("猜数字")
    async def _(self, event: AstrMessageEvent, action: str = ""):
        """猜数字游戏，/猜数字 start 开始，/猜数字 <数字> 猜"""
        user_id = self._get_user_id(event)

        # 正在进行中的游戏
        if user_id in self.guess_games:
            game = self.guess_games[user_id]

            if not action or action == "start":
                yield event.plain_result(
                    f"猜数字游戏进行中\n"
                    f"范围: 1-{game['max']}\n"
                    f"已猜: {game['attempts']} 次\n"
                    f"输入 /猜数字 <数字> 开始猜！\n"
                    f"输入 /猜数字 start 重新开始"
                )
                return

            # 猜数字
            try:
                guess = int(action)
            except ValueError:
                yield event.plain_result("请输入一个有效的数字！")
                return

            game["attempts"] += 1
            target = game["target"]

            if guess == target:
                attempts = game["attempts"]
                self.guess_games.pop(user_id, None)
                if attempts <= 3:
                    rating = "天才！"
                elif attempts <= 5:
                    rating = "厉害！"
                elif attempts <= 8:
                    rating = "不错！"
                else:
                    rating = "终于猜到了！"
                yield event.plain_result(
                    f"恭喜你猜对了！答案就是 {target}！\n"
                    f"共用了 {attempts} 次 — {rating}\n"
                    f"输入 /猜数字 start 开始新一局"
                )
            elif guess < target:
                yield event.plain_result(
                    f"{guess}？再大一点\n已猜 {game['attempts']} 次，继续加油！"
                )
            else:
                yield event.plain_result(
                    f"{guess}？再小一点\n已猜 {game['attempts']} 次，继续加油！"
                )
            return

        # 开始新游戏
        if action == "start":
            target = random.randint(1, 100)
            self.guess_games[user_id] = {"target": target, "attempts": 0, "max": 100}
            yield event.plain_result(
                f"猜数字游戏开始！\n"
                f"范围: 1-100\n"
                f"输入 /猜数字 <数字> 来猜\n"
                f"输入 /猜数字 start 随时重新开始"
            )
        else:
            yield event.plain_result(
                "猜数字游戏\n输入 /猜数字 start 开始游戏"
            )

    @filter.command("复读")
    async def _(self, event: AstrMessageEvent, content: str = ""):
        """复读一句话，/复读 <内容>"""
        if not content:
            yield event.plain_result("请输入要复读的内容，如: /复读 你好世界")
            return
        yield event.plain_result(content)

    # ==================== 实用查询 ====================

    @filter.command("天气")
    async def _(self, event: AstrMessageEvent, city: str = ""):
        """查询天气，/天气 [城市英文名]，如: /天气 Tokyo"""
        if not city:
            city = self._get_conf("weather_city_default", "Beijing")

        try:
            data = await self._fetch_json(
                f"https://wttr.in/{city}?format=j1&lang=zh", timeout=15
            )
            cur = data.get("current_condition", [{}])[0]
            desc_list = cur.get("lang_zh", [{}])
            desc = desc_list[0].get("value", cur.get("weatherDesc", [{}])[0].get("value", "未知"))
            temp = cur.get("temp_C", "??")
            feels = cur.get("FeelsLikeC", "??")
            humidity = cur.get("humidity", "??")
            wind = cur.get("windspeedKmph", "??")
            vis = cur.get("visibility", "??")

            result = (
                f"天气查询 — {city}\n"
                f"{'='*20}\n"
                f"当前温度: {temp}°C（体感 {feels}°C）\n"
                f"天气状况: {desc}\n"
                f"湿度: {humidity}%\n"
                f"风速: {wind}km/h\n"
                f"能见度: {vis}km"
            )
            yield event.plain_result(result)
        except Exception as e:
            logger.error(f"天气查询失败: {e}")
            yield event.plain_result("查询天气失败，请检查城市名是否正确。\n示例: /天气 Beijing")

    @filter.command("黄历")
    async def _(self, event: AstrMessageEvent):
        """今日黄历宜忌"""
        today = datetime.date.today()
        year, month, day = today.year, today.month, today.day

        seed = self._daily_hash("huangli_global", str(today))
        random.seed(seed)

        good_things = [
            "嫁娶", "搬家", "开业", "出行", "交易", "签约", "面试",
            "约会", "学习", "运动", "购物", "聚会", "写代码", "摸鱼",
            "发朋友圈", "读书", "整理房间", "联系老友", "规划未来", "烘焙",
        ]
        bad_things = [
            "跳槽", "表白", "借钱", "网购", "熬夜", "吵架", "迟到",
            "吃辣", "看恐怖片", "翻老照片", "称体重", "打排位",
            "考驾照", "洗车", "晒被子", "吃路边摊",
        ]

        random.shuffle(good_things)
        random.shuffle(bad_things)

        lucky_num = random.randint(1, 99)
        lucky_color = random.choice(["红色", "橙色", "金色", "绿色", "蓝色", "紫色"])
        direction_map = ["东", "南", "西", "北", "东南", "东北", "西南", "西北"]
        lucky_dir = direction_map[random.randint(0, 7)]
        star_map = ["水瓶座", "双鱼座", "白羊座", "金牛座", "双子座", "巨蟹座",
                     "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座"]
        star_idx = (month * 2 + day) % 12
        star = star_map[star_idx]

        random.seed()  # 重置随机种子

        result = (
            f"老黄历 — {year}年{month}月{day}日\n"
            f"{'='*24}\n"
            f"宜: {'、'.join(good_things[:5])}\n"
            f"忌: {'、'.join(bad_things[:5])}\n"
            f"{'='*24}\n"
            f"幸运数字: {lucky_num}\n"
            f"幸运颜色: {lucky_color}\n"
            f"幸运方位: {lucky_dir}\n"
            f"今日星座: {star}"
        )
        yield event.plain_result(result)

    @filter.command("汇率")
    async def _(self, event: AstrMessageEvent, from_cur: str = "", to_cur: str = "CNY"):
        """查询汇率，/汇率 USD CNY"""
        if not from_cur:
            yield event.plain_result(
                "汇率查询\n"
                "用法: /汇率 <源货币> <目标货币>\n"
                "示例: /汇率 USD CNY\n"
                "常见: USD EUR GBP JPY KRW CNY"
            )
            return

        try:
            data = await self._fetch_json(
                f"https://api.exchangerate-api.com/v4/latest/{from_cur.upper()}", timeout=10
            )
            rates = data.get("rates", {})
            rate = rates.get(to_cur.upper())
            if not rate:
                yield event.plain_result(f"未找到 {from_cur.upper()} -> {to_cur.upper()} 的汇率")
                return
            yield event.plain_result(
                f"汇率查询\n"
                f"{'='*20}\n"
                f"1 {from_cur.upper()} = {rate:.4f} {to_cur.upper()}\n"
                f"1 {to_cur.upper()} = {1/rate:.4f} {from_cur.upper()}\n"
                f"更新时间: {data.get('date', '未知')}"
            )
        except Exception as e:
            logger.error(f"汇率查询失败: {e}")
            yield event.plain_result("汇率查询失败，请稍后重试。")

    @filter.command("查IP")
    async def _(self, event: AstrMessageEvent, ip: str = ""):
        """查询IP归属地，/查IP 8.8.8.8"""
        if not ip:
            yield event.plain_result(
                "IP 归属地查询\n"
                "用法: /查IP <IP地址>\n"
                "示例: /查IP 8.8.8.8"
            )
            return

        try:
            data = await self._fetch_json(
                f"http://ip-api.com/json/{ip}?lang=zh-CN", timeout=10
            )
            if data.get("status") != "success":
                yield event.plain_result(f"查询失败: {data.get('message', '未知错误')}")
                return

            yield event.plain_result(
                f"IP 归属地查询\n"
                f"{'='*20}\n"
                f"IP: {data.get('query', ip)}\n"
                f"位置: {data.get('country', '')} {data.get('regionName', '')} {data.get('city', '')}\n"
                f"ISP: {data.get('isp', '')}\n"
                f"经纬度: {data.get('lat', '')}, {data.get('lon', '')}\n"
                f"时区: {data.get('timezone', '')}"
            )
        except Exception as e:
            logger.error(f"IP查询失败: {e}")
            yield event.plain_result("IP 查询失败，请稍后重试。")

    @filter.command("GitHub")
    async def _(self, event: AstrMessageEvent, username: str = ""):
        """查询GitHub用户信息，/GitHub xiaohondan"""
        if not username:
            yield event.plain_result(
                "GitHub 用户查询\n"
                "用法: /GitHub <用户名>\n"
                "示例: /GitHub xiaohondan"
            )
            return

        try:
            data = await self._fetch_json(
                f"https://api.github.com/users/{username}", timeout=10
            )
            if "message" in data:
                yield event.plain_result(f"未找到用户: {username}")
                return

            yield event.plain_result(
                f"GitHub — {data.get('login', username)}\n"
                f"{'='*20}\n"
                f"名字: {data.get('name') or '未设置'}\n"
                f"简介: {data.get('bio') or '暂无简介'}\n"
                f"位置: {data.get('location') or '未知'}\n"
                f"博客: {data.get('blog') or '无'}\n"
                f"粉丝: {data.get('followers', 0)} | 关注: {data.get('following', 0)}\n"
                f"公开仓库: {data.get('public_repos', 0)} 个\n"
                f"Gist: {data.get('public_gists', 0)} 个\n"
                f"注册于: {str(data.get('created_at', ''))[:10]}"
            )
        except Exception as e:
            logger.error(f"GitHub查询失败: {e}")
            yield event.plain_result("GitHub 查询失败，请稍后重试。")

    # ==================== 内容生成 ====================

    @filter.command("二维码")
    async def _(self, event: AstrMessageEvent, content: str = ""):
        """生成二维码，/二维码 <内容或URL>"""
        if not content:
            yield event.plain_result(
                "二维码生成\n"
                "用法: /二维码 <内容或URL>\n"
                "示例: /二维码 https://github.com"
            )
            return

        try:
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(content)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            yield event.image_result(buf.read())
        except Exception as e:
            logger.error(f"二维码生成失败: {e}")
            yield event.plain_result("二维码生成失败，请稍后重试。")

    @filter.command("名言")
    async def _(self, event: AstrMessageEvent):
        """随机名言"""
        quotes = [
            ("生活不是等待暴风雨过去，而是学会在雨中跳舞。", "未知"),
            ("千里之行，始于足下。", "老子"),
            ("学而不思则罔，思而不学则殆。", "孔子"),
            ("不积跬步，无以至千里。", "荀子"),
            ("路漫漫其修远兮，吾将上下而求索。", "屈原"),
            ("天行健，君子以自强不息。", "周易"),
            ("知之者不如好之者，好之者不如乐之者。", "孔子"),
            ("己所不欲，勿施于人。", "孔子"),
            ("三军可夺帅也，匹夫不可夺志也。", "孔子"),
            ("温故而知新，可以为师矣。", "孔子"),
            ("人生自古谁无死，留取丹心照汗青。", "文天祥"),
            ("山重水复疑无路，柳暗花明又一村。", "陆游"),
            ("长风破浪会有时，直挂云帆济沧海。", "李白"),
            ("天生我材必有用，千金散尽还复来。", "李白"),
            ("会当凌绝顶，一览众山小。", "杜甫"),
            ("世上无难事，只怕有心人。", "谚语"),
            ("宝剑锋从磨砺出，梅花香自苦寒来。", "古训"),
            ("业精于勤，荒于嬉；行成于思，毁于随。", "韩愈"),
            ("读书破万卷，下笔如有神。", "杜甫"),
            ("不畏浮云遮望眼，自缘身在最高层。", "王安石"),
        ]
        quote, author = random.choice(quotes)
        yield event.plain_result(f"「{quote}」\n—— {author}")

    @filter.command("歌词")
    async def _(self, event: AstrMessageEvent):
        """随机歌词"""
        lyrics = [
            ("晴天", "周杰伦", "故事的小黄花，从出生那年就飘着"),
            ("稻香", "周杰伦", "对这个世界如果你有太多的抱怨"),
            ("七里香", "周杰伦", "窗外的麻雀，在电线杆上多嘴"),
            ("告白气球", "周杰伦", "塞纳河畔，左岸的咖啡"),
            ("简单爱", "周杰伦", "说不上为什么，我变得很主动"),
            ("起风了", "买辣椒也用券", "我曾将青春翻涌成她，也曾指尖弹出盛夏"),
            ("南山南", "马頔", "你在南方的艳阳里大雪纷飞"),
            ("平凡之路", "朴树", "我曾经跨过山和大海，也穿过人山人海"),
            ("成都", "赵雷", "和我在成都的街头走一走"),
            ("光年之外", "邓紫棋", "缘分让我们相遇乱世以外"),
            ("泡沫", "邓紫棋", "阳光下的泡沫是彩色的"),
            ("小幸运", "田馥甄", "我听见雨滴落在青青草地"),
            ("后来", "刘若英", "后来我总算学会了如何去爱"),
            ("红豆", "王菲", "还没为你把红豆，熬成缠绵的伤口"),
            ("夜空中最亮的星", "逃跑计划", "夜空中最亮的星，能否听清"),
            ("平凡的一天", "毛不易", "每个早晨七点半就自然醒"),
            ("消愁", "毛不易", "一杯敬朝阳，一杯敬月光"),
            ("漂洋过海来看你", "李宗盛", "为你我用了半年的积蓄，漂洋过海的来看你"),
            ("匆匆那年", "王菲", "匆匆那年，我们究竟说了几遍再见之后再拖延"),
            ("大鱼", "周深", "海浪无声将夜幕深深淹没"),
        ]
        song, artist, line = random.choice(lyrics)
        yield event.plain_result(f"「{line}」\n—— {artist}《{song}》")

    @filter.command("文字转图片")
    async def _(self, event: AstrMessageEvent, content: str = ""):
        """文字转图片，/文字转图片 <内容>"""
        if not content:
            yield event.plain_result(
                "文字转图片\n"
                "用法: /文字转图片 <内容>\n"
                "示例: /文字转图片 今天也要加油鸭"
            )
            return

        try:
            # 计算图片尺寸
            width = max(400, min(len(content) * 22 + 80, 1200))
            height = 160

            img = Image.new("RGB", (width, height))
            draw = ImageDraw.Draw(img)

            # 随机渐变背景
            seed_val = random.randint(0, 99999)
            r1 = seed_val * 37 % 80 + 30
            g1 = seed_val * 53 % 80 + 30
            b1 = seed_val * 71 % 120 + 80
            r2 = seed_val * 43 % 80 + 30
            g2 = seed_val * 67 % 80 + 30
            b2 = seed_val * 83 % 120 + 80

            for y in range(height):
                ratio = y / max(height - 1, 1)
                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))

            # 加载字体
            font_size = 24
            try:
                font_paths = [
                    "C:/Windows/Fonts/msyh.ttc",
                    "C:/Windows/Fonts/simhei.ttf",
                    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                ]
                font = None
                for fp in font_paths:
                    if Path(fp).exists():
                        font = ImageFont.truetype(fp, font_size)
                        break
                if font is None:
                    font = ImageFont.load_default()
            except Exception:
                font = ImageFont.load_default()

            # 自动换行
            max_chars = max(4, (width - 60) // (font_size + 2))
            lines = []
            for i in range(0, len(content), max_chars):
                lines.append(content[i:i + max_chars])

            y_offset = (height - len(lines) * (font_size + 8)) // 2
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                tw = bbox[2] - bbox[0]
                x = (width - tw) // 2
                draw.text((x, y_offset), line, fill=(255, 255, 255), font=font)
                y_offset += font_size + 8

            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            yield event.image_result(buf.read())
        except Exception as e:
            logger.error(f"文字转图片失败: {e}")
            yield event.plain_result("图片生成失败，请稍后重试。")

    # ==================== 工具 ====================

    @filter.command("计算")
    async def _(self, event: AstrMessageEvent, expr: str = ""):
        """计算器，/计算 <表达式>"""
        if not expr:
            yield event.plain_result(
                "计算器\n"
                "用法: /计算 <数学表达式>\n"
                "示例: /计算 (3+5)*2\n"
                "支持: + - * / ** ( ) % 等"
            )
            return

        # 安全白名单
        allowed = set("0123456789+-*/().% \t")
        if not all(c in allowed for c in expr):
            yield event.plain_result("表达式包含不允许的字符。仅支持数字和 +-*/()%. ")
            return

        try:
            result = eval(expr, {"__builtins__": {}}, {})
            yield event.plain_result(f"{expr} = {result}")
        except ZeroDivisionError:
            yield event.plain_result("错误: 除数不能为零。")
        except Exception:
            yield event.plain_result("表达式格式错误，请检查输入。")

    # ==================== 帮助菜单 ====================

    @filter.command("helpme")
    async def _(self, event: AstrMessageEvent):
        """帮助菜单"""
        help_text = (
            "QQ 功能工具箱 v1.0.0\n"
            "{'='*24}\n\n"
            "[娱乐趣味]\n"
            "  /毒鸡汤      随机毒鸡汤\n"
            "  /彩虹屁      随机彩虹屁\n"
            "  /土味情话    随机土味情话\n"
            "  /抽签        今日签运\n"
            "  /运势        今日运势详情\n"
            "  /骰子 [ndm]  掷骰子\n"
            "  /抛硬币      抛硬币\n"
            "  /摇一摇      随机选人(群聊)\n"
            "  /猜数字      猜数字游戏\n"
            "  /复读 <文>   复读一句话\n\n"
            "[实用查询]\n"
            "  /天气 [城市]  查天气\n"
            "  /黄历        今日黄历\n"
            "  /汇率 <币>   查汇率\n"
            "  /查IP <地址> IP归属地\n"
            "  /GitHub <名> GitHub用户\n\n"
            "[内容生成]\n"
            "  /二维码 <内容> 生成二维码\n"
            "  /名言        随机名言\n"
            "  /歌词        随机歌词\n"
            "  /文字转图片   文字转图片\n\n"
            "[工具]\n"
            "  /计算 <表达式> 计算器\n\n"
            "/helpme 显示本帮助\n"
            "by 小红蛋"
        )
        yield event.plain_result(help_text)

    # ==================== 事件监听：自动复读 ====================

    @filter.event_message_type(EventMessageType.GROUP_MESSAGE)
    async def auto_repeat(self, event: AstrMessageEvent):
        """监听群消息，连续相同消息达到阈值时自动复读"""
        group_id = self._get_group_id(event)
        if not group_id:
            return

        threshold = self._get_conf("repeater_threshold", 3)
        if threshold <= 0:
            return

        text = event.message_str.strip()
        if not text or text.startswith("/"):
            return

        if group_id not in self.repeater_state:
            self.repeater_state[group_id] = {"last_msg": "", "count": 0}

        state = self.repeater_state[group_id]
        if text == state["last_msg"]:
            state["count"] += 1
            if state["count"] == threshold:
                yield event.plain_result(text)
                state["count"] = 0
                state["last_msg"] = ""
        else:
            state["last_msg"] = text
            state["count"] = 1
