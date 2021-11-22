class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        """处理一组礼物或者心愿"""
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    @staticmethod
    def __map_to_trade(single):
        """处理单个礼物或者心愿"""
        return {
            'user_name': single.user.nickname,
            'time': single.create_datetime.strftime('%Y-%m-%d') if single.create_time else '未知',
            'id': single.id
        }
