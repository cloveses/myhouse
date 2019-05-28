
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

        # 前后符合顺子规则
        if get_face_value(remain_cards[0]) == pre_card_val + 1 and get_color(res_cards[-1]) != get_color(remain_cards[0]):
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

def comp10001go_score_group(cards):
    if len(cards) > 1:
        a_cards = [card for card in cards if 'A' in card]
        o_cards = [card for card in cards if 'A' not in card]
        o_cards.sort(key=get_face_value)
        print(o_cards)
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
    hand.sort(key=get_face_value)
    mid = len(hand) // 2
    discard = hand[mid]
    hand.remove(discard)
    if player_no == 0:
        discard_history.append([discard,])
    else:
        discard_history[-1].append(discard)
    return discard

def comp10001go_group(discard_history, player_no):
    return [[cards[player_no],] for cards in discard_history]


def val_col_card(val,col):
    values = {10: '0', 11: 'J', 12: 'Q', 13: 'K'}
    if val in values:
        val = values[val]
    else:
        val = str(val)
    sub_colors = {'B':['S', 'C'], 'R':['H', 'D']}
    return [val + c for c in sub_colors[col]]

def comp10001go_best_partitions(cards):
    o_cards = [card for card in cards if 'A' not in card]
    a_cards = [card for card in cards if 'A' in card]

    runs = []

    for i in range(len(o_cards)):
        o_cards = o_cards[1:]
        start_cart = o_cards[i]
        seq = get_face_value(start_cart)
        colors = ['B', 'R']
        # sub_colors = {'B':['S', 'C'], 'R':['H', 'D']}
        color = get_color(start_cart)
        if colors[0] != color:
            colors = colors[::-1]
        run = [start_cart, ]

        while True:
            seq += 1
            color = colors[seq % 2]
            next_cards = val_col_card(seq, color)
            next_a_cards = set('A'+c[1] for c in next_cards)
            next_card = None
            for c in next_cards:
                if c in o_cards:
                    next_card = c
                    break
            if next_card:
                run.append(next_card)
                o_cards.remove(next_card)
                seq += 1
            elif a_cards and next_a_cards & set(a_cards):
                seq += 1
                next_card = (next_a_cards & set(a_cards)).pop()
                run.append(next_card)
                a_cards.remove(next_card)
            else:
                break
        for i in range(-1,-len(run), -1):
            if 'A' in run[i]:
                run = run[:-1]
            else:
                break
        if len(run) > 2:
            runs.append(run)
    









    

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
    # discard = comp10001go_play([['0S', 'KH', 'AC', '3C'], ['JH', 'AD', 'QS', '5H'], ['9C', '8S', 'QH', '9S'], ['8C', '9D', '0D', 'JS'], ['5C', 'AH', '5S', '4C'], ['8H', '2D', '6C', '2C'], ['8D', '4D', 'JD', 'AS'], ['0H', '6S', '2H', 'KC'], ['KS', 'KD', '7S', '6H']], 3, ['QC'])
    # print(discard)

    # print(comp10001go_group([['0S', 'KH', 'AC', '3C'], ['JH', 'AD', 'QS', '5H'], ['9C', '8S', 'QH', '9S'], ['8C', '9D', '0D', 'JS'], ['5C', 'AH', '5S', '4C'], ['8H', '2D', '6C', '2C'], ['8D', '4D', 'JD', 'AS'], ['0H', '6S', '2H', 'KC'], ['KS', 'KD', '7S', '6H'], ['JC', 'QD', '4H', 'QC']], 3))
    print(comp10001go_best_partitions(['9D', 'AS', '4D', '4H', '6D', 'AH', '2C', 'JH', '3C', '9H']))