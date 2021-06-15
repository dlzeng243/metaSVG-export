'''
client
======

Convenience functions for working with the Onshape API
'''

from onshape import Onshape

import mimetypes
import random
import string
import os

'''
Need get feature list
Need update feature

'''
class Client():
    '''
    Defines methods for testing the Onshape API. Comes with several methods:

    - Create a document
    - Delete a document
    - Get a list of documents

    Attributes:
        - stack (str, default='https://cad.onshape.com'): Base URL
        - logging (bool, default=True): Turn logging on or off
    '''

    def __init__(self, stack='https://cad.onshape.com', logging=True):
        '''
        Instantiates a new Onshape client.

        Args:
            - stack (str, default='https://cad.onshape.com'): Base URL
            - logging (bool, default=True): Turn logging on or off
        '''

        self._stack = stack
        self._api = Onshape(stack=stack, logging=logging)

    def new_document(self, name='Test Document', owner_type=0, public=False):
        '''
        Create a new document.

        Args:
            - name (str, default='Test Document'): The doc name
            - owner_type (int, default=0): 0 for user, 1 for company, 2 for team
            - public (bool, default=False): Whether or not to make doc public

        Returns:
            - requests.Response: Onshape response data
        '''

        payload = {
            'name': name,
            'ownerType': owner_type,
            'isPublic': public
        }

        return self._api.request('post', '/api/documents', body=payload)

    def rename_document(self, did, name):
        '''
        Renames the specified document.

        Args:
            - did (str): Document ID
            - name (str): New document name

        Returns:
            - requests.Response: Onshape response data
        '''

        payload = {
            'name': name
        }

        return self._api.request('post', '/api/documents/' + did, body=payload)

    def del_document(self, did):
        '''
        Delete the specified document.

        Args:
            - did (str): Document ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('delete', '/api/documents/' + did)

    def get_document(self, did):
        '''
        Get details for a specified document.

        Args:
            - did (str): Document ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('get', '/api/documents/' + did)

    def list_documents(self):
        '''
        Get list of documents for current user.

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('get', '/api/documents')

    def create_assembly(self, did, wid, name='My Assembly'):
        '''
        Creates a new assembly element in the specified document / workspace.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - name (str, default='My Assembly')

        Returns:
            - requests.Response: Onshape response data
        '''

        payload = {
            'name': name
        }

        return self._api.request('post', '/api/assemblies/d/' + did + '/w/' + wid, body=payload)

    def get_parts(self, did, wid):
        '''
        Gets the part list for specified document / workspace / part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('get', '/api/parts/d/' + did + '/w/' + wid)

    def get_body_details(self, did, wid, eid, pid):
        '''
        Gets the body details of a specific part.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element Id
            - pid (str): Part Id

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('get', '/api/parts/d/' + did + '/w/' + wid + '/e/' + eid + '/partid/' + pid + '/bodydetails' )

    def get_features(self, did, wid, eid):
        '''
        Gets the feature list for specified document / workspace / part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('get', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/features')

    def update_feature(self, did, wid, eid, payload):
        '''
        Updates a feature for specified document / workspace / part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('post', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/features/updates', body=payload)

    def add_feature(self, did, wid, eid, payload):
        '''
        Adds a feature for specified document / workspace / part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID
            - payload (json): Feature to be added

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('post', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/features', body=payload)
    def evaluate_feature(self, did, wid, eid, payload):
        '''
        Evaluates a feature for specified document / workspace / part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID
            - payload (json): Feature to be added

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('post', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/featurescript', body=payload)

    def delete_feature(self, did, wid, eid, fid):
        '''
        Deletes a feature for specified document / workspace / part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID
            - fid (str): Feature ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('delete', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/features/featureid/' + fid)


