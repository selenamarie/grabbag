#!/usr/bin/python

import StringIO
import os
import shutil
import tempfile
import time

import boto

# Read developer keys from the ~/.boto config file.
config = boto.config

# URI scheme for Google Storage.
GOOGLE_STORAGE = 'gs'
# URI scheme for accessing local files.
LOCAL_FILE = 'file'

now = time.time()
CHESNOK_BUCKET = 'chesnok-%d' % now

for name in (CHESNOK_BUCKET,):
	# Instantiate a BucketStorageUri object.
	print name
	uri = boto.storage_uri(name, GOOGLE_STORAGE)
	print uri
	# Try to create the bucket.
	try:
		uri.create_bucket()
		print 'Successfully created bucket "%s"' % name
	except boto.exception.StorageCreateError, e:
		print 'Failed to create bucket:', e

# Upload deez files
tempfiles = { 'access.log': 'chesnok.com access logs' }
for filename, descr in tempfiles.iteritems():
	contents = file(filename, 'r')
	print GOOGLE_STORAGE + '/' + CHESNOK_BUCKET + '/' + filename
	dst_uri = boto.storage_uri( CHESNOK_BUCKET + '/' + filename, GOOGLE_STORAGE)
	# The key-related functions are a consequence of boto's
	# interoperability with Amazon S3 (which employs the
	# concept of a key mapping to contents).
	try:
		dst_uri.new_key().set_contents_from_file(contents)
		print 'Successfully created "%s/%s"' % (dst_uri.bucket_name, dst_uri.object_name)
	except boto.exception.GSResponseError, e:
		print 'Failed to create new key:', e

	contents.close()

uri = boto.storage_uri(CHESNOK_BUCKET, GOOGLE_STORAGE)
for obj in uri.get_bucket():
  print '%s://%s/%s' % (uri.scheme, uri.bucket_name, obj.name)
  print '  "%s"' % obj.get_contents_as_string()
