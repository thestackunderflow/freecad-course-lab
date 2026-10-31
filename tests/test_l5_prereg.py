"""Lesson 5: the pre-registered messages are what prereg.json says they are (B-1 = A-1 + a space + one sentence)."""
import json
import os

LAB = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
M = os.path.join(LAB, 'out', 'l5', 'messages')


def read(n):
    return open(os.path.join(M, n), encoding='utf-8').read().rstrip('\n')


def test_b1_is_a1_plus_one_sentence():
    a, b = read('A-1.txt'), read('B-1.txt')
    assert b.startswith(a + ' ')
    extra = b[len(a) + 1:]
    assert extra.startswith('Then check that STL') and extra.count('. ') == 0 and extra.endswith('volume.')


def test_message_two_is_the_same():
    assert read('A-2.txt') == read('B-2.txt')


def test_prereg_names_two_runs_at_most():
    p = json.load(open(os.path.join(LAB, 'out', 'l5', 'prereg.json'), encoding='utf-8'))
    assert p['max_runs'] == 2 and p['order'] == ['B1', 'A1']
