
def fac(n):
    res = 1
    for i in range(1,n+1):
        res *= i
    return res

get_color = lambda i: 'B' if i[1] in 'SC' else 'R'

def get_face_value(i):
    values = {'J':11 ,'Q':12, 'K':13, 'A': 20}
    v = values[i[0]] if i[0] in values else int(i[0])
    if v == 0:
        v = 10
    return v

def is_run(o_cards, a_cards):
    #保存A
    _a_cards = a_cards[:]
    #保存检测顺子扑克
    res_cards = o_cards[:1]
    #保存未检测扑克
    remain_cards = o_cards[1:]
    while True:
        if len(res_cards) == len(o_cards) + len(a_cards):
            break
        #计算已检测顺子末尾扑克面值
        for index,card in enumerate(res_cards[::-1]):
            if 'A' in card:
                continue
            else:
                pre_card_val = get_face_value(card) + index

        # print('remain_cards', remain_cards)

        # 前后符合顺子规则
        if remain_cards and get_face_value(remain_cards[0]) == pre_card_val + 1 and get_color(res_cards[-1]) != get_color(remain_cards[0]):
            res_cards.append(remain_cards[0])
            remain_cards = remain_cards[1:]
        # 尝试用A补齐
        elif _a_cards:
            for a in _a_cards:
                if get_color(a) != get_color(res_cards[-1]):
                    res_cards.append(a)
                    _a_cards.remove(a)
                    break
            else:
                return False
        else:
            return False
    # 末尾为A,则不符合
    if 'A' in res_cards[-1]:
        return False
    else:
        return True

def val_col_card(val,col):
    if col == 'B':
        col = 'R'
    else:
        col = 'B'
    values = {10: '0', 11: 'J', 12: 'Q', 13: 'K'}
    if val in values:
        val = values[val]
    else:
        val = str(val)
    sub_colors = {'B':['S', 'C'], 'R':['H', 'D']}
    return [val + c for c in sub_colors[col]]

def comp10001go_score_group(cards):
    if len(cards) > 1:
        a_cards = [card for card in cards if 'A' in card]
        o_cards = [card for card in cards if 'A' not in card]
        o_cards.sort(key=get_face_value)
        # print(o_cards)
        # 以下检测N-of-a-kind
        if not a_cards:
            face_values = set([o_card[0] for o_card in o_cards])
            if len(face_values) == 1:
                face_value = face_values.pop()
                face_value = get_face_value(o_cards[0])
                return face_value * fac(len(cards))
        if len(cards) >= 3 and is_run(o_cards, a_cards):
            min_card = o_cards[0]
            min_val = get_face_value(min_card)
            return sum(range(min_val, min_val+len(cards)))
    return -sum([get_face_value(c) for c in cards])


def  comp10001go_valid_groups(groups):
    # print('groups', groups)
    no_single_groups = [group for group in groups if len(group) > 1]
    if not no_single_groups:
        return True
    scores = [comp10001go_score_group(group) for group in no_single_groups]
    scores = [s for s in scores if s < 0]
    if scores:
        return False
    else:
        return True

def comp10001go_play(discard_history, player_no, hand):
    my_discards = []
    for cards in discard_history:
        try:
            my_discards.append(cards[player_no])
        except:
            pass
    o_cards = [card for card in my_discards if 'A' not in card]
    discard = None
    if o_cards:
        o_cards.sort(key=get_face_value,reverse=True)
        need_cards = set()
        for card in o_cards:
            val = get_face_value(card)
            need_cards.update(val_col_card(val + 1, get_color(card)))
            need_cards.update(val_col_card(val + 1, get_color(card)))

        need_cards_val = [card[0] for card in o_cards]


        for hand_card_val in need_cards_val:
            for hand_card in hand:
                if hand_card_val in hand_card:
                    discard = hand_card
                    break
            if discard:
                break

        if not discard:
            for need_card in need_cards:
                if need_card in hand:
                    discard = need_card
                    break

    if not discard:
        a_hand = [card for card in hand if 'A' not in card]
        if a_hand:
            a_hand.sort(key=get_face_value)
            discard = a_hand[0]
        else:
            mid = len(hand) // 2
            discard = hand[mid]

    hand.remove(discard)

    if player_no == 0:
        discard_history.append([discard,])
    else:
        if discard_history:
            if player_no < len(discard_history[-1]):
                discard_history[-1][player_no] = discard
            else:
                discard_history[-1].append(discard)
        else:
            history = [None, ] * player_no
            history.append(discard)
            discard_history.append(history)
    return discard


