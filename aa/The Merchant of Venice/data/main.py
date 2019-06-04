import re
import os
import collections

def get_txt(file_path: str):
    txt = None
    if os.path.isfile(file_path) and os.path.exists(file_path):
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
    return all_urls

def  get_count_tags(txt):
    if not txt:
        return
    txt = txt.lower()
    tags = re.findall(r'<[^!]*?>', txt, re.S)
    tags = [tag if ' ' not in tag else tag[:tag.index(' ')]+tag[-1] for tag in tags if not tag.startswith('</')]
    counters = collections.Counter(tags)
    return counters

def get_scene_script(file_path):
    txt = get_txt(file_path)
    if not txt:
        return
    counter = get_count_tags(txt)
    titles = re.findall(r'<i>(.*?)</i>', txt, re.I)
    speeches = re.findall(r'<A NAME=speech\d+><b>(.*?)</b></a>', txt, re.I)
    contents = re.findall(r'<A NAME=speech(.*?</blockquote>)', txt, re.I|re.S)
    contents = [re.findall(r'<blockquote>(.*?)</blockquote>', content, re.I|re.S)[0] for content in contents]
    contents = [re.findall(r'<A NAME=\d+>(.*?)</A>', content, re.I|re.S) for content in contents]
    contents = [[c.strip() for c in content] for content in contents]
    datas = ''
    for t, s, cs in zip(titles, speeches, contents):
        t = '\n*{}*\n'.format(t)
        s = '\n**{}**\n\n'.format(s)
        cs = ''.join([''.join((c, '\n')) for c in cs])
        datas = ''.join((t,s,cs))
    return datas, counter

def write_script(file_name: str, content: str):
    with open(file_name, 'w') as f:
        f.write(content)

def get_main_info(file_path):
    all_datas = []
    txt = get_txt(file_path)
    if not txt:
        return
    all_counter = get_count_tags(txt)
    titles = re.findall(r'<td.*?>(.*?)</td>', txt, re.I|re.S)
    titles = [title.strip() for title in titles]
    title = [title for title in titles if title][0]
    title = '\n{} {}\n\n'.format('#',title)
    all_datas.append(title)
    acts = re.findall(r'<p>(.*?)</p>', txt, re.I|re.S)
    # 此处获取对应URL
    urls = [get_list_scene(act) for act in acts]
    acts = [act.strip().split('\n') for act in acts]
    for act in acts:
        act_seq = act[0]
        act_seq = act_seq[:act_seq.index(',')]
        scenes = [a[a.index(',')+1:a.index(':')] for a in act]
        scene_names = [re.findall(r'<a.*?>(.*?)</a>', a, re.I)[0] for a in act]
        all_datas.append('## {}\n\n'.format(act_seq))
        for scene_name, url in zip(scene_names, urls):
            all_datas.append('### {}\n'.format(scene_name))
            for u in url:
                datas, counter = get_scene_script(u)
                all_datas.append(datas)
                all_counter.update(counter)
            all_datas.append('\n')
    write_script('res.txt', ''.join(all_datas))
    counter = [(k, all_counter[k]) for k in all_counter]
    counter.sort(key=lambda x:x[1])
    counter = counter[-3:]
    for k,v in counter[::-1]:
        print(k,v)

if __name__ == '__main__':
    get_main_info('Merchant of Venice_ List of Scenes.html')
