from app.view_models.book import BookViewModel


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


class MyTrades:
    def __init__(self, trades_of_mine, trade_count_list):
        self.trades = []
        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list
        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.__trades_of_mine:
            my_trade = self.matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def matching(self, trade):
        """
        提取一个函数简化两层 for 循环
        """
        count = 0
        for trade_count in self.__trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        r = {
            'count': count,
            'book': BookViewModel(trade.book),
            'id': trade.id
        }
        return r