# def comp10001go_best_partitions(cards):
#     # 获取非A牌
#     o_cards = [card for card in cards if 'A' not in card]
#     # 获取A牌
#     a_cards = [card for card in cards if 'A' in card]
#     #非A牌按face value从大到小排序
#     o_cards.sort(key=get_face_value,reverse=True)
#     runs = []
#     # 尝试每张牌开始可构成的顺子
#     for start_cart in o_cards[:-1]:
#         if len(o_cards) < 2 or start_cart not in o_cards:
#             break
#         o_cards.sort(key=get_face_value,reverse=True)
#         seq = get_face_value(start_cart)
#         run = [start_cart, ]
#         o_cards.remove(start_cart)
#         # 循环构成顺子
#         while True:
#             seq -= 1
#             color = get_color(run[-1])
#             #构成顺子的下一张牌可能值
#             next_cards = val_col_card(seq, color)
#             next_a_cards = set('A'+c[1] for c in next_cards)
#             # 非A牌中查找可能的下一张牌
#             next_card = None
#             for c in next_cards:
#                 if c in o_cards:
#                     next_card = c
#                     break

#             if next_card:
#                 run.append(next_card)
#                 o_cards.remove(next_card)
#             # 尝试用A牌补齐顺子
#             elif a_cards and next_a_cards & set(a_cards):
#                 next_card = (next_a_cards & set(a_cards)).pop()
#                 run.append(next_card)
#                 a_cards.remove(next_card)
#             else:
#                 break
#             # print('run', run)

#         # 除去顺子结尾的A牌
#         while True:
#             if 'A' in run[-1]:
#                 a_cards.append(run[-1])
#                 run = run[:-1]
#             else:
#                 break

#         # 丢弃长度小于2的顺子
#         if len(run) > 2:
#             runs.append(run)
#         else:
#             o_cards.extend(run)
            
#     # 处理组成顺子剩下的牌
#     val_group = {}
#     for card in o_cards:
#         if card[0] in val_group:
#             val_group[card[0]].append(card)
#         else:
#             val_group[card[0]] = [card, ]
#     res = list(val_group.values())
#     if a_cards:
#         for a in a_cards:
#             res.append([a,])
#     res.extend(runs)
#     return res

def comp10001go_best_partitions(cards):
    # 获取非A牌
    o_cards = [card for card in cards if 'A' not in card]
    # 获取A牌
    a_cards = [card for card in cards if 'A' in card]

    res = []
    val_group = {}
    for card in o_cards:
        if card[0] in val_group:
            val_group[card[0]].append(card)
        else:
            val_group[card[0]] = [card, ]
    for k,v in val_group.items():
        if len(v) > 1:
            res.append(v)
            for c in v:
                o_cards.remove(c)

    #非A牌按face value从大到小排序
    o_cards.sort(key=get_face_value,reverse=True)
    runs = []
    # 尝试每张牌开始可构成的顺子
    for start_cart in o_cards[:-1]:
        if len(o_cards) < 2 or start_cart not in o_cards:
            break
        o_cards.sort(key=get_face_value,reverse=True)
        seq = get_face_value(start_cart)
        run = [start_cart, ]
        o_cards.remove(start_cart)
        # 循环构成顺子
        while True:
            seq -= 1
            color = get_color(run[-1])
            #构成顺子的下一张牌可能值
            next_cards = val_col_card(seq, color)
            next_a_cards = set('A'+c[1] for c in next_cards)
            # 非A牌中查找可能的下一张牌
            next_card = None
            for c in next_cards:
                if c in o_cards:
                    next_card = c
                    break

            if next_card:
                run.append(next_card)
                o_cards.remove(next_card)
            # 尝试用A牌补齐顺子
            elif a_cards and next_a_cards & set(a_cards):
                next_card = (next_a_cards & set(a_cards)).pop()
                run.append(next_card)
                a_cards.remove(next_card)
            else:
                break
            # print('run', run)

        # 除去顺子结尾的A牌
        while True:
            if 'A' in run[-1]:
                a_cards.append(run[-1])
                run = run[:-1]
            else:
                break

        # 丢弃长度小于2的顺子
        if len(run) > 2:
            runs.append(run)
        else:
            o_cards.extend(run)
            
    # 处理组成顺子剩下的牌
    val_group = {}
    for card in o_cards:
        if card[0] in val_group:
            val_group[card[0]].append(card)
        else:
            val_group[card[0]] = [card, ]
    res.extend(val_group.values())
    if a_cards:
        for a in a_cards:
            res.append([a,])
    res.extend(runs)
    return res

