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

from savanna.openstack.common import log as logging
from savanna.service import api
import savanna.utils.api as u
from savanna.utils.openstack.nova import novaclient

LOG = logging.getLogger(__name__)

rest = u.Rest('v10', __name__)


## Cluster ops

@rest.get('/clusters')
def clusters_list(ctx):
    return u.render(clusters=[c.dict for c in api.get_clusters()])


@rest.post('/clusters')
def clusters_create(data):
    return u.render(api.create_cluster(data).wrapped_dict)


@rest.get('/clusters/<cluster_id>')
def clusters_get(cluster_id):
    return u.render(api.get_cluster(id=cluster_id).wrapped_dict)


@rest.put('/clusters/<cluster_id>')
def clusters_update(cluster_id):
    return u.internal_error(501, NotImplementedError(
        "Cluster update op isn't implemented (id '%s')"
        % cluster_id))


@rest.delete('/clusters/<cluster_id>')
def clusters_delete(cluster_id):
    api.terminate_cluster(id=cluster_id)
    return u.render()


## ClusterTemplate ops

@rest.get('/cluster-templates')
def cluster_templates_list():
    return u.render(
        cluster_templates=[t.dict for t in api.get_cluster_templates()])


@rest.post('/cluster-templates')
def cluster_templates_create(data):
    return u.render(api.create_cluster_template(data).wrapped_dict)


@rest.get('/cluster-templates/<cluster_template_id>')
def cluster_templates_get(cluster_template_id):
    return u.render(
        api.get_cluster_template(id=cluster_template_id).wrapped_dict)


@rest.put('/cluster-templates/<cluster_template_id>')
def cluster_templates_update(_cluster_template_id):
    pass


@rest.delete('/cluster-templates/<cluster_template_id>')
def cluster_templates_delete(cluster_template_id):
    api.terminate_cluster_template(id=cluster_template_id)
    return u.render()


## NodeGroupTemplate ops

@rest.get('/node-group-templates')
def node_group_templates_list():
    return u.render(
        node_group_template=[t.dict for t in api.get_node_group_templates()])


@rest.post('/node-group-templates')
def node_group_templates_create(data):
    return u.render(api.create_node_group_template(data).wrapped_dict)


@rest.get('/node-group-templates/<node_group_template_id>')
def node_group_templates_get(node_group_template_id):
    return u.render(
        api.get_node_group_template(id=node_group_template_id).wrapped_dict)


@rest.put('/node-group-templates/<node_group_template_id>')
def node_group_templates_update(_node_group_template_id):
    pass


@rest.delete('/node-group-templates/<node_group_template_id>')
def node_group_templates_delete(node_group_template_id):
    api.terminate_node_group_template(id=node_group_template_id)
    return u.render()


## Plugins ops

@rest.get('/plugins')
def plugins_list():
    return u.render(plugins=[p.dict for p in api.get_plugins()])


@rest.get('/plugins/<plugin_name>')
def plugins_get(plugin_name):
    return u.render(api.get_plugin(plugin_name).wrapped_dict)


@rest.get('/plugins/<plugin_name>/<version>')
def plugins_get_version(plugin_name, version):
    return u.render(api.get_plugin(plugin_name, version).wrapped_dict)


## Image Registry ops

@rest.get('/images')
def images_list():
    return u.render(
        images=[i.dict for i in novaclient().images.list_registered()])


@rest.get('/images/<image_id>')
def images_get(image_id):
    return u.render(novaclient().images.get(image_id).dict)


def _render_image(image_id, nova):
    return u.render(nova.images.get(image_id).wrapped_dict)


@rest.post('/images/<image_id>')
def images_set(image_id, data):
    nova = novaclient()
    nova.images.set_description(image_id, **data)
    return _render_image(image_id, nova)


@rest.post('/images/<image_id>/tag')
def image_tags_add(image_id, data):
    nova = novaclient()
    nova.images.tag(image_id, **data)
    return _render_image(image_id, nova)


@rest.post('/images/<image_id>/untag')
def image_tags_delete(image_id, data):
    nova = novaclient()
    nova.images.untag(image_id, **data)
    return _render_image(image_id, nova)