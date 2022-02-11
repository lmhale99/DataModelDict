# coding: utf-8

# Standard Python libraries
from pathlib import Path
import io

# https://docs.pytest.org/
from pytest import raises

from DataModelDict import uber_open_rmode

class Test_uber_open_rmode():

    @property
    def content(self):
        """bytes: File contents for testing"""
        return b"This is the contents of my file."

    def test_bytes(self):
        """Test that bytes is opened as BytesIO"""
        # Read bytes content
        with uber_open_rmode(self.content) as f:
            assert isinstance(f, io.BytesIO)
            content = f.read()

        # Check value of content and that f is closed
        assert content == self.content
        assert f.closed

    def test_str(self):
        """Test that str is encoded and opened as BytesIO"""
        
        # Convert bytes content to str
        str_content = self.content.decode() 
        
        # Read str content as bytes
        with uber_open_rmode(str_content) as f:
            assert isinstance(f, io.BytesIO)
            content = f.read()
        
        # Check value of content and that f is closed
        assert content == self.content
        assert f.closed

    def test_file(self, tmpdir):
        """Test that files are read in binary mode"""

        # Save content to a file in a temp directory
        filepath = Path(str(tmpdir), 'content.txt')
        with open(filepath, 'wb') as f:
            f.write(self.content)
        
        # Test reading from filepath
        with uber_open_rmode(filepath) as f:
            assert 'b' in f.mode
            content = f.read()
        
        # Check value of content and that f is closed
        assert content == self.content
        assert f.closed

        # Check that bad file paths throw errors
        with raises(FileNotFoundError):
            badpath = Path(tmpdir, 'DOES NOT EXIST.txt')
            with uber_open_rmode(badpath) as f:
                content = f.read()

    def test_stream_objs(self):
        """Test that BytesIO objects are passed through"""
        
        # Test BytesIO around content
        bstream = io.BytesIO(self.content)
        with uber_open_rmode(bstream) as f:
            assert isinstance(f, io.BytesIO)
            content = f.read()

        # Check value of content and that f is not closed
        assert content == self.content
        assert not f.closed
        f.close()

        # Test StringIO throws error
        tstream = io.StringIO(self.content.decode())
        with raises(ValueError):
            with uber_open_rmode(tstream) as f:
                content = f.read()

    def test_file_objs(self, tmpdir):
        """Test that file objects in rb mode are passed through"""
        
        # Save content to a file in a temp directory
        filepath = Path(str(tmpdir), 'content.txt')
        with open(filepath, 'wb') as f:
            f.write(self.content)

        # Test file open in rb mode
        with open(filepath, 'rb') as openf:
            with uber_open_rmode(openf) as f:
                content = f.read()
            
            # Check value of content and that f is not closed
            assert content == self.content
            assert not f.closed

        # Test that error is thrown for file in rt mode
        with open(filepath, 'rt') as openf:
            with raises(ValueError):
                with uber_open_rmode(openf) as f:
                    content = f.read()

    def test_bad_types(self):
        """Test for a TypeError if other junk is given"""
        with raises(TypeError):
            with uber_open_rmode(132498) as f:
                content = f.read()