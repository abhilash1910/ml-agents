# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mlagents/envs/communicator_objects/custom_reset_parameters.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mlagents/envs/communicator_objects/custom_reset_parameters.proto',
  package='communicator_objects',
  syntax='proto3',
  serialized_pb=_b('\n@mlagents/envs/communicator_objects/custom_reset_parameters.proto\x12\x14\x63ommunicator_objects\"\x1c\n\x1a\x43ustomResetParametersProtoB\x1f\xaa\x02\x1cMLAgents.CommunicatorObjectsb\x06proto3')
)




_CUSTOMRESETPARAMETERSPROTO = _descriptor.Descriptor(
  name='CustomResetParametersProto',
  full_name='communicator_objects.CustomResetParametersProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=90,
  serialized_end=118,
)

DESCRIPTOR.message_types_by_name['CustomResetParametersProto'] = _CUSTOMRESETPARAMETERSPROTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CustomResetParametersProto = _reflection.GeneratedProtocolMessageType('CustomResetParametersProto', (_message.Message,), dict(
  DESCRIPTOR = _CUSTOMRESETPARAMETERSPROTO,
  __module__ = 'mlagentsenvs.envs.communicator_objects.custom_reset_parameters_pb2'
  # @@protoc_insertion_point(class_scope:communicator_objects.CustomResetParametersProto)
  ))
_sym_db.RegisterMessage(CustomResetParametersProto)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\252\002\034MLAgents.CommunicatorObjects'))
# @@protoc_insertion_point(module_scope)