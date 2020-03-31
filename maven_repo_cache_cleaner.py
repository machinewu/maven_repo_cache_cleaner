#!/usr/bin/env python
# coding=utf-8

__author__ = 'machinewu'

import os
import time


class DDir:
    def __init__(self, value, depth):
        self.v = value  # value
        self.d = depth  # depth


_rule_func = lambda x: False


def check_to_clean(ddir):
    global _rule_func
    if _rule_func(ddir):
        clean_dir(ddir)


def clean_dir(ddir):
    for f in os.listdir(ddir.v):
        if f != "." and f != "..":
            os.remove(os.path.join(ddir.v, f))

    if ddir.d > 0:
        print("Clean dir: " + ddir.v)
        os.removedirs(ddir.v)


def walk_dir(ddir):
    has_sub_dir = False
    for _dir in [x for x in [os.path.join(ddir.v, d) for d in os.listdir(ddir.v) if not d.startswith(".")] if os.path.isdir(x)]:
        walk_dir(DDir(_dir, ddir.d + 1))
        has_sub_dir = True

    if not has_sub_dir:
        check_to_clean(ddir)


def run(path, rule_func):
    global _rule_func
    _rule_func = rule_func

    walk_dir(DDir(os.path.abspath(path), 0))


def rule_func1(ddir, modified_date):
    # Purge based on time of file _remote.repositories
    meta_file = os.path.join(ddir.v, "_remote.repositories")
    if not os.path.isfile(meta_file):
        meta_file = os.path.join(ddir.v, "_maven.repositories")
        if not os.path.isfile(meta_file):
            return False

    meta_mod_time = time.strftime('%Y-%m-%d', time.localtime(os.stat(meta_file).st_mtime))
    return os.path.isfile(meta_file) and meta_mod_time < modified_date


if __name__ == "__main__":
    maven_repo_path = str(raw_input("Input maven repo path (e.g ${user.home}/.m2/repository):")).strip()
    modified_date = str(raw_input("Clean the modified date of _remote.repositories before your input date (exclude this date YYYY-MM-DD):")).strip()
    run(maven_repo_path, lambda x: rule_func1(x, modified_date))
