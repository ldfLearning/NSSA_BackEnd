import json



if __name__ == '__main__':
    # with open('oldtopo.json', encoding="utf-8") as f:
    #     temp = json.load(f)
    #     load_dict = {'topology_json': json.loads(temp['topology_json'])}
    #     print(load_dict)
    # with open('testtopo.json', "w", encoding='utf-8') as f:
    #     # json.dump(dict_, f) # 写为一行
    #     json.dump(load_dict, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行

    with open('testtopo.json', encoding="utf-8") as f:
        load_dict = json.load(f)
        print(load_dict)
