# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest2

from savanna.conductor import resource as r
from savanna.utils import types

SAMPLE_DICT = {
    'first': [1, 2],
    'second': {'a': 1, 'b': 2}
}


SAMPLE_CLUSTER_DICT = {
    'name': 'test-cluster',
    'cluster_configs': {
        'general': {
            'some_overridden_config': 'somevalue'
        }
    },
    'node_groups': [
        {
            'name': 'master',
        },
        {
            'name': 'worker',
            'node_processes': ['tasktracker', 'datanode'],
            'node_configs': {},
            'instances': [
                {
                    'name': 'test-cluster-001',
                    'ip': '1.1.1.1'
                }
            ]
        }
    ]
}


class TestResource(unittest2.TestCase):
    def test_resource_creation(self):
        res = r.Resource(SAMPLE_DICT)

        self.assertIsInstance(res.first, list)
        self.assertEqual(res.first, [1, 2])
        self.assertIsInstance(res.second, r.Resource)
        self.assertEqual(res.second.a, 1)
        self.assertEqual(res.second.b, 2)

    def test_resource_immutability(self):
        res = r.Resource(SAMPLE_DICT)

        with self.assertRaises(types.FrozenClassError):
            res.first.append(123)

        with self.assertRaises(types.FrozenClassError):
            res.first = 123

        with self.assertRaises(types.FrozenClassError):
            res.second.a = 123

    def test_cluster_resource(self):
        cluster = r.ClusterResource(SAMPLE_CLUSTER_DICT)

        self.assertEqual(cluster.name, 'test-cluster')

        self.assertEqual(cluster.node_groups[0].name, 'master')
        self.assertIsInstance(cluster.node_groups[0], r.NodeGroupResource)
        self.assertEqual(cluster.node_groups[0].cluster.name, 'test-cluster')

        self.assertEqual(cluster.node_groups[1].instances[0].name,
                         'test-cluster-001')
        self.assertIsInstance(cluster.node_groups[1].instances[0],
                              r.InstanceResource)
        self.assertEqual(
            cluster.node_groups[1].instances[0].node_group.name,
            'worker')
