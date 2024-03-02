import math as m
import random as rnd

#Levels and constants initialization, time step setting
##constants
init_account = 10000
vat_rate = 0.2
vages_and_taxes = 500
transport_capacity = 30
transfer_vol = 50
transfer_rate = 75
transfer_decision = 0
stop_sell = 1
ret_price = 100
rent_rate = 200
opt_offer_base_volume = 50
opt_offer_accept_decision = 0
mean_d_price = 100
max_demand = 30
basic_opt_offer_vol = 50
basic_opt_offer_price = 35
cur_time = 0
sim_continue = True

##levels
Account = init_account
Basic_store = 80
Transport = 0
Shop_store = 30
All_lost = 0

#Auxiliary variables and temps initialization
truck_unloading = Transport
trucks_needed = m.ceil(min(Basic_store, transfer_vol) / transport_capacity)
rnd_offer_volume = round(opt_offer_base_volume * (rnd.random() / 2 + 0.7))
demand = round(max_demand * (1 - 1 / (1 + m.exp(-0.05 * (ret_price - mean_d_price)))))
daily_spending = min(rent_rate + vages_and_taxes, Account)
basic_price_rnd = basic_opt_offer_vol * (rnd.random() * 0.6 + 0.7)
add_price_by_time = basic_opt_offer_price * 0.03 * cur_time + basic_opt_offer_price * 0.01 * cur_time * rnd.random()
lost = Shop_store + truck_unloading - 100 if Shop_store + truck_unloading > 100 else 0
tr_need_and_affordable = min(trucks_needed, m.floor(Account / transfer_rate))
rnd_demand = round(demand * (rnd.random() / 2 + 0.7))
offer_one_price = add_price_by_time + basic_price_rnd
trans_spend = transfer_rate * tr_need_and_affordable if transfer_decision else 0
transfer_actual_volume = min(transfer_vol * transfer_decision, tr_need_and_affordable * transport_capacity)
sold_ret = (1 - stop_sell) * min(rnd_demand, Shop_store)
offer_full_price = offer_one_price * rnd_offer_volume
truck_loading = m.floor(transfer_actual_volume)
selling = sold_ret
income = ret_price * sold_ret
offer_accept_possibility = 1 if Account >= offer_full_price else 0
vat = income * vat_rate
small_opt_income = offer_accept_possibility * opt_offer_accept_decision * rnd_offer_volume
opt_purchase_spend = opt_offer_accept_decision * offer_accept_possibility * offer_full_price

#Step-by-step parameters output, decision making and computations
while True:
	##Parameters output
	print(f'Сумма денег на расчётном счёте: {Account}')
	print(f'Затраты на закупку партии на прошлом шаге: {-opt_purchase_spend}')
	print(f'Затраты на транспорт на прошлом шаге: {-trans_spend}')
	print(f'Ежедневные бытовые фиксированные затраты: {-daily_spending}')
	print(f'Доход от продажи за прошлый шаг за вычетом налогов: {income - vat}')
	print(f'На прошлом шаге было продано {selling} ед. товара по цене {ret_price} за ед. (без учёта налогов с продажи)\n')

	print(f'Товар на базовом складе: {Basic_store} ед.')
	print(f'Товар в дороге: {Transport} ед.')
	print(f'Товар на складе магазина: {Shop_store} ед.')
	print(f'Ожидаемые потери товара на данном шаге: {lost}')
	print(f'Потери товара за всё время: {All_lost}\n')

	print('Оптовое предложение:')
	print(f'Объём партии - {rnd_offer_volume} ед.')
	print(f'Цена за штуку - {m.ceil(offer_one_price * 100) / 100}')
	print(f'Общая цена - {m.ceil(offer_full_price * 100) / 100}\n')

	print(f'Стоимость перевозки товара - {transfer_rate} за машину, в которую поместится 30 ед. товара')
	print('Спрос при цене 50 за ед. будет около',
		round(max_demand * (1 - 1 / (1 + m.exp(-0.05 * (50 - mean_d_price))))),
		'\nА при цене 100 за ед. - около',
		round(max_demand * (1 - 1 / (1 + m.exp(-0.05 * (100 - mean_d_price))))),
		'\n')

	print(f'С начала моделирования прошло {cur_time} дней')

	##Manual parameters change
	sim_continue = int(input('Введите 1, чтобы продолжить симуляцию, или 0, чтобы завершить её\n'))
	if sim_continue == 0:
		break

	opt_offer_accept_decision = float(input('Введите 1, чтобы согласиться на оптовое предложение и произвести закупку, или 0, чтобы отказаться\n'))
	small_opt_income = offer_accept_possibility * opt_offer_accept_decision * rnd_offer_volume
	opt_purchase_spend = opt_offer_accept_decision * offer_accept_possibility * offer_full_price
	
	transfer_decision = int(input('Введите 1, чтобы осуществить перевозку, или 0, чтобы отказаться\n'))
	if transfer_decision:
		transfer_vol = int(input('Введите количество единиц товара, которые будут перевезены\n'))
	else:
		transfer_vol = 0
	trucks_needed = m.ceil(min(Basic_store, transfer_vol) / transport_capacity)
	tr_need_and_affordable = min(trucks_needed, m.floor(Account / transfer_rate))
	transfer_actual_volume = min(transfer_vol * transfer_decision, tr_need_and_affordable * transport_capacity)
	trans_spend = transfer_rate * tr_need_and_affordable if transfer_decision else 0
	truck_loading = m.floor(transfer_actual_volume)
	
	stop_sell = int(input('Введите 1, чтобы производить торговлю на этом шаге, или 0, чтобы не производить\n'))
	stop_sell = 1 - stop_sell
	if stop_sell == 0:
		ret_price = float(input('Установите цену для покупателей в магазине за одну единицу товара\n'))
	demand = round(max_demand * (1 - 1 / (1 + m.exp(-0.05 * (ret_price - mean_d_price)))))
	rnd_demand = round(demand * (rnd.random() / 2 + 0.7))
	sold_ret = (1 - stop_sell) * min(rnd_demand, Shop_store)
	income = ret_price * sold_ret
	selling = sold_ret
	vat = income * vat_rate


	##Levels, auxiliary_variables and temps recounting
	###Levels
	Account = Account + income - vat - daily_spending - trans_spend - opt_purchase_spend
	Basic_store = Basic_store + small_opt_income - truck_loading
	Transport = Transport + truck_loading - truck_unloading
	Shop_store = Shop_store + truck_unloading - lost - selling
	All_lost = All_lost + lost
	###Auxiliary_variables and temps
	truck_unloading = Transport
	rnd_offer_volume = round(opt_offer_base_volume * (rnd.random() / 2 + 0.7))
	daily_spending = min(rent_rate + vages_and_taxes, Account)
	basic_price_rnd = basic_opt_offer_vol * (rnd.random() * 0.6 + 0.7)
	add_price_by_time = basic_opt_offer_price * 0.03 * cur_time + basic_opt_offer_price * 0.01 * cur_time * rnd.random()
	lost = Shop_store + truck_unloading - 100 if Shop_store + truck_unloading > 100 else 0
	offer_one_price = add_price_by_time + basic_price_rnd
	offer_full_price = offer_one_price * rnd_offer_volume
	offer_accept_possibility = 1 if Account >= offer_full_price else 0
	cur_time += 1
