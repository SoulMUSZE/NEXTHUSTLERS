l = ['#dasjklas', '#djeiwoji', '#asdf', '#asdf']
ui = list(set(l))
# >>> ui
# ['#dasjklas', '#djeiwoji', '#asdf']
ci = [l.count(i) for i in tuple(ui)]
# >>> ci
# [1, 1, 2]
h = [{'key':ui[i], 'count':ci[i]} for i in range(len(ci))]
# >>> h
# [{'key': '#dasjklas', 'count': 1}, {'key': '#djeiwoji', 'count': 1}, {'key': '#asdf', 'count': 2}]
