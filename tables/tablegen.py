def emit(input):
    print(input.rstrip())


def emit_table(name, data, base=0, type='uint8_t'):
    emit('const %s %s[] = {' % (type, name))
    out = '  '
    for i, item in enumerate(data):
        if i and (i % 8 == 0):
            emit(out)
            out = '  '
        h = hex(item - base)
        out += (h.replace('0x', '0x0') if len(h) == 3 else h) + ', '
    emit(out)
    emit('}; // %s' % name)


def encode_line(line, just=48):
    # escape stuff
    line = line.replace('\\', '\\\\')
    line = line.replace('"', '\\"')
    # format
    str  = '  '
    str += '"' + line[0:-1]
    str += '\\x%s"' % hex(ord(line[-1]) | 0x80)[2:]
    str = str.ljust(just)
    str += ' // \'%s\'' % line
    # emit
    emit(str)


def encode_tab36376():
    tab = [
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 2, 2, 2, 2, 2, 2, 130,
        0, 0, 2, 2, 2, 2, 2, 2,
        3, 3, 3, 3, 3, 3, 3, 3,
        3, 3, 2, 2, 2, 2, 2, 2,
        2, 192, 168, 176, 172, 192, 160, 184,
        160, 192, 188, 160, 172, 168, 172, 192,
        160, 160, 172, 180, 164, 192, 168, 168,
        176, 192, 188, 0, 0, 0, 2, 0,
        32, 32, 155, 32, 192, 185, 32, 205,
        163, 76, 138, 142]
    emit('// some flags')
    emit_table('tab36376', tab)


def encode_tab37489():
    ''' depricated, see encode_rule_tab '''
    tab = [
        0, 149, 247, 162, 57, 197, 6, 126,
        199, 38, 55, 78, 145, 241, 85, 161,
        254, 36, 69, 45, 167, 54, 83, 46,
        71, 218]
    emit('// 26 items. From \'A\' to \'Z\'')
    emit('// positions for mem62 and mem63 for each character')
    emit_table('tab37489', tab)


def encode_tab37515():
    ''' depricated, see encode_rule_tab '''
    tab = [
        125, 126, 126, 127, 128, 129, 130, 130,
        130, 132, 132, 132, 132, 132, 133, 135,
        135, 136, 136, 137, 138, 139, 139, 140,
        140, 140]
    emit_table('tab37515', tab)


def encode_rule_tab():
    ''' this table is a combination of the tab37489 and tab37515
        (the msb and lsb respectively).
    '''
    tab = [
        0x7d00, 0x7e95, 0x7ef7, 0x7fa2,
        0x8039, 0x81c5, 0x8206, 0x827e,
        0x82c7, 0x8426, 0x8437, 0x844e,
        0x8491, 0x84f1, 0x8555, 0x87a1,
        0x87fe, 0x8824, 0x8845, 0x892d,
        0x8aa7, 0x8b36, 0x8b53, 0x8c2e,
        0x8c47, 0x8cda]
    emit('// 26 items. From \'A\' to \'Z\'')
    emit('// positions for mem62 and mem63 for each character')
    emit_table('rule_tab', tab, base=0x7d00, type='uint16_t')


def encode_rules_1():
    emit('const int8_t rules[] = {')
    with open('rules_1.txt', 'r') as fd:
        for line in fd.readlines():
            line = line.rstrip('\r\n')
            if line:
                encode_line(line)
            else:
                emit('')
    emit('}; // rules[]')


def encode_rules_2():
    emit('const int8_t rules2[] = {')
    with open('rules_2.txt', 'r') as fd:
        for line in fd.readlines():
            line = line.rstrip('\r\n')
            if line:
                encode_line(line)
            else:
                emit('')
    emit('}; // rules2[]')


def main():
    emit('// Auto generated by "%s", do not modify!' % __file__)
    emit('''\
#ifndef RECITERTABS_H
#define RECITERTABS_H
#include <stdint.h>''')
    emit('')
    encode_tab36376()
    emit('')
    encode_rules_1()
    emit('')
    encode_rules_2()
    emit('')
    '''
    # redundant
    encode_tab37489()
    emit('')
    encode_tab37515()
    '''
    encode_rule_tab()
    emit('''\
#endif
    ''')


if __name__ == '__main__':
    main()
