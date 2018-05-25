
class TradeInfo:
    def __init__(self):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    # 处理一组礼物或者心愿
    def __parse(self, goods):
        self.total = len(goods)
        # 列表推导式简化代码
        self.trades = [self.__map_to_trade(single) for single in goods]

    # 处理单个礼物或者心愿
    def __map_to_trade(self, single):
        return dict(
            user_name=single.user.nickname,
            # 格式化时间
            time=single.create_time.strtime('%Y-%m-%d'),
            id=single.id
        )
