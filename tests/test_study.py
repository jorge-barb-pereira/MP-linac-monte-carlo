from pathlib import Path
import unittest
import numpy as np
from linac_study.mesh import read_mesh
from linac_study.source import bin_probabilities

ROOT=Path(__file__).resolve().parents[1]


class SourceTests(unittest.TestCase):
    def test_known_cauchy_quartiles(self):
        np.testing.assert_allclose(bin_probabilities([-1,0,1],0,1),[.5,.5])

    def test_exact_cdf_integration(self):
        p=bin_probabilities([0,1,3],0,1)
        self.assertAlmostEqual(p[0], np.arctan(1)/np.arctan(3))
        self.assertAlmostEqual(p.sum(),1)

    def test_symmetric_energy(self):
        p=bin_probabilities(np.linspace(0,12,35),6,.6)
        np.testing.assert_allclose(p,p[::-1],atol=1e-14)

    def test_invalid_inputs(self):
        for edges,location,scale in [([0,0],0,1),([1,0],0,1),([0,1],0,0),
                                      ([0,float('inf')],0,1),([0,1],float('nan'),1),([[0,1]],0,1)]:
            with self.subTest(edges=edges,scale=scale):
                with self.assertRaises(ValueError):bin_probabilities(edges,location,scale)


class MeshTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text=(ROOT/'data/historical/meshtas').read_text(encoding='utf-8')
        cls.histories,cls.meshes=read_mesh(cls.text)

    def test_historical_metadata(self):
        self.assertEqual(self.histories,100320422)
        self.assertEqual([m.number for m in self.meshes],[44,54,64])
        self.assertEqual([m.values.shape for m in self.meshes],[(100,100),(100,100),(250,250)])

    def test_hand_checked_orientation_and_values(self):
        m=self.meshes[0]
        self.assertAlmostEqual(m.values[0,0],3.69273e-7)
        self.assertAlmostEqual(m.values[0,1],2.72361e-7)
        self.assertAlmostEqual(m.values[1,0],4.08477e-7)
        np.testing.assert_allclose(m.z_edges,[-1.25,-.75])

    def test_no_missing_or_nonfinite_data(self):
        for m in self.meshes:
            self.assertEqual(m.values.shape,m.relative_errors.shape)
            self.assertTrue(np.all(np.isfinite(m.values)))
            self.assertTrue(np.all((m.relative_errors>=0)&(m.relative_errors<=1)))

    def test_missing_metadata_rejected(self):
        with self.assertRaises(ValueError):read_mesh('Mesh Tally Number 44')

    def test_truncation_rejected(self):
        with self.assertRaises(ValueError):read_mesh(self.text[:10000])

    def test_coordinate_corruption_rejected(self):
        broken=self.text.replace('-9.90 3.69273E-07','-8.90 3.69273E-07',1)
        with self.assertRaises(ValueError):read_mesh(broken)

    def test_unsupported_particle_rejected(self):
        with self.assertRaises(ValueError):read_mesh(self.text.replace('photon   mesh tally.','neutron  mesh tally.',1))

    def test_invalid_history_count_rejected(self):
        with self.assertRaises(ValueError):read_mesh(self.text.replace('100320422.00','0.00',1))


if __name__=='__main__':unittest.main()
