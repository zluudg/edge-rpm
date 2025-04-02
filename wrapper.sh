#! /bin/bash
rpmlint SPECS/tapir-edge.spec
spectool --get-file SPECS/tapir-edge.spec --directory SOURCES
rpmbuild -ba SPECS/tapir-edge.spec

