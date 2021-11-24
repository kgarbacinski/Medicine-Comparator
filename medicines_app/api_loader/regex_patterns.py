from enum import Enum


class RegexPatterns(Enum):
    primary_pair_regex = r'^(\d[\d\ \.\-x\^]*)(([\w\.]*)[\w\+\ \(\)\.]*\/(([\d\.]*)? ?([\w]*))|([\w\.\%]*))?'
    brackets_regex = r'^\((.*)\) ?\/((\d*\.*\,*\d*) *(.*))'