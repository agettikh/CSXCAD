# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 21:47:29 2015

@author: thorsten
"""

import numpy as np

from CSXCAD import ParameterObjects
from CSXCAD import CSProperties

import unittest

class Test_CSPrimMethods(unittest.TestCase):
    def setUp(self):
        self.pset  = ParameterObjects.ParameterSet()

    def test_metal(self):
        prop = CSProperties.CSPropMetal(self.pset)

        self.assertEqual( prop.GetType(), CSProperties.METAL)
        self.assertEqual( prop.GetTypeString(), 'Metal')

    def test_material(self):
        prop = CSProperties.CSPropMaterial(self.pset, epsilon = 5.0)

        self.assertEqual( prop.GetType(), CSProperties.MATERIAL)
        self.assertEqual( prop.GetTypeString(), 'Material')

        self.assertEqual( prop.GetMaterialProperty('epsilon'), 5.0)
        self.assertEqual( prop.GetMaterialProperty('mue'), 1.0)

#        print(CSX.GetQtyProperties())

        prop.SetMaterialProperty(epsilon=[1.0, 2.0, 3.0], mue=2.0)
        self.assertEqual( prop.GetMaterialProperty('epsilon'), 1.0)
        self.assertEqual( prop.GetMaterialProperty('mue'), 2.0)

        prop.SetMaterialWeight(epsilon=['sin(x)', 'y', 'z'],  mue='cos(y)', density='z*z')
        self.assertEqual( prop.GetMaterialWeight('epsilon'), 'sin(x)')
        self.assertEqual( prop.GetMaterialWeight('mue'), 'cos(y)')
        self.assertEqual( prop.GetMaterialWeight('density'), 'z*z')

        prop.SetIsotropy(False)
        self.assertFalse( prop.GetIsotropy(),False)
        self.assertTrue( (prop.GetMaterialProperty('epsilon')==[1.0, 2.0, 3.0]).all())

    def test_lumped_elem(self):
        prop = CSProperties.CSPropLumpedElement(self.pset, R = 50, C=1e-12, caps=True, ny='x')

        self.assertEqual( prop.GetType(), CSProperties.LUMPED_ELEMENT)
        self.assertEqual( prop.GetTypeString(), 'LumpedElement')

        self.assertEqual( prop.GetResistance(), 50)
        prop.SetResistance(55.0)
        prop.SetDirection('x')
        self.assertEqual( prop.GetResistance(), 55)
        self.assertEqual( prop.GetCapacity(), 1e-12)
        self.assertTrue( prop.GetCaps())
        prop.SetCaps(False)
        self.assertFalse( prop.GetCaps())
        self.assertEqual( prop.GetDirection(), 0)

    def test_cond_sheet(self):
        prop = CSProperties.CSPropConductingSheet(self.pset, conductivity=56e6, thickness=35e-6)

        self.assertEqual( prop.GetType(), CSProperties.CONDUCTINGSHEET + CSProperties.METAL)
        self.assertEqual( prop.GetTypeString(), 'ConductingSheet')

        self.assertEqual( prop.GetConductivity(), 56e6)
        self.assertEqual( prop.GetThickness(), 35e-6)

    def test_excitation(self):
        prop = CSProperties.CSPropExcitation(self.pset,  exc_type=1, exc_val=[-1.0, 0, 1.0], delay=1e-9)

        self.assertEqual( prop.GetType(), CSProperties.EXCITATION)
        self.assertEqual( prop.GetTypeString(), 'Excitation')

        self.assertEqual( prop.GetExcitType(), 1)
        self.assertTrue( (prop.GetExcitation()==[-1.0, 0, 1.0]).all() )
        self.assertEqual( prop.GetDelay(),1e-9)

    def test_probe(self):
        prop = CSProperties.CSPropProbeBox(self.pset)

        self.assertEqual( prop.GetType(), CSProperties.PROBEBOX)
        self.assertEqual( prop.GetTypeString(), 'ProbeBox')

    def test_dump(self):
        prop = CSProperties.CSPropDumpBox(self.pset)

        self.assertEqual( prop.GetType(), CSProperties.DUMPBOX)
        self.assertEqual( prop.GetTypeString(), 'DumpBox')

if __name__ == '__main__':
    unittest.main()