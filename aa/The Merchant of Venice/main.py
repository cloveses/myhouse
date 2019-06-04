import re
import os
import collections

def get_txt(file_path: str):
    txt = None
    if os.path.exists(file_path):
        with open(file_path) as f:
            txt = f.read()
    return txt

def get_list_scene(txt):
    all_urls = []
    res = re.findall(r'<a.*?href=.*?<\/a>', txt, re.I)
    for url_txt in res:
        urls = re.findall(r'href=["\'](.*?)["\']', url_txt)
        urls = [u for u in urls if u]
        if urls:
            all_urls.extend(urls)
    # print(all_urls)
    return all_urls

def  get_list_tags(file_path: str) -> set:
    txt = get_txt(file_path)
    if not txt:
        return
    tags = re.findall(r'<[^!]*?>', txt, re.S)
    tags = [tag if ' ' not in tag else tag[:tag.index(' ')]+tag[-1] for tag in tags if not tag.startswith('</')]
    counters = collections.Counter(tags)
    return counters

def get_main_info(file_path):
    txt = get_txt(file_path)
    if not txt:
        return
    titles = re.findall(r'<td.*?>(.*?)</td>', txt, re.I|re.S)
    titles = [title.strip() for title in titles]
    title = [title for title in titles if title][0]
    print(title)
    acts = re.findall(r'<p>(.*?)</p>', txt, re.I|re.S)
    # 此处添加获取对应URL
    urls = [get_list_scene(act) for act in acts]
    print(urls)
    acts = [act.strip().split('\n') for act in acts]
    # print(acts)
    for act in acts:
        act_seq = act[0]
        act_seq = act_seq[:act_seq.index(',')]
        scenes = [a[a.index(',')+1:a.index(':')] for a in act]
        scene_names = [re.findall(r'<a.*?>(.*?)</a>', a, re.I)[0] for a in act]
        print(act_seq, scene_names)

        

def get_scene_script(file_path):
    txt = get_txt(file_path)
    if not txt:
        return
    titles = re.findall(r'<i>(.*?)</i>', txt, re.I)
    speeches = re.findall(r'<A NAME=speech\d+><b>(.*?)</b></a>', txt, re.I)
    contents = re.findall(r'<A NAME=speech(.*?</blockquote>)', txt, re.I|re.S)
    contents = [re.findall(r'<blockquote>(.*?)</blockquote>', content, re.I|re.S)[0] for content in contents]
    contents = [re.findall(r'<A NAME=\d+>(.*?)</A>', content, re.I|re.S) for content in contents]
    contents = [[c.strip() for c in content] for content in contents]
    datas = ''
    for t, s, c in zip(titles, speeches, contents):
        datas += ''.join(('*{}*\n'.format(t), '\n**{}**\n\n'.format(s), '\n'.join(c)))
    print(datas)
    return datas

def write_script(file_name: str, content: str):
    with open(file_name, 'a') as f:
        f.write(content)


# def get_tagnum(file_path: str, tag_name: str) -> int:
#     txt = get_txt(file_path)
#     if not txt:
#         return
#     tags = re.findall(r'<[^!]*?>', txt, re.S)
#     tags = [tag if ' ' not in tag else tag[:tag.index(' ')]+tag[-1] for tag in tags if not tag.startswith('</')]
#     print(tags.count(tag_name))
#     return tags.count(tag_name)


if __name__ == '__main__':
    # get_list_scene('./data/Merchant of Venice_ List of Scenes.html')
    # get_scene_script('./data/merchant/merchant.1.1.html')
    # write_script('aa.txt', '11')
    # write_script('aa.txt', '22')
    # get_list_tags('./data/Merchant of Venice_ List of Scenes.html')
    # get_tagnum('./data/Merchant of Venice_ List of Scenes.html', '<p>')
    get_main_info('./data/Merchant of Venice_ List of Scenes.html')