def comp10001go_group(discard_history, player_no):
    # cards = [cards[player_no] for cards in discard_history]
    my_discards = []
    for cards in discard_history:
        if player_no < len(cards):
            my_discards.append(cards[player_no])
    # print(my_discards)
    return comp10001go_best_partitions(my_discards)

if __name__ == '__main__':
    # v = [
    #     comp10001go_score_group(['2C']),
    #     comp10001go_score_group(['2C', '2S']),
    #     comp10001go_score_group(['4C', '4H', '4S']),
    #     comp10001go_score_group(['4C', '4H', '3S']),
    #     comp10001go_score_group(['4C', '4H', 'AS']),
    #     comp10001go_score_group(['KC', 'KH', 'KS', 'KD']),
    #     comp10001go_score_group(['2C', '3D', '4S']),
    #     comp10001go_score_group(['4S', '2C', '3D'])
    #     ]
    # print(v)
    # v = [
    #     comp10001go_valid_groups([['KC', 'KH', 'KS', 'KD'], ['2C']]),
    #     comp10001go_valid_groups([['KC', 'KH', 'KS', 'AD'], ['2C']]),
    #     comp10001go_valid_groups([['KC', 'KH', 'KS', 'KD'], ['2C', '3H']]),
    #      comp10001go_valid_groups([])
    # ]
    # print(v)
    # discard = comp10001go_play([['0S', 'KH', 'AC', '3C'], ['JH', 'AD', 'QS', '5H'], ['9C', '8S', 'QH', '9S'], ['8C', '9D', '0D', 'JS'], ['5C', 'AH', '5S', '4C'], ['8H', '2D', '6C', '2C'], ['8D', '4D', 'JD', 'AS'], ['0H', '6S', '2H', 'KC'], ['KS', 'KD', '7S', '6H']], 3, ['QC', '6S', '2H', 'KC', '6C', '2C'])
    # print(discard)

    # print(comp10001go_group([['0S', 'KH', 'AC', '3C'], ['JH', 'AD', 'QS', '5H'], ['9C', '8S', 'QH', '9S'], ['8C', '9D', '0D', 'JS'], ['5C', 'AH', '5S', '4C'], ['8H', '2D', '6C', '2C'], ['8D', '4D', 'JD', 'AS'], ['0H', '6S', '2H', 'KC'], ['KS', 'KD', '7S', '6H'], ['JC', 'QD', '4H', 'QC']], 0))
    # print(comp10001go_best_partitions(['9D', '7H', '6S', '6D', '8S', '1D', 'JH']))
    # print(comp10001go_best_partitions(['9D', '7H', '6S', '6D', 'AS', '1D', 'KH']))
    # print(comp10001go_best_partitions(['0H', '8S', '6H', 'AC', '0S', 'JS', '8C', '7C', '6D', 'QS']))
    # groups = comp10001go_best_partitions(['9D', '7H', '6S', '6D', 'AS', '1D', 'KH'])[0]
    # print(groups)
    # print(comp10001go_valid_groups(groups))
    # print(comp10001go_score_group(['3C', '4H', 'AS']))
    # print(comp10001go_valid_groups([['KC', 'KH', 'KS', 'KD'], ['2C']]))
    print(comp10001go_best_partitions(['8C', '8S', '9D', '0S', '8D', 'JD', '5S', '5C', 'AC', 'AD']))