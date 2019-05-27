
def fac(n):
    res = 1
    for i in range(1,n+1):
        res *= i
    return res

values = {'J':11 ,'Q':12, 'K':13, 'A': 20}

get_face_value = lambda i:values[i[0]] if i[0] in values else int(i[0])
get_color = lambda i: 'B' if i[1] in 'SC' else 'R'

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
        o_cards.sort(key=lambda card:int(card[0]) if card[0] not in values else values[card[0]])
        print(o_cards)
        # 以下检测N-of-a-kind
        if not a_cards:
            face_values = set([o_card[0] for o_card in o_cards])
            if len(face_values) == 1:
                face_value = face_values.pop()
                if face_value in values:
                    face_value = values[face_value]
                else:
                    face_value = int(face_value)
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
    pass

def comp10001go_group(discard_history, player_no):
    pass

if __name__ == '__main__':
    v = [
        comp10001go_score_group(['2C']),
        comp10001go_score_group(['2C', '2S']),
        comp10001go_score_group(['4C', '4H', '4S']),
        comp10001go_score_group(['4C', '4H', '3S']),
        comp10001go_score_group(['4C', '4H', 'AS']),
        comp10001go_score_group(['KC', 'KH', 'KS', 'KD']),
        comp10001go_score_group(['2C', '3D', '4S']),
        comp10001go_score_group(['4S', '2C', '3D'])
        ]
    print(v)
    v = [
        comp10001go_valid_groups([['KC', 'KH', 'KS', 'KD'], ['2C']]),
        comp10001go_valid_groups([['KC', 'KH', 'KS', 'AD'], ['2C']]),
        comp10001go_valid_groups([['KC', 'KH', 'KS', 'KD'], ['2C', '3H']]),
         comp10001go_valid_groups([])
    ]
    print(v)