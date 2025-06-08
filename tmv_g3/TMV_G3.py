class Strategy(StrategyBase):

    def initialize(self): # 初始化
        declare_strategy_type(AlgoStrategyType.SECURITY)
        self.trigger_symbols()
        self.custom_indicator()
        self.global_variables()

    def trigger_symbols(self):  # 定义驱动标的
        self.驱动标的1 = declare_trig_symbol()

    def global_variables(self):  # 定义全局变量
        self.recent_low = show_variable(0.0, GlobalType.FLOAT)
        self.recent_high = show_variable(0.0, GlobalType.FLOAT)
        self.出售数量 = show_variable(0, GlobalType.INT)
        self.last_sell_price = show_variable(0.0, GlobalType.FLOAT)
        self.sell_count = show_variable(0, GlobalType.INT)
        self.last_buy_price = show_variable(0.0, GlobalType.FLOAT)
        self.buy_count = show_variable(0.0, GlobalType.FLOAT)

    def custom_indicator(self):  # 
        pass

    def handle_data(self):  # K线推送、Tick推送、固定时间间隔、指定时刻，这4种事件会触发handle_data()函数
        self.action_7337428812802637510_invoke()  # 执行路径1

    def action_7337428812802637510(self):
        crt_price =  current_price(symbol=self.驱动标的1, price_type=THType.FTH)
        ol_cst = 31.4
        
        
        
        
        mqts = max_qty_to_sell(symbol=self.驱动标的1)
        
        
        # 止盈
        
        _variable_1 = position_pl_ratio(symbol=self.驱动标的1, cost_price_model=CostPriceModel.AVG)
        if _variable_1 > 0.75:
            print("当前收益率为：", _variable_1 * 100, "，成功触发止盈")
            place_limit(symbol=self.驱动标的1, price=crt_price,qty=mqts*0.84 , side=OrderSide.SELL, time_in_force=TimeInForce.DAY) 
            self.last_sell_price = crt_price
            self.recent_low = crt_price
            self.recent_high = 0.0
            self.sell_count = 0
            self.buy_count = 0.0
            self.recent_high = crt_price
            self.recent_low = 0.0
            self.last_buy_price = crt_price
            self.sell_count = 0
            self.buy_count = 0
            return True
        
        
        
        
        print("low_price:", self.recent_low)
        print("high_price:", self.recent_high) 
        
        mcb =  max_qty_to_buy_on_cash(symbol=self.驱动标的1, order_type=OrdType.LMT, price=crt_price)
        
        print("max_qty_can_buy", mcb)
        
        
        
        def raise_l9(x):
            return 9+15 if x < 9 else x
        
        def raise_l5(x):
            return 5 if x < 5 else x
        def raise_l3(x):
            return 3 if x < 3 else x
            
            
            
            
        
        
        if mqts <= 0:
             place_limit(symbol=self.驱动标的1, price=crt_price, qty=2000, side=OrderSide.BUY, time_in_force=TimeInForce.GTC)
             return
             
             
        #买入价差
        #cwratio = [0.01, 0.02, 0.04, 0.08, 0.064, 0.128, 0.064, 0.128, 0.256, 0.512, 1.024, 8.192, 16.384]     
        
        cwratio = [0.02,  0.04,  0.08, 0.12,  0.14,   0.18,  0.26,  0.42,  0.74,  1.38,  2.66,  5.22, 10.34, 20.48]     
         
        #卖出价差 
        kkwratio = [0.001,  0.08, 0.016, 0.032, 1.024, 2.048, 4.096, 8.192, 16.384, 32.0, 64.0, 128.0, 512.0, 1024.0, 2048.0]     
        
        if self.recent_high > 0 and self.recent_high > crt_price * 1.0125 and mcb > 0:
                add_amount = 0
                tms_buy = 2 ** (self.buy_count+3) * cwratio[ceil(self.buy_count)]
                add_amount =   add_amount +  ( self.last_buy_price  - crt_price + ol_cst)   * tms_buy
                 
                    
                print("last_sell_price", self.last_sell_price, "crt_price", crt_price, "buy add_amount", add_amount) 
                if add_amount > 8000.0:
                    add_amount = 8000.0
                nto_buy = 0
                nto_buy = raise_l9(mcb * 0.001) +add_amount
                
         #保持剩余资金，防止被平仓
                if (mcb - nto_buy) > 200 and nto_buy > 5:       
                        if self.last_sell_price > 0 and crt_price > self.last_sell_price:
                            place_limit(symbol=self.驱动标的1, price=crt_price,qty=nto_buy , side=OrderSide.SELL, time_in_force=TimeInForce.GTC) 
                            self.last_sell_price = crt_price
                            self.recent_low = crt_price
                            self.recent_high = 0.0
                            self.sell_count = self.sell_count + 1.0
                            self.buy_count = 0.0
                        else:     
                            place_limit(symbol=self.驱动标的1, price=crt_price, qty=nto_buy, side=OrderSide.BUY, time_in_force=TimeInForce.GTC)
                            self.recent_high = crt_price
                            self.recent_low = 0.0
                            self.last_buy_price = crt_price
                            self.sell_count = 0
                            self.buy_count = self.buy_count+1
            
        mqts = max_qty_to_sell(symbol=self.驱动标的1)
             
        
        add_amount = 0
        tms_sell = 2 ** (self.sell_count + 3) * kkwratio[ceil(self.sell_count)]
        add_amount =   add_amount +  ( crt_price - self.last_sell_price)   * tms_sell
            
            
            
        
        print("crt_price", crt_price, "last_buy_price", self.last_buy_price, "sell add_amount", add_amount)
        
        if add_amount > 8000.0:
            add_amount = 8000.0
            
            
        # 如果卖价 比上次买价还要低，就不卖。
        sell_amount = raise_l3(mqts * 0.001) + add_amount
        if sell_amount > mqts:
            sell_amount  = mqts * 0.2178
            
        
         
        if self.recent_low > 0 and self.recent_low < crt_price * 0.9775 and sell_amount > 2 and mqts > 0:    
            # 如果比上一次买价还低，那么这一次就把卖出方向，改为买入方向
            if self.last_buy_price > 0 and crt_price < self.last_buy_price:
                place_limit(symbol=self.驱动标的1, price=crt_price, qty=sell_amount, side=OrderSide.BUY, time_in_force=TimeInForce.GTC)
                self.recent_high = crt_price
                self.recent_low = 0.0
                self.last_buy_price = crt_price
                self.sell_count = 0
                self.buy_count = self.buy_count+1
            else:
                place_limit(symbol=self.驱动标的1, price=crt_price,qty=sell_amount , side=OrderSide.SELL, time_in_force=TimeInForce.GTC) 
                self.last_sell_price = crt_price
                self.recent_low = crt_price
                self.recent_high = 0.0
                self.sell_count = self.sell_count + 1.0
                self.buy_count = 0.0
        
        if crt_price < self.recent_low or self.recent_low == 0:
            self.recent_low = crt_price
            
        if crt_price >= self.recent_high:
            self.recent_high = crt_price
            
            
                
        # 底仓优化，如果小于50，就调整
        if mqts < 50.0:
            self.recent_high = crt_price
            
        
            
        print("after low_price:", self.recent_low)
        print("after high_price:", self.recent_high)

    def action_7337428812802637510_invoke(self):  # 自编码动作
        self.action_7337428812802637510()