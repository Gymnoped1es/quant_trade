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
        self.action_7336364283120678834_invoke()  # 执行路径1

    def action_7336364283120678834(self):
        crt_price =  current_price(symbol=self.驱动标的1, price_type=THType.FTH)
        
        if self.recent_high <= 0:
            self.recent_high = crt_price
        
        if self.recent_low <= 0:
            self.recent_low = crt_price
        
        print("low_price:", self.recent_low)
        print("high_price:", self.recent_high) 
        
        mcb =  max_qty_to_buy_on_margin(symbol=self.驱动标的1, order_type=OrdType.MKT, price=crt_price)
        
        print("max_qty_can_buy", mcb)
        
        if self.recent_high > 0 and self.recent_high > crt_price * 1.02:
                add_amount = ( (   ( self.last_sell_price - crt_price)/crt_price)*19)**(self.buy_count+1)
                print("buy add_amount", add_amount)
                if add_amount < 25.0:
                    add_amount = 25.0
                if add_amount > 7000.0:
                    add_amount = 7000.0
                    
                nto_buy = mcb * 0.03 +add_amount
                if nto_buy > mcb:
                    nto_buy = mcb * 0.7    
                    
                place_limit(symbol=self.驱动标的1, price=crt_price, qty=nto_buy, side=OrderSide.BUY, time_in_force=TimeInForce.GTC)
                self.recent_high = crt_price
                self.last_buy_price = crt_price
                self.sell_count = 0
                self.buy_count = self.buy_count+1
            
        mqts = max_qty_to_sell(symbol=self.驱动标的1)
             
        
        
        add_amount =  ( ( (crt_price - self.last_buy_price)/self.last_buy_price)*19 )** (self.sell_count+1)
        print("sell add_amount", add_amount)
        if add_amount < 25.0:
            add_amount = 25.0
        if add_amount > 7500.0:
            add_amount = 7500.0
        
        self.出售数量 = mqts * 0.03 + add_amount
        if self.出售数量 > mqts:
            self.出售数量  = mqts * 0.2178
        
         
        if self.recent_low > 0 and self.recent_low < crt_price * 0.97 and self.出售数量 > 0:    
            place_limit(symbol=self.驱动标的1, price=crt_price,qty=self.出售数量 , side=OrderSide.SELL, time_in_force=TimeInForce.GTC) 
            self.last_sell_price = crt_price
            self.recent_low = crt_price
            self.sell_count = self.sell_count + 1.0
            self.buy_count = 0.0
        
        if crt_price < self.recent_low:
            self.recent_low = crt_price
            
        if crt_price > self.recent_high:
            self.recent_high = crt_price
            
            
                
        # 底仓优化，如果小于50，就调整
        if mqts < 50.0:
            self.recent_high = crt_price
            
        
            
        print("after low_price:", self.recent_low)
        print("after high_price:", self.recent_high)

    def action_7336364283120678834_invoke(self):  # 自编码动作
        self.action_7336364283120678834()