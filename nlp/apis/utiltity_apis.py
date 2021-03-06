import simplejson
from flask import send_file, Blueprint

from data_access import *
from algorithms import *
from .docs import auto
import tasks

utility_app = Blueprint('utility_app', __name__)


@utility_app.route('/')
def home():
    return "Welcome to ClarityNLP!"


@utility_app.route('/job_results/<int:job_id>/<string:job_type>', methods=['GET'])
@auto.doc(groups=['private'])
def get_job_results(job_id: int, job_type: str):
    """GET job results as CSV"""
    try:
        job_output = job_results(job_type, str(job_id))
        return send_file(job_output)
    except Exception as ex:
        return "Failed to get job results" + str(ex)


@utility_app.route('/sections', methods=['GET'])
@auto.doc(groups=['public', 'private', 'utilities'])
def get_section_source():
    """GET source file for sections and synonyms"""
    try:
        file_path = get_sec_tag_source_tags()
        return send_file(file_path)
    except Exception as ex:
        print(ex)
        return "Failed to retrieve sections source file"


@utility_app.route("/report_type_mappings", methods=["GET"])
@auto.doc(groups=['public', 'private', 'utilities'])
def report_type_mappings():
    """GET dictionary of report type mappings"""
    mappings = get_report_type_mappings(util.report_mapper_url, util.report_mapper_inst, util.report_mapper_key)
    return simplejson.dumps(mappings, sort_keys=True, indent=4 * ' ')


@utility_app.route('/pipeline_types', methods=['GET'])
@auto.doc(groups=['public', 'private', 'utilities'])
def pipeline_types():
    """GET valid pipeline types"""
    try:
        return repr(list(tasks.registered_pipelines.keys()))
    except Exception as ex:
        return "Failed to get pipeline types" + str(ex)


@utility_app.route('/status/<int:job_id>', methods=['GET'])
@auto.doc(groups=['public', 'private', 'utilities'])
def get_job_status(job_id: int):
    """GET current job status"""
    try:
        status = jobs.get_job_status(job_id, util.conn_string)
        return json.dumps(status, indent=4)
    except Exception as e:
        return "Failed to get job status" + str(e)
