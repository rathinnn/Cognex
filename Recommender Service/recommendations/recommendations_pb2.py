# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: recommendations.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15recommendations.proto\"1\n\x0b\x46indRequest\x12\r\n\x05skill\x18\x01 \x01(\t\x12\x13\n\x0bmax_results\x18\x02 \x01(\x05\" \n\x12UserRecommendation\x12\n\n\x02id\x18\x01 \x01(\x05\"F\n\x16RecommendationResponse\x12,\n\x0frecommendations\x18\x01 \x03(\x0b\x32\x13.UserRecommendation\"(\n\nPutRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0e\n\x06skills\x18\x02 \x03(\t\"\x1d\n\x0bPutResponse\x12\x0e\n\x06status\x18\x01 \x01(\x05\x32\x45\n\x0fRecommendations\x12\x32\n\tRecommend\x12\x0c.FindRequest\x1a\x17.RecommendationResponse2.\n\nPutService\x12 \n\x03Put\x12\x0b.PutRequest\x1a\x0c.PutResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'recommendations_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _FINDREQUEST._serialized_start=25
  _FINDREQUEST._serialized_end=74
  _USERRECOMMENDATION._serialized_start=76
  _USERRECOMMENDATION._serialized_end=108
  _RECOMMENDATIONRESPONSE._serialized_start=110
  _RECOMMENDATIONRESPONSE._serialized_end=180
  _PUTREQUEST._serialized_start=182
  _PUTREQUEST._serialized_end=222
  _PUTRESPONSE._serialized_start=224
  _PUTRESPONSE._serialized_end=253
  _RECOMMENDATIONS._serialized_start=255
  _RECOMMENDATIONS._serialized_end=324
  _PUTSERVICE._serialized_start=326
  _PUTSERVICE._serialized_end=372
# @@protoc_insertion_point(module_scope)
