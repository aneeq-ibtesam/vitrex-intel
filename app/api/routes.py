from flask import jsonify, request
from . import api
from app.ingestor.manager import IngestionManager
from app.enricher.vt import VirusTotalEnricher

# Instantiate global manager (in a real app, use app context or singleton)
ingestion_manager = IngestionManager()
enricher = VirusTotalEnricher()

@api.route('/status')
def status():
    return jsonify({'status': 'ok'})

@api.route('/ingest/trigger')
def trigger_ingest():
    # Run synchronously for better UI feedback
    stats = ingestion_manager.run_sync_ingestion()
    return jsonify({
        'message': 'Ingestion completed successfully',
        'stats': stats
    })

@api.route('/enrich')
def enrich():
    ioc_type = request.args.get('type')
    ioc_value = request.args.get('value')
    
    if not ioc_type or not ioc_value:
        return jsonify({'error': 'Missing type or value'}), 400
        
    result = enricher.enrich_ioc(ioc_value, ioc_type)
    return jsonify(result)
