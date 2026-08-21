# coding: utf-8
from pytest import raises
from pathlib import Path

from DataModelDict import DataModelDict as DM

class TestDataModelDict():

    @property
    def model(self):
        """DataModelDict.DataModelDict: A model for testing"""
        # Create an empty DataModel
        model = DM()

        # Build model element by element
        model['my-data-model'] = DM()

        model['my-data-model']['name'] = 'Demo'
        model['my-data-model']['author'] = 'Me'

        model['my-data-model']['process'] = DM()
        model['my-data-model']['process']['Instrument'] = DM()
        model['my-data-model']['process']['Instrument']['Name'] = 'Shiny Thing'
        model['my-data-model']['process']['Instrument']['Model'] = 'Newest Most\nExpensive'
        model['my-data-model']['process']['method'] = 'By the book'

        # Build multiple measurement elements
        model['my-data-model']['measurement'] = []
        measurement = DM([('temperature', DM([('value', 100),  ('unit', 'K')])),
                          ('length',      DM([('value', 1.24), ('unit', 'm')]))])
        model['my-data-model']['measurement'].append(measurement) 
        measurement = DM([('temperature', DM([('value', 200),  ('unit', 'K')])),
                          ('length',      DM([('value', 1.25), ('unit', 'm')]))])
        model['my-data-model']['measurement'].append(measurement) 
        measurement = DM([('temperature', DM([('value', 300),  ('unit', 'K')])),
                          ('length',      DM([('value', 1.26), ('unit', 'm')]))])
        model['my-data-model']['measurement'].append(measurement) 
        measurement = DM([('temperature', DM([('value', 400),  ('unit', 'K')])),
                          ('length',      DM([('value', 1.28), ('unit', 'm')]))])
        model['my-data-model']['measurement'].append(measurement) 
        measurement = DM([('temperature', DM([('value', 500),  ('unit', 'K')])),
                          ('length',      DM([('value', 1.29), ('unit', 'm')]))])
        model['my-data-model']['measurement'].append(measurement) 
        
        return model

    @property
    def jsoncompact(self):
        """str: Compact JSON representation of model"""
        return '{"my-data-model": {"name": "Demo", "author": "Me", "process": {"Instrument": {"Name": "Shiny Thing", "Model": "Newest Most\\nExpensive"}, "method": "By the book"}, "measurement": [{"temperature": {"value": 100, "unit": "K"}, "length": {"value": 1.24, "unit": "m"}}, {"temperature": {"value": 200, "unit": "K"}, "length": {"value": 1.25, "unit": "m"}}, {"temperature": {"value": 300, "unit": "K"}, "length": {"value": 1.26, "unit": "m"}}, {"temperature": {"value": 400, "unit": "K"}, "length": {"value": 1.28, "unit": "m"}}, {"temperature": {"value": 500, "unit": "K"}, "length": {"value": 1.29, "unit": "m"}}]}}'
    
    @property
    def jsonindent(self):
        """str: JSON representation of model with indent=4"""
        return '{\n    "my-data-model": {\n        "name": "Demo",\n        "author": "Me",\n        "process": {\n            "Instrument": {\n                "Name": "Shiny Thing",\n                "Model": "Newest Most\\nExpensive"\n            },\n            "method": "By the book"\n        },\n        "measurement": [\n            {\n                "temperature": {\n                    "value": 100,\n                    "unit": "K"\n                },\n                "length": {\n                    "value": 1.24,\n                    "unit": "m"\n                }\n            },\n            {\n                "temperature": {\n                    "value": 200,\n                    "unit": "K"\n                },\n                "length": {\n                    "value": 1.25,\n                    "unit": "m"\n                }\n            },\n            {\n                "temperature": {\n                    "value": 300,\n                    "unit": "K"\n                },\n                "length": {\n                    "value": 1.26,\n                    "unit": "m"\n                }\n            },\n            {\n                "temperature": {\n                    "value": 400,\n                    "unit": "K"\n                },\n                "length": {\n                    "value": 1.28,\n                    "unit": "m"\n                }\n            },\n            {\n                "temperature": {\n                    "value": 500,\n                    "unit": "K"\n                },\n                "length": {\n                    "value": 1.29,\n                    "unit": "m"\n                }\n            }\n        ]\n    }\n}'

    @property
    def xmlcompact(self):
        """str: Compact XML representation of model"""
        return '<?xml version="1.0" encoding="utf-8"?>\n<my-data-model><name>Demo</name><author>Me</author><process><Instrument><Name>Shiny Thing</Name><Model>Newest Most\\nExpensive</Model></Instrument><method>By the book</method></process><measurement><temperature><value>100</value><unit>K</unit></temperature><length><value>1.24</value><unit>m</unit></length></measurement><measurement><temperature><value>200</value><unit>K</unit></temperature><length><value>1.25</value><unit>m</unit></length></measurement><measurement><temperature><value>300</value><unit>K</unit></temperature><length><value>1.26</value><unit>m</unit></length></measurement><measurement><temperature><value>400</value><unit>K</unit></temperature><length><value>1.28</value><unit>m</unit></length></measurement><measurement><temperature><value>500</value><unit>K</unit></temperature><length><value>1.29</value><unit>m</unit></length></measurement></my-data-model>'

    @property
    def xmlindent(self):
        """str: XML representation of model with indent=4"""
        return '<?xml version="1.0" encoding="utf-8"?>\n<my-data-model>\n    <name>Demo</name>\n    <author>Me</author>\n    <process>\n        <Instrument>\n            <Name>Shiny Thing</Name>\n            <Model>Newest Most\\nExpensive</Model>\n        </Instrument>\n        <method>By the book</method>\n    </process>\n    <measurement>\n        <temperature>\n            <value>100</value>\n            <unit>K</unit>\n        </temperature>\n        <length>\n            <value>1.24</value>\n            <unit>m</unit>\n        </length>\n    </measurement>\n    <measurement>\n        <temperature>\n            <value>200</value>\n            <unit>K</unit>\n        </temperature>\n        <length>\n            <value>1.25</value>\n            <unit>m</unit>\n        </length>\n    </measurement>\n    <measurement>\n        <temperature>\n            <value>300</value>\n            <unit>K</unit>\n        </temperature>\n        <length>\n            <value>1.26</value>\n            <unit>m</unit>\n        </length>\n    </measurement>\n    <measurement>\n        <temperature>\n            <value>400</value>\n            <unit>K</unit>\n        </temperature>\n        <length>\n            <value>1.28</value>\n            <unit>m</unit>\n        </length>\n    </measurement>\n    <measurement>\n        <temperature>\n            <value>500</value>\n            <unit>K</unit>\n        </temperature>\n        <length>\n            <value>1.29</value>\n            <unit>m</unit>\n        </length>\n    </measurement>\n</my-data-model>'

    def test_json(self, tmpdir):
        """Test model <-> JSON conversions"""
        model = self.model
        assert model.json() == self.jsoncompact
        assert model.json(indent=4) == self.jsonindent

        model = DM(self.jsoncompact)
        assert model.json() == self.jsoncompact
        assert model.json(indent=4) == self.jsonindent

        model = DM(self.jsonindent)
        assert model.json() == self.jsoncompact
        assert model.json(indent=4) == self.jsonindent

        jsonfile = Path(tmpdir, 'model.json')
        
        with open(jsonfile, 'w') as f:
            model.json(fp=f)
        with open(jsonfile) as f:
            assert f.read() == self.jsoncompact

        with open(jsonfile, 'w') as f:
            model.json(fp=f, indent=4)
        with open(jsonfile) as f:
            assert f.read() == self.jsonindent

    def test_xml(self, tmpdir):
        """Test model <-> XML conversions"""
        model = self.model
        assert model.xml() == self.xmlcompact
        assert model.xml(indent=4) == self.xmlindent

        model = DM(self.xmlcompact)
        assert model.xml() == self.xmlcompact
        assert model.xml(indent=4) == self.xmlindent

        model = DM(self.xmlindent)
        assert model.xml() == self.xmlcompact
        assert model.xml(indent=4) == self.xmlindent

        xmlfile = Path(tmpdir, 'model.xml')
        
        with open(xmlfile, 'w') as f:
            model.xml(fp=f)
        with open(xmlfile) as f:
            assert f.read() == self.xmlcompact

        with open(xmlfile, 'w') as f:
            model.xml(fp=f, indent=4)
        with open(xmlfile) as f:
            assert f.read() == self.xmlindent

    def test_getset(self):
        model = self.model

        path = ['my-data-model', 'process', 'Instrument', 'Name']
        assert model['my-data-model']['process']['Instrument']['Name'] == 'Shiny Thing'
        assert model[path] == 'Shiny Thing'
    
        # Change the value using path list and test
        model[path] = 'Scuffed-Up Thing'
        assert model['my-data-model']['process']['Instrument']['Name'] == 'Scuffed-Up Thing'
        assert model[path] == 'Scuffed-Up Thing'
        
        # Change the value directly and test 
        model['my-data-model']['process']['Instrument']['Name'] = 'Shiny Thing'
        assert model['my-data-model']['process']['Instrument']['Name'] == 'Shiny Thing'
        assert model[path] == 'Shiny Thing'
    
    def test_find(self):
        model = self.model
        assert model.find('Name') == 'Shiny Thing'

        measurements = model.finds('measurement')
        assert len(measurements) == 5

        t = 0
        for measurement in model.iterfinds('measurement'):
            t += 100
            assert measurement['temperature']['value'] == t
            
        # Search for measurement where temp is 300
        temp = DM([('value', 300), ('unit', 'K')])
        val = model.find('measurement', yes={'temperature':temp})['length']['value']
        assert val == 1.26

        # Search for measurements where temp is not 200
        temp = DM([('value', 200), ('unit', 'K')])
        measurements = model.finds('measurement', no={'temperature':temp})
        assert len(measurements) == 4

    def test_path(self):
        model = self.model
        path = model.path('Name')
        assert '.'.join(path) == 'my-data-model.process.Instrument.Name'
        assert model[path] == 'Shiny Thing'

        temp = DM([('value', 200), ('unit', 'K')])
        measurement_paths = model.paths('measurement', no={'temperature':temp})
        assert measurement_paths[0] == ['my-data-model', 'measurement', 0]
        assert measurement_paths[1] == ['my-data-model', 'measurement', 2]
        assert measurement_paths[2] == ['my-data-model', 'measurement', 3]
        assert measurement_paths[3] == ['my-data-model', 'measurement', 4]

    def test_append(self):
        model = DM()
        model['test'] = DM()
        
        # Check fields that don't exist
        assert model['test'].get('ordinal', None) is None
        assert model['test'].aslist('ordinal') == []
 
        # Append a value and check again
        model['test'].append('ordinal', 'first')
        assert model['test'].get('ordinal', None) == 'first'
        assert model['test'].aslist('ordinal') == ['first']

        # Append a value and check again
        model['test'].append('ordinal', 'second')
        assert model['test'].get('ordinal', None) == ['first', 'second']
        assert model['test'].aslist('ordinal') == ['first', 'second']

        # Append a value and check again
        model['test'].append('ordinal', 'third')
        assert model['test'].get('ordinal', None) == ['first', 'second', 'third']
        assert model['test'].aslist('ordinal') == ['first', 'second', 'third']

    def test_move(self):
        # Move uses different options based on high index, low index
        # And before/after index identification depends on left/right shifts

        # Create simple model for testing
        model = DM('{"a":"a","b":"b","c":"c","d":"d","e":"e","f":"f","g":"g","h":"h","i":"i"}')

        # move by index to low i
        model.move('f', index=1)
        model2 = DM('{"a":"a","f":"f","b":"b","c":"c","d":"d","e":"e","g":"g","h":"h","i":"i"}')
        assert model == model2

        # move by index to high and negative i
        model.move('b', index=-2)
        model2 = DM('{"a":"a","f":"f","c":"c","d":"d","e":"e","g":"g","h":"h","b":"b","i":"i"}')
        assert model == model2

        # move before to the left
        model.move('h', before='c')
        model2 = DM('{"a":"a","f":"f","h":"h","c":"c","d":"d","e":"e","g":"g","b":"b","i":"i"}')
        assert model == model2

        # move before to the right
        model.move('a', before='g')
        model2 = DM('{"f":"f","h":"h","c":"c","d":"d","e":"e","a":"a","g":"g","b":"b","i":"i"}')
        assert model == model2
        
        # move after to the left
        model.move('g', after='f')
        model2 = DM('{"f":"f","g":"g","h":"h","c":"c","d":"d","e":"e","a":"a","b":"b","i":"i"}')
        assert model == model2

        # move after to the right
        model.move('h', after='b')
        model2 = DM('{"f":"f","g":"g","c":"c","d":"d","e":"e","a":"a","b":"b","h":"h","i":"i"}')
        assert model == model2

        # Check errors
        with raises(KeyError):
            model.move('h', after='z')
        with raises(KeyError):
            model.move('h', before='z')
        with raises(IndexError):
            model.move('h', index=9)
        with raises(IndexError):
            model.move('h', index=-10)

    def test_append_with_move(self):
        # Create simple model for testing
        model = DM('{"a":"a","b":"b","c":"c","d":"d","e":"e","f":"f","g":"g","h":"h","i":"i"}')

        # Append new keys with known references
        model.append('j', 'j', before='b')
        model2 = DM('{"a":"a","j":"j","b":"b","c":"c","d":"d","e":"e","f":"f","g":"g","h":"h","i":"i"}')
        assert model == model2

        model.append('k', 'k', after='g')
        model2 = DM('{"a":"a","j":"j","b":"b","c":"c","d":"d","e":"e","f":"f","g":"g","k":"k","h":"h","i":"i"}')
        assert model == model2

        # Append new keys with unknown references
        model.append('l', 'l', before='z')
        model2 = DM('{"a":"a","j":"j","b":"b","c":"c","d":"d","e":"e","f":"f","g":"g","k":"k","h":"h","i":"i","l":"l"}')
        assert model == model2

        model.append('m', 'm', after='z')
        model2 = DM('{"a":"a","j":"j","b":"b","c":"c","d":"d","e":"e","f":"f","g":"g","k":"k","h":"h","i":"i","l":"l","m":"m"}')
        assert model == model2

        # Append to old keys and move based on references
        model.append('j', 'j', before='l')
        model2 = DM('{"a":"a","b":"b","c":"c","d":"d","e":"e","f":"f","g":"g","k":"k","h":"h","i":"i","j":["j","j"],"l":"l","m":"m"}')
        assert model == model2

        model.append('k', 'k', after='j')
        model2 = DM('{"a":"a","b":"b","c":"c","d":"d","e":"e","f":"f","g":"g","h":"h","i":"i","j":["j","j"],"k":["k","k"],"l":"l","m":"m"}')
        assert model == model2

    def test_reorder(self):
        # Create simple model for testing
        model = DM('{"a":"a","b":"b","c":"c","d":"d","e":"e","f":"f","g":"g","h":"h","i":"i"}')

        # Specify reorder keys with extras and missing values
        model.reorder(['a','c','e','g','i','k','l','n'])

        # Check final order: 'a', 'c', 'e', 'g' reordered, others ignored
        model2 = DM('{"a":"a","c":"c","e":"e","g":"g","i":"i","b":"b","d":"d","f":"f","h":"h"}')
        assert model == model2
    def test_leading_blank_lines(self, tmpdir):
        """Test format detection when content starts with blank lines"""
        # The format sniffer reads past blank lines before looking at the first
        # character, so a file that starts with a newline still loads.
        assert DM('\n' + self.jsoncompact) == self.model
        assert DM('\n\n  \n' + self.jsoncompact) == self.model
        # an XML declaration cannot be preceded by whitespace, so use a bare
        # element to check the sniffer reaches '<'
        assert DM('\n<a>1</a>') == DM('<a>1</a>')

        jsonfile = Path(tmpdir, 'leading-blank.json')
        with open(jsonfile, 'w', encoding='UTF-8') as f:
            f.write('\n' + self.jsoncompact)
        assert DM(jsonfile) == self.model

    def test_unidentifiable_content(self):
        """Test that content with no format raises ValueError, not IndexError"""
        with raises(ValueError):
            DM('')
        with raises(ValueError):
            DM('   \n  \n')
