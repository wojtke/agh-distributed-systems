import logging
import time
import tkinter as tk
from tkinter import ttk
from kazoo.client import KazooClient


logging.basicConfig(level=logging.INFO)

ZNODE_PATH = "/z"


class ZooKeeperApp:
    def __init__(self):
        self.zk = KazooClient(hosts="127.0.0.1:2181")
        self.children = set()

        self.gui = ZooKeeperGUI()

        self.zk.start()

        logging.info("Connected to ZooKeeper")

    def watch(self, path=ZNODE_PATH):
        logging.info(f"Watching {path}")
        if self.zk.exists(ZNODE_PATH, watch=self.on_node_changed):
            logging.info(f"Node {ZNODE_PATH} exists")
            self.gui.root.deiconify()
            self.zk.ChildrenWatch(ZNODE_PATH)(self.on_children_changed)
        else:
            logging.info(f"Node {ZNODE_PATH} does not exist")
            self.gui.root.withdraw()

    def run(self):
        logging.info("Running ZooKeeperApp")
        self.gui.root.after(1000, self.watch)
        self.gui.root.mainloop()

    def on_node_changed(self, event):
        logging.info(f"Node {event.path} changed: {event.type}")
        if event.type == "DELETED":
            self.gui.root.withdraw()
            self.zk.exists(ZNODE_PATH, watch=self.on_node_changed)
        elif event.type == "CREATED":
            self.gui.root.deiconify()
            self.zk.exists(ZNODE_PATH, watch=self.on_node_changed)
            self.zk.ChildrenWatch(ZNODE_PATH)(self.on_children_changed)

    def on_children_changed(self, children, path=ZNODE_PATH):
        logging.info(f"Children of {path} changed, new children: {children}")
        for child in children:

            child_path = path + "/" + child
            self.zk.ChildrenWatch(child_path)(lambda ch: self.on_children_changed(ch, child_path))
            logging.info(f"Watching {child_path}")
            self.children.add(child_path)

        tree, n = self.build_children_tree()
        self.gui.update_children(n-1)
        self.gui.update_treeview(tree)

    def build_children_tree(self, path = ZNODE_PATH):
        n = 1
        children = self.zk.get_children(path)
        tree = {"name": path, "children": []}
        for child in children:
            child_tree, child_n = self.build_children_tree(path + "/" + child)
            tree["children"].append(child_tree)
            n += child_n
        return tree, n

    def stop(self):
        logging.info("Stopping ZooKeeperApp")
        self.zk.stop()


class ZooKeeperGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title("ZooKeeper GUI")

        self.child_count_label = tk.Label(self.root, text="Descendants of /z: 0", font=("Arial", 12))
        self.child_count_label.pack(pady=5)

        self.treeview_frame = tk.Frame(self.root)
        self.treeview_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.treeview = ttk.Treeview(self.treeview_frame, show="tree", height=10)
        self.treeview.heading("#0", text="Node Structure", anchor="w")
        self.treeview.pack(side="left", fill=tk.BOTH, expand=True)

        self.treeview_scrollbar = ttk.Scrollbar(self.treeview_frame, orient="vertical", command=self.treeview.yview)
        self.treeview_scrollbar.pack(side="right", fill="y")

        self.treeview.configure(yscrollcommand=self.treeview_scrollbar.set)

    def update_children(self, n):
        self.child_count_label.config(text=f"Descendants of /z: {n}")

        # self.children_listbox.delete(0, tk.END)
        # for child in children:
        #     self.children_listbox.insert(tk.END, child)

    def update_treeview(self, children_tree):
        self.treeview.delete(*self.treeview.get_children())
        self._populate_treeview(children_tree, "")

    def _populate_treeview(self, children_tree, parent):
        node_id = self.treeview.insert(parent, "end", text=children_tree["name"], open=True)
        for child in children_tree["children"]:
            self._populate_treeview(child, node_id)


if __name__ == "__main__":
    app = ZooKeeperApp()
    try:
        app.run()
    except KeyboardInterrupt:
        pass
