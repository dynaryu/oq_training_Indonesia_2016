#!/usr/bin/env python
from __future__ import print_function

__author__ = 'Hyeuk Ryu'

'''
Post-process risk calculation data to convert loss maps into different
formats
'''

import os
from lxml import etree
import matplotlib.pyplot as plt


def fragilityModelParser(input_file):

    def continuousfragilityModelParser(children):

        dict_children= dict()

        for item in children:

            if 'imls' in item.tag:
                dict_children['imt'] = item.attrib['imt']
                dict_children['noDamageLimit'] = float(item.attrib['noDamageLimit'])
                dict_children['iml'] = (item.attrib['minIML'], item.attrib['maxIML'])
            elif 'params' in item.tag:
                limit_state = item.attrib['ls']
                dict_children.setdefault(limit_state, {})['mean'] = item.attrib['mean']
                dict_children.setdefault(limit_state, {})['stddev'] = item.attrib['stddev']

        return dict_children

    def discretefragilityModelParser(children):

        dict_children = dict()

        for item in children:

            if 'imls' in item.tag:
                dict_children['imt'] = item.attrib['imt']
                dict_children['noDamageLimit'] = float(item.attrib['noDamageLimit'])
                dict_children['iml'] = [float(x) for x in item.text.split()]

            elif 'poes' in item.tag:
                limit_state = item.attrib['ls']
                dict_children[limit_state] = [float(x) for x in item.text.split()]

        return dict_children

    frag_model = dict()

    for _, element in etree.iterparse(input_file):

        if 'fragilityFunction' in element.tag:
            taxonomy = element.attrib['id']
            frag_format = element.attrib['format']
            children = element.getchildren()

            if frag_format == 'continuous':
                frag_model[taxonomy] = continuousfragilityModelParser(children)
                frag_model[taxonomy]['shape'] = element.attrib['shape']
            else:
                frag_model[taxonomy] = discretefragilityModelParser(children)

        else:
            continue

    return frag_model

# def plotfragilityModel(frag_model):

#     for taxonomy, item in frag_model.iteritems():
#         plt.figure()



