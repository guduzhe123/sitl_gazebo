#-*- coding:utf-8 -*-
import xml.dom.minidom

# 在内存中创建一个空的文档
doc = xml.dom.minidom.Document()

mesh_size = 80
grass_number = 3

# 创建一个根节点Managers对象
root = doc.createElement('sdf')
# 设置根节点的属性
root.setAttribute('version', '1.4')
doc.appendChild(root)

model = doc.createElement('model')
model.setAttribute('name', 'grass_plane')
root.appendChild(model)

static = doc.createElement('static')
static.appendChild(doc.createTextNode('true'))
model.appendChild(static)

link = doc.createElement('link')
link.setAttribute('name', 'link')
model.appendChild(link)


# add collision
collision = doc.createElement('collision')
collision.setAttribute('name', 'collision')
# geometry
geometry = doc.createElement('geometry')
plane = doc.createElement('plane')
geometry.appendChild(plane)
normal = doc.createElement('normal')
normal.appendChild(doc.createTextNode('0 0 1'))
plane.appendChild(normal)
size = doc.createElement('size')
collision_size = mesh_size * grass_number
size.appendChild(doc.createTextNode(str(collision_size) + ' ' + str(collision_size)))
plane.appendChild(size)
collision.appendChild(geometry)
# surface
surface = doc.createElement('surface')
friction = doc.createElement('friction')
surface.appendChild(friction)
ode = doc.createElement('ode')
friction.appendChild(ode)
mu = doc.createElement('mu')
mu.appendChild(doc.createTextNode('0.5'))
ode.appendChild(mu)
mu2 = doc.createElement('mu2')
mu2.appendChild(doc.createTextNode('0.5'))
ode.appendChild(mu2)
name = doc.createElement('name')
name.appendChild(doc.createTextNode('vrc/grass'))
friction.appendChild(name)
collision.appendChild(surface)

link.appendChild(collision)

# 10*10 = 100
for i in range(grass_number):
    for j in range(grass_number):
        visual = doc.createElement('visual')
        sn = i * grass_number + j
        visual.setAttribute('name', 'visual_' + str(sn))
        print(sn, i, j)

        # pose
        pose = doc.createElement('pose')
        x = mesh_size * i
        y = mesh_size * j
        pose.appendChild(doc.createTextNode(str(x) + ' ' + str(y) + ' 0 0 0 0'))
        visual.appendChild(pose)

        # cast_shadows
        cast_shadows = doc.createElement('cast_shadows')
        cast_shadows.appendChild(doc.createTextNode('false'))
        visual.appendChild(cast_shadows)

        # geometry
        geometry = doc.createElement('geometry')
        plane = doc.createElement('plane')
        geometry.appendChild(plane)
        normal = doc.createElement('normal')
        normal.appendChild(doc.createTextNode('0 0 1'))
        plane.appendChild(normal)
        size = doc.createElement('size')
        size.appendChild(doc.createTextNode(str(mesh_size) + ' ' + str(mesh_size)))
        plane.appendChild(size)
        visual.appendChild(geometry)

        # material
        material = doc.createElement('material')
        script = doc.createElement('script')
        material.appendChild(script)
        uri = doc.createElement('uri')
        uri.appendChild(doc.createTextNode('model://grass_plane/materials/scripts'))
        script.appendChild(uri)
        uri = doc.createElement('uri')
        uri.appendChild(doc.createTextNode('model://grass_plane/materials/textures'))
        script.appendChild(uri)
        name = doc.createElement('name')
        name.appendChild(doc.createTextNode('vrc/grass'))
        script.appendChild(name)
        visual.appendChild(material)

        link.appendChild(visual)

# 开始写xml文档
fp = open('model.sdf', 'w')
doc.writexml(fp, indent='  ', addindent='  ', newl='\n')
