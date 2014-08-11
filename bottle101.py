#!/usr/bin/env python3
from bottle    import get,  post, request, run, static_file
from copy      import copy
from yaml      import load, dump
from Model     import *
from Validator import *
import signal
import sys


with open('forms.yml',     'r') as f: forms  = load(f)
validator = Validator(forms)

with open('web_ui.yml',    'r') as w: web_ui = load(w)

try:
    with open('companies.yml', 'r') as c: model = load(c)
except IOError as e:
    print(e)
    print('Using sample company as model.')
    model = Model([sample()])
uuids = model.uuids()


def err(text):
    return {'messages' : [{'type' : 'error', 'text' : text}]}


@get('/')
def index():
    return static_file('web_ui.html', './public')

@post('/')
def config():
    return web_ui

@get('/public/:path#.*#')
def public(path):
    return static_file(path, './public')


@post('/tree')
def tree():
    return model.to_json()


@post('/cut')
def cut():
    obj       = uuids[request.params.id]
    commands  = []
    for employee in obj.cut():
        commands.append({'type' : 'edit', 'node' : employee.to_json()})
    return {'commands' : commands}

@post('/depth')
def total():
    obj = uuids[request.params.id]
    return {'messages' : 'Depth: {0}'.format(obj.depth())}

@post('/median')
def total():
    obj = uuids[request.params.id]
    return {'messages' : 'Median: {0}'.format(obj.median())}

@post('/total')
def total():
    obj = uuids[request.params.id]
    return {'messages' : 'Total: {0}'.format(obj.total())}


def field_values(obj, fields):
    values = []
    for f in fields:
        val = copy(f)
        val['value'] = getattr(obj, f['name'])
        values.append(val)
    return values

def get_form(action):
    obj    = uuids[request.params.id]
    type   = request.params.type if action == 'add' else obj.type_name()
    label  = forms[type]['label']
    fields = forms[type]['fields']
    return {
        'commands' : {
            'type'   : 'form',
            'title'  : '{0} {1}'.format(action.capitalize(), label),
            'submit' : 'save/{0}/{1}/{2}'.format(action, type, obj.id),
            'fields' : fields if action == 'add' else field_values(obj, fields),
        },
    }

@post('/add')
def add():
    return get_form('add')

@post('/edit')
def edit():
    return get_form('edit')


@post('/save/<action>/<type>/<id>')
def save(action, type, id):
    valid, result = validator.validate(type, request.params)
    if not valid: return {
        'form'     : {
            'errors'  : result,
        },
        'messages' : {
            'type' : 'error',
            'text' : 'The form data entered was invalid.',
        }
    }

    if action == 'add':
        if type == 'company':
            parent_id   = 'root'
            parent_list = model.children
        else:
            tmp = uuids[id]
            if type not in tmp.child_types():
                return err("{0} can't adopt {1}.".format(id, type))
            parent_id   = tmp.id
            parent_list = tmp.children

        node = globals()[forms[type]['class']](**result)
        uuids[node.id] = node
        parent_list.append(node)

        return {
            'form'     : {'valid' : True},
            'messages' : 'Added {0}'.format(result['text']),
            'commands' : {
                'type'   : 'add',
                'parent' : parent_id,
                'node'   : node.to_json(),
            },
        }
    else:
        node = uuids[id]
        if node.type_name() != type:
            return err('{0} is not a {1}'.format(id, type))

        for k, v in result.items():
            setattr(node, k, v)

        return {
            'form'     : {'valid' : True},
            'messages' : 'Modified {0}'.format(result['text']),
            'commands' : {'type' : 'edit', 'node' : node.to_json()},
        }


def delete_uuids(obj):
    del uuids[obj.id]
    for child in obj.children: delete_uuids(child)

@post('/delete')
def delete():
    obj = uuids[request.params.id]
    if obj.type_name() == 'root':
        return err("Can't delete root.")
    model.remove(obj)
    delete_uuids(obj)
    return {'commands' : {'type' : 'delete', 'id' : obj.id}}


@post('/restructure')
def restructure():
    source = uuids[request.params.id    ]
    target = uuids[request.params.target]

    if source.type_name() not in target.child_types():
        return err('Restructure: Incompatible types.')

    children = target.children
    try:
        pos = int(request.params.pos)
    except AttributeError:
        pos = len(children) - 1

    i, l   = model.remove(source)
    offset = pos - 1 if l is children and pos >= i else pos
    children.insert(offset, source)

    return {
        'commands' : {
            'type'   : 'move',
            'source' : source.id,
            'target' : target.id,
            'pos'    : pos,
        },
    }


# Exit gracefully on interrupt
def sigint(signal, frame):
    try:
        with open('companies.yml', 'w') as c:
            c.write(dump(model))
    except:
        print("Couldn't write to companies.yml.")
    sys.exit(0)
signal.signal(signal.SIGINT, sigint)


run(port = 3000)
