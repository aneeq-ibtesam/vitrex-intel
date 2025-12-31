from flask import render_template, abort, request
from . import web
from app.extensions import mongo

@web.route('/')
def index():
    if mongo.db is None:
        return render_template('dashboard.html', stats={}, latest_iocs=[])
        
    stats = {
        'total_iocs': mongo.db.iocs.count_documents({}),
        'limo_count': mongo.db.iocs.count_documents({'labels': 'limo'}), # Assuming label
        'abuse_count': mongo.db.iocs.count_documents({'labels': {'$in': ['urlhaus', 'feodotracker']}}),
        'tor_count': mongo.db.iocs.count_documents({'labels': 'tor-exit-node'})
    }
    
    latest_iocs = list(mongo.db.iocs.find().sort('created', -1).limit(10))
    
    return render_template('dashboard.html', stats=stats, latest_iocs=latest_iocs)

@web.route('/iocs')
def ioc_list():
    if mongo.db is None:
        return render_template('ioc_list.html', iocs=[])
    
    source_filter = request.args.get('source')
    type_filter = request.args.get('type')
    query = {}
    
    if source_filter:
        if source_filter == 'limo':
            query['labels'] = 'limo'
        elif source_filter == 'abusech':
            query['labels'] = {'$in': ['urlhaus', 'feodotracker']}
        elif source_filter == 'tor':
            query['labels'] = 'tor-exit-node'
            
    if type_filter:
        if type_filter == 'ip':
            query['pattern'] = {'$regex': 'ipv4-addr'}
        elif type_filter == 'url':
            query['pattern'] = {'$regex': 'url'}
        elif type_filter == 'file':
            query['pattern'] = {'$regex': 'file'}
            
    iocs = list(mongo.db.iocs.find(query).sort('created', -1).limit(100))
    return render_template('ioc_list.html', iocs=iocs, active_filter=source_filter, active_type=type_filter)

@web.route('/ioc/<ioc_id>')
def ioc_detail(ioc_id):
    if mongo.db is None:
        abort(500)
    
    ioc = mongo.db.iocs.find_one({'id': ioc_id})
    if not ioc:
        abort(404)
    
    # Fix ObjectId serialization
    if '_id' in ioc:
        ioc['_id'] = str(ioc['_id'])
        
    return render_template('ioc_detail.html', ioc=ioc)
