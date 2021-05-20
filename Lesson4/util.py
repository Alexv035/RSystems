

def prefilter_items(data):
    # Уберем самые популярные товары (их и так купят)
    popularity = data_train.groupby('item_id')['user_id'].nunique().reset_index() / data_train['user_id'].nunique()
    popularity.rename(columns={'user_id': 'share_unique_users'}, inplace=True)
    
    top_popular = popularity[popularity['share_unique_users'] > 0.5].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]
    
    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_notpopular = popularity[popularity['share_unique_users'] < 0.01].item_id.tolist()
    data = data[~data['item_id'].isin(top_notpopular)]
    
    # Уберем товары, которые не продавались за последние 12 месяцев
    not_sales = popularity[popularity['week_no'] > 52].item_id.tolist()
    data = data[~data['item_id'].isin(not_sales)]
    
    # Уберем не интересные для рекоммендаций категории (department)
    not_int = popularity[popularity['quantity'] < 1].item_id.tolist()
    data = data[~data['item_id'].isin(not_int)]
    
    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб. 
    sales_cheap = popularity[popularity['sales_value'] < 1].item_id.tolist()
    data = data[~data['item_id'].isin(sales_cheap)]
        
    # Уберем слишком дорогие товары
    sales_exp = popularity[popularity['sales_value'] > 10].item_id.tolist()
    data = data[~data['item_id'].isin(sales_exp)]
    
    return data
    
def postfilter_items(user_id, recommednations):
    pass
