slice_price = 0
min_w = 0
max_w = 0
Acc_weight = 0
shipping_packages = ''
Remaining_weight = 0
cost = 0
f = False

slices_list = [{'slice_min': 10,'slice_max': 15,'price_average': 7},
               {'slice_min': 20,'slice_max': 25,'price_average': 8},
               {'slice_min': 5,'slice_max': 10,'price_average': 9},
               {'slice_min': 0,'slice_max': 5,'price_average': 10},
               {'slice_min': 15,'slice_max': 20,'price_average': 11},]
cart_list = [{'name':'a','quantity': 3,'weight': 5},
             {'name':'b','quantity': 4,'weight': 6},
             {'name':'c','quantity': 5,'weight': 7},
             {'name':'d','quantity': 6,'weight': 8},
             {'name':'e','quantity': 7,'weight': 9},
             {'name':'f','quantity': 8,'weight': 10}]
package_list = []
Remaining_list = []


for s in slices_list:
    min_w = s['slice_min']
    max_w = s['slice_max']
    slice_price = s['price_average']
    if cart_list is None:
        break
    for rl in Remaining_list:
        if rl['quantity'] != 0:
            cart_list.append(rl)
        else:
            Remaining_list = []
    while True:
        Remaining_weight = 0
        f = False
        for item2 in cart_list:
            if item2['weight'] <= max_w and item2['quantity'] != 0:
                f = True
                break
        if f is False:
            break
        for item in range(len(cart_list)):  # cart loop
            if cart_list[item]['weight'] > max_w:
                break
            if cart_list[item]['quantity'] != 0:
                for q in range(cart_list[item]['quantity']):  # product loop
                    Acc_weight += cart_list[item]['weight']
                    if Acc_weight > max_w:
                        Acc_weight -= cart_list[item]['weight']
                        break
                    else:
                        package_list.append({'name': cart_list[item]['name'],'quantity': 1,'weight': cart_list[item]['weight']}, )
                        cart_list[item]['quantity'] -= 1
        for item3 in range(len(Remaining_list)):  # Remaining loop
            if Remaining_list[item3]['weight'] > max_w:
                break
            if Remaining_list[item3]['quantity'] != 0:
                Acc_weight += Remaining_list[item3]['weight']
                if Acc_weight > max_w:
                    Acc_weight -= Remaining_list[item3]['weight']
                    break
                else:
                    package_list.append({'name': Remaining_list[item3]['name'],'quantity': 1,'weight': Remaining_list[item3]['weight']}, )
                    Remaining_list[item3]['quantity'] -= 1
        if Acc_weight < min_w:
            for pl in package_list:
                Remaining_list.append(pl)
        else:
            for p in range(len(package_list)):
                shipping_packages += package_list[p]['name'] + '+'
            cost = int(Acc_weight) * int(slice_price)
            shipping_packages += ' , weight = ' + str(Acc_weight) + ' , cost = ' + str(cost) + '\n'
        package_list = []
        Acc_weight = 0
        for item5 in cart_list:
            if item5['quantity'] == 0:
                cart_list.remove(item5)
print(shipping_packages)