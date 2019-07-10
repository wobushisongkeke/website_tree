import traverse_result_1
import settings
import collections


class BuildTree:

    """use the traverse_result to build a static tree, and produce a .md file"""

    def __init__(self):
        self.index = traverse_result_1.index
        self.md_path = settings.MARKDOWN_PATH

        self.root = None

        if len(self.index) > 0:
            self.root_index = 0
        else:
            print("illegal index")

        self.d = collections.OrderedDict()

    def _find_root(self):
        # use referer_count to define the root
        root_list = []
        max_refer_count = self.index[self.root_index]["referer_count"]
        for i in range(len(self.index)):
            if self.index[i]["referer_count"] > max_refer_count:
                max_refer_count = self.index[i]["referer_count"]
        for i in range(len(self.index)):
            if self.index[i]["referer_count"] == max_refer_count:
                root_list.append(self.index[i])

        if len(root_list) == 1:
            return root_list[0]
        else:
            # use url hierarchy to define the root
            root_list_hierarchy = []
            min_hierarchy = len(root_list[0]["url"].split("/"))
            for i in range(len(root_list)):
                if len(root_list[i]["url"].split("/")) < min_hierarchy:
                    min_hierarchy = len(root_list[i]["url"].split("/"))
            for i in range(len(root_list)):
                if len(root_list[i]["url"].split("/")) == min_hierarchy:
                    root_list_hierarchy.append(root_list[i])

            if len(root_list_hierarchy) == 1:
                return root_list_hierarchy[0]
            else:
                # use inner_link to define the root
                root_list_inner = []
                max_inner = root_list_hierarchy[0]["inner_link_count"]
                for i in range(len(root_list_hierarchy)):
                    if root_list_hierarchy[i]["inner_link_count"] > max_inner:
                        max_inner = root_list_hierarchy[i]["inner_link_count"]
                for i in range(len(root_list_hierarchy)):
                    if root_list_hierarchy[i]["inner_link_count"] == max_inner:
                        root_list_inner.append(root_list_hierarchy[i])
                return root_list_inner[0]

    def _find_parents(self, obj):
        if "parents" in obj:
            return obj["parents"]
        else:
            contain = []
            for i in range(len(self.index)):
                uo = self.index[i]
                if uo['url'] != obj['url'] and obj['url'] in uo["inner_link"]:
                    contain.append(i)

            if len(contain) == 0:
                obj["parents"] = -1
                return obj["parents"]
            elif len(contain) == 1:
                obj["parents"] = contain[0]
                return obj["parents"]
            else:
                max_referer = 0
                refer_count_contain = []
                for i in contain:
                    if self.index[i]["referer_count"] > max_referer:
                        max_referer = self.index[i]["referer_count"]
                for i in contain:
                    if self.index[i]["referer_count"] == max_referer:
                        refer_count_contain.append(i)

                if len(refer_count_contain) == 1:
                    obj["parents"] = refer_count_contain[0]
                    return obj["parents"]
                else:
                    max_inner = 0
                    for i in contain:
                        if self.index[i]["inner_link_count"] > max_inner:
                            max_inner = self.index[i]["inner_link_count"]
                    for i in contain:
                        if self.index[i]["inner_link_count"] == max_inner:
                            obj["parents"] = i
                            return obj["parents"]

            return obj["parents"]

    def construct_tree(self):
        self.root = self._find_root()
        self.root["parents"] = -1
        for dic in self.index:
            self._find_parents(dic)

    def _traverse_tree(self):
        level = 0
        self.d[self.root['url']] = level
        self._pre_order(self.root['url'], level)

    def _pre_order(self, url, level):
        all_children = []

        # find the index of the url
        for i in range(len(self.index)):
            dic = self.index[i]
            if dic['url'] == url:
                break

        for uo in self.index:
            if uo["parents"] == i:
                all_children.append(uo["url"])

        # leaves or middle node
        if len(all_children) == 0:
            self.d[url] = level
        else:
            self.d[url] = level
            for child in all_children:
                self._pre_order(child, level+1)

    def tree2md(self):
        self._traverse_tree()
        with open(self.md_path, "w") as f:
            for k, v in self.d.items():
                head = "#" * (v+1) + " "
                content = head + k + "\n"
                f.write(content)


def main():
    """An example to construct a tree and form a .md file"""
    bt = BuildTree()
    bt.construct_tree()
    bt.tree2md()


if __name__ == "__main__":
    main()
