
#----------------------------------------------------
'''权限管理生成菜单树'''
def getPermissionTree(menu_list, includeBtn=True):
    # print("="*50)
    # print(menu_list)
    # print("="*50)
    # 处理数据
    menu_map = {}
    for item in menu_list:

        # 如果包含按钮，则渲染宣布菜单
        if includeBtn:
            item["children"] = []
            menu_map[item["id"]] = item
            continue
        # 如果 includeBtn=False 代表用户第请求获取后台菜单树，不包含按钮权限
        # item['menu'] != 1  不包含按钮标识数字
        if not includeBtn and item['menu'] != 1 or item['status'] == 0:
            continue

        item["children"] = []
        menu_map[item["id"]] = item

    tree = []
    for item in menu_map.values():
        if menu_map.get(item["parent_id"]): # 找儿子
            menu_map[item["parent_id"]]["children"].append(item)
            menu_map[item["parent_id"]]["children"].sort(key=lambda x: x['sort'], reverse=False)
        else: # 找出所有的顶级
            tree.append(item)
    
        
    tree.sort(key=lambda x: x['sort'], reverse=False)

    return tree



#----------------------------------------------------