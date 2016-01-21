#!/usr/bin/env python
from __future__ import print_function

__author__ = 'Hyeuk Ryu'

'''
Post-process risk calculation data to convert loss maps into different
formats
'''

import os
import sys
from lxml import etree
from scipy
import matplotlib.pyplot as plt


class FragilityModel(object):
    '''
    class for a fragility model which is a collection of fragility functions
    '''

    def parse_xml(self, input_file=None):

        if not os.path.exists(input_file):
            print('file {} not found'.format(input_file))
            sys.exit(1)

        self.input_file = input_file

        for _, element in etree.iterparse(input_file):

            if 'fragilityModel' in element.tag:

                self.asset_category = element.attrib['assetCategory']
                self.id = element.attrib['id']
                self.loss_category = element.attrib['lossCategory']
                self.frag = dict()

                for item in element.getchildren():

                    if 'description' in item.tag:
                        self.description = item.text.strip()
                    elif 'limitStates' in item.tag:
                        self.limit_states = item.text.split()
                    elif 'fragilityFunction' in item.tag:
                        taxonomy = item.attrib['id']
                        self.frag[taxonomy] = FragilityFunction(item)


class FragilityFunction(object):

    def __init__(self, element):

        self.taxonomy = element.attrib['id']
        self.frag_format = element.attrib['format']
        children = element.getchildren()

        if self.frag_format == 'continuous':
            self.shape = element.attrib['shape']
            self.continuousfragilityModelParser(children)
        else:
            self.discretefragilityModelParser(children)

    def plot_fragility(self, im_range):
        if self.frag_format == 'continuous':
            self.plot_fragility_continuous(im_range)
        else:
            self.plot_fragility_discrete(im_range)

    def plot_fragility_continuous(self, im_range):


    def plot_fragility_discrete(self, im_range):


    def compute_poes(self, im):

        if self.frag_format == 'continuous':
            est_poes = dict()
            for state, poe_values in self.poes.iteritems():
                est_poes[state] = np.interp(im_range,
                                            self.iml,
                                            poe_values,
                                            left=0.0,
                                            right=1.0)
        else:
            est_poes = dict()
            for state, poe_values in self.poes.iteritems():
                est_poes[state] = np.interp(im_range,
                                            self.iml,
                                            poe_values,
                                            left=0.0,
                                            right=1.0)






        else:
            self.plot_fragility_discrete(im_range)




    def continuousfragilityModelParser(self, children):

        self.params = dict()
        for item in children:

            if 'imls' in item.tag:
                self.imt = item.attrib['imt']
                self.noDamageLimit = float(item.attrib['noDamageLimit'])
                self.iml = (float(item.attrib['minIML']),
                            float(item.attrib['maxIML']))
            elif 'params' in item.tag:
                limit_state = item.attrib['ls']
                self.params[limit_state] = (float(item.attrib['mean']),
                                            float(item.attrib['stddev']))

    def discretefragilityModelParser(self, children):

        self.poes = dict()
        for item in children:

            if 'imls' in item.tag:
                self.imt = item.attrib['imt']
                self.noDamageLimit = float(item.attrib['noDamageLimit'])
                self.iml = [float(x) for x in item.text.split()]

            elif 'poes' in item.tag:
                limit_state = item.attrib['ls']
                self.poes[limit_state] = [float(x) for x in item.text.split()]
