import pandas as pd


#load files
visits = pd.read_csv('visits.csv',
                     parse_dates=[1])
cart = pd.read_csv('cart.csv',
                   parse_dates=[1])
checkout = pd.read_csv('checkout.csv',
                       parse_dates=[1])
purchase = pd.read_csv('purchase.csv',
                       parse_dates=[1])

#inspect dataframes
print(visits.head(3))
print(cart.head(3))
print(checkout.head(3))
print(purchase.head(3))


####BUILD A FUNNEL FOR COOL TSHIRTS INC.

#first left merge
visits_cart = pd.merge(
  visits,
  cart,
  how='left'
)
#NaT = not a time, meaning user didn't add tshirt to cart.
visits = len(visits_cart.user_id) #2000 rows
no_cart = visits_cart.cart_time.isnull().sum() #1652 rows
visit_no_cart = no_cart/visits
#82.6% of users who visited cool t-shirts inc. ended up not placing a tshirt in their cart.

#2nd left merge
cart_checkout = pd.merge(
  cart,
  checkout,
  how='left'
)

carts = len(cart_checkout.user_id)
no_checkout = cart_checkout.checkout_time.isnull().sum()
cart_no_checkout = no_checkout/carts
#25.31% of users put items in cart but did not checkout

#merge all data together into a single dataframe.
all_data = visits_cart.merge(
  cart_checkout,
  how='left').merge(
    purchase,
    how='left'
  )

checkout = all_data.checkout_time.count()
no_purchase = all_data.purchase_time[all_data.checkout_time.notnull()].isnull().sum()
checkout_no_purchase = no_purchase/checkout
#16.8% of users who checked out didn't purchase tshirt in their cart.
#step1 => highest percentage of users not putting tshirt in cart. maybe tshirts aren't cool enough??

####Average Time To Purchase
all_data['time_to_purchase'] = all_data.purchase_time \
 - all_data.visit_time
print(all_data['time_to_purchase'])

time_to_purch_avg = all_data['time_to_purchase'].mean()
print(time_to_purch_avg)
#43min53secs.
