import simplejson 

from studio.tests import *
from studio.model import *
from studio.tests.lib.helpers import log_in, log_out

class TestDatastoresController(TestController):

    def setUp(self):
        self._clean_datastores()

    def tearDown(self):
        self._clean_datastores()
    
    def test_index(self):
        self._create_datastores()
        log_in(self.app, 'admin', 'password')
        response = self.app.get(url('datastores'))
        assert response.response.content_type == 'application/json'
        response = simplejson.loads(response.response._body)
        assert isinstance(response, dict)
        r = response['datastores']
        assert isinstance(r, list)
        assert len(r) == 2
        log_out(self.app)
        # test anonymous user
        response = self.app.get(url('datastores'), status=302)
        assert response.location.find('signin') >= 0

    def test_create(self):
        params = {'name': 'datastore3',
                  'type': 'postgis',
                  'ogrstring': 'pgsql://titi'}
        log_in(self.app, 'admin', 'password')
        response = self.app.post(url('datastores'),
                                 params = simplejson.dumps(params),
                                 content_type='application/json')
        results = meta.Session.query(DataStore).all()
        assert len(results) == 1
        assert results[0].id == 1
        assert results[0].name == 'datastore3'
        assert results[0].type == 'postgis'
        assert results[0].ogrstring == 'pgsql://titi'
        log_out(self.app)
        # test forbidden user
        log_in(self.app, 'enduser', 'password')
        response = self.app.post(url('datastores'), status=403,
                                 params = simplejson.dumps(params),
                                 content_type='application/json')
        log_out(self.app)
        # test anonymous user
        response = self.app.post(url('datastores'), status=302,
                                 params = simplejson.dumps(params),
                                 content_type='application/json')
        assert response.location.find('signin') >= 0
        
    def test_update(self):
        params = {'name': 'datastore3',
                  'type': 'postgis',
                  'ogrstring': 'pgsql://titi'}
        self._create_datastores()        
        log_in(self.app, 'admin', 'password')
        response = self.app.put(url('DataStores', id=2),
                                params = simplejson.dumps(params),
                                content_type='application/json')
        results = meta.Session.query(DataStore).all()
        assert len(results) == 2
        assert results[1].id == 2
        assert results[1].name == 'datastore3'
        assert results[1].type == 'postgis'
        assert results[1].ogrstring == 'pgsql://titi'        
        log_out(self.app)
        # test forbidden user
        log_in(self.app, 'enduser', 'password')
        response = self.app.put(url('DataStores', id=2), status=403,
                                params = simplejson.dumps(params),
                                content_type='application/json')
        log_out(self.app)
        # test anonymous user
        response = self.app.put(url('DataStores', id=2), status=302,
                                params = simplejson.dumps(params),
                                content_type='application/json')
        assert response.location.find('signin') >= 0

    def test_delete(self):
        self._create_datastores()        
        log_in(self.app, 'admin', 'password')
        response = self.app.delete(url('DataStores', id=1), status=204)
        results = meta.Session.query(DataStore).all()
        assert len(results) == 1
        assert results[0].id == 2
        assert results[0].name == 'datastore2'
        assert results[0].type == 'path'
        assert results[0].ogrstring == 'file://my/path'
        log_out(self.app)
        # test forbidden user
        log_in(self.app, 'enduser', 'password')
        response = self.app.delete(url('DataStores', id=1), status=403)
        log_out(self.app)
        # test anonymous user
        response = self.app.delete(url('DataStores', id=1), status=302)
        assert response.location.find('signin') >= 0

    def test_show(self):
        self._create_datastores()
        log_in(self.app, 'admin', 'password')
        response = self.app.get(url('DataStores', id=1))
        assert response.response.content_type == 'application/json'
        r = simplejson.loads(response.response._body)
        assert r['id'] == 1
        assert r['type'] == 'postgis'
        assert r['ogrstring'] == 'pgsql://toto'
        log_out(self.app)
        # test anonymous user
        response = self.app.get(url('DataStores', id=1), status=302)
        assert response.location.find('signin') >= 0

    def _create_datastores(self):
        meta.Session.add_all([
            DataStore('datastore1', 'postgis', 'pgsql://toto'),
            DataStore('datastore2', 'path', 'file://my/path')
            ])
        meta.Session.commit()

    def _clean_datastores(self):
        meta.Session.query(DataStore).delete()
        meta.Session.commit()
